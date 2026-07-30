#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для Data Validation (app/data_validator.py).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data_validator import DataValidator, FieldRule, FieldType, ValidationResult


class TestRequiredFields(unittest.TestCase):
    """Тесты обязательности полей / отсутствующих значений."""

    def test_missing_required_field_is_error(self):
        rules = [FieldRule("title", FieldType.STRING, required=True)]
        result = DataValidator.validate_record({}, rules)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("отсутствует" in e for e in result.errors))

    def test_missing_optional_field_is_warning_not_error(self):
        rules = [FieldRule("description", FieldType.STRING, required=False)]
        result = DataValidator.validate_record({}, rules)
        self.assertTrue(result.is_valid)
        self.assertTrue(len(result.warnings) >= 1)

    def test_none_value_treated_as_missing(self):
        rules = [FieldRule("title", FieldType.STRING, required=True)]
        result = DataValidator.validate_record({"title": None}, rules)
        self.assertFalse(result.is_valid)

    def test_empty_string_not_allowed_by_default(self):
        rules = [FieldRule("title", FieldType.STRING, required=True)]
        result = DataValidator.validate_record({"title": ""}, rules)
        self.assertFalse(result.is_valid)

    def test_empty_string_allowed_when_flagged(self):
        rules = [FieldRule("title", FieldType.STRING, required=True, allow_empty=True)]
        result = DataValidator.validate_record({"title": ""}, rules)
        self.assertTrue(result.is_valid)

    def test_valid_required_field_passes(self):
        rules = [FieldRule("title", FieldType.STRING, required=True)]
        result = DataValidator.validate_record({"title": "Product"}, rules)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.corrected_data["title"], "Product")


class TestTypeValidation(unittest.TestCase):
    """Тесты валидации типов полей."""

    def test_string_type_valid(self):
        rules = [FieldRule("name", FieldType.STRING)]
        result = DataValidator.validate_record({"name": "abc"}, rules)
        self.assertTrue(result.is_valid)

    def test_string_type_invalid(self):
        rules = [FieldRule("name", FieldType.STRING)]
        result = DataValidator.validate_record({"name": 123}, rules)
        self.assertFalse(result.is_valid)

    def test_integer_type_valid(self):
        rules = [FieldRule("count", FieldType.INTEGER)]
        result = DataValidator.validate_record({"count": 5}, rules)
        self.assertTrue(result.is_valid)

    def test_integer_type_rejects_bool(self):
        # bool — подкласс int в Python, но не должен считаться integer-полем.
        rules = [FieldRule("count", FieldType.INTEGER)]
        result = DataValidator.validate_record({"count": True}, rules)
        self.assertFalse(result.is_valid)

    def test_integer_type_rejects_float(self):
        rules = [FieldRule("count", FieldType.INTEGER)]
        result = DataValidator.validate_record({"count": 5.5}, rules)
        self.assertFalse(result.is_valid)

    def test_float_type_valid_with_int_value(self):
        rules = [FieldRule("price", FieldType.FLOAT)]
        result = DataValidator.validate_record({"price": 10}, rules)
        self.assertTrue(result.is_valid)

    def test_float_type_valid(self):
        rules = [FieldRule("price", FieldType.FLOAT)]
        result = DataValidator.validate_record({"price": 19.99}, rules)
        self.assertTrue(result.is_valid)

    def test_boolean_type_valid(self):
        rules = [FieldRule("in_stock", FieldType.BOOLEAN)]
        result = DataValidator.validate_record({"in_stock": True}, rules)
        self.assertTrue(result.is_valid)

    def test_boolean_type_invalid(self):
        rules = [FieldRule("in_stock", FieldType.BOOLEAN)]
        result = DataValidator.validate_record({"in_stock": "yes"}, rules)
        self.assertFalse(result.is_valid)

    def test_list_type_valid(self):
        rules = [FieldRule("tags", FieldType.LIST)]
        result = DataValidator.validate_record({"tags": ["a", "b"]}, rules)
        self.assertTrue(result.is_valid)

    def test_dict_type_valid(self):
        rules = [FieldRule("meta", FieldType.DICT)]
        result = DataValidator.validate_record({"meta": {"a": 1}}, rules)
        self.assertTrue(result.is_valid)


