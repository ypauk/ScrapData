#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sticky Sessions.

Централизованный компонент, отвечающий ТОЛЬКО за привязку одного прокси к
одной логической сессии (`session_id`), чтобы связанные запросы (один
скрапинг-джоб, одна сессия сайта, один авторизованный логин, одна сессия
браузера, одна сессия API) продолжали использовать один и тот же прокси.

Sticky Sessions:

* НЕ скачивает, НЕ валидирует и НЕ выбирает "лучший" прокси — выбор нового
  прокси для сессии всегда делегируется `ProxyManager` (который, в свою
  очередь, использует Proxy Selection/Proxy Rotation/Health Check);
* НЕ ротирует прокси самостоятельно — пока сессия активна и не истекла,
  прокси не меняется, независимо от активной политики Proxy Rotation;
* НЕ выполняет HTTP-запросы и НЕ содержит provider-specific логики;
* НЕ знает, откуда прокси взялся (Webshare/File Provider/Proxy Cache).

Интегрируется с:

* Configuration Manager (`app/config.py`) — вкл/выкл, тайм-аут сессии,
  лимит запросов на сессию и поведение при отказе прокси конфигурируются
  через `.env`, без правок кода;
* Proxy Manager (`app/proxy_manager.py`) — единственная точка входа,
  которая знает о Sticky Sessions. `ProxyManager.get_proxy(session_id=...)`
  сначала спрашивает `StickySessionManager.get_proxy()`, и только если
  привязки нет/она истекла — запрашивает новый прокси обычным способом
  (Proxy Rotation + Proxy Selection + Health Check) и привязывает его к
  сессии через `bind()`. Если `session_id` не передан — поведение Proxy
  Manager полностью прежнее (обратная совместимость);
* Proxy Health Check (`app/health_check.py`) — привязка считается
  истекшей, если прокси стал `DISABLED` (см. `_is_expired()`), а
  `ProxyManager.report_proxy_success()/report_proxy_failure()` с
  `session_id` обновляют пассивную статистику именно привязанного прокси;
* Proxy Rotation/Proxy Selection — косвенно: пока сессия активна, Sticky
  Sessions полностью перекрывает их вызов внутри `ProxyManager.get_proxy()`
  для данного `session_id`.

