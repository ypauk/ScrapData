#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Cache.

Централизованный, provider-независимый кэш списка прокси, снижающий
количество ненужных обращений к провайдерам (Webshare API, File Provider
и т.д.) за счет хранения последнего успешно загруженного списка прокси в
локальном JSON-файле.

Состоит из двух частей:

* `ProxyCache` — низкоуровневое файловое хранилище. Не знает о
  провайдерах, ProxyManager или формате прокси-URL — просто
  читает/пишет список строк + timestamp в JSON-файл и умеет проверять,
  истек ли TTL. Может быть заменен другим механизмом хранения (Redis,
  БД) в будущем без изменения остального кода — этим и обусловлено
  выделение его в отдельный класс (см. TASK.md, "Storage").

* `CachedProxyProvider` — прозрачная обертка (декоратор) вокруг ЛЮБОГО
  существующего `ProxyProvider` (Webshare, File, будущий BrightData).
  Сама реализует интерфейс `ProxyProvider`, поэтому Proxy Manager
  продолжает работать без единого изменения — просто оборачиваем
  провайдер при регистрации:

      ProxyManager.set_provider(CachedProxyProvider(WebshareProxyProvider()))

  `CachedProxyProvider` не содержит provider-specific логики — он вызывает
  `wrapped_provider.get_proxy()` только тогда, когда файловый кэш пуст
  или истек, и сохраняет результат обратно в кэш. Если провайдер
  недоступен (сеть, невалидный ключ и т.д.), но в кэше есть валидные
  (даже просроченные) данные — используются они, чтобы не терять список
  прокси из-за временного сбоя провайдера.

