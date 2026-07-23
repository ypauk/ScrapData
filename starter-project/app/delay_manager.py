#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Delay Manager.

Единый компонент, отвечающий за паузы между запросами — помогает
имитировать естественное поведение пользователя и снижать риск блокировок
по Rate Limiting.

Delay Manager:

* поддерживает фиксированные и случайные (в диапазоне) задержки;
* берет политику задержек (режим, диапазон, фиксированное значение) из
  Configuration Manager (`app/config.py`);
* переиспользует существующую функцию `random_delay()` из `app/utils.py`
  вместо повторной реализации `random.uniform` + `time.sleep`.

Delay Manager НЕ выполняет HTTP-запросы, НЕ выполняет повторы, НЕ управляет
куками/прокси/User-Agent и НЕ содержит логики скрапинга — это ответственность
других компонентов (Session Manager, Retry Manager, Cookie Manager,
будущий Proxy Manager).
"""

import time
from typing import Optional

from app import config
from app.utils import random_delay


class DelayManager:
    """
    Централизованная политика пауз между запросами.

    Поддерживает два режима, конфигурируемых через `app/config.py`:
    * "fixed"  — постоянная пауза длительностью `config.DELAY_FIXED_SECONDS`;
    * "random" — случайная пауза в диапазоне
      [`config.DELAY_MIN_SECONDS`, `config.DELAY_MAX_SECONDS`].
    """

    @staticmethod
    def wait_fixed(seconds: Optional[float] = None) -> None:
        """
        Выполняет фиксированную паузу.

        Args:
            seconds (float, optional): Длительность паузы в секундах.
                По умолчанию — `config.DELAY_FIXED_SECONDS`.
        """
        delay = seconds if seconds is not None else config.DELAY_FIXED_SECONDS
        time.sleep(delay)

    @staticmethod
    def wait_random(min_seconds: Optional[float] = None, max_seconds: Optional[float] = None) -> None:
        """
        Выполняет случайную паузу в заданном диапазоне.

        Переиспользует `app.utils.random_delay()` — не дублирует логику
        генерации случайной задержки.

        Args:
            min_seconds (float, optional): Минимум паузы.
                По умолчанию — `config.DELAY_MIN_SECONDS`.
            max_seconds (float, optional): Максимум паузы.
                По умолчанию — `config.DELAY_MAX_SECONDS`.
        """
        low = min_seconds if min_seconds is not None else config.DELAY_MIN_SECONDS
        high = max_seconds if max_seconds is not None else config.DELAY_MAX_SECONDS
        random_delay(low, high)

    @classmethod
    def wait(cls, mode: Optional[str] = None) -> None:
        """
        Выполняет паузу согласно текущей политике задержек
        (`config.DELAY_MODE`, если `mode` не передан явно).

        Это основная точка входа, которую должны использовать будущие
        компоненты (Requests Engine, Playwright Engine) между запросами.

        Args:
            mode (str, optional): "fixed" или "random". По умолчанию —
                `config.DELAY_MODE`.
        """
        active_mode = (mode or config.DELAY_MODE).strip().lower()

        if active_mode == "fixed":
            cls.wait_fixed()
        elif active_mode == "random":
            cls.wait_random()
        else:
            print(f"[{__file__}] Предупреждение: неизвестный режим задержки '{active_mode}', "
                  f"используется 'random' по умолчанию.")
            cls.wait_random()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Текущая политика: mode={config.DELAY_MODE}, "
          f"fixed={config.DELAY_FIXED_SECONDS}s, "
          f"random=[{config.DELAY_MIN_SECONDS}s, {config.DELAY_MAX_SECONDS}s]")

    print(f"[{__file__}] Тест wait_fixed(0.2)...")
    start = time.time()
    DelayManager.wait_fixed(0.2)
    print(f"  Прошло: {time.time() - start:.2f}с")

    print(f"[{__file__}] Тест wait_random(0.1, 0.3)...")
    start = time.time()
    DelayManager.wait_random(0.1, 0.3)
    print(f"  Прошло: {time.time() - start:.2f}с")

    print(f"[{__file__}] Тест wait() согласно политике из конфигурации...")
    start = time.time()
    DelayManager.wait()
    print(f"  Прошло: {time.time() - start:.2f}с")
