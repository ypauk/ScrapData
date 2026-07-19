# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Скрапер упал с ошибкой. Найди причину и исправь **минимальным изменением**.

---

# ПРАВИЛА

ПРАВИЛА РАЗРАБОТКИ

1. Всегда использовать starter-project.

2. Не менять структуру каталогов.

3. Не создавать новые папки без необходимости.

4. Не писать код, который не требуется клиентом.

5. Предпочитать простое решение сложному.

6. Сначала искать API.

7. Если API нет — рассматривать requests + BeautifulSoup.

8. Playwright использовать только при необходимости.

9. Код должен быть модульным.

10. Docker создавать только после успешного локального запуска.

---

# АНАЛИЗ ПРОЕКТА

1. Краткое описание задачи

Клиент хочет однократно собрать данные только со страницы №2 результатов поиска AUTO.RIA:

https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page=2

Необходимо получить список автомобилей и сохранить его в CSV.

Для каждого объявления нужно собрать:

URL изображения;
название автомобиля;
цену;
тип топлива;
город.

Уровень уверенности: высокий (≈99%).

2. Какой конечный результат нужен

Формат результата:

CSV.

Поля:

Image URL;
Car Name;
Price;
Fuel Type;
City.

Это одноразовая задача, без необходимости периодического парсинга.

Уровень уверенности: высокий.

3. Как лучше решить задачу
Рекомендуемый вариант

Python + requests + BeautifulSoup

Почему

Из предоставленного HTML видно, что все необходимые данные уже присутствуют в разметке страницы:

название автомобиля;
цена;
изображение;
тип топлива;
город.

Следовательно, нет признаков того, что для получения этих данных требуется выполнение JavaScript.

Для одноразового сбора одной страницы полноценный браузер является избыточным.

Уровень уверенности: высокий (≈95%).

4. Почему остальные варианты хуже
Playwright

Не рекомендуется.

Причина:

значительно медленнее;
сложнее;
не дает преимуществ, если HTML уже содержит нужные данные.
Selenium

Не рекомендуется.

Причины:

тяжелее;
менее стабилен;
не нужен для данной задачи.
Scrapy

Не рекомендуется.

Причина:

проект слишком маленький;
настройка Scrapy не оправдана ради одной страницы.
API

Пока рекомендовать нельзя.

Причина:

network.har пустой;
наличие внутреннего API не подтверждено.
5. Анализ сайта

На основании предоставленных материалов.

Возможность	Статус
JavaScript Rendering	Частично используется, но необходимые данные уже есть в HTML
React	Определить невозможно
Vue	Определить невозможно
Angular	Определить невозможно
API	Не подтверждено
GraphQL	Не подтверждено
Infinite Scroll	Нет
Pagination	Да
Login	Нет
Cookies	Не требуются (cookies.json пустой)
JWT	Не обнаружен
Bearer Token	Не обнаружен
CAPTCHA	Не обнаружена
Cloudflare	Не подтвержден
Rate Limits	Неизвестно
Download Files	Нет
Upload Files	Нет
Lazy Loading	Частично (изображения через <picture>)
WebSocket	Не обнаружен
XHR / Fetch	Не удалось определить
Sitemap	Не проверялся
robots.txt	Не проверялся

Уровень уверенности: средний (≈75%), поскольку отсутствует HAR.

6. Что необходимо собрать до начала разработки

Для данной задачи дополнительная информация практически не требуется.

Полезно иметь:

пример ожидаемого CSV (не обязательно);
network.har (если HTML внезапно окажется неполным).

На текущий момент имеющегося HTML достаточно для выбора стратегии.

7. Возможные сложности

Возможные риски:

изменение HTML-разметки;
изменение CSS-классов;
временные ограничения сайта по частоте запросов;
возможное появление антибот-защиты в будущем.

Для одной страницы вероятность возникновения проблем невысока.

8. Что нужно уточнить у клиента

Информации в целом достаточно.

При желании можно уточнить:

Нужно ли сохранять цену только в долларах или вместе с гривной?
Нужно ли сохранять абсолютный URL изображения (как в HTML)?
Нужно ли включать заголовок (header) в CSV?
Какая кодировка CSV предпочтительна (UTF-8 обычно подходит)?

