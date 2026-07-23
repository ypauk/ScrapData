#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Централизованный менеджер конфигурации проекта.

Единый источник правды для всех настраиваемых параметров: путей проекта,
поведения запуска (Docker/Headless), таймаутов и повторов, а также
настроек идентификации клиента (User-Agent, локаль, часовой пояс, viewport),
которые используются как модулем Playwright (app/browser.py), так и любым
кодом на базе requests/httpx.

Все значения читаются из переменных окружения (.env) с безопасными
дефолтами, поэтому изменение поведения парсера не требует правок кода —
достаточно поменять .env.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

# Загружаем переменные из .env (в корне starter-project) в окружение процесса
# ДО того, как ниже будут читаться os.getenv(...). Без этого вызова значения
# из .env не подхватываются при обычном запуске (python -m app...), только
# если переменные заданы вручную в самой ОС/оболочке.
# override=False — переменные, уже заданные в реальном окружении (например,
# в Docker/CI), имеют приоритет над файлом .env.
load_dotenv(Path(__file__).parent.parent / ".env", override=False)


# =====================================================================
# 0. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ЧТЕНИЯ ОКРУЖЕНИЯ
# =====================================================================


def _get_bool(name: str, default: str = "0") -> bool:
    """Читает булево значение из переменной окружения ("1"/"true"/"yes" -> True)."""
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes")


def _get_int(name: str, default: int) -> int:
    """Читает целочисленное значение из переменной окружения с безопасным фолбэком."""
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


# =====================================================================
# 1. ПУТИ К ПАПКАМ СТРУКТУРЫ (Абсолютные)
# =====================================================================
APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent.resolve()

# Папки для работы с ИИ
AI_INPUT_DIR = ROOT_DIR / "AI_INPUT"
AI_OUTPUT_DIR = ROOT_DIR / "AI_OUTPUT"

# Входные и выходные данные для скрипта
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"

# Файлы окружения и зависимостей
COOKIES_FILE = AI_INPUT_DIR / "cookies.json"
HEADERS_FILE = AI_INPUT_DIR / "headers.json"
PAGE_HTML_FILE = AI_INPUT_DIR / "page.html"

# Гарантируем, что рабочие папки проекта существуют
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 2. НАСТРОЙКИ ЗАПУСКА, ТАЙМАУТЫ И ПОВТОРЫ
#    (общие для Requests и Playwright, .env / Окружение)
# =====================================================================

# Если переменная IS_DOCKER установлена, принудительно включаем headless
IS_DOCKER = _get_bool("IS_DOCKER", "0")
HEADLESS = _get_bool("HEADLESS", "1") or IS_DOCKER

# Таймауты и повторы применимы как к HTTP-запросам (requests), так и к Playwright
TIMEOUT = _get_int("SCRAPER_TIMEOUT", 30)  # в секундах
RETRY_COUNT = _get_int("SCRAPER_RETRY", 3)

# Множитель экспоненциальной задержки между повторами (используется Retry Manager).
# Задержка между попытками растет как: backoff_factor * (2 ** (попытка - 1))
RETRY_BACKOFF_FACTOR = float(os.getenv("SCRAPER_RETRY_BACKOFF", "0.5"))

# Добавлять случайный джиттер к задержке повтора, чтобы избежать
# синхронных всплесков запросов при параллельном скрапинге.
RETRY_JITTER = _get_bool("SCRAPER_RETRY_JITTER", "1")

# HTTP-статусы, которые считаются временными сбоями и подлежат повтору.
RETRYABLE_STATUS_CODES: List[int] = [
    int(code.strip())
    for code in os.getenv("SCRAPER_RETRYABLE_STATUS_CODES", "429,500,502,503,504").split(",")
    if code.strip()
]

# Политика задержек между запросами (используется Delay Manager).
# Режим: "fixed" — постоянная пауза, "random" — случайная пауза в диапазоне.
DELAY_MODE = os.getenv("SCRAPER_DELAY_MODE", "random").strip().lower()
DELAY_FIXED_SECONDS = float(os.getenv("SCRAPER_DELAY_FIXED", "2.0"))
DELAY_MIN_SECONDS = float(os.getenv("SCRAPER_DELAY_MIN", "1.0"))
DELAY_MAX_SECONDS = float(os.getenv("SCRAPER_DELAY_MAX", "3.0"))

# --- Requests Engine (app/requests_engine.py) ---
REQUESTS_VERIFY_SSL = _get_bool("REQUESTS_VERIFY_SSL", "1")
REQUESTS_ALLOW_REDIRECTS = _get_bool("REQUESTS_ALLOW_REDIRECTS", "1")
REQUESTS_MAX_REDIRECTS = _get_int("REQUESTS_MAX_REDIRECTS", 30)




# Настройки сети и прокси
PROXY_URL: Optional[str] = os.getenv("PROXY_URL") or None  # Формат: http://username:password@host:port

