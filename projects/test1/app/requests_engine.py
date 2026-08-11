#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Requests Engine.

Централизованный HTTP-исполнительный слой фреймворка для всех
не-браузерных задач скрапинга (см. `framework/ROADMAP.md`, Milestone 4).

Requests Engine — единственная точка, через которую скрапер-модули должны
выполнять HTTP GET/POST запросы. Он НЕ содержит собственной логики
куки/повторов/задержек/прокси — вся эта логика уже инкапсулирована в
существующих менеджерах и автоматически применяется через Session Manager
(`app/session_manager.py`), который остается единственным компонентом,
координирующим Cookie/Retry/Delay/Proxy Manager вокруг `requests.Session`.

Архитектура (см. `app/session_manager.py` для полной схемы HTTP-слоя):

    Requests Engine
            │
            ▼
    Session Manager  ──────────────────────────────┐
            │                                       │
     ┌──────┼────────┬────────┐                     │
     ▼      ▼         ▼        ▼                     ▼
    Cookie  Retry    Delay    Proxy            Configuration
    Manager Manager  Manager  Manager               Manager

Requests Engine:

* создает (через `SessionManager.create_session()`) и хранит одну
  `requests.Session` на инстанс — это обеспечивает переиспользование
  TCP-соединений (keep-alive) и куки между вызовами одного скрапинг-джоба,
  при этом сама сессия уже полностью настроена (профиль идентичности,
  куки, retry-адаптер, прокси) без единой строчки дополнительного кода;
* делает паузу перед каждым запросом через
  `SessionManager.wait_before_request()` (Delay Manager) — вызывающий код
  не должен думать о задержках между запросами;
* НЕ реализует собственный цикл повторов — повторы транспортного уровня
  (сетевые сбои, HTTP 429/500/502/503/504) уже покрыты retry-адаптером,
  смонтированным Session Manager через Retry Manager
  (`RetryManager.apply_to_session()`), поэтому добавление еще одного слоя
  повторов здесь привело бы к дублированию логики и непредсказуемому
  умножению количества попыток — что запрещено `framework/AI_RULES.md`
  (DRY, avoid overengineering);
* сообщает Proxy Manager об успехе/сбое каждого запроса
  (`ProxyManager.report_proxy_success()`/`report_proxy_failure()`), что
  прозрачно питает Proxy Health Check и Proxy Rotation/Sticky Sessions,
  если движку передан `session_id`;
* оборачивает все ожидаемые сетевые сбои (таймаут, соединение, DNS, SSL),
  оставшиеся после исчерпания повторов Retry Manager, в единое понятное
  исключение `RequestsEngineError` — вызывающему коду не нужно знать о
  внутренних исключениях `requests`;
* возвращает "сырой" `requests.Response` из `get()`/`post()`/`request()`
  (по требованию задачи), а также предоставляет удобные шорткаты
  `get_json()`/`post_json()`/`get_text()` и `download_file()` для
  скачивания бинарного содержимого — без парсинга HTML/JSON в бизнес-объекты
  (это ответственность будущего Parsing-слоя, Milestone 5).