Без ответов на эти вопросы разработку также можно выполнить.

9. Рекомендуемый стек технологий
Python
requests
BeautifulSoup
10. План разработки
Этап 1. Получение страницы

Цель

Получить HTML страницы №2.

Результат

Исходный HTML страницы.

Зависимости

Нет.

Этап 2. Извлечение данных

Цель

Получить:

URL изображения;
название;
цену;
тип топлива;
город.

Результат

Структурированный список автомобилей.

Зависимости

HTML страницы.

Этап 3. Экспорт

Цель

Сохранить данные.

Результат

CSV-файл.

Зависимости

Успешный парсинг данных.

11. Оценка сложности
Параметр	Оценка
Сложность	2/10
Estimation	0.5–1.5 часа
Вероятность блокировок	Низкая
Вероятность необходимости браузера	Низкая (~10%)
Вероятность изменения сайта	Средняя
Общий риск	Низкий
12. Можно ли решить проще

Да.

Самое простое решение:

requests → BeautifulSoup → CSV

Использование браузера (Playwright/Selenium) не выглядит оправданным для данной задачи.

Если бы в network.har обнаружился внутренний API, его стоило бы предпочесть HTML-парсингу. Однако предоставленный network.har пуст, поэтому оснований рекомендовать API нет.

13. Итоговая рекомендация

Рекомендуемое решение:

Python;
requests;
BeautifulSoup;
экспорт в CSV.

Почему это оптимально:

задача одноразовая;
требуется обработать только одну страницу;
необходимые данные уже присутствуют в HTML;
решение будет самым простым, быстрым и надежным без использования браузера.

Что желательно получить перед началом разработки:

Дополнительные материалы не обязательны. При необходимости можно уточнить формат CSV (например, кодировку или точный формат цены), но это не препятствует началу работы.

Можно ли переходить к написанию кода?

Да. На основании предоставленного описания и HTML информации достаточно для реализации. Единственное ограничение — внутренний API нельзя оценить, так как network.har пуст, но для данной задачи это не является критичным.

---

# ПЛАН ПРОЕКТА

1. Полный поток данныхURL (заданная страница 2)↓[Технология: requests]↓[Сырые данные: HTML]↓[Парсер: BeautifulSoup]↓[Структура: dict]↓[Список: list[dict]]↓[Экспортер: exporter.py → CSV]2. Проектирование app/scraper.py2.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеfetch_page(url)Выполняет GET-запрос к заданной странице.url: strstr (HTML)2.2 АлгоритмПагинация: В данной задаче пагинация не требуется, так как клиент запрашивает конкретную страницу (№2). Скрапер просто забирает контент по переданному URL.Поведение: Поскольку данные уже присутствуют в статическом HTML (согласно анализу), браузер не нужен.Утилиты: Вызвать random_delay() из app.utils перед выполнением сетевого запроса для имитации поведения человека.3. Проектирование app/parser.py3.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеparse_listing(html)Ищет все карточки товаров в HTML-коде.html: strList[dict]parse_single_item(card)Извлекает данные из конкретной карточки.card: bs4.element.Tagdict3.2. Спецификация полейImage URL: img (атрибут src внутри тега <picture>).Car Name: Текст из блока class="common-text size-16-20 titleS fw-bold mb-4".Price: Текст из блока class="common-text titleM c-green". Используем clean_price() из utils.py.Fuel Type: Текст из 3-го блока structure-row внутри grid-wrapper.City: Текст из 4-го блока structure-row внутри grid-wrapper.3.3. Финальная структура результатаJSON{
    "Image URL": "https://cdn3.riastatic.com/photosnew/auto/photo/...",
    "Car Name": "BMW 3 Series 2017",
    "Price": "16 500 $",
    "Fuel Type": "Бензин, 2 л",
    "City": "Львів (Львівська)"
}
4. Обработка ошибокСценарийДействиеTimeoutПовторить запрос 3 раза с паузой. Если не помогло — логировать и завершить.HTTP 403/404Логировать ошибку и прервать выполнение (одноразовая задача).Элемент не найденВернуть None для конкретного поля, чтобы не ломать структуру CSV.5. Оценка рисковCloudflare (защита): Низкий риск (для одной страницы).Rate Limiting: Низкий риск.Сложная структура DOM: Средний риск (возможны изменения имен классов).6. Порядок реализацииparser.py: Создать на базе page.html. Протестировать извлечение всех полей.scraper.py: Реализовать запрос requests и передачу ответа в парсер.Интеграция: Вызвать связку в main.py и передать результат в exporter.save_to_csv().7. Краткое резюмеВыбранная технология: requests + BeautifulSoup (стандартный HTTP-запрос).Основные функции scraper.py: fetch_page.Основные функции parser.py: parse_listing, parse_single_item.Итоговая структура данных: Словарь с полями: Image URL, Car Name, Price, Fuel Type, City.Главные риски: Изменение верстки сайта (классов CSS).Что останется неизвестнымТочное соответствие CSS-селекторов: ПРЕДПОЛОЖЕНИЕ: Использование представленных в HTML классов будет стабильным для текущей версии страницы.Наличие защиты: ПРЕДПОЛОЖЕНИЕ: Сайт не выдаст 403 ошибку при стандартном User-Agent.Почему выбран именно этот способ:Выбран HTML-парсинг, так как сайт отдает полный HTML с данными в первом же ответе. Playwright избыточен, медленнее и потребляет больше ресурсов. Метод requests + BS4 является самым быстрым и надежным для одноразовой операции.Могу ли я приступать к написанию логики (псевдокода) или реализации?Да, проект спроектирован полностью в рамках требований.

