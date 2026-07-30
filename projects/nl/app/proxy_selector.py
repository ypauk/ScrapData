#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Selection.

Централизованный компонент, отвечающий ТОЛЬКО за выбор одного прокси из
уже готового пула (`List[str]`), полученного от Proxy Manager.

Proxy Selection:

* НЕ знает, откуда взялся пул прокси (Webshare, File Provider, Proxy Cache
  и т.д.) — работает исключительно со списком строк, который ему передают;
* НЕ скачивает, НЕ валидирует и НЕ проверяет здоровье прокси;
* НЕ ротирует прокси после сбоев и НЕ поддерживает sticky-сессии — это
  ответственность будущих компонентов (Proxy Rotation, Health Check,
  Sticky Sessions, см. `framework/ROADMAP.md`, Milestone 3);
* НЕ выполняет HTTP-запросы.

Поддерживает несколько стратегий выбора через простой реестр
(`ProxySelector.register_strategy()`), что позволяет добавлять новые
стратегии (Round Robin, LRU, Fastest Proxy, Priority Based и т.д.) в
будущем без изменения существующего кода — достаточно зарегистрировать
новый класс `SelectionStrategy` и переключить `PROXY_SELECTION_STRATEGY`
в Configuration Manager.
"""

import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app import config


class SelectionStrategy(ABC):
    """
    Абстрактная стратегия выбора одного прокси из пула.

    Любая новая стратегия (Round Robin, LRU, Fastest Proxy и т.д.) должна
    реализовать этот интерфейс и быть зарегистрирована через
    `ProxySelector.register_strategy()` — сам `ProxySelector` при этом не
    меняется.
    """

    @abstractmethod
    def select(self, proxies: List[str]) -> Optional[str]:
        """
        Выбирает один прокси из переданного пула.

        Args:
            proxies (List[str]): Пул доступных прокси (может быть пустым).

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        raise NotImplementedError


class FirstAvailableStrategy(SelectionStrategy):
    """Всегда выбирает первый прокси из пула (самая простая, детерминированная стратегия)."""

    def select(self, proxies: List[str]) -> Optional[str]:
        return proxies[0] if proxies else None


class RandomStrategy(SelectionStrategy):
    """Выбирает случайный прокси из пула — простое равномерное распределение нагрузки."""

    def select(self, proxies: List[str]) -> Optional[str]:
        return random.choice(proxies) if proxies else None


class ProxySelector:
    """
    Централизованная точка доступа к логике выбора прокси.

    Proxy Manager вызывает только `ProxySelector.select(pool)` — он не
    знает, какая стратегия активна и как она устроена. Активная стратегия
    настраивается через Configuration Manager (`config.PROXY_SELECTION_STRATEGY`)
    и может быть переключена в рантайме через `set_strategy()`.
    """

    # Реестр доступных стратегий: имя -> экземпляр. Новые стратегии
    # добавляются через `register_strategy()` без изменения этого класса.
    _strategies: Dict[str, SelectionStrategy] = {
        "first": FirstAvailableStrategy(),
        "random": RandomStrategy(),
    }

    _active_strategy_name: str = config.PROXY_SELECTION_STRATEGY

    @classmethod
    def register_strategy(cls, name: str, strategy: SelectionStrategy) -> None:
        """
        Регистрирует новую стратегию выбора без изменения существующего кода.

        Args:
            name (str): Уникальное имя стратегии (используется в
                `config.PROXY_SELECTION_STRATEGY` и `set_strategy()`).
            strategy (SelectionStrategy): Экземпляр стратегии.
        """
        cls._strategies[name] = strategy

    @classmethod
    def set_strategy(cls, name: str) -> None:
        """
        Переключает активную стратегию выбора в рантайме.

        Args:
            name (str): Имя зарегистрированной стратегии.

        Raises:
            ValueError: Если стратегия с таким именем не зарегистрирована.
        """
        if name not in cls._strategies:
            raise ValueError(
                f"Неизвестная стратегия выбора прокси: '{name}'. "
                f"Доступные: {list(cls._strategies.keys())}"
            )
        cls._active_strategy_name = name

    @classmethod
    def get_strategy_name(cls) -> str:
        """Возвращает имя текущей активной стратегии."""
        return cls._active_strategy_name

    @classmethod
    def select(cls, proxies: List[str]) -> Optional[str]:
        """
        Выбирает один прокси из пула, используя текущую активную стратегию.

        Если сконфигурированная стратегия неизвестна (например, опечатка в
        `.env`), не падает — откатывается на `FirstAvailableStrategy` с
        предупреждением в лог, чтобы не ломать работу фреймворка.

        Args:
            proxies (List[str]): Пул доступных прокси.

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        strategy = cls._strategies.get(cls._active_strategy_name)
        if strategy is None:
            print(f"[{__file__}] Предупреждение: стратегия выбора прокси "
                  f"'{cls._active_strategy_name}' не зарегистрирована. "
                  f"Используется 'first'.")
            strategy = cls._strategies["first"]
        return strategy.select(proxies)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    pool = ["http://1.1.1.1:1111", "http://2.2.2.2:2222", "http://3.3.3.3:3333"]

    print(f"[{__file__}] Активная стратегия (из config): {ProxySelector.get_strategy_name()}")
    print(f"[{__file__}] select() с текущей стратегией: {ProxySelector.select(pool)}")

    ProxySelector.set_strategy("first")
    print(f"[{__file__}] FirstAvailable: {ProxySelector.select(pool)}")

    ProxySelector.set_strategy("random")
    print(f"[{__file__}] Random (3 выбора): "
          f"{[ProxySelector.select(pool) for _ in range(3)]}")

    print(f"[{__file__}] select() на пустом пуле: {ProxySelector.select([])}")

    # Демонстрация расширения без изменения ProxySelector/SelectionStrategy
    class LastAvailableStrategy(SelectionStrategy):
        """Пример будущей стратегии — выбирает последний прокси в пуле."""

        def select(self, proxies: List[str]) -> Optional[str]:
            return proxies[-1] if proxies else None

    ProxySelector.register_strategy("last", LastAvailableStrategy())
    ProxySelector.set_strategy("last")
    print(f"[{__file__}] Новая стратегия 'last' (пример расширения): {ProxySelector.select(pool)}")

    # Возвращаем стратегию по умолчанию, чтобы не влиять на другие запуски модуля
    ProxySelector.set_strategy(config.PROXY_SELECTION_STRATEGY)
