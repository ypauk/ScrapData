#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль scraper — сбор сырого HTML-контента с сайта professionele-koeling.nl.

Отвечает только за сетевые запросы, навигацию и пагинацию.
Использует requests + BeautifulSoup для обхода категории и получения HTML карточек товаров.

Не выполняет парсинг данных — только возвращает список HTML-строк для parser.py.
"""

import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from app.config import TIMEOUT, RETRY_COUNT, DEFAULT_USER_AGENT
from app.utils import random_delay


def fetch_listing_page(url: str) -> Optional[str]:
    """
    Получить HTML страницы категории.

    Args:
        url: URL страницы категории

    Returns:
        str: HTML страницы или None при ошибке
    """
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text

        except requests.exceptions.Timeout:
            print(f"[{__file__}] Таймаут при загрузке {url} (попытка {attempt + 1}/{RETRY_COUNT})")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"[{__file__}] Ошибка 403 (доступ запрещен) при загрузке {url}")
                return None
            print(f"[{__file__}] HTTP ошибка {e.response.status_code} при загрузке {url}")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке {url}: {e}")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

    print(f"[{__file__}] Не удалось загрузить {url} после {RETRY_COUNT} попыток")
    return None


def fetch_product_page(url: str) -> Optional[str]:
    """
    Получить HTML страницы товара.

    Args:
        url: URL страницы товара

    Returns:
        str: HTML страницы товара или None при ошибке
    """
    return fetch_listing_page(url)


def get_product_urls_from_listing(html: str) -> List[str]:
    """
    Извлечь URL товаров из HTML страницы категории.

    Args:
        html: HTML страницы категории

    Returns:
        List[str]: Список URL товаров
    """
    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        product_urls = []

        # Ищем все элементы с классом "item" (как в предоставленном HTML)
        items = soup.find_all("li", class_="item")

        for item in items:
            # Ищем ссылку внутри блока product-image-wrapper или h2.product-name
            link = item.find("a", class_="product-image")
            if not link:
                # Пробуем найти ссылку в заголовке
                title_link = item.find("h2", class_="product-name")
                if title_link:
                    link = title_link.find("a")

            if link and link.get("href"):
                url = link.get("href")
                # Преобразуем относительный URL в абсолютный
                if url.startswith("/"):
                    url = "https://www.professionele-koeling.nl" + url
                product_urls.append(url)

        print(f"[{__file__}] Найдено {len(product_urls)} товаров на странице")
        return product_urls

    except Exception as e:
        print(f"[{__file__}] Ошибка при извлечении URL товаров: {e}")
        return []


def get_next_page_url(html: str, current_url: str) -> Optional[str]:
    """
    Определить URL следующей страницы пагинации.

    Args:
        html: HTML текущей страницы
        current_url: URL текущей страницы (для построения абсолютных ссылок)

    Returns:
        str: URL следующей страницы или None
    """
    if not html:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")

        # Ищем ссылку "Next" или "Следующая"
        # На сайте могут быть разные варианты пагинации
        next_link = None

        # Вариант 1: пагинация с классом "next"
        next_link = soup.find("a", class_="next")
        if not next_link:
            # Вариант 2: любой элемент с текстом "Next" или "Следующая"
            for link in soup.find_all("a"):
                if link.get_text(strip=True).lower() in ["next", "следующая", "следующая страница", "›", "»"]:
                    next_link = link
                    break

        if next_link and next_link.get("href"):
            url = next_link.get("href")
            if url.startswith("/"):
                url = "https://www.professionele-koeling.nl" + url
            return url

        return None

    except Exception as e:
        print(f"[{__file__}] Ошибка при поиске следующей страницы: {e}")
        return None


def fetch_all_product_pages(start_url: str) -> List[str]:
    """
    Оркестрация обхода сайта: загружает все страницы категории и все карточки товаров.

    Алгоритм:
    1. Загрузить HTML страницы категории
    2. Извлечь URL товаров
    3. Для каждого URL товара загрузить HTML
    4. Если есть следующая страница категории, перейти на неё и повторить

    Args:
        start_url: URL начальной страницы категории

    Returns:
        List[str]: Список HTML страниц товаров
    """
    product_htmls = []
    current_url = start_url
    page_number = 1
    seen_urls = set()

    print(f"[{__file__}] Начало сбора данных с {start_url}")

    while current_url:
        print(f"[{__file__}] Загрузка страницы категории #{page_number}: {current_url}")

        # Загружаем страницу категории
        listing_html = fetch_listing_page(current_url)
        if not listing_html:
            print(f"[{__file__}] Не удалось загрузить страницу категории {current_url}")
            break

        # Извлекаем URL товаров
        product_urls = get_product_urls_from_listing(listing_html)

        if not product_urls:
            print(f"[{__file__}] На странице не найдено товаров")
            break

        print(f"[{__file__}] Найдено {len(product_urls)} товаров на странице #{page_number}")

        # Загружаем каждую карточку товара
        for idx, product_url in enumerate(product_urls, 1):
            if product_url in seen_urls:
                continue
            seen_urls.add(product_url)

            print(f"[{__file__}] Загрузка товара {idx}/{len(product_urls)}: {product_url}")

            # Задержка между запросами товаров
            if idx > 1:
                random_delay(1.0, 2.5)

            product_html = fetch_product_page(product_url)
            if product_html:
                product_htmls.append(product_html)
            else:
                print(f"[{__file__}] Не удалось загрузить товар {product_url}")

        # Ищем следующую страницу
        next_url = get_next_page_url(listing_html, current_url)
        if next_url and next_url != current_url:
            current_url = next_url
            page_number += 1

            # Задержка перед следующей страницей категории
            random_delay(1.5, 3.0)
        else:
            print(f"[{__file__}] Достигнут конец пагинации")
            break

    print(f"[{__file__}] Сбор данных завершен. Собрано {len(product_htmls)} карточек товаров")
    return product_htmls


def fetch_page_data(context=None) -> List[str]:
    """
    Главная точка входа для сбора данных, вызываемая из main.py.

    Args:
        context: Необязательный контекст браузера (для совместимости с main.py)

    Returns:
        List[str]: Список HTML страниц товаров
    """
    print(f"[{__file__}] Запуск сбора данных...")

    # Стартовый URL категории koelkasten-kisten
    start_url = "https://www.professionele-koeling.nl/koelkasten-kisten.html"

    try:
        product_htmls = fetch_all_product_pages(start_url)

        if not product_htmls:
            print(f"[{__file__}] Предупреждение: Не удалось собрать ни одной карточки товара")
            return []

        print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(product_htmls)}")
        return product_htmls

    except Exception as e:
        print(f"[{__file__}] Критическая ошибка при сборе данных: {e}")
        return []