---

# ТЕКУЩИЙ КОД



--- app/browser.py ---
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

--- app/config.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# =====================================================================
# 1. ПУТИ К ПАПКАМ СТРУКТУРЫ (Абсолютные)
# =====================================================================
APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent.resolve()

# Папки для работы с ИИ
AI_INPUT_DIR = ROOT_DIR / "AI_INPUT"
AI_OUTPUT_DIR = ROOT_DIR / "AI_OUTPUT"

# Входные и выходные данные для скрипта
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"

# Файлы окружения и зависимостей
COOKIES_FILE = AI_INPUT_DIR / "cookies.json"
HEADERS_FILE = AI_INPUT_DIR / "headers.json"

# Гарантируем, что рабочие папки проекта существуют
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 2. НАСТРОЙКИ ЗАПУСКА И БРАУЗЕРА (.env / Окружение)
# =====================================================================

# Режим работы браузера: "1" — без экрана, "0" — с экраном (дебаг)
# Если переменная IS_DOCKER установлена, принудительно включаем headless
IS_DOCKER = os.getenv("IS_DOCKER", "0") == "1"
HEADLESS = os.getenv("HEADLESS", "1") == "1" or IS_DOCKER

# Логирование и таймауты
TIMEOUT = int(os.getenv("SCRAPER_TIMEOUT", "30"))  # в секундах
RETRY_COUNT = int(os.getenv("SCRAPER_RETRY", "3"))

# Настройки сети и прокси
PROXY_URL = os.getenv("PROXY_URL", None)  # Формат: http://username:password@host:port


# =====================================================================
# 3. МАСКИРОВКА И КЛИЕНТСКИЕ ДАННЫЕ
# =====================================================================

# Реалистичный дефолтный User-Agent, если не передан кастомный в headers.json
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


# =====================================================================
# 4. ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ПУТЕЙ
# =====================================================================
if __name__ == "__main__":
    print(f"[{__file__}] Проверка путей конфигурации:")
    print(f"  Корень проекта (ROOT_DIR): {ROOT_DIR}")
    print(f"  Папка вывода (OUTPUT_DIR): {OUTPUT_DIR}")
    print(f"  Файл кук (COOKIES_FILE):   {COOKIES_FILE}")
    print(f"  Режим Headless:            {HEADLESS}")
    print(f"  Запуск в Docker:           {IS_DOCKER}")

--- app/exporter.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
from typing import List, Dict, Any
from app.config import OUTPUT_DIR

def save_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Сохраняет список словарей в CSV файл.
    Автоматически берет ключи первого словаря в качестве заголовков.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в CSV.")
        return ""

    # Если расширение не указано, добавляем его
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = OUTPUT_DIR / filename
    
    # Берем заголовки из ключей первого элемента
    fieldnames = list(data[0].keys())

    try:
        # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"[{__file__}] Данные успешно сохранены в CSV: {filepath.name} (Строк: {len(data)})")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в CSV: {e}")
        return ""

