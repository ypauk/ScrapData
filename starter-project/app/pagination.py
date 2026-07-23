#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pagination.

Централизованный компонент пагинации для скрапинга многостраничных
сайтов (см. `framework/ROADMAP.md`, Milestone 4).

Pagination — единственная точка, через которую скрапер-модули должны
выполнять навигацию между страницами. Он НЕ содержит логики парсинга/
экспорта/логина/бесконечного скролла и НЕ знает о селекторах конкретных
сайтов — единственное, что он умеет, это итерировать страницы по одной
из настраиваемых стратегий и останавливаться по одному из настраиваемых
условий.

Pagination engine-независим: он никогда не вызывает `engine.get()` или
`engine.goto()` сам. Вместо этого вызывающий код передаёт `fetch_callback`
— функцию, которая принимает `PageContext` и возвращает `PageFetchResult`.
Это позволяет использовать Paginator как с Requests Engine, так и с
Playwright Engine без изменения самих движков.

    Paginator.paginate(fetch_callback, pagination_type, ...)
            │
            ▼
      loop: build PageContext (url/params for url/offset/ajax;
                               None for next_button/custom)
            │
            ▼
      fetch_callback(context) -> PageFetchResult
            │           (caller internally uses RequestsEngine.get()
            │            OR PlaywrightEngine.goto()+content())
            ▼
      Paginator evaluates stop conditions
      (last_page / no_items / max_pages / duplicate / custom_callback / error)
            │
            ▼
      DelayManager.wait(...) between pages (reused, not reimplemented)

Поддерживаемые стратегии (PaginationType):
    URL         — генерация URL с меняющимся query-параметром (?page=2,3,4...)
    OFFSET      — генерация URL с меняющимся offset-параметром (?offset=20,40,60...)
    NEXT_BUTTON — Playwright: клик по кнопке "Next" (требует selector).
    AJAX        — то же, что URL/Offset, но подразумевает API-запрос;
                  генерация URL/params идентична, вызывающий код решает,
                  как выполнять запрос (Requests GET или Playwright goto).
    CUSTOM      — полностью делегирована вызывающему коду через
                  `custom_context_generator`; для самых сложных сайтов.

Пример использования (Requests Engine):

    from app.pagination import Paginator, PaginationType, PageContext, PageFetchResult
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()
    results = []

    def fetch(ctx: PageContext) -> PageFetchResult:
        resp = engine.get(ctx.url, params=ctx.params)
        items = resp.json() if ctx.pagination_type == PaginationType.AJAX else resp.text
        return PageFetchResult(
            content=items,
            item_count=len(items) if isinstance(items, list) else None,
            dedupe_key=resp.url,
        )

    for page_result in Paginator.paginate(
        fetch, PaginationType.URL, max_pages=5,
        url="https://api.example.com/items",
        page_param="page", start_page=1, page_step=1,
    ):
        results.append(page_result.content)

Пример использования (Playwright Engine + Next Button):

    from app.pagination import Paginator, PaginationType, PageContext, PageFetchResult
    from app.playwright_engine import PlaywrightEngine

    with PlaywrightEngine() as engine:
        engine.goto("https://example.com/items")

        def fetch(ctx: PageContext) -> PageFetchResult:
            if ctx.use_next_button:
                success = Paginator.click_next_button(engine, "a.next, button.next")
                if not success:
                    return PageFetchResult(content=engine.content(), has_next=False)
            return PageFetchResult(content=engine.content())

        for page_result in Paginator.paginate(
            fetch, PaginationType.NEXT_BUTTON,
            next_button_selector="a.next, button.next",
            max_pages=10,
        ):
            pass  # page_result.content содержит HTML очередной страницы
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from app import config
from app.delay_manager import DelayManager
from app.utils import log_message


class PaginationError(Exception):
    """
    Единое исключение Pagination для непредвиденных сбоев конфигурации
    (например, некорректных аргументов), не связанных с ожидаемыми
    условиями остановки цикла пагинации.

    Сбои самого fetch_callback во время запроса НЕ поднимаются как это
    исключение — они обрабатываются graceful (см. `PaginationStopReason.ERROR`),
    чтобы одна неудачная страница не прерывала весь процесс скрапинга.
    """


class PaginationType(str, Enum):
    """Стратегия пагинации."""

    URL = "url"
    OFFSET = "offset"
    NEXT_BUTTON = "next_button"
    AJAX = "ajax"
    CUSTOM = "custom"


class PaginationStopReason(str, Enum):
    """Причина остановки цикла пагинации."""

    LAST_PAGE = "last_page"
    NO_ITEMS = "no_items"
    MAX_PAGES = "max_pages"
    DUPLICATE_PAGE = "duplicate_page"
    CUSTOM_CALLBACK = "custom_callback"
    ERROR = "error"


