#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session Manager.

Единая точка входа для создания и настройки `requests.Session`, а также
координатор HTTP-слоя фреймворка.

Архитектура HTTP-слоя (см. framework/ROADMAP.md, Milestone 2 и 3):

    Configuration Manager
            │
            ▼
    Request Profile Manager
            │
            ▼
    Session Manager
            │
     ┌──────┼────────┬────────┐
     ▼      ▼         ▼        ▼
    Cookie  Retry    Delay    Proxy
    Manager Manager  Manager  Manager

Session Manager — единственный компонент, который знает обо всех четырех
менеджерах (Cookie/Retry/Delay/Proxy) и координирует их вокруг сессии.

Важно: Cookie Manager, Retry Manager, Delay Manager и Proxy Manager
НЕ вызывают друг друга напрямую и ничего не знают друг о друге — каждый
зависит только от Configuration Manager. Это сохраняет их слабую
связанность и позволяет свободно добавлять новые компоненты
(Browser Manager) без риска затронуть уже существующие.

Session Manager:

* берет таймауты из Configuration Manager (`app/config.py`);
* берет браузерную идентичность из Request Profile Manager
  (`app/request_profile.py`) и применяет её заголовки к каждой новой сессии;
* делегирует куки — Cookie Manager, повторы — Retry Manager,
  задержки между запросами — Delay Manager, прокси — Proxy Manager
  (каждому — независимо от других);
* возвращает готовую к использованию сессию.

Session Manager НЕ реализует куки/повторы/задержки/прокси самостоятельно и
НЕ содержит логики скрапинга — вся реализация инкапсулирована в
соответствующих менеджерах.
"""

import requests

from app import config
from app.cookie_manager import CookieManager
from app.delay_manager import DelayManager
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile, RequestProfileManager
from app.retry_manager import RetryManager


class SessionManager:
    """
    Фабрика HTTP-сессий (`requests.Session`).

    Централизует создание сессий, чтобы вызывающий код никогда не создавал
    `requests.Session()` напрямую и не настраивал заголовки/куки/повторы вручную.
    """

    @staticmethod
    def create_session(
        profile: RequestProfile = None,
        load_cookies: bool = True,
        apply_retries: bool = True,
        apply_proxy: bool = True,
    ) -> requests.Session:
        """
        Создает новую `requests.Session`, настроенную выбранным профилем
        идентичности, таймаутом из конфигурации, куки из Cookie Manager,
        политикой повторов из Retry Manager и прокси из Proxy Manager.

        Args:
            profile (RequestProfile, optional): Профиль идентичности для
                применения к сессии. Если не передан, используется
                профиль по умолчанию (`RequestProfileManager.default_profile()`).
            load_cookies (bool): Если True (по умолчанию), сессия получает
                куки из Cookie Manager (`CookieManager.load()`).
            apply_retries (bool): Если True (по умолчанию), на сессию
                монтируется retry-адаптер из Retry Manager
                (`RetryManager.apply_to_session()`).
            apply_proxy (bool): Если True (по умолчанию), на сессию
                применяется прокси из Proxy Manager
                (`ProxyManager.apply_to_session()`). Если прокси не
                настроен (нет активного провайдера), сессия остается
                без изменений.

        Returns:
            requests.Session: Готовая к использованию HTTP-сессия с
                предустановленными заголовками, куки, повторами и прокси.
                Таймаут не хранится в самой сессии (`requests` не
                поддерживает это нативно) — используйте
                `SessionManager.timeout` при вызове
                `session.get(url, timeout=...)`.
        """
        session = requests.Session()

        active_profile = profile or RequestProfileManager.default_profile()
        session.headers.update(active_profile.to_headers())

        if load_cookies:
            CookieManager.apply_to_session(session)

        if apply_retries:
            RetryManager.apply_to_session(session)

        if apply_proxy:
            ProxyManager.apply_to_session(session)

        return session

    @staticmethod
    def wait_before_request(mode: str = None) -> None:
        """
        Выполняет паузу перед следующим запросом согласно политике
        Delay Manager (`DelayManager.wait()`).

        Это единая точка, через которую вызывающий код (будущие Requests
        Engine / Playwright Engine) может делать паузы между запросами,
        не импортируя Delay Manager напрямую — Session Manager выступает
        координатором HTTP-слоя, а сама логика задержки остается
        полностью в Delay Manager.

        Args:
            mode (str, optional): "fixed" или "random". По умолчанию —
                политика из `config.DELAY_MODE`.
        """
        DelayManager.wait(mode)

    # Таймаут запросов централизован в Configuration Manager.
    # Вызывающий код должен передавать его явно при выполнении запроса,
    # например: session.get(url, timeout=SessionManager.timeout)
    timeout: int = config.TIMEOUT


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    session = SessionManager.create_session()
    print(f"[{__file__}] Сессия создана. Заголовки:")
    for key, value in session.headers.items():
        print(f"  {key}: {value}")
    print(f"[{__file__}] Таймаут по умолчанию: {SessionManager.timeout}s")

    custom_profile = RequestProfileManager.create_profile(user_agent="TEST-UA/1.0")
    custom_session = SessionManager.create_session(profile=custom_profile)
    print(f"[{__file__}] Сессия с кастомным профилем, User-Agent: {custom_session.headers['User-Agent']}")