# Путь к файлу со списком прокси для File Proxy Provider (app/file_proxy_provider.py).
# Формат файла — по одной записи в строке, поддерживаются: ip:port,
# ip:port:username:password, а также готовые URL (http://..., socks5://...).
PROXY_FILE = Path(os.getenv("PROXY_FILE_PATH", str(AI_INPUT_DIR / "proxies.txt")))

# Схема (http/https/socks5), используемая File Proxy Provider для записей без
# явной схемы (ip:port или ip:port:username:password).
PROXY_FILE_DEFAULT_SCHEME = os.getenv("PROXY_FILE_DEFAULT_SCHEME", "http")

# --- Webshare Proxy Provider (app/webshare_proxy_provider.py) ---
# API-ключ Webshare. Никогда не хардкодится — только через окружение (.env).
WEBSHARE_API_KEY: Optional[str] = os.getenv("WEBSHARE_API_KEY") or None

# Базовый URL официального Webshare Proxy List API.
WEBSHARE_API_URL = os.getenv("WEBSHARE_API_URL", "https://proxy.webshare.io/api/v2/proxy/list/")

# Сколько секунд переиспользовать закэшированный список прокси до повторного
# запроса к API (снижает нагрузку на API и риск упереться в rate limit).
WEBSHARE_CACHE_TTL_SECONDS = _get_int("WEBSHARE_CACHE_TTL_SECONDS", 300)

# Таймаут запроса к Webshare API (секунды). По умолчанию — общий TIMEOUT проекта.
WEBSHARE_API_TIMEOUT = _get_int("WEBSHARE_API_TIMEOUT", TIMEOUT)

# --- Proxy Cache (app/proxy_cache.py) ---
# Локальный файл, в котором Proxy Cache хранит последний успешно
# загруженный список прокси (provider-независимо: Webshare, File и т.д.).
PROXY_CACHE_FILE = Path(os.getenv("PROXY_CACHE_FILE_PATH", str(AI_INPUT_DIR / "proxy_cache.json")))

# Сколько секунд считать закэшированный список прокси актуальным до
# необходимости обновления через провайдер (не путать с
# WEBSHARE_CACHE_TTL_SECONDS — это TTL персистентного файлового кэша,
# который переживает перезапуск процесса).
PROXY_CACHE_TTL_SECONDS = _get_int("PROXY_CACHE_TTL_SECONDS", 300)

# --- Proxy Selection (app/proxy_selector.py) ---
# Активная стратегия выбора прокси из пула: "first" (первый доступный)
# или "random" (случайный). Новые стратегии регистрируются через
# `ProxySelector.register_strategy()` без изменения кода.
PROXY_SELECTION_STRATEGY = os.getenv("PROXY_SELECTION_STRATEGY", "first").strip().lower()

# --- Proxy Rotation (app/proxy_rotation.py) ---
# Активная политика ротации прокси: "never", "every_request",
# "every_n_requests" или "after_failure". Новые политики регистрируются
# через `ProxyRotation.register_policy()` без изменения кода.
# "every_request" — политика по умолчанию, воспроизводящая поведение
# Proxy Manager до появления Proxy Rotation (обратная совместимость).
PROXY_ROTATION_POLICY = os.getenv("PROXY_ROTATION_POLICY", "every_request").strip().lower()

# Количество запросов между ротациями для политики "every_n_requests".
PROXY_ROTATION_EVERY_N = _get_int("PROXY_ROTATION_EVERY_N", 5)

