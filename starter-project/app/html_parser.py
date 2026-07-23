#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTML Parser (BeautifulSoup) — централизованный слой обработки HTML.

Единая точка входа для превращения сырого HTML в структурированные Python-
объекты (текст, атрибуты, ссылки, изображения, таблицы, списки, метаданные).

HTML Parser:

* НЕ выполняет HTTP-запросов, НЕ открывает браузер, НЕ скроллит и НЕ кликает
  (этим занимаются RequestsEngine/PlaywrightEngine — см. app/requests_engine.py,
  app/playwright_engine.py);
* НЕ содержит селекторов конкретных сайтов (это ответственность модулей
  вроде app/parser.py, которые используют этот компонент как инструмент);
* НЕ экспортирует данные (этим занимается будущий Export layer);
* никогда не бросает исключение из-за отсутствующего элемента, невалидного
  HTML или "битой" разметки — все ошибки безопасно логируются через
  `app.utils.log_message()`, а вызывающему коду возвращается безопасное
  значение по умолчанию (None / "" / [] / {}).

Использование (пример):

    from app.html_parser import HtmlParser

    soup = HtmlParser.parse(html)
    card = HtmlParser.select_one(soup, "div.product-card")
    title = HtmlParser.get_text(HtmlParser.select_one(card, "h4"))
    price_attr = HtmlParser.get_attr(card, "data-price")
