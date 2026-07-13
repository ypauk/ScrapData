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

(нет analysis.md)

---

# ПЛАН ПРОЕКТА

(нет project_plan.md)

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

--- app/scraper.py ---
import os
from typing import List
from app.config import AI_INPUT_DIR

def load_local_html(file_path: str) -> str:
    """
    Открывает и считывает текстовое содержимое сохраненного HTML-файла.
    
    Args:
        file_path (str): Абсолютный или относительный путь к файлу.
        
    Returns:
        str: Строка с сырым HTML-кодом страницы.
        
    Raises:
        FileNotFoundError: Если целевой файл отсутствует на диске.
    """
    if not os.path.exists(file_path):
        print(f"[{__file__}] Ошибка: Файл не найден по пути {file_path}")
        raise FileNotFoundError(f"Файл {file_path} не найден.")
        
    print(f"[{__file__}] Чтение локального файла: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def fetch_page_data() -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Собирает сырой HTML-контент из локального источника.
    
    Returns:
        List[str]: Список строк, содержащих сырой HTML страниц.
    """
    print(f"[{__file__}] Запуск процесса сбора данных...")
    
    # Формируем путь к файлу на основе конфигурационных путей ядра
    target_file = os.path.join(AI_INPUT_DIR, "page.html")
    
    html_contents = []
    try:
        html_data = load_local_html(target_file)
        if html_data.strip():
            html_contents.append(html_data)
        else:
            print(f"[{__file__}] Предупреждение: Считанный файл page.html пуст.")
    except FileNotFoundError as e:
        print(f"[{__file__}] Критическая ошибка сбора данных: {e}")
        # Возвращаем пустой список, чтобы не вызывать критическое падение всей системы
    except Exception as e:
        print(f"[{__file__}] Непредвиденная ошибка при чтении файла: {e}")
        
    print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(html_contents)}")
    return html_contents

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

(traceback не найден — сохрани ошибку в AI_OUTPUT/traceback.txt)

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
