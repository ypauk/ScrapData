#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Normalization — централизованный слой приведения спарсенных значений
к консистентному, предсказуемому формату (Milestone 5).

Стоит между Parsing и Data Validation в общем потоке обработки:

    fetch_page_data() -> parse_html_data() -> DataNormalizer -> DataValidator -> Export

Отвечает за то, чтобы сырые значения, извлечённые `HtmlParser`/`JsonParser`/
`ApiResponseParser` из разных сайтов/API, превращались в единое внутреннее
представление (чистые строки, `float`/`int`, `bool`, ISO-даты, абсолютные
URL и т.д.) ДО того, как запись попадёт в `DataValidator`.

DataNormalizer (по аналогии с `HtmlParser`/`JsonParser`/`DataValidator`):

* НЕ выполняет HTTP-запросов, НЕ парсит HTML/JSON (это `app/html_parser.py`,
  `app/json_parser.py`, `app/api_response_parser.py`);
* НЕ валидирует бизнес-правила (обязательность поля, диапазоны, дубликаты —
  это `app/data_validator.py`);
* НЕ экспортирует данные (это `app/exporter.py`);
* НЕ содержит логики, специфичной для конкретного сайта — правила
  (`NormalizationRule`) описываются вызывающим кодом (обычно `app/parser.py`
  конкретного заказа) под структуру его записей;
* никогда не бросает исключение — любая ошибка нормализации (неподдерживаемый
  формат, "битое" значение) логируется через `app.utils.log_message()` и
  превращается в безопасное значение по умолчанию, не прерывая обработку
  остальных полей/записей.

Расширяемость (без изменения существующей логики, только регистрацией —
как и в `DataValidator.register_type()`):

    from app.data_normalizer import DataNormalizer

    def _normalize_sku(value, rule):
        return str(value).strip().upper()

    DataNormalizer.register_type("sku", _normalize_sku)

Использование (одно значение):

    from app.data_normalizer import DataNormalizer

    title = DataNormalizer.normalize_string("  Продам   ВАЗ 2104  ")
    price = DataNormalizer.normalize_price("$1,299.99")
    in_stock = DataNormalizer.normalize_bool("in stock")
    published = DataNormalizer.normalize_date("31.12.2024")
    url = DataNormalizer.normalize_url("/item/42", base_url="https://example.com")

Использование (целая запись, по правилам — как `DataValidator.validate_records`):

    from app.data_normalizer import DataNormalizer, NormalizationRule, NormalizationType

    rules = [
        NormalizationRule("title", NormalizationType.STRING),
        NormalizationRule("price", NormalizationType.PRICE),
        NormalizationRule("in_stock", NormalizationType.BOOLEAN),
        NormalizationRule("url", NormalizationType.URL, base_url="https://example.com"),
    ]

    normalized_records = DataNormalizer.normalize_records(scraped_results, rules)
    validated = DataValidator.validate_records(normalized_records, validation_rules)
"""

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence
from urllib.parse import urljoin, urlsplit, urlunsplit

from app import config
from app.utils import clean_price, log_message


class NormalizationType(str, Enum):
    """Поддерживаемые типы нормализации значений."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    PRICE = "price"
    CURRENCY = "currency"
    DATE = "date"
    TIMESTAMP = "timestamp"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    COUNTRY = "country"
    LIST = "list"
    DICT = "dict"


@dataclass
class NormalizationRule:
    """
    Правило нормализации одного поля записи.

    Атрибуты:
        name (str): Имя поля (ключ в словаре записи).
        normalization_type (NormalizationType): Тип нормализации, применяемой
            к значению поля (сопоставляется с реестром `DataNormalizer`).
        default (Any): Значение, которое подставляется, если поле
            отсутствует в записи, равно `None`, либо нормализация не смогла
            распознать формат исходного значения.
        base_url (Optional[str]): Базовый URL для разрешения относительных
            ссылок (используется только `NormalizationType.URL`).
        options (Dict[str, Any]): Дополнительные именованные параметры,
            передаваемые конкретному нормализатору (например,
            `{"item_separator": "|"}` для `NormalizationType.LIST`).
    """

    name: str
    normalization_type: NormalizationType
    default: Any = None
    base_url: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)


