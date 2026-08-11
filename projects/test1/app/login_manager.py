#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login Manager (Login Support).

Централизованный компонент аутентификации фреймворка (см.
`framework/ROADMAP.md`, Milestone 4 — Login Support).

Login Manager — единственная точка, через которую скрапер-модули должны
выполнять аутентификацию на сайтах, требующих логин. Он НЕ дублирует
существующие менеджеры, а координирует их вокруг единого понятия
"аутентификация":

    Login Manager
            │
     ┌──────┼────────────┬─────────────────┐
     ▼      ▼             ▼                 ▼
    Requests  Playwright  Cookie Manager   Configuration
    Engine    Engine      (persist/restore) Manager

* Requests Engine / Playwright Engine — Login Manager использует уже
  созданный вызывающим кодом движок (сессию/браузер) для выполнения
  логина; он НЕ создает `requests.Session`/браузер самостоятельно —
  идентичность клиента (User-Agent, headers, locale, timezone) уже
  применена этими движками через Request Profile Manager;
* Cookie Manager — после успешного логина куки сохраняются/обновляются
  через `CookieManager.update()`/`CookieManager.save()`
  (Requests) или `PlaywrightEngine.update_cookies()` (Playwright,
  который сам делегирует Cookie Manager) — Login Manager не хранит
  куки самостоятельно;
* Configuration Manager — лимит попыток, тайм-аут, срок жизни
  аутентифицированной сессии и заголовки Bearer/API Key берутся из
  `app/config.py` (.env), без хардкода;
* Logging — используется `app.utils.log_message()`, как и во всех
  остальных менеджерах. Пароли/токены/куки никогда не логируются.

Архитектура основана на паттерне Strategy (аналогично `ProxyProvider` в
`app/proxy_manager.py`): `AuthStrategy` — абстрактный интерфейс
аутентификации, конкретные стратегии (`RequestsFormLoginStrategy`,
`PlaywrightFormLoginStrategy`, `CookieSessionStrategy`,
`BearerTokenStrategy`, `ApiKeyStrategy`) реализуют конкретные методы.
Добавление нового способа аутентификации (например, OAuth) в будущем —
это просто новый класс, реализующий `AuthStrategy.authenticate()`, без
изменения `LoginManager` или других стратегий.

