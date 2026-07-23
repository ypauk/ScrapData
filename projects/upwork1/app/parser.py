"""
⚠️ ДЕМО-ПРИМЕР, А НЕ УНИВЕРСАЛЬНЫЙ ДЕФОЛТ ⚠️

Код ниже — рабочий сквозной пример парсинга объявлений OLX (авто: название,
цена, вид топлива), созданный для демонстрации полного цикла workflow
(`ai_workflow.py analyze/project/module scraper/module parser`) на реальном
сайте. Селекторы (`css-1sw7q4x`, `css-wlcw7o`, `data-testid="ad-price"` и т.д.)
специфичны именно для OLX и НЕ подходят для других сайтов "как есть".

Для нового заказа этот файл нужно заменить одним из способов:
  1. python ai_workflow.py module parser <project_name>
     (сгенерирует промпт для ИИ на основе анализа/плана нового сайта,
     ответ ИИ сохраняется в AI_OUTPUT/04_parser_answer.py и переносится сюда)
  2. Вручную переписать `parse_single_item`/`parse_listing` под структуру
     карточек нового сайта, сохранив сигнатуру `parse_html_data(html_contents)`,
     которую вызывает `app/main.py`.

Модуль `app/html_parser.py` (HtmlParser) — универсальный и НЕ требует правок,
используй его безопасные методы (`select_one`, `find`, `get_text`, `get_attr`
и т.д.) при написании парсера для нового сайта. Аналогично, для приведения
извлечённых значений к консистентному формату (числа, даты, bool, URL и т.д.)
используй `app/data_normalizer.py` (DataNormalizer) вместо ручного разбора
строк прямо здесь.
"""

from typing import List, Dict, Any
from app.html_parser import HtmlParser
from app.data_normalizer import DataNormalizer
from app.utils import log_message


def parse_single_item(card) -> Dict[str, Any]:
    """
    Извлекает целевые поля (название, цена, топливо) из структуры одной карточки товара.

    Args:
        card (bs4.element.Tag): Объект тега одной карточки объявления.

    Returns:
        dict: Словарь с извлеченными данными объявления.
    """
    # 1. Извлечение названия (безопасно через HtmlParser: не бросает исключение,
    #    если элемент отсутствует, и нормализует пробелы/переносы строк).
    title_element = HtmlParser.find(card, "h4", class_="css-wlcw7o")
    title = HtmlParser.get_text(title_element, default="")

    # 2. Извлечение цены и её нормализация через централизованный
    #    Data Normalization слой (app/data_normalizer.py, Milestone 5) —
    #    вместо разбора строки цены прямо здесь (DataNormalizer.normalize_price
    #    переиспользует app.utils.clean_price, чтобы логика не дублировалась).
    price_element = HtmlParser.find(card, "p", attrs={"data-testid": "ad-price"})
    raw_price = HtmlParser.get_text(price_element, default="")
    if raw_price:
        price = DataNormalizer.normalize_price(raw_price)
        if price is None:
            log_message("error", f"[{__file__}] Не удалось нормализовать цену '{raw_price}'")
    else:
        log_message("warning", f"[{__file__}] Предупреждение: Элемент цены не найден в карточке с ID {HtmlParser.get_attr(card, 'id')}")
        price = None

    # 3. Извлечение вида топлива
    fuel = ""
    params_container = HtmlParser.find(card, "div", class_="css-13vv2xi")
    param_spans = HtmlParser.find_all(params_container, "span", class_="css-h59g4b")
    if len(param_spans) >= 3:
        fuel = HtmlParser.get_text(param_spans[2], default="")
    elif params_container is not None:
        log_message("warning", f"[{__file__}] Предупреждение: Недостаточно параметров для извлечения топлива в карточке с ID {HtmlParser.get_attr(card, 'id')}")
        fuel = "Не указано"

    return {
        "title": title,
        "price": price,
        "fuel": fuel
    }

def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Инициализирует HTML Parser, находит коллекцию всех карточек автомобилей на странице
    и передает каждую в parse_single_item.

    Args:
        html (str): Строка сырого HTML-кода страницы.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными по автомобилям.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        # HtmlParser.parse() уже залогировал причину (пустой/невалидный HTML).
        return []

    cards = HtmlParser.find_all(soup, "div", class_="css-1sw7q4x")

    if not cards:
        log_message("warning", f"[{__file__}] Предупреждение: Карточки объявлений на странице не найдены.")
        return []

    log_message("info", f"[{__file__}] Найдено карточек для парсинга: {len(cards)}")

    results = []
    for card in cards:
        try:
            item_data = parse_single_item(card)
            results.append(item_data)
        except Exception as e:
            card_id = HtmlParser.get_attr(card, "id", "unknown")
            log_message("error", f"[{__file__}] Критическая ошибка при парсинге карточки ID {card_id}: {e}")
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
    log_message("info", f"[{__file__}] Начало обработки {len(html_contents)} страниц(ы)...")

    for idx, html in enumerate(html_contents, 1):
        try:
            page_results = parse_listing(html)
            all_results.extend(page_results)
        except Exception as e:
            log_message("error", f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
            continue

    log_message("info", f"[{__file__}] Парсинг успешно завершен. Всего собрано элементов: {len(all_results)}")
    return all_results