def save_to_json(data: List[Dict[str, Any]], filename: str, indent: int = 4) -> str:
    """
    Сохраняет данные в формате JSON с красивыми отступами.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в JSON.")
        return ""

    if not filename.endswith(".json"):
        filename += ".json"

    filepath = OUTPUT_DIR / filename

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
            
        print(f"[{__file__}] Данные успешно сохранены в JSON: {filepath.name}")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в JSON: {e}")
        return ""


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    test_data = [
        {"id": 1, "title": "Ноутбук", "price": 1200.50, "in_stock": True},
        {"id": 2, "title": "Смартфон", "price": 550.00, "in_stock": False},
    ]
    print(f"[{__file__}] Запуск теста экспортера...")
    save_to_csv(test_data, "test_products")
    save_to_json(test_data, "test_products.json")

--- app/main.py ---
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

--- app/parser.py ---
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

--- app/scraper.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import List, Optional

from app.config import AI_INPUT_DIR
from app.utils import random_delay

# Константы для запроса
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
TARGET_URL = "https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page=2"
TIMEOUT = 30  # секунд
MAX_RETRIES = 3


def fetch_page(url: str) -> Optional[str]:
    """
    Выполняет GET-запрос к заданной странице.

    Args:
        url (str): URL страницы для загрузки.

    Returns:
        Optional[str]: HTML-код страницы в виде строки или None в случае ошибки.
    """
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "uk,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    for attempt in range(MAX_RETRIES):
        try:
            print(f"[{__file__}] Попытка {attempt + 1}/{MAX_RETRIES}: Загрузка страницы {url}")

            # Имитация поведения человека перед запросом
            random_delay(1.0, 2.5)

            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )

            # Проверка статуса ответа
            if response.status_code == 200:
                print(f"[{__file__}] Страница успешно загружена. Размер: {len(response.text)} символов")
                return response.text
            else:
                print(f"[{__file__}] Ошибка HTTP {response.status_code}: {response.reason}")
                if attempt < MAX_RETRIES - 1:
                    print(f"[{__file__}] Повтор через 2 секунды...")
                    random_delay(2.0, 3.0)
                    continue
                else:
                    print(f"[{__file__}] Достигнут лимит попыток. Загрузка страницы не удалась.")
                    return None

        except requests.exceptions.Timeout:
            print(f"[{__file__}] Ошибка таймаута при попытке {attempt + 1}")
            if attempt < MAX_RETRIES - 1:
                print(f"[{__file__}] Повтор через 2 секунды...")
                random_delay(2.0, 3.0)
                continue
            else:
                print(f"[{__file__}] Достигнут лимит попыток. Загрузка страницы не удалась.")
                return None

        except requests.exceptions.ConnectionError:
            print(f"[{__file__}] Ошибка соединения при попытке {attempt + 1}")
            if attempt < MAX_RETRIES - 1:
                print(f"[{__file__}] Повтор через 3 секунды...")
                random_delay(3.0, 4.0)
                continue
            else:
                print(f"[{__file__}] Достигнут лимит попыток. Загрузка страницы не удалась.")
                return None

        except Exception as e:
            print(f"[{__file__}] Непредвиденная ошибка при попытке {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"[{__file__}] Повтор через 3 секунды...")
                random_delay(3.0, 4.0)
                continue
            else:
                print(f"[{__file__}] Достигнут лимит попыток. Загрузка страницы не удалась.")
                return None

    return None


def fetch_page_data(context=None) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Загружает страницу №2 AUTO.RIA и возвращает HTML-контент.

    Args:
        context (BrowserContext, optional): Контекст браузера Playwright (не используется в requests-реализации).

    Returns:
        List[str]: Список строк, содержащих сырой HTML страницы.
    """
    print(f"[{__file__}] Запуск процесса сбора данных с AUTO.RIA...")
    print(f"[{__file__}] Целевой URL: {TARGET_URL}")

    # Проверка интернета: пробуем загрузить страницу
    html_content = fetch_page(TARGET_URL)

    if html_content:
        print(f"[{__file__}] Сбор данных завершен. Получено страниц: 1")
        return [html_content]
    else:
        print(f"[{__file__}] Ошибка: Не удалось загрузить страницу. Возвращаем пустой список.")
        return []


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тестовый запуск scraper...")
    result = fetch_page_data()
    if result:
        print(f"[{__file__}] Успешно получен HTML. Размер: {len(result[0])} символов")
        # Сохраняем для проверки
        with open(AI_INPUT_DIR / "fetched_page.html", "w", encoding="utf-8") as f:
            f.write(result[0])
        print(f"[{__file__}] HTML сохранен в {AI_INPUT_DIR / 'fetched_page.html'}")
    else:
        print(f"[{__file__}] Не удалось получить HTML")

