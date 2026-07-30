#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Response Parser — стандартный слой обработки структурированных
API-ответов после того, как они получены Requests Engine (Milestone 5).

Отвечает за извлечение бизнес-данных (записей/объектов) и метаданных
пагинации из уже распарсенного JSON-объекта (`dict`/`list`) и приведение
их к предсказуемому внутреннему представлению — независимо от того, какую
конвенцию именования использует конкретный API (`data`, `results`, `items`,
`records`, `products`, `payload`, GraphQL `edges → node` и т.д.).

Разделение ответственности с `app/json_parser.py`:

* `JsonParser` — синтаксический слой: парсит JSON-строку в Python-объект
  и обеспечивает безопасный (без исключений) доступ к вложенным полям
  по пути (`"a.b[0].c"`).
* `ApiResponseParser` — семантический слой: НЕ парсит JSON-строки сам
  (принимает уже разобранный объект — результат `JsonParser.parse()` или
  `RequestsEngine.get_json()`), а понимает типовые "формы" API-ответов
  (обёртки коллекций, пагинацию) и использует `JsonParser` для безопасного
  извлечения отдельных полей.

ApiResponseParser:

* НЕ выполняет HTTP-запросов (это `app/requests_engine.py`);
* НЕ парсит HTML (это `app/html_parser.py`);
* НЕ парсит сырые JSON-строки (это `app/json_parser.py`);
* НЕ аутентифицирует пользователей и не выполняет повторы запросов;
* НЕ экспортирует данные (это Export layer, Milestone 6);
* НЕ содержит предположений о конкретном сайте/API — только общеотраслевые
  конвенции именования полей, полностью переопределяемые аргументами;
* никогда не бросает исключение из-за отсутствующих полей, неожиданной
  вложенности или неподдерживаемого формата — ошибки логируются через
  `app.utils.log_message()`, а вызывающему коду возвращается безопасное
  значение по умолчанию (пустой список/`None`/пустая метаинформация).

Использование (пример REST API):

    from app.requests_engine import RequestsEngine
    from app.api_response_parser import ApiResponseParser

    engine = RequestsEngine()
    response = engine.get_json("https://api.example.com/products?page=2")

    records = ApiResponseParser.extract_records(response)      # -> List[Any]
    pagination = ApiResponseParser.extract_pagination(response)
    if pagination.has_next:
        next_page = pagination.next_page

Использование (пример GraphQL, `data.products.edges[].node`):

    records = ApiResponseParser.extract_records(response)  # автоматически
                                                             # разворачивает edges->node

Использование (одиночный объект, например `GET /users/42`):

    user = ApiResponseParser.extract_single(response)  # -> Optional[dict]
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from app.json_parser import JsonParser
from app.utils import log_message

# Максимальная глубина рекурсивного обхода при поиске коллекции/объекта
# записей внутри вложенных словарей. Защищает от аномально глубоких или
# зациклленных структур ответа без введения отдельной настройки в
# Configuration Manager (значение — архитектурный предел компонента,
# а не поведение, которое имеет смысл менять на уровне сайта/заказа).
_MAX_SEARCH_DEPTH = 5

# Общеотраслевые ключи-обёртки коллекций записей, проверяются по порядку.
# Порядок — приоритет при неоднозначности (если в ответе одновременно
# присутствуют несколько кандидатов на одном уровне).
DEFAULT_LIST_KEYS: Sequence[str] = (
    "data",
    "results",
    "items",
    "records",
    "products",
    "payload",
    "edges",
)

# Общеотраслевые ключи-обёртки одиночного объекта.
DEFAULT_OBJECT_KEYS: Sequence[str] = (
    "data",
    "result",
    "payload",
    "item",
    "record",
    "product",
    "node",
)

# Контейнеры, в которых обычно находятся метаданные пагинации.
_PAGINATION_CONTAINER_KEYS: Sequence[str] = ("meta", "pagination", "pageInfo", "page_info")

# Альтернативные имена полей пагинации (snake_case и camelCase-варианты
# самых распространенных REST/GraphQL конвенций).
_CURRENT_PAGE_KEYS: Sequence[str] = ("current_page", "currentPage", "page", "page_number", "pageNumber")
_NEXT_PAGE_KEYS: Sequence[str] = ("next_page", "nextPage")
_PAGE_SIZE_KEYS: Sequence[str] = ("page_size", "pageSize", "per_page", "perPage", "limit")
_TOTAL_ITEMS_KEYS: Sequence[str] = ("total_items", "totalItems", "total", "total_count", "totalCount")
_TOTAL_PAGES_KEYS: Sequence[str] = ("total_pages", "totalPages", "page_count", "pageCount")
_CURSOR_KEYS: Sequence[str] = ("cursor", "next_cursor", "nextCursor", "endCursor", "end_cursor")
_HAS_NEXT_KEYS: Sequence[str] = ("has_next", "hasNext", "has_next_page", "hasNextPage", "has_more", "hasMore")