# --- Proxy Health Check (app/health_check.py) ---
# Все пороги настраиваются через .env; смена любого порога не требует правок кода.
# URL для активной проверки прокси (лёгкий GET, проверяющий доступность прокси).
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", "https://httpbin.org/ip")
# Таймаут активной проверки (секунды).
HEALTH_CHECK_TIMEOUT = _get_int("HEALTH_CHECK_TIMEOUT", 10)
# Максимальное число последовательных сбоев, после которого прокси
# автоматически DISABLED на `HEALTH_DISABLE_DURATION_SECONDS`.
HEALTH_MAX_CONSECUTIVE_FAILURES = _get_int("HEALTH_MAX_CONSECUTIVE_FAILURES", 5)
# Число последовательных сбоев, после которого прокси переходит в статус
# UNHEALTHY (более серьёзная деградация, чем WARNING, но ещё не DISABLED).
# По умолчанию — половина от HEALTH_MAX_CONSECUTIVE_FAILURES, чтобы
# обеспечить промежуточную ступень предупреждения перед автоотключением.
HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES = _get_int(
    "HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES",
    max(1, HEALTH_MAX_CONSECUTIVE_FAILURES // 2),
)

# Минимальная допустимая доля успешных запросов (0.0–1.0). При падении ниже
# этого порога (и наличии хотя бы `HEALTH_MIN_REQUESTS_FOR_RATE` запросов
# для достоверности) статус прокси становится WARNING.
HEALTH_MIN_SUCCESS_RATE = float(os.getenv("HEALTH_MIN_SUCCESS_RATE", "0.5"))
# Минимальное количество запросов, необходимое для учёта порога success rate
# (при малой выборке порог не применяется во избежание ложно-негативных статусов).
HEALTH_MIN_REQUESTS_FOR_RATE = _get_int("HEALTH_MIN_REQUESTS_FOR_RATE", 10)
# Максимально допустимое среднее время ответа (миллисекунды). При превышении —
# WARNING. Применяется только при наличии хотя бы одного успешного запроса.
HEALTH_MAX_RESPONSE_TIME_MS = _get_int("HEALTH_MAX_RESPONSE_TIME_MS", 5000)
# Длительность отключения прокси при достижении порога последовательных
# сбоев (секунды). По истечении этого окна прокси автоматически
# перепроверяется и может вернуться в строй.
HEALTH_DISABLE_DURATION_SECONDS = _get_int("HEALTH_DISABLE_DURATION_SECONDS", 300)

# --- Sticky Sessions (app/sticky_sessions.py) ---
# Все параметры настраиваются через .env; смена любого значения не требует правок кода.
# Включает/выключает привязку прокси к логической сессии в Proxy Manager.
STICKY_SESSIONS_ENABLED = _get_bool("STICKY_SESSIONS_ENABLED", "1")
# Максимальная длительность привязки сессии к прокси (секунды). 0 — без ограничения по времени.
STICKY_SESSION_TIMEOUT_SECONDS = _get_int("STICKY_SESSION_TIMEOUT_SECONDS", 600)
# Максимальное количество запросов в рамках одной сессии. 0 — без ограничения.
STICKY_SESSION_MAX_REQUESTS = _get_int("STICKY_SESSION_MAX_REQUESTS", 100)
# Поведение при отказе привязанного прокси: "replace" — сессия продолжается
# с новым прокси при следующем запросе, "terminate" — сессия помечается
# терминированной (вызывающий код должен начать новую логическую сессию).
STICKY_SESSION_ON_FAILURE = os.getenv("STICKY_SESSION_ON_FAILURE", "replace").strip().lower()



# =====================================================================
# 3. МАСКИРОВКА И КЛИЕНТСКИЕ ДАННЫЕ
#    (используются и в headers для requests, и в контексте Playwright)
# =====================================================================

# Реалистичный дефолтный User-Agent, если не передан кастомный в headers.json
DEFAULT_USER_AGENT = os.getenv(
    "SCRAPER_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
)

# Локаль и часовой пояс браузерного контекста / заголовков запросов
BROWSER_LOCALE = os.getenv("BROWSER_LOCALE", "en-US")
BROWSER_TIMEZONE = os.getenv("BROWSER_TIMEZONE", "America/New_York")

# Размер окна браузера (viewport). Ранее было захардкожено внутри browser.py
BROWSER_VIEWPORT: Dict[str, int] = {
    "width": _get_int("BROWSER_VIEWPORT_WIDTH", 1920),
    "height": _get_int("BROWSER_VIEWPORT_HEIGHT", 1080),
}

# Флаги запуска Chromium, снижающие типовые признаки автоматизации.
# Централизованы здесь, чтобы не дублировать список в разных местах кода.
BROWSER_LAUNCH_ARGS: List[str] = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
]


# =====================================================================
# 3.1 ЗАГОЛОВКИ ЗАПРОСОВ (сырые дефолты для Request Profile Manager)
#     Эти значения — единственный источник правды для HTTP-заголовков.
#     Используются app/request_profile.py для сборки полного профиля
#     идентичности (Requests + Playwright).
# =====================================================================

DEFAULT_ACCEPT = os.getenv(
    "SCRAPER_ACCEPT",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
)
DEFAULT_ACCEPT_LANGUAGE = os.getenv("SCRAPER_ACCEPT_LANGUAGE", "en-US,en;q=0.9")
DEFAULT_ACCEPT_ENCODING = os.getenv("SCRAPER_ACCEPT_ENCODING", "gzip, deflate, br")
DEFAULT_CONNECTION = os.getenv("SCRAPER_CONNECTION", "keep-alive")
DEFAULT_UPGRADE_INSECURE_REQUESTS = os.getenv("SCRAPER_UPGRADE_INSECURE_REQUESTS", "1")
DEFAULT_SEC_FETCH_DEST = os.getenv("SCRAPER_SEC_FETCH_DEST", "document")
DEFAULT_SEC_FETCH_MODE = os.getenv("SCRAPER_SEC_FETCH_MODE", "navigate")
DEFAULT_SEC_FETCH_SITE = os.getenv("SCRAPER_SEC_FETCH_SITE", "none")
DEFAULT_DNT = os.getenv("SCRAPER_DNT", "1")