Состояние хранится в памяти (in-memory), без персистентности — аналогично
Proxy Selection/Rotation/Health Check, это осознанное упрощение для
текущей версии фреймворка (см. рекомендации в конце файла).
"""

import time
from dataclasses import dataclass
from typing import Dict, Optional, Set

from app import config


@dataclass
class StickySessionState:
    """Состояние одной привязки сессии к прокси."""

    proxy: str
    created_at: float
    last_used_at: float
    request_count: int = 0


class StickySessionManager:
    """
    Централизованная точка доступа к привязке прокси к логическим сессиям.

    Proxy Manager вызывает `get_proxy()`/`bind()` для получения/установки
    привязки, `report_failure()` — при сбое привязанного прокси, `release()`
    — при явном завершении сессии вызывающим кодом (Requests Engine,
    Playwright Engine, Login Support и т.д. — будущие компоненты).
    """

    _sessions: Dict[str, StickySessionState] = {}
    # Сессии, терминированные из-за отказа прокси при
    # `config.STICKY_SESSION_ON_FAILURE == "terminate"`. Хранится отдельно от
    # `_sessions`, чтобы вызывающий код мог отличить "сессии никогда не было"
    # от "сессия была явно закрыта из-за отказа" через `is_terminated()`.
    _terminated: Set[str] = set()

    @classmethod
    def is_enabled(cls) -> bool:
        """Включены ли Sticky Sessions согласно Configuration Manager."""
        return config.STICKY_SESSIONS_ENABLED

    @classmethod
    def _is_expired(cls, state: StickySessionState) -> bool:
        """
        Проверяет, истекла ли привязка сессии по любому из настраиваемых
        критериев (Session Expiration, см. TASK.md):

        * максимальная длительность сессии (`STICKY_SESSION_TIMEOUT_SECONDS`,
          0 — без ограничения по времени);
        * максимальное количество запросов
          (`STICKY_SESSION_MAX_REQUESTS`, 0 — без ограничения);
        * привязанный прокси стал непригоден для использования согласно
          Proxy Health Check (`HealthCheck.is_usable()` -> `False`, то есть
          прокси `DISABLED`) — это связывает Failure Handling с пассивным
          мониторингом здоровья без дублирования его логики здесь.
        """
        now = time.monotonic()

        if (
            config.STICKY_SESSION_TIMEOUT_SECONDS > 0
            and (now - state.created_at) >= config.STICKY_SESSION_TIMEOUT_SECONDS
        ):
            return True

        if (
            config.STICKY_SESSION_MAX_REQUESTS > 0
            and state.request_count >= config.STICKY_SESSION_MAX_REQUESTS
        ):
            return True

        from app.health_check import HealthCheck  # локальный импорт: избегаем циклической зависимости

        if not HealthCheck.is_usable(state.proxy):
            return True

        return False

    @classmethod
    def get_proxy(cls, session_id: str) -> Optional[str]:
        """
        Возвращает прокси, привязанный к сессии, если привязка существует
        и не истекла. Каждый вызов считается одним запросом в рамках
        сессии — увеличивает `request_count` и обновляет `last_used_at`.

        Если привязки нет или она истекла — истекшая привязка удаляется, и
        возвращается `None`. Вызывающий код (`ProxyManager.get_proxy()`)
        в этом случае должен запросить новый прокси обычным способом и
        вызвать `bind()`.

        Args:
            session_id (str): Идентификатор логической сессии.

        Returns:
            Optional[str]: Привязанный прокси, либо `None`.
        """
        state = cls._sessions.get(session_id)
        if state is None:
            return None

        if cls._is_expired(state):
            print(
                f"[{__file__}] Сессия '{session_id}' истекла "
                f"(запросов: {state.request_count}) — привязка снята."
            )
            cls._sessions.pop(session_id, None)
            return None

        state.request_count += 1
        state.last_used_at = time.monotonic()
        return state.proxy

    @classmethod
    def peek_proxy(cls, session_id: str) -> Optional[str]:
        """
        Возвращает привязанный прокси без побочных эффектов (не увеличивает
        `request_count`, не проверяет истечение). Используется Proxy
        Manager в `report_proxy_success()`/`report_proxy_failure()`, чтобы
        узнать, какой именно прокси обновлять в Health Check.

        Args:
            session_id (str): Идентификатор логической сессии.

        Returns:
            Optional[str]: Привязанный прокси, либо `None`, если привязки нет.
        """
        state = cls._sessions.get(session_id)
        return state.proxy if state is not None else None

    @classmethod
    def bind(cls, session_id: str, proxy: str) -> None:
        """
        Создает (или пересоздает) привязку сессии к прокси. Вызывается
        Proxy Manager сразу после того, как для сессии без активной
        привязки был выбран новый прокси обычным способом.

        Снимает возможную отметку "terminated" — новая привязка означает
        новый жизненный цикл сессии.

        Args:
            session_id (str): Идентификатор логической сессии.
            proxy (str): URL прокси для привязки.
        """
        now = time.monotonic()
        cls._sessions[session_id] = StickySessionState(
            proxy=proxy, created_at=now, last_used_at=now
        )
        cls._terminated.discard(session_id)

    @classmethod
    def release(cls, session_id: str, reason: str = "manual") -> None:
        """
        Явно завершает сессию и освобождает привязанный прокси
        (Explicit Session Termination).

        Args:
            session_id (str): Идентификатор логической сессии.
            reason (str): Причина завершения — попадает в лог
                (например, "manual", "job_finished").
        """
        state = cls._sessions.pop(session_id, None)
        if state is not None:
            print(f"[{__file__}] Сессия '{session_id}' завершена ({reason}).")

    @classmethod
    def report_failure(cls, session_id: str) -> None:
        """
        Реагирует на отказ прокси, привязанного к сессии (Failure Handling,
        см. TASK.md): освобождает текущую привязку и, в зависимости от
        `config.STICKY_SESSION_ON_FAILURE`, либо позволяет сессии
        продолжиться со свежим прокси при следующем вызове `get_proxy()`
        ("replace" — поведение по умолчанию), либо помечает сессию как
        терминированную ("terminate") — тогда вызывающий код должен начать
        новую логическую сессию (новый `session_id`).

        Сам метод не выбирает и не запрашивает новый прокси — это остается
        ответственностью Proxy Manager при следующем обращении с тем же
        `session_id`.

        Args:
            session_id (str): Идентификатор логической сессии, чей прокси отказал.
        """
        state = cls._sessions.pop(session_id, None)
        if state is None:
            return

        behavior = config.STICKY_SESSION_ON_FAILURE
        if behavior == "terminate":
            cls._terminated.add(session_id)
            print(
                f"[{__file__}] Сессия '{session_id}': прокси отказал — "
                f"сессия терминирована (STICKY_SESSION_ON_FAILURE=terminate)."
            )
        else:
            print(
                f"[{__file__}] Сессия '{session_id}': прокси отказал — "
                f"будет назначен новый прокси при следующем запросе "
                f"(STICKY_SESSION_ON_FAILURE=replace)."
            )

    @classmethod
    def is_terminated(cls, session_id: str) -> bool:
        """
        Была ли сессия терминирована из-за отказа прокси при
        `STICKY_SESSION_ON_FAILURE=terminate`.

        Позволяет будущему вызывающему коду (Requests Engine, Login
        Support) отличить "сессию нужно начать заново" от обычного
        отсутствия привязки.
        """
        return session_id in cls._terminated

    @classmethod
    def get_stats(cls, session_id: str) -> Optional[Dict[str, object]]:
        """Возвращает информацию о сессии для отладки/логирования, либо None."""
        state = cls._sessions.get(session_id)
        if state is None:
            return None
        return {
            "proxy": state.proxy,
            "created_at": state.created_at,
            "last_used_at": state.last_used_at,
            "request_count": state.request_count,
        }

    @classmethod
    def get_all_sessions(cls) -> Dict[str, StickySessionState]:
        """Возвращает все активные привязки (для отладки/логирования)."""
        return cls._sessions

    @classmethod
    def reset(cls, session_id: Optional[str] = None) -> None:
        """
        Сбрасывает состояние: для одной сессии (если указана) или полностью.

        Args:
            session_id (str, optional): Идентификатор сессии для сброса.
                Если `None`, сбрасывается всё (все привязки и отметки
                terminated).
        """
        if session_id is not None:
            cls._sessions.pop(session_id, None)
            cls._terminated.discard(session_id)
        else:
            cls._sessions.clear()
            cls._terminated.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    session = "job-42"


    print(f"[{__file__}] Sticky Sessions включены: {StickySessionManager.is_enabled()}")
    print(f"[{__file__}] get_proxy() без привязки: {StickySessionManager.get_proxy(session)}")

    StickySessionManager.bind(session, "http://demo_user:demo_pass@10.0.0.1:8000")
    print(f"[{__file__}] После bind(): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] Повторный вызов (тот же прокси): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] Статистика сессии: {StickySessionManager.get_stats(session)}")

    print(f"[{__file__}] Симулируем отказ прокси (behavior=replace по умолчанию)...")
    StickySessionManager.report_failure(session)
    print(f"[{__file__}] После отказа, get_proxy(): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] is_terminated(): {StickySessionManager.is_terminated(session)}")

    StickySessionManager.bind(session, "http://2.2.2.2:2222")
    StickySessionManager.release(session, reason="job_finished")
    print(f"[{__file__}] После release(): {StickySessionManager.get_proxy(session)}")

    StickySessionManager.reset()
