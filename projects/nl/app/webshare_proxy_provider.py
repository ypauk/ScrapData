#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Webshare Proxy Provider.

Реализация `ProxyProvider` (см. `app/proxy_manager.py`), получающая список
прокси из официального Webshare Proxy List API
(https://proxy.webshare.io/api/v2/proxy/list/).

Как и `FileProxyProvider` (`app/file_proxy_provider.py`), этот модуль
подтверждает провайдер-независимость Proxy Manager: Proxy Manager работает
с `WebshareProxyProvider` через тот же интерфейс `ProxyProvider`, не зная
ничего об API Webshare, аутентификации или формате его ответа.

Webshare Proxy Provider:

* аутентифицируется через API-ключ (`config.WEBSHARE_API_KEY`), который
  берется ИСКЛЮЧИТЕЛЬНО из Configuration Manager (переменные окружения /
  .env) — ключ никогда не хардкодится и не появляется в логах;
* нормализует ответ API в тот же формат URL-строк
  (`http://[user:pass@]host:port`), который использует File Provider —
  Proxy Manager получает данные в едином виде независимо от источника;
* кэширует загруженный список прокси в памяти на `config.WEBSHARE_CACHE_TTL_SECONDS`
  секунд, чтобы не дергать API при каждом обращении (`get_proxy()`) и не
  упереться в rate limit;
* корректно обрабатывает сетевые ошибки, таймауты, невалидный API-ключ,
  HTTP 401/403/429, а также некорректный/пустой ответ API — во всех
  случаях возвращает пустой список вместо падения приложения.

Webshare Proxy Provider НЕ выбирает и НЕ ротирует прокси из списка, НЕ
валидирует их и НЕ проверяет здоровье, НЕ выполняет retry-логику (это
ответственность Retry Manager, а не провайдера) и ничего не знает о других
провайдерах (File Provider, BrightData и т.д.).
"""

import time
from typing import Any, Dict, List, Optional

import requests

from app import config
from app.proxy_manager import ProxyProvider


class WebshareProxyProvider(ProxyProvider):
    """
    Провайдер, получающий список прокси из Webshare Proxy List API.

    Хранит нормализованный список прокси в памяти и обновляет его не
    чаще, чем раз в `cache_ttl_seconds` — простой TTL-кэш без внешних
    зависимостей (БД/Redis не требуются для этой задачи).
    """

    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        cache_ttl_seconds: int = None,
        timeout: int = None,
    ):
        """
        Args:
            api_key (str, optional): API-ключ Webshare. По умолчанию —
                `config.WEBSHARE_API_KEY` (переменная окружения `WEBSHARE_API_KEY`).
            api_url (str, optional): URL Webshare Proxy List API.
                По умолчанию — `config.WEBSHARE_API_URL`.
            cache_ttl_seconds (int, optional): Время жизни кэша в секундах.
                По умолчанию — `config.WEBSHARE_CACHE_TTL_SECONDS`.
            timeout (int, optional): Таймаут HTTP-запроса к API (секунды).
                По умолчанию — `config.WEBSHARE_API_TIMEOUT`.
        """
        self.api_key = api_key if api_key is not None else config.WEBSHARE_API_KEY
        self.api_url = api_url or config.WEBSHARE_API_URL
        self.cache_ttl_seconds = (
            cache_ttl_seconds if cache_ttl_seconds is not None else config.WEBSHARE_CACHE_TTL_SECONDS
        )
        self.timeout = timeout if timeout is not None else config.WEBSHARE_API_TIMEOUT

        self._proxies: List[str] = []
        self._last_fetched_at: float = 0.0

    def _is_cache_valid(self) -> bool:
        """Проверяет, не истек ли TTL текущего закэшированного списка прокси."""
        if not self._proxies:
            return False
        return (time.time() - self._last_fetched_at) < self.cache_ttl_seconds

    @staticmethod
    def _normalize_entry(entry: Dict[str, Any]) -> Optional[str]:
        """
        Приводит одну запись прокси из ответа Webshare API к единому
        формату URL (`http://[user:pass@]host:port`), совпадающему с
        форматом File Provider.

        Webshare возвращает записи вида:
            {
                "proxy_address": "1.2.3.4",
                "port": 8080,
                "username": "user",
                "password": "pass",
                ...
            }

        Args:
            entry (Dict[str, Any]): Одна запись из `results` ответа API.

        Returns:
            Optional[str]: Нормализованный URL прокси, либо `None`, если
                запись не содержит обязательных полей `proxy_address`/`port`.
        """
        host = entry.get("proxy_address")
        port = entry.get("port")
        if not host or not port:
            return None

        username = entry.get("username")
        password = entry.get("password")
        if username and password:
            return f"http://{username}:{password}@{host}:{port}"
        return f"http://{host}:{port}"

    def _fetch_from_api(self) -> List[str]:
        """
        Выполняет запрос к Webshare Proxy List API и нормализует ответ.

        Обрабатывает все ожидаемые сбои (нет ключа, сетевые ошибки,
        таймаут, неавторизован, rate limit, невалидный JSON) без падения
        приложения — во всех случаях возвращает пустой список с понятным
        сообщением в лог. API-ключ никогда не попадает в лог.

        Returns:
            List[str]: Нормализованный список прокси (пустой при любой ошибке).
        """
        if not self.api_key:
            print(f"[{__file__}] Ошибка: WEBSHARE_API_KEY не задан в конфигурации "
                  f"(Configuration Manager) — запрос к Webshare API не выполнен.")
            return []

        headers = {"Authorization": f"Token {self.api_key}"}
        # Webshare Proxy List API v2 требует обязательный query-параметр "mode".
        # "direct" — прямое подключение к прокси (стандартный режим для большинства планов).
        params = {"mode": "direct", "page_size": 100}

        try:
            response = requests.get(self.api_url, headers=headers, params=params, timeout=self.timeout)

        except requests.exceptions.Timeout:
            print(f"[{__file__}] Ошибка: превышен таймаут запроса к Webshare API "
                  f"({self.timeout}с).")
            return []
        except requests.exceptions.ConnectionError as e:
            print(f"[{__file__}] Ошибка сети при запросе к Webshare API: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[{__file__}] Непредвиденная ошибка запроса к Webshare API: {e}")
            return []

        if response.status_code in (401, 403):
            print(f"[{__file__}] Ошибка авторизации Webshare API "
                  f"(HTTP {response.status_code}): проверьте WEBSHARE_API_KEY.")
            return []

        if response.status_code == 429:
            print(f"[{__file__}] Webshare API вернул HTTP 429 (превышен лимит запросов). "
                  f"Попробуйте позже или увеличьте WEBSHARE_CACHE_TTL_SECONDS.")
            return []

        if response.status_code != 200:
            print(f"[{__file__}] Webshare API вернул неожиданный статус "
                  f"HTTP {response.status_code}: {response.text[:200]}")
            return []

        try:
            payload = response.json()
        except ValueError as e:
            print(f"[{__file__}] Ошибка: невалидный JSON в ответе Webshare API: {e}")
            return []

        results = payload.get("results")
        if not isinstance(results, list):
            print(f"[{__file__}] Ошибка: неожиданный формат ответа Webshare API "
                  f"(отсутствует список 'results').")
            return []

        proxies: List[str] = []
        for entry in results:
            normalized = self._normalize_entry(entry) if isinstance(entry, dict) else None
            if normalized:
                proxies.append(normalized)

        if not proxies:
            print(f"[{__file__}] Предупреждение: Webshare API вернул пустой список прокси.")

        print(f"[{__file__}] Загружено прокси из Webshare API: {len(proxies)}")
        return proxies

    def _ensure_fresh(self) -> None:
        """Обновляет кэш прокси из API, если TTL истек или кэш пуст."""
        if self._is_cache_valid():
            return

        self._proxies = self._fetch_from_api()
        self._last_fetched_at = time.time()

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый прокси из (при необходимости обновленного) кэша,
        либо `None`, если список пуст или запрос к API не удался.
        """
        self._ensure_fresh()
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный закэшированный список прокси (обновляя кэш при
        необходимости). Полезно для будущего Proxy Rotation.

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        self._ensure_fresh()
        return list(self._proxies)

    def reload(self) -> List[str]:
        """
        Принудительно обновляет список прокси из API, игнорируя TTL кэша.

        Returns:
            List[str]: Обновленный список загруженных прокси.
        """
        self._proxies = self._fetch_from_api()
        self._last_fetched_at = time.time()
        return list(self._proxies)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.proxy_manager import ProxyManager

    provider = WebshareProxyProvider()
    print(f"[{__file__}] Webshare API URL: {provider.api_url}")
    print(f"[{__file__}] API-ключ задан: {bool(provider.api_key)}")
    print(f"[{__file__}] Все загруженные прокси: {provider.get_all_proxies()}")
    print(f"[{__file__}] Активный прокси (get_proxy): {provider.get_proxy()}")

    # Демонстрация интеграции с Proxy Manager без изменения его кода/API —
    # тот же паттерн, что и для FileProxyProvider.
    ProxyManager.set_provider(provider)
    print(f"[{__file__}] ProxyManager.get_proxy() после смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] ProxyManager.to_requests_dict(): {ProxyManager.to_requests_dict()}")
