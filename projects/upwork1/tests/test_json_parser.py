#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для JSON Parser (app/json_parser.py).

Все тесты используют статические JSON-строки/объекты — без сети,
так как JsonParser чисто вычислительный (JSON-строка/объект -> данные).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.json_parser import JsonParser


SAMPLE_JSON = """
{
    "product": {
        "id": 42,
        "title": "Тестовый товар",
        "price": {"amount": 1299.99, "currency": "USD"},
        "in_stock": true,
        "tags": ["новинка", "скидка"],
        "images": [
            {"url": "/img/1.jpg"},
            {"url": "/img/2.jpg"}
        ],
        "description": null,
        "count": 0
    }
}
"""


class TestParse(unittest.TestCase):
    """Тесты парсинга и валидации JSON."""

    def test_parse_valid_object(self):
        data = JsonParser.parse(SAMPLE_JSON)
        self.assertIsInstance(data, dict)

    def test_parse_valid_array(self):
        data = JsonParser.parse("[1, 2, 3]")
        self.assertEqual(data, [1, 2, 3])

    def test_parse_none_returns_none(self):
        self.assertIsNone(JsonParser.parse(None))

    def test_parse_non_string_returns_none(self):
        self.assertIsNone(JsonParser.parse(12345))

    def test_parse_empty_string_returns_none(self):
        self.assertIsNone(JsonParser.parse(""))

    def test_parse_whitespace_only_returns_none(self):
        self.assertIsNone(JsonParser.parse("   \n\t  "))

    def test_parse_invalid_json_returns_none(self):
        self.assertIsNone(JsonParser.parse("{invalid json,,,"))

    def test_parse_malformed_trailing_comma_returns_none(self):
        self.assertIsNone(JsonParser.parse('{"a": 1,}'))

    def test_parse_does_not_raise_on_garbage(self):
        # Совершенно не-JSON контент (например, HTML ошибки сервера)
        garbage = "<html><body>500 Internal Server Error</body></html>"
        self.assertIsNone(JsonParser.parse(garbage))

    def test_is_valid_true_for_valid_json(self):
        self.assertTrue(JsonParser.is_valid('{"a": 1}'))

    def test_is_valid_false_for_invalid_json(self):
        self.assertFalse(JsonParser.is_valid("{invalid"))

    def test_is_valid_false_for_empty_string(self):
        self.assertFalse(JsonParser.is_valid(""))

    def test_is_valid_false_for_none(self):
        self.assertFalse(JsonParser.is_valid(None))


class TestPathResolution(unittest.TestCase):
    """Тесты разбора путей и has_path()/get()."""

    def setUp(self):
        self.data = JsonParser.parse(SAMPLE_JSON)

    def test_has_path_existing_nested_key(self):
        self.assertTrue(JsonParser.has_path(self.data, "product.title"))

    def test_has_path_existing_array_index(self):
        self.assertTrue(JsonParser.has_path(self.data, "product.tags[0]"))

    def test_has_path_missing_key(self):
        self.assertFalse(JsonParser.has_path(self.data, "product.missing_field"))

    def test_has_path_out_of_range_index(self):
        self.assertFalse(JsonParser.has_path(self.data, "product.tags[99]"))

    def test_has_path_null_value_is_still_found(self):
        # null считается "найденным" путем (в отличие от отсутствующего ключа).
        self.assertTrue(JsonParser.has_path(self.data, "product.description"))

    def test_get_with_dotted_string_path(self):
        self.assertEqual(JsonParser.get(self.data, "product.title"), "Тестовый товар")

    def test_get_with_list_path(self):
        self.assertEqual(JsonParser.get(self.data, ["product", "title"]), "Тестовый товар")

    def test_get_with_nested_array_object_path(self):
        self.assertEqual(JsonParser.get(self.data, "product.images[1].url"), "/img/2.jpg")

    def test_get_empty_path_returns_root(self):
        self.assertEqual(JsonParser.get(self.data, ""), self.data)

    def test_get_missing_path_returns_default(self):
        self.assertEqual(JsonParser.get(self.data, "product.missing", default="N/A"), "N/A")

    def test_get_negative_index_supported(self):
        self.assertEqual(JsonParser.get(self.data, "product.tags[-1]" if False else ["product", "tags", -1]), "скидка")

    def test_get_none_data_returns_default(self):
        self.assertEqual(JsonParser.get(None, "any.path", default="fallback"), "fallback")

    def test_get_unsupported_path_type_returns_default(self):
        # Путь как int/float — не строка и не список/тюпл.
        self.assertEqual(JsonParser.get(self.data, 123, default="fallback"), "fallback")


