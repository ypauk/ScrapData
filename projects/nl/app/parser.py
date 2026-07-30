#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Парсер товаров с сайта professionele-koeling.nl.

Модуль отвечает за извлечение структурированных данных из HTML-кода:
1. Извлечение ссылок на товары из HTML категории (parse_listing)
2. Парсинг отдельных страниц товаров (parse_product)
3. Разворачивание характеристик (Extra informatie) в отдельные колонки
4. Нормализация цен, текста, URL через централизованные утилиты

Сигнатура parse_html_data(html_contents) сохраняется для совместимости
с main.py, который передаёт список сырых HTML-строк.
"""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.html_parser import HtmlParser
from app.data_normalizer import DataNormalizer
from app.utils import log_message, clean_price


def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Извлекает URL первых двух товаров из HTML-кода страницы категории.
    Возвращает список словарей с URL и заголовком для совместимости с BatchWriter.

    Args:
        html: Строка сырого HTML-кода страницы категории.

    Returns:
        List[Dict[str, Any]]: Список словарей с полями URL и Title.
                   Возвращает пустой список, если товары не найдены.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        log_message("error", f"[{__file__}] parse_listing: невалидный HTML")
        return []

    # Найти все карточки товаров
    cards = HtmlParser.find_all(soup, "li", class_="item")
    
    if not cards:
        log_message("warning", f"[{__file__}] parse_listing: карточки товаров не найдены")
        return []

    log_message("info", f"[{__file__}] parse_listing: найдено карточек: {len(cards)}")

    products = []
    for card in cards[:2]:  # Берём только первые два товара
        link = HtmlParser.find(card, "a", class_="product-image")
        if link:
            href = HtmlParser.get_attr(link, "href")
            if href:
                # Извлекаем название товара для информации
                title_elem = HtmlParser.find(card, "h2", class_="product-name")
                if title_elem:
                    title_link = HtmlParser.find(title_elem, "a")
                    title = HtmlParser.get_text(title_link) if title_link else ""
                else:
                    title = ""
                
                products.append({
                    "URL": href,
                    "Title": title.strip()
                })

    log_message("info", f"[{__file__}] parse_listing: извлечено товаров: {len(products)}")
    return products


def parse_specs(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Извлекает характеристики товара из таблицы Extra informatie.

    Args:
        soup: BeautifulSoup объект HTML-кода страницы товара.

    Returns:
        Dict[str, Any]: Словарь с характеристиками {название: значение}.
    """
    specs = {}

    # Найти таблицу характеристик
    specs_table = HtmlParser.find(soup, "table", id="product-attribute-specs-table")
    if not specs_table:
        log_message("warning", f"[{__file__}] parse_specs: таблица характеристик не найдена")
        return specs

    # Извлечь все строки таблицы
    rows = HtmlParser.find_all(specs_table, "tr")
    for row in rows:
        th = HtmlParser.find(row, "th", class_="label")
        td = HtmlParser.find(row, "td", class_="data")
        
        if th and td:
            key = HtmlParser.get_text(th, default="").strip()
            value = HtmlParser.get_text(td, default="").strip()
            if key and value:
                specs[key] = value

    log_message("debug", f"[{__file__}] parse_specs: извлечено характеристик: {len(specs)}")
    return specs


