#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Playwright Engine.

Централизованный слой браузерной автоматизации фреймворка для всех
JavaScript-зависимых сайтов (см. `framework/ROADMAP.md`, Milestone 4).

Playwright Engine — единственная точка, через которую скрапер-модули
должны запускать браузер, открывать страницы и получать их содержимое.
Он НЕ содержит собственной логики куки/прокси/задержек/идентичности —
вся эта логика уже инкапсулирована в существующих менеджерах и
применяется автоматически, аналогично тому, как Requests Engine
использует Session Manager для HTTP-запросов:

    Playwright Engine
            │
            ▼
    app/browser.py (get_browser_context)  ──────────────────┐
            │                                                │
     ┌──────┼─────────┬─────────┬─────────┐                  │
     ▼      ▼          ▼         ▼         ▼                 ▼
    Request Cookie    Proxy    Delay   Configuration     (Retry остаётся
    Profile Manager   Manager  Manager Manager           централизованным,
    Manager                                               см. ниже)

Playwright Engine:

* делегирует запуск браузера и создание контекста функции
  `app.browser.get_browser_context()` — единственному месту, где
  реально вызывается `playwright.chromium.launch()` / `browser.new_context()`,
  чтобы не дублировать эту логику (см. `app/browser.py`);
* автоматически применяет идентичность клиента через Request Profile
  Manager (`app/request_profile.py`), куки — через Cookie Manager
  (`app/cookie_manager.py`), прокси — через Proxy Manager
  (`app/proxy_manager.py`) — вызывающий код ничего не настраивает вручную;
* делает паузу перед каждой навигацией через `SessionManager.wait_before_request()`
  (Delay Manager) — как и Requests Engine, не реализует собственную политику пауз;
* сообщает Proxy Manager об успехе/сбое каждой навигации
  (`ProxyManager.report_proxy_success()`/`report_proxy_failure()`), что
  прозрачно питает Proxy Health Check/Rotation/Sticky Sessions, если
  движку передан `session_id` — идентично Requests Engine;
* НЕ реализует собственный цикл повторов при навигации — как и Requests
  Engine, Playwright Engine оставляет retry-политику централизованной
  (вызывающий код может обернуть `goto()` в `RetryManager.call_with_retry()`
  при необходимости — сам движок только сообщает об исходе через Proxy Manager);
* оборачивает все ожидаемые сбои Playwright (таймаут, навигация, отсутствие
  селектора, ошибка запуска браузера, падение страницы) в единое понятное
  исключение `PlaywrightEngineError` — вызывающему коду не нужно знать о
  внутренних исключениях Playwright;
* использует централизованную функцию логирования `app.utils.log_message`
  для запуска/закрытия браузера, навигации и ошибок (без избыточного лога).

