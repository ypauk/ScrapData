#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON Parser — централизованный слой обработки JSON (Milestone 5).

Единая точка входа для превращения сырых JSON-строк (ответы API, встроенные
`<script type="application/json">` блоки, файлы конфигурации и т.д.) в
предсказуемые Python-объекты и для безопасного доступа к вложенным полям
без риска `KeyError`/`IndexError`/`TypeError` при отсутствующих ключах,
неожиданных типах или "битой" структуре ответа.

JSON Parser (по аналогии с `app/html_parser.py::HtmlParser`):

* НЕ выполняет HTTP-запросов и не вызывает API — сырую JSON-строку туда
  передает вызывающий код (например, `RequestsEngine.get_text()`/
  `response.text`, см. `app/requests_engine.py`);
* НЕ содержит логики конкретного сайта/API (это ответственность модулей
  вроде `app/parser.py`, которые используют этот компонент как инструмент);
* НЕ экспортирует данные (этим занимается Export layer, Milestone 6);
* никогда не бросает исключение из-за невалидного JSON, отсутствующего
  ключа/индекса или несовпадения типа — все ошибки безопасно логируются
  через `app.utils.log_message()`, а вызывающему коду возвращается
  безопасное значение по умолчанию.

Использование (пример):

    from app.json_parser import JsonParser

    data = JsonParser.parse(raw_response_text)
    title = JsonParser.get_string(data, "product.title")
    price = JsonParser.get_float(data, "product.price.amount")
    images = JsonParser.get_list(data, "product.images")
    first_tag = JsonParser.get_string(data, "product.tags[0]")
