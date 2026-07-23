#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для Pagination (app/pagination.py).

Все тесты используют простые мок-функции fetch_callback вместо реальных
запросов/браузера — компонент engine-независим по конструкции, поэтому
тестируется без RequestsEngine/PlaywrightEngine.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pagination import (
    PageContext,
    PageFetchResult,
    Paginator,
    PaginationError,
    PaginationStopReason,
    PaginationType,
)


class TestPaginationUrlStrategy(unittest.TestCase):
    """Тесты стратегии URL-пагинации (?page=2,3,4...)."""

    def test_stops_at_max_pages(self):
        calls = []

        def fetch(ctx: PageContext) -> PageFetchResult:
            calls.append(ctx.params["page"])
            return PageFetchResult(content=f"page-{ctx.params['page']}", item_count=5)

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=3,
            page_param="page",
            start_page=1,
            page_step=1,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(calls, [1, 2, 3])
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.MAX_PAGES.value)
        self.assertEqual(results[-1].pages_fetched, 3)

    def test_stops_on_no_items(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            count = 5 if ctx.params["page"] < 3 else 0
            return PageFetchResult(content="x", item_count=count)

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            page_param="page",
            start_page=1,
            page_step=1,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.NO_ITEMS.value)

    def test_stops_on_has_next_false(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            is_last = ctx.params["page"] == 2
            return PageFetchResult(content="x", has_next=not is_last)

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            page_param="page",
            start_page=1,
            page_step=1,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.LAST_PAGE.value)

    def test_page_step_and_start_page(self):
        seen_pages = []

        def fetch(ctx: PageContext) -> PageFetchResult:
            seen_pages.append(ctx.params["page"])
            return PageFetchResult(content="x")

        Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=3,
            page_param="page",
            start_page=10,
            page_step=5,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(seen_pages, [10, 15, 20])


class TestPaginationOffsetStrategy(unittest.TestCase):
    """Тесты стратегии Offset-пагинации (?offset=20,40,60...)."""

    def test_offset_increments_correctly(self):
        seen_offsets = []

        def fetch(ctx: PageContext) -> PageFetchResult:
            seen_offsets.append(ctx.params["offset"])
            return PageFetchResult(content="x")

        Paginator.paginate(
            fetch, PaginationType.OFFSET,
            url="https://example.com/items",
            max_pages=3,
            offset_param="offset",
            start_offset=0,
            offset_step=20,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(seen_offsets, [0, 20, 40])


class TestPaginationDuplicateDetection(unittest.TestCase):
    """Тесты обнаружения дублирующихся страниц по dedupe_key."""

    def test_stops_on_duplicate(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            # Всегда возвращает одинаковый dedupe_key -> дубликат на 2-й странице
            return PageFetchResult(content="x", dedupe_key="same-key")

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            detect_duplicates=True,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.DUPLICATE_PAGE.value)

    def test_duplicate_detection_disabled_by_default_does_not_stop_early(self):
        """При detect_duplicates=False одинаковый dedupe_key не должен останавливать цикл раньше max_pages."""

        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content="x", dedupe_key="same-key")

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=3,
            detect_duplicates=False,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.MAX_PAGES.value)


class TestPaginationCustomCallback(unittest.TestCase):
    """Тесты пользовательского stop_callback."""

    def test_stop_callback_triggers_stop(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content=ctx.page_number)

        def stop_callback(page_number, content):
            return page_number >= 2

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            stop_callback=stop_callback,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.CUSTOM_CALLBACK.value)

    def test_stop_callback_exception_is_handled_gracefully(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content="x")

        def bad_stop_callback(page_number, content):
            raise RuntimeError("boom")

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            stop_callback=bad_stop_callback,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.ERROR.value)


class TestPaginationErrorHandling(unittest.TestCase):
    """Тесты graceful-обработки сбоев fetch_callback — не должны прерывать процесс."""

    def test_fetch_callback_exception_stops_gracefully(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            if ctx.page_number == 1:
                return PageFetchResult(content="ok")
            raise ConnectionError("network down")

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.ERROR.value)

    def test_invalid_fetch_result_type_stops_gracefully(self):
        def fetch(ctx: PageContext):
            return "not a PageFetchResult"

        results = Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=0,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 0)