@dataclass
class PageContext:
    """
    Контекст очередной страницы, передаваемый в `fetch_callback`.

    Атрибуты:
        url (str): URL страницы (для URL/Offset/AJAX/CUSTOM).
        params (dict, optional): Query-параметры для запроса.
        page_number (int): Номер текущей страницы (1-based).
        pagination_type (PaginationType): Текущая стратегия.
        use_next_button (bool): True, если стратегия NEXT_BUTTON
            (в этом случае fetch_callback должен сам кликнуть кнопку
            и вернуть контент).
        custom_data (Any, optional): Произвольные данные от
            `custom_context_generator` (только для CUSTOM).
    """

    url: str
    page_number: int
    pagination_type: PaginationType
    params: Optional[Dict[str, Any]] = None
    use_next_button: bool = False
    custom_data: Any = None


@dataclass
class PageFetchResult:
    """
    Результат, возвращаемый `fetch_callback` после получения одной страницы.

    Атрибуты:
        content (Any): HTML/JSON/текст страницы (может быть любым —
            Paginator не парсит его, а просто передаёт в итератор).
        item_count (int, optional): Количество элементов на странице
            (для условия остановки NO_ITEMS). Если None — не проверяется.
        has_next (bool, optional): Явный признак наличия следующей страницы
            (для сайтов, где это можно определить до следующего запроса).
            По умолчанию True (если не указано иное).
        dedupe_key (str, optional): Уникальный ключ для обнаружения
            дублирующихся страниц (например, URL ответа, заголовок, hash).
            Если None — не проверяется.
    """

    content: Any
    item_count: Optional[int] = None
    has_next: Optional[bool] = None
    dedupe_key: Optional[str] = None


@dataclass
class PageResult:
    """
    Итоговый результат одной итерации пагинации, возвращаемый
    генератором `Paginator.paginate()`.

    Атрибуты:
        page_number (int): Номер страницы (1-based).
        content (Any): Содержимое страницы (как вернул fetch_callback).
        stop_reason (str, optional): Причина остановки (только в
            последнем элементе итератора; для всех остальных — None).
        pages_fetched (int, optional): Общее число успешно загруженных
            страниц (только в последнем элементе).
        elapsed_seconds (float, optional): Общее время пагинации
            (только в последнем элементе).
    """

    page_number: int
    content: Any
    stop_reason: Optional[str] = None
    pages_fetched: Optional[int] = None
    elapsed_seconds: Optional[float] = None