# Тип функции-нормализатора конкретного NormalizationType: принимает сырое
# значение и правило, возвращает нормализованное значение (без исключений).
_TypeNormalizer = Callable[[Any, NormalizationRule], Any]


class DataNormalizer:
    """
    Централизованный, не хранящий состояния (stateless) помощник для
    приведения спарсенных значений к консистентному Python-представлению.

    Правила (`NormalizationRule`) передаются вызывающим кодом — компонент
    не содержит предположений о структуре данных конкретного сайта/заказа.
    Поддерживаемые типы регистрируются в `_type_normalizers` и могут быть
    расширены через `register_type()` без изменения существующей логики
    (открыт для расширения, закрыт для модификации — как `DataValidator`).
    """

    # Реестр нормализаторов по типу поля. Заполняется в конце модуля через
    # register_type() для каждого встроенного NormalizationType, чтобы
    # диспетчеризация была отделена от самой логики нормализации.
    _type_normalizers: Dict[str, _TypeNormalizer] = {}

    # =====================================================================
    # РЕЕСТР ТИПОВ (расширяемость без изменения существующей логики)
    # =====================================================================

    @classmethod
    def register_type(cls, type_name: str, normalizer_func: _TypeNormalizer) -> None:
        """
        Регистрирует (или переопределяет) нормализатор для имени типа.

        Позволяет добавлять поддержку новых типов полей (например,
        специфичных для конкретного заказа — "sku", "rating" и т.д.)
        без изменения кода `DataNormalizer`.

        Args:
            type_name (str): Строковое имя типа (совпадает со значением
                `NormalizationType`, либо произвольное новое имя для
                кастомного типа).
            normalizer_func (Callable[[Any, NormalizationRule], Any]):
                Функция, принимающая (значение, правило) и возвращающая
                нормализованное значение. Не должна бросать исключения —
                любая внутренняя ошибка должна быть обработана самой
                функцией (см. встроенные `_normalize_*` ниже как пример).
        """
        cls._type_normalizers[type_name] = normalizer_func

    # =====================================================================
    # НОРМАЛИЗАЦИЯ ОДНОЙ ЗАПИСИ / ПАКЕТА ЗАПИСЕЙ
    # =====================================================================

    @classmethod
    def normalize_record(cls, record: Dict[str, Any], rules: Sequence[NormalizationRule]) -> Dict[str, Any]:
        """
        Нормализует одну запись по списку правил полей.

        Поля записи, для которых не задано правило, копируются в результат
        без изменений (нормализатор не отбрасывает "неизвестные" поля).

        Args:
            record (Dict[str, Any]): Спарсенная запись (например, один
                элемент результата `parse_html_data()`).
            rules (Sequence[NormalizationRule]): Правила нормализации полей.

        Returns:
            Dict[str, Any]: Новая запись с нормализованными значениями.
        """
        if not isinstance(record, dict):
            log_message("warning", f"[{__file__}] normalize_record(): запись не является словарём ({type(record).__name__})")
            return {}

        normalized = dict(record)

        for rule in rules:
            raw_value = record.get(rule.name)

            if raw_value is None:
                normalized[rule.name] = rule.default
                continue

            type_name = (
                rule.normalization_type.value
                if isinstance(rule.normalization_type, NormalizationType)
                else str(rule.normalization_type)
            )
            normalizer_func = cls._type_normalizers.get(type_name)

            if normalizer_func is None:
                log_message("warning", f"[{__file__}] Неизвестный тип нормализации: {rule.normalization_type}")
                normalized[rule.name] = raw_value
                continue

            try:
                result = normalizer_func(raw_value, rule)
            except Exception as e:
                # Встроенные нормализаторы уже не должны бросать исключения,
                # но кастомные (зарегистрированные через register_type())
                # могут — защищаем обработку остальных полей записи.
                log_message("error", f"[{__file__}] Непредвиденная ошибка нормализации поля '{rule.name}': {e}")
                result = rule.default

            normalized[rule.name] = result if result is not None else rule.default

        return normalized

    @classmethod
    def normalize_records(
        cls, records: Sequence[Dict[str, Any]], rules: Sequence[NormalizationRule]
    ) -> List[Dict[str, Any]]:
        """
        Нормализует пакет записей по списку правил полей.

        Args:
            records (Sequence[Dict[str, Any]]): Список спарсенных записей.
            rules (Sequence[NormalizationRule]): Правила нормализации полей.

        Returns:
            List[Dict[str, Any]]: Список нормализованных записей в исходном
                порядке (без исключений — ошибка одной записи не прерывает
                обработку остальных).
        """
        results: List[Dict[str, Any]] = []
        for record in records:
            try:
                results.append(cls.normalize_record(record, rules))
            except Exception as e:
                log_message("error", f"[{__file__}] Не удалось нормализовать запись: {e}")
                results.append(record if isinstance(record, dict) else {})
        return results

    # =====================================================================
    # СТРОКИ / WHITESPACE
    # =====================================================================

    @staticmethod
    def normalize_whitespace(value: Optional[str]) -> str:
        """
        Сворачивает пробелы, табы и переносы строк в один пробел и
        обрезает края. Не декодирует HTML-сущности (см. `normalize_string`
        для полной строковой нормализации).

        Args:
            value (Optional[str]): Сырое строковое значение.

        Returns:
            str: Строка без лишних пробелов ("" для `None`/пустой строки).
        """
        if not value:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return re.sub(r"\s+", " ", value).strip()

    @classmethod
    def normalize_string(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> str:
        """
        Полностью нормализует текстовое значение: декодирует HTML-сущности,
        применяет Unicode-нормализацию (NFKC — приводит "похожие" символы
        к единому представлению, например полноширинные цифры/пробелы),
        сворачивает пробелы/табы/переносы строк и обрезает края.

        Безопасна для любого входного типа: нестроковые значения приводятся
        через `str()` перед обработкой.

        Args:
            value (Any): Сырое значение (обычно строка из HTML/JSON).
            _rule (Optional[NormalizationRule]): Не используется, присутствует
                для единообразной сигнатуры реестра `_type_normalizers`.

        Returns:
            str: Нормализованный текст ("" для `None`).
        """
        if value is None:
            return ""
        try:
            import html as html_module

            text = value if isinstance(value, str) else str(value)
            decoded = html_module.unescape(text)
            normalized_unicode = unicodedata.normalize("NFKC", decoded)
            return cls.normalize_whitespace(normalized_unicode)
        except Exception as e:
            log_message("warning", f"[{__file__}] Ошибка нормализации строки: {e}")
            return str(value).strip() if value is not None else ""

    # =====================================================================
    # ЧИСЛА / ЦЕНЫ / ВАЛЮТЫ
    # =====================================================================

    @classmethod
    def normalize_float(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[float]:
        """
        Безопасно приводит значение к `float`. Строки очищаются через
        `app.utils.clean_price()` (переиспользует единственную существующую
        логику разбора чисел с разделителями тысяч/десятичных — "1,299.99",
        "1.299,99", "1 299" и т.д.), чтобы не дублировать её здесь.

        Args:
            value (Any): Сырое числовое или строковое значение.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[float]: Число, либо `None`, если разбор не удался.
        """
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            if not value.strip():
                return None
            try:
                return clean_price(value)
            except Exception as e:
                log_message("warning", f"[{__file__}] Не удалось нормализовать число '{value}': {e}")
                return None
        log_message("warning", f"[{__file__}] Неподдерживаемый тип для normalize_float(): {type(value).__name__}")
        return None

    @classmethod
    def normalize_int(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[int]:
        """
        Безопасно приводит значение к `int` (через `normalize_float()`,
        отбрасывая дробную часть — консистентно с любым числовым форматом,
        который умеет разбирать `clean_price`).

        Args:
            value (Any): Сырое числовое или строковое значение.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[int]: Целое число, либо `None`, если разбор не удался.
        """
        float_value = cls.normalize_float(value)
        return int(float_value) if float_value is not None else None

    @classmethod
    def normalize_price(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[float]:
        """
        Нормализует значение цены (например, "$1,299.99", "€1.299,99",
        "1 299 грн") в `float`. Тонкий, семантический алиас над
        `normalize_float()` — цена всегда число, но именование метода
        делает правила (`NormalizationRule`) понятнее для читающего код.

        Args:
            value (Any): Сырая строка/число цены.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[float]: Цена как `float`, либо `None`, если не удалось
                разобрать.
        """
        return cls.normalize_float(value)

    @classmethod
    def normalize_currency(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Определяет ISO-код валюты по символу/названию, встреченному в
        строковом значении (например, "$1,299.99" -> "USD", "150 €" -> "EUR").

        Соответствия символ -> код настраиваются через
        `config.DATA_NORMALIZATION_CURRENCY_SYMBOLS` (без хардкода в коде).
        Если в значении уже присутствует трёхбуквенный ISO-код (например,
        "USD", "EUR") — он возвращается как есть (в верхнем регистре).

        Args:
            value (Any): Сырая строка с ценой/валютой.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[str]: ISO-код валюты (например, "USD"), либо `None`,
                если валюту не удалось определить.
        """
        if not isinstance(value, str) or not value.strip():
            return None

        text = value.strip()

        iso_match = re.search(r"\b([A-Za-z]{3})\b", text)
        if iso_match:
            candidate = iso_match.group(1).upper()
            if candidate in set(config.DATA_NORMALIZATION_CURRENCY_SYMBOLS.values()):
                return candidate

        for symbol, iso_code in config.DATA_NORMALIZATION_CURRENCY_SYMBOLS.items():
            if symbol in text:
                return iso_code

        log_message("warning", f"[{__file__}] Не удалось определить валюту в значении: '{value}'")
        return None

    # =====================================================================
    # БУЛЕВЫ ЗНАЧЕНИЯ
    # =====================================================================

    @classmethod
    def normalize_bool(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[bool]:
        """
        Приводит значение к `bool`, распознавая распространённые текстовые
        представления ("true"/"false", "yes"/"no", "1"/"0",
        "available"/"unavailable", "in stock"/"out of stock" и т.д.).

        Списки истинных/ложных слов настраиваются через
        `config.DATA_NORMALIZATION_BOOL_TRUE_VALUES` /
        `DATA_NORMALIZATION_BOOL_FALSE_VALUES` (без хардкода в коде).

        Args:
            value (Any): Сырое значение (`bool`, число или строка).
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[bool]: `True`/`False`, либо `None`, если значение не
                распознано.
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return bool(value)

        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in config.DATA_NORMALIZATION_BOOL_TRUE_VALUES:
                return True
            if normalized in config.DATA_NORMALIZATION_BOOL_FALSE_VALUES:
                return False

        log_message("warning", f"[{__file__}] Не удалось нормализовать булево значение: '{value}'")
        return None

    # =====================================================================
    # ДАТЫ / TIMESTAMP
    # =====================================================================

    @classmethod
    def normalize_date(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Разбирает дату в одном из известных форматов
        (`config.DATA_NORMALIZATION_DATE_INPUT_FORMATS`) и приводит её к
        единому выходному строковому формату
        (`config.DATA_NORMALIZATION_DATE_OUTPUT_FORMAT`, по умолчанию —
        ISO "%Y-%m-%d").

        Компонент не предполагает конкретный формат конкретного сайта —
        пробует все настроенные форматы по порядку и использует первый,
        который успешно разобрался.

        Args:
            value (Any): Сырая строка с датой, либо `datetime`/`date`.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[str]: Дата в едином выходном формате, либо `None`,
                если ни один формат не подошёл.
        """
        if isinstance(value, datetime):
            return value.strftime(config.DATA_NORMALIZATION_DATE_OUTPUT_FORMAT)

        if not isinstance(value, str) or not value.strip():
            return None

        text = value.strip()
        for date_format in config.DATA_NORMALIZATION_DATE_INPUT_FORMATS:
            try:
                parsed = datetime.strptime(text, date_format)
                return parsed.strftime(config.DATA_NORMALIZATION_DATE_OUTPUT_FORMAT)
            except ValueError:
                continue

        log_message("warning", f"[{__file__}] Не удалось нормализовать дату: '{value}'")
        return None

    @classmethod
    def normalize_timestamp(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[int]:
        """
        Приводит значение к Unix-timestamp (целые секунды, UTC).

        Поддерживает:
            * число (уже timestamp) — секунды или миллисекунды
              (миллисекунды распознаются по величине > 10**12 и делятся на 1000);
            * строку с датой в одном из `config.DATA_NORMALIZATION_DATE_INPUT_FORMATS`.

        Args:
            value (Any): Сырое числовое или строковое значение даты/времени.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[int]: Unix-timestamp в секундах (UTC), либо `None`,
                если значение не распознано.
        """
        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            numeric = float(value)
            if numeric > 10 ** 12:
                numeric /= 1000.0
            try:
                return int(numeric)
            except (ValueError, OverflowError):
                return None

        if isinstance(value, str) and value.strip():
            text = value.strip()

            if re.fullmatch(r"-?\d+(\.\d+)?", text):
                return cls.normalize_timestamp(float(text))

            for date_format in config.DATA_NORMALIZATION_DATE_INPUT_FORMATS:
                try:
                    parsed = datetime.strptime(text, date_format)
                    return int(parsed.replace(tzinfo=timezone.utc).timestamp())
                except ValueError:
                    continue

        log_message("warning", f"[{__file__}] Не удалось нормализовать timestamp: '{value}'")
        return None

    # =====================================================================
    # URL / EMAIL / ТЕЛЕФОН
    # =====================================================================

    @classmethod
    def normalize_url(cls, value: Any, rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Нормализует URL: разрешает относительные ссылки относительно
        `rule.base_url` (если передан), убирает fragment (`#...`),
        схлопывает повторяющиеся слэши в пути и добавляет схему по
        умолчанию (`config.DATA_NORMALIZATION_URL_DEFAULT_SCHEME`), если
        URL начинается с "//" (protocol-relative) или не содержит схемы.

        Args:
            value (Any): Сырая строка URL (абсолютная или относительная).
            rule (Optional[NormalizationRule]): Правило, из которого читается
                `base_url` для разрешения относительных ссылок.

        Returns:
            Optional[str]: Нормализованный абсолютный URL (если удалось
                разрешить), либо `None` для пустых/невалидных значений.
        """
        if not isinstance(value, str) or not value.strip():
            return None

        text = value.strip()
        base_url = rule.base_url if rule is not None else None

        try:
            if text.startswith("//"):
                text = f"{config.DATA_NORMALIZATION_URL_DEFAULT_SCHEME}:{text}"

            if base_url:
                text = urljoin(base_url, text)

            parts = urlsplit(text)

            if not parts.scheme:
                text = f"{config.DATA_NORMALIZATION_URL_DEFAULT_SCHEME}://{text}"
                parts = urlsplit(text)

            clean_path = re.sub(r"/{2,}", "/", parts.path)
            normalized = urlunsplit((parts.scheme, parts.netloc, clean_path, parts.query, ""))
            return normalized
        except Exception as e:
            log_message("warning", f"[{__file__}] Не удалось нормализовать URL '{value}': {e}")
            return None

    @classmethod
    def normalize_email(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Нормализует email-адрес: обрезает пробелы и приводит к нижнему
        регистру. Не изменяет структуру адреса (регистр локальной части
        технически может быть значимым для некоторых серверов, но de facto
        индустриальный стандарт — сравнивать/хранить email в lower-case).

        Args:
            value (Any): Сырая строка email.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[str]: Нормализованный email, либо `None`, если значение
                не похоже на email (нет "@" или домена).
        """
        if not isinstance(value, str) or not value.strip():
            return None

        text = value.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text):
            log_message("warning", f"[{__file__}] Значение не похоже на email: '{value}'")
            return None
        return text

    @classmethod
    def normalize_phone(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Нормализует телефонный номер: убирает все символы кроме цифр и
        (опционально) ведущего "+", сохраняя код страны.

        Сохранение "+" настраивается через
        `config.DATA_NORMALIZATION_PHONE_KEEP_PLUS` (без хардкода в коде).

        Args:
            value (Any): Сырая строка номера телефона.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[str]: Нормализованный номер (только цифры, опционально
                с ведущим "+"), либо `None` для пустых значений.
        """
        if not isinstance(value, str) or not value.strip():
            return None

        has_plus = value.strip().startswith("+")
        digits = re.sub(r"\D", "", value)

        if not digits:
            log_message("warning", f"[{__file__}] Значение не содержит цифр телефона: '{value}'")
            return None

        if has_plus and config.DATA_NORMALIZATION_PHONE_KEEP_PLUS:
            return f"+{digits}"
        return digits

    # =====================================================================
    # СТРАНЫ
    # =====================================================================

    @classmethod
    def normalize_country(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Optional[str]:
        """
        Приводит название/код страны к каноническому виду через таблицу
        псевдонимов `config.DATA_NORMALIZATION_COUNTRY_ALIASES`
        (например, "US"/"USA"/"U.S." -> "United States").

        Если значение не найдено среди псевдонимов, возвращается очищенное
        (whitespace-нормализованное) исходное значение — компонент не
        пытается угадывать незнакомые названия стран.

        Args:
            value (Any): Сырое название/код страны.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Optional[str]: Каноническое название страны, либо
                whitespace-нормализованное исходное значение.
        """
        if not isinstance(value, str) or not value.strip():
            return None

        cleaned = cls.normalize_whitespace(value)
        alias_key = cleaned.upper()

        aliases_upper = {k.upper(): v for k, v in config.DATA_NORMALIZATION_COUNTRY_ALIASES.items()}
        if alias_key in aliases_upper:
            return aliases_upper[alias_key]

        return cleaned

    # =====================================================================
    # КОЛЛЕКЦИИ (списки / словари)
    # =====================================================================

    @classmethod
    def normalize_list(cls, value: Any, rule: Optional[NormalizationRule] = None) -> List[Any]:
        """
        Приводит значение к предсказуемому списку:
            * `list`/`tuple` -> `list` (элементы копируются как есть);
            * строка с разделителем (`rule.options["item_separator"]`,
              по умолчанию ",") -> список обрезанных непустых частей;
            * `None`/пустая строка -> пустой список;
            * любое другое одиночное значение -> список из одного элемента.

        Args:
            value (Any): Сырое значение (строка, список, кортеж или
                одиночное значение).
            rule (Optional[NormalizationRule]): Правило, из которого читается
                `options["item_separator"]`.

        Returns:
            List[Any]: Нормализованный список (никогда `None`).
        """
        if value is None:
            return []

        if isinstance(value, (list, tuple)):
            return list(value)

        if isinstance(value, str):
            separator = (rule.options.get("item_separator") if rule else None) or ","
            if not value.strip():
                return []
            return [part.strip() for part in value.split(separator) if part.strip()]

        return [value]

    @classmethod
    def normalize_dict(cls, value: Any, _rule: Optional[NormalizationRule] = None) -> Dict[Any, Any]:
        """
        Приводит значение к предсказуемому словарю: `dict` возвращается как
        есть (копия), любое другое значение (включая `None`) — к пустому
        словарю, без попыток угадать структуру.

        Args:
            value (Any): Сырое значение.
            _rule (Optional[NormalizationRule]): Не используется.

        Returns:
            Dict[Any, Any]: Нормализованный словарь (никогда `None`).
        """
        if isinstance(value, dict):
            return dict(value)
        return {}


# =====================================================================
# ВСТРОЕННЫЕ НОРМАЛИЗАТОРЫ ТИПОВ (регистрируются в реестре DataNormalizer)
# =====================================================================

DataNormalizer.register_type(NormalizationType.STRING.value, DataNormalizer.normalize_string)
DataNormalizer.register_type(NormalizationType.INTEGER.value, DataNormalizer.normalize_int)
DataNormalizer.register_type(NormalizationType.FLOAT.value, DataNormalizer.normalize_float)
DataNormalizer.register_type(NormalizationType.BOOLEAN.value, DataNormalizer.normalize_bool)
DataNormalizer.register_type(NormalizationType.PRICE.value, DataNormalizer.normalize_price)
DataNormalizer.register_type(NormalizationType.CURRENCY.value, DataNormalizer.normalize_currency)
DataNormalizer.register_type(NormalizationType.DATE.value, DataNormalizer.normalize_date)
DataNormalizer.register_type(NormalizationType.TIMESTAMP.value, DataNormalizer.normalize_timestamp)
DataNormalizer.register_type(NormalizationType.URL.value, DataNormalizer.normalize_url)
DataNormalizer.register_type(NormalizationType.EMAIL.value, DataNormalizer.normalize_email)
DataNormalizer.register_type(NormalizationType.PHONE.value, DataNormalizer.normalize_phone)
DataNormalizer.register_type(NormalizationType.COUNTRY.value, DataNormalizer.normalize_country)
DataNormalizer.register_type(NormalizationType.LIST.value, DataNormalizer.normalize_list)
DataNormalizer.register_type(NormalizationType.DICT.value, DataNormalizer.normalize_dict)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тест отдельных нормализаторов:")
    print(f"  normalize_string('  Продам   ВАЗ 2104  '): '{DataNormalizer.normalize_string('  Продам   ВАЗ 2104  ')}'")
    print(f"  normalize_price('$1,299.99'): {DataNormalizer.normalize_price('$1,299.99')}")
    print(f"  normalize_price('€1.299,99'): {DataNormalizer.normalize_price('€1.299,99')}")
    print(f"  normalize_currency('$1,299.99'): {DataNormalizer.normalize_currency('$1,299.99')}")
    print(f"  normalize_bool('in stock'): {DataNormalizer.normalize_bool('in stock')}")
    print(f"  normalize_bool('out of stock'): {DataNormalizer.normalize_bool('out of stock')}")
    print(f"  normalize_date('31.12.2024'): {DataNormalizer.normalize_date('31.12.2024')}")
    print(f"  normalize_date('December 31, 2024'): {DataNormalizer.normalize_date('December 31, 2024')}")
    print(f"  normalize_timestamp('2024-12-31'): {DataNormalizer.normalize_timestamp('2024-12-31')}")
    print(f"  normalize_email('  User@Example.com '): {DataNormalizer.normalize_email('  User@Example.com ')}")
    print(f"  normalize_phone('+1 (555) 123-4567'): {DataNormalizer.normalize_phone('+1 (555) 123-4567')}")
    print(f"  normalize_country('USA'): {DataNormalizer.normalize_country('USA')}")

    rule = NormalizationRule("url", NormalizationType.URL, base_url="https://example.com/catalog/")
    print(f"  normalize_url('/item//42?x=1#frag', base_url=...): {DataNormalizer.normalize_url('/item//42?x=1#frag', rule)}")

    sample_record = {
        "title": "  Ноутбук   Acer  ",
        "price": "$1,299.99",
        "in_stock": "in stock",
        "published": "31.12.2024",
        "url": "/item/42",
        "tags": "новинка, скидка, топ",
    }
    sample_rules = [
        NormalizationRule("title", NormalizationType.STRING),
        NormalizationRule("price", NormalizationType.PRICE, default=0.0),
        NormalizationRule("in_stock", NormalizationType.BOOLEAN, default=False),
        NormalizationRule("published", NormalizationType.DATE),
        NormalizationRule("url", NormalizationType.URL, base_url="https://example.com"),
        NormalizationRule("tags", NormalizationType.LIST),
    ]
    print(f"[{__file__}] normalize_record(): {DataNormalizer.normalize_record(sample_record, sample_rules)}")
