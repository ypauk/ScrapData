#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Фабрика браузерного контекста Playwright.

Низкоуровневая функция, инкапсулирующая запуск Chromium и создание
изолированного `BrowserContext`. Используется Playwright Engine
(`app/playwright_engine.py`) как единственная точка, где реально
вызывается `playwright_instance.chromium.launch()` / `browser.new_context()` —
сам движок не дублирует эту логику.

Идентичность клиента (User-Agent, Accept-Language, locale, timezone,
viewport) берется из Request Profile Manager (`app/request_profile.py`),
который остается единственным источником правды об идентичности — как для
`requests` (`RequestProfile.to_headers()`), так и для Playwright
(`RequestProfile.to_playwright_context_kwargs()`). Прокси (если передан)
применяется "как есть" — ротацию и выбор прокси выполняет Proxy Manager
до вызова этой функции.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext

from app.config import (
    HEADLESS,
    BROWSER_VIEWPORT,
    BROWSER_LOCALE,
    BROWSER_TIMEZONE,
    BROWSER_LAUNCH_ARGS,
)
from app.cookie_manager import CookieManager
from app.request_profile import RequestProfile, RequestProfileManager


def get_browser_context(
    playwright_instance,
    headless: bool = None,
    user_agent: str = None,
    cookies_path: Path = None,
    profile: Optional[RequestProfile] = None,
    proxy: Optional[Dict[str, Any]] = None,
) -> BrowserContext:
    """
    Инициализирует настроенный браузер и возвращает изолированный контекст.

    Все дефолтные значения (headless, флаги запуска) берутся из
    единого источника правды — app/config.py. Идентичность клиента
    (user-agent, viewport, локаль, часовой пояс, Accept-Language, DNT)
    берется из Request Profile Manager (`profile`, либо профиль по
    умолчанию, если не передан). Явно переданный `user_agent` имеет
    приоритет над профилем (обратная совместимость).

    Args:
        playwright_instance: Запущенный драйвер Playwright
            (`sync_playwright().start()` или `with sync_playwright() as p`).
        headless (bool, optional): Режим headless. По умолчанию — `config.HEADLESS`.
        user_agent (str, optional): Явный User-Agent, переопределяющий профиль.
        cookies_path (Path, optional): Путь к файлу куки (Cookie Manager).
        profile (RequestProfile, optional): Профиль идентичности клиента.
            По умолчанию — `RequestProfileManager.default_profile()`.
        proxy (Dict[str, Any], optional): Kwargs прокси в формате Playwright
            (`{"server": ..., "username": ..., "password": ...}`), обычно
            полученные через `ProxyManager.to_playwright_proxy_kwargs()`.
            Проверка/ротация/выбор прокси НЕ выполняется здесь.

    Returns:
        BrowserContext: Готовый к использованию изолированный контекст браузера.
    """
    # 1. Режим headless определяется централизованно в config.py (.env / Docker)
    if headless is None:
        headless = HEADLESS

    # 2. Идентичность клиента — единый источник правды: Request Profile Manager
    active_profile = profile or RequestProfileManager.default_profile()
    profile_kwargs = active_profile.to_playwright_context_kwargs()

    # Явно переданный user_agent имеет приоритет над профилем (обратная совместимость)
    if user_agent:
        profile_kwargs["user_agent"] = user_agent

    print(f"[{__file__}] Запуск Chromium (Headless={headless})...")

    # 3. Запуск браузера с флагами против падений в Docker (централизованы в config.py)
    browser: Browser = playwright_instance.chromium.launch(
        headless=headless,
        args=BROWSER_LAUNCH_ARGS
    )

    # 4. Создание контекста с маскировкой параметров профиля идентичности
    new_context_kwargs: Dict[str, Any] = {
        "user_agent": profile_kwargs["user_agent"],
        "viewport": profile_kwargs.get("viewport") or BROWSER_VIEWPORT,
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": profile_kwargs.get("locale") or BROWSER_LOCALE,
        "timezone_id": profile_kwargs.get("timezone_id") or BROWSER_TIMEZONE,
        "extra_http_headers": profile_kwargs.get("extra_http_headers"),
    }

    # 5. Прокси применяется "как есть" — Proxy Manager уже выбрал/проверил его
    if proxy:
        new_context_kwargs["proxy"] = proxy

    context: BrowserContext = browser.new_context(**new_context_kwargs)

    # 6. Подкладываем куки через Cookie Manager (единая точка загрузки куки)
    if cookies_path:
        CookieManager.apply_to_playwright_context(context, cookies=CookieManager.load(cookies_path))

    return context



# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    # Локальный тест
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    test_cookies = ROOT_DIR / "AI_INPUT" / "cookies.json"
    
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False, cookies_path=test_cookies)
        page = ctx.new_page()
        page.goto("https://bot.sannysoft.com/") # Хороший сайт для проверки детекта
        page.wait_for_timeout(5000)
        ctx.browser.close()
