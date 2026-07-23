#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для Proxy Health Check (`app/health_check.py`).

Проверяют:
* пассивный мониторинг (record_success/record_failure);
* пересчет статусов (HEALTHY -> UNHEALTHY -> DISABLED);
* восстановление (Recovery) после успешного запроса и после истечения
  окна DISABLED;
* filter_healthy() (включая fallback, когда все прокси DISABLED);
* изоляцию статистики между разными прокси.

Используется unittest (без внешних зависимостей типа pytest), запуск:
    python -m unittest starter-project/tests/test_health_check.py
или из корня starter-project:
    python -m unittest tests.test_health_check
"""

import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app import config
from app.health_check import HealthCheck, HealthStatus


class HealthCheckTestCase(unittest.TestCase):
    """Базовый класс, обеспечивающий чистое состояние HealthCheck между тестами."""

    def setUp(self) -> None:
        HealthCheck.reset()
        self.proxy = "http://demo_user:demo_pass@10.0.0.1:8000"

    def tearDown(self) -> None:
        HealthCheck.reset()


class TestPassiveMonitoring(HealthCheckTestCase):
    """Проверка пассивного мониторинга: запись успехов/сбоев и базовые метрики."""

    def test_no_data_defaults_to_healthy(self):
        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.HEALTHY)
        self.assertTrue(HealthCheck.is_usable(self.proxy))
        self.assertIsNone(HealthCheck.get_stats(self.proxy))

    def test_record_success_updates_stats(self):
        HealthCheck.record_success(self.proxy, response_time_ms=100.0)
        HealthCheck.record_success(self.proxy, response_time_ms=200.0)

        stats = HealthCheck.get_stats(self.proxy)
        self.assertEqual(stats.total_requests, 2)
        self.assertEqual(stats.successful_requests, 2)
        self.assertEqual(stats.failed_requests, 0)
        self.assertEqual(stats.consecutive_failures, 0)
        self.assertAlmostEqual(stats.avg_response_time_ms, 150.0)
        self.assertEqual(stats.success_rate, 1.0)
        self.assertEqual(stats.status, HealthStatus.HEALTHY)

    def test_record_failure_updates_stats(self):
        HealthCheck.record_failure(self.proxy)
        HealthCheck.record_failure(self.proxy)

        stats = HealthCheck.get_stats(self.proxy)
        self.assertEqual(stats.total_requests, 2)
        self.assertEqual(stats.failed_requests, 2)
        self.assertEqual(stats.consecutive_failures, 2)

    def test_success_resets_consecutive_failures(self):
        HealthCheck.record_failure(self.proxy)
        HealthCheck.record_failure(self.proxy)
        self.assertEqual(HealthCheck.get_stats(self.proxy).consecutive_failures, 2)

        HealthCheck.record_success(self.proxy)
        self.assertEqual(HealthCheck.get_stats(self.proxy).consecutive_failures, 0)


class TestStatusTransitions(HealthCheckTestCase):
    """Проверка переходов между статусами по настраиваемым порогам."""

    def test_unhealthy_after_intermediate_failures(self):
        for _ in range(config.HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)

        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.UNHEALTHY)
        # UNHEALTHY все еще считается пригодным для использования
        self.assertTrue(HealthCheck.is_usable(self.proxy))

    def test_disabled_after_max_consecutive_failures(self):
        for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)

        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.DISABLED)
        self.assertFalse(HealthCheck.is_usable(self.proxy))

    def test_warning_on_low_success_rate_with_enough_samples(self):
        # Достаточно данных, но низкий success rate (без последовательных сбоев,
        # которые дали бы UNHEALTHY/DISABLED раньше).
        n = config.HEALTH_MIN_REQUESTS_FOR_RATE
        for _ in range(n):
            HealthCheck.record_success(self.proxy)
            HealthCheck.record_failure(self.proxy)
            HealthCheck.record_success(self.proxy)  # сбрасывает consecutive_failures

        stats = HealthCheck.get_stats(self.proxy)
        if stats.success_rate < config.HEALTH_MIN_SUCCESS_RATE:
            self.assertEqual(stats.status, HealthStatus.WARNING)

    def test_no_warning_with_insufficient_samples(self):
        # Один сбой — success_rate низкий, но выборка недостаточна для WARNING.
        HealthCheck.record_failure(self.proxy)
        stats = HealthCheck.get_stats(self.proxy)
        self.assertLess(stats.total_requests, config.HEALTH_MIN_REQUESTS_FOR_RATE)
        self.assertNotEqual(stats.status, HealthStatus.WARNING)

    def test_warning_on_slow_response_time(self):
        slow_ms = config.HEALTH_MAX_RESPONSE_TIME_MS + 1000
        HealthCheck.record_success(self.proxy, response_time_ms=slow_ms)
        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.WARNING)


class TestRecovery(HealthCheckTestCase):
    """Проверка автоматического восстановления (Recovery)."""

    def test_recovers_from_unhealthy_after_success(self):
        for _ in range(config.HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)
        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.UNHEALTHY)

        HealthCheck.record_success(self.proxy)
        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.HEALTHY)

    def test_recovers_from_disabled_after_window_expires(self):
        for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)
        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.DISABLED)

        stats = HealthCheck.get_stats(self.proxy)
        # Симулируем истечение окна отключения, не дожидаясь реального времени.
        stats.disabled_until = 0.0

        self.assertEqual(HealthCheck.get_status(self.proxy), HealthStatus.HEALTHY)
        self.assertTrue(HealthCheck.is_usable(self.proxy))
        self.assertEqual(stats.consecutive_failures, 0)


class TestFilterHealthy(HealthCheckTestCase):
    """Проверка фильтрации пула прокси перед Proxy Selection."""

    def test_filters_out_disabled_proxies(self):
        healthy_proxy = "http://1.1.1.1:1111"
        for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)

        pool = [healthy_proxy, self.proxy]
        filtered = HealthCheck.filter_healthy(pool)

        self.assertIn(healthy_proxy, filtered)
        self.assertNotIn(self.proxy, filtered)

    def test_fallback_when_all_disabled(self):
        for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
            HealthCheck.record_failure(self.proxy)

        pool = [self.proxy]
        filtered = HealthCheck.filter_healthy(pool)

        # Fallback: возвращаем исходный пул, чтобы не остановить фреймворк
        self.assertEqual(filtered, pool)

    def test_empty_pool_returns_empty(self):
        self.assertEqual(HealthCheck.filter_healthy([]), [])


class TestStatsIsolation(HealthCheckTestCase):
    """Проверка независимости статистики между разными прокси."""

    def test_stats_are_independent_per_proxy(self):
        proxy_a = "http://1.1.1.1:1111"
        proxy_b = "http://2.2.2.2:2222"

        HealthCheck.record_success(proxy_a)
        HealthCheck.record_failure(proxy_b)

        stats_a = HealthCheck.get_stats(proxy_a)
        stats_b = HealthCheck.get_stats(proxy_b)

        self.assertEqual(stats_a.successful_requests, 1)
        self.assertEqual(stats_a.failed_requests, 0)
        self.assertEqual(stats_b.successful_requests, 0)
        self.assertEqual(stats_b.failed_requests, 1)

    def test_reset_single_proxy_does_not_affect_others(self):
        proxy_a = "http://1.1.1.1:1111"
        proxy_b = "http://2.2.2.2:2222"

        HealthCheck.record_success(proxy_a)
        HealthCheck.record_success(proxy_b)

        HealthCheck.reset(proxy_a)

        self.assertIsNone(HealthCheck.get_stats(proxy_a))
        self.assertIsNotNone(HealthCheck.get_stats(proxy_b))


if __name__ == "__main__":
    unittest.main()
