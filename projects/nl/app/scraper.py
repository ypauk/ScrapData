#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scraper Module — сетевой слой для сбора HTML-контента через Playwright.

Отвечает только за запросы и получение HTML-кода страниц.
Не выполняет парсинг DOM — это задача parser.py.

Использует Playwright для загрузки страниц с JavaScript-рендерингом.
"""

from typing import List, Optional

from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError
from app.utils import log_message, random_delay


def fetch_page_with_engine(engine: PlaywrightEngine, url: str) -> Optional[str]:
    """
    Загружает страницу через PlaywrightEngine и возвращает HTML.

    Args:
        engine: Экземпляр PlaywrightEngine.
        url: URL для загрузки.

    Returns:
        HTML-код страницы или None при ошибке.
    """
    try:
        # Используем "load" вместо "networkidle" — сайт держит фоновые соединения
        engine.goto(url, wait_until="load")
        return engine.content()
    except PlaywrightEngineError as e:
        log_message("error", f"[{__file__}] Ошибка загрузки {url}: {e}")
        return None


def fetch_listing(engine: PlaywrightEngine, category_url: str) -> Optional[str]:
    """
    Загружает HTML-код страницы категории через Playwright.

    Args:
        engine: Экземпляр PlaywrightEngine.
        category_url: URL страницы категории.

    Returns:
        HTML-код категории или None при ошибке.
    """
    log_message("info", f"[{__file__}] Загрузка категории через Playwright: {category_url}")
    return fetch_page_with_engine(engine, category_url)


def fetch_product(engine: PlaywrightEngine, product_url: str) -> Optional[str]:
    """
    Загружает HTML-код страницы товара через Playwright.

    Args:
        engine: Экземпляр PlaywrightEngine.
        product_url: URL страницы товара.

    Returns:
        HTML-код товара или None при ошибке.
    """
    log_message("debug", f"[{__file__}] Загрузка товара через Playwright: {product_url}")
    return fetch_page_with_engine(engine, product_url)


def collect_product_urls(engine: PlaywrightEngine, category_url: str, limit: int = 2) -> List[str]:
    """
    Загружает категорию и извлекает ссылки на товары.

    Args:
        engine: Экземпляр PlaywrightEngine.
        category_url: URL страницы категории.
        limit: Максимальное количество ссылок.

    Returns:
        Список URL товаров (не более limit).
    """
    from app.parser import parse_listing

    html = fetch_listing(engine, category_url)
    if not html:
        log_message("error", f"[{__file__}] Не удалось загрузить категорию: {category_url}")
        return []

    urls = parse_listing(html)
    if limit and len(urls) > limit:
        urls = urls[:limit]

    log_message("info", f"[{__file__}] Найдено {len(urls)} URL товаров")
    return urls


def fetch_page_data(engine: Optional[PlaywrightEngine] = None, category_url: str = None) -> List[str]:
    """
    Главная точка входа для main.py.

    Загружает категорию через Playwright, извлекает URL первых двух товаров,
    загружает их страницы и возвращает список HTML-кодов.

    Формат возврата:
        [HTML категории, HTML товара 1, HTML товара 2]

    Args:
        engine: Экземпляр PlaywrightEngine (обязателен).
        category_url: URL категории (опционально).

    Returns:
        Список HTML-кодов страниц.
    """
    if engine is None:
        log_message("error", f"[{__file__}] fetch_page_data: engine не передан")
        return []

    if category_url is None:
        category_url = "https://www.professionele-koeling.nl/koelkasten-kisten.html"

    log_message("info", f"[{__file__}] fetch_page_data: начало")

    # 1. Загружаем категорию
    category_html = fetch_listing(engine, category_url)
    if not category_html:
        log_message("error", f"[{__file__}] fetch_page_data: не удалось загрузить категорию")
        return []

    # 2. Извлекаем URL товаров
    from app.parser import parse_listing
    product_urls = parse_listing(category_html)
    product_urls = product_urls[:2]  # Только первые два

    if not product_urls:
        log_message("error", f"[{__file__}] fetch_page_data: не найдено товаров в категории")
        return []

    log_message("info", f"[{__file__}] fetch_page_data: найдено {len(product_urls)} товаров")

    # 3. Загружаем страницы товаров
    product_htmls = []
    for idx, url in enumerate(product_urls, 1):
        log_message("debug", f"[{__file__}] fetch_page_data: загрузка товара {idx}/{len(product_urls)}")
        html = fetch_product(engine, url)
        if html:
            product_htmls.append(html)
        else:
            log_message("error", f"[{__file__}] fetch_page_data: не удалось загрузить {url}")

        if idx < len(product_urls):
            random_delay(1.0, 2.0)

    result = [category_html] + product_htmls
    log_message(
        "info",
        f"[{__file__}] fetch_page_data: завершено, получено {len(result)} страниц "
        f"(категория + {len(product_htmls)} товаров)"
    )
    return result


# ============================================================================
# ТЕСТОВЫЙ ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(f"[{__file__}] ТЕСТОВЫЙ ЗАПУСК SCRAPER (Playwright)")
    print("=" * 70)

    with PlaywrightEngine(headless=False) as engine:
        print("\n--- Тест: fetch_page_data() ---")
        pages = fetch_page_data(engine)
        print(f"Получено страниц: {len(pages)}")
        if pages:
            print(f"Категория: {len(pages[0])} символов")
            for i, html in enumerate(pages[1:], 1):
                print(f"Товар {i}: {len(html)} символов")

    print("\n" + "=" * 70)
    print(f"[{__file__}] Тест завершён")