Requests Engine НЕ парсит HTML, НЕ парсит JSON в бизнес-объекты, НЕ
экспортирует данные, ничего не знает о BeautifulSoup или Playwright.
"""

import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests

from app import config
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile
from app.session_manager import SessionManager

# Размер буфера чтения при потоковом скачивании файлов (байт). Стандартное
# для requests значение — используется как единственная точка правды,
# чтобы не хардкодить "магическое число" в нескольких местах.
DEFAULT_DOWNLOAD_CHUNK_SIZE = 8192

# HTTP-статус, начиная с которого ответ считается серверной ошибкой.
_HTTP_SERVER_ERROR_THRESHOLD = 500
# HTTP-статус, начиная с которого ответ считается клиентской/серверной
# ошибкой (используется только для логирования уровня warning).
_HTTP_CLIENT_ERROR_THRESHOLD = 400

# Исключения `requests`, которые считаются "ожидаемыми" сетевыми сбоями
# (таймаут, соединение, DNS-резолвинг, SSL, слишком много редиректов) и
# оборачиваются в `RequestsEngineError` вместо падения с трассировкой
# внутренностей `requests`/`urllib3`.
_HANDLED_REQUEST_EXCEPTIONS = (
    requests.exceptions.ConnectionError,  # покрывает также DNS-сбои и SSLError (см. requests.exceptions)
    requests.exceptions.Timeout,
    requests.exceptions.TooManyRedirects,
)


class RequestsEngineError(Exception):
    """
    Единое исключение Requests Engine для всех сбоев HTTP-запроса,
    оставшихся после исчерпания повторов Retry Manager.

    Позволяет вызывающему коду (будущим скрапер-модулям) обрабатывать
    ошибки сети без необходимости импортировать и знать про исключения
    `requests`/`urllib3`.
    """


class RequestsEngine:
    """
    Централизованный исполнитель HTTP-запросов для скрапинга без браузера.

    Каждый инстанс хранит одну настроенную `requests.Session`, что позволяет
    переиспользовать соединения и куки между запросами одного логического
    джоба. Все компоненты HTTP-слоя (Configuration/Request Profile/Session/
    Cookie/Retry/Delay/Proxy Manager) подключаются автоматически — вызывающий
    код не настраивает их вручную.
    """

    def __init__(
        self,
        profile: Optional[RequestProfile] = None,
        session_id: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        """
        Args:
            profile (RequestProfile, optional): Профиль идентичности для
                новой сессии. Игнорируется, если передан готовый `session`.
                По умолчанию — профиль из `RequestProfileManager.default_profile()`
                (применяется внутри `SessionManager.create_session()`).
            session_id (str, optional): Идентификатор логической сессии для
                Sticky Sessions/Proxy Rotation/Health Check
                (см. `ProxyManager.get_proxy(session_id=...)`). Если не
                передан — прокси выбирается без привязки к сессии
                (обратная совместимость, поведение как раньше).
            session (requests.Session, optional): Готовая сессия для
                переиспользования (например, между несколькими движками).
                Если не передана, создается новая через
                `SessionManager.create_session()`.
        """
        self.session_id = session_id
        self.session: requests.Session = session or SessionManager.create_session(profile=profile)
        # Максимальная длина цепочки редиректов централизована в Configuration Manager.
        self.session.max_redirects = config.REQUESTS_MAX_REDIRECTS

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        allow_redirects: Optional[bool] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Выполняет один HTTP-запрос через настроенную сессию.

        Перед запросом выполняется пауза согласно Delay Manager
        (`SessionManager.wait_before_request()`). Повторы при временных
        сбоях выполняются прозрачно retry-адаптером, смонтированным Session
        Manager через Retry Manager — эта функция не реализует собственный
        цикл повторов.

        Args:
            method (str): HTTP-метод ("GET", "POST" и т.д.).
            url (str): Целевой URL.
            params (dict, optional): Query-параметры.
            data (dict | str | bytes, optional): Тело запроса
                (form-encoded, если передан словарь).
            json (Any, optional): Тело запроса, сериализуемое в JSON
                (устанавливает `Content-Type: application/json`).
            headers (dict, optional): Дополнительные заголовки,
                дополняющие (и переопределяющие при совпадении имени)
                заголовки профиля идентичности сессии.
            files (dict, optional): Файлы для multipart-запроса
                (например, `{"file": open(path, "rb")}`).
            timeout (float, optional): Таймаут запроса (секунды).
                По умолчанию — `SessionManager.timeout` (Configuration Manager).
            allow_redirects (bool, optional): Следовать ли редиректам.
                По умолчанию — `config.REQUESTS_ALLOW_REDIRECTS`.
            stream (bool): Не загружать содержимое ответа немедленно
                (используется `download_file()` для потокового скачивания).
            **kwargs: Дополнительные именованные аргументы, передаваемые
                напрямую в `requests.Session.request()`.

        Returns:
            requests.Response: "Сырой" объект ответа.

        Raises:
            RequestsEngineError: При сетевом сбое (таймаут, соединение,
                DNS, SSL, слишком много редиректов), оставшемся после
                исчерпания повторов Retry Manager.
        """
        SessionManager.wait_before_request()

        effective_timeout = timeout if timeout is not None else SessionManager.timeout
        effective_redirects = (
            allow_redirects if allow_redirects is not None else config.REQUESTS_ALLOW_REDIRECTS
        )

        start = time.monotonic()
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                files=files,
                timeout=effective_timeout,
                allow_redirects=effective_redirects,
                verify=config.REQUESTS_VERIFY_SSL,
                stream=stream,
                **kwargs,
            )
        except _HANDLED_REQUEST_EXCEPTIONS as exc:
            print(f"[{__file__}] Сбой запроса {method} {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise RequestsEngineError(f"{method} {url} завершился ошибкой: {exc}") from exc

        elapsed_ms = (time.monotonic() - start) * 1000.0

        if response.status_code >= _HTTP_SERVER_ERROR_THRESHOLD:
            print(f"[{__file__}] Предупреждение: HTTP {response.status_code} для {method} {url}")
            # Серверная ошибка (после исчерпания повторов Retry Manager) —
            # сигнализируем Proxy Manager как сбой, чтобы Health Check/Rotation
            # учли деградацию именно этого прокси.
            ProxyManager.report_proxy_failure(session_id=self.session_id)
        else:
            if response.status_code >= _HTTP_CLIENT_ERROR_THRESHOLD:
                print(f"[{__file__}] Предупреждение: HTTP {response.status_code} для {method} {url}")
            # Соединение через прокси отработало (даже если сайт вернул 4xx) —
            # это успех с точки зрения Proxy Health Check.
            ProxyManager.report_proxy_success(response_time_ms=elapsed_ms, session_id=self.session_id)

        return response

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Выполняет HTTP GET-запрос. См. `request()` для описания аргументов."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        """Выполняет HTTP POST-запрос. См. `request()` для описания аргументов."""
        return self.request("POST", url, **kwargs)

    def get_text(self, url: str, **kwargs: Any) -> str:
        """Выполняет GET и возвращает тело ответа как декодированный текст."""
        return self.get(url, **kwargs).text

    def get_json(self, url: str, **kwargs: Any) -> Optional[Any]:
        """
        Выполняет GET и декодирует тело ответа как JSON.

        Returns:
            Optional[Any]: Декодированный JSON, либо `None`, если ответ
                не является валидным JSON (невалидный ответ обрабатывается
                гарантированно, без падения вызывающего кода).
        """
        return self._safe_json(self.get(url, **kwargs))

    def post_json(self, url: str, **kwargs: Any) -> Optional[Any]:
        """Выполняет POST и декодирует тело ответа как JSON. См. `get_json()`."""
        return self._safe_json(self.post(url, **kwargs))

    @staticmethod
    def _safe_json(response: requests.Response) -> Optional[Any]:
        """Декодирует JSON из ответа, гарантированно обрабатывая невалидный формат."""
        try:
            return response.json()
        except ValueError as exc:
            print(f"[{__file__}] Предупреждение: невалидный JSON в ответе {response.url}: {exc}")
            return None

    def download_file(
        self,
        url: str,
        destination: Union[str, Path],
        chunk_size: int = DEFAULT_DOWNLOAD_CHUNK_SIZE,
        **kwargs: Any,
    ) -> Path:
        """
        Скачивает бинарное содержимое по URL и сохраняет его в файл,
        не загружая весь ответ в память сразу (потоковое чтение).

        Args:
            url (str): URL файла для скачивания.
            destination (str | Path): Путь для сохранения файла.
                Родительские директории создаются автоматически.
            chunk_size (int): Размер буфера чтения в байтах.
                По умолчанию — `DEFAULT_DOWNLOAD_CHUNK_SIZE`.
            **kwargs: Дополнительные аргументы, передаваемые в `get()`
                (например, `headers`, `params`).

        Returns:
            Path: Путь к сохраненному файлу.

        Raises:
            RequestsEngineError: При сетевом сбое во время скачивания.
        """
        destination_path = Path(destination)
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        kwargs.pop("stream", None)  # stream=True принудительно для скачивания файлов
        response = self.get(url, stream=True, **kwargs)

        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        print(f"[{__file__}] Файл сохранен: {destination_path} ({url})")
        return destination_path

    def close(self) -> None:
        """Закрывает внутреннюю HTTP-сессию (освобождает соединения)."""
        self.session.close()

    def __enter__(self) -> "RequestsEngine":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# =====================================================================
# Модульные шорткаты на общем движке по умолчанию — удобны для простых
# скриптов, где не требуется явное управление сессией/session_id
# (аналогично `get_default_profile()` в app/request_profile.py).
# =====================================================================

_default_engine: Optional[RequestsEngine] = None


def get_default_engine() -> RequestsEngine:
    """Возвращает общий (ленивая инициализация) движок по умолчанию."""
    global _default_engine
    if _default_engine is None:
        _default_engine = RequestsEngine()
    return _default_engine


def get(url: str, **kwargs: Any) -> requests.Response:
    """Шорткат: GET-запрос через движок по умолчанию."""
    return get_default_engine().get(url, **kwargs)


def post(url: str, **kwargs: Any) -> requests.Response:
    """Шорткат: POST-запрос через движок по умолчанию."""
    return get_default_engine().post(url, **kwargs)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    engine = RequestsEngine()
    print(f"[{__file__}] Тестовый GET-запрос...")
    try:
        resp = engine.get("https://httpbin.org/get")
        print(f"[{__file__}] Статус: {resp.status_code}")
        print(f"[{__file__}] JSON: {engine.get_json('https://httpbin.org/get')}")
    except RequestsEngineError as e:
        print(f"[{__file__}] Ошибка запроса (ожидаемо без интернета в CI): {e}")
    finally:
        engine.close()
