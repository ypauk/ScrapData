#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Rotation.

Централизованный компонент, отвечающий ТОЛЬКО за то, КОГДА текущий прокси
должен быть заменен новым. Он НЕ решает, КАКОЙ прокси выбрать следующим
(это ответственность Proxy Selection, `app/proxy_selector.py`) и НЕ знает,
откуда прокси берутся (Webshare/File Provider/Proxy Cache и т.д.).

Proxy Rotation:

* НЕ выбирает следующий прокси;
* НЕ скачивает и НЕ валидирует прокси;
* НЕ проверяет здоровье прокси (Health Check — будущий компонент);
* НЕ выполняет HTTP-запросы;
* НЕ содержит provider-specific логики.

Интегрируется только с:
* Configuration Manager (`app/config.py`) — активная политика конфигурируется
  через `.env`, смена политики не требует правок кода;
* Proxy Manager (`app/proxy_manager.py`) — единственный вызывающий код,
  который спрашивает `ProxyRotation.should_rotate()` перед тем, как
  запросить новый выбор у Proxy Selection;
* Proxy Selection — косвенно, только в том смысле, что Rotation определяет
  МОМЕНТ вызова `ProxySelector.select()`, но сам его не вызывает.

Поддерживает несколько политик ротации через реестр
(`ProxyRotation.register_policy()`), что позволяет добавлять будущие
политики (Rotate Every X Minutes, Adaptive Rotation, Manual Rotation и
т.д.) без изменения существующего кода.
"""

from abc import ABC, abstractmethod
from typing import Dict

from app import config


class RotationPolicy(ABC):
    """
    Абстрактная политика ротации.

    Каждый вызов `Proxy Manager.get_proxy()` соответствует одному
    "запросу" в терминах политики. Политика решает, нужно ли сменить
    текущий прокси ПЕРЕД тем, как он будет использован для этого запроса.

    Любая новая политика (Rotate Every X Minutes, Adaptive Rotation и
    т.д.) должна реализовать этот интерфейс и быть зарегистрирована через
    `ProxyRotation.register_policy()` — сам `ProxyRotation` при этом не
    меняется.
    """

    @abstractmethod
    def should_rotate(self) -> bool:
        """
        Определяет, нужно ли заменить текущий прокси перед следующим
        использованием.

        Вызывается Proxy Manager перед каждым `get_proxy()` (после того,
        как уже есть хотя бы один выбранный прокси — самый первый выбор
        всегда происходит независимо от политики, это ответственность
        Proxy Manager, а не Rotation).

        Returns:
            bool: `True`, если Proxy Manager должен запросить новый выбор
                у Proxy Selection.
        """
        raise NotImplementedError

    def record_failure(self) -> None:
        """
        Уведомляет политику о сбое при использовании текущего прокси.

        Базовая реализация — no-op. Переопределяется политиками, которым
        это важно (например, `RotateAfterFailurePolicy`). Вызывается
        через `ProxyManager.report_proxy_failure()` — сам Rotation никогда
        не узнает о сбое иначе, чем через явный вызов извне (Retry Manager
        или будущий Health Check).
        """
        return

    def reset(self) -> None:
        """
        Сбрасывает внутреннее состояние политики (счетчики и т.д.).

        Вызывается Proxy Manager каждый раз, когда фактически происходит
        смена прокси — большинство политик считают именно "запросы с
        текущим прокси", поэтому счетчик должен обнуляться при ротации.
        Базовая реализация — no-op (например, у `NeverRotatePolicy` и
        `RotateEveryRequestPolicy` нет состояния для сброса).
        """
        return


class NeverRotatePolicy(RotationPolicy):
    """Прокси никогда не меняется автоматически после первого выбора."""

    def should_rotate(self) -> bool:
        return False


class RotateEveryRequestPolicy(RotationPolicy):
    """
    Прокси меняется перед каждым запросом.

    Это политика по умолчанию (`config.PROXY_ROTATION_POLICY == "every_request"`),
    воспроизводящая поведение Proxy Manager до появления Proxy Rotation —
    свежий выбор из пула при каждом вызове `get_proxy()`. Гарантирует
    полную обратную совместимость.
    """

    def should_rotate(self) -> bool:
        return True


class RotateEveryNRequestsPolicy(RotationPolicy):
    """Прокси меняется каждый N-й запрос (счетчик сбрасывается при ротации)."""

    def __init__(self, n: int = None):
        """
        Args:
            n (int, optional): Количество запросов между ротациями.
                По умолчанию — `config.PROXY_ROTATION_EVERY_N`.
        """
        self.n = n if n is not None else config.PROXY_ROTATION_EVERY_N
        self._request_count = 0

    def should_rotate(self) -> bool:
        self._request_count += 1
        return self._request_count >= self.n

    def reset(self) -> None:
        self._request_count = 0


class RotateAfterFailurePolicy(RotationPolicy):
    """
    Прокси меняется только после явного сигнала о сбое
    (`ProxyManager.report_proxy_failure()` -> `record_failure()`).

    Сама политика НЕ выполняет HTTP-запросы и НЕ проверяет здоровье прокси —
    она лишь реагирует на внешний сигнал, источник которого (Retry Manager,
    будущий Health Check и т.д.) не является ее заботой.
    """

    def __init__(self):
        self._failed = False

    def record_failure(self) -> None:
        self._failed = True

    def should_rotate(self) -> bool:
        return self._failed

    def reset(self) -> None:
        self._failed = False


class ProxyRotation:
    """
    Централизованная точка доступа к логике ротации прокси.

    Proxy Manager вызывает только `ProxyRotation.should_rotate()` (и,
    при сбоях, `record_failure()`) — он не знает, какая политика активна
    и как она устроена. Активная политика настраивается через
    Configuration Manager (`config.PROXY_ROTATION_POLICY`) и может быть
    переключена в рантайме через `set_policy()`.
    """

    # Реестр доступных политик: имя -> экземпляр. Новые политики
    # добавляются через `register_policy()` без изменения этого класса.
    _policies: Dict[str, RotationPolicy] = {
        "never": NeverRotatePolicy(),
        "every_request": RotateEveryRequestPolicy(),
        "every_n_requests": RotateEveryNRequestsPolicy(),
        "after_failure": RotateAfterFailurePolicy(),
    }

    _active_policy_name: str = config.PROXY_ROTATION_POLICY

    @classmethod
    def register_policy(cls, name: str, policy: RotationPolicy) -> None:
        """
        Регистрирует новую политику ротации без изменения существующего кода.

        Args:
            name (str): Уникальное имя политики (используется в
                `config.PROXY_ROTATION_POLICY` и `set_policy()`).
            policy (RotationPolicy): Экземпляр политики.
        """
        cls._policies[name] = policy

    @classmethod
    def set_policy(cls, name: str) -> None:
        """
        Переключает активную политику ротации в рантайме.

        Args:
            name (str): Имя зарегистрированной политики.

        Raises:
            ValueError: Если политика с таким именем не зарегистрирована.
        """
        if name not in cls._policies:
            raise ValueError(
                f"Неизвестная политика ротации прокси: '{name}'. "
                f"Доступные: {list(cls._policies.keys())}"
            )
        cls._active_policy_name = name

    @classmethod
    def get_policy_name(cls) -> str:
        """Возвращает имя текущей активной политики."""
        return cls._active_policy_name

    @classmethod
    def _get_active_policy(cls) -> RotationPolicy:
        """
        Возвращает экземпляр активной политики.

        Если сконфигурированная политика неизвестна (например, опечатка
        в `.env`), не падает — откатывается на `RotateEveryRequestPolicy`
        (эквивалент прежнего поведения) с предупреждением в лог.
        """
        policy = cls._policies.get(cls._active_policy_name)
        if policy is None:
            print(f"[{__file__}] Предупреждение: политика ротации прокси "
                  f"'{cls._active_policy_name}' не зарегистрирована. "
                  f"Используется 'every_request'.")
            policy = cls._policies["every_request"]
        return policy

    @classmethod
    def should_rotate(cls) -> bool:
        """
        Определяет, нужно ли заменить текущий прокси перед следующим
        использованием, используя текущую активную политику.

        Returns:
            bool: `True`, если Proxy Manager должен запросить новый выбор
                у Proxy Selection.
        """
        return cls._get_active_policy().should_rotate()

    @classmethod
    def record_failure(cls) -> None:
        """
        Уведомляет активную политику о сбое при использовании текущего
        прокси (см. `ProxyManager.report_proxy_failure()`).
        """
        cls._get_active_policy().record_failure()

    @classmethod
    def reset(cls) -> None:
        """
        Сбрасывает состояние активной политики. Вызывается Proxy Manager
        каждый раз, когда фактически происходит смена прокси.
        """
        cls._get_active_policy().reset()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Активная политика (из config): {ProxyRotation.get_policy_name()}")

    ProxyRotation.set_policy("every_request")
    print(f"[{__file__}] every_request x3: "
          f"{[ProxyRotation.should_rotate() for _ in range(3)]}")

    ProxyRotation.set_policy("never")
    print(f"[{__file__}] never x3: {[ProxyRotation.should_rotate() for _ in range(3)]}")

    ProxyRotation.set_policy("every_n_requests")
    policy = ProxyRotation._get_active_policy()
    policy.n = 3
    policy.reset()
    results = []
    for _ in range(7):
        rotate = ProxyRotation.should_rotate()
        results.append(rotate)
        if rotate:
            ProxyRotation.reset()
    print(f"[{__file__}] every_n_requests (n=3) за 7 вызовов: {results}")

    ProxyRotation.set_policy("after_failure")
    print(f"[{__file__}] after_failure до сбоя: {ProxyRotation.should_rotate()}")
    ProxyRotation.record_failure()
    print(f"[{__file__}] after_failure после сбоя: {ProxyRotation.should_rotate()}")
    ProxyRotation.reset()
    print(f"[{__file__}] after_failure после reset(): {ProxyRotation.should_rotate()}")

    # Демонстрация расширения без изменения ProxyRotation/RotationPolicy
    class RotateEveryXMinutesPolicy(RotationPolicy):
        """Пример будущей политики — заглушка, всегда возвращает False."""

        def should_rotate(self) -> bool:
            return False

    ProxyRotation.register_policy("every_x_minutes", RotateEveryXMinutesPolicy())
    ProxyRotation.set_policy("every_x_minutes")
    print(f"[{__file__}] Новая политика 'every_x_minutes' (пример расширения): "
          f"{ProxyRotation.should_rotate()}")

    # Возвращаем политику по умолчанию, чтобы не влиять на другие запуски модуля
    ProxyRotation.set_policy(config.PROXY_ROTATION_POLICY)
