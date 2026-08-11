#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Validation — централизованный слой проверки корректности спарсенных
записей перед экспортом (Milestone 5).

Стоит на границе между Parsing и Export layer:

    fetch_page_data() -> parse_html_data() -> DataValidator -> save_to_csv/json()

Отвечает за проверку того, что спарсенные данные полны, консистентны и
готовы к экспорту: обязательные поля присутствуют, типы соответствуют
ожиданиям, значения не искажены (отрицательные там, где не должны быть,
некорректный формат URL/email/даты и т.д.).

DataValidator:

* НЕ выполняет HTTP-запросов, НЕ парсит HTML/JSON (это `app/html_parser.py`,
  `app/json_parser.py`, `app/api_response_parser.py`);
* НЕ экспортирует данные (это `app/exporter.py`);
* НЕ содержит правил, специфичных для конкретного сайта — правила
  (`FieldRule`) описываются вызывающим кодом (обычно `app/parser.py`
  конкретного заказа) под структуру его записей;
* никогда не бросает исключение — любая непредвиденная ошибка валидации
  логируется через `app.utils.log_message()` и превращается в обычную
  ошибку валидации (`is_valid=False`), не прерывая обработку остальных
  записей;
* НЕ решает, что делать с невалидными записями (пропускать/экспортировать
  как есть) — это решение вызывающего кода (`app/parser.py`/`app/main.py`),
  валидатор только сообщает структурированный результат.

Расширяемость (без изменения существующей логики, только регистрацией):

    from app.data_validator import DataValidator

    def _validate_custom_sku(value, rule):
        return isinstance(value, str) and value.upper().startswith("SKU-")

    DataValidator.register_type("sku", _validate_custom_sku)

Использование (пример):

    from app.data_validator import DataValidator, FieldRule, FieldType

    rules = [
        FieldRule("title", FieldType.STRING, required=True, allow_empty=False),
        FieldRule("price", FieldType.FLOAT, required=True, min_value=0),
        FieldRule("url", FieldType.URL, required=True),
        FieldRule("description", FieldType.STRING, required=False),
    ]

    validated = DataValidator.validate_records(scraped_results, rules)

    clean_records = [
        result.corrected_data for record, result in validated if result.is_valid
    ]
    for record, result in validated:
        if not result.is_valid:
            log_message("warning", f"Запись отклонена: {result.errors}")
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from app import config
from app.utils import log_message


