#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для Sticky Sessions (`app/sticky_sessions.py`) и его интеграции с
Proxy Manager (`app/proxy_manager.py`, `session_id` параметр).

Проверяют:
* базовую привязку/переиспользование прокси в рамках одной сессии;
* независимость привязок разных сессий друг от друга;
* Session Expiration: тайм-аут по времени, лимит запросов, отказ
  прокси (Health Check DISABLED);
* явное завершение сессии (release);
* Failure Handling: поведение "replace" и "terminate";
* обратную совместимость `ProxyManager.get_proxy()` без `session_id`;
* интеграцию `ProxyManager.get_proxy(session_id=...)` с пулом провайдера.

Запуск:
    python -m unittest tests.test_sticky_sessions
(из директории starter-project)
"""

import sys
import unittest
from pathlib import Path
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app import config
from app.health_check import HealthCheck
from app.proxy_manager import EnvProxyProvider, ProxyManager, ProxyProvider
from app.sticky_sessions import StickySessionManager


class StickySessionTestCase(unittest.TestCase):
    """Базовый класс: чистое состояние Sticky Sessions/Health Check между тестами."""

    def setUp(self) -> None:
        StickySessionManager.reset()
        HealthCheck.reset()

        # Сохраняем оригинальные значения конфигурации, чтобы тесты могли
        # временно их переопределять без побочных эффектов на другие тесты.
        self._orig_enabled = config.STICKY_SESSIONS_ENABLED
        self._orig_timeout = config.STICKY_SESSION_TIMEOUT_SECONDS
        self._orig_max_requests = config.STICKY_SESSION_MAX_REQUESTS
        self._orig_on_failure = config.STICKY_SESSION_ON_FAILURE

        config.STICKY_SESSIONS_ENABLED = True
        config.STICKY_SESSION_TIMEOUT_SECONDS = 0  # без ограничения по умолчанию в тестах
        config.STICKY_SESSION_MAX_REQUESTS = 0  # без ограничения по умолчанию в тестах
        config.STICKY_SESSION_ON_FAILURE = "replace"

    def tearDown(self) -> None:
        StickySessionManager.reset()
        HealthCheck.reset()
        config.STICKY_SESSIONS_ENABLED = self._orig_enabled
        config.STICKY_SESSION_TIMEOUT_SECONDS = self._orig_timeout
        config.STICKY_SESSION_MAX_REQUESTS = self._orig_max_requests
        config.STICKY_SESSION_ON_FAILURE = self._orig_on_failure


class TestBasicBinding(StickySessionTestCase):
    """Проверка базовой привязки и переиспользования прокси в рамках сессии."""

    def test_no_binding_returns_none(self):
        self.assertIsNone(StickySessionManager.get_proxy("job-1"))

    def test_bind_and_reuse(self):
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")
        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")
        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")

    def test_get_proxy_increments_request_count(self):
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        StickySessionManager.get_proxy("job-1")
        StickySessionManager.get_proxy("job-1")
        stats = StickySessionManager.get_stats("job-1")
        self.assertEqual(stats["request_count"], 2)

    def test_peek_proxy_does_not_increment(self):
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        StickySessionManager.peek_proxy("job-1")
        StickySessionManager.peek_proxy("job-1")
        stats = StickySessionManager.get_stats("job-1")
        self.assertEqual(stats["request_count"], 0)

    def test_sessions_are_independent(self):
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        StickySessionManager.bind("job-2", "http://2.2.2.2:2222")

        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")
        self.assertEqual(StickySessionManager.get_proxy("job-2"), "http://2.2.2.2:2222")


class TestExplicitRelease(StickySessionTestCase):
    """Проверка явного завершения сессии."""

    def test_release_removes_binding(self):
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        StickySessionManager.release("job-1", reason="job_finished")
        self.assertIsNone(StickySessionManager.get_proxy("job-1"))

    def test_release_unknown_session_is_noop(self):
        # Не должно бросать исключение
        StickySessionManager.release("unknown-session")


class TestExpiration(StickySessionTestCase):
    """Проверка Session Expiration (тайм-аут, лимит запросов, отказ прокси)."""

    def test_expires_after_max_requests(self):
        config.STICKY_SESSION_MAX_REQUESTS = 2
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")

        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")  # 1-й запрос
        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")  # 2-й запрос, лимит достигнут

        # Привязка должна быть снята при следующем обращении
        self.assertIsNone(StickySessionManager.get_proxy("job-1"))

    def test_expires_after_timeout(self):
        config.STICKY_SESSION_TIMEOUT_SECONDS = 5
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")

        state = StickySessionManager.get_all_sessions()["job-1"]
        # Симулируем истечение тайм-аута, не дожидаясь реального времени.
        state.created_at -= 10

        self.assertIsNone(StickySessionManager.get_proxy("job-1"))

    def test_expires_when_proxy_becomes_disabled(self):
        proxy = "http://1.1.1.1:1111"
        StickySessionManager.bind("job-1", proxy)

        for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(proxy)

        self.assertFalse(HealthCheck.is_usable(proxy))
        self.assertIsNone(StickySessionManager.get_proxy("job-1"))

    def test_no_expiration_when_limits_are_zero(self):
        config.STICKY_SESSION_TIMEOUT_SECONDS = 0
        config.STICKY_SESSION_MAX_REQUESTS = 0
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")

        for _ in range(50):
            self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://1.1.1.1:1111")


class TestFailureHandling(StickySessionTestCase):
    """Проверка Failure Handling: политики 'replace' и 'terminate'."""

    def test_replace_allows_new_binding(self):
        config.STICKY_SESSION_ON_FAILURE = "replace"
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")

        StickySessionManager.report_failure("job-1")

        self.assertIsNone(StickySessionManager.get_proxy("job-1"))
        self.assertFalse(StickySessionManager.is_terminated("job-1"))

        # Новая привязка разрешена
        StickySessionManager.bind("job-1", "http://2.2.2.2:2222")
        self.assertEqual(StickySessionManager.get_proxy("job-1"), "http://2.2.2.2:2222")

    def test_terminate_marks_session(self):
        config.STICKY_SESSION_ON_FAILURE = "terminate"
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")

        StickySessionManager.report_failure("job-1")

        self.assertIsNone(StickySessionManager.get_proxy("job-1"))
        self.assertTrue(StickySessionManager.is_terminated("job-1"))

    def test_bind_after_terminate_clears_flag(self):
        config.STICKY_SESSION_ON_FAILURE = "terminate"
        StickySessionManager.bind("job-1", "http://1.1.1.1:1111")
        StickySessionManager.report_failure("job-1")
        self.assertTrue(StickySessionManager.is_terminated("job-1"))

        StickySessionManager.bind("job-1", "http://2.2.2.2:2222")
        self.assertFalse(StickySessionManager.is_terminated("job-1"))

    def test_report_failure_on_unknown_session_is_noop(self):
        # Не должно бросать исключение
        StickySessionManager.report_failure("unknown-session")


class PoolProvider(ProxyProvider):
    """Тестовый провайдер с пулом прокси для проверки интеграции с Proxy Manager."""

    def __init__(self, proxies: Optional[List[str]] = None):
        self._proxies = proxies or ["http://1.1.1.1:1111", "http://2.2.2.2:2222", "http://3.3.3.3:3333"]

    def get_proxy(self) -> Optional[str]:
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        return self._proxies


class TestProxyManagerIntegration(StickySessionTestCase):
    """Проверка интеграции Sticky Sessions с Proxy Manager (session_id) и обратной совместимости."""

    def setUp(self) -> None:
        super().setUp()
        self._orig_provider = ProxyManager.get_provider()

    def tearDown(self) -> None:
        ProxyManager.set_provider(self._orig_provider)
        super().tearDown()

    def test_backward_compatible_without_session_id(self):
        # Без session_id поведение должно быть прежним — не использует Sticky Sessions.
        ProxyManager.set_provider(EnvProxyProvider())
        # EnvProxyProvider без config.PROXY_URL обычно возвращает None,
        # главное — что вызов не требует session_id и не бросает исключений.
        result = ProxyManager.get_proxy()
        self.assertTrue(result is None or isinstance(result, str))

    def test_same_session_id_reuses_proxy_from_pool(self):
        ProxyManager.set_provider(PoolProvider())

        first = ProxyManager.get_proxy(session_id="job-1")
        second = ProxyManager.get_proxy(session_id="job-1")
        third = ProxyManager.get_proxy(session_id="job-1")

        self.assertIsNotNone(first)
        self.assertEqual(first, second)
        self.assertEqual(second, third)

    def test_different_session_ids_are_independent(self):
        ProxyManager.set_provider(PoolProvider(["http://1.1.1.1:1111"]))

        proxy_a = ProxyManager.get_proxy(session_id="job-a")
        proxy_b = ProxyManager.get_proxy(session_id="job-b")

        # Оба session_id получают прокси независимо от общего _current_proxy
        self.assertIsNotNone(proxy_a)
        self.assertIsNotNone(proxy_b)

    def test_report_failure_and_success_with_session_id(self):
        ProxyManager.set_provider(PoolProvider())
        proxy = ProxyManager.get_proxy(session_id="job-1")
        self.assertIsNotNone(proxy)

        # Не должно бросать исключений
        ProxyManager.report_proxy_success(response_time_ms=123.0, session_id="job-1")
        stats = HealthCheck.get_stats(proxy)
        self.assertIsNotNone(stats)
        self.assertEqual(stats.successful_requests, 1)

        ProxyManager.report_proxy_failure(session_id="job-1")
        stats = HealthCheck.get_stats(proxy)
        self.assertEqual(stats.failed_requests, 1)

    def test_sticky_sessions_disabled_falls_back_to_normal_flow(self):
        config.STICKY_SESSIONS_ENABLED = False
        ProxyManager.set_provider(PoolProvider())

        proxy1 = ProxyManager.get_proxy(session_id="job-1")
        proxy2 = ProxyManager.get_proxy(session_id="job-1")

        # При выключенных Sticky Sessions привязка не создается вообще
        self.assertIsNone(StickySessionManager.get_stats("job-1"))
        self.assertIsNotNone(proxy1)
        self.assertIsNotNone(proxy2)


if __name__ == "__main__":
    unittest.main()
