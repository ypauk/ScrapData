#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль parser — извлечение структурированных данных из HTML-страниц.

Отвечает только за парсинг HTML и извлечение данных.
Использует BeautifulSoup для работы с DOM.

Не выполняет сетевые запросы — только обрабатывает переданный HTML.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup

from app.utils import clean_price, log_message


def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Парсит страницу категории и извлекает данные товаров.

    На странице категории находятся карточки товаров с краткой информацией.
    Извлекает URL, Title, Price, Sale price, imageurl для каждого товара.

    Args:
        html: HTML страницы категории

    Returns:
        List[Dict[str, Any]]: Список словарей с данными товаров
    """
    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        results = []

        # Ищем все карточки товаров на странице категории
        items = soup.find_all("li", class_="item")

        if not items:
            log_message("warning", f"[{__file__}] На странице не найдены карточки товаров (li.item)")
            return []

        log_message("info", f"[{__file__}] Найдено {len(items)} карточек товаров")

        for item in items:
            try:
                product_data = parse_listing_item(item)
                if product_data:
                    results.append(product_data)
            except Exception as e:
                log_message("error", f"[{__file__}] Ошибка при парсинге карточки: {e}")
                continue

        return results

    except Exception as e:
        log_message("error", f"[{__file__}] Ошибка при парсинге страницы категории: {e}")
        return []


def parse_listing_item(item) -> Optional[Dict[str, Any]]:
    """
    Парсит одну карточку товара на странице категории.

    Извлекает базовую информацию: URL, Title, изображение, цены.

    Args:
        item: BeautifulSoup элемент карточки товара (li.item)

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными товара или None
    """
    try:
        # 1. Извлечение URL товара
        product_url = None
        title_link = item.find("a", class_="product-image")
        if not title_link:
            title_elem = item.find("h2", class_="product-name")
            if title_elem:
                title_link = title_elem.find("a")

        if title_link and title_link.get("href"):
            product_url = title_link.get("href")
            if product_url.startswith("/"):
                product_url = "https://www.professionele-koeling.nl" + product_url

        if not product_url:
            log_message("warning", f"[{__file__}] Не найден URL товара в карточке")
            return None

        # 2. Извлечение Title
        title = ""
        title_elem = item.find("h2", class_="product-name")
        if title_elem:
            title_link = title_elem.find("a")
            if title_link:
                title = title_link.get_text(strip=True)

        # 3. Извлечение изображения
        image_url = ""
        image_wrapper = item.find("div", class_="product-image-wrapper")
        if image_wrapper:
            img = image_wrapper.find("img")
            if img and img.get("src"):
                image_url = img.get("src")
                if image_url.startswith("/"):
                    image_url = "https://www.professionele-koeling.nl" + image_url

        # 4. Извлечение цен
        price_box = item.find("div", class_="price-box")
        regular_price = None
        sale_price = None

        if price_box:
            # Обычная цена (old-price)
            old_price_elem = price_box.find("p", class_="old-price")
            if old_price_elem:
                price_span = old_price_elem.find("span", class_="price")
                if price_span:
                    raw_price = price_span.get_text(strip=True)
                    regular_price = clean_price(raw_price)

            # Акционная цена (special-price)
            special_price_elem = price_box.find("p", class_="special-price")
            if special_price_elem:
                price_span = special_price_elem.find("span", class_="price")
                if price_span:
                    raw_price = price_span.get_text(strip=True)
                    sale_price = clean_price(raw_price)

        # Если нет специальной цены, то sale_price = regular_price (или None)
        if sale_price is None:
            sale_price = regular_price

        return {
            "URL": product_url,
            "Breadcrumb": "",
            "Title": title,
            "Short description": "",
            "imageurl": image_url,
            "image_name": extract_image_name(image_url),
            "Price": regular_price,
            "Sale price": sale_price,
            "Description": "",
            "Specs": "",
            "Spec_detail": ""
        }

    except Exception as e:
        log_message("error", f"[{__file__}] Ошибка при парсинге карточки товара: {e}")
        return None


def parse_product(html: str, base_url: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Парсит страницу товара и извлекает все необходимые поля.

    Args:
        html: HTML страницы товара
        base_url: Базовый URL для построения абсолютных ссылок

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными товара или None
    """
    if not html:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")

        # 1. URL страницы
        url = extract_url(soup, base_url)

        # 2. Breadcrumb
        breadcrumb = extract_breadcrumb(soup)

        # 3. Title
        title = extract_title(soup)

        # 4. Short description
        short_desc = extract_short_description(soup)

        # 5. Изображения
        image_urls, image_names = extract_images(soup)

        # 6. Цены
        regular_price, sale_price = extract_prices(soup)

        # 7. Description
        description = extract_description(soup)

        # 8. Specs и Spec_detail
        specs, spec_details = extract_specs(soup)

        return {
            "URL": url or "",
            "Breadcrumb": breadcrumb,
            "Title": title,
            "Short description": short_desc,
            "imageurl": ",".join(image_urls) if image_urls else "",
            "image_name": ",".join(image_names) if image_names else "",
            "Price": regular_price,
            "Sale price": sale_price,
            "Description": description,
            "Specs": specs,
            "Spec_detail": spec_details
        }

    except Exception as e:
        log_message("error", f"[{__file__}] Ошибка при парсинге страницы товара: {e}")
        return None