"""

import json
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from app.utils import log_message

# Тип пути к вложенному значению: либо готовый список ключей/индексов
# (например, ["product", "images", 0]), либо строка в точечной нотации
# с необязательными индексами в квадратных скобках (например,
# "product.images[0]").
JsonPath = Union[str, Sequence[Union[str, int]]]

# Тип разобранного JSON: словарь, список или примитив (строка/число/bool/None).
JsonValue = Optional[Union[Dict[str, Any], List[Any], str, int, float, bool]]


class JsonParser:
    """
    Централизованный, не хранящий состояния (stateless) помощник для
    безопасного парсинга JSON и доступа к вложенным полям.

    Все методы — статические, ничего не знают о конкретном сайте/API и
    никогда не бросают исключения наружу: любая ошибка (невалидный JSON,
    отсутствующий ключ/индекс, несовпадение типа) логируется и заменяется
    безопасным значением по умолчанию, чтобы не прерывать обработку
    остальных элементов/страниц.
    """

    # =====================================================================
    # ПАРСИНГ И ВАЛИДАЦИЯ
    # =====================================================================

    @staticmethod
    def parse(raw: Optional[str]) -> JsonValue:
        """
        Безопасно парсит сырую JSON-строку в Python-объект.

        Args:
            raw (Optional[str]): Сырая JSON-строка (например, тело ответа
                API или текст `<script type="application/json">`).

        Returns:
            JsonValue: Разобранный объект (`dict`/`list`/примитив), либо
                `None`, если строка пустая, не является строкой, либо
                содержит невалидный JSON (ошибка логируется, исключение
                не бросается).
        """
        if raw is None:
            log_message("warning", f"[{__file__}] JsonParser.parse() получил None вместо JSON-строки")
            return None

        if not isinstance(raw, str):
            log_message("warning", f"[{__file__}] JsonParser.parse() получил не строку ({type(raw).__name__})")
            return None

        if not raw.strip():
            log_message("warning", f"[{__file__}] JsonParser.parse() получил пустую JSON-строку")
            return None

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            log_message("error", f"[{__file__}] Невалидный JSON (строка {e.lineno}, столбец {e.colno}): {e.msg}")
            return None
        except Exception as e:
            log_message("error", f"[{__file__}] Непредвиденная ошибка парсинга JSON: {e}")
            return None

    @staticmethod
    def is_valid(raw: Optional[str]) -> bool:
        """
        Проверяет синтаксическую валидность JSON-строки без логирования
        (тихая проверка — полезна для условной логики без лишнего шума в логах).

        Args:
            raw (Optional[str]): Сырая JSON-строка для проверки.

        Returns:
            bool: True, если строка — валидный JSON, иначе False.
        """
        if not raw or not isinstance(raw, str):
            return False
        try:
            json.loads(raw)
            return True
        except Exception:
            return False

    # =====================================================================
    # РАЗБОР ПУТИ ДОСТУПА (dotted-string <-> список ключей/индексов)
    # =====================================================================

    @staticmethod
    def _normalize_path(path: JsonPath) -> List[Union[str, int]]:
        """
        Приводит путь к единому внутреннему формату — списку ключей (str)
        и индексов (int).

        Поддерживает:
            * готовый список/тюпл: ["product", "images", 0]
            * точечную строковую нотацию: "product.images[0]" или "[0].name"

        Args:
            path (JsonPath): Путь в одном из поддерживаемых форматов.

        Returns:
            List[Union[str, int]]: Нормализованный список токенов пути.
                Пустой список означает "путь не задан" (вернуть корень).
        """
        if path is None:
            return []

        if isinstance(path, (list, tuple)):
            return list(path)

        if isinstance(path, str):
            if not path.strip():
                return []
            tokens: List[Union[str, int]] = []
            # Разбиваем строку на сегменты вида "key" или "[123]".
            for raw_token in re.findall(r"[^.\[\]]+|\[\d+\]", path):
                if raw_token.startswith("[") and raw_token.endswith("]"):
                    tokens.append(int(raw_token[1:-1]))
                else:
                    tokens.append(raw_token)
            return tokens

        # Неподдерживаемый тип пути — безопасно логируем и считаем путь пустым.
        log_message("warning", f"[{__file__}] Неподдерживаемый тип пути: {type(path).__name__}")
        return []

    @classmethod
    def _resolve_path(cls, data: JsonValue, path: JsonPath) -> Tuple[Any, bool]:
        """
        Безопасно разрешает путь внутри разобранной JSON-структуры.

        Args:
            data (JsonValue): Корневой объект (обычно результат `parse()`).
            path (JsonPath): Путь к искомому значению.

        Returns:
            Tuple[Any, bool]: (значение, найдено). Если найдено=False,
                значение всегда None — вызывающий код должен использовать
                собственный default, а не это значение.
        """
        # Путь неподдерживаемого типа (не None/str/list/tuple) — это ошибка
        # вызывающего кода, а не легитимный "пустой путь", поэтому явно
        # считаем его ненайденным, а не тихо возвращаем корень `data`.
        if path is not None and not isinstance(path, (str, list, tuple)):
            log_message("warning", f"[{__file__}] Неподдерживаемый тип пути: {type(path).__name__}")
            return None, False

        tokens = cls._normalize_path(path)
        current = data


        for token in tokens:
            try:
                if isinstance(token, int):
                    if isinstance(current, list) and -len(current) <= token < len(current):
                        current = current[token]
                    else:
                        return None, False
                else:
                    if isinstance(current, dict) and token in current:
                        current = current[token]
                    else:
                        return None, False
            except Exception as e:
                log_message("warning", f"[{__file__}] Ошибка разрешения пути на токене '{token}': {e}")
                return None, False

        return current, True

    # =====================================================================
    # БЕЗОПАСНЫЙ ДОСТУП К ВЛОЖЕННЫМ ЗНАЧЕНИЯМ
    # =====================================================================

    @classmethod
    def has_path(cls, data: JsonValue, path: JsonPath) -> bool:
        """
        Проверяет, существует ли значение по указанному пути (в том числе
        если само значение равно `None`/`null`).

        Args:
            data (JsonValue): Корневой объект.
            path (JsonPath): Путь к искомому значению.

        Returns:
            bool: True, если путь разрешился успешно (ключ/индекс найден).
        """
        _, found = cls._resolve_path(data, path)
        return found

    @classmethod
    def get(cls, data: JsonValue, path: JsonPath = "", default: Any = None) -> Any:
        """
        Безопасно извлекает значение по пути без проверки типа.

        Args:
            data (JsonValue): Корневой объект (обычно результат `parse()`).
            path (JsonPath): Путь к искомому значению. Пустой путь ("" или
                []) возвращает сам `data`.
            default (Any): Значение, возвращаемое, если путь не найден.

        Returns:
            Any: Найденное значение либо `default`.
        """
        value, found = cls._resolve_path(data, path)
        return value if found else default

    @classmethod
    def _get_typed(
        cls,
        data: JsonValue,
        path: JsonPath,
        expected_types: Tuple[type, ...],
        default: Any,
        exclude_bool: bool = False,
    ) -> Any:
        """
        Внутренний помощник: извлекает значение по пути и проверяет, что
        оно соответствует одному из `expected_types`. При несовпадении
        типа (значение найдено, но неожиданного типа) логирует
        предупреждение и возвращает `default` — без исключений и без
        неявного приведения типов.

        Args:
            data (JsonValue): Корневой объект.
            path (JsonPath): Путь к искомому значению.
            expected_types (Tuple[type, ...]): Допустимые типы значения.
            default (Any): Значение по умолчанию.
            exclude_bool (bool): Если True — значения типа `bool`
                считаются несовпадением (нужно для `get_int`/`get_float`,
                так как `bool` — подкласс `int` в Python).

        Returns:
            Any: Найденное значение подходящего типа либо `default`.
        """
        value, found = cls._resolve_path(data, path)

        if not found:
            # Отсутствующий ключ — ожидаемая, частая ситуация. Не логируем,
            # чтобы не создавать избыточный шум в логах при нормальной работе.
            return default

        if value is None:
            # Явный JSON null — тоже безопасно приравниваем к default.
            return default

        if exclude_bool and isinstance(value, bool):
            log_message(
                "warning",
                f"[{__file__}] Ожидался тип {[t.__name__ for t in expected_types]}, "
                f"получен bool по пути '{path}'",
            )
            return default

        if not isinstance(value, expected_types):
            log_message(
                "warning",
                f"[{__file__}] Ожидался тип {[t.__name__ for t in expected_types]}, "
                f"получен {type(value).__name__} по пути '{path}'",
            )
            return default

        return value

    @classmethod
    def get_string(cls, data: JsonValue, path: JsonPath, default: str = "") -> str:
        """Безопасно извлекает строковое значение по пути."""
        return cls._get_typed(data, path, (str,), default)

    @classmethod
    def get_int(cls, data: JsonValue, path: JsonPath, default: int = 0) -> int:
        """Безопасно извлекает целочисленное значение по пути (bool не считается int)."""
        return cls._get_typed(data, path, (int,), default, exclude_bool=True)

    @classmethod
    def get_float(cls, data: JsonValue, path: JsonPath, default: float = 0.0) -> float:
        """
        Безопасно извлекает числовое значение по пути и приводит его к float
        (JSON не различает int/float на уровне синтаксиса, поэтому `int`
        значения — например, "price": 100 — тоже допустимы).
        """
        value = cls._get_typed(data, path, (int, float), default, exclude_bool=True)
        return float(value) if isinstance(value, (int, float)) else default

    @classmethod
    def get_bool(cls, data: JsonValue, path: JsonPath, default: bool = False) -> bool:
        """Безопасно извлекает булево значение по пути."""
        return cls._get_typed(data, path, (bool,), default)

    @classmethod
    def get_list(cls, data: JsonValue, path: JsonPath, default: Optional[List[Any]] = None) -> List[Any]:
        """Безопасно извлекает список по пути (возвращает [] по умолчанию, если не указано иначе)."""
        safe_default = default if default is not None else []
        return cls._get_typed(data, path, (list,), safe_default)

    @classmethod
    def get_dict(cls, data: JsonValue, path: JsonPath, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Безопасно извлекает словарь по пути (возвращает {} по умолчанию, если не указано иначе)."""
        safe_default = default if default is not None else {}
        return cls._get_typed(data, path, (dict,), safe_default)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    sample_json = """
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
            "description": null
        }
    }
    """

    data = JsonParser.parse(sample_json)

    print(f"[{__file__}] title: {JsonParser.get_string(data, 'product.title')}")
    print(f"[{__file__}] id (int): {JsonParser.get_int(data, 'product.id')}")
    print(f"[{__file__}] price.amount (float): {JsonParser.get_float(data, 'product.price.amount')}")
    print(f"[{__file__}] in_stock (bool): {JsonParser.get_bool(data, 'product.in_stock')}")
    print(f"[{__file__}] tags[0]: {JsonParser.get_string(data, 'product.tags[0]')}")
    print(f"[{__file__}] images[1].url: {JsonParser.get_string(data, 'product.images[1].url')}")
    print(f"[{__file__}] description (null -> default): '{JsonParser.get_string(data, 'product.description', default='нет описания')}'")
    print(f"[{__file__}] missing.key (default): '{JsonParser.get_string(data, 'product.missing_field', default='N/A')}'")
    print(f"[{__file__}] wrong type (str запрошен для dict): '{JsonParser.get_string(data, 'product.price')}'")
    print(f"[{__file__}] has_path('product.tags'): {JsonParser.has_path(data, 'product.tags')}")
    print(f"[{__file__}] is_valid('{{invalid}}'): {JsonParser.is_valid('{invalid}')}")
    print(f"[{__file__}] parse('') -> {JsonParser.parse('')}")
