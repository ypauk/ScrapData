#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Infinite Scroll.

Централизованный компонент бесконечного скроллинга для JS-сайтов,
подгружающих контент динамически при прокрутке страницы (см.
`framework/ROADMAP.md`, Milestone 4).

Infinite Scroll — единственная точка, через которую скрапер-модули
должны запускать цикл прокрутки страницы. Он НЕ содержит логики
парсинга/экспорта/логина/пагинации и НЕ знает о селекторах конкретных
сайтов — единственное, что он умеет, это скроллить страницу и
останавливаться по одному из настраиваемых условий:

    Infinite Scroll
            │
            ▼
    PlaywrightEngine.evaluate() / .wait_for_load()  ─────────────┐
            │                                                     │
     ┌──────┼─────────┐                                           │
     ▼      ▼          ▼                                          ▼
    Delay  Logging  Configuration                          (PlaywrightEngine
    Manager          Manager                                 остаётся единственной
                                                               точкой навигации/JS)

Infinite Scroll:

* выполняет прокрутку страницы через `PlaywrightEngine.evaluate()` —
  не дублирует логику запуска браузера/навигации (это ответственность
  Playwright Engine, `app/playwright_engine.py`);
* делает паузу между скроллами через `DelayManager.wait_fixed()`/
  `wait_random()` (Delay Manager, `app/delay_manager.py`) — не реализует
  собственный `time.sleep()`;
* поддерживает несколько независимых условий остановки одновременно
  (срабатывает то, которое выполнилось первым): отсутствие нового
  контента, лимит итераций, лимит высоты страницы, целевое количество
  элементов, таймаут, пользовательский callback;
* использует централизованную функцию логирования `app.utils.log_message`
  для старта/завершения цикла, числа итераций и причины остановки
  (без избыточного лога на каждой итерации);
* оборачивает все ожидаемые сбои Playwright (полученные как
  `PlaywrightEngineError` от Playwright Engine) — одна неудачная
  прокрутка не прерывает весь процесс скрапинга, цикл просто
  останавливается с причиной `error`, а вызывающий код продолжает
  работу с уже загруженным контентом;
* берет все параметры поведения (лимиты, задержки, флаги) из
  Configuration Manager (`app/config.py`) с возможностью точечного
  переопределения аргументами метода — без хардкода значений.

Infinite Scroll НЕ парсит HTML, НЕ извлекает данные, НЕ выполняет логин,
НЕ экспортирует данные и НЕ содержит селекторов конкретных сайтов —
опциональный `item_selector`/`count_callback` передается вызывающим
кодом извне и используется исключительно для подсчета количества
элементов (для условия остановки "target_item_count"), а не для
извлечения самих данных.
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

from app import config
from app.delay_manager import DelayManager
from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError
from app.utils import log_message


class InfiniteScrollError(Exception):
    """
    Единое исключение Infinite Scroll для непредвиденных сбоев конфигурации
    (например, некорректных аргументов), не связанных с ожидаемыми
    условиями остановки цикла скроллинга.

    Сбои самого Playwright во время скроллинга НЕ поднимаются как это
    исключение — они обрабатываются graceful (см. `ScrollStopReason.ERROR`),
    чтобы одна неудачная прокрутка не прерывала весь процесс скрапинга.
    """


class ScrollStopReason(str, Enum):
    """Причина остановки цикла бесконечного скроллинга."""

    DISABLED = "disabled"
    NO_NEW_CONTENT = "no_new_content"
    MAX_SCROLLS = "max_scrolls"
    MAX_HEIGHT = "max_height"
    TARGET_COUNT = "target_count"
    TIMEOUT = "timeout"
    CUSTOM_CALLBACK = "custom_callback"
    ERROR = "error"


@dataclass
class ScrollState:
    """
    Снимок состояния текущей итерации скроллинга.

    Передается в пользовательский `stop_callback`, чтобы вызывающий код
    мог реализовать произвольную логику остановки без необходимости
    иметь доступ к внутренностям `InfiniteScroll`.
    """

    engine: PlaywrightEngine
    iteration: int
    elapsed_seconds: float
    page_height: int
    item_count: Optional[int] = None