def extract_url(soup: BeautifulSoup, base_url: Optional[str] = None) -> Optional[str]:
    """
    Извлекает URL страницы товара.

    Args:
        soup: BeautifulSoup объект
        base_url: Базовый URL

    Returns:
        Optional[str]: URL страницы
    """
    # Пробуем найти canonical URL
    canonical = soup.find("link", {"rel": "canonical"})
    if canonical and canonical.get("href"):
        return canonical.get("href")

    # Пробуем найти через meta og:url
    og_url = soup.find("meta", {"property": "og:url"})
    if og_url and og_url.get("content"):
        return og_url.get("content")

    # Если есть base_url, возвращаем его
    if base_url:
        return base_url

    return None


def extract_breadcrumb(soup: BeautifulSoup) -> str:
    """
    Извлекает хлебные крошки.

    Args:
        soup: BeautifulSoup объект

    Returns:
        str: Строка breadcrumb (разделитель - пробел)
    """
    try:
        # Ищем breadcrumb на сайте
        breadcrumb_container = soup.find("div", class_="breadcrumbs")
        if not breadcrumb_container:
            return ""

        # Собираем все ссылки и текст в breadcrumb
        crumbs = []
        for li in breadcrumb_container.find_all("li"):
            # Пропускаем последний элемент (текущая страница) с классом "current"
            if li.get("class") and "current" in li.get("class"):
                continue

            text = li.get_text(strip=True)
            if text:
                crumbs.append(text)

        # Если нет breadcrumb, пробуем альтернативный вариант
        if not crumbs:
            breadcrumb_items = breadcrumb_container.find_all("span")
            for item in breadcrumb_items:
                if item.get_text(strip=True):
                    crumbs.append(item.get_text(strip=True))

        return " ".join(crumbs) if crumbs else ""

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении breadcrumb: {e}")
        return ""


def extract_title(soup: BeautifulSoup) -> str:
    """
    Извлекает заголовок товара (h1).

    Args:
        soup: BeautifulSoup объект

    Returns:
        str: Заголовок товара
    """
    try:
        # Ищем h1 с классом product-name или просто h1
        title_elem = soup.find("h1", class_="product-name")
        if not title_elem:
            title_elem = soup.find("h1")

        if title_elem:
            return title_elem.get_text(strip=True)

        # Альтернатива: meta title
        meta_title = soup.find("meta", {"property": "og:title"})
        if meta_title and meta_title.get("content"):
            return meta_title.get("content")

        return ""

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении заголовка: {e}")
        return ""


def extract_short_description(soup: BeautifulSoup) -> str:
    """
    Извлекает краткое описание товара.

    Args:
        soup: BeautifulSoup объект

    Returns:
        str: Краткое описание
    """
    try:
        # Ищем блок краткого описания
        short_desc_elem = soup.find("div", class_="short-description")
        if short_desc_elem:
            return short_desc_elem.get_text(strip=True)

        # Альтернатива: meta description
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc.get("content")

        return ""

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении краткого описания: {e}")
        return ""


