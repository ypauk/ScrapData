#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from app.playwright_engine import PlaywrightEngine


def scrape_data(engine: PlaywrightEngine) -> List[str]:
    """
    Главная функция сбора данных. Принимает запущенный PlaywrightEngine.
    Выполняет навигацию, пагинацию, сбор HTML.
    Возвращает список HTML-строк (одна строка = одна страница).

    ИИ перепишет эту функцию под конкретный проект.
    """
    raw_pages_content: List[str] = []

    # TODO: ИИ заменит этот stub на реальную логику обхода
    from app import config
    engine.goto(config.BASE_URL)
    engine.wait_for_load("domcontentloaded")
    raw_pages_content.append(engine.content())

    print(f"[{__file__}] Сбор завершён. Страниц: {len(raw_pages_content)}")
    return raw_pages_content