class Paginator:
    """
    Централизованный исполнитель цикла пагинации.

    Не зависит от конкретного движка: вызывающий код передаёт
    `fetch_callback`, который использует Requests Engine или
    Playwright Engine по своему усмотрению.

    Пагинация — не Infinite Scroll, она не выполняется на уже
    открытой странице. Для каждой новой страницы (кроме NEXT_BUTTON)
    требуется новый запрос/навигация через fetch_callback.
    """

    # =====================================================================
    # ГЕНЕРАТОРЫ URL/ПАРАМЕТРОВ (для URL, OFFSET, AJAX)
    # =====================================================================

    @staticmethod
    def _build_url_params(
        base_url: str,
        param_name: str,
        value: int,
        existing_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Строит query-параметры для URL/Offset/AJAX пагинации.

        Args:
            base_url: Базовый URL (без параметров).
            param_name: Имя параметра (например, "page" или "offset").
            value: Значение параметра.
            existing_params: Дополнительные статические параметры.

        Returns:
            Dict[str, Any]: Query-параметры для запроса.
        """
        params = dict(existing_params or {})
        params[param_name] = value
        return params

    # =====================================================================
    # ПОМОЩНИК ДЛЯ NEXT BUTTON (Playwright)
    # =====================================================================

    @staticmethod
    def click_next_button(
        engine: Any,
        selector: str,
        timeout_ms: Optional[float] = None,
    ) -> bool:
        """
        Пытается кликнуть по кнопке "Next" на текущей странице Playwright.

        Вызывается из fetch_callback при стратегии NEXT_BUTTON.

        Args:
            engine: Экземпляр PlaywrightEngine (с уже открытой страницей).
            selector: CSS-селектор кнопки перехода на следующую страницу.
            timeout_ms: Таймаут ожидания селектора (мс).
                По умолчанию — config.PLAYWRIGHT_TIMEOUT_MS.

        Returns:
            bool: True, если кнопка найдена и кликнута (страница перешла);
                  False, если кнопка не найдена (считается последней
                  страницей — без исключения).
        """
        from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError

        effective_timeout = timeout_ms if timeout_ms is not None else config.PLAYWRIGHT_TIMEOUT_MS

        try:
            element = engine.page.wait_for_selector(selector, timeout=effective_timeout)
            if element is None:
                return False
            # Проверяем, что кнопка не disabled
            is_disabled = engine.page.evaluate(
                f"document.querySelector('{selector}')?.disabled ?? false"
            )
            if is_disabled:
                return False
            element.click()
            engine.wait_for_load("networkidle")
            return True
        except PlaywrightEngineError:
            # Селектор не появился — считаем последней страницей
            return False
        except Exception:
            # Любая другая ошибка клика — тоже graceful
            return False

    # =====================================================================
    # ОСНОВНАЯ ТОЧКА ВХОДА
    # =====================================================================

    @classmethod
    def paginate(
        cls,
        fetch_callback: Callable[[PageContext], PageFetchResult],
        pagination_type: Union[PaginationType, str],
        *,
        # --- Общие параметры ---
        url: Optional[str] = None,
        existing_params: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        timeout_seconds: Optional[float] = None,
        stop_callback: Optional[Callable[[int, Any], bool]] = None,
        detect_duplicates: Optional[bool] = None,
        # --- URL / Offset ---
        page_param: Optional[str] = None,
        start_page: Optional[int] = None,
        page_step: Optional[int] = None,
        offset_param: Optional[str] = None,
        start_offset: Optional[int] = None,
        offset_step: Optional[int] = None,
        # --- Next Button ---
        next_button_selector: Optional[str] = None,
        # --- Custom ---
        custom_context_generator: Optional[Callable[[int, "PageContext"], Optional[PageContext]]] = None,
        # --- Delay ---
        delay_mode: Optional[str] = None,
        delay_fixed_seconds: Optional[float] = None,
        delay_min_seconds: Optional[float] = None,
        delay_max_seconds: Optional[float] = None,
    ) -> List[PageResult]:
        """
        Выполняет цикл пагинации, вызывая `fetch_callback` для каждой
        страницы, пока не сработает одно из условий остановки.

        Все условия остановки проверяются одновременно — цикл завершается
        по первому сработавшему. Любой аргумент, не переданный явно,
        берётся из Configuration Manager (`app/config.py`).

        Args:
            fetch_callback: Функция, принимающая `PageContext` и
                возвращающая `PageFetchResult`. Вызывается один раз
                на страницу. Должна быть чистой (без побочных эффектов,
                кроме самого запроса) — Paginator сам управляет
                количеством вызовов и паузами между ними.
            pagination_type: Стратегия пагинации ("url", "offset",
                "next_button", "ajax", "custom").

        --- Общие параметры ---
            url: Базовый URL (обязателен для URL/Offset/AJAX/CUSTOM).
            existing_params: Статические query-параметры, добавляемые
                к каждому запросу.
            max_pages: Максимальное количество страниц. 0 — без
                ограничения. По умолчанию — config.PAGINATION_MAX_PAGES.
            timeout_seconds: Общий таймаут цикла пагинации (секунды).
                0 — без ограничения. По умолчанию —
                config.PAGINATION_TIMEOUT_SECONDS.
            stop_callback: Пользовательская функция остановки.
                Принимает (page_number, content), возвращает True
                для немедленной остановки.
            detect_duplicates: Включает обнаружение дублирующихся
                страниц (по dedupe_key из fetch_callback).
                По умолчанию — config.PAGINATION_DUPLICATE_DETECTION.

        --- Параметры URL/Offset пагинации ---
            page_param: Имя query-параметра для URL-пагинации
                (например, "page"). По умолчанию —
                config.PAGINATION_PAGE_PARAM.
            start_page: Начальное значение счётчика страниц
                (например, 1). По умолчанию —
                config.PAGINATION_START_PAGE.
            page_step: Шаг счётчика страниц (например, 1).
                По умолчанию — config.PAGINATION_PAGE_STEP.
            offset_param: Имя query-параметра для offset-пагинации
                (например, "offset"). По умолчанию —
                config.PAGINATION_OFFSET_PARAM.
            start_offset: Начальное значение offset (например, 0
                или 20). По умолчанию —
                config.PAGINATION_START_OFFSET.
            offset_step: Шаг offset (например, 20).
                По умолчанию — config.PAGINATION_OFFSET_STEP.

        --- Параметры Next Button ---
            next_button_selector: CSS-селектор кнопки "Next"
                (обязателен для NEXT_BUTTON).

        --- Параметры Custom ---
            custom_context_generator: Функция, принимающая
                (page_number, предыдущий PageContext) и возвращающая
                новый PageContext для следующей страницы, либо None
                для остановки. Обязательна для CUSTOM.

        --- Параметры задержки ---
            delay_mode: "fixed" или "random".
            delay_fixed_seconds: Фиксированная задержка (сек).
            delay_min_seconds / delay_max_seconds: Диапазон
                случайной задержки.

        Returns:
            List[PageResult]: Список результатов всех страниц.
                Последний элемент содержит stop_reason,
                pages_fetched, elapsed_seconds.

        Raises:
            PaginationError: При некорректных аргументах (например,
                не указан обязательный параметр для выбранной стратегии).
        """
        # --- Нормализация типа пагинации ---
        if isinstance(pagination_type, str):
            pagination_type = PaginationType(pagination_type)

        # --- Валидация аргументов ---
        if pagination_type in (PaginationType.URL, PaginationType.OFFSET, PaginationType.AJAX, PaginationType.CUSTOM):
            if not url:
                raise PaginationError(
                    f"Параметр 'url' обязателен для стратегии '{pagination_type.value}'"
                )
        if pagination_type == PaginationType.NEXT_BUTTON and not next_button_selector:
            raise PaginationError("Параметр 'next_button_selector' обязателен для стратегии 'next_button'")
        if pagination_type == PaginationType.CUSTOM and not custom_context_generator:
            raise PaginationError("Параметр 'custom_context_generator' обязателен для стратегии 'custom'")

        # --- Значения по умолчанию из Configuration Manager ---
        effective_max_pages = max_pages if max_pages is not None else config.PAGINATION_MAX_PAGES
        effective_timeout = timeout_seconds if timeout_seconds is not None else config.PAGINATION_TIMEOUT_SECONDS
        effective_detect_duplicates = (
            detect_duplicates if detect_duplicates is not None else config.PAGINATION_DUPLICATE_DETECTION
        )
        effective_page_param = page_param or config.PAGINATION_PAGE_PARAM
        effective_start_page = start_page if start_page is not None else config.PAGINATION_START_PAGE
        effective_page_step = page_step if page_step is not None else config.PAGINATION_PAGE_STEP
        effective_offset_param = offset_param or config.PAGINATION_OFFSET_PARAM
        effective_start_offset = start_offset if start_offset is not None else config.PAGINATION_START_OFFSET
        effective_offset_step = offset_step if offset_step is not None else config.PAGINATION_OFFSET_STEP

        # --- Задержки ---
        eff_delay_mode = delay_mode if delay_mode is not None else config.PAGINATION_DELAY_MODE
        eff_delay_fixed = delay_fixed_seconds if delay_fixed_seconds is not None else config.PAGINATION_DELAY_FIXED_SECONDS
        eff_delay_min = delay_min_seconds if delay_min_seconds is not None else config.PAGINATION_DELAY_MIN_SECONDS
        eff_delay_max = delay_max_seconds if delay_max_seconds is not None else config.PAGINATION_DELAY_MAX_SECONDS

        # --- Инициализация цикла ---
        results: List[PageResult] = []
        seen_dedupe_keys: set = set()
        start_time = time.monotonic()
        stop_reason: Optional[PaginationStopReason] = None
        current_value = effective_start_page
        current_offset = effective_start_offset

        # --- Первый PageContext ---
        if pagination_type == PaginationType.NEXT_BUTTON:
            context = PageContext(
                url=url or "",
                page_number=1,
                pagination_type=pagination_type,
                use_next_button=True,
            )
        elif pagination_type == PaginationType.CUSTOM:
            context = custom_context_generator(1, None) if custom_context_generator else None
            if context is None:
                return [
                    PageResult(0, None, PaginationStopReason.LAST_PAGE.value, 0, 0.0)
                ]
        elif pagination_type in (PaginationType.URL, PaginationType.AJAX):
            params = cls._build_url_params(url, effective_page_param, current_value, existing_params)
            context = PageContext(url=url, page_number=1, pagination_type=pagination_type, params=params)
        else:  # OFFSET
            params = cls._build_url_params(url, effective_offset_param, current_offset, existing_params)
            context = PageContext(url=url, page_number=1, pagination_type=pagination_type, params=params)

        log_message("info", f"Pagination: начата (тип={pagination_type.value})")

        # --- Цикл ---
        while True:
            # --- Таймаут ---
            elapsed = time.monotonic() - start_time
            if effective_timeout > 0 and elapsed >= effective_timeout:
                stop_reason = PaginationStopReason.ERROR  # timeout как ошибка
                log_message("error", "Pagination: таймаут цикла")
                break

            # --- Выполняем запрос ---
            try:
                fetch_result = fetch_callback(context)
            except Exception as exc:
                log_message("error", f"Pagination: сбой на странице {context.page_number}: {exc}")
                stop_reason = PaginationStopReason.ERROR
                break

            if not isinstance(fetch_result, PageFetchResult):
                log_message("error", "Pagination: fetch_callback должен возвращать PageFetchResult")
                stop_reason = PaginationStopReason.ERROR
                break

            content = fetch_result.content
            item_count = fetch_result.item_count
            has_next = fetch_result.has_next if fetch_result.has_next is not None else True
            dedupe_key = fetch_result.dedupe_key

            page_number = context.page_number

            # --- Сохраняем результат ---
            results.append(PageResult(page_number=page_number, content=content))

            log_message("info", f"Pagination: страница {page_number} загружена")

            # --- Остановка по last_page (has_next == False) ---
            if not has_next:
                stop_reason = PaginationStopReason.LAST_PAGE
                break

            # --- Остановка по no_items ---
            if item_count is not None and item_count == 0:
                stop_reason = PaginationStopReason.NO_ITEMS
                break

            # --- Остановка по max_pages ---
            if effective_max_pages > 0 and page_number >= effective_max_pages:
                stop_reason = PaginationStopReason.MAX_PAGES
                break

            # --- Остановка по duplicate ---
            if effective_detect_duplicates and dedupe_key is not None:
                if dedupe_key in seen_dedupe_keys:
                    stop_reason = PaginationStopReason.DUPLICATE_PAGE
                    break
                seen_dedupe_keys.add(dedupe_key)

            # --- Остановка по custom_callback ---
            if stop_callback is not None:
                try:
                    should_stop = stop_callback(page_number, content)
                except Exception as exc:
                    log_message("error", f"Pagination: ошибка в stop_callback: {exc}")
                    stop_reason = PaginationStopReason.ERROR
                    break
                if should_stop:
                    stop_reason = PaginationStopReason.CUSTOM_CALLBACK
                    break

            # --- Пауза перед следующей страницей ---
            if eff_delay_mode == "fixed":
                DelayManager.wait_fixed(eff_delay_fixed)
            else:
                DelayManager.wait_random(eff_delay_min, eff_delay_max)

            # --- Генерируем контекст следующей страницы ---
            next_page_number = page_number + 1

            if pagination_type == PaginationType.NEXT_BUTTON:
                context = PageContext(
                    url=url or "",
                    page_number=next_page_number,
                    pagination_type=pagination_type,
                    use_next_button=True,
                )
            elif pagination_type == PaginationType.CUSTOM:
                if custom_context_generator is not None:
                    context = custom_context_generator(next_page_number, context)
                    if context is None:
                        stop_reason = PaginationStopReason.LAST_PAGE
                        break
                else:
                    stop_reason = PaginationStopReason.LAST_PAGE
                    break
            elif pagination_type in (PaginationType.URL, PaginationType.AJAX):
                current_value += effective_page_step
                params = cls._build_url_params(url, effective_page_param, current_value, existing_params)
                context = PageContext(url=url, page_number=next_page_number, pagination_type=pagination_type, params=params)
            else:  # OFFSET
                current_offset += effective_offset_step
                params = cls._build_url_params(url, effective_offset_param, current_offset, existing_params)
                context = PageContext(url=url, page_number=next_page_number, pagination_type=pagination_type, params=params)

        # --- Завершение ---
        elapsed_total = time.monotonic() - start_time
        stop_reason_str = stop_reason.value if stop_reason else PaginationStopReason.LAST_PAGE.value
        log_message(
            "info",
            f"Pagination: завершено (страниц={len(results)}, "
            f"причина={stop_reason_str}, время={elapsed_total:.1f}с)",
        )

        # Добавляем мета-информацию в последний элемент
        if results:
            results[-1].stop_reason = stop_reason_str
            results[-1].pages_fetched = len(results)
            results[-1].elapsed_seconds = elapsed_total

        return results


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()

    def mock_fetch(ctx: PageContext) -> PageFetchResult:
        resp = engine.get(ctx.url, params=ctx.params)
        return PageFetchResult(content=resp.text, dedupe_key=resp.url)

    results = Paginator.paginate(
        mock_fetch,
        PaginationType.URL,
        url="https://httpbin.org/get",
        max_pages=3,
        page_param="page",
        start_page=1,
        page_step=1,
    )
    print(f"Загружено страниц: {len(results)}")
    if results:
        last = results[-1]
        print(f"Причина остановки: {last.stop_reason}")