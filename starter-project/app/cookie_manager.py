#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cookie Manager.

Единый компонент, отвечающий за загрузку, сохранение, обновление и очистку
HTTP-куки для всего фреймворка.

Cookie Manager:

* хранит куки в простом JSON-файле (по умолчанию `app/config.py::COOKIES_FILE`);
* валидирует формат куки перед применением;
* предоставляет куки для `requests.Session` (Session Manager);
* предоставляет куки для контекста Playwright (готово для будущей интеграции).

Формат хранения — список словарей вида Playwright/Puppeteer:
    {"name": str, "value": str, "domain": str, "path": str, ...}
Это универсальный, широко используемый формат, легко конвертируемый как в
`requests.cookies.RequestsCookieJar`, так и в `BrowserContext.add_cookies()`.

Cookie Manager НЕ создает HTTP-сессии, НЕ выполняет запросы, НЕ управляет
прокси/повторами/задержками и НЕ содержит логики скрапинга.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import COOKIES_FILE

# Минимально обязательные поля, без которых куки считаются невалидными.
_REQUIRED_COOKIE_FIELDS = ("name", "value")


class CookieManager:
    """
    Централизованный менеджер персистентных HTTP-куки.

    Хранилище по умолчанию — JSON-файл (`COOKIES_FILE`). Для миграции на
    другое хранилище (например, БД) достаточно переопределить методы
    `load`/`save`/`clear` — остальные методы (`apply_to_session`,
    `apply_to_playwright_context`, `_validate`) не зависят от способа хранения.
    """

    @staticmethod
    def _validate(cookies: Any) -> List[Dict[str, Any]]:
        """
        Проверяет, что куки представлены списком словарей с обязательными
        полями `name` и `value`. Невалидные записи отбрасываются с
        предупреждением, чтобы не блокировать работу всего фреймворка.

        Args:
            cookies (Any): Сырые данные, прочитанные из хранилища.

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список валидных куки.
        """
        if not isinstance(cookies, list):
            print(f"[{__file__}] Ошибка формата: ожидался список куки, получено {type(cookies)}")
            return []

        valid_cookies = []
        for cookie in cookies:
            if isinstance(cookie, dict) and all(field in cookie for field in _REQUIRED_COOKIE_FIELDS):
                valid_cookies.append(cookie)
            else:
                print(f"[{__file__}] Предупреждение: пропущена невалидная запись куки: {cookie}")

        return valid_cookies

    @classmethod
    def load(cls, path: Path = COOKIES_FILE) -> List[Dict[str, Any]]:
        """
        Загружает и валидирует куки из JSON-файла.

        Args:
            path (Path): Путь к файлу хранения куки.

        Returns:
            List[Dict[str, Any]]: Список валидных куки (пустой, если файл
                отсутствует, пуст или содержит некорректные данные).
        """
        if not path.exists() or path.stat().st_size == 0:
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_cookies = json.load(f)
        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке куки из {path.name}: {e}")
            return []

        return cls._validate(raw_cookies)

    @classmethod
    def save(cls, cookies: List[Dict[str, Any]], path: Path = COOKIES_FILE) -> None:
        """
        Сохраняет куки в JSON-файл, перезаписывая предыдущее содержимое.

        Args:
            cookies (List[Dict[str, Any]]): Список куки для сохранения.
            path (Path): Путь к файлу хранения куки.
        """
        valid_cookies = cls._validate(cookies)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(valid_cookies, f, ensure_ascii=False, indent=2)
            print(f"[{__file__}] Куки сохранены в {path.name} (Всего: {len(valid_cookies)})")
        except Exception as e:
            print(f"[{__file__}] Ошибка при сохранении куки в {path.name}: {e}")

    @classmethod
    def update(cls, new_cookies: List[Dict[str, Any]], path: Path = COOKIES_FILE) -> List[Dict[str, Any]]:
        """
        Обновляет существующие куки новыми значениями (по совпадению
        `name` + `domain`) и добавляет отсутствующие, затем сохраняет результат.

        Args:
            new_cookies (List[Dict[str, Any]]): Новые/обновленные куки
                (например, полученные после успешного запроса).
            path (Path): Путь к файлу хранения куки.

        Returns:
            List[Dict[str, Any]]: Итоговый объединенный список куки.
        """
        existing = cls.load(path)
        valid_new = cls._validate(new_cookies)

        index = {(c.get("name"), c.get("domain")): i for i, c in enumerate(existing)}
        for cookie in valid_new:
            key = (cookie.get("name"), cookie.get("domain"))
            if key in index:
                existing[index[key]] = cookie
            else:
                existing.append(cookie)

        cls.save(existing, path)
        return existing

    @classmethod
    def clear(cls, path: Path = COOKIES_FILE) -> None:
        """
        Очищает хранилище куки (перезаписывает файл пустым списком).

        Args:
            path (Path): Путь к файлу хранения куки.
        """
        cls.save([], path)
        print(f"[{__file__}] Куки очищены: {path.name}")

    @staticmethod
    def apply_to_session(session, cookies: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Применяет куки к `requests.Session`, предоставляя их Session Manager.

        Args:
            session (requests.Session): Сессия, к которой будут применены куки.
            cookies (List[Dict[str, Any]], optional): Список куки. Если не
                передан, куки загружаются из хранилища по умолчанию.
        """
        active_cookies = cookies if cookies is not None else CookieManager.load()
        for cookie in active_cookies:
            session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain", ""),
                path=cookie.get("path", "/"),
            )

        if active_cookies:
            print(f"[{__file__}] Куки применены к сессии (Всего: {len(active_cookies)})")

    @staticmethod
    def apply_to_playwright_context(context, cookies: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Применяет куки к контексту Playwright (`BrowserContext.add_cookies`).

        Args:
            context (BrowserContext): Контекст браузера Playwright.
            cookies (List[Dict[str, Any]], optional): Список куки. Если не
                передан, куки загружаются из хранилища по умолчанию.
        """
        active_cookies = cookies if cookies is not None else CookieManager.load()
        if not active_cookies:
            return

        try:
            context.add_cookies(active_cookies)
            print(f"[{__file__}] Куки применены к контексту Playwright (Всего: {len(active_cookies)})")
        except Exception as e:
            print(f"[{__file__}] Ошибка при применении куки к контексту Playwright: {e}")


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    sample_cookies = [
        {"name": "session_id", "value": "abc123", "domain": "example.com", "path": "/"},
        {"name": "invalid_entry"},  # будет отбракован при валидации
    ]

    print(f"[{__file__}] Сохранение тестовых куки...")
    CookieManager.save(sample_cookies)

    loaded = CookieManager.load()
    print(f"[{__file__}] Загружено куки: {loaded}")

    CookieManager.update([{"name": "session_id", "value": "updated456", "domain": "example.com", "path": "/"}])
    print(f"[{__file__}] После обновления: {CookieManager.load()}")

    CookieManager.clear()
    print(f"[{__file__}] После очистки: {CookieManager.load()}")