Login Manager НЕ парсит HTML в бизнес-объекты, НЕ извлекает данные, НЕ
экспортирует данные, НЕ управляет пагинацией и НЕ содержит логики,
специфичной для конкретного сайта (URL/селекторы форм передаются
вызывающим кодом при создании стратегии).
"""

import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse

from app import config
from app.cookie_manager import CookieManager
from app.utils import log_message

# Причины неуспеха/сбоя логина, при которых повтор попытки НЕ выполняется
# (неверные учетные данные, CAPTCHA, отсутствующая форма — повтор не поможет
# и может усилить риск блокировки/лишних попыток входа).
_NON_RETRYABLE_REASONS = frozenset({"invalid_credentials", "captcha_detected", "missing_form"})


class LoginError(Exception):
    """
    Единое исключение Login Support для сбоев, возникших во время
    аутентификации (сетевые ошибки движка, таймаут навигации/запроса,
    отсутствие ожидаемой формы логина).

    Args:
        message (str): Человекочитаемое описание ошибки.
        reason (str): Машиночитаемая причина — одна из: "invalid_credentials",
            "timeout", "missing_form", "captcha_detected", "expired_session",
            "unexpected_redirect", "unknown".
    """

    def __init__(self, message: str, reason: str = "unknown") -> None:
        super().__init__(message)
        self.reason = reason


@dataclass
class AuthCredentials:
    """
    Универсальный (не привязанный к конкретному сайту) набор данных для
    аутентификации. Каждая стратегия использует только нужные ей поля.
    """

    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    api_key: Optional[str] = None
    # Дополнительные поля формы логина (например, CSRF-токен, "remember_me").
    extra_fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class AuthResult:
    """Результат попытки аутентификации."""

    success: bool
    reason: Optional[str] = None
    session_id: Optional[str] = None


# =====================================================================
# LOGIN DETECTION
#     Переиспользуемая, не зависящая от конкретного сайта логика
#     обнаружения ситуаций, требующих (пере-)аутентификации.
# =====================================================================


class LoginDetector:
    """
    Набор статических, не хранящих состояние проверок для обнаружения
    ситуаций логина (см. `tasks/TASK.md`, раздел Login Detection).

    Не содержит селекторов/URL конкретных сайтов — только структурные
    проверки (HTTP-статус, наличие пароля в форме, совпадение URL с
    известным URL страницы логина, ключевые слова CAPTCHA).
    """

    @staticmethod
    def is_unauthorized(status_code: int) -> bool:
        """True, если ответ сигнализирует об отсутствии/истечении авторизации (401/403)."""
        return status_code in (401, 403)

    @staticmethod
    def was_redirected_to_login(current_url: str, login_url: str) -> bool:
        """
        True, если текущий URL страницы совпадает с URL страницы логина
        (сравнение по пути, без query/fragment — типичный признак редиректа
        неавторизованного запроса на страницу входа).
        """
        if not current_url or not login_url:
            return False
        return urlparse(current_url).path.rstrip("/") == urlparse(login_url).path.rstrip("/")

    @staticmethod
    def contains_login_form(html: str) -> bool:
        """True, если HTML содержит поле пароля (`<input type="password">`)."""
        if not html:
            return False
        return bool(re.search(r'type=["\']password["\']', html, re.IGNORECASE))

    @staticmethod
    def contains_captcha(html: str) -> bool:
        """
        True, если HTML содержит одно из ключевых слов CAPTCHA
        (`config.LOGIN_CAPTCHA_KEYWORDS`, регистронезависимо).
        """
        if not html:
            return False
        lowered = html.lower()
        return any(keyword in lowered for keyword in config.LOGIN_CAPTCHA_KEYWORDS)


# =====================================================================
# AUTH STRATEGIES
#     Паттерн Strategy: LoginManager не знает, КАК выполняется логин —
#     эта логика инкапсулирована в конкретных реализациях AuthStrategy.
# =====================================================================


class AuthStrategy(ABC):
    """
    Абстрактный способ аутентификации.

    Любой новый метод аутентификации (OAuth, MFA и т.д.) должен
    реализовать этот интерфейс. `LoginManager` работает только через него
    и никогда не содержит специфичной для конкретной стратегии логики.
    """

    @abstractmethod
    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """
        Выполняет один шаг аутентификации.

        Args:
            credentials (AuthCredentials): Учетные данные для этой попытки.

        Returns:
            AuthResult: Результат попытки (успех/неуспех + причина).

        Raises:
            LoginError: При технических сбоях (таймаут, сеть, отсутствие
                ожидаемой формы) — вызывающий код (`LoginManager`) решает,
                стоит ли повторять попытку, на основе `LoginError.reason`.
        """
        raise NotImplementedError


def _requests_session_cookies_to_list(session: Any) -> List[Dict[str, Any]]:
    """
    Конвертирует куки `requests.Session.cookies` (RequestsCookieJar) в
    универсальный формат Cookie Manager (список словарей
    `{"name", "value", "domain", "path"}`).
    """
    return [
        {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain or "",
            "path": cookie.path or "/",
        }
        for cookie in session.cookies
    ]


class RequestsFormLoginStrategy(AuthStrategy):
    """
    Аутентификация через HTML-форму логина (username/password) с
    использованием `RequestsEngine` (без браузера).

    После успешного логина куки сессии сохраняются через Cookie Manager
    (если `config.LOGIN_COOKIE_PERSISTENCE` включен), чтобы сессия могла
    быть восстановлена в будущих запусках через `CookieSessionStrategy`.
    """

    def __init__(
        self,
        engine: Any,
        login_url: str,
        username_field: str = "username",
        password_field: str = "password",
        extra_data: Optional[Dict[str, str]] = None,
        success_check: Optional[Callable[[Any], bool]] = None,
        failure_check: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """
        Args:
            engine (RequestsEngine): Движок, через который отправляется
                POST-запрос логина (уже несет применённые Request Profile/
                Cookie/Proxy Manager настройки).
            login_url (str): URL, на который отправляется форма логина.
            username_field (str): Имя поля формы для логина/email.
            password_field (str): Имя поля формы для пароля.
            extra_data (Dict[str, str], optional): Дополнительные
                статические поля формы (например, CSRF-токен, "remember_me").
            success_check (Callable[[Response], bool], optional): Кастомная
                проверка успеха по `requests.Response` (переопределяет
                дефолтную эвристику "нет формы логина в ответе").
            failure_check (Callable[[Response], bool], optional): Кастомная
                проверка неуспеха по `requests.Response` (например, наличие
                текста "Invalid password" на странице).
        """
        self.engine = engine
        self.login_url = login_url
        self.username_field = username_field
        self.password_field = password_field
        self.extra_data = extra_data or {}
        self.success_check = success_check
        self.failure_check = failure_check

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        from app.requests_engine import RequestsEngineError  # локальный импорт: избегаем циклической зависимости

        data = {
            self.username_field: credentials.username or "",
            self.password_field: credentials.password or "",
            **self.extra_data,
            **credentials.extra_fields,
        }

        try:
            response = self.engine.post(self.login_url, data=data)
        except RequestsEngineError as exc:
            raise LoginError(f"Запрос логина завершился ошибкой: {exc}", reason="timeout") from exc

        if LoginDetector.is_unauthorized(response.status_code):
            return AuthResult(success=False, reason="invalid_credentials")

        html = response.text

        if LoginDetector.contains_captcha(html):
            return AuthResult(success=False, reason="captcha_detected")

        if self.failure_check is not None and self.failure_check(response):
            return AuthResult(success=False, reason="invalid_credentials")

        if self.success_check is not None:
            if not self.success_check(response):
                return AuthResult(success=False, reason="invalid_credentials")
        elif LoginDetector.contains_login_form(html):
            # Дефолтная эвристика: форма логина всё еще на странице -> вход не удался.
            return AuthResult(success=False, reason="invalid_credentials")

        if config.LOGIN_COOKIE_PERSISTENCE:
            CookieManager.update(_requests_session_cookies_to_list(self.engine.session))

        return AuthResult(success=True)


class PlaywrightFormLoginStrategy(AuthStrategy):
    """
    Аутентификация через HTML-форму логина с использованием
    `PlaywrightEngine` (заполнение полей и клик по кнопке отправки в
    реальном браузере — для сайтов с JS-защитой/динамическими формами).

    После успешного логина куки браузерного контекста сохраняются через
    `PlaywrightEngine.update_cookies()` (который сам делегирует Cookie
    Manager) — Login Manager не дублирует эту логику.
    """

    def __init__(
        self,
        engine: Any,
        login_url: str,
        username_selector: str,
        password_selector: str,
        submit_selector: str,
        failure_selector: Optional[str] = None,
        success_check: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """
        Args:
            engine (PlaywrightEngine): Движок, через который выполняется
                навигация и заполнение формы.
            login_url (str): URL страницы логина.
            username_selector (str): CSS/text-селектор поля логина/email.
            password_selector (str): CSS/text-селектор поля пароля.
            submit_selector (str): CSS/text-селектор кнопки отправки формы.
            failure_selector (str, optional): Селектор, появляющийся только
                при неудачном логине (например, ".error-message").
            success_check (Callable[[PlaywrightEngine], bool], optional):
                Кастомная проверка успеха (переопределяет дефолтную
                эвристику "нет формы логина в HTML после отправки").
        """
        self.engine = engine
        self.login_url = login_url
        self.username_selector = username_selector
        self.password_selector = password_selector
        self.submit_selector = submit_selector
        self.failure_selector = failure_selector
        self.success_check = success_check

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        from app.playwright_engine import PlaywrightEngineError  # локальный импорт: избегаем циклической зависимости

        try:
            self.engine.goto(self.login_url)
            self.engine.wait_for_selector(self.username_selector)
            self.engine.page.fill(self.username_selector, credentials.username or "")
            self.engine.page.fill(self.password_selector, credentials.password or "")
            self.engine.page.click(self.submit_selector)
            self.engine.wait_for_load("networkidle")
        except PlaywrightEngineError as exc:
            raise LoginError(f"Навигация/заполнение формы логина завершилось ошибкой: {exc}", reason="timeout") from exc

        html = self.engine.content()

        if LoginDetector.contains_captcha(html):
            return AuthResult(success=False, reason="captcha_detected")

        if self.failure_selector is not None:
            try:
                self.engine.page.wait_for_selector(self.failure_selector, timeout=1000)
                return AuthResult(success=False, reason="invalid_credentials")
            except Exception:
                pass  # селектор ошибки не появился — логин, вероятно, успешен

        if self.success_check is not None:
            if not self.success_check(self.engine):
                return AuthResult(success=False, reason="invalid_credentials")
        elif LoginDetector.contains_login_form(html):
            return AuthResult(success=False, reason="invalid_credentials")

        if config.LOGIN_COOKIE_PERSISTENCE:
            self.engine.update_cookies()

        return AuthResult(success=True)


class CookieSessionStrategy(AuthStrategy):
    """
    Восстанавливает аутентифицированную сессию исключительно из ранее
    сохраненных куки (Cookie Manager), без учетных данных — используется,
    когда логин уже был выполнен в прошлом запуске и куки еще валидны.
    """

    def __init__(self, validate: Optional[Callable[[], bool]] = None) -> None:
        """
        Args:
            validate (Callable[[], bool], optional): Дополнительная проверка
                валидности восстановленной сессии (например, тестовый запрос
                к защищенной странице). Если не передана, сессия считается
                валидной при наличии хотя бы одной сохраненной куки.
        """
        self.validate = validate

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        cookies = CookieManager.load()
        if not cookies:
            return AuthResult(success=False, reason="expired_session")

        if self.validate is not None and not self.validate():
            return AuthResult(success=False, reason="expired_session")

        return AuthResult(success=True)


class BearerTokenStrategy(AuthStrategy):
    """
    Аутентификация через Bearer Token — токен добавляется как заголовок
    к переданной сессии/движку без выполнения HTTP-запроса логина.
    """

    def __init__(self, session: Any, header_name: Optional[str] = None) -> None:
        """
        Args:
            session (requests.Session): Сессия, к которой применяется заголовок.
            header_name (str, optional): Имя заголовка.
                По умолчанию — `config.LOGIN_BEARER_HEADER_NAME`.
        """
        self.session = session
        self.header_name = header_name or config.LOGIN_BEARER_HEADER_NAME

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        if not credentials.token:
            return AuthResult(success=False, reason="invalid_credentials")

        self.session.headers[self.header_name] = f"Bearer {credentials.token}"
        return AuthResult(success=True)


class ApiKeyStrategy(AuthStrategy):
    """
    Аутентификация через статический API Key — добавляется как заголовок
    к переданной сессии без выполнения HTTP-запроса логина.
    """

    def __init__(self, session: Any, header_name: Optional[str] = None) -> None:
        """
        Args:
            session (requests.Session): Сессия, к которой применяется заголовок.
            header_name (str, optional): Имя заголовка.
                По умолчанию — `config.LOGIN_API_KEY_HEADER_NAME`.
        """
        self.session = session
        self.header_name = header_name or config.LOGIN_API_KEY_HEADER_NAME

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        if not credentials.api_key:
            return AuthResult(success=False, reason="invalid_credentials")

        self.session.headers[self.header_name] = credentials.api_key
        return AuthResult(success=True)


# =====================================================================
# LOGIN MANAGER
#     Единая точка входа: оркестрирует выбранную стратегию, повторы,
#     логирование и переиспользование уже аутентифицированных сессий.
# =====================================================================


class LoginManager:
    """
    Централизованная точка входа для аутентификации.

    Хранит только факт "сессия X аутентифицирована в момент времени T"
    (`_authenticated_sessions`) — сам процесс логина полностью делегирован
    переданной `AuthStrategy`. Это позволяет `ensure_login()` избегать
    повторного логина для уже аутентифицированной логической сессии.
    """

    # session_id -> monotonic-время последней успешной аутентификации.
    _authenticated_sessions: Dict[str, float] = {}

    @classmethod
    def login(
        cls,
        strategy: AuthStrategy,
        credentials: Optional[AuthCredentials] = None,
        session_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
    ) -> AuthResult:
        """
        Выполняет аутентификацию через переданную стратегию, повторяя
        попытку только при технических сбоях (`LoginError`, отличных от
        "invalid_credentials"/"captcha_detected"/"missing_form") — эти три
        причины считаются окончательными и никогда не повторяются, чтобы
        не спровоцировать блокировку аккаунта/IP.

        Args:
            strategy (AuthStrategy): Реализация способа аутентификации.
            credentials (AuthCredentials, optional): Учетные данные.
                По умолчанию — пустые (валидно для `CookieSessionStrategy`).
            session_id (str, optional): Идентификатор логической сессии —
                при успехе помечается как аутентифицированная для
                последующего переиспользования через `ensure_login()`.
            max_attempts (int, optional): Максимум попыток.
                По умолчанию — `config.LOGIN_MAX_ATTEMPTS`.

        Returns:
            AuthResult: Результат последней попытки.
        """
        active_credentials = credentials or AuthCredentials()
        attempts = max_attempts if max_attempts is not None else config.LOGIN_MAX_ATTEMPTS

        session_suffix = f" (session={session_id})" if session_id else ""
        log_message("info", f"Попытка логина начата{session_suffix}")

        last_result = AuthResult(success=False, reason="unknown")

        for attempt in range(1, max(attempts, 1) + 1):
            try:
                result = strategy.authenticate(active_credentials)
            except LoginError as exc:
                log_message("error", f"Ошибка логина{session_suffix}: {exc} (причина={exc.reason})")
                last_result = AuthResult(success=False, reason=exc.reason)
                if exc.reason in _NON_RETRYABLE_REASONS:
                    return last_result
                continue

            if result.success:
                log_message("info", f"Логин успешен{session_suffix}")
                if session_id:
                    cls._authenticated_sessions[session_id] = time.monotonic()
                    result.session_id = session_id
                return result

            log_message("error", f"Логин не удался{session_suffix} (причина={result.reason})")
            last_result = result
            if result.reason in _NON_RETRYABLE_REASONS:
                return last_result

        return last_result

    @classmethod
    def is_session_authenticated(cls, session_id: str) -> bool:
        """
        Проверяет, аутентифицирована ли логическая сессия и не истек ли
        срок её жизни (`config.LOGIN_SESSION_LIFETIME_SECONDS`, 0 — без
        ограничения). Истекшая запись автоматически удаляется.
        """
        authenticated_at = cls._authenticated_sessions.get(session_id)
        if authenticated_at is None:
            return False

        lifetime = config.LOGIN_SESSION_LIFETIME_SECONDS
        if lifetime > 0 and (time.monotonic() - authenticated_at) >= lifetime:
            cls._authenticated_sessions.pop(session_id, None)
            log_message("info", f"Сессия '{session_id}' истекла (превышен срок жизни логина)")
            return False

        return True

    @classmethod
    def ensure_login(
        cls,
        strategy: AuthStrategy,
        credentials: Optional[AuthCredentials] = None,
        session_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
    ) -> AuthResult:
        """
        Переиспользует уже аутентифицированную сессию, если она
        существует и не истекла (`is_session_authenticated()`), иначе
        выполняет полный логин через `login()`.

        Это основной метод для вызывающего кода (скрапер-модулей) —
        избавляет от необходимости самостоятельно проверять, нужен ли
        повторный вход перед каждым скрапинг-джобом.

        Args:
            strategy (AuthStrategy): Реализация способа аутентификации.
            credentials (AuthCredentials, optional): Учетные данные.
            session_id (str, optional): Идентификатор логической сессии.
            max_attempts (int, optional): Максимум попыток логина.

        Returns:
            AuthResult: Результат (успех переиспользования или нового логина).
        """
        if session_id and cls.is_session_authenticated(session_id):
            log_message("info", f"Сессия '{session_id}' переиспользована (уже аутентифицирована)")
            return AuthResult(success=True, session_id=session_id)

        return cls.login(strategy, credentials, session_id=session_id, max_attempts=max_attempts)

    @classmethod
    def invalidate_session(cls, session_id: str) -> None:
        """Явно помечает сессию как неаутентифицированную (например, после 401 в середине скрапинга)."""
        if cls._authenticated_sessions.pop(session_id, None) is not None:
            log_message("info", f"Сессия '{session_id}' помечена как неаутентифицированная")

    @classmethod
    def reset(cls) -> None:
        """Сбрасывает состояние всех аутентифицированных сессий (используется в тестах)."""
        cls._authenticated_sessions.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()
    strategy = RequestsFormLoginStrategy(
        engine=engine,
        login_url="https://httpbin.org/post",  # демо-эндпоинт, не реальная форма логина
        username_field="username",
        password_field="password",
        success_check=lambda response: response.status_code == 200,
    )

    result = LoginManager.login(strategy, AuthCredentials(username="demo", password="demo"), session_id="demo-job")
    print(f"[{__file__}] Результат логина: {result}")
    print(f"[{__file__}] Сессия аутентифицирована: {LoginManager.is_session_authenticated('demo-job')}")

    engine.close()
