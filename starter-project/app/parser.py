#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from bs4 import BeautifulSoup

def parse_single_item(element) -> Dict[str, Any]:
    """
    Вспомогательная функция для парсинга одного конкретного элемента 
    (например, одной карточки товара, одной строки таблицы).
    Именно этот кусок ИИ будет переписывать под селекторы конкретного сайта.
    """
    item_data = {}
    
    try:
        # --- Пример базовой логики (заменяется под ТЗ клиента) ---
        # Находим название товара
        title_node = element.select_one(".product-title, h1, h2")
        item_data["title"] = title_node.get_text(strip=True) if title_node else None
        
        # Находим цену
        price_node = element.select_one(".price, .amount")
        item_data["price"] = price_node.get_text(strip=True) if price_node else None
        
        # Находим ссылку
        link_node = element.select_one("a")
        item_data["url"] = link_node.get("href") if link_node else None
        # ---------------------------------------------------------
        
    except Exception as e:
        print(f"[{__file__}] Ошибка при парсинге элемента: {e}")
        
    return item_data

def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Парсит HTML одной страницы. Возвращает список записей (dict на каждый товар).
    ИИ перепишет эту функцию под конкретный сайт.
    """
    return parse_html_data([html])


def parse_html_data(raw_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Главная функция парсера. Принимает список сырых HTML-строк (страниц),
    обрабатывает их через BeautifulSoup и собирает финальный массив словарей.
    """
    parsed_items = []

    if not raw_contents:
        print(f"[{__file__}] Предупреждение: Получен пустой список контента для парсинга.")
        return parsed_items

    for index, html_content in enumerate(raw_contents, start=1):
        if not html_content:
            continue
            
        try:
            # Инициализируем BeautifulSoup для текущей страницы
            soup = BeautifulSoup(html_content, "html.parser")
            
            # --- Логика поиска контейнеров (заменяется под ТЗ клиента) ---
            # Например, ищем все карточки товаров на странице
            items_containers = soup.select(".product-card, .item")
            # ---------------------------------------------------------
            
            if not items_containers:
                # Если кастомных контейнеров нет, можно спарсить страницу целиком как один элемент
                single_item = parse_single_item(soup)
                if single_item:
                    parsed_items.append(single_item)
                continue

            # Парсим каждый найденный контейнер
            for element in items_containers:
                item_data = parse_single_item(element)
                
                # Добавляем элемент, только если он не пустой (есть хотя бы одно поле)
                if any(item_data.values()):
                    parsed_items.append(item_data)
                    
            print(f"[{__file__}] Страница {index}: Успешно спарсено элементов: {len(items_containers)}")
            
        except Exception as e:
            print(f"[{__file__}] Ошибка при обработке страницы {index}: {e}")

    print(f"[{__file__}] Всего извлечено элементов: {len(parsed_items)}")
    return parsed_items


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Запуск теста парсера...")
    
    # Фейковый HTML для проверки структуры
    mock_html = """
    <html>
        <div class="product-card">
            <h2 class="product-title"> Смартфон X </h2>
            <span class="price"> $999 </span>
            <a href="https://example.com/item1">Подробнее</a>
        </div>
        <div class="product-card">
            <h2 class="product-title"> Наушники Y </h2>
            <span class="price"> $150 </span>
            <a href="https://example.com/item2">Подробнее</a>
        </div>
    </html>
    """
    
    results = parse_html_data([mock_html])
    print("Результат теста:", results)