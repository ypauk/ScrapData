Диагноз
В файле app/parser.py произошла синтаксическая ошибка SyntaxError на строке 22. В Python при вызове функций именованные аргументы (keyword arguments) не могут содержать дефис (-), так как интерпретатор воспринимает его как оператор вычитания (data минус testid). Для поиска элементов по нестандартным атрибутам с дефисами в BeautifulSoup необходимо использовать специальный аргумент attrs и передавать параметры в виде словаря.

Исправление
Полный исправленный код модуля app/parser.py:

Python
import os
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from app.utils import clean_price

def parse_single_item(card: BeautifulSoup) -> Dict[str, Any]:
    """
    Извлекает целевые поля (название, цена, топливо) из структуры одной карточки товара.
    
    Args:
        card (BeautifulSoup): Объект тега одной карточки объявления.
        
    Returns:
        dict: Словарь с извлеченными данными объявления.
    """
    # 1. Извлечение названия
    title_element = card.find("h4", class_="css-wlcw7o")
    title = title_element.get_text(strip=True) if title_element else ""
    
    # 2. Извлечение и очистка цены (исправлен синтаксис поиска по data-testid)
    price_element = card.find("p", attrs={"data-testid": "ad-price"})
    if price_element:
        raw_price = price_element.get_text(strip=True)
        try:
            price = clean_price(raw_price)
        except Exception as e:
            print(f"[{__file__}] Ошибка при очистке цены '{raw_price}': {e}")
            price = None
    else:
        print(f"[{__file__}] Предупреждение: Элемент цены не найден в карточке с ID {card.get('id')}")
        price = None
        
    # 3. Извлечение вида топлива
    fuel = ""
    params_container = card.find("div", class_="css-13vv2xi")
    if params_container:
        param_spans = params_container.find_all("span", class_="css-h59g4b")
        if len(param_spans) >= 3:
            fuel = param_spans[2].get_text(strip=True)
        else:
            print(f"[{__file__}] Предупреждение: Недостаточно параметров для извлечения топлива в карточке с ID {card.get('id')}")
            fuel = "Не указано"
            
    return {
        "title": title,
        "price": price,
        "fuel": fuel
    }

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
        
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="css-1sw7q4x")
    
    if not cards:
        print(f"[{__file__}] Предупреждение: Карточки объявлений на странице не найдены.")
        return []
        
    print(f"[{__file__}] Найдено карточек для парсинга: {len(cards)}")
    
    results = []
    for card in cards:
        try:
            item_data = parse_single_item(card)
            results.append(item_data)
        except Exception as e:
            card_id = card.get("id", "unknown")
            print(f"[{__file__}] Критическая ошибка при парсинге карточки ID {card_id}: {e}")
            continue
            
    return results

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
        except Exception as e:
            print(f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
            continue
            
    print(f"[{__file__}] Парсинг успешно завершен. Всего собрано элементов: {len(all_results)}")
    return all_results
Как проверить
Сохраните изменения в файле app/parser.py.

Запустите скрипт из корневой директории проекта через терминал:

Bash
python -m app.main
Убедитесь, что исключение SyntaxError больше не возникает, а в логах отображается успешный сбор карточек и генерация финального отчета.