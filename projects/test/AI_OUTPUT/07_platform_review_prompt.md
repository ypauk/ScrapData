# CLIENT DESCRIPTION

# Описание задачи клиента

URL:https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1


собери мне в любом формате csv инфу только первую страницу (однопазовая задача)
урл картинки
название авто
цену
тип топливо
город





------------------------------------------------------------

# ANALYSIS

Как опытный Python Web Scraping Engineer, я проанализировал ваш проект. Ниже представлен подробный отчет и стратегия реализации.

1. Краткое описание задачи
Клиенту необходимо выполнить разовый сбор данных (однопазовая задача) с первой страницы результатов поиска сайта auto.ria.com по заданному URL.

2. Какой конечный результат нужен
Файл в формате CSV.

3. Как лучше решить задачу
Рекомендуемый метод: requests + BeautifulSoup.
Почему: Сайт auto.ria.com отдает структуру HTML-страницы при обычном GET-запросе, и данные, которые вы хотите собрать, присутствуют в статичной верстке. Использование тяжелых браузерных инструментов (Playwright/Selenium) здесь избыточно, так как они потребляют больше ресурсов и работают медленнее.

4. Почему остальные варианты хуже
Playwright/Selenium: Избыточны. Они необходимы для динамического контента, который рендерится через JavaScript после загрузки страницы. В данном случае данные доступны сразу в HTML-коде.

Scrapy: Слишком мощный инструмент для задачи, состоящей всего из одной страницы. Это приведет к неоправданному усложнению кода (создание проекта, настройка пауков и т.д.).

5. Анализ сайта
JavaScript Rendering: Не требуется для первой страницы (HTML-код содержит нужные данные).

Структура: Данные разметки доступны в тегах <a> с классом link product-card horizontal.

Блокировки/Защита: Возможны стандартные проверки на ботов, поэтому необходимо использовать корректные User-Agent заголовки.

Остальное: Определить наличие сложной защиты (CAPTCHA, Cloudflare) через предоставленный фрагмент кода невозможно, но на текущий момент явных препятствий для обычного запроса нет.

6. Что необходимо собрать до начала разработки
На данный момент предоставленного page.html и URL достаточно для понимания структуры. Дополнительных данных не требуется.

7. Возможные сложности
Блокировки: Если делать много запросов часто, сайт может ограничить доступ. Для разовой задачи это маловероятно.

Изменение верстки: Если сайт обновит дизайн, селекторы (классы элементов) могут измениться.

8. Что нужно уточнить у клиента
На текущий момент информация полная. Уточнения не требуются.

9. Рекомендуемый стек технологий
Python

requests (для получения HTML)

BeautifulSoup4 (для парсинга HTML)

csv (стандартная библиотека Python для формирования файла)

10. План разработки
Настройка: Написание скрипта, отправляющего GET-запрос с корректными заголовками (User-Agent).

Парсинг: Извлечение нужных полей (URL картинки, название, цена, топливо, город) с помощью BeautifulSoup на основе анализа структуры page.html.

Сохранение: Запись полученных данных в CSV-файл.

11. Оценка сложности
Сложность: 2/10

Время на разработку: 1–2 часа.

Вероятность блокировок: Низкая (для разового сбора).

Вероятность необходимости браузера: Крайне низкая.

Вероятность изменения сайта: Средняя (верстка меняется редко, но бывает).

Общая оценка риска: Низкий.

12. Можно ли решить проще
Текущее решение через requests + BeautifulSoup — это самый простой и эффективный способ.

13. Итоговая рекомендация
Рекомендуется использовать связку requests + BeautifulSoup. Она обеспечит максимальную скорость разработки и выполнения задачи.

Уровень уверенности в выводах: 95% (исходя из предоставленного HTML).

Могу ли я приступать к написанию кода для решения этой задачи?

------------------------------------------------------------

# PROJECT PLAN

