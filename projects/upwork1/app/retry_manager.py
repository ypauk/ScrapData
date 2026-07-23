#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retry Manager.

Единый компонент, отвечающий за повторные попытки при временных сбоях
HTTP-операций (сетевые ошибки, таймауты, HTTP 429/500/502/503/504).

Retry Manager:

* строит настроенный `requests.adapters.HTTPAdapter` на базе `urllib3.Retry`
  для автоматических повторов транспортного уровня (используется Session
  Manager при монтировании адаптера на сессию);
* предоставляет `call_with_retry()` — универсальную обертку с экспоненциальным
  backoff и опциональным джиттером для повтора произвольных вызовов, которые
  выбрасывают "временные" исключения (например, до создания HTTP-сессии);
* берет всю политику повторов (лимит попыток, backoff, retryable-статусы)
  из Configuration Manager (`app/config.py`) — без хардкода значений.

Retry Manager НЕ выполняет скрапинг, НЕ управляет куками/прокси/User-Agent
и НЕ вводит намеренные задержки между обычными запросами — паузы существуют
исключительно как часть повторной попытки после сбоя (Delay Manager будет
отвечать за паузы между успешными запросами).
"""

import random
import time
from typing import Any, Callable, Iterable, Tuple, Type

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app import config

# Исключения, которые считаются временными и подлежат повтору в call_with_retry.
DEFAULT_RETRYABLE_EXCEPTIONS: Tuple[Type[BaseException], ...] = (
    ConnectionError,
    TimeoutError,
)


class RetryManager:
    """
    Централизованная политика повторов для HTTP-операций фреймворка.
    """

    @staticmethod
    def build_retry_adapter(
        total: int = None,
        backoff_factor: float = None,
        status_forcelist: Iterable[int] = None,
    ) -> HTTPAdapter:
        """
        Создает `HTTPAdapter`, настроенный политикой повторов `urllib3.Retry`.

        Адаптер монтируется на `requests.Session` (см. Session Manager) и
        прозрачно повторяет запросы при сетевых сбоях и указанных HTTP-статусах,
        без необходимости оборачивать каждый вызов `session.get(...)` вручную.

        Args:
            total (int, optional): Максимальное количество повторов.
                По умолчанию — `config.RETRY_COUNT`.
            backoff_factor (float, optional): Множитель экспоненциальной
                задержки. По умолчанию — `config.RETRY_BACKOFF_FACTOR`.
            status_forcelist (Iterable[int], optional): HTTP-статусы,
                считающиеся временным сбоем. По умолчанию —
                `config.RETRYABLE_STATUS_CODES`.

        Returns:
            HTTPAdapter: Адаптер, готовый к монтированию через
                `session.mount("http://", adapter)` / `mount("https://", adapter)`.
        """
        retry_policy = Retry(
            total=total if total is not None else config.RETRY_COUNT,
            backoff_factor=backoff_factor if backoff_factor is not None else config.RETRY_BACKOFF_FACTOR,
            status_forcelist=list(status_forcelist) if status_forcelist is not None else config.RETRYABLE_STATUS_CODES,
            allowed_methods=None,  # повторяем для всех методов, включая POST
            raise_on_status=False,
        )
        return HTTPAdapter(max_retries=retry_policy)

    @staticmethod
    def apply_to_session(session, **overrides: Any) -> None:
        """
        Монтирует настроенный retry-адаптер на все схемы (`http://`, `https://`)
        переданной сессии. Используется Session Manager при создании сессии.

        Args:
            session (requests.Session): Сессия, на которую монтируется адаптер.
            **overrides: Необязательные переопределения для `build_retry_adapter`
                (`total`, `backoff_factor`, `status_forcelist`).
        """
        adapter = RetryManager.build_retry_adapter(**overrides)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    @staticmethod
    def call_with_retry(
        func: Callable[[], Any],
        retries: int = None,
        backoff_factor: float = None,
        jitter: bool = None,
        retryable_exceptions: Tuple[Type[BaseException], ...] = DEFAULT_RETRYABLE_EXCEPTIONS,
    ) -> Any:
        """
        Выполняет `func()` с повторными попытками при временных сбоях, используя
        экспоненциальный backoff и опциональный джиттер.

        Полезно для операций, не проходящих через `requests.Session`
        (например, точечных вызовов, где адаптер не применим).

        Args:
            func (Callable[[], Any]): Вызываемый без аргументов callable
                (используйте `functools.partial` или lambda для передачи аргументов).
            retries (int, optional): Максимум повторов. По умолчанию — `config.RETRY_COUNT`.
            backoff_factor (float, optional): Множитель задержки.
                По умолчанию — `config.RETRY_BACKOFF_FACTOR`.
            jitter (bool, optional): Добавлять случайный джиттер к задержке.
                По умолчанию — `config.RETRY_JITTER`.
            retryable_exceptions (Tuple[Type[BaseException], ...]): Классы
                исключений, при которых выполняется повтор.

        Returns:
            Any: Результат успешного вызова `func()`.

        Raises:
            BaseException: Последнее пойманное исключение, если все попытки исчерпаны.
        """
        max_retries = retries if retries is not None else config.RETRY_COUNT
        factor = backoff_factor if backoff_factor is not None else config.RETRY_BACKOFF_FACTOR
        use_jitter = jitter if jitter is not None else config.RETRY_JITTER

        last_exception: BaseException = None
        for attempt in range(1, max_retries + 2):  # +1 — первая (не повторная) попытка
            try:
                return func()
            except retryable_exceptions as e:
                last_exception = e
                if attempt > max_retries:
                    break

                delay = factor * (2 ** (attempt - 1))
                if use_jitter:
                    delay += random.uniform(0, factor)

                print(
                    f"[{__file__}] Попытка {attempt}/{max_retries} не удалась ({e}). "
                    f"Повтор через {delay:.2f}с..."
                )
                time.sleep(delay)

        raise last_exception


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import requests

    session = requests.Session()
    RetryManager.apply_to_session(session)
    print(f"[{__file__}] Retry-адаптер смонтирован на сессию (лимит={config.RETRY_COUNT}, "
          f"статусы={config.RETRYABLE_STATUS_CODES})")

    counter = {"attempts": 0}

    def flaky_call():
        counter["attempts"] += 1
        if counter["attempts"] < 3:
            raise ConnectionError("Симуляция временного сбоя сети")
        return "OK"

    result = RetryManager.call_with_retry(flaky_call, retries=3, backoff_factor=0.1)
    print(f"[{__file__}] Результат call_with_retry: {result} (попыток: {counter['attempts']})")