class TestUrlEmailPhoneDate(unittest.TestCase):
    """Тесты специализированных типов: URL, EMAIL, PHONE, DATE."""

    def test_valid_url(self):
        rules = [FieldRule("url", FieldType.URL)]
        result = DataValidator.validate_record({"url": "https://example.com/item/1"}, rules)
        self.assertTrue(result.is_valid)

    def test_malformed_url(self):
        rules = [FieldRule("url", FieldType.URL)]
        result = DataValidator.validate_record({"url": "not-a-url"}, rules)
        self.assertFalse(result.is_valid)

    def test_valid_email(self):
        rules = [FieldRule("email", FieldType.EMAIL)]
        result = DataValidator.validate_record({"email": "test@example.com"}, rules)
        self.assertTrue(result.is_valid)

    def test_invalid_email(self):
        rules = [FieldRule("email", FieldType.EMAIL)]
        result = DataValidator.validate_record({"email": "not-an-email"}, rules)
        self.assertFalse(result.is_valid)

    def test_valid_phone(self):
        rules = [FieldRule("phone", FieldType.PHONE)]
        result = DataValidator.validate_record({"phone": "+1 (555) 123-4567"}, rules)
        self.assertTrue(result.is_valid)

    def test_invalid_phone_too_short(self):
        rules = [FieldRule("phone", FieldType.PHONE)]
        result = DataValidator.validate_record({"phone": "123"}, rules)
        self.assertFalse(result.is_valid)

    def test_valid_date(self):
        rules = [FieldRule("published", FieldType.DATE)]
        result = DataValidator.validate_record({"published": "2024-01-15"}, rules)
        self.assertTrue(result.is_valid)

    def test_invalid_date_format(self):
        rules = [FieldRule("published", FieldType.DATE)]
        result = DataValidator.validate_record({"published": "not a date"}, rules)
        self.assertFalse(result.is_valid)


class TestNumericRangeAndNegative(unittest.TestCase):
    """Тесты диапазона значений и допустимости отрицательных чисел."""

    def test_negative_not_allowed_by_default_config_flag(self):
        rules = [FieldRule("price", FieldType.FLOAT, allow_negative=False)]
        result = DataValidator.validate_record({"price": -5.0}, rules)
        self.assertFalse(result.is_valid)

    def test_negative_allowed_when_flagged(self):
        rules = [FieldRule("delta", FieldType.FLOAT, allow_negative=True)]
        result = DataValidator.validate_record({"delta": -5.0}, rules)
        self.assertTrue(result.is_valid)

    def test_min_value_violation(self):
        rules = [FieldRule("price", FieldType.FLOAT, min_value=10)]
        result = DataValidator.validate_record({"price": 5}, rules)
        self.assertFalse(result.is_valid)

    def test_max_value_violation(self):
        rules = [FieldRule("price", FieldType.FLOAT, max_value=100)]
        result = DataValidator.validate_record({"price": 500}, rules)
        self.assertFalse(result.is_valid)

    def test_value_within_range_passes(self):
        rules = [FieldRule("price", FieldType.FLOAT, min_value=0, max_value=1000)]
        result = DataValidator.validate_record({"price": 50}, rules)
        self.assertTrue(result.is_valid)


class TestNormalization(unittest.TestCase):
    """Тесты нормализации значений перед проверкой типа."""

    def test_normalize_converts_string_price_to_float(self):
        rules = [FieldRule("price", FieldType.FLOAT, normalize=lambda v: float(str(v).replace("$", "")))]
        result = DataValidator.validate_record({"price": "$19.99"}, rules)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.corrected_data["price"], 19.99)

    def test_normalize_failure_falls_back_to_raw_value(self):
        def bad_normalize(v):
            raise ValueError("boom")

        rules = [FieldRule("price", FieldType.FLOAT, normalize=bad_normalize)]
        result = DataValidator.validate_record({"price": 19.99}, rules)
        # normalize упал -> используется исходное значение, тип всё равно валиден
        self.assertTrue(result.is_valid)
        self.assertTrue(any("нормализ" in w for w in result.warnings))


class TestCustomPatternAndRegistry(unittest.TestCase):
    """Тесты дополнительного regex-паттерна и реестра кастомных типов."""

    def test_pattern_violation(self):
        rules = [FieldRule("sku", FieldType.STRING, pattern=r"^SKU-\d+$")]
        result = DataValidator.validate_record({"sku": "invalid"}, rules)
        self.assertFalse(result.is_valid)

    def test_pattern_match(self):
        rules = [FieldRule("sku", FieldType.STRING, pattern=r"^SKU-\d+$")]
        result = DataValidator.validate_record({"sku": "SKU-12345"}, rules)
        self.assertTrue(result.is_valid)

    def test_register_custom_type_without_modifying_existing_logic(self):
        def _validate_currency_code(value, _rule):
            return isinstance(value, str) and len(value) == 3 and value.isupper()

        DataValidator.register_type("currency_code", _validate_currency_code)

        rules = [FieldRule("currency", "currency_code")]
        valid_result = DataValidator.validate_record({"currency": "USD"}, rules)
        invalid_result = DataValidator.validate_record({"currency": "us"}, rules)

        self.assertTrue(valid_result.is_valid)
        self.assertFalse(invalid_result.is_valid)

    def test_unknown_type_produces_warning_not_crash(self):
        rules = [FieldRule("mystery", "totally_unknown_type")]
        result = DataValidator.validate_record({"mystery": "value"}, rules)
        # Неизвестный тип -> предупреждение, не ошибка/исключение.
        self.assertTrue(result.is_valid)
        self.assertTrue(len(result.warnings) >= 1)


