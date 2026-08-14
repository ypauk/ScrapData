Прочитал prompt целиком, включая анализ, план проекта, DS-PRK-Scraper.json, примеры HTML, контракт main.py, обязательные сигнатуры и финальные требования. 
GitHub
+3
GitHub
+3
GitHub
+3

Ниже — только app/parser.py. Он:

использует только BeautifulSoup для HTML;

экспортирует обязательные parse_listing() и parse_html_data();

поддерживает HTML товарных страниц и листингов;

сохраняет точные имена полей, включая пробелы в "Title " и "Description ";

корректно обрабатывает EU-цены;

извлекает breadcrumb, title, short description, description, изображения и характеристики;

при отсутствии данных возвращает "";

не содержит классов, HTTP-запросов, Playwright или другой сетевой логики. 
GitHub
+2
GitHub
+2

Python
Run
# app/parser.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import Any, Dict, List
from urllib.parse import urlparse, unquote


from bs4 import BeautifulSoup




def _clean_text(value: str, preserve_lines: bool = False) -> str:
    """Очищает текст от лишних пробелов, сохраняя переносы при необходимости."""
    if not value:
        return ""


    value = value.replace("\xa0", " ")


    lines = []
    for line in value.splitlines():
        line = " ".join(line.split())
        if line:
            lines.append(line)


    if preserve_lines:
        return "\n".join(lines)


    return " ".join(lines)




def _text_from_node(node: Any, preserve_lines: bool = False) -> str:
    """Извлекает чистый текст из BeautifulSoup node."""
    if node is None:
        return ""


    try:
        for unwanted in node.find_all(
            ["script", "style", "noscript", "template"]
        ):
            unwanted.decompose()


        text = node.get_text("\n" if preserve_lines else " ", strip=True)
        return _clean_text(text, preserve_lines=preserve_lines)
    except Exception as exc:
        print(f"[{__file__}] text extraction error: {exc}")
        return ""




def _extract_url(soup: BeautifulSoup) -> str:
    """Извлекает URL страницы товара из canonical/og:url."""
    try:
        canonical = soup.select_one('link[rel="canonical"]')
        if canonical and canonical.get("href"):
            return canonical["href"].strip()


        og_url = soup.select_one('meta[property="og:url"]')

Локально достаточно проверить импорт и парсинг сохранённого HTML, например:

Bash
python -c "from app.parser import parse_listing, parse_html_data; print('parser import OK')"

или:

Bash
python -c "from pathlib import Path; from app.parser import parse_listing; html=Path('page.html').read_text(encoding='utf-8'); print(parse_listing(html))"

Код намеренно не пытается скачивать изображения: согласно контракту из prompt, parser.py отвечает только за извлечение данных из сырого HTML, а сетевой доступ и получение страниц относятся к scraper.py/PlaywrightEngine. 
GitHub
+1