# =====================================================================
# 3.2 PLAYWRIGHT ENGINE (app/playwright_engine.py, app/browser.py)
#     Настройки движка браузерной автоматизации. Идентичность клиента
#     (User-Agent, viewport, locale, timezone) уже берется из Request
#     Profile Manager (см. раздел 3 выше) — здесь только специфичные
#     для Playwright параметры навигации, не дублирующие эти значения.
# =====================================================================

# Таймаут навигации/ожидания селекторов Playwright (миллисекунды).
# По умолчанию — общий TIMEOUT проекта (секунды), переведенный в мс,
# чтобы не дублировать еще одно значение по умолчанию.
PLAYWRIGHT_TIMEOUT_MS = _get_int("PLAYWRIGHT_TIMEOUT_MS", TIMEOUT * 1000)

# Условие, при котором навигация (`page.goto()`) считается завершенной:
# "load", "domcontentloaded", "networkidle" или "commit".
PLAYWRIGHT_WAIT_UNTIL = os.getenv("PLAYWRIGHT_WAIT_UNTIL", "load").strip().lower()


# =====================================================================
# 3.3 INFINITE SCROLL (app/infinite_scroll.py)
#     Настройки централизованного компонента бесконечного скроллинга.
#     Не хранит селекторы конкретных сайтов — только поведение скроллинга
#     и условия остановки, полностью настраиваемые через .env.
# =====================================================================

# Включает/выключает бесконечный скроллинг. Если выключен,
# `InfiniteScroll.scroll()` сразу возвращается без единой прокрутки.
INFINITE_SCROLL_ENABLED = _get_bool("INFINITE_SCROLL_ENABLED", "1")

# Максимальное количество итераций скроллинга. 0 — без ограничения
# (в этом случае должно быть настроено хотя бы одно другое условие
# остановки, иначе цикл может выполняться до timeout/no_new_content).
INFINITE_SCROLL_MAX_SCROLLS = _get_int("INFINITE_SCROLL_MAX_SCROLLS", 20)

# Общий таймаут цикла скроллинга (секунды). 0 — без ограничения.
INFINITE_SCROLL_TIMEOUT_SECONDS = float(os.getenv("INFINITE_SCROLL_TIMEOUT_SECONDS", "60"))

# Высота страницы (px), при достижении которой скроллинг останавливается.
# 0 — без ограничения по высоте.
INFINITE_SCROLL_MAX_PAGE_HEIGHT = _get_int("INFINITE_SCROLL_MAX_PAGE_HEIGHT", 0)

# Число последовательных прокруток без увеличения высоты страницы, после
# которого считается, что новый контент больше не подгружается.
INFINITE_SCROLL_MAX_NO_NEW_CONTENT = _get_int("INFINITE_SCROLL_MAX_NO_NEW_CONTENT", 3)

# Шаг прокрутки в пикселях. 0 — скроллить сразу к текущему низу страницы
# (`document.body.scrollHeight`) на каждой итерации.
INFINITE_SCROLL_STEP_PX = _get_int("INFINITE_SCROLL_STEP_PX", 0)

# Плавная (smooth) прокрутка вместо мгновенной.
INFINITE_SCROLL_SMOOTH = _get_bool("INFINITE_SCROLL_SMOOTH", "0")

# Ожидать состояние "networkidle" после каждого скролла — полезно для
# сайтов, подгружающих контент через задержанные XHR/fetch запросы.
INFINITE_SCROLL_WAIT_NETWORK_IDLE = _get_bool("INFINITE_SCROLL_WAIT_NETWORK_IDLE", "0")

# Политика паузы между итерациями скроллинга (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
INFINITE_SCROLL_DELAY_MODE = os.getenv("INFINITE_SCROLL_DELAY_MODE", "random").strip().lower()
INFINITE_SCROLL_DELAY_FIXED_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_FIXED_SECONDS", "1.0"))
INFINITE_SCROLL_DELAY_MIN_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MIN_SECONDS", "0.5"))
INFINITE_SCROLL_DELAY_MAX_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MAX_SECONDS", "1.5"))


# =====================================================================
# 3.4 PAGINATION (app/pagination.py)
#     Настройки централизованного компонента пагинации.
#     Не хранит селекторы конкретных сайтов — только стратегию
#     пагинации, лимиты и поведение, полностью настраиваемые через .env.
# =====================================================================

# Максимальное количество страниц. 0 — без ограничения.
PAGINATION_MAX_PAGES = _get_int("PAGINATION_MAX_PAGES", 0)

# Общий таймаут цикла пагинации (секунды). 0 — без ограничения.
PAGINATION_TIMEOUT_SECONDS = float(os.getenv("PAGINATION_TIMEOUT_SECONDS", "0"))