Playwright Engine НЕ парсит HTML (это Milestone 5 — Parsing), НЕ
экспортирует данные, НЕ содержит селекторов конкретных сайтов, НЕ
реализует пагинацию/infinite scroll/логин — эти возможности будут
реализованы отдельными задачами (см. `tasks/TASK.md`, раздел Scope) на
основе этого движка.
"""

from pathlib import Path
from typing import Any, List, Optional

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from app import config
from app.browser import get_browser_context
from app.cookie_manager import CookieManager
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile, RequestProfileManager
from app.session_manager import SessionManager
from app.utils import log_message


class PlaywrightEngineError(Exception):
    """
    Единое исключение Playwright Engine для всех сбоев браузерной
    автоматизации (запуск браузера, навигация, таймаут, отсутствие
    селектора, выполнение JS), оставшихся после обработки движком.

    Позволяет вызывающему коду (будущим скрапер-модулям) обрабатывать
    ошибки браузера без необходимости импортировать и знать про
    исключения `playwright.sync_api`.
    """


class PlaywrightEngine:
    """
    Централизованный исполнитель браузерной автоматизации для JS-сайтов.

    Каждый инстанс управляет одним запущенным Playwright-драйвером, одним
    браузером и одним изолированным `BrowserContext`. Все компоненты слоя
    автоматизации (Configuration/Request Profile/Cookie/Proxy/Delay Manager)
    подключаются автоматически — вызывающий код не настраивает их вручную.

    Используется как контекстный менеджер (рекомендуемый способ):

        with PlaywrightEngine() as engine:
            engine.goto("https://example.com")
            html = engine.content()

    либо через явные `start()`/`close()`.
    """

    def __init__(
        self,
        profile: Optional[RequestProfile] = None,
        session_id: Optional[str] = None,
        cookies_path: Optional[Path] = None,
        headless: Optional[bool] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Args:
            profile (RequestProfile, optional): Профиль идентичности клиента
                (User-Agent, locale, timezone, viewport, Accept-Language).
                По умолчанию — `RequestProfileManager.default_profile()`.
            session_id (str, optional): Идентификатор логической сессии для
                Sticky Sessions/Proxy Rotation/Health Check
                (см. `ProxyManager.get_proxy(session_id=...)`). Если не
                передан — прокси выбирается без привязки к сессии.
            cookies_path (Path, optional): Путь к файлу куки (Cookie Manager).
                По умолчанию — `config.COOKIES_FILE`.
            headless (bool, optional): Режим headless. По умолчанию — `config.HEADLESS`.
            user_agent (str, optional): Явный User-Agent, переопределяющий профиль.
        """
        self.profile = profile
        self.session_id = session_id
        self.cookies_path = cookies_path or config.COOKIES_FILE
        self.headless = headless
        self.user_agent = user_agent

        self._playwright = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    # =====================================================================
    # ЖИЗНЕННЫЙ ЦИКЛ БРАУЗЕРА
    # =====================================================================

    def start(self) -> "PlaywrightEngine":
        """
        Запускает драйвер Playwright, браузер Chromium и создает изолированный
        контекст с автоматически примененными идентичностью/куки/прокси.

        Returns:
            PlaywrightEngine: self (для удобного чейнинга).

        Raises:
            PlaywrightEngineError: При сбое запуска браузера.
        """
        proxy_url = ProxyManager.get_proxy(session_id=self.session_id)
        proxy_kwargs = ProxyManager.to_playwright_proxy_kwargs(proxy_url) if proxy_url else None

        try:
            self._playwright = sync_playwright().start()
            self._context = get_browser_context(
                self._playwright,
                headless=self.headless,
                user_agent=self.user_agent,
                cookies_path=self.cookies_path,
                profile=self.profile,
                proxy=proxy_kwargs,
            )
        except Exception as exc:
            self._teardown_playwright()
            log_message("error", f"Не удалось запустить браузер: {exc}")
            raise PlaywrightEngineError(f"Ошибка запуска браузера: {exc}") from exc

        self._context.set_default_timeout(config.PLAYWRIGHT_TIMEOUT_MS)
        log_message("info", f"Браузер запущен (headless={self.headless if self.headless is not None else config.HEADLESS})")
        return self

    def close(self) -> None:
        """
        Сохраняет актуальные куки сессии и закрывает браузер/драйвер Playwright.

        Безопасна к повторному вызову и к вызову без предварительного `start()`.
        """
        if self._context is not None:
            try:
                self.save_cookies()
            except Exception as exc:
                log_message("error", f"Не удалось сохранить куки при закрытии: {exc}")

            try:
                browser: Optional[Browser] = self._context.browser
                self._context.close()
                if browser is not None:
                    browser.close()
            except Exception as exc:
                log_message("error", f"Ошибка при закрытии браузера: {exc}")
            finally:
                self._context = None
                self._page = None

        self._teardown_playwright()
        log_message("info", "Браузер закрыт")

    def _teardown_playwright(self) -> None:
        """Останавливает драйвер Playwright, если он был запущен."""
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
            finally:
                self._playwright = None

    def __enter__(self) -> "PlaywrightEngine":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # =====================================================================
    # СТРАНИЦЫ И НАВИГАЦИЯ
    # =====================================================================

    @property
    def context(self) -> BrowserContext:
        """Возвращает активный `BrowserContext` (после `start()`)."""
        if self._context is None:
            raise PlaywrightEngineError("Контекст браузера не инициализирован — вызовите start() перед использованием.")
        return self._context

    @property
    def page(self) -> Page:
        """Возвращает текущую страницу, создавая её при первом обращении."""
        if self._page is None:
            self._page = self.new_page()
        return self._page

    def new_page(self) -> Page:
        """
        Создает новую страницу в текущем контексте и делает её активной.

        Returns:
            Page: Новая страница Playwright.
        """
        try:
            self._page = self.context.new_page()
        except Exception as exc:
            raise PlaywrightEngineError(f"Не удалось создать страницу: {exc}") from exc
        return self._page

    def goto(
        self,
        url: str,
        wait_until: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Открывает URL на текущей странице.

        Перед навигацией выполняется пауза согласно Delay Manager
        (`SessionManager.wait_before_request()`) — как и в Requests Engine.
        После навигации сообщает Proxy Manager об успехе/сбое.

        Args:
            url (str): Целевой URL.
            wait_until (str, optional): Условие завершения навигации
                ("load", "domcontentloaded", "networkidle", "commit").
                По умолчанию — `config.PLAYWRIGHT_WAIT_UNTIL`.
            timeout (float, optional): Таймаут навигации (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            Response Playwright (или None, если навигация не создала документ).

        Raises:
            PlaywrightEngineError: При таймауте или сбое навигации.
        """
        effective_wait_until = wait_until or config.PLAYWRIGHT_WAIT_UNTIL
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS

        SessionManager.wait_before_request()

        log_message("info", f"Навигация: {url}")
        try:
            response = self.page.goto(
                url,
                wait_until=effective_wait_until,
                timeout=effective_timeout,
            )
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Таймаут навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Таймаут при открытии {url}: {exc}") from exc
        except PlaywrightError as exc:
            log_message("error", f"Сбой навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Не удалось открыть {url}: {exc}") from exc

        ProxyManager.report_proxy_success(session_id=self.session_id)
        self.update_cookies()
        return response

    def wait_for_load(self, state: str = "load", timeout: Optional[float] = None) -> None:
        """
        Ожидает завершения загрузки страницы.

        Args:
            state (str): Состояние загрузки ("load", "domcontentloaded", "networkidle").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Raises:
            PlaywrightEngineError: При таймауте ожидания.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            self.page.wait_for_load_state(state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            raise PlaywrightEngineError(f"Таймаут ожидания состояния загрузки '{state}': {exc}") from exc

    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Ожидает появления селектора на странице.

        Args:
            selector (str): CSS/text-селектор Playwright.
            state (str): Ожидаемое состояние элемента
                ("attached", "detached", "visible", "hidden").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            ElementHandle: Найденный элемент.

        Raises:
            PlaywrightEngineError: Если селектор не появился до истечения таймаута.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            return self.page.wait_for_selector(selector, state=state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Селектор не найден: {selector}")
            raise PlaywrightEngineError(f"Селектор '{selector}' не появился: {exc}") from exc

    def content(self) -> str:
        """
        Возвращает полный HTML текущей страницы (без какого-либо парсинга).

        Returns:
            str: Сырой HTML страницы.

        Raises:
            PlaywrightEngineError: При сбое получения содержимого (например,
                падении страницы).
        """
        try:
            return self.page.content()
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось получить содержимое страницы: {exc}") from exc

    def evaluate(self, script: str, *args: Any) -> Any:
        """
        Выполняет JavaScript в контексте текущей страницы.

        Args:
            script (str): JS-выражение или функция (`page.evaluate()`).
            *args: Аргументы, передаваемые в скрипт.

        Returns:
            Any: Результат выполнения скрипта.

        Raises:
            PlaywrightEngineError: При сбое выполнения скрипта.
        """
        try:
            return self.page.evaluate(script, *args)
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось выполнить JavaScript: {exc}") from exc

    # =====================================================================
    # ИНТЕГРАЦИЯ С COOKIE MANAGER
    # =====================================================================

    def update_cookies(self) -> List[dict]:
        """
        Забирает текущие куки контекста браузера и обновляет ими персистентное
        хранилище через Cookie Manager (`CookieManager.update()`), не
        затирая куки, установленные вне текущей сессии.

        Returns:
            List[dict]: Итоговый объединенный список куки.
        """
        current_cookies = self.context.cookies()
        return CookieManager.update(current_cookies, path=self.cookies_path)

    def save_cookies(self) -> None:
        """
        Полностью перезаписывает файл куки текущим состоянием контекста
        браузера (`CookieManager.save()`).
        """
        current_cookies = self.context.cookies()
        CookieManager.save(current_cookies, path=self.cookies_path)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    with PlaywrightEngine(headless=False) as engine:
        engine.goto("https://bot.sannysoft.com/")
        engine.wait_for_load("networkidle")
        print(f"[{__file__}] Длина HTML: {len(engine.content())}")
