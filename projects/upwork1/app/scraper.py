# app/scraper.py
"""
⚠️ ДЕМО-ПРИМЕР, А НЕ УНИВЕРСАЛЬНЫЙ ДЕФОЛТ ⚠️

Код ниже — рабочий сквозной пример сбора данных для демонстрации полного
цикла workflow (`ai_workflow.py analyze/project/module scraper/module parser`)
на реальном заказе (OLX, объявления авто). В демо-режиме HTML не скачивается
по сети, а читается локально из `AI_INPUT/page.html` — это соответствует
именно тому кейсу, под который был сгенерирован `app/parser.py` (см. его
докстринг), а не общий шаблон получения данных для любого сайта.

Для нового заказа этот файл нужно заменить одним из способов:
  1. python ai_workflow.py module scraper <project_name>
     (сгенерирует промпт для ИИ на основе анализа/плана нового сайта:
     запросы через RequestsEngine/PlaywrightEngine, пагинация, логин и т.д.;
     ответ ИИ сохраняется в AI_OUTPUT/03_scraper_answer.py и переносится сюда)
  2. Вручную переписать `fetch_page_data`, сохранив сигнатуру
     `fetch_page_data(context=None) -> List[str]`, которую вызывает
     `app/main.py`, и используя готовые компоненты `app/requests_engine.py`,
     `app/playwright_engine.py`, `app/pagination.py`, `app/infinite_scroll.py`,
     `app/login_manager.py` и т.д. — они универсальны и НЕ требуют правок.
"""
import os
from typing import List
from app.config import PAGE_HTML_FILE


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

def fetch_page_data(context=None) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Собирает сырой HTML-контент из локального источника.
    Принимает необязательный аргумент context для совместимости с основным потоком main.py.
    
    Args:
        context (BrowserContext, optional): Контекст браузера Playwright.
        
    Returns:
        List[str]: Список строк, содержащих сырой HTML страниц.
    """
    print(f"[{__file__}] Запуск процесса сбора данных...")
    
    # Путь к тестовому HTML-файлу централизован в конфигурации (app/config.py)
    target_file = PAGE_HTML_FILE
    
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