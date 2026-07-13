import os
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

try:
    from app.utils import clean_price
except ImportError:
    def clean_price(price_str: str) -> str:
        return "".join(filter(lambda ch: ch.isdigit() or ch == ".", price_str.replace(",", ".")))


def parse_single_item(card: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """
    Извлекает целевые данные из одного HTML-элемента (карточки автомобиля).
    """
    try:
        # 1. Извлечение названия
        title_tag = card.find("h4", class_="css-wlcw7o")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # 2. Извлечение цены
        price_tag = card.find("p", data-testid="ad-price")
        if not price_tag:
            price_tag = card.find("p", class_="css-61fb99")
            
        price_val = None
        if price_tag:
            raw_price = price_tag.get_text(strip=True)
            cleaned = clean_price(raw_price)
            if cleaned:
                try:
                    price_val = float(cleaned)
                except ValueError:
                    price_val = raw_price

        # 3. Извлечение вида топлива
        fuel_type = ""
        param_tags = card.find_all("span", class_="css-h59g4b")
        fuel_keywords = ["бензин", "газ", "дизель", "гибрид", "електро", "електрика"]
        
        for param in param_tags:
            param_text = param.get_text(strip=True)
            if any(kw in param_text.lower() for kw in fuel_keywords):
                fuel_type = param_text
                break
                
        if not fuel_type and len(param_tags) >= 3:
            fuel_type = param_tags[2].get_text(strip=True)

        return {
            "title": title,
            "price": price_val,
            "fuel_type": fuel_type if fuel_type else None
        }

    except Exception as e:
        filename = os.path.basename(__file__)
        print(f"[{filename}] Ошибка при парсинге элемента: {e}")
        return None


def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Главная функция парсера, вызываемая оркестратором main.py.
    """
    filename = os.path.basename(__file__)
    print(f"[{filename}] Запуск парсинга контента. Получено страниц: {len(html_contents)}")
    
    result_collection = []

    for index, html_raw in enumerate(html_contents, start=1):
        if not html_raw:
            print(f"[{filename}] Страница {index} пуста. Пропуск.")
            continue
            
        try:
            soup = BeautifulSoup(html_raw, "html.parser")
            cards = soup.find_all("div", {"data-testid": "l-card"})
            if not cards:
                cards = soup.find_all("div", class_="css-1sw7q4x")

            print(f"[{filename}] Страница {index}: обнаружено карточек: {len(cards)}")

            for card in cards:
                parsed_item = parse_single_item(card)
                if parsed_item:
                    result_collection.append(parsed_item)

        except Exception as e:
            print(f"[{filename}] Критическая ошибка при обработке страницы {index}: {e}")
            continue

    print(f"[{filename}] Парсинг успешно завершен. Всего собрано записей: {len(result_collection)}")
    return result_collection