# Включает обнаружение дублирующихся страниц (по dedupe_key из fetch_callback).
PAGINATION_DUPLICATE_DETECTION = _get_bool("PAGINATION_DUPLICATE_DETECTION", "0")

# --- URL-пагинация ---
# Имя query-параметра для номера страницы (например, "page").
PAGINATION_PAGE_PARAM = os.getenv("PAGINATION_PAGE_PARAM", "page").strip().lower()
# Начальное значение счётчика страниц.
PAGINATION_START_PAGE = _get_int("PAGINATION_START_PAGE", 1)
# Шаг счётчика страниц.
PAGINATION_PAGE_STEP = _get_int("PAGINATION_PAGE_STEP", 1)

# --- Offset-пагинация ---
# Имя query-параметра для offset (например, "offset").
PAGINATION_OFFSET_PARAM = os.getenv("PAGINATION_OFFSET_PARAM", "offset").strip().lower()
# Начальное значение offset.
PAGINATION_START_OFFSET = _get_int("PAGINATION_START_OFFSET", 0)
# Шаг offset.
PAGINATION_OFFSET_STEP = _get_int("PAGINATION_OFFSET_STEP", 20)

# Политика паузы между страницами (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
PAGINATION_DELAY_MODE = os.getenv("PAGINATION_DELAY_MODE", "random").strip().lower()
PAGINATION_DELAY_FIXED_SECONDS = float(os.getenv("PAGINATION_DELAY_FIXED_SECONDS", "2.0"))
PAGINATION_DELAY_MIN_SECONDS = float(os.getenv("PAGINATION_DELAY_MIN_SECONDS", "1.0"))
PAGINATION_DELAY_MAX_SECONDS = float(os.getenv("PAGINATION_DELAY_MAX_SECONDS", "3.0"))


# =====================================================================
# 3.5 LOGIN SUPPORT (app/login_manager.py)
#     Настройки централизованного компонента аутентификации.
#     Не хранит учетные данные/URL/селекторы конкретных сайтов — только
#     лимиты, тайм-ауты и имена заголовков, полностью настраиваемые
#     через .env.
# =====================================================================

# Максимальное количество попыток логина (см. LoginManager.login()).
# Повтор пропускается автоматически при "окончательных" причинах сбоя
# (invalid_credentials, captcha_detected, missing_form) независимо от
# этого значения — см. _NON_RETRYABLE_REASONS в app/login_manager.py.
LOGIN_MAX_ATTEMPTS = _get_int("LOGIN_MAX_ATTEMPTS", 3)

# Тайм-аут одной попытки логина (секунды). В текущей реализации
# используется как рекомендованное значение для передачи в
# RequestsEngine/PlaywrightEngine вызывающим кодом (сами движки уже
# имеют собственный TIMEOUT/PLAYWRIGHT_TIMEOUT_MS — это отдельная,
# более узкая настройка именно для операции логина).
LOGIN_TIMEOUT_SECONDS = _get_int("LOGIN_TIMEOUT_SECONDS", TIMEOUT)

# Срок жизни аутентифицированной логической сессии (секунды) в памяти
# LoginManager (`ensure_login()` выполнит повторный логин по истечении).
# 0 — без ограничения по времени (сессия считается валидной, пока не
# инвалидирована явно через `LoginManager.invalidate_session()`).
LOGIN_SESSION_LIFETIME_SECONDS = _get_int("LOGIN_SESSION_LIFETIME_SECONDS", 1800)

# Сохранять ли куки после успешного логина через Cookie Manager
# (для восстановления сессии в будущих запусках через CookieSessionStrategy).
LOGIN_COOKIE_PERSISTENCE = _get_bool("LOGIN_COOKIE_PERSISTENCE", "1")

# Имя HTTP-заголовка для BearerTokenStrategy.
LOGIN_BEARER_HEADER_NAME = os.getenv("LOGIN_BEARER_HEADER_NAME", "Authorization")

# Имя HTTP-заголовка для ApiKeyStrategy.
LOGIN_API_KEY_HEADER_NAME = os.getenv("LOGIN_API_KEY_HEADER_NAME", "X-API-Key")

# Ключевые слова для обнаружения CAPTCHA в HTML (LoginDetector.contains_captcha()),
# через запятую, регистронезависимо.
LOGIN_CAPTCHA_KEYWORDS: List[str] = [
    keyword.strip().lower()
    for keyword in os.getenv("LOGIN_CAPTCHA_KEYWORDS", "captcha,recaptcha,hcaptcha,are you a robot").split(",")
    if keyword.strip()
]


# =====================================================================
# 3.6 HTML PARSER (app/html_parser.py)
#     Настройки централизованного слоя обработки HTML через BeautifulSoup.
#     Не хранит селекторы конкретных сайтов — только бэкенд-парсер,
#     полностью настраиваемый через .env.
# =====================================================================