def extract_images(soup: BeautifulSoup) -> Tuple[List[str], List[str]]:
    """
    Извлекает все изображения товара.

    Args:
        soup: BeautifulSoup объект

    Returns:
        Tuple[List[str], List[str]]: (список URL изображений, список имен файлов)
    """
    image_urls = []
    image_names = []

    try:
        # Ищем главное изображение
        main_img = soup.find("img", {"id": "image-main"})
        if not main_img:
            main_img = soup.find("img", class_="product-image")

        if main_img and main_img.get("src"):
            img_url = main_img.get("src")
            if img_url.startswith("/"):
                img_url = "https://www.professionele-koeling.nl" + img_url
            image_urls.append(img_url)
            image_names.append(extract_image_name(img_url))

        # Ищем дополнительные изображения в галерее
        gallery = soup.find("div", class_="product-image-gallery")
        if gallery:
            for img in gallery.find_all("img"):
                if img.get("src"):
                    img_url = img.get("src")
                    # Проверяем, не добавлено ли уже это изображение
                    if img_url not in image_urls:
                        if img_url.startswith("/"):
                            img_url = "https://www.professionele-koeling.nl" + img_url
                        image_urls.append(img_url)
                        image_names.append(extract_image_name(img_url))

        # Если не нашли галерею, ищем все изображения в описании
        if not image_urls:
            description = soup.find("div", class_="product-description")
            if description:
                for img in description.find_all("img"):
                    if img.get("src"):
                        img_url = img.get("src")
                        if img_url.startswith("/"):
                            img_url = "https://www.professionele-koeling.nl" + img_url
                        image_urls.append(img_url)
                        image_names.append(extract_image_name(img_url))

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении изображений: {e}")

    return image_urls, image_names


def extract_image_name(image_url: str) -> str:
    """
    Извлекает имя файла из URL изображения.

    Args:
        image_url: URL изображения

    Returns:
        str: Имя файла изображения
    """
    if not image_url:
        return ""

    try:
        # Парсим URL и берем последнюю часть пути
        parsed = urlparse(image_url)
        path = parsed.path
        filename = os.path.basename(path)

        # Декодируем URL-encoded символы
        filename = unquote(filename)

        # Удаляем параметры запроса
        if "?" in filename:
            filename = filename.split("?")[0]

        # Если имя пустое или содержит только расширение
        if not filename or filename == "/":
            return ""

        return filename

    except Exception:
        return ""


def extract_prices(soup: BeautifulSoup) -> Tuple[Optional[float], Optional[float]]:
    """
    Извлекает обычную и акционную цену.

    Args:
        soup: BeautifulSoup объект

    Returns:
        Tuple[Optional[float], Optional[float]]: (обычная цена, акционная цена)
    """
    regular_price = None
    sale_price = None

    try:
        # Ищем блок цен
        price_box = soup.find("div", class_="price-box")
        if not price_box:
            # Пробуем найти цены напрямую
            price_elem = soup.find("span", class_="price")
            if price_elem:
                raw_price = price_elem.get_text(strip=True)
                regular_price = clean_price(raw_price)
                return regular_price, regular_price

        # Обычная цена (old-price)
        old_price_elem = price_box.find("p", class_="old-price")
        if old_price_elem:
            price_span = old_price_elem.find("span", class_="price")
            if price_span:
                raw_price = price_span.get_text(strip=True)
                regular_price = clean_price(raw_price)

        # Акционная цена (special-price)
        special_price_elem = price_box.find("p", class_="special-price")
        if special_price_elem:
            price_span = special_price_elem.find("span", class_="price")
            if price_span:
                raw_price = price_span.get_text(strip=True)
                sale_price = clean_price(raw_price)

        # Если нет специальной цены, используем обычную
        if sale_price is None:
            sale_price = regular_price

        # Если обычная цена не найдена, пытаемся найти любую цену
        if regular_price is None:
            price_elem = price_box.find("span", class_="price")
            if price_elem:
                raw_price = price_elem.get_text(strip=True)
                regular_price = clean_price(raw_price)
                if sale_price is None:
                    sale_price = regular_price

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении цен: {e}")

    return regular_price, sale_price


def extract_description(soup: BeautifulSoup) -> str:
    """
    Извлекает полное описание товара.

    Args:
        soup: BeautifulSoup объект

    Returns:
        str: Полное описание (текст, без HTML)
    """
    try:
        # Ищем блок описания
        description_container = soup.find("div", class_="product-description")
        if not description_container:
            # Пробуем другие варианты
            description_container = soup.find("div", class_="description")
            if not description_container:
                description_container = soup.find("div", class_="product-details")

        if description_container:
            # Удаляем блоки "Uitvoering" и "Specificaties" если они есть внутри описания
            # (это будет обработано в extract_specs)
            text = description_container.get_text(separator="\n", strip=True)
            # Нормализуем пробелы
            text = re.sub(r"\n\s*\n", "\n\n", text)
            return text

        # Альтернатива: meta description
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc.get("content")

        return ""

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении описания: {e}")
        return ""