@dataclass
class ScrollResult:
    """Итоговый результат выполнения `InfiniteScroll.scroll()`."""

    scrolls_performed: int
    stop_reason: str
    elapsed_seconds: float
    final_height: int
    final_item_count: Optional[int] = None


class InfiniteScroll:
    """
    Централизованный исполнитель цикла бесконечного скроллинга.

    Работает с любым объектом, предоставляющим интерфейс Playwright Engine
    (`evaluate()`, `wait_for_load()`) — на практике это экземпляр
    `PlaywrightEngine` (`app/playwright_engine.py`). Сам компонент не
    запускает браузер и не выполняет навигацию — предполагается, что
    вызывающий код уже открыл нужную страницу через
    `PlaywrightEngine.goto()`.

    Пример использования:

        with PlaywrightEngine() as engine:
            engine.goto("https://example.com/feed")
            result = InfiniteScroll.scroll(engine, max_scrolls=20)
            html = engine.content()
    """

    # =====================================================================
    # НИЗКОУРОВНЕВЫЕ ОПЕРАЦИИ (скролл / замер высоты / подсчет элементов)
    # =====================================================================

    @staticmethod
    def _get_page_height(engine: PlaywrightEngine) -> int:
        """Возвращает текущую высоту документа (`document.body.scrollHeight`)."""
        return int(engine.evaluate("document.body.scrollHeight"))

    @staticmethod
    def _perform_scroll(engine: PlaywrightEngine, step_px: int, smooth: bool) -> None:
        """
        Выполняет одну прокрутку страницы.

        Args:
            step_px (int): Шаг прокрутки в пикселях. Если <= 0, страница
                скроллится сразу к текущему низу (`scrollHeight`).
            smooth (bool): Использовать плавную прокрутку вместо мгновенной.
        """
        behavior = "smooth" if smooth else "auto"
        if step_px and step_px > 0:
            script = f"window.scrollBy({{top: {step_px}, left: 0, behavior: '{behavior}'}})"
        else:
            script = (
                f"window.scrollTo({{top: document.body.scrollHeight, left: 0, "
                f"behavior: '{behavior}'}})"
            )
        engine.evaluate(script)

    @staticmethod
    def _count_items(
        engine: PlaywrightEngine,
        item_selector: Optional[str],
        count_callback: Optional[Callable[[PlaywrightEngine], int]],
        previous_count: Optional[int],
    ) -> Optional[int]:
        """
        Подсчитывает текущее количество загруженных элементов, если
        передан `count_callback` или `item_selector`. Иначе возвращает `None`.

        Сбой подсчета (например, элемент временно отсутствует в DOM) не
        прерывает цикл скроллинга — возвращается предыдущее известное
        значение, а сбой попадает в лог.
        """
        if count_callback is None and not item_selector:
            return None
        try:
            if count_callback is not None:
                return int(count_callback(engine))
            return int(engine.evaluate(f"document.querySelectorAll('{item_selector}').length"))
        except Exception as exc:
            log_message("error", f"Infinite Scroll: не удалось подсчитать элементы: {exc}")
            return previous_count

    @staticmethod
    def _wait_between_scrolls(delay_mode: str, fixed_seconds: float, min_seconds: float, max_seconds: float) -> None:
        """Пауза между итерациями скроллинга, делегированная Delay Manager."""
        if delay_mode == "fixed":
            DelayManager.wait_fixed(fixed_seconds)
        else:
            DelayManager.wait_random(min_seconds, max_seconds)

    # =====================================================================
    # ОСНОВНАЯ ТОЧКА ВХОДА
    # =====================================================================

    @classmethod
    def scroll(
        cls,
        engine: PlaywrightEngine,
        *,
        enabled: Optional[bool] = None,
        max_scrolls: Optional[int] = None,
        timeout_seconds: Optional[float] = None,
        max_page_height: Optional[int] = None,
        max_no_new_content_attempts: Optional[int] = None,
        target_item_count: Optional[int] = None,
        item_selector: Optional[str] = None,
        count_callback: Optional[Callable[[PlaywrightEngine], int]] = None,
        stop_callback: Optional[Callable[[ScrollState], bool]] = None,
        scroll_step_px: Optional[int] = None,
        smooth: Optional[bool] = None,
        wait_for_network_idle: Optional[bool] = None,
    ) -> ScrollResult:
        """
        Выполняет цикл прокрутки текущей страницы `engine` до срабатывания
        одного из настроенных условий остановки.

        Все условия остановки проверяются одновременно — цикл завершается
        по первому сработавшему условию. Любой аргумент, не переданный
        явно, берется из Configuration Manager (`app/config.py`).

        Args:
            engine (PlaywrightEngine): Активный движок с уже открытой
                страницей (после `engine.goto(...)`).
            enabled (bool, optional): Включает/выключает скроллинг.
                По умолчанию — `config.INFINITE_SCROLL_ENABLED`. Если
                `False`, метод сразу возвращает результат с
                `stop_reason="disabled"` без единой прокрутки.
            max_scrolls (int, optional): Максимум итераций скроллинга.
                `0` — без ограничения. По умолчанию —
                `config.INFINITE_SCROLL_MAX_SCROLLS`.
            timeout_seconds (float, optional): Общий таймаут цикла (секунды).
                `0` — без ограничения. По умолчанию —
                `config.INFINITE_SCROLL_TIMEOUT_SECONDS`.
            max_page_height (int, optional): Высота страницы (px), при
                достижении которой скроллинг останавливается. `0` — без
                ограничения. По умолчанию — `config.INFINITE_SCROLL_MAX_PAGE_HEIGHT`.
            max_no_new_content_attempts (int, optional): Число
                последовательных прокруток без увеличения высоты страницы,
                после которого считается, что новый контент больше не
                подгружается. По умолчанию —
                `config.INFINITE_SCROLL_MAX_NO_NEW_CONTENT`.
            target_item_count (int, optional): Целевое количество
                элементов — требует `item_selector` или `count_callback`.
            item_selector (str, optional): CSS-селектор для подсчета
                текущего количества загруженных элементов (передается
                вызывающим кодом — компонент не хранит селекторы сам).
            count_callback (Callable[[PlaywrightEngine], int], optional):
                Альтернатива `item_selector` — произвольная функция подсчета
                элементов. Имеет приоритет над `item_selector`, если оба переданы.
            stop_callback (Callable[[ScrollState], bool], optional):
                Пользовательская функция остановки — вызывается на каждой
                итерации, получает `ScrollState`, возвращает `True` для
                немедленной остановки.
            scroll_step_px (int, optional): Шаг прокрутки в пикселях.
                `0`/`None` — скроллить сразу к низу страницы на каждой
                итерации. По умолчанию — `config.INFINITE_SCROLL_STEP_PX`.
            smooth (bool, optional): Плавная прокрутка вместо мгновенной.
                По умолчанию — `config.INFINITE_SCROLL_SMOOTH`.
            wait_for_network_idle (bool, optional): Ожидать `networkidle`
                после каждого скролла (для сайтов с задержкой подгрузки
                через XHR/fetch). По умолчанию —
                `config.INFINITE_SCROLL_WAIT_NETWORK_IDLE`.

        Returns:
            ScrollResult: Итоговая статистика цикла (число итераций,
                причина остановки, затраченное время, финальная высота
                страницы и, если применимо, финальное количество элементов).
        """
        effective_enabled = enabled if enabled is not None else config.INFINITE_SCROLL_ENABLED
        if not effective_enabled:
            log_message("info", "Infinite Scroll: отключен конфигурацией — скроллинг не выполняется")
            return ScrollResult(0, ScrollStopReason.DISABLED.value, 0.0, 0)

        effective_max_scrolls = max_scrolls if max_scrolls is not None else config.INFINITE_SCROLL_MAX_SCROLLS
        effective_timeout = timeout_seconds if timeout_seconds is not None else config.INFINITE_SCROLL_TIMEOUT_SECONDS
        effective_max_height = max_page_height if max_page_height is not None else config.INFINITE_SCROLL_MAX_PAGE_HEIGHT
        effective_no_new_content = (
            max_no_new_content_attempts
            if max_no_new_content_attempts is not None
            else config.INFINITE_SCROLL_MAX_NO_NEW_CONTENT
        )
        effective_step = scroll_step_px if scroll_step_px is not None else config.INFINITE_SCROLL_STEP_PX
        effective_smooth = smooth if smooth is not None else config.INFINITE_SCROLL_SMOOTH
        effective_wait_network_idle = (
            wait_for_network_idle if wait_for_network_idle is not None else config.INFINITE_SCROLL_WAIT_NETWORK_IDLE
        )

        start_time = time.monotonic()

        try:
            last_height = cls._get_page_height(engine)
        except PlaywrightEngineError as exc:
            log_message("error", f"Infinite Scroll: не удалось получить высоту страницы: {exc}")
            return ScrollResult(0, ScrollStopReason.ERROR.value, 0.0, 0)

        current_item_count = cls._count_items(engine, item_selector, count_callback, None)

        log_message("info", "Infinite Scroll: скроллинг начат")

        iteration = 0
        no_new_content_streak = 0
        stop_reason = ScrollStopReason.MAX_SCROLLS  # запасное значение, переопределяется ниже

        while True:
            elapsed = time.monotonic() - start_time

            if effective_timeout > 0 and elapsed >= effective_timeout:
                stop_reason = ScrollStopReason.TIMEOUT
                break
            if effective_max_scrolls > 0 and iteration >= effective_max_scrolls:
                stop_reason = ScrollStopReason.MAX_SCROLLS
                break
            if effective_max_height > 0 and last_height >= effective_max_height:
                stop_reason = ScrollStopReason.MAX_HEIGHT
                break
            if (
                target_item_count is not None
                and target_item_count > 0
                and current_item_count is not None
                and current_item_count >= target_item_count
            ):
                stop_reason = ScrollStopReason.TARGET_COUNT
                break
            if stop_callback is not None:
                state = ScrollState(engine, iteration, elapsed, last_height, current_item_count)
                try:
                    should_stop = stop_callback(state)
                except Exception as exc:
                    log_message("error", f"Infinite Scroll: ошибка в пользовательском stop_callback: {exc}")
                    stop_reason = ScrollStopReason.ERROR
                    break
                if should_stop:
                    stop_reason = ScrollStopReason.CUSTOM_CALLBACK
                    break

            try:
                cls._perform_scroll(engine, effective_step, effective_smooth)
                cls._wait_between_scrolls(
                    config.INFINITE_SCROLL_DELAY_MODE,
                    config.INFINITE_SCROLL_DELAY_FIXED_SECONDS,
                    config.INFINITE_SCROLL_DELAY_MIN_SECONDS,
                    config.INFINITE_SCROLL_DELAY_MAX_SECONDS,
                )
                if effective_wait_network_idle:
                    engine.wait_for_load("networkidle")
                new_height = cls._get_page_height(engine)
            except PlaywrightEngineError as exc:
                log_message("error", f"Infinite Scroll: сбой во время прокрутки: {exc}")
                stop_reason = ScrollStopReason.ERROR
                break
            except Exception as exc:
                log_message("error", f"Infinite Scroll: непредвиденная ошибка во время прокрутки: {exc}")
                stop_reason = ScrollStopReason.ERROR
                break

            current_item_count = cls._count_items(engine, item_selector, count_callback, current_item_count)

            iteration += 1
            if new_height <= last_height:
                no_new_content_streak += 1
            else:
                no_new_content_streak = 0
            last_height = new_height

            if no_new_content_streak >= effective_no_new_content:
                stop_reason = ScrollStopReason.NO_NEW_CONTENT
                break

        elapsed_total = time.monotonic() - start_time
        log_message(
            "info",
            f"Infinite Scroll: завершено (итераций={iteration}, "
            f"причина={stop_reason.value}, время={elapsed_total:.1f}с)",
        )
        return ScrollResult(iteration, stop_reason.value, elapsed_total, last_height, current_item_count)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    with PlaywrightEngine(headless=False) as engine:
        engine.goto("https://infinite-scroll.com/demo/full-page/")
        result = InfiniteScroll.scroll(engine, max_scrolls=5, timeout_seconds=30)
        print(f"[{__file__}] Результат: {result}")