# Парсер-бэкенд BeautifulSoup: "html.parser" (встроенный, без доп. зависимостей),
# "lxml" (быстрее, требует пакет lxml) или "html5lib" (максимально терпимый к
# невалидной разметке, требует пакет html5lib). По умолчанию — "html.parser",
# так как lxml/html5lib не входят в requirements.txt проекта по умолчанию.
HTML_PARSER_BACKEND = os.getenv("HTML_PARSER_BACKEND", "html.parser").strip().lower()


# =====================================================================
# 3.7 DATA VALIDATION (app/data_validator.py)
#     Настройки централизованного компонента валидации спарсенных
#     записей перед экспортом. Не хранит правила полей конкретного
#     сайта/заказа (это программный API `FieldRule`) — только поведение
#     встроенных type-валидаторов, полностью настраиваемое через .env.
# =====================================================================

# Включает обнаружение дублирующихся записей по умолчанию в
# `DataValidator.validate_records()` (можно переопределить явным
# аргументом `detect_duplicates` при вызове).
DATA_VALIDATION_DUPLICATE_DETECTION = _get_bool("DATA_VALIDATION_DUPLICATE_DETECTION", "0")

# Требовать ли обязательную схему (http:// или https://) для полей типа URL.
DATA_VALIDATION_URL_REQUIRE_SCHEME = _get_bool("DATA_VALIDATION_URL_REQUIRE_SCHEME", "1")

# Допустимый диапазон количества цифр для полей типа PHONE (после удаления
# всех нецифровых символов — пробелов, дефисов, скобок, кода страны "+").
DATA_VALIDATION_PHONE_MIN_DIGITS = _get_int("DATA_VALIDATION_PHONE_MIN_DIGITS", 7)
DATA_VALIDATION_PHONE_MAX_DIGITS = _get_int("DATA_VALIDATION_PHONE_MAX_DIGITS", 15)

# Список допустимых форматов даты (Python `strptime`), через запятую.
# Значение считается валидной датой, если совпадает хотя бы с одним форматом.
DATA_VALIDATION_DATE_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv("DATA_VALIDATION_DATE_FORMATS", "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%Y-%m-%dT%H:%M:%S").split(",")
    if fmt.strip()
]


# =====================================================================
# 3.8 DATA NORMALIZATION (app/data_normalizer.py)
#     Настройки централизованного слоя приведения спарсенных значений
#     к консистентному формату (числа, bool, даты, валюта, URL, страны).
#     Не хранит правила полей конкретного сайта/заказа (это программный
#     API `NormalizationRule`) — только словари/списки распознаваемых
#     значений и форматы вывода, полностью настраиваемые через .env.
# =====================================================================

# Текстовые представления, распознаваемые `DataNormalizer.normalize_bool()`
# как True/False (через запятую, регистронезависимо, сравнение по .lower()).
DATA_NORMALIZATION_BOOL_TRUE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_TRUE_VALUES",
        "true,1,yes,y,in stock,instock,available,да,есть,в наличии",
    ).split(",")
    if value.strip()
]
DATA_NORMALIZATION_BOOL_FALSE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_FALSE_VALUES",
        "false,0,no,n,out of stock,outofstock,unavailable,нет,отсутствует,нет в наличии",
    ).split(",")
    if value.strip()
]

# Список форматов даты (Python `strptime`), которые пробует
# `DataNormalizer.normalize_date()`/`normalize_timestamp()` по порядку,
# через запятую. Первый успешно разобранный формат используется.
DATA_NORMALIZATION_DATE_INPUT_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv(
        "DATA_NORMALIZATION_DATE_INPUT_FORMATS",
        "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%d/%m/%Y,%Y-%m-%dT%H:%M:%S,%B %d, %Y,%d %B %Y",
    ).split(",")
    if fmt.strip()
]

# Единый выходной формат даты для `DataNormalizer.normalize_date()`.
DATA_NORMALIZATION_DATE_OUTPUT_FORMAT = os.getenv("DATA_NORMALIZATION_DATE_OUTPUT_FORMAT", "%Y-%m-%d")

# Соответствия символ/название валюты -> ISO-код, для
# `DataNormalizer.normalize_currency()`. Формат: "символ:КОД", записи через
# запятую (например, "$:USD,€:EUR,₴:UAH"). Порядок важен только для
# читаемости — поиск в тексте выполняется по всем ключам.
DATA_NORMALIZATION_CURRENCY_SYMBOLS: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip().upper()
    for pair in os.getenv(
        "DATA_NORMALIZATION_CURRENCY_SYMBOLS",
        "$:USD,€:EUR,£:GBP,₴:UAH,₽:RUB,zł:PLN,грн:UAH,руб:RUB",
    ).split(",")
    if ":" in pair
}

