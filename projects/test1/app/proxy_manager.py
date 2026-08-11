#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Manager.

Единый компонент, отвечающий за предоставление прокси для HTTP-запросов
(`requests.Session`) и, в будущем, для браузерной автоматизации (Playwright,
см. Milestone 4 — Browser Manager).

Proxy Manager:

* НЕ скачивает, НЕ валидирует, НЕ ротирует и НЕ проверяет здоровье прокси —
  это ответственность будущих компонентов (Proxy Providers, Rotation,
  Health Check, см. `framework/ROADMAP.md`, Milestone 3), которые будут
  реализованы отдельными задачами;
* абстрагирует источник прокси через простой интерфейс `ProxyProvider`,
  поэтому смена провайдера (Webshare, BrightData, Oxylabs, SmartProxy,
  File Provider и т.д.) НЕ требует изменения публичного API Proxy Manager —
  достаточно зарегистрировать новый провайдер через `ProxyManager.set_provider()`;
* если провайдер предоставляет пул прокси (`get_all_proxies()`), выбор
  одного прокси из пула делегируется отдельному компоненту Proxy Selection
  (`app/proxy_selector.py`, `ProxySelector.select()`) — Proxy Manager не
  содержит и не должен содержать логики выбора (round robin/random/и т.д.),
  это ответственность Proxy Selection;
* момент, когда нужно выбрать новый прокси вместо повторного использования
  текущего, определяется отдельным компонентом Proxy Rotation
  (`app/proxy_rotation.py`, `ProxyRotation.should_rotate()`) — Proxy
  Manager хранит только текущий выбранный прокси (`_current_proxy`) и не
  содержит и не должен содержать логики принятия решения "когда менять";


* по умолчанию использует `EnvProxyProvider` — адаптер к единственному
  источнику прокси, существовавшему до этой задачи (`config.PROXY_URL`),
  сохраняя обратную совместимость;
* предоставляет прокси в формате, готовом для `requests.Session`
  (`ProxyManager.apply_to_session()`), и — на будущее — для контекста
  Playwright (`ProxyManager.to_playwright_proxy_kwargs()`).

Proxy Manager НЕ выполняет HTTP-запросы и НЕ содержит логики скрапинга.
Как и Cookie/Retry/Delay Manager, он зависит только от Configuration
Manager и НЕ вызывает и ничего не знает о других менеджерах напрямую —
это сохраняет слабую связанность компонентов вокруг Session Manager
(см. `app/session_manager.py`).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from app import config


class ProxyProvider(ABC):
    """
    Абстрактный источник прокси.

    Любой провайдер (Webshare, BrightData, File Provider и т.д.) должен
    реализовать этот интерфейс. Proxy Manager работает только через него
    и никогда не содержит специфичной для конкретного провайдера логики.
    """

    @abstractmethod
    def get_proxy(self) -> Optional[str]:
        """
        Возвращает URL прокси в формате
        `http://[username:password@]host:port`, либо `None`, если прокси
        не настроен/недоступен.
        """
        raise NotImplementedError


class EnvProxyProvider(ProxyProvider):
    """
    Провайдер по умолчанию — берет единственный прокси из переменной
    окружения `PROXY_URL` (Configuration Manager, `app/config.py`).

    Это не полноценный провайдер вроде Webshare/BrightData, а простой
    адаптер к уже существовавшей настройке `config.PROXY_URL`,
    обеспечивающий обратную совместимость до появления настоящих
    провайдеров (см. рекомендации в конце файла / TASK.md deliverable 5).
    """

    def get_proxy(self) -> Optional[str]:
        return config.PROXY_URL


