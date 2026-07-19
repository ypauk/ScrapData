# app/scraper.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from playwright.sync_api import BrowserContext
from app.config import TIMEOUT


def fetch_page_with_playwright(context: BrowserContext, url: str) -> Optional[str]:
    """
    Выполняет GET-запрос к указанному URL с использованием Playwright.
    Получает HTML после выполнения JavaScript.
    
    Args:
        context (BrowserContext): Контекст браузера Playwright
        url (str): URL для запроса
        
    Returns:
        Optional[str]: HTML-код страницы или None при ошибке
    """
    try:
        print(f"[{__file__}] Загрузка страницы через Playwright: {url[:50]}...")
        
        # Создаем новую страницу
        page = context.new_page()
        
        # Устанавливаем таймаут
        page.set_default_timeout(TIMEOUT * 1000)  # конвертируем в миллисекунды
        
        # Переходим на страницу и ждем загрузки
        response = page.goto(url, wait_until="networkidle")
        
        if not response or response.status != 200:
            print(f"[{__file__}] Ошибка загрузки: статус {response.status if response else 'None'}")
            page.close()
            return None
        
        # Ждем появления карточек (динамическая загрузка)
        try:
            page.wait_for_selector("a.link.product-card.horizontal", timeout=10000)
            print(f"[{__file__}] Карточки объявлений загружены")
        except Exception:
            print(f"[{__file__}] Предупреждение: Карточки не найдены после ожидания")
        
        # Получаем HTML после рендеринга JavaScript
        html_content = page.content()
        page.close()
        
        print(f"[{__file__}] Контент получен (длина: {len(html_content)} символов)")
        return html_content
        
    except Exception as e:
        print(f"[{__file__}] Ошибка при загрузке страницы через Playwright: {e}")
        return None


def fetch_page_data(context=None) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Собирает сырой HTML-контент с первой страницы поиска.
    
    Args:
        context: BrowserContext от Playwright для динамической загрузки
        
    Returns:
        List[str]: Список с HTML-кодом страницы (всегда один элемент)
    """
    print(f"[{__file__}] Запуск процесса сбора данных...")
    
    # Проверка: контекст обязателен
    if context is None:
        print(f"[{__file__}] Критическая ошибка: контекст Playwright не передан")
        return []
    
    # URL из задания
    target_url = "https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1"
    
    html_contents = []
    
    try:
        html_content = fetch_page_with_playwright(context, target_url)
        if html_content and html_content.strip():
            html_contents.append(html_content)
            print(f"[{__file__}] Сбор данных успешно завершен. Получено страниц: 1")
        else:
            print(f"[{__file__}] Предупреждение: Получен пустой HTML-контент")
    except Exception as e:
        print(f"[{__file__}] Критическая ошибка при сборе данных: {e}")
    
    print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(html_contents)}")
    return html_contents