class TestSafeGetters(unittest.TestCase):
    """Тесты типизированных геттеров (get_string/get_int/get_float/get_bool/get_list/get_dict)."""

    def setUp(self):
        self.data = JsonParser.parse(SAMPLE_JSON)

    def test_get_string_correct_type(self):
        self.assertEqual(JsonParser.get_string(self.data, "product.title"), "Тестовый товар")

    def test_get_string_missing_returns_default(self):
        self.assertEqual(JsonParser.get_string(self.data, "product.missing"), "")
        self.assertEqual(JsonParser.get_string(self.data, "product.missing", default="N/A"), "N/A")

    def test_get_string_wrong_type_returns_default(self):
        # price — это dict, не строка.
        self.assertEqual(JsonParser.get_string(self.data, "product.price", default="N/A"), "N/A")

    def test_get_string_null_returns_default(self):
        self.assertEqual(JsonParser.get_string(self.data, "product.description", default="нет описания"), "нет описания")

    def test_get_int_correct_type(self):
        self.assertEqual(JsonParser.get_int(self.data, "product.id"), 42)

    def test_get_int_zero_value(self):
        # Проверка, что валидный 0 не подменяется дефолтом.
        self.assertEqual(JsonParser.get_int(self.data, "product.count", default=-1), 0)

    def test_get_int_bool_is_rejected(self):
        # bool - подкласс int в Python, но семантически это не число.
        self.assertEqual(JsonParser.get_int(self.data, "product.in_stock", default=-1), -1)

    def test_get_int_wrong_type_returns_default(self):
        self.assertEqual(JsonParser.get_int(self.data, "product.title", default=-1), -1)

    def test_get_float_from_float_value(self):
        self.assertEqual(JsonParser.get_float(self.data, "product.price.amount"), 1299.99)

    def test_get_float_from_int_value(self):
        # int значения тоже допустимы для get_float (JSON не различает их).
        self.assertEqual(JsonParser.get_float(self.data, "product.id"), 42.0)
        self.assertIsInstance(JsonParser.get_float(self.data, "product.id"), float)

    def test_get_float_bool_is_rejected(self):
        self.assertEqual(JsonParser.get_float(self.data, "product.in_stock", default=-1.0), -1.0)

    def test_get_float_wrong_type_returns_default(self):
        self.assertEqual(JsonParser.get_float(self.data, "product.title", default=-1.0), -1.0)

    def test_get_bool_correct_type(self):
        self.assertTrue(JsonParser.get_bool(self.data, "product.in_stock"))

    def test_get_bool_missing_returns_default(self):
        self.assertFalse(JsonParser.get_bool(self.data, "product.missing"))
        self.assertTrue(JsonParser.get_bool(self.data, "product.missing", default=True))

    def test_get_bool_wrong_type_returns_default(self):
        self.assertFalse(JsonParser.get_bool(self.data, "product.id", default=False))

    def test_get_list_correct_type(self):
        self.assertEqual(JsonParser.get_list(self.data, "product.tags"), ["новинка", "скидка"])

    def test_get_list_missing_returns_empty_list(self):
        self.assertEqual(JsonParser.get_list(self.data, "product.missing"), [])

    def test_get_list_wrong_type_returns_default(self):
        self.assertEqual(JsonParser.get_list(self.data, "product.title"), [])

    def test_get_dict_correct_type(self):
        self.assertEqual(JsonParser.get_dict(self.data, "product.price"), {"amount": 1299.99, "currency": "USD"})

    def test_get_dict_missing_returns_empty_dict(self):
        self.assertEqual(JsonParser.get_dict(self.data, "product.missing"), {})

    def test_get_dict_wrong_type_returns_default(self):
        self.assertEqual(JsonParser.get_dict(self.data, "product.tags"), {})


class TestRobustness(unittest.TestCase):
    """Тесты устойчивости: парсер никогда не должен бросать исключение наружу."""

    def test_deeply_nested_missing_path_does_not_raise(self):
        data = JsonParser.parse('{"a": {"b": {"c": 1}}}')
        result = JsonParser.get_string(data, "a.b.c.d.e.f.g", default="safe")
        self.assertEqual(result, "safe")

    def test_index_into_non_list_does_not_raise(self):
        data = JsonParser.parse('{"a": "not a list"}')
        result = JsonParser.get(data, ["a", 0], default="safe")
        self.assertEqual(result, "safe")

    def test_key_into_non_dict_does_not_raise(self):
        data = JsonParser.parse('{"a": [1, 2, 3]}')
        result = JsonParser.get(data, "a.b.c", default="safe")
        self.assertEqual(result, "safe")

    def test_operations_on_none_data_do_not_raise(self):
        self.assertEqual(JsonParser.get_string(None, "a.b.c"), "")
        self.assertEqual(JsonParser.get_int(None, "a.b.c"), 0)
        self.assertEqual(JsonParser.get_float(None, "a.b.c"), 0.0)
        self.assertFalse(JsonParser.get_bool(None, "a.b.c"))
        self.assertEqual(JsonParser.get_list(None, "a.b.c"), [])
        self.assertEqual(JsonParser.get_dict(None, "a.b.c"), {})
        self.assertFalse(JsonParser.has_path(None, "a.b.c"))

    def test_empty_object_and_array_are_handled(self):
        data = JsonParser.parse('{"items": [], "meta": {}}')
        self.assertEqual(JsonParser.get_list(data, "items"), [])
        self.assertEqual(JsonParser.get_dict(data, "meta"), {})

    def test_top_level_array_with_path_indexing(self):
        data = JsonParser.parse('[{"name": "a"}, {"name": "b"}]')
        self.assertEqual(JsonParser.get_string(data, "[1].name"), "b")

    def test_top_level_primitive_with_empty_path(self):
        data = JsonParser.parse("42")
        self.assertEqual(JsonParser.get(data, ""), 42)


if __name__ == "__main__":
    unittest.main()
