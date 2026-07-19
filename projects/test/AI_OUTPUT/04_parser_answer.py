#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.utils import clean_price


def parse_single_item(card) -> Dict[str, Any]:
    """
    Извлекает целевые поля из структуры одной карточки объявления.
    
    Args:
        card (bs4.element.Tag): Объект тега одной карточки объявления.
        
    Returns:
        dict: Словарь с извлеченными данными объявления.
    """
    card_id = card.get("id", "unknown")
    result = {
        "title": "",
        "price": 0.0,
        "fuel": "",
        "city": "",
        "image_url": ""
    }
    
    try:
        # 1. URL картинки (img внутри picture)
        picture = card.find("picture")
        if picture:
            img = picture.find("img")
            if img and img.get("src"):
                result["image_url"] = img.get("src")
            elif img and img.get("data-src"):
                result["image_url"] = img.get("data-src")
        
        # 2. Название авто (div.titleS)
        title_elem = card.find("div", class_="titleS")
        if title_elem:
            result["title"] = title_elem.get_text(strip=True)
        
        # 3. Цена (span.c-green)
        price_elem = card.find("span", class_="c-green")
        if price_elem:
            raw_price = price_elem.get_text(strip=True)
            try:
                result["price"] = clean_price(raw_price)
            except Exception as e:
                print(f"[{__file__}] Ошибка очистки цены '{raw_price}' в карточке {card_id}: {e}")
        
        # 4. Топливо и Город (из grid-wrapper)
        grid_wrapper = card.find("div", class_="grid-wrapper")
        if grid_wrapper:
            # Находим все строки с информацией внутри grid-wrapper
            info_rows = grid_wrapper.find_all("div", class_="structure-row", recursive=False)
            
            # Топливо - 3-й по счету div (индекс 2)
            if len(info_rows) >= 3:
                fuel_row = info_rows[2]
                # Извлекаем текст из span
                fuel_span = fuel_row.find("span", class_="body")
                if fuel_span:
                    result["fuel"] = fuel_span.get_text(strip=True)
            
            # Город - 4-й по счету div (индекс 3)
            if len(info_rows) >= 4:
                city_row = info_rows[3]
                city_span = city_row.find("span", class_="body")
                if city_span:
                    result["city"] = city_span.get_text(strip=True)
    
    except Exception as e:
        print(f"[{__file__}] Ошибка при парсинге карточки {card_id}: {e}")
    
    return result


def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Инициализирует BS4, находит коллекцию всех карточек автомобилей на странице 
    и передает каждую в parse_single_item.
    
    Args:
        html (str): Строка сырого HTML-кода страницы.
        
    Returns:
        List[Dict[str, Any]]: Список словарей с данными по автомобилям.
    """
    if not html or not html.strip():
        print(f"[{__file__}] Ошибка: Передан пустой HTML-контент.")
        return []
    
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        # Ищем все карточки по селектору из project_plan.md
        cards = soup.find_all("a", class_="link", class_="product-card", class_="horizontal")
        
        # Альтернативный поиск, если предыдущий не сработал (BeautifulSoup может не обработать несколько классов)
        if not cards:
            cards = soup.find_all("a", {"class": ["link", "product-card", "horizontal"]})
        
        # Если все еще не найдены, пробуем найти по наличию всех классов через селектор CSS
        if not cards:
            cards = soup.select("a.link.product-card.horizontal")
        
        if not cards:
            print(f"[{__file__}] Предупреждение: Карточки объявлений на странице не найдены.")
            return []
        
        print(f"[{__file__}] Найдено карточек для парсинга: {len(cards)}")
        
        results = []
        for card in cards:
            try:
                item_data = parse_single_item(card)
                # Проверяем, что данные не пустые (хотя бы название или цена)
                if item_data["title"] or item_data["price"] > 0:
                    results.append(item_data)
                else:
                    card_id = card.get("id", "unknown")
                    print(f"[{__file__}] Пропуск карточки {card_id}: нет значимых данных")
            except Exception as e:
                card_id = card.get("id", "unknown")
                print(f"[{__file__}] Критическая ошибка при парсинге карточки ID {card_id}: {e}")
                continue
        
        return results
        
    except Exception as e:
        print(f"[{__file__}] Ошибка при инициализации парсинга: {e}")
        return []


def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Точка интеграции с главным оркестратором main.py. 
    Принимает список строк HTML и возвращает агрегированные результаты.
    
    Args:
        html_contents (List[str]): Список строк сырого HTML.
        
    Returns:
        List[Dict[str, Any]]: Общий список спарсенных данных.
    """
    all_results = []
    print(f"[{__file__}] Начало обработки {len(html_contents)} страниц(ы)...")
    
    for idx, html in enumerate(html_contents, 1):
        try:
            page_results = parse_listing(html)
            all_results.extend(page_results)
            print(f"[{__file__}] Страница #{idx}: найдено {len(page_results)} объявлений")
        except Exception as e:
            print(f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
            continue
    
    print(f"[{__file__}] Парсинг успешно завершен. Всего собрано элементов: {len(all_results)}")
    return all_results


# Для локального тестирования модуля
if __name__ == "__main__":
    # Тест с локальным файлом page.html
    import os
    from app.config import AI_INPUT_DIR
    
    test_file = AI_INPUT_DIR / "page.html"
    
    if test_file.exists():
        print(f"[{__file__}] Тестовый запуск с файлом {test_file}")
        with open(test_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        results = parse_listing(html_content)
        print(f"\n[{__file__}] Результаты теста (первые 3 записи):")
        for i, item in enumerate(results[:3], 1):
            print(f"\n{i}. {item}")
        
        print(f"\n[{__file__}] Всего найдено: {len(results)} объявлений")
    else:
        print(f"[{__file__}] Файл {test_file} не найден для теста")