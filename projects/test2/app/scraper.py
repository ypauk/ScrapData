# app/scraper.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from playwright.sync_api import BrowserContext

from app.config import AI_INPUT_DIR
from app.utils import random_delay

# Константы для запроса
TARGET_URL = "https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page=2"
TIMEOUT = 30000  # миллисекунд


def fetch_page(context: BrowserContext, url: str) -> Optional[str]:
    """
    Выполняет загрузку страницы через Playwright для корректного рендеринга JavaScript.

    Args:
        context (BrowserContext): Контекст браузера Playwright.
        url (str): URL страницы для загрузки.

    Returns:
        Optional[str]: HTML-код страницы в виде строки или None в случае ошибки.
    """
    try:
        print(f"[{__file__}] Загрузка страницы: {url}")
        
        # Создаем новую страницу
        page = context.new_page()
        
        # Устанавливаем таймаут
        page.set_default_timeout(TIMEOUT)
        
        # Переходим на страницу и ждем загрузки
        page.goto(url, wait_until="networkidle")
        
        # Имитация поведения человека
        random_delay(1.0, 2.0)
        
        # Получаем HTML после рендеринга JavaScript
        html_content = page.content()
        
        # Закрываем страницу
        page.close()
        
        print(f"[{__file__}] Страница успешно загружена. Размер: {len(html_content)} символов")
        return html_content
        
    except Exception as e:
        print(f"[{__file__}] Ошибка при загрузке страницы: {e}")
        return None


def fetch_page_data(context: BrowserContext) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Загружает страницу №2 AUTO.RIA через Playwright и возвращает HTML-контент.

    Args:
        context (BrowserContext): Контекст браузера Playwright.

    Returns:
        List[str]: Список строк, содержащих сырой HTML страницы.
    """
    print(f"[{__file__}] Запуск процесса сбора данных с AUTO.RIA...")
    print(f"[{__file__}] Целевой URL: {TARGET_URL}")

    # Загружаем страницу через Playwright
    html_content = fetch_page(context, TARGET_URL)

    if html_content:
        print(f"[{__file__}] Сбор данных завершен. Получено страниц: 1")
        return [html_content]
    else:
        print(f"[{__file__}] Ошибка: Не удалось загрузить страницу. Возвращаем пустой список.")
        return []


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    from app.browser import get_browser_context
    from app.config import COOKIES_FILE
    
    print(f"[{__file__}] Тестовый запуск scraper...")
    
    with sync_playwright() as playwright:
        context = get_browser_context(
            playwright_instance=playwright,
            cookies_path=COOKIES_FILE
        )
        
        result = fetch_page_data(context)
        
        if result:
            print(f"[{__file__}] Успешно получен HTML. Размер: {len(result[0])} символов")
            # Сохраняем для проверки
            with open(AI_INPUT_DIR / "fetched_page.html", "w", encoding="utf-8") as f:
                f.write(result[0])
            print(f"[{__file__}] HTML сохранен в {AI_INPUT_DIR / 'fetched_page.html'}")
        else:
            print(f"[{__file__}] Не удалось получить HTML")
        
        context.browser.close()