"""

from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import Tag

from app.config import HTML_PARSER_BACKEND
from app.data_normalizer import DataNormalizer
from app.utils import log_message

# Тип элемента, с которым может работать большинство методов: либо целый
# "суп" документа, либо отдельный тег внутри него. Оба поддерживают
# одинаковый API BeautifulSoup (find/find_all/select/select_one/get_text).
SoupOrTag = Union[BeautifulSoup, Tag]


class HtmlParser:
    """
    Централизованный, не хранящий состояния (stateless) помощник для
    безопасной работы с HTML через BeautifulSoup.

    Все методы — статические, ничего не знают о конкретном сайте и никогда
    не бросают исключения наружу: любая ошибка парсинга логируется и
    заменяется безопасным значением по умолчанию, чтобы не прерывать
    обработку остальных элементов/страниц.
    """

    # =====================================================================
    # СОЗДАНИЕ SOUP-ОБЪЕКТА
    # =====================================================================

    @staticmethod
    def parse(html: Optional[str], backend: Optional[str] = None) -> Optional[BeautifulSoup]:
        """
        Безопасно создает объект BeautifulSoup из сырого HTML.

        Args:
            html (Optional[str]): Сырой HTML-код страницы/фрагмента.
            backend (Optional[str]): Парсер-бэкенд BeautifulSoup
                ("html.parser", "lxml", "html5lib"). Если не передан —
                используется `app.config.HTML_PARSER_BACKEND`.

        Returns:
            Optional[BeautifulSoup]: Объект supа, либо None, если HTML
                пустой/невалидный (ошибка логируется, исключение не бросается).
        """
        if not html or not isinstance(html, str) or not html.strip():
            log_message("warning", f"[{__file__}] Пустой или некорректный HTML передан в HtmlParser.parse()")
            return None

        active_backend = backend or HTML_PARSER_BACKEND
        try:
            return BeautifulSoup(html, active_backend)
        except Exception as e:
            log_message("error", f"[{__file__}] Ошибка при парсинге HTML (backend={active_backend}): {e}")
            # Фолбэк на встроенный html.parser, если, например, lxml не установлен.
            if active_backend != "html.parser":
                try:
                    return BeautifulSoup(html, "html.parser")
                except Exception as fallback_error:
                    log_message("error", f"[{__file__}] Фолбэк-парсинг также не удался: {fallback_error}")
            return None

    # =====================================================================
    # ПОИСК ЭЛЕМЕНТОВ (CSS-СЕЛЕКТОРЫ)
    # =====================================================================

    @staticmethod
    def select_one(scope: Optional[SoupOrTag], css_selector: str) -> Optional[Tag]:
        """
        Безопасно находит первый элемент по CSS-селектору.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            css_selector (str): CSS-селектор (например, "div.card > h4").

        Returns:
            Optional[Tag]: Найденный элемент либо None.
        """
        if scope is None:
            return None
        try:
            return scope.select_one(css_selector)
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка CSS-селектора '{css_selector}': {e}")
            return None

    @staticmethod
    def select_all(scope: Optional[SoupOrTag], css_selector: str) -> List[Tag]:
        """
        Безопасно находит все элементы по CSS-селектору.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            css_selector (str): CSS-селектор.

        Returns:
            List[Tag]: Список найденных элементов (пустой список, если ничего
                не найдено или произошла ошибка).
        """
        if scope is None:
            return []
        try:
            return scope.select(css_selector)
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка CSS-селектора '{css_selector}': {e}")
            return []

    # =====================================================================
    # ПОИСК ЭЛЕМЕНТОВ (ПО ИМЕНИ ТЕГА / АТРИБУТАМ)
    # =====================================================================

    @staticmethod
    def find(
        scope: Optional[SoupOrTag],
        name: Optional[str] = None,
        attrs: Optional[Dict[str, Any]] = None,
        class_: Optional[str] = None,
    ) -> Optional[Tag]:
        """
        Безопасно находит первый тег по имени/атрибутам/классу.

        Поддерживает нестандартные атрибуты с дефисом (например, `data-testid`)
        через словарь `attrs`, что избегает синтаксической ошибки Python при
        попытке передать их именованным аргументом (`data-testid=...` невалидно).

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            name (Optional[str]): Имя HTML-тега (например, "div", "h4").
            attrs (Optional[Dict[str, Any]]): Словарь атрибутов для фильтрации.
            class_ (Optional[str]): CSS-класс для фильтрации.

        Returns:
            Optional[Tag]: Найденный элемент либо None.
        """
        if scope is None:
            return None
        try:
            kwargs: Dict[str, Any] = {}
            if class_ is not None:
                kwargs["class_"] = class_
            return scope.find(name, attrs=attrs or {}, **kwargs)
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка поиска тега '{name}': {e}")
            return None

    @staticmethod
    def find_all(
        scope: Optional[SoupOrTag],
        name: Optional[str] = None,
        attrs: Optional[Dict[str, Any]] = None,
        class_: Optional[str] = None,
    ) -> List[Tag]:
        """
        Безопасно находит все теги по имени/атрибутам/классу.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            name (Optional[str]): Имя HTML-тега.
            attrs (Optional[Dict[str, Any]]): Словарь атрибутов для фильтрации.
            class_ (Optional[str]): CSS-класс для фильтрации.

        Returns:
            List[Tag]: Список найденных элементов (пустой список при отсутствии
                совпадений или ошибке).
        """
        if scope is None:
            return []
        try:
            kwargs: Dict[str, Any] = {}
            if class_ is not None:
                kwargs["class_"] = class_
            return scope.find_all(name, attrs=attrs or {}, **kwargs)
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка поиска тегов '{name}': {e}")
            return []

    # =====================================================================
    # БЕЗОПАСНАЯ ЭКСТРАКЦИЯ ТЕКСТА И АТРИБУТОВ
    # =====================================================================

    @staticmethod
    def normalize_text(text: Optional[str]) -> str:
        """
        Нормализует извлеченный текст: декодирует HTML-сущности, сворачивает
        повторяющиеся пробелы/переносы строк в один пробел и обрезает края.

        Делегирует к централизованному `DataNormalizer.normalize_string()`
        (Data Normalization, Milestone 5), чтобы логика очистки текста жила
        в одном месте, а не дублировалась здесь и в других парсерах —
        HTML Parser остаётся тонким слоем извлечения данных из разметки.

        Args:
            text (Optional[str]): Сырой текст.

        Returns:
            str: Нормализованный текст ("" для None/пустой строки).
        """
        return DataNormalizer.normalize_string(text)

    @classmethod
    def get_text(cls, element: Optional[Tag], default: str = "") -> str:
        """
        Безопасно извлекает и нормализует текст элемента.

        Args:
            element (Optional[Tag]): Элемент (может быть None).
            default (str): Значение, возвращаемое при отсутствии элемента
                или ошибке извлечения.

        Returns:
            str: Нормализованный текст либо `default`.
        """
        if element is None:
            return default
        try:
            raw_text = element.get_text(separator=" ", strip=True)
            normalized = cls.normalize_text(raw_text)
            return normalized if normalized else default
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка извлечения текста: {e}")
            return default

    @staticmethod
    def get_attr(element: Optional[Tag], attr_name: str, default: str = "") -> str:
        """
        Безопасно извлекает значение атрибута тега (href, src, alt, title,
        value, data-*, ...).

        Args:
            element (Optional[Tag]): Элемент (может быть None).
            attr_name (str): Имя атрибута.
            default (str): Значение по умолчанию, если атрибут отсутствует.

        Returns:
            str: Значение атрибута либо `default`. Если атрибут — список
                (например, `class`), элементы объединяются пробелом.
        """
        if element is None:
            return default
        try:
            value = element.get(attr_name, default)
            if isinstance(value, list):
                return " ".join(value)
            return value if value is not None else default
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка извлечения атрибута '{attr_name}': {e}")
            return default

    # =====================================================================
    # ИЗВЛЕЧЕНИЕ ТИПОВЫХ СТРУКТУР
    # =====================================================================

    @classmethod
    def get_links(cls, scope: Optional[SoupOrTag], selector: str = "a") -> List[Dict[str, str]]:
        """
        Извлекает все ссылки внутри `scope`.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            selector (str): CSS-селектор тегов ссылок (по умолчанию "a").

        Returns:
            List[Dict[str, str]]: Список словарей {"href": str, "text": str}.
        """
        links = []
        for tag in cls.select_all(scope, selector):
            links.append({
                "href": cls.get_attr(tag, "href"),
                "text": cls.get_text(tag),
            })
        return links

    @classmethod
    def get_images(cls, scope: Optional[SoupOrTag], selector: str = "img") -> List[Dict[str, str]]:
        """
        Извлекает все изображения внутри `scope`.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем.
            selector (str): CSS-селектор тегов изображений (по умолчанию "img").

        Returns:
            List[Dict[str, str]]: Список словарей {"src": str, "alt": str}.
        """
        images = []
        for tag in cls.select_all(scope, selector):
            images.append({
                "src": cls.get_attr(tag, "src"),
                "alt": cls.get_attr(tag, "alt"),
            })
        return images

    @classmethod
    def get_table(cls, table_element: Optional[Tag]) -> List[List[str]]:
        """
        Извлекает содержимое HTML-таблицы построчно.

        Args:
            table_element (Optional[Tag]): Элемент `<table>` (может быть None).

        Returns:
            List[List[str]]: Список строк, каждая строка — список
                нормализованного текста ячеек (`th`/`td`). Пустой список,
                если таблица не передана/невалидна.
        """
        if table_element is None:
            return []
        try:
            rows = []
            for row in table_element.find_all("tr"):
                cells = row.find_all(["th", "td"])
                if not cells:
                    continue
                rows.append([cls.get_text(cell) for cell in cells])
            return rows
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка извлечения таблицы: {e}")
            return []

    @classmethod
    def get_list_items(cls, scope: Optional[SoupOrTag], selector: str = "li") -> List[str]:
        """
        Извлекает нормализованный текст всех элементов списка.

        Args:
            scope (Optional[SoupOrTag]): Suop или тег, внутри которого ищем
                (например, `<ul>`/`<ol>`).
            selector (str): CSS-селектор элементов списка (по умолчанию "li").

        Returns:
            List[str]: Список нормализованных текстовых значений.
        """
        return [cls.get_text(tag) for tag in cls.select_all(scope, selector)]

    @classmethod
    def get_metadata(cls, soup: Optional[SoupOrTag]) -> Dict[str, str]:
        """
        Извлекает базовые метаданные документа: заголовок страницы и все
        теги `<meta>` с атрибутом `name` или `property` (включая OpenGraph:
        `og:title`, `og:description`, и т.д.).

        Args:
            soup (Optional[SoupOrTag]): Объект supа всего документа.

        Returns:
            Dict[str, str]: Словарь метаданных, например
                {"title": "...", "description": "...", "og:title": "..."}.
        """
        if soup is None:
            return {}

        metadata: Dict[str, str] = {}
        try:
            title_tag = cls.find(soup, "title")
            if title_tag:
                metadata["title"] = cls.get_text(title_tag)

            for meta_tag in cls.find_all(soup, "meta"):
                key = cls.get_attr(meta_tag, "name") or cls.get_attr(meta_tag, "property")
                content = cls.get_attr(meta_tag, "content")
                if key and content:
                    metadata[key] = content
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка извлечения метаданных: {e}")

        return metadata


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    sample_html = """
    <html>
      <head>
        <title>Тестовая страница</title>
        <meta name="description" content="Пример  описания   с пробелами">
        <meta property="og:title" content="OG Заголовок">
      </head>
      <body>
        <div class="card" data-id="42">
          <h4 class="title">  Продам   ВАЗ 2104  </h4>
          <p data-testid="ad-price">1&nbsp;500 грн</p>
          <a href="/item/42">Подробнее</a>
          <img src="/img/42.jpg" alt="Фото авто">
          <ul>
            <li>Бензин</li>
            <li>2004 год</li>
          </ul>
          <table>
            <tr><th>Параметр</th><th>Значение</th></tr>
            <tr><td>Пробег</td><td>150000 км</td></tr>
          </table>
        </div>
      </body>
    </html>
    """

    soup = HtmlParser.parse(sample_html)
    card = HtmlParser.select_one(soup, "div.card")

    print(f"[{__file__}] Заголовок карточки: {HtmlParser.get_text(HtmlParser.select_one(card, 'h4'))}")
    print(f"[{__file__}] data-id: {HtmlParser.get_attr(card, 'data-id')}")
    print(f"[{__file__}] Цена (raw text): {HtmlParser.get_text(HtmlParser.find(card, 'p', attrs={'data-testid': 'ad-price'}))}")
    print(f"[{__file__}] Ссылки: {HtmlParser.get_links(card)}")
    print(f"[{__file__}] Изображения: {HtmlParser.get_images(card)}")
    print(f"[{__file__}] Список: {HtmlParser.get_list_items(card)}")
    print(f"[{__file__}] Таблица: {HtmlParser.get_table(HtmlParser.select_one(card, 'table'))}")
    print(f"[{__file__}] Метаданные документа: {HtmlParser.get_metadata(soup)}")
    print(f"[{__file__}] Пустой HTML -> parse(): {HtmlParser.parse('')}")
