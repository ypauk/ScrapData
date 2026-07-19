# app/scraper.py
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