Приветствую! Как Senior Web Scraping Engineer, я изучил структуру page.html и задачу. Сайт отдает данные в статичном HTML, поэтому мы не будем использовать «тяжелые» инструменты.1. Полный поток данныхURL (заданный)↓[Технология: requests + BeautifulSoup]↓[Сырые данные: HTML]↓[Парсер: parser.py (BeautifulSoup)]↓[Структура: dict (одна карточка)]↓[Список: list[dict] (все карточки на странице)]↓[Экспортер: exporter.py → save_to_csv()]2. Проектирование app/scraper.py2.1. Интерфейс функцийfetch_page(url: str): Выполняет GET-запрос. Использует requests.get(). Включает заголовки User-Agent. Возвращает объект ответа response или None.get_first_page_content(url: str): Функция-обертка, которая вызывает fetch_page, проверяет статус-код и возвращает response.text.2.2 Алгоритм работыЛогика: Задача разовая, поэтому пагинация не требуется.Поведение: Просто загрузить HTML-код страницы.Утилиты: Внутри fetch_page вызвать random_delay() из app.utils перед выполнением запроса (хорошая практика даже для разовой задачи, чтобы не выглядеть как DDoS).3. Проектирование app/parser.py3.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеparse_listing(html)Ищет все блоки товаров, вызывает parse_single_item для каждого.html: strList[dict]parse_single_item(card)Извлекает поля из конкретного блока <a> (карточки).card: bs4.element.Tagdict3.2. Спецификация полей и селекторыДля парсинга используем следующие селекторы на основе структуры page.html:Карточка: a.link.product-card.horizontalНазвание: div.titleS (текст внутри)Цена: span.c-green (использовать utils.clean_price())URL картинки: img (атрибут src внутри picture)Топливо: 3-й по счету div внутри grid-wrapper (или поиск по тексту внутри structure-row)Город: 4-й по счету div внутри grid-wrapper3.3. Финальная структура результатаJSON{
    "title": "BMW 3 Series 2017",
    "price": 16500, 
    "fuel": "Бензин, 2 л",
    "city": "Львів (Львівська)",
    "image_url": "https://cdn3.riastatic.com/photosnew/auto/photo/..."
}
4. Обработка ошибокСценарийДействиеTimeoutПовторить запрос 3 раза с экспоненциальной задержкой. Если не помогло — логировать и выйти.HTTP 403Записать в лог, что доступ закрыт. Завершить программу.Элемент не найденЗаписать пустую строку "" или None. Не прерывать цикл парсинга карточки.5. Оценка рисковRate Limiting: Низкий риск, так как задача разовая.Изменение верстки: Средний риск. Если RIA обновит верстку, селекторы перестанут работать.Блокировки: Минимальные, если соблюдать адекватные заголовки и задержки.6. Порядок реализацииparser.py: Пишется первым. Тестируется на page.html (локально), чтобы убедиться, что селекторы верно вытаскивают данные.scraper.py: Пишется вторым. Реализует сетевой запрос.Интеграция: Сборка в main.py.7. Краткое резюмеТехнология: requests + BeautifulSoup4.scraper.py: fetch_page (GET-запрос с заголовками).parser.py: parse_listing (итерация по карточкам), parse_single_item (извлечение данных).Риски: Изменение селекторов верстки со стороны сайта.Что останется неизвестным:Неизвестно, потребуется ли при просмотре всех результатов (если клиент решит расширить задачу) обход через параметры ?page=X.Нет полной уверенности, что все карточки имеют одинаковую структуру (могут быть рекламные или спец-предложения), что потребует проверок на наличие элементов в parser.py.Я готов приступать к разработке (написанию кода) по этой схеме, если вы подтверждаете план.

------------------------------------------------------------

# SCRAPER.PY

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
from typing import List, Optional
from app.config import DEFAULT_USER_AGENT, TIMEOUT, RETRY_COUNT
from app.utils import random_delay