--- app/utils.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from datetime import datetime

def log_message(level: str, message: str) -> None:
    """
    Универсальный форматированный логгер для вывода в консоль.
    Заменяет тяжелые библиотеки логирования простым и понятным для ИИ кодом.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """
    Генерирует случайную паузу. Помогает имитировать поведение 
    реального пользователя и обходить базовые лимиты запросов (Rate Limiting).
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def clean_price(price_string: str) -> float:
    """
    Утилита очистки строки цены (например, '$1,299.99' или '150.00 €') 
    и конвертации её в чистое число с плавающей точкой (float).
    Очень частый запрос от клиентов на Upwork.
    """
    if not price_string:
        return 0.0
        
    try:
        # Удаляем все пробельные символы
        cleaned = re.sub(r"\s+", "", price_string)
        # Оставляем только цифры, точки и запятые
        cleaned = re.sub(r"[^\d.,]", "", cleaned)
        
        # Если в цене есть и точка, и запятая (например, 1,250.50)
        if "," in cleaned and "." in cleaned:
            # Если запятая идет первой, это разделитель тысяч (US стиль) -> просто убираем её
            if cleaned.find(",") < cleaned.find("."):
                cleaned = cleaned.replace(",", "")
            # Если точка идет первой (EU стиль, например, 1.250,50) -> убираем точку, запятую меняем на точку
            else:
                cleaned = cleaned.replace(".", "").replace(",", ".")
        # Если есть только запятая (EU стиль без копеек или с копейками через запятую: '150,50')
        elif "," in cleaned and "." not in cleaned:
            cleaned = cleaned.replace(",", ".")
            
        return float(cleaned)
    except Exception:
        # Если очистить не удалось, возвращаем 0.0, чтобы скрипт не падал
        return 0.0


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тест утилит:")
    
    log_message("info", "Запуск теста очистки цен...")
    
    # Тестируем разные форматы валют, которые могут прилететь с сайтов
    prices_to_test = ["$1,249.99", "350,00 €", " 1.500,75 руб ", "99"]
    
    for p in prices_to_test:
        print(f"  Исходная: {p:<15} -> Результат: {clean_price(p)}")

---

# ОШИБКА / TRACEBACK

(Ни traceback, ни лог выполнения не найдены.
 Сохрани вывод консоли в AI_INPUT/log.txt или реальный traceback в AI_INPUT/traceback.txt перед запуском debug.)

---

# ЗАДАЧА

1. **Диагноз** — что именно сломалось и почему (2–5 предложений).
2. **Исправление** — покажи только изменённые файлы с полным содержимым.
3. **Проверка** — как убедиться, что исправление работает.

## Ограничения

- Меняй **только** файлы, где реальная ошибка.
- Не рефактори код «заодно».
- Не меняй `main.py`, `config.py`, `exporter.py`, `browser.py`, `utils.py` без крайней необходимости.
- Не добавляй новые зависимости без объяснения.

## Типичные причины

- Неверный CSS-селектор (сайт изменил разметку)
- Timeout (страница грузится дольше ожидаемого)
- Cloudflare / 403
- Пустой ответ API
- Неверный формат cookies.json
- Playwright: элемент не найден / не кликабелен

---

# ФОРМАТ ОТВЕТА

### Диагноз
...

### Исправление

```python
# app/scraper.py (или другой файл) — полный исправленный код
```

### Как проверить
...
