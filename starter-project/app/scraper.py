#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from typing import List
from playwright.sync_api import BrowserContext, Page
from app.config import TIMEOUT

def navigate_and_wait(page: Page, url: str) -> bool:
    """
    Безопасно переходит по URL и ждет полной загрузки страницы.
    Возвращает True в случае успеха, False при ошибке.
    """
    try:
        print(f"[{__file__}] Переход на: {url}")
        
        # Переходим на сайт и ждем, пока сеть полностью успокоится (domcontentloaded или networkidle)
        response = page.goto(url, timeout=TIMEOUT * 1000, wait_until="domcontentloaded")
        
        # Проверяем статус ответа (актуально для незащищенных Cloudflare сайтов)
        if response and response.status in [403, 503]:
            print(f"[{__file__}] Предупреждение: Сайт вернул статус {response.status} (Возможно блокировка).")
            return False
            
        # Даем небольшую паузу для отработки JavaScript-скриптов сайта
        page.wait_for_timeout(2000)
        return True
        
    except Exception as e:
        print(f"[{__file__}] Ошибка при переходе на {url}: {e}")
        return False

def fetch_page_data(context: BrowserContext) -> List[str]:
    """
    Главная сетевая функция сборщика. Управляет перемещением по сайту.
    Принимает контекст Playwright, возвращает список сырых строк HTML.
    """
    raw_pages_content = []
    
    # Создаем новую вкладку внутри переданного контекста
    page: Page = context.new_page()

    # --- Пример логики обхода страниц (ИИ перепишет это под конкретную пагинацию/ТЗ) ---
    # Для теста берем одну базовую страницу
    target_urls = ["https://example.com"]
    
    for url in target_urls:
        success = navigate_and_wait(page, url)
        
        if success:
            # --- Сюда можно вставить логику скролла или кликов (если нужно по ТЗ) ---
            # page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            # ---------------------------------------------------------------------
            
            # Забираем текущее состояние HTML-кода (уже после отработки всего JS)
            html_content = page.content()
            raw_pages_content.append(html_content)
        else:
            print(f"[{__file__}] Пропуск страницы из-за ошибки загрузки: {url}")
            
        # Защитная пауза между запросами (краулинг-делей), чтобы не забанили
        time.sleep(1)
    # ---------------------------------------------------------------------------------

    # Закрываем конкретную вкладку после сбора данных
    page.close()
    
    print(f"[{__file__}] Сбор контента завершен. Собрано страниц: {len(raw_pages_content)}")
    return raw_pages_content


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    from app.browser import get_browser_context
    
    print(f"[{__file__}] Запуск изолированного теста скрапера...")
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False)
        pages = fetch_page_data(ctx)
        ctx.browser.close()
        
        if pages:
            print("Тест успешный. Длина полученного HTML:", len(pages[0]))