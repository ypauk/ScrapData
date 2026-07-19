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