def parse_product(html: str, url: str) -> Dict[str, Any]:
    """
    Извлекает все данные из HTML-кода страницы товара.

    Args:
        html: Строка сырого HTML-кода страницы товара.
        url: URL страницы товара.

    Returns:
        Dict[str, Any]: Словарь с данными товара.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        log_message("error", f"[{__file__}] parse_product: невалидный HTML для {url}")
        return {}

    result = {"URL": url}

    # 1. Breadcrumb (хлебные крошки)
    breadcrumb_items = []
    breadcrumb = HtmlParser.find(soup, "div", class_="breadcrumbs")
    if breadcrumb:
        links = HtmlParser.find_all(breadcrumb, "a")
        for link in links:
            text = HtmlParser.get_text(link, default="").strip()
            if text:
                breadcrumb_items.append(text)
        # Добавляем последний элемент (текущая страница) если есть
        last_crumb = HtmlParser.find(breadcrumb, "span", class_="last-crumb")
        if last_crumb:
            breadcrumb_items.append(HtmlParser.get_text(last_crumb, default="").strip())
    
    result["Breadcrumb"] = " > ".join(breadcrumb_items) if breadcrumb_items else ""

    # 2. Title (заголовок)
    title_elem = HtmlParser.find(soup, "h1", itemprop="name")
    result["Title"] = HtmlParser.get_text(title_elem, default="").strip()

    # 3. Short description (краткое описание)
    short_desc = HtmlParser.find(soup, "div", class_="short-description")
    if short_desc:
        desc_elem = HtmlParser.find(short_desc, "div", class_="std")
        result["Short description"] = HtmlParser.get_text(desc_elem, default="").strip()
    else:
        result["Short description"] = ""

    # 4. Image URL (изображение)
    # Ищем оригинальное изображение через zoom-inside или cloud-zoom
    img_url = ""
    image_container = HtmlParser.find(soup, "p", class_="product-image")
    if image_container:
        zoom_link = HtmlParser.find(image_container, "a", class_="cloud-zoom")
        if zoom_link:
            img_url = HtmlParser.get_attr(zoom_link, "href")
    
    if not img_url:
        # Fallback: ищем любую картинку в product-image
        img_elem = HtmlParser.find(soup, "img", class_="gallery-image")
        if img_elem:
            img_url = HtmlParser.get_attr(img_elem, "src")
    
    result["imageurl"] = img_url or ""

    # 5. Image name (имя файла)
    if img_url:
        result["image_name"] = img_url.split("/")[-1] if "/" in img_url else ""
    else:
        result["image_name"] = ""

    # 6. Price (старая цена) и Sale price (скидочная цена)
    price_box = HtmlParser.find(soup, "div", class_="price-box")
    result["Price"] = None
    result["Sale price"] = None

    if price_box:
        # Обычная цена
        old_price_elem = HtmlParser.find(price_box, "span", class_="old-price")
        if old_price_elem:
            price_span = HtmlParser.find(old_price_elem, "span", class_="price")
            if price_span:
                price_text = HtmlParser.get_text(price_span, default="").strip()
                if price_text:
                    cleaned = DataNormalizer.normalize_price(price_text)
                    result["Price"] = cleaned if cleaned is not None else price_text

        # Скидочная цена
        special_price_elem = HtmlParser.find(price_box, "span", class_="special-price")
        if special_price_elem:
            price_span = HtmlParser.find(special_price_elem, "span", class_="price")
            if price_span:
                price_text = HtmlParser.get_text(price_span, default="").strip()
                if price_text:
                    cleaned = DataNormalizer.normalize_price(price_text)
                    result["Sale price"] = cleaned if cleaned is not None else price_text

    # 7. Description (полное описание из вкладки Productbeschrijving)
    description = ""
    description_panel = HtmlParser.find(soup, "div", id="product-tabs")
    if description_panel:
        # Ищем панель с описанием (скрыта по умолчанию, но HTML присутствует)
        panels = HtmlParser.find_all(description_panel, "div", class_="panel")
        for panel in panels:
            # Проверяем, что это панель описания (может содержать заголовок h2)
            if panel.get("style") == "display: block;" or panel.find("h2"):
                desc_elem = HtmlParser.find(panel, "div", class_="std")
                if desc_elem:
                    description = HtmlParser.get_text(desc_elem, default="").strip()
                    break
    
    if not description:
        # Fallback: ищем любой блок с описанием
        desc_block = HtmlParser.find(soup, "div", class_="product-description")
        if desc_block:
            description = HtmlParser.get_text(desc_block, default="").strip()
    
    result["Description"] = description

    # 8. Specs (характеристики) - разворачиваем в отдельные поля
    specs = parse_specs(soup)
    
    # Добавляем все характеристики в результат
    for key, value in specs.items():
        result[key] = value

    # 9. Дополнительно: извлекаем наличие (availability) из страницы
    availability_elem = HtmlParser.find(soup, "p", class_="availability")
    if availability_elem:
        availability_text = HtmlParser.get_text(availability_elem, default="").strip()
        result["Availability"] = availability_text
    else:
        result["Availability"] = ""

    return result


def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Точка интеграции с главным оркестратором main.py.
    Принимает список сырых HTML-строк, извлекает URL товаров из первой страницы
    и парсит все переданные страницы товаров.

    Args:
        html_contents: Список строк сырого HTML-кода.
                      Ожидается, что первый элемент — HTML категории,
                      остальные — HTML страниц товаров.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными товаров.
    """
    if not html_contents:
        log_message("warning", f"[{__file__}] parse_html_data: список HTML пуст")
        return []

    log_message("info", f"[{__file__}] parse_html_data: обработка {len(html_contents)} HTML-строк")

    # Первая строка — HTML категории, извлекаем URL товаров
    category_html = html_contents[0]
    product_infos = parse_listing(category_html)
    
    if not product_infos:
        log_message("error", f"[{__file__}] parse_html_data: не удалось извлечь товары")
        return []

    log_message("info", f"[{__file__}] parse_html_data: найдено товаров: {len(product_infos)}")

    results = []
    # Остальные HTML-строки — страницы товаров (может быть 1 или 2)
    # Используем их последовательно для парсинга каждого товара
    for idx, html in enumerate(html_contents[1:], 0):
        if idx >= len(product_infos):
            break
        
        try:
            url = product_infos[idx]["URL"]
            # Если есть переданный HTML для этого товара — парсим его
            product_data = parse_product(html, url)
            if product_data:
                results.append(product_data)
                log_message("debug", f"[{__file__}] parse_html_data: успешно спарсен товар #{idx+1}: {product_data.get('Title', 'N/A')}")
        except Exception as e:
            log_message("error", f"[{__file__}] parse_html_data: ошибка парсинга товара #{idx+1}: {e}")

    log_message("info", f"[{__file__}] parse_html_data: завершено, получено товаров: {len(results)}")
    return results


# Алиас для совместимости с другими частями кода
# (parse_html_data уже используется в main.py)