# Схема по умолчанию, добавляемая `DataNormalizer.normalize_url()` к
# protocol-relative ("//example.com/...") и бесхема ("example.com/...") URL.
DATA_NORMALIZATION_URL_DEFAULT_SCHEME = os.getenv("DATA_NORMALIZATION_URL_DEFAULT_SCHEME", "https").strip().lower()

# Сохранять ли ведущий "+" (код страны) в `DataNormalizer.normalize_phone()`.
DATA_NORMALIZATION_PHONE_KEEP_PLUS = _get_bool("DATA_NORMALIZATION_PHONE_KEEP_PLUS", "1")

# Псевдонимы названий/кодов стран -> каноническое название, для
# `DataNormalizer.normalize_country()`. Формат: "псевдоним:Каноническое",
# записи через запятую (сравнение псевдонимов регистронезависимо).
DATA_NORMALIZATION_COUNTRY_ALIASES: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip()
    for pair in os.getenv(
        "DATA_NORMALIZATION_COUNTRY_ALIASES",
        "US:United States,USA:United States,U.S.:United States,U.S.A.:United States,"
        "UK:United Kingdom,U.K.:United Kingdom,GB:United Kingdom,"
        "UA:Ukraine,Ukraine:Ukraine,Украина:Ukraine,"
        "RU:Russia,Russian Federation:Russia,"
        "PL:Poland,Poland:Poland,"
        "DE:Germany,Germany:Germany",
    ).split(",")
    if ":" in pair
}


# =====================================================================
# 3.9 INCREMENTAL SAVING (app/exporter.py)
#     Настройки централизованного механизма прогрессивного сохранения
#     спарсенных записей во время скрапинга (вместо накопления всего
#     набора данных в памяти и экспорта единым вызовом в самом конце).
#     Не хранит формат/структуру записей конкретного сайта/заказа —
#     только поведение самого механизма записи, полностью настраиваемое
#     через .env.
# =====================================================================

# Включает/выключает Incremental Saving в `app/main.py`. При выключении
# сохраняется прежнее (batch) поведение: все записи копятся в памяти и
# экспортируются одним вызовом `save_to_csv`/`save_to_json` после
# завершения скрапинга — обратная совместимость с поведением до появления
# Incremental Saving.
EXPORT_INCREMENTAL_ENABLED = _get_bool("EXPORT_INCREMENTAL_ENABLED", "1")

# Принудительно сбрасывать буфер ОС на диск (`file.flush()` + `os.fsync()`)
# после каждой записи/пачки записей. Повышает устойчивость к потере данных
# при сбое (данные гарантированно физически на диске), но снижает
# производительность на очень больших объёмах — поэтому настраивается,
# а не хардкодится.
EXPORT_INCREMENTAL_FLUSH_ON_WRITE = _get_bool("EXPORT_INCREMENTAL_FLUSH_ON_WRITE", "1")


# =====================================================================
# 3.10 BATCH WRITER (app/exporter.py)
#      Настройки централизованного буферизующего слоя, оборачивающего
#      писатели Incremental Saving (IncrementalCSVWriter/JSONWriter).
#      Вместо записи на диск при каждом вызове write_records(), записи
#      копятся в памяти и сбрасываются пачками — уменьшая количество
#      операций записи на диск на больших объёмах данных. Не хранит
#      формат/структуру записей конкретного сайта/заказа — только
#      поведение самого буфера, полностью настраиваемое через .env.
# =====================================================================

# Максимальное количество записей, накапливаемых в буфере до
# автоматического сброса на диск (см. BatchWriter.add_records()).
BATCH_WRITER_BATCH_SIZE = _get_int("BATCH_WRITER_BATCH_SIZE", 100)

# Включает автоматический сброс буфера при достижении BATCH_WRITER_BATCH_SIZE.
# При выключении буфер растет неограниченно до явного вызова flush()/close() —
# использовать с осторожностью только под контролем вызывающего кода.
BATCH_WRITER_AUTO_FLUSH_ENABLED = _get_bool("BATCH_WRITER_AUTO_FLUSH_ENABLED", "1")

# Сбрасывать оставшиеся в буфере записи при завершении работы
# (BatchWriter.close() / выход из контекстного менеджера), чтобы
# ни одна накопленная запись не была потеряна при штатном завершении.
BATCH_WRITER_FLUSH_ON_SHUTDOWN = _get_bool("BATCH_WRITER_FLUSH_ON_SHUTDOWN", "1")


# =====================================================================
# 3.11 CHECKPOINT MANAGER (app/checkpoint_manager.py)
#      Настройки централизованного механизма периодического сохранения
#      прогресса скрапинга на диск (см. `tasks/TASK.md` и
#      `framework/ROADMAP.md`, Milestone 6). Checkpoint Manager только
#      ЗАПИСЫВАЕТ прогресс — он не восстанавливает и не продолжает
#      скрапинг (это будущий Resume Support, потребляющий сохраненные
#      здесь checkpoint-файлы). Не хранит логику конкретного
#      сайта/заказа — только поведение самого механизма чекпоинтинга,
#      полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает создание чекпоинтов. При выключении вызовы
# `CheckpointManager.record_page()`/`record_records()` становятся no-op —
# обратная совместимость с поведением до появления Checkpoint Manager.
CHECKPOINT_ENABLED = _get_bool("CHECKPOINT_ENABLED", "1")

