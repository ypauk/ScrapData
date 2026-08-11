#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для Infinite Scroll (`app/infinite_scroll.py`).

Проверяют (без реального запуска браузера, через мокирование
`PlaywrightEngine`):
* остановку по причине "disabled" (когда компонент выключен конфигурацией);
* остановку по отсутствию нового контента (no_new_content);
* остановку по лимиту итераций (max_scrolls);
* остановку по лимиту высоты страницы (max_height);
* остановку по целевому количеству элементов (target_count);
* остановку по таймауту (timeout);
* остановку по пользовательскому stop_callback (custom_callback);
* graceful-обработку сбоя Playwright во время прокрутки (error), без
  прерывания всего процесса;
* делегирование пауз Delay Manager между итерациями.

Запуск (из директории starter-project):
    python -m unittest tests.test_infinite_scroll
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app.infinite_scroll import InfiniteScroll, ScrollStopReason
from app.playwright_engine import PlaywrightEngineError


def _make_mock_engine(heights, evaluate_side_effect=None):
    """
    Строит мок PlaywrightEngine.

    Args:
        heights (list[int]): Последовательность значений, возвращаемых
            при вызове `evaluate("document.body.scrollHeight")` —
            первое значение — начальная высота, остальные — высота
            после каждого скролла.
        evaluate_side_effect: Если передан, полностью переопределяет
            поведение `evaluate()` (для симуляции сбоев).
    """
    engine = MagicMock()
    heights_iter = iter(heights)

    if evaluate_side_effect is not None:
        engine.evaluate.side_effect = evaluate_side_effect
    else:
        def _evaluate(script, *args):
            if "scrollHeight" in script and "scrollTo" not in script and "scrollBy" not in script:
                return next(heights_iter)
            return None

        engine.evaluate.side_effect = _evaluate

    return engine


class InfiniteScrollTestCase(unittest.TestCase):
    """Базовый класс: мокирует DelayManager, чтобы тесты не спали реально."""

    def setUp(self) -> None:
        self._delay_patcher = patch("app.infinite_scroll.DelayManager")
        self.mock_delay = self._delay_patcher.start()

    def tearDown(self) -> None:
        self._delay_patcher.stop()


class TestDisabled(InfiniteScrollTestCase):
    """Проверка остановки, когда компонент выключен конфигурацией."""

    def test_disabled_returns_immediately(self):
        engine = _make_mock_engine([1000])
        result = InfiniteScroll.scroll(engine, enabled=False)

        self.assertEqual(result.stop_reason, ScrollStopReason.DISABLED.value)
        self.assertEqual(result.scrolls_performed, 0)
        engine.evaluate.assert_not_called()


class TestNoNewContent(InfiniteScrollTestCase):
    """Проверка остановки по отсутствию нового контента."""

    def test_stops_after_no_new_content_streak(self):
        # Начальная высота 1000, после первого скролла высота растет до 2000,
        # затем перестает расти (2000, 2000, 2000) -> остановка по streak=3.
        engine = _make_mock_engine([1000, 2000, 2000, 2000, 2000])
        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=3,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.NO_NEW_CONTENT.value)
        self.assertEqual(result.scrolls_performed, 4)


class TestMaxScrolls(InfiniteScrollTestCase):
    """Проверка остановки по лимиту количества итераций."""

    def test_stops_after_max_scrolls(self):
        # Высота растет бесконечно, но лимит итераций должен остановить цикл раньше.
        heights = [1000] + [1000 + i * 100 for i in range(1, 20)]
        engine = _make_mock_engine(heights)
        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=5,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=100,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.MAX_SCROLLS.value)
        self.assertEqual(result.scrolls_performed, 5)


class TestMaxHeight(InfiniteScrollTestCase):
    """Проверка остановки по лимиту высоты страницы."""

    def test_stops_after_max_height_reached(self):
        heights = [1000, 3000, 6000]
        engine = _make_mock_engine(heights)
        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=5000,
            max_no_new_content_attempts=100,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.MAX_HEIGHT.value)
        self.assertEqual(result.scrolls_performed, 2)