class TestPaginationValidation(unittest.TestCase):
    """Тесты валидации обязательных аргументов для каждой стратегии."""

    def test_url_strategy_requires_url(self):
        def fetch(ctx):
            return PageFetchResult(content="x")

        with self.assertRaises(PaginationError):
            Paginator.paginate(fetch, PaginationType.URL)

    def test_next_button_requires_selector(self):
        def fetch(ctx):
            return PageFetchResult(content="x")

        with self.assertRaises(PaginationError):
            Paginator.paginate(fetch, PaginationType.NEXT_BUTTON)

    def test_custom_requires_generator(self):
        def fetch(ctx):
            return PageFetchResult(content="x")

        with self.assertRaises(PaginationError):
            Paginator.paginate(fetch, PaginationType.CUSTOM, url="https://example.com")

    def test_string_pagination_type_is_normalized(self):
        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content="x")

        results = Paginator.paginate(
            fetch, "url",
            url="https://example.com/items",
            max_pages=1,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )
        self.assertEqual(len(results), 1)


class TestPaginationNextButtonStrategy(unittest.TestCase):
    """Тесты стратегии NEXT_BUTTON (Playwright)."""

    def test_next_button_context_flags_use_next_button(self):
        seen_contexts = []

        def fetch(ctx: PageContext) -> PageFetchResult:
            seen_contexts.append(ctx.use_next_button)
            is_last = ctx.page_number >= 2
            return PageFetchResult(content="x", has_next=not is_last)

        results = Paginator.paginate(
            fetch, PaginationType.NEXT_BUTTON,
            url="https://example.com",
            next_button_selector="a.next",
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertTrue(all(seen_contexts))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.LAST_PAGE.value)

    def test_click_next_button_returns_false_when_selector_missing(self):
        from app.playwright_engine import PlaywrightEngineError

        mock_engine = MagicMock()
        mock_engine.page.wait_for_selector.side_effect = PlaywrightEngineError("not found")

        result = Paginator.click_next_button(mock_engine, "a.missing")
        self.assertFalse(result)

    def test_click_next_button_returns_true_on_success(self):
        mock_engine = MagicMock()
        mock_element = MagicMock()
        mock_engine.page.wait_for_selector.return_value = mock_element
        mock_engine.page.evaluate.return_value = False  # not disabled

        result = Paginator.click_next_button(mock_engine, "a.next")
        self.assertTrue(result)
        mock_element.click.assert_called_once()
        mock_engine.wait_for_load.assert_called_once_with("networkidle")

    def test_click_next_button_returns_false_when_disabled(self):
        mock_engine = MagicMock()
        mock_element = MagicMock()
        mock_engine.page.wait_for_selector.return_value = mock_element
        mock_engine.page.evaluate.return_value = True  # disabled

        result = Paginator.click_next_button(mock_engine, "a.next")
        self.assertFalse(result)
        mock_element.click.assert_not_called()


class TestPaginationCustomStrategy(unittest.TestCase):
    """Тесты стратегии CUSTOM (полностью делегированной вызывающему коду)."""

    def test_custom_generator_drives_pagination(self):
        def generator(page_number, prev_context):
            if page_number > 3:
                return None
            return PageContext(
                url=f"https://example.com/custom/{page_number}",
                page_number=page_number,
                pagination_type=PaginationType.CUSTOM,
            )

        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content=ctx.url)

        results = Paginator.paginate(
            fetch, PaginationType.CUSTOM,
            url="https://example.com",
            custom_context_generator=generator,
            delay_mode="fixed",
            delay_fixed_seconds=0,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(results[-1].stop_reason, PaginationStopReason.LAST_PAGE.value)


class TestPaginationDelayIntegration(unittest.TestCase):
    """Проверяет, что пауза между страницами делегируется Delay Manager."""

    @patch("app.pagination.DelayManager.wait_fixed")
    def test_uses_delay_manager_fixed(self, mock_wait_fixed):
        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content="x")

        Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=2,
            delay_mode="fixed",
            delay_fixed_seconds=0.01,
        )

        mock_wait_fixed.assert_called_once_with(0.01)

    @patch("app.pagination.DelayManager.wait_random")
    def test_uses_delay_manager_random(self, mock_wait_random):
        def fetch(ctx: PageContext) -> PageFetchResult:
            return PageFetchResult(content="x")

        Paginator.paginate(
            fetch, PaginationType.URL,
            url="https://example.com/items",
            max_pages=2,
            delay_mode="random",
            delay_min_seconds=0.01,
            delay_max_seconds=0.02,
        )

        mock_wait_random.assert_called_once_with(0.01, 0.02)


if __name__ == "__main__":
    unittest.main()