class TestValidateRecordsBatch(unittest.TestCase):
    """Тесты пакетной валидации и обнаружения дублей."""

    def setUp(self):
        self.rules = [
            FieldRule("title", FieldType.STRING, required=True),
            FieldRule("price", FieldType.FLOAT, required=True, min_value=0),
        ]

    def test_batch_returns_pair_per_record(self):
        records = [{"title": "A", "price": 10}, {"title": "B", "price": 20}]
        results = DataValidator.validate_records(records, self.rules)
        self.assertEqual(len(results), 2)
        for record, result in results:
            self.assertIsInstance(result, ValidationResult)

    def test_batch_mixed_valid_invalid(self):
        records = [{"title": "A", "price": 10}, {"title": "", "price": -5}]
        results = DataValidator.validate_records(records, self.rules)
        self.assertTrue(results[0][1].is_valid)
        self.assertFalse(results[1][1].is_valid)

    def test_duplicate_detection_by_key(self):
        records = [
            {"title": "A", "price": 10, "url": "https://example.com/1"},
            {"title": "B", "price": 20, "url": "https://example.com/1"},
        ]
        results = DataValidator.validate_records(
            records, self.rules, detect_duplicates=True, duplicate_key="url"
        )
        self.assertTrue(results[0][1].is_valid)
        self.assertFalse(results[1][1].is_valid)
        self.assertTrue(any("Дублир" in e for e in results[1][1].errors))

    def test_duplicate_detection_by_full_record(self):
        records = [
            {"title": "A", "price": 10},
            {"title": "A", "price": 10},
        ]
        results = DataValidator.validate_records(records, self.rules, detect_duplicates=True)
        self.assertTrue(results[0][1].is_valid)
        self.assertFalse(results[1][1].is_valid)

    def test_duplicate_detection_disabled_by_default(self):
        records = [
            {"title": "A", "price": 10, "url": "https://example.com/1"},
            {"title": "B", "price": 20, "url": "https://example.com/1"},
        ]
        results = DataValidator.validate_records(records, self.rules)
        # По умолчанию detect_duplicates=False (config), оба валидны.
        self.assertTrue(results[0][1].is_valid)
        self.assertTrue(results[1][1].is_valid)

    def test_empty_records_list(self):
        results = DataValidator.validate_records([], self.rules)
        self.assertEqual(results, [])


class TestRobustness(unittest.TestCase):
    """Тесты устойчивости: компонент никогда не должен бросать исключение."""

    def test_non_dict_record_returns_invalid_without_raising(self):
        rules = [FieldRule("title", FieldType.STRING)]
        result = DataValidator.validate_record("not a dict", rules)
        self.assertFalse(result.is_valid)

    def test_none_record_returns_invalid_without_raising(self):
        rules = [FieldRule("title", FieldType.STRING)]
        result = DataValidator.validate_record(None, rules)
        self.assertFalse(result.is_valid)

    def test_exception_in_normalize_does_not_crash_whole_record(self):
        def broken(v):
            raise RuntimeError("unexpected")

        rules = [
            FieldRule("title", FieldType.STRING, required=True),
            FieldRule("price", FieldType.FLOAT, normalize=broken),
        ]
        result = DataValidator.validate_record({"title": "OK", "price": 10}, rules)
        # Ошибка нормализации не должна ронять весь процесс валидации.
        self.assertIsInstance(result, ValidationResult)

    def test_pattern_with_invalid_regex_is_handled_gracefully(self):
        rules = [FieldRule("title", FieldType.STRING, pattern="[invalid(regex")]
        result = DataValidator.validate_record({"title": "test"}, rules)
        # Некорректный regex -> перехваченная ошибка, не исключение наружу.
        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_multiple_field_errors_all_collected(self):
        rules = [
            FieldRule("title", FieldType.STRING, required=True),
            FieldRule("price", FieldType.FLOAT, required=True),
        ]
        result = DataValidator.validate_record({}, rules)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)


if __name__ == "__main__":
    unittest.main()