class FieldType(str, Enum):
    """Поддерживаемые типы полей записи."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    DATE = "date"
    LIST = "list"
    DICT = "dict"


@dataclass
class FieldRule:
    """
    Правило валидации одного поля записи.

    Атрибуты:
        name (str): Имя поля (ключ в словаре записи).
        field_type (FieldType): Ожидаемый тип значения.
        required (bool): Обязательно ли поле (отсутствующий ключ или
            `None` — ошибка, если True; предупреждение/пропуск, если False).
        allow_empty (bool): Разрешена ли пустая строка/список/словарь.
        allow_negative (bool): Разрешены ли отрицательные числа
            (применимо к INTEGER/FLOAT).
        min_value (Optional[float]): Минимально допустимое числовое значение.
        max_value (Optional[float]): Максимально допустимое числовое значение.
        pattern (Optional[str]): Дополнительный regex, которому должно
            соответствовать строковое значение (проверяется в дополнение
            к встроенной проверке типа, например, для STRING/PHONE).
        normalize (Optional[Callable[[Any], Any]]): Необязательная функция
            нормализации значения перед проверкой типа (например,
            `app.utils.clean_price` для FLOAT-поля с ценой в виде "$1,299.99").
            Если функция бросает исключение, оно перехватывается, значение
            не нормализуется, а ошибка логируется.
    """

    name: str
    field_type: FieldType
    required: bool = True
    allow_empty: bool = False
    allow_negative: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None
    normalize: Optional[Callable[[Any], Any]] = None


@dataclass
class ValidationResult:
    """
    Структурированный результат валидации одной записи.

    Атрибуты:
        is_valid (bool): Итоговый статус — True, если не было ни одной
            ошибки (warnings не влияют на итоговый статус).
        errors (List[str]): Список сообщений об ошибках (нарушение
            обязательности поля, типа, диапазона и т.д.).
        warnings (List[str]): Список предупреждений (например, отсутствие
            необязательного поля, малозначимые нарушения формата).
        corrected_data (Dict[str, Any]): Копия записи с примененными
            нормализациями (`FieldRule.normalize`), пригодная для экспорта.
    """

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    corrected_data: Dict[str, Any] = field(default_factory=dict)


# Тип функции-валидатора конкретного FieldType: принимает нормализованное
# значение и правило, возвращает True/False (соответствует ли типу).
_TypeValidator = Callable[[Any, FieldRule], bool]


class DataValidator:
    """
    Централизованный, не хранящий состояния (stateless) валидатор записей.

    Правила (`FieldRule`) передаются вызывающим кодом — компонент не
    содержит предположений о структуре данных конкретного сайта/заказа.
    Поддерживаемые типы полей регистрируются в `_type_validators` и могут
    быть расширены через `register_type()` без изменения существующей
    логики (открыт для расширения, закрыт для модификации).
    """

    # Реестр валидаторов по типу поля. Заполняется в конце модуля через
    # register_type() для каждого встроенного FieldType, чтобы логика
    # проверки была отделена от диспетчеризации (легко добавить новый тип).
    _type_validators: Dict[str, _TypeValidator] = {}

    # =====================================================================
    # РЕЕСТР ТИПОВ (расширяемость без изменения существующей логики)
    # =====================================================================

    @classmethod
    def register_type(cls, type_name: str, validator_func: _TypeValidator) -> None:
        """
        Регистрирует (или переопределяет) валидатор для имени типа.

        Позволяет добавлять поддержку новых типов полей (например,
        специфичных для конкретного заказа — "sku", "currency_code" и т.д.)
        без изменения кода `DataValidator`.

        Args:
            type_name (str): Строковое имя типа (совпадает со значением
                `FieldType`, либо произвольное новое имя для кастомного типа).
            validator_func (Callable[[Any, FieldRule], bool]): Функция,
                принимающая (значение, правило) и возвращающая True, если
                значение соответствует типу.
        """
        cls._type_validators[type_name] = validator_func

    # =====================================================================
    # ВАЛИДАЦИЯ ОДНОЙ ЗАПИСИ
    # =====================================================================

    @classmethod
    def validate_record(cls, record: Dict[str, Any], rules: Sequence[FieldRule]) -> ValidationResult:
        """
        Валидирует одну запись по списку правил полей.

        Args:
            record (Dict[str, Any]): Спарсенная запись (например, один
                элемент результата `parse_html_data()`).
            rules (Sequence[FieldRule]): Правила валидации полей записи.

        Returns:
            ValidationResult: Структурированный результат — статус,
                ошибки, предупреждения и скорректированные данные.
        """
        if not isinstance(record, dict):
            log_message("warning", f"[{__file__}] validate_record(): запись не является словарём ({type(record).__name__})")
            return ValidationResult(is_valid=False, errors=["Запись должна быть словарём (dict)"], corrected_data={})

        result = ValidationResult(corrected_data=dict(record))

        for rule in rules:
            try:
                cls._validate_field(record, rule, result)
            except Exception as e:
                # Любая непредвиденная ошибка в самом правиле (например,
                # исключение внутри кастомного normalize/regex) не должна
                # прерывать валидацию остальных полей записи.
                log_message("error", f"[{__file__}] Непредвиденная ошибка валидации поля '{rule.name}': {e}")
                result.errors.append(f"Поле '{rule.name}': непредвиденная ошибка валидации ({e})")

        result.is_valid = len(result.errors) == 0
        return result

    @classmethod
    def _validate_field(cls, record: Dict[str, Any], rule: FieldRule, result: ValidationResult) -> None:
        """
        Валидирует одно поле записи согласно `rule`, дописывая
        ошибки/предупреждения и скорректированное значение в `result`.
        """
        has_key = rule.name in record
        raw_value = record.get(rule.name)

        # --- Обязательность / отсутствие значения ---
        is_missing = (not has_key) or raw_value is None
        if is_missing:
            if rule.required:
                result.errors.append(f"Поле '{rule.name}': обязательное поле отсутствует")
            else:
                result.warnings.append(f"Поле '{rule.name}': необязательное поле отсутствует")
                result.corrected_data.pop(rule.name, None)
            return

        # --- Нормализация (перед проверкой типа) ---
        value = raw_value
        if rule.normalize is not None:
            try:
                value = rule.normalize(raw_value)
            except Exception as e:
                log_message("warning", f"[{__file__}] Ошибка нормализации поля '{rule.name}': {e}")
                result.warnings.append(f"Поле '{rule.name}': не удалось нормализовать значение ({e})")
                value = raw_value

        # --- Проверка "пустоты" (применимо к строкам/спискам/словарям) ---
        if isinstance(value, (str, list, dict)) and len(value) == 0:
            if rule.allow_empty:
                result.corrected_data[rule.name] = value
                return
            if rule.required:
                result.errors.append(f"Поле '{rule.name}': пустое значение не допускается")
            else:
                result.warnings.append(f"Поле '{rule.name}': пустое значение")
            result.corrected_data[rule.name] = value
            return

        # --- Проверка типа через реестр валидаторов ---
        type_name = rule.field_type.value if isinstance(rule.field_type, FieldType) else str(rule.field_type)
        validator_func = cls._type_validators.get(type_name)
        if validator_func is None:
            log_message("warning", f"[{__file__}] Неизвестный тип поля: {rule.field_type}")
            result.warnings.append(f"Поле '{rule.name}': неизвестный тип валидации '{rule.field_type}'")
            result.corrected_data[rule.name] = value
            return

        if not validator_func(value, rule):
            result.errors.append(
                f"Поле '{rule.name}': значение '{value!r}' не соответствует типу '{type_name}'"
            )
            result.corrected_data[rule.name] = value
            return


        # --- Диапазон значений (числовые типы) ---
        if rule.field_type in (FieldType.INTEGER, FieldType.FLOAT):
            if not rule.allow_negative and value < 0:
                result.errors.append(f"Поле '{rule.name}': отрицательное значение не допускается ({value})")
            if rule.min_value is not None and value < rule.min_value:
                result.errors.append(f"Поле '{rule.name}': значение {value} меньше минимального {rule.min_value}")
            if rule.max_value is not None and value > rule.max_value:
                result.errors.append(f"Поле '{rule.name}': значение {value} больше максимального {rule.max_value}")

        # --- Дополнительный regex-паттерн (для строковых типов) ---
        if rule.pattern is not None and isinstance(value, str):
            if not re.match(rule.pattern, value):
                result.errors.append(f"Поле '{rule.name}': значение не соответствует ожидаемому формату")

        result.corrected_data[rule.name] = value

    # =====================================================================
    # ВАЛИДАЦИЯ ПАКЕТА ЗАПИСЕЙ
    # =====================================================================

    @classmethod
    def validate_records(
        cls,
        records: Sequence[Dict[str, Any]],
        rules: Sequence[FieldRule],
        detect_duplicates: Optional[bool] = None,
        duplicate_key: Optional[str] = None,
    ) -> List[Tuple[Dict[str, Any], ValidationResult]]:
        """
        Валидирует пакет записей, опционально помечая дубликаты как ошибку.

        Args:
            records (Sequence[Dict[str, Any]]): Список спарсенных записей.
            rules (Sequence[FieldRule]): Правила валидации полей записи.
            detect_duplicates (bool, optional): Включает обнаружение
                дублирующихся записей. По умолчанию —
                `config.DATA_VALIDATION_DUPLICATE_DETECTION`.
            duplicate_key (str, optional): Имя поля, по которому определять
                дубликаты (например, "url" или "sku"). Если не указано —
                дубликат определяется по полному совпадению всех полей
                записи (может давать false positives для записей с
                одинаковыми значениями, но разной семантикой — используйте
                осознанно).

        Returns:
            List[Tuple[Dict[str, Any], ValidationResult]]: Список пар
                (исходная запись, результат валидации) в исходном порядке.
                Обнаруженный дубликат получает дополнительную ошибку в
                `ValidationResult.errors`, не прерывая обработку остальных
                записей.
        """
        effective_detect_duplicates = (
            detect_duplicates if detect_duplicates is not None else config.DATA_VALIDATION_DUPLICATE_DETECTION
        )

        results: List[Tuple[Dict[str, Any], ValidationResult]] = []
        seen_keys: set = set()

        for record in records:
            validation = cls.validate_record(record, rules)

            if effective_detect_duplicates:
                try:
                    dedupe_value = record.get(duplicate_key) if duplicate_key else _stable_record_key(record)
                except Exception as e:
                    log_message("warning", f"[{__file__}] Ошибка вычисления ключа дубликата: {e}")
                    dedupe_value = None

                if dedupe_value is not None:
                    if dedupe_value in seen_keys:
                        validation.errors.append("Дублирующаяся запись")
                        validation.is_valid = False
                        log_message("warning", f"[{__file__}] Обнаружена дублирующаяся запись: {dedupe_value!r}")
                    else:
                        seen_keys.add(dedupe_value)

            results.append((record, validation))

        skipped = sum(1 for _, v in results if not v.is_valid)
        if skipped:
            log_message("info", f"[{__file__}] Валидация завершена: {skipped} из {len(results)} записей не прошли проверку")

        return results


def _stable_record_key(record: Dict[str, Any]) -> str:
    """
    Строит стабильный строковый ключ для полного словаря записи (для
    обнаружения дублей "по всей записи", когда `duplicate_key` не указан).

    Использует сортировку по ключам и `repr()` значений — не криптографический
    хэш, а просто предсказуемый детерминированный идентификатор содержимого.
    """
    return repr(sorted(record.items(), key=lambda kv: kv[0]))


# =====================================================================
# ВСТРОЕННЫЕ ВАЛИДАТОРЫ ТИПОВ (регистрируются в реестре DataValidator)
# =====================================================================

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_string(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, str)


def _validate_integer(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_float(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_boolean(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, bool)


def _validate_url(value: Any, _rule: FieldRule) -> bool:
    if not isinstance(value, str):
        return False
    if config.DATA_VALIDATION_URL_REQUIRE_SCHEME:
        return bool(re.match(r"^https?://[^\s]+\.[^\s]+", value))
    return bool(re.match(r"^(https?://)?[^\s]+\.[^\s]+", value))


def _validate_email(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, str) and bool(_EMAIL_PATTERN.match(value))


def _validate_phone(value: Any, _rule: FieldRule) -> bool:
    if not isinstance(value, str):
        return False
    digits = re.sub(r"\D", "", value)
    return config.DATA_VALIDATION_PHONE_MIN_DIGITS <= len(digits) <= config.DATA_VALIDATION_PHONE_MAX_DIGITS


def _validate_date(value: Any, _rule: FieldRule) -> bool:
    if not isinstance(value, str):
        return False
    for date_format in config.DATA_VALIDATION_DATE_FORMATS:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            continue
    return False


def _validate_list(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, list)


def _validate_dict(value: Any, _rule: FieldRule) -> bool:
    return isinstance(value, dict)


DataValidator.register_type(FieldType.STRING.value, _validate_string)
DataValidator.register_type(FieldType.INTEGER.value, _validate_integer)
DataValidator.register_type(FieldType.FLOAT.value, _validate_float)
DataValidator.register_type(FieldType.BOOLEAN.value, _validate_boolean)
DataValidator.register_type(FieldType.URL.value, _validate_url)
DataValidator.register_type(FieldType.EMAIL.value, _validate_email)
DataValidator.register_type(FieldType.PHONE.value, _validate_phone)
DataValidator.register_type(FieldType.DATE.value, _validate_date)
DataValidator.register_type(FieldType.LIST.value, _validate_list)
DataValidator.register_type(FieldType.DICT.value, _validate_dict)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.utils import clean_price

    sample_rules = [
        FieldRule("title", FieldType.STRING, required=True, allow_empty=False),
        FieldRule("price", FieldType.FLOAT, required=True, min_value=0, normalize=clean_price),
        FieldRule("url", FieldType.URL, required=True),
        FieldRule("email", FieldType.EMAIL, required=False),
        FieldRule("description", FieldType.STRING, required=False),
    ]

    sample_records = [
        {"title": "Ноутбук", "price": "$1,299.99", "url": "https://example.com/item/1"},
        {"title": "", "price": -5, "url": "not-a-url"},
        {"price": "100", "url": "https://example.com/item/3"},
    ]

    validated = DataValidator.validate_records(sample_records, sample_rules)

    for record, result in validated:
        print(f"[{__file__}] Запись: {record}")
        print(f"  is_valid={result.is_valid}, errors={result.errors}, warnings={result.warnings}")
        print(f"  corrected_data={result.corrected_data}")
