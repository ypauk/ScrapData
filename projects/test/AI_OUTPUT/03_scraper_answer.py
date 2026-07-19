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