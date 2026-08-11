#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Health Check.

Централизованный компонент, отвечающий ТОЛЬКО за мониторинг доступности и
качества прокси. Он собирает и поддерживает метрики для каждого прокси
(успехи/сбои/время ответа/статус), но НЕ выбирает, какой прокси использовать
(это Proxy Selection), и НЕ решает, когда менять (это Proxy Rotation).

Proxy Health Check:

* НЕ скачивает прокси;
* НЕ выбирает прокси;
* НЕ ротирует прокси;
* НЕ содержит provider-specific логики;
* НЕ выполняет логику скрапинга (единственный HTTP-запрос — легковесная
  активная проверка `check_proxy()` на настраиваемый тестовый URL).

Интегрируется с:
* Configuration Manager (`app/config.py`) — все пороги конфигурируются
  через `.env`, смена порогов не требует правок кода;
* Proxy Manager (`app/proxy_manager.py`) — пассивный мониторинг через
  `record_success()`/`record_failure()`, фильтрация пула через
  `filter_healthy()`, активная проверка доступна через `check_proxy()`;
* Proxy Selection — косвенно, только в том смысле, что Health Check
  фильтрует пул ДО передачи в `ProxySelector.select()`, но сам не
  выбирает конкретный прокси;
* Proxy Rotation — косвенно, через общий `ProxyManager.report_proxy_failure()`
  hook.

Метрики и состояния хранятся в памяти (in-memory), без персистентности —
аналогично Proxy Selection и Proxy Rotation, это осознанное упрощение
для текущей версии фреймворка.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

from app import config


class HealthStatus(str, Enum):
    """Статус здоровья прокси."""

    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"


@dataclass
class ProxyStats:
    """Метрики одного прокси."""

    proxy: str

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0

    _total_response_time_ms: float = 0.0  # накопительная сумма для вычисления среднего

    last_success_at: Optional[float] = None
    last_failure_at: Optional[float] = None
    status: HealthStatus = HealthStatus.HEALTHY
    disabled_until: Optional[float] = None

    @property
    def success_rate(self) -> float:
        """Доля успешных запросов от общего числа (0.0–1.0)."""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def avg_response_time_ms(self) -> float:
        """Среднее время ответа в миллисекундах."""
        if self.successful_requests == 0:
            return 0.0
        return self._total_response_time_ms / self.successful_requests

    def record_success(self, response_time_ms: Optional[float] = None) -> None:
        """Записывает успешный запрос с этим прокси."""
        self.total_requests += 1
        self.successful_requests += 1
        self.consecutive_failures = 0
        self.last_success_at = time.monotonic()
        if response_time_ms is not None:
            self._total_response_time_ms += response_time_ms

    def record_failure(self) -> None:
        """Записывает сбой при использовании этого прокси."""
        self.total_requests += 1
        self.failed_requests += 1
        self.consecutive_failures += 1
        self.last_failure_at = time.monotonic()

    def as_dict(self) -> Dict[str, object]:
        """Возвращает словарь метрик для отладки/логирования (все поля кроме `proxy`)."""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.success_rate, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 1),
            "consecutive_failures": self.consecutive_failures,
            "last_success_at": self.last_success_at,
            "last_failure_at": self.last_failure_at,
            "status": self.status.value,
            "disabled_until": self.disabled_until,
        }


