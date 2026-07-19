#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

# Поля результата в соответствии с project_plan.md
RESULT_FIELDS = ["Image URL", "Car Name", "Price", "Fuel Type", "City"]


def parse_single_item(card: Tag) -> Optional[Dict[str, Any]]:
    """
    Извлекает данные из конкретной карточки автомобиля.

    Args:
        card (Tag): Объект тега одной карточки объявления (a.link.product-card).

    Returns:
        Optional[Dict[str, Any]]: Словарь с извлеченными данными или None в случае ошибки.
    """
    try:
        # 1. Image URL - из тега img внутри picture
        image_url = ""
        picture = card.find("picture")
        if picture:
            img = picture.find("img")
            if img and img.get("src"):
                image_url = img.get("src")
            elif img and img.get("data-src"):
                image_url = img.get("data-src")

        # 2. Car Name - из блока common-text size-16-20 titleS fw-bold mb-4
        car_name = ""
        name_element = card.find("div", class_="common-text size-16-20 titleS fw-bold mb-4")
        if name_element:
            car_name = name_element.get_text(strip=True)

        # 3. Price - из блока common-text titleM c-green
        price = ""
        price_element = card.find("span", class_="common-text titleM c-green")
        if price_element:
            price = price_element.get_text(strip=True)

        # 4. Fuel Type - из 3-го блока structure-row внутри grid-wrapper
        fuel_type = ""
        grid_wrapper = card.find("div", class_="grid-wrapper")
        if grid_wrapper:
            structure_rows = grid_wrapper.find_all("div", class_="structure-row ai-center gap-8 flex-1")
            if len(structure_rows) >= 3:
                fuel_element = structure_rows[2].find("span", class_="common-text ellipsis-1 body")
                if fuel_element:
                    fuel_type = fuel_element.get_text(strip=True)

        # 5. City - из 4-го блока structure-row внутри grid-wrapper
        city = ""
        if grid_wrapper:
            structure_rows = grid_wrapper.find_all("div", class_="structure-row ai-center gap-8 flex-1")
            if len(structure_rows) >= 4:
                city_element = structure_rows[3].find("span", class_="common-text ellipsis-1 body")
                if city_element:
                    city = city_element.get_text(strip=True)

        # Проверяем, что у нас есть хотя бы название (минимально валидная карточка)
        if not car_name:
            print(f"[{__file__}] Предупреждение: Карточка без названия, пропускаем")
            return None

        return {
            "Image URL": image_url,
            "Car Name": car_name,
            "Price": price,
            "Fuel Type": fuel_type,
            "City": city
        }

    except Exception as e:
        card_id = card.get("id", "unknown")
        print(f"[{__file__}] Ошибка при парсинге карточки ID {card_id}: {e}")
        return None


def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Ищет все карточки товаров в HTML-коде и извлекает данные из каждой.

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
        # Ищем все ссылки с классом product-card horizontal
        cards = soup.find_all("a", class_="link product-card horizontal")

        if not cards:
            print(f"[{__file__}] Предупреждение: Карточки объявлений на странице не найдены.")
            return []

        print(f"[{__file__}] Найдено карточек для парсинга: {len(cards)}")

        results = []
        for card in cards:
            item_data = parse_single_item(card)
            if item_data:
                results.append(item_data)

        print(f"[{__file__}] Успешно спарсено карточек: {len(results)}")
        return results

    except Exception as e:
        print(f"[{__file__}] Критическая ошибка при парсинге HTML: {e}")
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
            print(f"[{__file__}] Страница #{idx}: собрано {len(page_results)} элементов")
        except Exception as e:
            print(f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
            continue

    print(f"[{__file__}] Парсинг успешно завершен. Всего собрано элементов: {len(all_results)}")
    return all_results


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тестовый запуск parser...")

    # Читаем тестовый HTML из AI_INPUT
    from pathlib import Path
    test_html_path = Path(__file__).parent.parent / "AI_INPUT" / "page.html"

    if test_html_path.exists():
        with open(test_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        results = parse_listing(html_content)

        print(f"\n[{__file__}] Результаты парсинга (первые 3):")
        for i, item in enumerate(results[:3], 1):
            print(f"\n{i}. {item}")

        print(f"\n[{__file__}] Всего спарсено: {len(results)}")
    else:
        print(f"[{__file__}] Файл {test_html_path} не найден для теста")