def fetch_page(url: str) -> Optional[requests.Response]:
    """
    Выполняет GET-запрос к указанному URL с корректными заголовками.
    Использует повторные попытки при сбоях.
    
    Args:
        url (str): URL для запроса
        
    Returns:
        Optional[requests.Response]: Объект ответа или None при ошибке
    """
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    for attempt in range(RETRY_COUNT):
        try:
            print(f"[{__file__}] Попытка {attempt + 1} запроса к {url[:50]}...")
            
            # Случайная задержка перед запросом (хорошая практика)
            random_delay(1.0, 3.0)
            
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )
            
            # Проверяем статус ответа
            if response.status_code == 200:
                print(f"[{__file__}] Успешный ответ (статус: {response.status_code})")
                return response
            elif response.status_code == 403:
                print(f"[{__file__}] Доступ запрещен (403). Проверьте заголовки или IP.")
                return None
            elif response.status_code == 404:
                print(f"[{__file__}] Страница не найдена (404). Проверьте URL.")
                return None
            else:
                print(f"[{__file__}] Неожиданный статус: {response.status_code}")
                
            # Если статус не 200, ждем перед повторной попыткой
            if attempt < RETRY_COUNT - 1:
                wait_time = 2 ** attempt  # Экспоненциальная задержка
                print(f"[{__file__}] Повторная попытка через {wait_time} сек...")
                time.sleep(wait_time)
                
        except requests.exceptions.Timeout:
            print(f"[{__file__}] Таймаут при попытке {attempt + 1}")
            if attempt < RETRY_COUNT - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        except requests.exceptions.ConnectionError:
            print(f"[{__file__}] Ошибка соединения при попытке {attempt + 1}")
            if attempt < RETRY_COUNT - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        except Exception as e:
            print(f"[{__file__}] Непредвиденная ошибка: {e}")
            if attempt < RETRY_COUNT - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
    
    print(f"[{__file__}] Не удалось получить ответ после {RETRY_COUNT} попыток")
    return None

def get_first_page_content(url: str) -> Optional[str]:
    """
    Функция-обертка для получения HTML-контента первой страницы.
    Вызывает fetch_page и возвращает текст ответа при успехе.
    
    Args:
        url (str): URL для запроса
        
    Returns:
        Optional[str]: HTML-код страницы или None при ошибке
    """
    print(f"[{__file__}] Получение контента страницы: {url}")
    
    response = fetch_page(url)
    if response and response.status_code == 200:
        print(f"[{__file__}] Контент получен (длина: {len(response.text)} символов)")
        return response.text
    else:
        print(f"[{__file__}] Не удалось получить контент страницы")
        return None