def extract_specs(soup: BeautifulSoup) -> Tuple[str, str]:
    """
    Извлекает характеристики товара (Specs и Spec_detail).

    Specs: названия характеристик (текст до ":")
    Spec_detail: значения характеристик (текст после ":")

    Все Specs объединяются в одну строку через пробел.
    Все Spec_detail объединяются в одну строку через пробел.

    Args:
        soup: BeautifulSoup объект

    Returns:
        Tuple[str, str]: (Specs, Spec_detail)
    """
    specs_list = []
    spec_details_list = []

    try:
        # Ищем блок спецификаций
        spec_container = None

        # Вариант 1: блок с классом "product-specs" или "specifications"
        spec_container = soup.find("div", class_="product-specs")
        if not spec_container:
            spec_container = soup.find("div", class_="specifications")
        if not spec_container:
            spec_container = soup.find("div", class_="specs")

        if spec_container:
            # Ищем все элементы с характеристиками
            # Обычно это dl (definition list) или таблица
            for item in spec_container.find_all(["dt", "th", "label"]):
                spec_name = item.get_text(strip=True)
                # Ищем соответствующее значение
                value_elem = None
                if item.name == "dt":
                    value_elem = item.find_next_sibling("dd")
                elif item.name == "th":
                    # Ищем следующую ячейку в строке
                    tr = item.find_parent("tr")
                    if tr:
                        tds = tr.find_all("td")
                        if len(tds) > 0:
                            value_elem = tds[0]
                elif item.name == "label":
                    # Ищем связанный элемент
                    value_elem = item.find_next_sibling()

                if value_elem:
                    spec_value = value_elem.get_text(strip=True)
                    specs_list.append(spec_name)
                    spec_details_list.append(spec_value)

            # Если не нашли в dl/table, ищем строки с двоеточием
            if not specs_list:
                for text_node in spec_container.find_all(text=True):
                    text = str(text_node).strip()
                    if ":" in text:
                        parts = text.split(":", 1)
                        if len(parts) == 2:
                            spec_name = parts[0].strip()
                            spec_value = parts[1].strip()
                            if spec_name and spec_value:
                                specs_list.append(spec_name)
                                spec_details_list.append(spec_value)

        # Если не нашли блок спецификаций, ищем в описании
        if not specs_list:
            description = soup.find("div", class_="product-description")
            if description:
                # Ищем строки с двоеточием
                for text_node in description.find_all(text=True):
                    text = str(text_node).strip()
                    if ":" in text:
                        parts = text.split(":", 1)
                        if len(parts) == 2:
                            spec_name = parts[0].strip()
                            spec_value = parts[1].strip()
                            # Фильтруем слишком длинные значения (это может быть не Spec)
                            if spec_name and spec_value and len(spec_value) < 200:
                                specs_list.append(spec_name)
                                spec_details_list.append(spec_value)

    except Exception as e:
        log_message("warning", f"[{__file__}] Ошибка при извлечении характеристик: {e}")

    # Объединяем все Specs в одну строку через пробел
    specs = " ".join(specs_list) if specs_list else ""

    # Объединяем все Spec_detail в одну строку через пробел
    spec_details = " ".join(spec_details_list) if spec_details_list else ""

    return specs, spec_details


def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Главная точка входа для парсинга, вызываемая из main.py.

    Принимает список HTML-строк (страниц товаров) и возвращает список
    словарей с извлеченными данными.

    Args:
        html_contents: Список HTML-строк страниц товаров

    Returns:
        List[Dict[str, Any]]: Список словарей с данными товаров
    """
    if not html_contents:
        log_message("warning", f"[{__file__}] Получен пустой список HTML для парсинга")
        return []

    log_message("info", f"[{__file__}] Начало парсинга {len(html_contents)} страниц товаров")

    all_results = []
    for idx, html in enumerate(html_contents, 1):
        try:
            # Проверяем, является ли HTML страницей категории (содержит li.item)
            if "li class=\"item\"" in html or '<li class="item"' in html:
                # Это страница категории, парсим как категорию
                page_results = parse_listing(html)
                all_results.extend(page_results)
            else:
                # Это страница товара
                product_data = parse_product(html)
                if product_data:
                    all_results.append(product_data)
                else:
                    log_message("warning", f"[{__file__}] Не удалось извлечь данные из страницы #{idx}")

        except Exception as e:
            log_message("error", f"[{__file__}] Ошибка при парсинге страницы #{idx}: {e}")
            continue

    log_message("info", f"[{__file__}] Парсинг завершен. Извлечено {len(all_results)} товаров")
    return all_results


# Добавляем недостающий импорт
import os
from urllib.parse import urlparse, unquote