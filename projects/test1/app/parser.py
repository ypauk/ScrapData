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