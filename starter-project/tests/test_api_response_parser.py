#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для API Response Parser (app/api_response_parser.py).

Все тесты используют статические словари/списки в памяти (уже
"разобранный" JSON) — без сети и без зависимости от JsonParser.parse(),
так как ApiResponseParser работает с уже распарсенными объектами.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api_response_parser import ApiResponseParser, PaginationMetadata


class TestExtractRecords(unittest.TestCase):
    """Тесты извлечения коллекции записей (extract_records)."""

    def test_top_level_list_response(self):
        response = [{"id": 1}, {"id": 2}]
        self.assertEqual(ApiResponseParser.extract_records(response), response)

    def test_data_key_wrapper(self):
        response = {"data": [{"id": 1}, {"id": 2}]}
        self.assertEqual(ApiResponseParser.extract_records(response), [{"id": 1}, {"id": 2}])

    def test_results_key_wrapper(self):
        response = {"results": [{"id": 1}]}
        self.assertEqual(ApiResponseParser.extract_records(response), [{"id": 1}])

    def test_items_key_wrapper(self):
        response = {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}
        self.assertEqual(len(ApiResponseParser.extract_records(response)), 3)

    def test_records_key_wrapper(self):
        response = {"records": [{"id": 1}]}
        self.assertEqual(ApiResponseParser.extract_records(response), [{"id": 1}])

    def test_products_key_wrapper(self):
        response = {"products": [{"id": 1}, {"id": 2}]}
        self.assertEqual(len(ApiResponseParser.extract_records(response)), 2)

    def test_payload_key_wrapper(self):
        response = {"payload": [{"id": 1}]}
        self.assertEqual(ApiResponseParser.extract_records(response), [{"id": 1}])

    def test_nested_data_wrapper(self):
        # Часто встречается двойная обертка: {"data": {"results": [...]}}
        response = {"data": {"results": [{"id": 1}, {"id": 2}]}}
        self.assertEqual(len(ApiResponseParser.extract_records(response)), 2)

    def test_priority_order_data_before_results(self):
        # Если одновременно есть "data" и "results" на одном уровне,
        # приоритет у "data" (первый в DEFAULT_LIST_KEYS).
        response = {"data": [{"id": "from_data"}], "results": [{"id": "from_results"}]}
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [{"id": "from_data"}])

    def test_custom_list_keys_override(self):
        response = {"my_custom_key": [{"id": 1}]}
        result = ApiResponseParser.extract_records(response, list_keys=["my_custom_key"])
        self.assertEqual(result, [{"id": 1}])

    def test_graphql_edges_node_unwrapped(self):
        response = {
            "data": {
                "products": {
                    "edges": [
                        {"node": {"id": "1", "title": "A"}},
                        {"node": {"id": "2", "title": "B"}},
                    ]
                }
            }
        }
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [{"id": "1", "title": "A"}, {"id": "2", "title": "B"}])

    def test_top_level_edges_list(self):
        response = [{"node": {"id": "1"}}, {"node": {"id": "2"}}]
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [{"id": "1"}, {"id": "2"}])

    def test_missing_collection_returns_empty_list(self):
        response = {"unrelated_key": "value"}
        self.assertEqual(ApiResponseParser.extract_records(response), [])

    def test_empty_dict_returns_empty_list(self):
        self.assertEqual(ApiResponseParser.extract_records({}), [])

    def test_none_response_returns_empty_list(self):
        self.assertEqual(ApiResponseParser.extract_records(None), [])

    def test_unsupported_type_returns_empty_list(self):
        self.assertEqual(ApiResponseParser.extract_records("just a string"), [])
        self.assertEqual(ApiResponseParser.extract_records(12345), [])

    def test_single_object_found_wrapped_as_list(self):
        # Если по ключу "data" найден одиночный dict (не список), он
        # оборачивается в список из одного элемента (нормализация).
        response = {"data": {"id": 1, "name": "Solo"}}
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [{"id": 1, "name": "Solo"}])

    def test_empty_list_collection_stays_empty(self):
        response = {"data": []}
        self.assertEqual(ApiResponseParser.extract_records(response), [])


class TestExtractSingle(unittest.TestCase):
    """Тесты извлечения одиночного объекта (extract_single)."""

    def test_data_key_wrapper(self):
        response = {"data": {"id": 42, "name": "Item"}}
        self.assertEqual(ApiResponseParser.extract_single(response), {"id": 42, "name": "Item"})

    def test_result_key_wrapper(self):
        response = {"result": {"id": 1}}
        self.assertEqual(ApiResponseParser.extract_single(response), {"id": 1})

    def test_flat_object_without_wrapper(self):
        # "Плоский" ответ без обёртки — сам response является объектом.
        response = {"id": 42, "name": "Flat item"}
        self.assertEqual(ApiResponseParser.extract_single(response), response)

    def test_graphql_data_node_pattern(self):
        response = {"data": {"node": {"id": "1", "title": "GraphQL item"}}}
        self.assertEqual(ApiResponseParser.extract_single(response), {"id": "1", "title": "GraphQL item"})

    def test_custom_object_keys_override(self):
        response = {"my_object": {"id": 1}}
        result = ApiResponseParser.extract_single(response, object_keys=["my_object"])
        self.assertEqual(result, {"id": 1})

    def test_none_response_returns_none(self):
        self.assertIsNone(ApiResponseParser.extract_single(None))

    def test_list_response_returns_none(self):
        self.assertIsNone(ApiResponseParser.extract_single([{"id": 1}]))

    def test_response_with_collection_key_but_no_object_returns_none(self):
        # response содержит коллекцию (data -> list), а не объект,
        # и не является "плоским" (уже содержит служебный ключ) -> None.
        response = {"data": [{"id": 1}, {"id": 2}]}
        self.assertIsNone(ApiResponseParser.extract_single(response))

    def test_empty_dict_returns_itself_as_flat_object(self):
        # Пустой dict не содержит служебных ключей -> считается "плоским" объектом.
        self.assertEqual(ApiResponseParser.extract_single({}), {})