Proxy Cache НЕ ротирует, НЕ валидирует и НЕ выбирает прокси, НЕ проверяет
их здоровье — вся эта логика вне его ответственности (Proxy Rotation /
Health Check / Proxy Selection, см. `framework/ROADMAP.md`).
"""

import json
import time
from pathlib import Path
from typing import List, Optional

from app import config
from app.proxy_manager import ProxyProvider


class ProxyCache:
    """
    Файловое хранилище последнего успешно загруженного списка прокси.

    Формат файла — простой JSON:
        {"proxies": ["http://...", "http://..."], "cached_at": 1719999999.123}

    `ProxyCache` не знает, откуда взялись прокси (Webshare, File Provider
    и т.д.) — он просто хранит список строк и время последнего сохранения.
    """

    def __init__(self, path: Path = None, ttl_seconds: int = None):
        """
        Args:
            path (Path, optional): Путь к файлу кэша. По умолчанию —
                `config.PROXY_CACHE_FILE`.
            ttl_seconds (int, optional): Время жизни кэша в секундах.
                По умолчанию — `config.PROXY_CACHE_TTL_SECONDS`.
        """
        self.path = path or config.PROXY_CACHE_FILE
        self.ttl_seconds = ttl_seconds if ttl_seconds is not None else config.PROXY_CACHE_TTL_SECONDS

    def load(self) -> Optional[dict]:
        """
        Читает содержимое файла кэша.

        Обрабатывает отсутствующий, пустой и поврежденный (невалидный JSON)
        файл без падения приложения.

        Returns:
            Optional[dict]: Словарь `{"proxies": [...], "cached_at": float}`,
                либо `None`, если файл отсутствует, пуст или поврежден.
        """
        if not self.path.exists():
            return None

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[{__file__}] Ошибка чтения файла кэша прокси {self.path.name}: {e}")
            return None

        if not raw.strip():
            return None

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[{__file__}] Предупреждение: кэш прокси поврежден "
                  f"({self.path.name}): {e}. Кэш будет перезаписан при следующем обновлении.")
            return None

        if not isinstance(data, dict) or "proxies" not in data or "cached_at" not in data:
            print(f"[{__file__}] Предупреждение: неожиданный формат файла кэша прокси "
                  f"{self.path.name}. Кэш будет перезаписан при следующем обновлении.")
            return None

        return data

    def get_proxies(self) -> List[str]:
        """
        Возвращает список прокси из кэша независимо от того, истек ли TTL.

        Returns:
            List[str]: Список закэшированных прокси (пустой, если кэша нет).
        """
        data = self.load()
        if not data:
            return []
        return list(data.get("proxies") or [])

    def is_expired(self) -> bool:
        """
        Проверяет, истек ли TTL кэша (или кэш вовсе отсутствует/поврежден/пуст).

        Returns:
            bool: `True`, если кэш нужно обновить через провайдер.
        """
        data = self.load()
        if not data or not data.get("proxies"):
            return True
        cached_at = data.get("cached_at", 0)
        return (time.time() - cached_at) >= self.ttl_seconds

    def save(self, proxies: List[str]) -> None:
        """
        Сохраняет список прокси в файл кэша с текущей временной меткой.

        Пустой список НЕ сохраняется — это защищает уже закэшированные
        валидные данные от затирания при временном сбое провайдера
        (см. `CachedProxyProvider.get_proxy()`).

        Args:
            proxies (List[str]): Список нормализованных URL прокси.
        """
        if not proxies:
            return

        payload = {"proxies": proxies, "cached_at": time.time()}
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError as e:
            print(f"[{__file__}] Ошибка записи файла кэша прокси {self.path.name}: {e}")

    def clear(self) -> None:
        """Удаляет файл кэша, если он существует."""
        if self.path.exists():
            try:
                self.path.unlink()
                print(f"[{__file__}] Кэш прокси очищен: {self.path.name}")
            except OSError as e:
                print(f"[{__file__}] Ошибка удаления файла кэша прокси {self.path.name}: {e}")


class CachedProxyProvider(ProxyProvider):
    """
    Прозрачная обертка над любым `ProxyProvider`, добавляющая персистентный
    файловый кэш (см. `ProxyCache`).

    Использование (без изменения Proxy Manager):

        from app.proxy_manager import ProxyManager
        from app.webshare_proxy_provider import WebshareProxyProvider
        from app.proxy_cache import CachedProxyProvider

        ProxyManager.set_provider(CachedProxyProvider(WebshareProxyProvider()))

    Proxy Manager продолжает вызывать только `get_proxy()` — он не знает
    и не должен знать, что результат кэшируется.
    """

    def __init__(self, provider: ProxyProvider, cache: ProxyCache = None):
        """
        Args:
            provider (ProxyProvider): Оборачиваемый провайдер (Webshare,
                File или любой другой, реализующий `ProxyProvider`).
            cache (ProxyCache, optional): Экземпляр файлового кэша.
                По умолчанию создается новый `ProxyCache()` с настройками
                из Configuration Manager.
        """
        self.provider = provider
        self.cache = cache or ProxyCache()
        self._proxies: List[str] = []

    def _refresh_from_provider(self) -> List[str]:
        """
        Запрашивает актуальный список прокси у оборачиваемого провайдера
        и сохраняет его в файловый кэш.

        Если провайдер поддерживает `get_all_proxies()` (как
        `FileProxyProvider`/`WebshareProxyProvider`), используется он —
        это позволяет закэшировать весь список, а не только один прокси.
        Иначе используется единственный результат `get_proxy()`.

        Returns:
            List[str]: Свежий список прокси от провайдера (может быть
                пустым, если провайдер недоступен).
        """
        get_all = getattr(self.provider, "get_all_proxies", None)
        if callable(get_all):
            proxies = get_all()
        else:
            proxy = self.provider.get_proxy()
            proxies = [proxy] if proxy else []

        if proxies:
            self.cache.save(proxies)

        return proxies

    def _ensure_loaded(self) -> None:
        """
        Гарантирует, что `self._proxies` заполнен: сначала пробует кэш
        (если не истек), иначе запрашивает провайдер. Если провайдер
        недоступен, но в кэше есть хоть просроченные данные — используются
        они (graceful degradation, см. TASK.md "Error Handling").
        """
        if self._proxies:
            return

        if not self.cache.is_expired():
            self._proxies = self.cache.get_proxies()
            if self._proxies:
                return

        fresh = self._refresh_from_provider()
        if fresh:
            self._proxies = fresh
            return

        # Провайдер недоступен/вернул пусто — используем то, что есть в
        # кэше, даже если оно просрочено, лучше устаревшие прокси, чем ничего.
        stale = self.cache.get_proxies()
        if stale:
            print(f"[{__file__}] Провайдер недоступен — используются устаревшие "
                  f"данные из кэша прокси ({len(stale)} шт.).")
        self._proxies = stale

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый доступный прокси (из кэша либо от провайдера).

        Returns:
            Optional[str]: URL прокси, либо `None`, если ни кэш, ни
                провайдер не смогли предоставить ни одного прокси.
        """
        self._ensure_loaded()
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный список прокси (из кэша либо от провайдера).

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        self._ensure_loaded()
        return list(self._proxies)

    def refresh(self) -> List[str]:
        """
        Принудительно обновляет кэш через оборачиваемый провайдер,
        игнорируя текущий TTL.

        Returns:
            List[str]: Обновленный список прокси (может быть пустым,
                если провайдер недоступен и кэш также пуст).
        """
        fresh = self._refresh_from_provider()
        self._proxies = fresh or self.cache.get_proxies()
        return list(self._proxies)

    def clear_cache(self) -> None:
        """Полностью очищает файловый кэш и внутреннее состояние обертки."""
        self.cache.clear()
        self._proxies = []


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.file_proxy_provider import FileProxyProvider
    from app.proxy_manager import ProxyManager

    cached = CachedProxyProvider(FileProxyProvider())
    print(f"[{__file__}] Файл кэша: {cached.cache.path}")
    print(f"[{__file__}] Кэш истек: {cached.cache.is_expired()}")
    print(f"[{__file__}] get_all_proxies(): {cached.get_all_proxies()}")
    print(f"[{__file__}] get_proxy(): {cached.get_proxy()}")

    # Интеграция с Proxy Manager без изменения его кода.
    ProxyManager.set_provider(cached)
    print(f"[{__file__}] ProxyManager.get_proxy(): {ProxyManager.get_proxy()}")