class ProxyManager:
    """
    Централизованная точка доступа к прокси для всего фреймворка.

    Работает с текущим провайдером (`ProxyProvider`), не зная о его
    внутренней реализации. Провайдер можно заменить в рантайме через
    `set_provider()` — например, на будущий `WebshareProxyProvider` —
    без изменения кода, использующего `ProxyManager` (Session Manager
    и в будущем Browser Manager).
    """

    _provider: ProxyProvider = EnvProxyProvider()

    # Текущий выбранный прокси для провайдеров с пулом (`get_all_proxies()`).
    # Proxy Manager хранит только сам факт "текущего" прокси — решение о
    # том, когда его заменить, принимает Proxy Rotation, а решение о том,
    # каким именно прокси заменить — Proxy Selection.
    _current_proxy: Optional[str] = None

    @classmethod
    def set_provider(cls, provider: ProxyProvider) -> None:
        """
        Заменяет текущий источник прокси на новый провайдер.

        Сбрасывает `_current_proxy` и состояние активной политики ротации,
        чтобы не вернуть устаревший прокси от предыдущего провайдера.

        Args:
            provider (ProxyProvider): Новая реализация источника прокси
                (например, будущий WebshareProxyProvider или FileProvider).
        """
        cls._provider = provider
        cls._current_proxy = None

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        ProxyRotation.reset()


    @classmethod
    def get_provider(cls) -> ProxyProvider:
        """Возвращает текущий активный провайдер прокси."""
        return cls._provider

    @classmethod
    def _select_from_pool(cls, get_all) -> Optional[str]:
        """
        Выбирает один прокси из пула провайдера, используя Proxy Health
        Check (фильтрация) и Proxy Selection (выбор). Общая логика для
        обычного (`get_proxy()`) и sticky (`get_proxy(session_id=...)`)
        путей — вынесена сюда, чтобы не дублировать её в обоих местах.

        Args:
            get_all (Callable[[], List[str]]): `provider.get_all_proxies`.

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        from app.health_check import HealthCheck    # локальный импорт: избегаем циклической зависимости
        from app.proxy_selector import ProxySelector  # локальный импорт: избегаем циклической зависимости

        # Фильтрация пула перед выбором: исключаем DISABLED прокси.
        # Если все прокси отфильтрованы, HealthCheck.filter_healthy()
        # вернёт исходный пул с предупреждением в лог — фреймворк
        # продолжит работу без полной остановки.
        healthy_pool = HealthCheck.filter_healthy(get_all())
        return ProxySelector.select(healthy_pool)

    @classmethod
    def get_proxy(cls, session_id: Optional[str] = None) -> Optional[str]:
        """
        Возвращает прокси-URL для использования сейчас.

        Если передан `session_id` и включены Sticky Sessions
        (`config.STICKY_SESSIONS_ENABLED`), Proxy Manager делегирует выбор
        `StickySessionManager` (`app/sticky_sessions.py`): пока привязка
        сессии активна и не истекла, всегда возвращается один и тот же
        прокси, независимо от активной политики Proxy Rotation. Если
        привязки нет или она истекла (тайм-аут/лимит запросов/прокси стал
        DISABLED) — выбирается новый прокси обычным способом (см. ниже) и
        привязывается к сессии.

        Без `session_id` (или при выключенных Sticky Sessions) поведение
        полностью прежнее — обратная совместимость сохраняется:

        Если активный провайдер предоставляет пул прокси (реализует
        `get_all_proxies()` — как `WebshareProxyProvider`, `FileProxyProvider`
        или `CachedProxyProvider`), Proxy Manager хранит текущий выбранный
        прокси (`_current_proxy`) и переиспользует его до тех пор, пока
        Proxy Rotation (`app/proxy_rotation.py`, `ProxyRotation.should_rotate()`)
        не решит, что пора выбрать новый — тогда выбор нового прокси из
        пула делегируется Proxy Selection (`app/proxy_selector.py`).

        Это единственное место, где Proxy Manager взаимодействует с Proxy
        Rotation, Proxy Selection и Sticky Sessions — сам он не содержит
        ни логики "когда менять", ни логики "какой выбрать", ни логики
        "как долго привязывать".

        Если у провайдера нет пула (например, `EnvProxyProvider`, у
        которого есть только единственное значение `config.PROXY_URL`),
        поведение остается прежним — используется `provider.get_proxy()`
        напрямую, что сохраняет полную обратную совместимость.

        Args:
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions). Если не передан — привязка не используется.

        Returns:
            Optional[str]: Прокси-URL, либо `None`, если прокси не настроен
                или пул провайдера пуст.
        """
        get_all = getattr(cls._provider, "get_all_proxies", None)

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            if StickySessionManager.is_enabled():
                sticky_proxy = StickySessionManager.get_proxy(session_id)
                if sticky_proxy is not None:
                    return sticky_proxy

                new_proxy = (
                    cls._select_from_pool(get_all)
                    if callable(get_all)
                    else cls._provider.get_proxy()
                )
                if new_proxy is not None:
                    StickySessionManager.bind(session_id, new_proxy)
                return new_proxy

        if not callable(get_all):
            return cls._provider.get_proxy()

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        # Первый выбор всегда происходит независимо от политики ротации —
        # без него Proxy Manager не смог бы отдать вообще ничего.
        if cls._current_proxy is None or ProxyRotation.should_rotate():
            cls._current_proxy = cls._select_from_pool(get_all)
            ProxyRotation.reset()

        return cls._current_proxy

    @classmethod
    def report_proxy_failure(cls, session_id: Optional[str] = None) -> None:
        """
        Сообщает Proxy Rotation и Proxy Health Check о сбое при
        использовании текущего прокси.

        Если передан `session_id` и для него есть активная привязка
        (Sticky Sessions), обновляется здоровье именно привязанного
        прокси, а сама привязка обрабатывается через
        `StickySessionManager.report_failure()` (Failure Handling,
        см. TASK.md Sticky Sessions) — политика Proxy Rotation в этом
        случае не затрагивается, так как ротация вне сессии не имеет
        смысла для привязанного прокси.

        Без `session_id` поведение прежнее — обратная совместимость
        сохраняется. Proxy Manager сам не определяет, что считать сбоем —
        это решает вызывающий код (например, будущая интеграция с Retry
        Manager). Используется политикой `RotateAfterFailurePolicy`
        (`app/proxy_rotation.py`) и пассивным мониторингом здоровья
        (`app/health_check.py`).

        Args:
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions).
        """
        from app.health_check import HealthCheck   # локальный импорт: избегаем циклической зависимости

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            sticky_proxy = StickySessionManager.peek_proxy(session_id)
            if sticky_proxy is not None:
                HealthCheck.record_failure(sticky_proxy)
                StickySessionManager.report_failure(session_id)
                return

        if cls._current_proxy is None:
            return

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        HealthCheck.record_failure(cls._current_proxy)
        ProxyRotation.record_failure()

    @classmethod
    def report_proxy_success(
        cls, response_time_ms: Optional[float] = None, session_id: Optional[str] = None
    ) -> None:
        """
        Сообщает Proxy Health Check об успешном запросе через текущий
        прокси (пассивный мониторинг).

        Если передан `session_id` и для него есть активная привязка
        (Sticky Sessions), обновляется здоровье именно привязанного прокси.

        Proxy Manager сам не определяет успешность — это решает
        вызывающий код (будущий Session Manager / Requests Engine).

        Args:
            response_time_ms (float, optional): Время ответа в миллисекундах
                (если доступно — для вычисления среднего времени ответа).
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions).
        """
        from app.health_check import HealthCheck  # локальный импорт: избегаем циклической зависимости

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            sticky_proxy = StickySessionManager.peek_proxy(session_id)
            if sticky_proxy is not None:
                HealthCheck.record_success(sticky_proxy, response_time_ms)
                return

        if cls._current_proxy is None:
            return

        HealthCheck.record_success(cls._current_proxy, response_time_ms)




    @classmethod
    def to_requests_dict(cls, proxy: Optional[str] = None) -> Dict[str, str]:
        """
        Формирует словарь прокси в формате `requests`
        (`{"http": proxy, "https": proxy}`), готовый для
        `session.proxies = ...` или `requests.get(url, proxies=...)`.

        Args:
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера (`get_proxy()`).

        Returns:
            Dict[str, str]: Словарь прокси для `requests`
                (пустой, если прокси не настроен).
        """
        active_proxy = proxy if proxy is not None else cls.get_proxy()
        if not active_proxy:
            return {}
        return {"http": active_proxy, "https": active_proxy}

    @classmethod
    def apply_to_session(cls, session, proxy: Optional[str] = None) -> None:
        """
        Применяет прокси к `requests.Session`. Используется Session
        Manager при создании сессии — аналогично Cookie Manager и
        Retry Manager, независимо от них.

        Args:
            session (requests.Session): Сессия, к которой применяется прокси.
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера.
        """
        proxies = cls.to_requests_dict(proxy)
        if proxies:
            session.proxies.update(proxies)
            print(f"[{__file__}] Прокси применен к сессии: {cls._mask(proxies['http'])}")

    @classmethod
    def to_playwright_proxy_kwargs(cls, proxy: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Формирует словарь, готовый для передачи в
        `browser.new_context(proxy=...)` в будущей интеграции с Playwright
        (Milestone 4 — Browser Manager).

        Args:
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера.

        Returns:
            Optional[Dict[str, Any]]: `{"server": ..., "username": ...,
                "password": ...}`, либо `None`, если прокси не настроен.
        """
        active_proxy = proxy if proxy is not None else cls.get_proxy()
        if not active_proxy:
            return None

        parsed = urlparse(active_proxy)
        server = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
        kwargs: Dict[str, Any] = {"server": server}
        if parsed.username:
            kwargs["username"] = parsed.username
        if parsed.password:
            kwargs["password"] = parsed.password
        return kwargs

    @staticmethod
    def _mask(proxy_url: str) -> str:
        """Маскирует учетные данные в URL прокси для безопасного логирования."""
        parsed = urlparse(proxy_url)
        if parsed.username or parsed.password:
            netloc = f"***:***@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return parsed._replace(netloc=netloc).geturl()
        return proxy_url


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import requests

    print(f"[{__file__}] Текущий прокси (из config.PROXY_URL): {ProxyManager.get_proxy()}")
    print(f"[{__file__}] Словарь для requests: {ProxyManager.to_requests_dict()}")
    print(f"[{__file__}] Kwargs для Playwright: {ProxyManager.to_playwright_proxy_kwargs()}")

    session = requests.Session()
    ProxyManager.apply_to_session(session)
    print(f"[{__file__}] session.proxies: {session.proxies}")

    class DummyProxyProvider(ProxyProvider):
        """Пример альтернативного провайдера для проверки замены без изменения ProxyManager."""

        def get_proxy(self) -> Optional[str]:
            return "http://demo_user:demo_pass@10.0.0.1:8000"

    ProxyManager.set_provider(DummyProxyProvider())
    print(f"[{__file__}] После смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] Замаскированный лог: {ProxyManager._mask(ProxyManager.get_proxy())}")
    print(f"[{__file__}] Playwright kwargs с учетными данными: {ProxyManager.to_playwright_proxy_kwargs()}")

    class PoolProxyProvider(ProxyProvider):
        """Пример провайдера с пулом — демонстрирует Sticky Sessions."""

        def get_proxy(self) -> Optional[str]:
            return self.get_all_proxies()[0]

        def get_all_proxies(self):
            return ["http://1.1.1.1:1111", "http://2.2.2.2:2222", "http://3.3.3.3:3333"]

    ProxyManager.set_provider(PoolProxyProvider())
    print(f"[{__file__}] Sticky Sessions — сессия 'job-1':")
    for _ in range(3):
        print(f"[{__file__}]   get_proxy(session_id='job-1'): {ProxyManager.get_proxy(session_id='job-1')}")

    from app.sticky_sessions import StickySessionManager
    StickySessionManager.reset()

    # Возвращаем провайдер по умолчанию, чтобы не влиять на другие запуски модуля
    ProxyManager.set_provider(EnvProxyProvider())