class TestTargetItemCount(InfiniteScrollTestCase):
    """Проверка остановки по целевому количеству элементов."""

    def test_stops_when_target_item_count_reached(self):
        engine = MagicMock()
        heights_iter = iter([1000, 2000, 3000, 4000])
        counts_iter = iter([2, 5, 10])  # первый вызов count_callback (до цикла), затем после каждого скролла

        def _evaluate(script, *args):
            if "scrollHeight" in script and "scrollTo" not in script:
                return next(heights_iter)
            return None

        engine.evaluate.side_effect = _evaluate

        def count_callback(_engine):
            return next(counts_iter)

        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=100,
            target_item_count=10,
            count_callback=count_callback,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.TARGET_COUNT.value)
        self.assertEqual(result.final_item_count, 10)


class TestTimeout(InfiniteScrollTestCase):
    """Проверка остановки по общему таймауту цикла."""

    def test_stops_on_timeout(self):
        engine = _make_mock_engine([1000] + [1000 + i * 100 for i in range(1, 50)])

        call_count = {"n": 0}
        real_monotonic = __import__("time").monotonic

        with patch("app.infinite_scroll.time.monotonic") as mock_monotonic:
            # Первый вызов — старт (0.0), затем каждый следующий вызов увеличивает
            # время, чтобы быстро сработал timeout=5 без реального ожидания.
            def _tick():
                call_count["n"] += 1
                return call_count["n"] * 3.0

            mock_monotonic.side_effect = _tick

            result = InfiniteScroll.scroll(
                engine,
                enabled=True,
                max_scrolls=0,
                timeout_seconds=5,
                max_page_height=0,
                max_no_new_content_attempts=100,
            )

        self.assertEqual(result.stop_reason, ScrollStopReason.TIMEOUT.value)


class TestCustomStopCallback(InfiniteScrollTestCase):
    """Проверка остановки по пользовательскому stop_callback."""

    def test_stops_when_custom_callback_returns_true(self):
        engine = _make_mock_engine([1000, 2000, 3000, 4000, 5000])

        def stop_callback(state):
            return state.iteration >= 2

        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=100,
            stop_callback=stop_callback,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.CUSTOM_CALLBACK.value)
        self.assertEqual(result.scrolls_performed, 2)


class TestErrorHandling(InfiniteScrollTestCase):
    """Проверка graceful-обработки сбоев Playwright во время прокрутки."""

    def test_scroll_failure_stops_gracefully_without_raising(self):
        engine = MagicMock()

        def _evaluate(script, *args):
            if "scrollHeight" in script and "scrollTo" not in script:
                return 1000
            if "scrollTo" in script:
                raise PlaywrightEngineError("сбой скролла")
            return None

        engine.evaluate.side_effect = _evaluate

        result = InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=100,
        )

        self.assertEqual(result.stop_reason, ScrollStopReason.ERROR.value)
        self.assertEqual(result.scrolls_performed, 0)

    def test_initial_height_failure_stops_gracefully(self):
        engine = MagicMock()
        engine.evaluate.side_effect = PlaywrightEngineError("сбой получения высоты")

        result = InfiniteScroll.scroll(engine, enabled=True)

        self.assertEqual(result.stop_reason, ScrollStopReason.ERROR.value)
        self.assertEqual(result.scrolls_performed, 0)


class TestDelayIntegration(InfiniteScrollTestCase):
    """Проверка делегирования пауз между скроллами Delay Manager."""

    def test_wait_random_called_by_default(self):
        engine = _make_mock_engine([1000, 2000, 2000, 2000])
        InfiniteScroll.scroll(
            engine,
            enabled=True,
            max_scrolls=0,
            timeout_seconds=0,
            max_page_height=0,
            max_no_new_content_attempts=2,
        )
        self.assertTrue(self.mock_delay.wait_random.called)
        self.mock_delay.wait_fixed.assert_not_called()


if __name__ == "__main__":
    unittest.main()