# Путь к файлу чекпоинта. По умолчанию — рядом с cookies.json/proxy_cache.json
# в AI_INPUT_DIR, по аналогии с уже существующими персистентными файлами
# состояния (COOKIES_FILE, PROXY_CACHE_FILE).
CHECKPOINT_FILE = Path(os.getenv("CHECKPOINT_FILE_PATH", str(AI_INPUT_DIR / "checkpoint.json")))

# Создавать новый чекпоинт раз в N обработанных страниц. 0 — не учитывать
# количество страниц как условие сохранения.
CHECKPOINT_INTERVAL_PAGES = _get_int("CHECKPOINT_INTERVAL_PAGES", 1)

# Создавать новый чекпоинт раз в N обработанных записей. 0 — не учитывать
# количество записей как условие сохранения.
CHECKPOINT_INTERVAL_RECORDS = _get_int("CHECKPOINT_INTERVAL_RECORDS", 0)

# Создавать новый чекпоинт не чаще, чем раз в N секунд (даже если условия
# по страницам/записям сработали раньше — не даёт чекпоинтингу создавать
# избыточную нагрузку на диск при очень частых страницах/записях). 0 —
# не учитывать время как условие (полагаться только на pages/records).
CHECKPOINT_INTERVAL_SECONDS = float(os.getenv("CHECKPOINT_INTERVAL_SECONDS", "0"))

# Политика хранения файлов чекпоинта:
#   "overwrite"   — всегда перезаписывать один и тот же файл (CHECKPOINT_FILE);
#   "timestamped" — дополнительно сохранять с суффиксом-таймстампом,
#                   сохраняя историю чекпоинтов (полезно для отладки/аудита).
CHECKPOINT_OVERWRITE_POLICY = os.getenv("CHECKPOINT_OVERWRITE_POLICY", "overwrite").strip().lower()


# =====================================================================
# 3.12 RESUME SUPPORT (app/resume_manager.py)
#      Настройки централизованного механизма автоматического продолжения
#      прерванной сессии скрапинга на основе чекпоинтов, сохраненных
#      Checkpoint Manager'ом (см. `tasks/TASK.md` и `framework/ROADMAP.md`,
#      Milestone 6). Resume Support только ЧИТАЕТ и валидирует чекпоинты —
#      он не создает их сам (это ответственность Checkpoint Manager) и не
#      знает о логике конкретного сайта/заказа — только поведение самого
#      механизма восстановления, полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает автоматическое обнаружение и восстановление
# прерванной сессии при старте. При выключении сохраняется прежнее
# поведение: скрапинг всегда начинается "с нуля" — обратная
# совместимость с поведением до появления Resume Support.
RESUME_ENABLED = _get_bool("RESUME_ENABLED", "1")

# Максимальный "возраст" чекпоинта (в секундах), при котором он ещё
# считается пригодным для восстановления. 0 — не ограничивать возраст
# (восстанавливать независимо от давности последнего сохранения).
RESUME_MAX_AGE_SECONDS = _get_int("RESUME_MAX_AGE_SECONDS", 0)

# Резервируется для будущего интерактивного подтверждения перед
# восстановлением (см. TASK.md, "Future versions may optionally ask
# the user whether to resume or restart"). Пока не используется в коде —
# уже присутствует в конфигурации, чтобы включение такого режима в
# будущем не требовало правок app/config.py.
RESUME_CONFIRMATION_REQUIRED = _get_bool("RESUME_CONFIRMATION_REQUIRED", "0")


# =====================================================================
# 4. ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ПУТЕЙ

# =====================================================================



if __name__ == "__main__":
    print(f"[{__file__}] Проверка путей конфигурации:")
    print(f"  Корень проекта (ROOT_DIR): {ROOT_DIR}")
    print(f"  Папка вывода (OUTPUT_DIR): {OUTPUT_DIR}")
    print(f"  Файл кук (COOKIES_FILE):   {COOKIES_FILE}")
    print(f"  Тестовый HTML (PAGE_HTML_FILE): {PAGE_HTML_FILE}")
    print(f"  Режим Headless:            {HEADLESS}")
    print(f"  Запуск в Docker:           {IS_DOCKER}")
    print(f"  Таймаут:                   {TIMEOUT}s, Повторы: {RETRY_COUNT}")
    print(f"  Viewport:                  {BROWSER_VIEWPORT}")
    print(f"  Locale/Timezone:           {BROWSER_LOCALE} / {BROWSER_TIMEZONE}")
