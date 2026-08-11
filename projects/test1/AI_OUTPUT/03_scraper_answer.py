Модуль отвечает за полный цикл сбора: переход по каталогу, извлечение URL товаров, обход пагинации и получение сырого HTML страниц товаров.
Использует только переданный PlaywrightEngine; DOM не парсит и не использует requests/httpx.
Также содержит отдельную функцию загрузки изображений в OUTPUT_DIR и построения сырой записи товара.
Пагинация останавливается при отсутствии .pager .pages a.next, повторном URL или ошибке страницы.

Python
Запустить
# app/scraper.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scraper layer.

Отвечает только за:
- навигацию через PlaywrightEngine;
- обход страниц каталога;
- извлечение URL товаров из HTML;
- получение HTML страниц товаров;
- загрузку изображений;
- построение сырой записи товара.

DOM-парсинг выполняется в parser.py.
"""

import base64
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from app.config import BASE_URL, OUTPUT_DIR
from app.playwright_engine import PlaywrightEngine


# ============================================================================
# CONSTANTS
# ============================================================================

_LISTING_SELECTOR = "ul.products-grid.category-products-grid"
_PRODUCT_ITEM_SELECTOR = "ul.products-grid.category-products-grid li.item"
_PRODUCT_LINK_SELECTOR = "h2.product-name a[href]"
_PRODUCT_LINK_FALLBACK_SELECTOR = "a.product-image[href]"
_PRODUCT_PAGE_SELECTOR = ".product-name h1"
_NEXT_PAGE_SELECTOR = ".pager .pages a.next"


# ============================================================================
# HELPERS
# ============================================================================


def _log(level: str, message: str) -> None:
    """Единый формат логирования scraper.py."""
    print(f"[{__file__}] {level.upper()}: {message}")


def _absolute_url(url: str, base_url: str = BASE_URL) -> str:
    """Преобразует относительный URL в абсолютный."""
    if not url:
        return ""

    return urljoin(base_url, url.strip())


def _safe_filename(value: str) -> str:
    """
    Делает строку безопасной для использования в имени файла.
    """
    value = value.strip()
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE)
    value = value.strip("._")

    return value or "product"


def _image_extension(url: str, content_type: str = "") -> str:
    """
    Определяет расширение изображения по URL или Content-Type.
    """
    path = urlparse(url).path.lower()

    known_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
        ".bmp",
        ".svg",
        ".avif",
    )

    for extension in known_extensions:
        if path.endswith(extension):
            return extension

    content_type = content_type.lower().split(";", 1)[0].strip()

    content_types = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/svg+xml": ".svg",
        "image/avif": ".avif",
    }

    return content_types.get(content_type, ".jpg")


def _image_urls_from_html(html: str, page_url: str) -> List[str]:
    """
    Вспомогательное извлечение URL изображений без полноценного DOM-парсинга.

    Эта функция используется только для определения ресурсов, которые
    scraper должен скачать. Извлечение бизнес-полей товара остаётся
    ответственностью parser.py.
    """
    if not html:
        return []

    urls: List[str] = []

    # Основной вариант для данного Magento-сайта:
    # <img src="..."> / <img data-src="...">
    patterns = (
        r'<img[^>]+(?:src|data-src)\s*=\s*["\']([^"\']+)["\']',
        r'<a[^>]+href\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif|bmp|avif)(?:\?[^"\']*)?)["\']',
    )

    for pattern in patterns:
        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            absolute = _absolute_url(match, page_url)
            if absolute and absolute not in urls:
                urls.append(absolute)

    return urls


# ============================================================================
# LISTING PAGE
# ============================================================================


def fetch_listing_page(engine: PlaywrightEngine, url: str) -> str:
    """
    Загружает страницу каталога и возвращает её отрендеренный HTML.

    Навигация выполняется исключительно через переданный PlaywrightEngine.
    """
    try:
        engine.goto(url)

        try:
            engine.wait_for_selector(_LISTING_SELECTOR)
        except Exception as selector_exc:
            _log(
                "warning",
                f"Не найден основной контейнер каталога {url}: {selector_exc}",
            )

        html = engine.content()

        if not html:
            _log("warning", f"Пустой HTML каталога: {url}")

        return html or ""

    except Exception as exc:
        _log("error", f"Ошибка загрузки страницы каталога {url}: {exc}")
        return ""


def extract_product_urls(html: str) -> List[str]:
    """
    Извлекает URL товаров из HTML страницы каталога.

    Основной селектор:
        h2.product-name a[href]

    Fallback:
        a.product-image[href]

    Здесь намеренно нет BeautifulSoup: scraper не занимается DOM-парсингом.
    """
    if not html:
        return []

    urls: List[str] = []

    try:
        # Сначала берём ссылки из product-name.
        pattern = (
            r'<h2[^>]*class=["\'][^"\']*\bproduct-name\b[^"\']*["\'][^>]*>'
            r'\s*<a[^>]+href=["\']([^"\']+)["\']'
        )

        for match in re.findall(pattern, html, flags=re.IGNORECASE):
            url = _absolute_url(match)

            if url and url not in urls:
                urls.append(url)

        # Fallback, если product-name ссылки не были найдены.
        if not urls:
            fallback_pattern = (
                r'<a[^>]*class=["\'][^"\']*\bproduct-image\b[^"\']*["\']'
                r'[^>]*href=["\']([^"\']+)["\']'
            )

            for match in re.findall(
                fallback_pattern,
                html,
                flags=re.IGNORECASE,
            ):
                url = _absolute_url(match)

                if url and url not in urls:
                    urls.append(url)

    except Exception as exc:
        _log("error", f"Ошибка извлечения URL товаров: {exc}")

    _log("info", f"Извлечено URL товаров: {len(urls)}")

    return urls


# ============================================================================
# PRODUCT PAGE
# ============================================================================


def fetch_product_page(engine: PlaywrightEngine, url: str) -> str:
    """
    Загружает страницу товара и возвращает сырой HTML.
    """
    try:
        engine.goto(url)

        try:
            engine.wait_for_selector(_PRODUCT_PAGE_SELECTOR)
        except Exception as selector_exc:
            _log(
                "warning",
                f"Не найден заголовок товара на {url}: {selector_exc}",
            )

        html = engine.content()

        if not html:
            _log("warning", f"Пустой HTML товара: {url}")

        return html or ""

    except Exception as exc:
        _log("error", f"Ошибка загрузки товара {url}: {exc}")
        return ""


# ============================================================================
# IMAGE DOWNLOAD
# ============================================================================


def download_product_images(
    engine: PlaywrightEngine,
    image_urls: List[str],
    product_key: str,
) -> List[str]:
    """
    Загружает изображения товаров через текущий Playwright page context.

    Изображения сохраняются непосредственно в OUTPUT_DIR.
    Возвращаются локальные имена файлов, а не абсолютные пути.

    Использование page.evaluate() позволяет выполнять загрузку в том же
    браузерном контексте, где уже присутствуют cookies/session.
    """
    if not image_urls:
        return []

    downloaded: List[str] = []
    safe_key = _safe_filename(product_key)

    try:
        page = engine.page
    except Exception as exc:
        _log("error", f"Не удалось получить engine.page: {exc}")
        return []

    for index, image_url in enumerate(image_urls, start=1):
        try:
            absolute_url = _absolute_url(image_url)

            if not absolute_url:
                continue

            result = page.evaluate(
                """
                async (url) => {
                    try {
                        const response = await fetch(url, {
                            credentials: "include"
                        });

                        if (!response.ok) {
                            return {
                                ok: false,
                                status: response.status,
                                contentType: response.headers.get("content-type") || ""
                            };
                        }

                        const buffer = await response.arrayBuffer();
                        const bytes = new Uint8Array(buffer);

                        let binary = "";
                        const chunkSize = 0x8000;

                        for (let i = 0; i < bytes.length; i += chunkSize) {
                            const chunk = bytes.subarray(
                                i,
                                Math.min(i + chunkSize, bytes.length)
                            );
                            binary += String.fromCharCode(...chunk);
                        }

                        return {
                            ok: true,
                            base64: btoa(binary),
                            contentType:
                                response.headers.get("content-type") || ""
                        };
                    } catch (error) {
                        return {
                            ok: false,
                            error: String(error),
                            contentType: ""
                        };
                    }
                }
                """,
                absolute_url,
            )

            if not isinstance(result, dict) or not result.get("ok"):
                _log(
                    "warning",
                    f"Не удалось скачать изображение {absolute_url}: "
                    f"{result.get('error', result.get('status', 'unknown')) "
                    if isinstance(result, dict) else 'unknown'}",
                )
                continue

            encoded = result.get("base64")

            if not encoded:
                _log("warning", f"Пустое содержимое изображения: {absolute_url}")
                continue

            extension = _image_extension(
                absolute_url,
                str(result.get("contentType", "")),
            )

            filename = f"{safe_key}_{index}{extension}"
            filepath = Path(OUTPUT_DIR) / filename

            # Не создаём новые директории — используем существующий OUTPUT_DIR.
            with open(filepath, "wb") as image_file:
                image_file.write(base64.b64decode(encoded))

            downloaded.append(filename)

            _log(
                "info",
                f"Изображение сохранено: {filename}",
            )

        except Exception as exc:
            _log(
                "error",
                f"Ошибка загрузки изображения {image_url}: {exc}",
            )

    return downloaded


# ============================================================================
# PAGINATION
# ============================================================================


def get_next_page(html: str, current_url: str) -> Optional[str]:
    """
    Возвращает URL следующей страницы каталога.

    Основной селектор:
        .pager .pages a.next

    Если следующая страница отсутствует — возвращается None.
    """
    if not html:
        return None

    try:
        # Проверяем именно ссылку с классом next внутри pager/pages.
        pattern = (
            r'<a[^>]*class=["\'][^"\']*\bnext\b[^"\']*["\']'
            r'[^>]*href=["\']([^"\']+)["\']'
        )

        matches = re.findall(
            pattern,
            html,
            flags=re.IGNORECASE,
        )

        if not matches:
            # Некоторые шаблоны могут менять порядок href/class.
            pattern_reverse = (
                r'<a[^>]*href=["\']([^"\']+)["\'][^>]*'
                r'class=["\'][^"\']*\bnext\b[^"\']*["\']'
            )

            matches = re.findall(
                pattern_reverse,
                html,
                flags=re.IGNORECASE,
            )

        if not matches:
            return None

        next_url = _absolute_url(matches[0], current_url)

        if not next_url:
            return None

        if next_url == current_url:
            return None

        return next_url

    except Exception as exc:
        _log(
            "error",
            f"Ошибка определения следующей страницы после {current_url}: {exc}",
        )
        return None


# ============================================================================
# RAW PRODUCT
# ============================================================================


def build_raw_product(
    html: str,
    url: str,
    downloaded_images: List[str],
) -> Dict[str, Any]:
    """
    Формирует минимальную сырую структуру товара.

    Бизнес-поля не извлекаются из HTML: это делает parser.py.

    URL и список локальных изображений сохраняются для последующего
    использования parser/exporter.
    """
    return {
        "URL": url,
        "html": html,
        "downloaded_images": downloaded_images,
    }


# ============================================================================
# MAIN SCRAPER ENTRY POINT
# ============================================================================


def fetch_page_data(engine: PlaywrightEngine) -> List[str]:
    """
    Полный обход каталога.

    Возвращает список сырого HTML страниц товаров.

    Порядок работы:
        BASE_URL
          -> listing HTML
          -> product URLs
          -> product HTML
          -> следующая listing page
          -> повтор

    DOM-парсинг и извлечение полей товара здесь не выполняются.
    """
    raw_pages: List[str] = []

    current_url = BASE_URL
    visited_pages = set()
    product_urls_seen = set()

    while current_url:
        if current_url in visited_pages:
            _log(
                "warning",
                f"Обнаружена повторная страница каталога, остановка: {current_url}",
            )
            break

        visited_pages.add(current_url)

        try:
            _log("info", f"Загрузка страницы каталога: {current_url}")

            listing_html = fetch_listing_page(
                engine,
                current_url,
            )

            if not listing_html:
                _log(
                    "warning",
                    f"Не удалось получить HTML каталога: {current_url}",
                )
                break

            product_urls = extract_product_urls(listing_html)

            if not product_urls:
                _log(
                    "warning",
                    f"На странице каталога не найдено товаров: {current_url}",
                )

            for product_url in product_urls:
                if product_url in product_urls_seen:
                    continue

                product_urls_seen.add(product_url)

                try:
                    _log("info", f"Загрузка товара: {product_url}")

                    product_html = fetch_product_page(
                        engine,
                        product_url,
                    )

                    if not product_html:
                        _log(
                            "warning",
                            f"Пропуск товара с пустым HTML: {product_url}",
                        )
                        continue

                    # Сохраняем сырой HTML именно как результат scraper.
                    # Извлечение полей остаётся parser.py.
                    raw_pages.append(product_html)

                except Exception as product_exc:
                    _log(
                        "error",
                        f"Ошибка обработки товара {product_url}: {product_exc}",
                    )
                    continue

        except Exception as page_exc:
            _log(
                "error",
                f"Ошибка обработки страницы каталога {current_url}: {page_exc}",
            )
            break

        try:
            next_url = get_next_page(
                listing_html,
                current_url,
            )
        except Exception as pagination_exc:
            _log(
                "error",
                f"Ошибка пагинации {current_url}: {pagination_exc}",
            )
            break

        if not next_url:
            break

        if next_url in visited_pages:
            _log(
                "warning",
                f"Следующая страница уже посещалась: {next_url}",
            )
            break

        current_url = next_url

    _log(
        "info",
        f"Скрапинг завершён: страниц товаров собрано={len(raw_pages)}, "
        f"уникальных URL товаров={len(product_urls_seen)}, "
        f"страниц каталога={len(visited_pages)}",
    )

    return raw_pages
Как протестировать локально
Bash
python -m py_compile app/scraper.py

Затем, из корня проекта, запустить штатный сценарий проекта:

Bash
python main.py

fetch_page_data() намеренно возвращает именно List[str] сырого HTML, поэтому извлечение 11 полей DS-PRK-Scraper.json должно оставаться в parser.py; дополнительные поля в результат scraper не добавляются.