@dataclass
class PaginationMetadata:
    """
    Нормализованные метаданные пагинации, извлечённые из тела API-ответа.

    Все поля — необязательные: отсутствие того или иного поля в конкретном
    API-ответе — ожидаемая ситуация, а не ошибка (не каждый API отдаёт все
    виды пагинации сразу).

    Атрибуты:
        current_page (Optional[int]): Номер текущей страницы.
        next_page (Optional[int]): Номер следующей страницы (page-based).
        page_size (Optional[int]): Размер страницы (количество записей).
        total_items (Optional[int]): Общее количество записей во всей коллекции.
        total_pages (Optional[int]): Общее количество страниц.
        cursor (Optional[str]): Курсор для cursor-based пагинации (следующая
            "страница" запрашивается с этим курсором).
        has_next (Optional[bool]): Явный признак наличия следующей страницы.
            `None`, если API не предоставляет такого индикатора явно
            (в этом случае вызывающий код может судить по `next_page`/`cursor`).
    """

    current_page: Optional[int] = None
    next_page: Optional[int] = None
    page_size: Optional[int] = None
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    cursor: Optional[str] = None
    has_next: Optional[bool] = None


class ApiResponseParser:
    """
    Централизованный, не хранящий состояния (stateless) помощник для
    извлечения бизнес-данных и метаданных пагинации из структурированных
    API-ответов (уже разобранных в `dict`/`list`).

    Все методы — classmethod/staticmethod, ничего не знают о конкретном
    сайте/API. Ключи-обёртки, которые распознаёт парсер, являются
    общеотраслевыми конвенциями и полностью переопределяемы через
    параметры каждого метода — без необходимости менять код компонента
    под конкретный заказ.
    """

    # =====================================================================
    # ИЗВЛЕЧЕНИЕ КОЛЛЕКЦИИ ЗАПИСЕЙ
    # =====================================================================

    @classmethod
    def extract_records(
        cls,
        response: Any,
        list_keys: Optional[Sequence[str]] = None,
    ) -> List[Any]:
        """
        Извлекает и нормализует коллекцию записей из API-ответа.

        Ищет первый подходящий контейнер-коллекцию среди `list_keys`
        (рекурсивно, до `_MAX_SEARCH_DEPTH` уровней вложенности), а если
        сам `response` уже является списком — возвращает его напрямую.

        Автоматически разворачивает распространённый GraphQL-паттерн
        `edges: [{"node": {...}}, ...]` в список самих `node`-объектов
        (без необходимости отдельно знать про GraphQL у вызывающего кода).

        Args:
            response (Any): Уже разобранный JSON-объект API-ответа
                (обычно `dict` или `list`, результат `JsonParser.parse()`
                или `RequestsEngine.get_json()`).
            list_keys (Sequence[str], optional): Кастомный приоритетный
                список ключей-обёрток коллекции. По умолчанию —
                `DEFAULT_LIST_KEYS`.

        Returns:
            List[Any]: Список найденных записей. Пустой список, если
                коллекция не найдена, `response` пуст/`None`, либо имеет
                неподдерживаемый формат — без исключений.
        """
        if response is None:
            return []

        # Уже готовый список записей (простейший, но частый случай —
        # "list-based responses").
        if isinstance(response, list):
            return cls._unwrap_graphql_edges(response)

        if not isinstance(response, dict):
            log_message(
                "warning",
                f"[{__file__}] extract_records(): неподдерживаемый тип ответа {type(response).__name__}",
            )
            return []

        effective_keys = list(list_keys) if list_keys is not None else list(DEFAULT_LIST_KEYS)

        # Сначала ищем именно список (приоритет — настоящая коллекция,
        # даже если она вложена глубже, чем первый найденный dict-контейнер
        # с тем же/другим ключом-кандидатом). Раздельный проход по типам
        # (list, затем dict) необходим, иначе поверхностное совпадение
        # ключа со значением-словарем (например, "data": {"results": [...]})
        # прервало бы поиск до того, как будет найден настоящий список.
        found = cls._find_first_matching(response, effective_keys, expect_type=(list,), max_depth=_MAX_SEARCH_DEPTH)

        if found is not None:
            return cls._unwrap_graphql_edges(found)

        # Список не найден — ищем одиночный dict-объект под одним из
        # ключей-обёрток (например, {"data": {"id": 1, "name": "Solo"}}).
        found_dict = cls._find_first_matching(response, effective_keys, expect_type=(dict,), max_depth=_MAX_SEARCH_DEPTH)

        if found_dict is None:
            log_message(
                "warning",
                f"[{__file__}] extract_records(): не найдена коллекция записей "
                f"(искали ключи: {effective_keys})",
            )
            return []

        # Найденное значение — одиночный dict, а не коллекция. Оборачиваем
        # его в список из одного элемента, чтобы вызывающий код мог
        # единообразно работать с "collections always return a list"
        # (см. Data Normalization в TASK.md), не считая это ошибкой.
        return [found_dict]


    @staticmethod
    def _unwrap_graphql_edges(items: List[Any]) -> List[Any]:
        """
        Разворачивает список GraphQL `edges` (`[{"node": {...}}, ...]`)
        в список самих `node`-объектов. Элементы без обёртки `node`
        возвращаются как есть (безопасно для не-GraphQL списков).

        Args:
            items (List[Any]): Список элементов (edges либо обычные записи).

        Returns:
            List[Any]: Список записей с развёрнутыми `node`, если применимо.
        """
        unwrapped: List[Any] = []
        for item in items:
            if isinstance(item, dict) and "node" in item and isinstance(item["node"], dict):
                unwrapped.append(item["node"])
            else:
                unwrapped.append(item)
        return unwrapped

    # =====================================================================
    # ИЗВЛЕЧЕНИЕ ОДИНОЧНОГО ОБЪЕКТА
    # =====================================================================

    @classmethod
    def extract_single(
        cls,
        response: Any,
        object_keys: Optional[Sequence[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Извлекает одиночный объект из API-ответа (например, ответ на
        `GET /users/42`, где данные могут быть как "плоскими", так и
        обёрнутыми в `{"data": {...}}`/`{"result": {...}}` и т.д.).

        Args:
            response (Any): Уже разобранный JSON-объект API-ответа.
            object_keys (Sequence[str], optional): Кастомный приоритетный
                список ключей-обёрток объекта. По умолчанию —
                `DEFAULT_OBJECT_KEYS`.

        Returns:
            Optional[Dict[str, Any]]: Найденный объект, либо `None`, если
                `response` пуст/не является словарём/объект не найден
                (без исключений).
        """
        if not isinstance(response, dict):
            if response is not None:
                log_message(
                    "warning",
                    f"[{__file__}] extract_single(): неподдерживаемый тип ответа {type(response).__name__}",
                )
            return None

        effective_keys = list(object_keys) if object_keys is not None else list(DEFAULT_OBJECT_KEYS)

        found = cls._find_first_matching(response, effective_keys, expect_type=(dict,), max_depth=_MAX_SEARCH_DEPTH)

        if isinstance(found, dict):
            # GraphQL-паттерн: {"data": {"node": {...}}}
            if "node" in found and isinstance(found["node"], dict) and len(found) == 1:
                return found["node"]
            return found

        # Ни один ключ-обёртка не подошёл — если сам response выглядит
        # как "плоский" бизнес-объект (не содержит служебных ключей
        # пагинации/коллекций), считаем его самим искомым объектом.
        if not any(key in response for key in (*effective_keys, *DEFAULT_LIST_KEYS)):
            return response

        log_message(
            "warning",
            f"[{__file__}] extract_single(): не найден одиночный объект "
            f"(искали ключи: {effective_keys})",
        )
        return None

    # =====================================================================
    # ИЗВЛЕЧЕНИЕ МЕТАДАННЫХ ПАГИНАЦИИ
    # =====================================================================

    @classmethod
    def extract_pagination(cls, response: Any) -> PaginationMetadata:
        """
        Извлекает нормализованные метаданные пагинации из API-ответа.

        Ищет поля пагинации сначала в типовых контейнерах (`meta`,
        `pagination`, `pageInfo`/`page_info`), а затем — прямо в корне
        ответа (для API, которые не оборачивают пагинацию отдельно).

        Args:
            response (Any): Уже разобранный JSON-объект API-ответа.

        Returns:
            PaginationMetadata: Датакласс с найденными полями. Поля,
                отсутствующие в ответе, остаются `None` — это ожидаемое,
                а не ошибочное поведение (см. docstring `PaginationMetadata`).
        """
        if not isinstance(response, dict):
            return PaginationMetadata()

        # Кандидаты-контейнеры для поиска, в порядке приоритета:
        # сначала специализированные обёртки (найденные на любом уровне
        # вложенности, до _MAX_SEARCH_DEPTH — например,
        # `data.products.pageInfo` в GraphQL-ответах), затем сам корень ответа.
        candidates: List[Dict[str, Any]] = []
        for container_key in _PAGINATION_CONTAINER_KEYS:
            container = cls._find_first_matching(
                response, [container_key], expect_type=(dict,), max_depth=_MAX_SEARCH_DEPTH
            )
            if isinstance(container, dict):
                candidates.append(container)
        candidates.append(response)


        def _first_int(keys: Sequence[str]) -> Optional[int]:
            for container in candidates:
                for key in keys:
                    if not JsonParser.has_path(container, key):
                        continue
                    value = JsonParser.get(container, key)
                    if isinstance(value, bool):
                        continue
                    if isinstance(value, int):
                        return value
                    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
                        return int(value)
            return None


        def _first_str(keys: Sequence[str]) -> Optional[str]:
            for container in candidates:
                for key in keys:
                    value = container.get(key)
                    if isinstance(value, str) and value.strip():
                        return value
                    if isinstance(value, int) and not isinstance(value, bool):
                        return str(value)
            return None

        def _first_bool(keys: Sequence[str]) -> Optional[bool]:
            for container in candidates:
                for key in keys:
                    value = container.get(key)
                    if isinstance(value, bool):
                        return value
            return None

        return PaginationMetadata(
            current_page=_first_int(_CURRENT_PAGE_KEYS),
            next_page=_first_int(_NEXT_PAGE_KEYS),
            page_size=_first_int(_PAGE_SIZE_KEYS),
            total_items=_first_int(_TOTAL_ITEMS_KEYS),
            total_pages=_first_int(_TOTAL_PAGES_KEYS),
            cursor=_first_str(_CURSOR_KEYS),
            has_next=_first_bool(_HAS_NEXT_KEYS),
        )

    # =====================================================================
    # ВНУТРЕННИЙ ПОМОЩНИК ПОИСКА
    # =====================================================================

    @staticmethod
    def _find_first_matching(
        node: Any,
        keys: Sequence[str],
        expect_type: Sequence[type],
        max_depth: int,
    ) -> Optional[Any]:
        """
        Рекурсивно ищет первый ключ из `keys` (в порядке приоритета),
        значение которого соответствует одному из `expect_type`, обходя
        вложенные словари в ширину по уровням до `max_depth`.

        Поиск идёт "по приоритету ключа, затем по уровню вложенности":
        сначала проверяется первый ключ на текущем уровне и во всех уже
        просмотренных вложенных словарях этого уровня, затем переходим
        глубже. Это соответствует интуитивному ожиданию, что ключ верхнего
        уровня важнее случайного совпадения имени где-то в глубине ответа.

        Args:
            node (Any): Текущий узел обхода (обычно `dict`).
            keys (Sequence[str]): Приоритетный список искомых ключей.
            expect_type (Sequence[type]): Допустимые типы найденного значения.
            max_depth (int): Максimальная глубина рекурсии.

        Returns:
            Optional[Any]: Найденное значение подходящего типа, либо `None`.
        """
        if max_depth < 0 or not isinstance(node, dict):
            return None

        # Уровень 0: проверяем все ключи прямо в текущем словаре.
        for key in keys:
            if key in node and isinstance(node[key], expect_type):
                return node[key]

        # Если ни один ключ не найден на этом уровне — спускаемся во
        # вложенные словари (в порядке их следования), не превышая max_depth.
        if max_depth == 0:
            return None

        for value in node.values():
            if isinstance(value, dict):
                result = ApiResponseParser._find_first_matching(value, keys, expect_type, max_depth - 1)
                if result is not None:
                    return result

        return None


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    rest_response = {
        "data": [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}],
        "meta": {"current_page": 2, "total_pages": 5, "total_items": 42, "has_next": True},
    }

    graphql_response = {
        "data": {
            "products": {
                "edges": [
                    {"node": {"id": "1", "title": "Product A"}},
                    {"node": {"id": "2", "title": "Product B"}},
                ],
                "pageInfo": {"hasNextPage": True, "endCursor": "cursor123"},
            }
        }
    }

    single_object_response = {"data": {"id": 42, "name": "Single item"}}

    print(f"[{__file__}] REST records: {ApiResponseParser.extract_records(rest_response)}")
    print(f"[{__file__}] REST pagination: {ApiResponseParser.extract_pagination(rest_response)}")

    print(f"[{__file__}] GraphQL records: {ApiResponseParser.extract_records(graphql_response)}")

    print(f"[{__file__}] Single object: {ApiResponseParser.extract_single(single_object_response)}")

    print(f"[{__file__}] Empty response records: {ApiResponseParser.extract_records({})}")
    print(f"[{__file__}] None response records: {ApiResponseParser.extract_records(None)}")