class TestExtractPagination(unittest.TestCase):
    """Тесты извлечения метаданных пагинации (extract_pagination)."""

    def test_pagination_in_meta_container(self):
        response = {
            "data": [],
            "meta": {
                "current_page": 2,
                "total_pages": 10,
                "total_items": 100,
                "page_size": 10,
                "has_next": True,
            },
        }
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 2)
        self.assertEqual(pagination.total_pages, 10)
        self.assertEqual(pagination.total_items, 100)
        self.assertEqual(pagination.page_size, 10)
        self.assertTrue(pagination.has_next)

    def test_pagination_in_pagination_container(self):
        response = {"pagination": {"current_page": 1, "total_pages": 3}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 1)
        self.assertEqual(pagination.total_pages, 3)

    def test_pagination_camel_case_page_info(self):
        response = {
            "data": {
                "products": {
                    "pageInfo": {"hasNextPage": True, "endCursor": "abc123"},
                }
            }
        }
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertTrue(pagination.has_next)
        self.assertEqual(pagination.cursor, "abc123")

    def test_pagination_in_root_without_container(self):
        response = {"page": 3, "total": 50, "has_more": False}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 3)
        self.assertEqual(pagination.total_items, 50)
        self.assertFalse(pagination.has_next)

    def test_pagination_camel_case_variants(self):
        response = {"meta": {"currentPage": 5, "totalPages": 20, "totalItems": 200, "pageSize": 10}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 5)
        self.assertEqual(pagination.total_pages, 20)
        self.assertEqual(pagination.total_items, 200)
        self.assertEqual(pagination.page_size, 10)

    def test_pagination_next_page_field(self):
        response = {"meta": {"next_page": 4}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.next_page, 4)

    def test_pagination_string_numeric_value_converted(self):
        # Некоторые API отдают номера страниц как строки ("2" вместо 2).
        response = {"meta": {"current_page": "2"}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 2)

    def test_pagination_missing_fields_stay_none(self):
        response = {"data": [{"id": 1}]}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertIsNone(pagination.current_page)
        self.assertIsNone(pagination.next_page)
        self.assertIsNone(pagination.total_pages)
        self.assertIsNone(pagination.total_items)
        self.assertIsNone(pagination.cursor)
        self.assertIsNone(pagination.has_next)

    def test_pagination_bool_not_confused_with_int(self):
        # has_next=True (bool) не должно быть спутано с числовым полем.
        response = {"meta": {"has_next": True, "current_page": 1}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 1)
        self.assertTrue(pagination.has_next)

    def test_non_dict_response_returns_empty_metadata(self):
        pagination = ApiResponseParser.extract_pagination([1, 2, 3])
        self.assertEqual(pagination, PaginationMetadata())

    def test_none_response_returns_empty_metadata(self):
        pagination = ApiResponseParser.extract_pagination(None)
        self.assertEqual(pagination, PaginationMetadata())

    def test_meta_container_prioritized_over_root(self):
        # Если поле есть и в meta, и в корне, приоритет у meta (container-first).
        response = {"current_page": 999, "meta": {"current_page": 1}}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination.current_page, 1)


class TestRobustness(unittest.TestCase):
    """Тесты устойчивости: компонент никогда не должен бросать исключение."""

    def test_deeply_nested_response_does_not_raise(self):
        nested = {"a": {"b": {"c": {"d": {"e": {"data": [{"id": 1}]}}}}}}
        # Глубина превышает _MAX_SEARCH_DEPTH — должен вернуть [] без исключения.
        result = ApiResponseParser.extract_records(nested)
        self.assertIsInstance(result, list)

    def test_circular_like_structure_does_not_raise(self):
        # Не настоящая циклическая ссылка (это привело бы к бесконечной
        # рекурсии в любом обходчике), но проверяем устойчивость на
        # структуре с повторяющимися одноуровневыми словарями.
        response = {"a": {"b": {}}, "c": {"d": {}}}
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [])

    def test_malformed_edges_without_node_key(self):
        response = {"data": {"edges": [{"not_node": 1}, {"not_node": 2}]}}
        result = ApiResponseParser.extract_records(response)
        # Элементы без "node" возвращаются как есть, не бросая исключение.
        self.assertEqual(result, [{"not_node": 1}, {"not_node": 2}])

    def test_extract_records_with_list_and_non_dict_items(self):
        response = [1, 2, "three", None]
        result = ApiResponseParser.extract_records(response)
        self.assertEqual(result, [1, 2, "three", None])

    def test_extract_single_with_malformed_data(self):
        response = {"data": "not a dict or list"}
        result = ApiResponseParser.extract_single(response)
        self.assertIsNone(result)

    def test_pagination_with_malformed_meta(self):
        response = {"meta": "not a dict"}
        pagination = ApiResponseParser.extract_pagination(response)
        self.assertEqual(pagination, PaginationMetadata())


if __name__ == "__main__":
    unittest.main()