class HealthCheck:
    """
    Централизованная точка доступа к мониторингу здоровья прокси.

    Proxy Manager вызывает `record_success()`/`record_failure()` при
    каждом исходе реального запроса (пассивный мониторинг), а также
    `filter_healthy()` перед тем, как передать пул в Proxy Selection.
    Активная проверка доступна через `check_proxy()`.

    Все пороговые значения берутся из Configuration Manager и могут быть
    изменены через `.env` без правок кода.
    """

    _stats: Dict[str, ProxyStats] = {}

    @classmethod
    def _get_or_create(cls, proxy_url: str) -> ProxyStats:
        """Возвращает (или создаёт) статистику для URL прокси."""
        stats = cls._stats.get(proxy_url)
        if stats is None:
            stats = ProxyStats(proxy=proxy_url)
            cls._stats[proxy_url] = stats
        return stats

    @classmethod
    def _recalc_status(cls, stats: ProxyStats) -> None:
        """
        Пересчитывает `stats.status` по текущим порогам из Configuration
        Manager. Вызывается после каждого `record_success()`/`record_failure()`.

        Логика (от самого строгого состояния к самому мягкому):
        * DISABLED: если `disabled_until` ещё не истёк — остаётся DISABLED.
          Если истёк — сбрасываем `disabled_until` и `consecutive_failures`,
          давая прокси шанс на восстановление (Recovery, см. TASK.md).
        * DISABLED (переход): если
          `consecutive_failures >= HEALTH_MAX_CONSECUTIVE_FAILURES`, то
          прокси автоматически DISABLED на `HEALTH_DISABLE_DURATION_SECONDS`.
        * UNHEALTHY: промежуточная (более серьёзная, чем WARNING, но ещё не
          DISABLED) деградация — если
          `consecutive_failures >= HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES`.
          Не блокирует использование прокси (в отличие от DISABLED) — это
          лишь сигнал для Proxy Selection на будущее.
        * WARNING: если `success_rate < HEALTH_MIN_SUCCESS_RATE` ТОЛЬКО
          при наличии хотя бы `config.HEALTH_MIN_REQUESTS_FOR_RATE` запросов
          (чтобы маленькая выборка не давала ложно-негативный статус), либо
          если среднее время ответа превышает `HEALTH_MAX_RESPONSE_TIME_MS`.
        * Иначе — HEALTHY.

        Restoring/Recovery: любой успешный запрос сбрасывает
        `consecutive_failures` в 0 (см. `ProxyStats.record_success()`), поэтому
        UNHEALTHY/WARNING статусы автоматически снимаются при следующем же
        успешном passive-запросе или активной проверке (`check_proxy()`) —
        отдельного фонового планировщика для них не требуется. Для DISABLED
        восстановление происходит по истечении `disabled_until` (см. выше).
        """
        now = time.monotonic()

        # Проверка окна DISABLED
        if stats.disabled_until is not None:
            if now < stats.disabled_until:
                stats.status = HealthStatus.DISABLED
                return
            # Окно истекло — сбрасываем счётчик и даём шанс на восстановление
            stats.disabled_until = None
            stats.consecutive_failures = 0

        # Порог последовательных сбоев → DISABLED
        if stats.consecutive_failures >= config.HEALTH_MAX_CONSECUTIVE_FAILURES:
            stats.status = HealthStatus.DISABLED
            stats.disabled_until = now + config.HEALTH_DISABLE_DURATION_SECONDS
            return

        # Промежуточный порог последовательных сбоев → UNHEALTHY
        if stats.consecutive_failures >= config.HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES:
            stats.status = HealthStatus.UNHEALTHY
            return

        # Порог success rate → WARNING (только при достаточной выборке)
        if (
            stats.total_requests >= config.HEALTH_MIN_REQUESTS_FOR_RATE
            and stats.success_rate < config.HEALTH_MIN_SUCCESS_RATE
        ):
            stats.status = HealthStatus.WARNING
            return

        # Порог времени ответа → WARNING
        if (
            stats.successful_requests > 0
            and stats.avg_response_time_ms > config.HEALTH_MAX_RESPONSE_TIME_MS
        ):
            stats.status = HealthStatus.WARNING
            return

        stats.status = HealthStatus.HEALTHY


    @classmethod
    def record_success(
        cls, proxy_url: str, response_time_ms: Optional[float] = None
    ) -> None:
        """
        Записывает успешный запрос через указанный прокси (пассивный мониторинг).

        Вызывается Proxy Manager через `report_proxy_success()`.

        Args:
            proxy_url (str): URL прокси, через который был выполнен запрос.
            response_time_ms (float, optional): Время ответа в миллисекундах
                (если доступно — для вычисления среднего).
        """
        stats = cls._get_or_create(proxy_url)
        stats.record_success(response_time_ms)
        cls._recalc_status(stats)

    @classmethod
    def record_failure(cls, proxy_url: str) -> None:
        """
        Записывает сбой при использовании указанного прокси (пассивный мониторинг).

        Вызывается Proxy Manager через `report_proxy_failure()`.

        Args:
            proxy_url (str): URL прокси, через который произошёл сбой.
        """
        stats = cls._get_or_create(proxy_url)
        stats.record_failure()
        cls._recalc_status(stats)

    @classmethod
    def get_status(cls, proxy_url: str) -> HealthStatus:
        """
        Возвращает текущий статус здоровья прокси.

        Если статистики для прокси ещё нет, он считается HEALTHY (ни один
        запрос не был сделан — нет данных, чтобы считать иначе).
        """
        stats = cls._stats.get(proxy_url)
        if stats is None:
            return HealthStatus.HEALTHY
        # Проверяем, не истекло ли окно DISABLED — если истекло, пересчитываем
        if (
            stats.status == HealthStatus.DISABLED
            and stats.disabled_until is not None
            and time.monotonic() >= stats.disabled_until
        ):
            cls._recalc_status(stats)
        return stats.status

    @classmethod
    def is_usable(cls, proxy_url: str) -> bool:
        """
        Считается ли прокси пригодным для использования сейчас.

        Непригодны: DISABLED прокси. UNHEALTHY/WARNING прокси по-прежнему
        считаются пригодными — их низкое качество может быть временным, и
        полное исключение привело бы к слишком агрессивной фильтрации.
        """
        return cls.get_status(proxy_url) != HealthStatus.DISABLED

    @classmethod
    def filter_healthy(cls, proxies: List[str]) -> List[str]:
        """
        Возвращает отфильтрованный список прокси, исключая DISABLED.

        Если ВСЕ прокси отфильтрованы (пустой результат), возвращает
        исходный список с предупреждением в лог — это гарантирует, что
        фреймворк не остановится полностью из-за временного всплеска сбоев.

        Args:
            proxies (List[str]): Исходный пул прокси.

        Returns:
            List[str]: Отфильтрованный пул (или исходный, если все нездоровы).
        """
        healthy = [p for p in proxies if cls.is_usable(p)]
        if not healthy and proxies:
            print(
                f"[{__file__}] Предупреждение: все прокси ({len(proxies)}) "
                f"непригодны (DISABLED). Используется нефильтрованный пул "
                f"для сохранения работоспособности."
            )
            return proxies
        return healthy

    @classmethod
    def get_stats(cls, proxy_url: str) -> Optional[ProxyStats]:
        """Возвращает статистику для указанного прокси, либо None."""
        return cls._stats.get(proxy_url)

    @classmethod
    def get_all_stats(cls) -> Dict[str, ProxyStats]:
        """Возвращает всю собранную статистику (для отладки/логирования)."""
        return cls._stats

    @classmethod
    def check_proxy(cls, proxy_url: str) -> bool:
        """
        Активная проверка: выполняет легковесный HTTP GET-запрос через
        указанный прокси на настраиваемый тестовый URL
        (`config.HEALTH_CHECK_URL`).

        Это ЕДИНСТВЕННЫЙ метод в Health Check, который выполняет реальный
        HTTP-запрос. Он не вызывается автоматически внутри `get_proxy()` —
        доступен как API для будущего фонового вызова (например, из
        Health Check scheduler или перед добавлением прокси в ротацию).

        Результат проверки автоматически обновляет пассивную статистику
        (`record_success`/`record_failure`).

        Args:
            proxy_url (str): URL прокси для проверки.

        Returns:
            bool: `True`, если прокси успешно ответил на тестовый запрос.
        """
        try:
            start = time.monotonic()
            response = requests.get(
                config.HEALTH_CHECK_URL,
                proxies={"http": proxy_url, "https": proxy_url},
                timeout=config.HEALTH_CHECK_TIMEOUT,
            )
            elapsed = (time.monotonic() - start) * 1000.0  # в миллисекундах
            cls.record_success(proxy_url, response_time_ms=elapsed)
            return True
        except Exception:
            cls.record_failure(proxy_url)
            return False

    @classmethod
    def reset(cls, proxy_url: Optional[str] = None) -> None:
        """
        Сбрасывает статистику: для одного прокси (если указан) или полностью.

        Args:
            proxy_url (str, optional): URL прокси для сброса. Если `None`,
                сбрасывается вся статистика.
        """
        if proxy_url is not None:
            cls._stats.pop(proxy_url, None)
        else:
            cls._stats.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    proxy = "http://demo_user:demo_pass@10.0.0.1:8000"

    print(f"[{__file__}] Начальный статус (без данных): {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] is_usable(): {HealthCheck.is_usable(proxy)}")

    print(f"[{__file__}] Симулируем 5 успешных запросов...")
    for i in range(5):
        HealthCheck.record_success(proxy, response_time_ms=150.0 + i * 10)
    print(f"[{__file__}] Статус после успехов: {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] Статистика: {HealthCheck.get_stats(proxy).as_dict()}")

    print(f"[{__file__}] Симулируем {config.HEALTH_MAX_CONSECUTIVE_FAILURES} "
          f"последовательных сбоев...")
    for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
        HealthCheck.record_failure(proxy)
    print(f"[{__file__}] Статус после сбоев: {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] is_usable(): {HealthCheck.is_usable(proxy)}")

    print(f"[{__file__}] filter_healthy() на пуле из 3 прокси (1 DISABLED):")
    pool = ["http://1.1.1.1:1111", proxy, "http://3.3.3.3:3333"]
    filtered = HealthCheck.filter_healthy(pool)
    print(f"[{__file__}]   Исходный: {pool}")
    print(f"[{__file__}]   Отфильтрованный: {filtered}")

    print(f"[{__file__}] filter_healthy() на пуле, где ВСЕ DISABLED:")
    all_disabled = [proxy]
    filtered = HealthCheck.filter_healthy(all_disabled)
    print(f"[{__file__}]   Исходный: {all_disabled}")
    print(f"[{__file__}]   Отфильтрованный (fallback): {filtered}")

    print(f"[{__file__}] Активная проверка реального недоступного прокси:")
    result = HealthCheck.check_proxy("http://192.0.2.1:9999")
    print(f"[{__file__}]   Результат: {result}")

    # Сброс статистики после тестов
    HealthCheck.reset()