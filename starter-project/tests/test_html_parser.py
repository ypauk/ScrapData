#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для HTML Parser (app/html_parser.py).

Все тесты используют статические HTML-фрагменты — без сети/браузера,
так как HtmlParser чисто вычислительный (HTML-строка -> структура данных).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.html_parser import HtmlParser


SAMPLE_HTML = """
<html>
  <head>
    <title>Тестовая страница</title>
    <meta name="description" content="Пример  описания   с пробелами">
    <meta property="og:title" content="OG Заголовок">
  </head>
  <body>
    <div class="card" data-id="42" data-testid="card-42">
      <h4 class="title">  Продам   ВАЗ 2104  </h4>
      <p data-testid="ad-price">1&nbsp;500 грн</p>
      <a href="/item/42">Подробнее</a>
      <a href="/item/43">Другое объявление</a>
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


class TestParse(unittest.TestCase):
    """Тесты создания soup-объекта."""

    def test_parse_valid_html_returns_soup(self):
        soup = HtmlParser.parse(SAMPLE_HTML)
        self.assertIsNotNone(soup)

    def test_parse_empty_string_returns_none(self):
        self.assertIsNone(HtmlParser.parse(""))

    def test_parse_none_returns_none(self):
        self.assertIsNone(HtmlParser.parse(None))

    def test_parse_whitespace_only_returns_none(self):
        self.assertIsNone(HtmlParser.parse("   \n\t  "))

    def test_parse_non_string_returns_none(self):
        self.assertIsNone(HtmlParser.parse(12345))

    def test_parse_malformed_html_does_not_raise(self):
        malformed = "<div><p>Незакрытый тег<div>Другой текст"
        soup = HtmlParser.parse(malformed)
        self.assertIsNotNone(soup)

    def test_parse_with_custom_backend_falls_back_on_error(self):
        # Несуществующий бэкенд должен привести к фолбэку на html.parser,
        # а не бросить исключение наружу.
        soup = HtmlParser.parse(SAMPLE_HTML, backend="nonexistent-backend")
        self.assertIsNotNone(soup)


class TestSelectors(unittest.TestCase):
    """Тесты CSS-селекторов (select_one/select_all)."""

    def setUp(self):
        self.soup = HtmlParser.parse(SAMPLE_HTML)

    def test_select_one_finds_element(self):
        card = HtmlParser.select_one(self.soup, "div.card")
        self.assertIsNotNone(card)

    def test_select_one_missing_returns_none(self):
        self.assertIsNone(HtmlParser.select_one(self.soup, "div.does-not-exist"))

    def test_select_one_none_scope_returns_none(self):
        self.assertIsNone(HtmlParser.select_one(None, "div.card"))

    def test_select_all_finds_multiple(self):
        links = HtmlParser.select_all(self.soup, "a")
        self.assertEqual(len(links), 2)

    def test_select_all_none_scope_returns_empty_list(self):
        self.assertEqual(HtmlParser.select_all(None, "a"), [])

    def test_select_all_no_match_returns_empty_list(self):
        self.assertEqual(HtmlParser.select_all(self.soup, "div.nope"), [])

    def test_invalid_css_selector_does_not_raise(self):
        # Синтаксически некорректный CSS-селектор не должен ронять парсер.
        result = HtmlParser.select_one(self.soup, ":::invalid:::")
        self.assertIsNone(result)


class TestFindByTag(unittest.TestCase):
    """Тесты поиска по имени тега/атрибутам/классу (find/find_all)."""

    def setUp(self):
        self.soup = HtmlParser.parse(SAMPLE_HTML)
        self.card = HtmlParser.select_one(self.soup, "div.card")

    def test_find_by_tag_name(self):
        h4 = HtmlParser.find(self.card, "h4")
        self.assertIsNotNone(h4)

    def test_find_by_class(self):
        h4 = HtmlParser.find(self.card, "h4", class_="title")
        self.assertIsNotNone(h4)

    def test_find_by_hyphenated_data_attribute(self):
        # Воспроизводит баг из AI_OUTPUT/5_debug_answer.md: data-testid не может
        # быть передан как именованный аргумент (data-testid=... невалиден в Python),
        # но безопасно работает через словарь attrs.
        price = HtmlParser.find(self.card, "p", attrs={"data-testid": "ad-price"})
        self.assertIsNotNone(price)

    def test_find_missing_returns_none(self):
        self.assertIsNone(HtmlParser.find(self.card, "span", class_="does-not-exist"))

    def test_find_none_scope_returns_none(self):
        self.assertIsNone(HtmlParser.find(None, "div"))

    def test_find_all_returns_list(self):
        items = HtmlParser.find_all(self.soup, "li")
        self.assertEqual(len(items), 2)

    def test_find_all_none_scope_returns_empty_list(self):
        self.assertEqual(HtmlParser.find_all(None, "li"), [])

    def test_find_all_no_match_returns_empty_list(self):
        self.assertEqual(HtmlParser.find_all(self.card, "span", class_="nope"), [])


class TestTextExtraction(unittest.TestCase):
    """Тесты безопасной экстракции и нормализации текста."""

    def setUp(self):
        self.soup = HtmlParser.parse(SAMPLE_HTML)
        self.card = HtmlParser.select_one(self.soup, "div.card")

    def test_get_text_normalizes_whitespace(self):
        h4 = HtmlParser.find(self.card, "h4")
        text = HtmlParser.get_text(h4)
        self.assertEqual(text, "Продам ВАЗ 2104")

    def test_get_text_decodes_html_entities(self):
        price = HtmlParser.find(self.card, "p", attrs={"data-testid": "ad-price"})
        text = HtmlParser.get_text(price)
        # &nbsp; должен быть декодирован и нормализован в обычный пробел.
        self.assertIn("1", text)
        self.assertIn("500", text)
        self.assertNotIn("\xa0", text)

    def test_get_text_none_element_returns_default(self):
        self.assertEqual(HtmlParser.get_text(None), "")
        self.assertEqual(HtmlParser.get_text(None, default="N/A"), "N/A")

    def test_get_text_empty_element_returns_default(self):
        soup = HtmlParser.parse("<div class='empty'></div>")
        empty_div = HtmlParser.select_one(soup, "div.empty")
        self.assertEqual(HtmlParser.get_text(empty_div, default="fallback"), "fallback")

    def test_normalize_text_collapses_multiple_spaces_and_newlines(self):
        raw = "  Много   \n\n  пробелов\tи\tтабов  "
        normalized = HtmlParser.normalize_text(raw)
        self.assertEqual(normalized, "Много пробелов и табов")

    def test_normalize_text_none_returns_empty_string(self):
        self.assertEqual(HtmlParser.normalize_text(None), "")

    def test_normalize_text_empty_string_returns_empty_string(self):
        self.assertEqual(HtmlParser.normalize_text(""), "")


class TestAttributeExtraction(unittest.TestCase):
    """Тесты безопасной экстракции атрибутов."""

    def setUp(self):
        self.soup = HtmlParser.parse(SAMPLE_HTML)
        self.card = HtmlParser.select_one(self.soup, "div.card")
        self.link = HtmlParser.find(self.card, "a")
        self.img = HtmlParser.find(self.card, "img")

    def test_get_attr_href(self):
        self.assertEqual(HtmlParser.get_attr(self.link, "href"), "/item/42")

    def test_get_attr_src(self):
        self.assertEqual(HtmlParser.get_attr(self.img, "src"), "/img/42.jpg")

    def test_get_attr_alt(self):
        self.assertEqual(HtmlParser.get_attr(self.img, "alt"), "Фото авто")

    def test_get_attr_data_dash_attribute(self):
        self.assertEqual(HtmlParser.get_attr(self.card, "data-id"), "42")

    def test_get_attr_missing_returns_default(self):
        self.assertEqual(HtmlParser.get_attr(self.link, "title"), "")
        self.assertEqual(HtmlParser.get_attr(self.link, "title", default="untitled"), "untitled")

    def test_get_attr_none_element_returns_default(self):
        self.assertEqual(HtmlParser.get_attr(None, "href", default="N/A"), "N/A")

    def test_get_attr_class_list_is_joined(self):
        soup = HtmlParser.parse('<div class="a b c">x</div>')
        div = HtmlParser.select_one(soup, "div")
        self.assertEqual(HtmlParser.get_attr(div, "class"), "a b c")


class TestStructuredExtraction(unittest.TestCase):
    """Тесты извлечения ссылок, изображений, таблиц, списков и метаданных."""

    def setUp(self):
        self.soup = HtmlParser.parse(SAMPLE_HTML)
        self.card = HtmlParser.select_one(self.soup, "div.card")

    def test_get_links(self):
        links = HtmlParser.get_links(self.card)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]["href"], "/item/42")
        self.assertEqual(links[0]["text"], "Подробнее")

    def test_get_links_none_scope_returns_empty_list(self):
        self.assertEqual(HtmlParser.get_links(None), [])

    def test_get_images(self):
        images = HtmlParser.get_images(self.card)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["src"], "/img/42.jpg")
        self.assertEqual(images[0]["alt"], "Фото авто")

    def test_get_list_items(self):
        items = HtmlParser.get_list_items(self.card)
        self.assertEqual(items, ["Бензин", "2004 год"])

    def test_get_list_items_missing_list_returns_empty(self):
        soup = HtmlParser.parse("<div class='no-list'></div>")
        scope = HtmlParser.select_one(soup, "div.no-list")
        self.assertEqual(HtmlParser.get_list_items(scope), [])

    def test_get_table(self):
        table = HtmlParser.select_one(self.card, "table")
        rows = HtmlParser.get_table(table)
        self.assertEqual(rows, [["Параметр", "Значение"], ["Пробег", "150000 км"]])

    def test_get_table_none_returns_empty_list(self):
        self.assertEqual(HtmlParser.get_table(None), [])

    def test_get_table_missing_table_returns_empty(self):
        soup = HtmlParser.parse("<div>no table here</div>")
        div = HtmlParser.select_one(soup, "div")
        self.assertEqual(HtmlParser.get_table(div), [])

    def test_get_metadata(self):
        metadata = HtmlParser.get_metadata(self.soup)
        self.assertEqual(metadata.get("title"), "Тестовая страница")
        self.assertIn("Пример", metadata.get("description", ""))
        self.assertEqual(metadata.get("og:title"), "OG Заголовок")

    def test_get_metadata_none_soup_returns_empty_dict(self):
        self.assertEqual(HtmlParser.get_metadata(None), {})

    def test_get_metadata_no_meta_tags_returns_partial_dict(self):
        soup = HtmlParser.parse("<html><head><title>Only Title</title></head></html>")
        metadata = HtmlParser.get_metadata(soup)
        self.assertEqual(metadata, {"title": "Only Title"})


class TestRobustness(unittest.TestCase):
    """Тесты устойчивости: парсер никогда не должен бросать исключение наружу."""

    def test_missing_nested_elements_chain_does_not_raise(self):
        # Цепочка поиска несуществующих вложенных элементов должна безопасно
        # возвращать None/[] на каждом шаге, а не бросать AttributeError.
        soup = HtmlParser.parse("<div>just text</div>")
        missing = HtmlParser.select_one(soup, "div.a")
        deeper_missing = HtmlParser.find(missing, "span")
        text = HtmlParser.get_text(deeper_missing, default="safe")
        self.assertEqual(text, "safe")

    def test_completely_broken_markup_does_not_raise(self):
        broken = "<<<>>>not even html###"
        soup = HtmlParser.parse(broken)
        # Не важно, что вернет BeautifulSoup — важно, что не было исключения.
        self.assertTrue(soup is None or soup is not None)


if __name__ == "__main__":
    unittest.main()