def fetch_page_data(context=None) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Собирает сырой HTML-контент с первой страницы поиска.
    
    Args:
        context: Не используется, сохранен для совместимости с main.py
        
    Returns:
        List[str]: Список с HTML-кодом страницы (всегда один элемент)
    """
    print(f"[{__file__}] Запуск процесса сбора данных...")
    
    # URL из задания
    target_url = "https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1"
    
    html_contents = []
    
    try:
        html_content = get_first_page_content(target_url)
        if html_content and html_content.strip():
            html_contents.append(html_content)
            print(f"[{__file__}] Сбор данных успешно завершен. Получено страниц: 1")
        else:
            print(f"[{__file__}] Предупреждение: Получен пустой HTML-контент")
    except Exception as e:
        print(f"[{__file__}] Критическая ошибка при сборе данных: {e}")
    
    print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(html_contents)}")
    return html_contents
```

------------------------------------------------------------

# PARSER.PY

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
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
        # Используем CSS селектор для поиска по нескольким классам
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
```

------------------------------------------------------------

# TRACEBACK

(traceback не найден — сохрани ошибку в AI_INPUT/traceback.txt)

------------------------------------------------------------

# EXECUTION LOG

(лог выполнения не найден — сохрани вывод консоли в AI_INPUT/log.txt)

------------------------------------------------------------

# BROWSER.PY

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext

def load_cookies_if_exist(context: BrowserContext, cookies_path: Path) -> None:
    """
    Загружает куки в контекст браузера, если файл существует.
    """
    if cookies_path.exists() and cookies_path.stat().st_size > 0:
        try:
            with open(cookies_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
            print(f"[{__file__}] Куки успешно загружены из {cookies_path.name}")
        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке кук: {e}")

def get_browser_context(
    playwright_instance, 
    headless: bool = None, 
    user_agent: str = None,
    cookies_path: Path = None
) -> BrowserContext:
    """
    Инициализирует настроенный браузер и возвращает изолированный контекст.
    """
    # 1. Автоматически определяем режим (Docker/переменные окружения или дефолт)
    # Если headless не передан, смотрим в .env или ставим True, если мы в Docker
    if headless is None:
        headless = os.getenv("HEADLESS", "0") == "1" or os.getenv("IS_DOCKER") == "1"

    # Дефолтный качественный User-Agent, если не передан кастомный
    if not user_agent:
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Anonymized/Chrome/120.0.0.0 Safari/537.36"
        )

    print(f"[{__file__}] Запуск Chromium (Headless={headless})...")

    # 2. Запуск браузера с флагами против падений в Docker
    browser: Browser = playwright_instance.chromium.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled" # Скрывает автоматизацию
        ]
    )

    # 3. Создание контекста с маскировкой параметров
    context: BrowserContext = browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        is_mobile=False,
        has_touch=False,
        locale="en-US",
        timezone_id="America/New_York"
    )

    # 4. Подкладываем куки, если передан путь (например, из AI_INPUT)
    if cookies_path:
        load_cookies_if_exist(context, cookies_path)

    return context


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    # Локальный тест
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    test_cookies = ROOT_DIR / "AI_INPUT" / "cookies.json"
    
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False, cookies_path=test_cookies)
        page = ctx.new_page()
        page.goto("https://bot.sannysoft.com/") # Хороший сайт для проверки детекта
        page.wait_for_timeout(5000)
        ctx.browser.close()
```

------------------------------------------------------------

# MAIN.PY

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Добавляет starter-project в пути Python
from playwright.sync_api import sync_playwright

from app.config import COOKIES_FILE
from app.browser import get_browser_context
from app.scraper import fetch_page_data
from app.parser import parse_html_data
from app.exporter import save_to_csv, save_to_json

def main() -> None:
    """
    Главная точка входа. Управляет жизненным циклом парсера.
    """
    print("=" * 70)
    print(f"[{__file__}] ЗАПУСК ПАРСЕРА")
    print("=" * 70)

    # Инициализируем хранилище для собранных данных
    scraped_results = []

    try:
        # 1. Запуск контекста автоматизации (Playwright)
        with sync_playwright() as playwright:
            
            # Получаем настроенный контекст браузера (переменные подтянутся из config)
            context = get_browser_context(
                playwright_instance=playwright,
                cookies_path=COOKIES_FILE
            )
            
            # 2. Сбор данных (Scraping)
            # Передаем контекст браузера в scraper.py для обхода страниц
            raw_pages_content = fetch_page_data(context)
            
            # Закрываем браузер сразу, как только закончили сетевую работу
            context.browser.close()
            print(f"[{__file__}] Браузер успешно закрыт.")

            # 3. Обработка данных (Parsing)
            # Передаем собранный HTML/JSON контент в parser.py для извлечения полей
            if raw_pages_content:
                print(f"[{__file__}] Начало парсинга контента...")
                scraped_results = parse_html_data(raw_pages_content)
            else:
                print(f"[{__file__}] Критическая ошибка: Нечего парсить (список страниц пуст).")
                sys.exit(1)

        # 4. Экспорт результатов (Export)
        if scraped_results:
            print(f"[{__file__}] Экспорт данных (Всего элементов: {len(scraped_results)})...")
            
            # Сохраняем в оба формата (на Upwork клиенты любят иметь выбор)
            save_to_csv(scraped_results, "output_results.csv")
            save_to_json(scraped_results, "output_results.json")
            
            print("=" * 70)
            print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО")
            print("=" * 70)
        else:
            print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат. Файлы не созданы.")

    except KeyError as ke:
        print(f"[{__file__}] Ошибка конфигурации или структуры: {ke}")
        sys.exit(1)
    except Exception as e:
        print(f"[{__file__}] Критический сбой в главном потоке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

------------------------------------------------------------

# PROJECT STRUCTURE

test/
├── AI_INPUT/
│   ├── screenshots/
│   ├── answers.txt
│   ├── cookies.json
│   ├── description.txt
│   ├── headers.json
│   ├── network.har
│   ├── notes.txt
│   ├── page.html
│   └── traceback.txt
├── AI_OUTPUT/
│   ├── 01_analysis_answer.md
│   ├── 01_analysis_prompt.md
│   ├── 02_project_answer.md
│   ├── 02_project_prompt.md
│   ├── 03_scraper_answer.py
│   ├── 03_scraper_prompt.md
│   ├── 04_parser_answer.py
│   └── 04_parser_prompt.md
├── app/
│   ├── browser.py
│   ├── config.py
│   ├── exporter.py
│   ├── main.py
│   ├── parser.py
│   ├── scraper.py
│   └── utils.py
├── docs/
│   └── здесь пилим документацию.txt
├── input/
├── output/
├── tests/
├── workflows/
│   ├── new_project.md
│   └── Вот чего сейчас не хватает..txt
├── docker-compose.yml
├── Dockerfile
├── project_state.json
├── PROJECT_STRUCTURE.md
├── README.md
├── requirements.txt
└── Как добиться не писать лишний код.txt

------------------------------------------------------------

# YOUR TASK

# ROLE

Ты Senior Python Architect и Senior Web Scraping Engineer.

Твоя задача — НЕ исправить код.

Твоя задача — провести архитектурное расследование.

Нужно определить, на каком этапе моего AI workflow была допущена ошибка.

---

# Контекст

Моя платформа состоит из следующих этапов:

1. Analysis
2. Project planning
3. Scraper generation
4. Parser generation
5. Debug

Я хочу улучшать платформу, а не только исправлять текущий проект.

---

# Задача

Проанализируй следующие материалы:

- описание клиента;
- анализ проекта;
- проектный план;
- scraper.py;
- parser.py;
- traceback;
- лог выполнения;
- browser.py;
- main.py.

---

# Ответь на вопросы

## 1. Где впервые появилась ошибка?

Выбери только один вариант.

- Analysis
- Project planning
- Scraper generation
- Parser generation
- Архитектура starter-project

Объясни почему.

---

## 2. Что стало причиной?

Например:

- ИИ выбрал неправильную технологию.
- Промпт недостаточно строгий.
- scraper.py проигнорировал проектный план.
- browser.py используется неправильно.
- requests используется вместо Playwright.
- Ошибка в архитектуре starter-project.

---

## 3. Что нужно изменить?

Раздели изменения по категориям.

### Нужно изменить prompt

Какие именно промпты?

Почему?

---

### Нужно изменить starter-project

Какие файлы?

Почему?

---

### Нужно изменить ai_workflow.py

Что автоматизировать?

---

### Нужно изменить шаблоны

Какие?

---

## 4. Можно ли было избежать этой ошибки автоматически?

Если да —

предложи правило проверки.

Например

"Если в analysis выбран Playwright,
а scraper.py использует requests —
считать это архитектурной ошибкой."

---

## 5. Что добавить в платформу?

Предложи улучшения платформы.

Не ограничивайся текущей структурой.

---

## 6. Что оставить без изменений?

Не предлагай менять то, что уже реализовано правильно.

---

# Важно

НЕ исправляй код.

НЕ переписывай scraper.py.

НЕ пиши parser.py.

Нужно определить,
как улучшить платформу,
чтобы подобная ошибка больше никогда не возникала.