#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Request Profile Manager.

Централизует понятие "браузерная идентичность" (Request Profile) —
набор HTTP-заголовков и клиентских параметров (locale, timezone, viewport),
которые описывают, "кем представляется" скрапер при обращении к сайту.

Профиль является ЕДИНСТВЕННЫМ источником правды об идентичности клиента
и может быть переиспользован:

* модулем на базе `requests`/`httpx` — через `RequestProfile.to_headers()`;
* модулем Playwright (`app/browser.py`) — через
  `RequestProfile.to_playwright_context_kwargs()`.

Этот модуль НЕ выполняет запросы, НЕ управляет сессиями, куками,
прокси или повторами — это ответственность будущих компонентов
(Session Manager, Cookie Manager, Proxy Manager, Retry Manager).
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from app import config


@dataclass(frozen=True)
class RequestProfile:
    """
    Неизменяемое описание полной браузерной идентичности клиента.

    Содержит как HTTP-заголовки, так и клиентские параметры окружения
    (locale, timezone, viewport), общие для Requests и Playwright.
    """

    user_agent: str
    accept: str
    accept_language: str
    accept_encoding: str
    connection: str
    upgrade_insecure_requests: str
    sec_fetch_dest: str
    sec_fetch_mode: str
    sec_fetch_site: str
    dnt: str
    locale: str
    timezone: str
    viewport: Dict[str, int] = field(default_factory=dict)

    def to_headers(self) -> Dict[str, str]:
        """
        Формирует словарь HTTP-заголовков, готовый для передачи в
        `requests`/`httpx` (например, `requests.get(url, headers=profile.to_headers())`).
        """
        return {
            "User-Agent": self.user_agent,
            "Accept": self.accept,
            "Accept-Language": self.accept_language,
            "Accept-Encoding": self.accept_encoding,
            "Connection": self.connection,
            "Upgrade-Insecure-Requests": self.upgrade_insecure_requests,
            "Sec-Fetch-Dest": self.sec_fetch_dest,
            "Sec-Fetch-Mode": self.sec_fetch_mode,
            "Sec-Fetch-Site": self.sec_fetch_site,
            "DNT": self.dnt,
        }

    def to_playwright_context_kwargs(self) -> Dict[str, Any]:
        """
        Формирует словарь именованных аргументов, готовый для передачи
        в `browser.new_context(**kwargs)` в будущей интеграции с Playwright.

        Заголовки Accept/Sec-Fetch-* здесь не передаются, так как Playwright
        сам управляет частью низкоуровневых заголовков навигации; при
        необходимости их можно точечно докинуть через `extra_http_headers`.
        """
        return {
            "user_agent": self.user_agent,
            "locale": self.locale,
            "timezone_id": self.timezone,
            "viewport": self.viewport,
            "extra_http_headers": {
                "Accept-Language": self.accept_language,
                "DNT": self.dnt,
            },
        }


class RequestProfileManager:
    """
    Фабрика/реестр Request Profile.

    Предоставляет один переиспользуемый профиль по умолчанию, собранный из
    централизованной конфигурации (`app/config.py`), а также позволяет
    создавать кастомные профили с точечным переопределением полей —
    без дублирования дефолтных значений.
    """

    @staticmethod
    def default_profile() -> RequestProfile:
        """Возвращает профиль идентичности, собранный из app/config.py."""
        return RequestProfile(
            user_agent=config.DEFAULT_USER_AGENT,
            accept=config.DEFAULT_ACCEPT,
            accept_language=config.DEFAULT_ACCEPT_LANGUAGE,
            accept_encoding=config.DEFAULT_ACCEPT_ENCODING,
            connection=config.DEFAULT_CONNECTION,
            upgrade_insecure_requests=config.DEFAULT_UPGRADE_INSECURE_REQUESTS,
            sec_fetch_dest=config.DEFAULT_SEC_FETCH_DEST,
            sec_fetch_mode=config.DEFAULT_SEC_FETCH_MODE,
            sec_fetch_site=config.DEFAULT_SEC_FETCH_SITE,
            dnt=config.DEFAULT_DNT,
            locale=config.BROWSER_LOCALE,
            timezone=config.BROWSER_TIMEZONE,
            viewport=dict(config.BROWSER_VIEWPORT),
        )

    @classmethod
    def create_profile(cls, **overrides: Any) -> RequestProfile:
        """
        Создает профиль на основе дефолтного, переопределяя только
        указанные поля. Позволяет получать кастомные идентичности
        (например, мобильный User-Agent) без дублирования остальных полей.

        Args:
            **overrides: Поля `RequestProfile` для переопределения.

        Returns:
            RequestProfile: Новый профиль с примененными переопределениями.
        """
        base = cls.default_profile()
        return RequestProfile(**{**base.__dict__, **overrides})


# Готовый к использованию профиль по умолчанию (ленивая точка доступа).
def get_default_profile() -> RequestProfile:
    """Возвращает профиль идентичности по умолчанию (удобный шорткат)."""
    return RequestProfileManager.default_profile()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    profile = RequestProfileManager.default_profile()
    print(f"[{__file__}] Профиль идентичности по умолчанию:")
    print("  Headers:", profile.to_headers())
    print("  Playwright kwargs:", profile.to_playwright_context_kwargs())

    mobile_profile = RequestProfileManager.create_profile(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
    )
    print(f"[{__file__}] Кастомный (мобильный) профиль:")
    print("  Headers:", mobile_profile.to_headers())
