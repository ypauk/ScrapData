# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Скрапер упал с ошибкой. Найди причину и исправь **минимальным изменением**.

---

# ПРАВИЛА

ПРАВИЛА РАЗРАБОТКИ

1. Всегда использовать starter-project.

2. Не менять структуру каталогов.

3. Не создавать новые папки без необходимости.

4. Не писать код, который не требуется клиентом.

5. Предпочитать простое решение сложному.

6. Сначала искать API.

7. Если API нет — рассматривать requests + BeautifulSoup.

8. Playwright использовать только при необходимости.

9. Код должен быть модульным.

10. Docker создавать только после успешного локального запуска.

---

# АНАЛИЗ ПРОЕКТА

1. Краткое описание задачи

Клиенту необходимо выполнить тестовый парсинг первых 2 товаров из категории:

https://www.professionele-koeling.nl/koelkasten-kisten.html

Результат требуется предоставить в CSV, где:

каждый товар — отдельная строка;
каждое поле — отдельная колонка;
структура соответствует example.json;
характеристики (Specs / Extra informatie) должны быть развернуты в отдельные столбцы (Merk, Kleur, Breedte, Diepte и т.д.);
изображения сохранять только в виде ссылки (одно изображение);
описание — обычный текст без HTML;
после проверки тестового CSV, вероятно, потребуется полный парсинг категории (или сайта — пока это не подтверждено).

Уверенность: высокая.

2. Какой конечный результат нужен

На текущем этапе:

✅ CSV
2 товара
одна категория (koelkasten-kisten)
одна строка = один товар
отдельная колонка для каждого поля
отдельная колонка для каждой характеристики (Specs)

Не требуется:

скачивание изображений
JSON
Excel
база данных
API

Уверенность: высокая.

3. Как лучше решить задачу
Рекомендуемое решение

Python + requests + BeautifulSoup

Причины:

HTML страницы уже содержит всю необходимую информацию.
В предоставленном HTML присутствуют:
название;
цены;
описание;
характеристики;
breadcrumb;
изображение.
Нет признаков обязательного JavaScript-рендеринга.
Нет необходимости использовать браузер для первых двух товаров.

Алгоритм будет максимально простой:

открыть страницу категории;
получить ссылки на первые два товара;
открыть страницы товаров;
извлечь поля;
развернуть таблицу характеристик;
сохранить CSV.

Это самое простое, быстрое и надежное решение.

Уверенность: высокая.

4. Почему остальные варианты хуже
Playwright

Не рекомендуется.

Причины:

лишняя сложность;
значительно медленнее;
HTML уже содержит нужные данные.

Использовать только если обнаружится защита или динамическая подгрузка.

Selenium

Еще тяжелее Playwright.

Преимуществ нет.

Scrapy

Подойдет для полного сайта.

Но сейчас задача — всего 2 товара.

Использование Scrapy будет избыточным.

API

Пока нет подтверждения существования API.

Комбинация requests + Playwright

Излишне.

Начинать стоит именно с requests.

5. Анализ сайта

На основании предоставленного HTML.

Возможность	Статус
JavaScript Rendering	признаков нет
React	не обнаружено
Vue	не обнаружено
Angular	не обнаружено
API	неизвестно
GraphQL	не обнаружено
Infinite Scroll	нет
Pagination	вероятно есть
Login	не требуется
Cookies	возможны, но не обязательны
JWT	не обнаружено
Bearer Token	не обнаружено
CAPTCHA	есть на форме отзывов, не относится к чтению страниц
Cloudflare	неизвестно
Rate Limits	неизвестно
Download Files	не требуется
Upload Files	нет
Lazy Loading	признаков нет
WebSocket	неизвестно
XHR / Fetch	определить невозможно (HAR отсутствует)
Sitemap	не проверялся
robots.txt	не проверялся

Уверенность: средняя.

6. Что необходимо собрать до начала разработки

Для выполнения тестового задания уже имеется практически всё необходимое:

✅ пример структуры (example.json);
✅ пример HTML страницы;
✅ ссылка на категорию;
✅ требования по CSV.

Однако для полной выгрузки позже желательно иметь:

пример ожидаемого CSV (если есть);
доступ к Google Sheet (для проверки полного списка полей, если он отличается от example.json);
подтверждение, потребуется ли после теста весь каталог.

Уверенность: высокая.

7. Возможные сложности

Возможные риски:

изменение HTML;
разные наборы характеристик у разных товаров;
отсутствие скидочной цены у части товаров;
разные форматы описания;
большое количество страниц при полном парсинге;
возможные ограничения по скорости запросов;
возможная защита сайта (не подтверждена).

На текущем тестовом этапе риски минимальны.

8. Что нужно уточнить у клиента

Для тестового задания критичных вопросов почти нет, но перед полной выгрузкой желательно уточнить:

После проверки тестового CSV нужно будет собирать:
только категорию koelkasten-kisten;
или весь сайт?
Если у товара отсутствует старая цена (Sale/Old Price), что записывать:
пустое значение;
текущую цену;
0?
Если характеристика отсутствует у товара, оставлять пустую колонку?
Нужно ли сохранять все найденные колонки характеристик, даже если они встречаются только у одного товара?
Нужно ли включать наличие товара (Availability) в CSV?
9. Рекомендуемый стек технологий

Минимальный стек:

Python
requests
BeautifulSoup
CSV

Больше ничего для данного проекта не требуется.

10. План разработки
Этап 1. Анализ страницы

Цель

Проверить структуру категории и товара.

Результат

Понимание расположения всех необходимых полей.

Зависимости

Нет.

Этап 2. Извлечение ссылок

Цель

Получить первые два товара из категории.

Результат

Список URL товаров.

Зависимости

Этап 1.

Этап 3. Извлечение данных

Цель

Собрать все требуемые поля каждого товара.

Результат

Полный набор данных.

Зависимости

Этап 2.

Этап 4. Разворачивание характеристик

Цель

Преобразовать таблицу Specs в отдельные колонки.

Результат

CSV с единым набором заголовков.

Зависимости

Этап 3.

Этап 5. Формирование CSV

Цель

Подготовить итоговый файл.

Результат

CSV с двумя товарами.

Зависимости

Этапы 3–4.

11. Оценка сложности
Параметр	Оценка
Сложность	2/10
Estimation	1–2 часа
Вероятность блокировок	низкая (~10%)
Вероятность необходимости браузера	низкая (~15%)
Вероятность изменения сайта	средняя (~30%)
Общий риск	низкий
12. Можно ли решить проще

Да.

На основании предоставленного HTML наиболее простое решение — парсинг статического HTML через requests + BeautifulSoup.

Нет оснований использовать:

Playwright;
Selenium;
Scrapy;
браузерную автоматизацию.

Также стоит проверить network.har, если он будет предоставлен, на наличие скрытого API. Однако сейчас HAR-файл отсутствует (пустой), поэтому подтверждений существования API нет.

CSV является оптимальным форматом — дополнительная база данных или промежуточный JSON не нужны.

Уверенность: высокая.

13. Итоговая рекомендация
Рекомендуемое решение

Использовать Python + requests + BeautifulSoup для получения первых двух товаров из категории и формирования CSV.

Почему это оптимально
HTML уже содержит все необходимые данные.
Не требуется JavaScript-рендеринг.
Минимальная сложность.
Быстрая разработка.
Простое сопровождение.
Что необходимо получить перед началом разработки

Для выполнения тестового задания достаточно имеющихся данных. Перед полной выгрузкой желательно получить подтверждение объема работ (только категория или весь сайт) и, при необходимости, пример итогового CSV или доступ к Google Sheet для сверки структуры.

Можно ли переходить к написанию кода

Да, для тестового задания (2 товара → CSV) информации достаточно, можно переходить к реализации. Для последующего полного парсинга рекомендуется дождаться ответов клиента на вопросы о полном объеме выгрузки и обработке отсутствующих полей.

---

# ПЛАН ПРОЕКТА

Проектирование решения
Почему выбран именно этот способ
Выбранный способ: requests + BeautifulSoup (статический HTML)

По имеющимся данным это оптимальное решение.

Почему не API

Признаков существования публичного API нет.

Имеющийся HAR-файл пустой, поэтому подтвердить наличие REST API, GraphQL или XHR-эндпоинтов невозможно.

Следовательно, использовать API сейчас нельзя.

Почему не Playwright

Признаков обязательного JavaScript-рендеринга нет.

Из предоставленного HTML уже доступны:

список товаров;
ссылки на товары;
название;
цены;
breadcrumb;
описание;
характеристики (Extra informatie);
изображение;
наличие.

Поэтому браузерная автоматизация лишь усложнит проект без получения преимуществ.

Плюсы выбранного подхода
минимальное количество зависимостей;
высокая скорость;
простая архитектура;
легко тестировать на сохраненном HTML;
полностью соответствует тестовому заданию (2 товара → CSV).
Минусы
если позже сайт начнет отдавать данные только после JavaScript, потребуется переход на Playwright;
неизвестно наличие возможной антибот-защиты при массовом обходе.
1. Полный поток данных
URL категории
↓
requests
↓
HTML категории
↓
parser.parse_listing()
↓
список URL первых двух товаров
↓
requests
↓
HTML товара
↓
parser.parse_product()
↓
dict
↓
list[dict]
↓
main.py
↓
exporter.save_to_csv()
↓
CSV

Более подробно:

main.py

↓

scraper.fetch_listing()

↓

requests получает HTML категории

↓

parser.parse_listing()

↓

возвращается список URL первых двух товаров

↓

scraper.fetch_product()

↓

requests получает HTML товара

↓

parser.parse_product()

↓

возвращается dict

↓

формируется list[dict]

↓

main.py

↓

exporter.save_to_csv()
2. Проектирование app/scraper.py
Ответственность

Только:

HTTP-запросы;
обход страниц;
получение HTML;
управление последовательностью запросов.

Без анализа DOM.

2.1 Интерфейс функций
Функция	Назначение
fetch_listing(url)	Скачать HTML страницы категории
fetch_product(url)	Скачать HTML товара
collect_product_urls(category_url, limit)	Получить HTML категории, передать в parser.parse_listing(), вернуть первые N ссылок
scrape_category(category_url, limit)	Полный цикл получения HTML товаров и передачи их в parser.parse_product()
fetch_listing()

Вход

category_url

Возвращает

str (HTML)
fetch_product()

Вход

product_url

Возвращает

str (HTML)
collect_product_urls()

Алгоритм

получить HTML категории

↓

parser.parse_listing(html)

↓

вернуть первые limit ссылок

Возвращает

list[str]
scrape_category()

Алгоритм

получить список URL

для каждого URL

↓

скачать HTML

↓

parser.parse_product()

↓

добавить dict в список

↓

вернуть list[dict]
2.2 Алгоритм обхода
Категория

На тестовом этапе:

одна страница

↓

первые две карточки

↓

стоп

Пагинация пока не используется.

Для полной версии

ПРЕДПОЛОЖЕНИЕ:

Magento использует

?p=2

или

?limit=

Это требует проверки.

Какие элементы ждать

Так как используется requests,

ничего ожидать не требуется.

Достаточно успешного HTTP-ответа.

Lazy Loading

Не обнаружен.

Раскрытие вкладок

Не требуется.

В HTML уже присутствуют:

Productbeschrijving

Extra informatie
random_delay()

Имеет смысл вызывать:

между запросами товаров

Например

товар1

↓

random_delay()

↓

товар2

На тестовом задании влияние минимально, но архитектурно это правильно.

3. Проектирование app/parser.py
Ответственность

Только обработка HTML.

Никаких HTTP-запросов.

3.1 Интерфейс функций
Функция	Назначение	Вход	Возвращает
parse_listing(html)	Найти карточки товаров	HTML	list[str]
parse_product(html, url)	Извлечь данные товара	HTML	dict
parse_specs(table)	Развернуть таблицу характеристик	bs4 Tag	dict
extract_price(text)	Подготовить цену к clean_price()	str	str
parse_listing()

Извлекает

все ссылки

или

первые две ссылки

Возвращает

[
 url1,
 url2
]
parse_product()

Извлекает:

URL
Breadcrumb
Title
Short description
Image URL
Image name
Price
Sale price
Description
Specs

После чего вызывает

parse_specs()
parse_specs()

Из HTML

<th>Merk</th>

<td>Polar</td>

получает

{
 "Merk":"Polar"
}

Аналогично

Breedte

Hoogte

Kleur

и т.д.

Возвращает обычный словарь.

extract_price()

Передает строку в

utils.clean_price()

Новая функция цену не очищает.

3.2 Спецификация полей
Поле	Источник
URL	URL товара
Breadcrumb	div.breadcrumbs
Title	h1
Short description	div.short-description
imageurl	product-image href (оригинал)
image_name	имя файла изображения
Price	old-price
Sale price	special-price
Description	Productbeschrijving
Merk	Extra informatie
Kleur	Extra informatie
Breedte	Extra informatie
Diepte	Extra informatie
Hoogte	Extra informatie
Inhoud	Extra informatie
Temperatuurbereik	Extra informatie
Vermogen	Extra informatie

Если поле отсутствует

None

или

""

для текстовых значений.

3.3 Финальная структура результата
{
  "URL": "https://www.professionele-koeling.nl/polar-dm071.html",
  "Breadcrumb": "Home > Koelkasten&Kisten",
  "Title": "Polar DM071",
  "Short description": "De Polar DM071...",
  "imageurl": "https://....jpg",
  "image_name": "polar_dm071_glasdeurkoelkast_46_liter.jpg",
  "Price": 179,
  "Sale price": 175,
  "Description": "Polar DM071: Witte glasdeurkoelkast...",
  "Merk": "Polar",
  "Kleur": "Wit",
  "Breedte": "400-500mm",
  "Diepte": "400-500mm",
  "Hoogte": "450-550mm",
  "Inhoud": "Nee",
  "Temperatuurbereik": "+4 ºC / +18 ºC",
  "Vermogen": "Nee"
}

Если у второго товара появятся дополнительные характеристики (например, Energieklasse), они также должны быть добавлены как отдельные колонки при формировании общего набора полей.

4. Обработка ошибок
Сценарий	Стратегия
Timeout	Повторить запрос до 3 раз. Если неудачно — записать ошибку в лог и пропустить страницу.
HTTP 403	Записать в лог и остановить выполнение, так как возможна блокировка.
HTTP 404	Записать в лог и пропустить товар.
CAPTCHA	Записать в лог и остановить выполнение. Требуется ручное вмешательство.
Ошибка сети	До 3 повторов с паузой через random_delay().
Пустая категория	Записать в лог и завершить обработку.
Отсутствует цена	Записать None, не прерывая парсинг.
Отсутствует изображение	Записать None.
Отсутствует описание	Записать пустую строку.
Отсутствует таблица характеристик	Вернуть пустой словарь характеристик.
Изменение структуры HTML	Записать предупреждение в лог, продолжить обработку остальных полей.
5. Оценка рисков
Риск	Статус
Cloudflare	❓ Не подтвержден
Login	✅ Не требуется
Rate Limiting	⚠ Возможен при полном обходе
CAPTCHA	⚠ Есть на форме отзывов, не влияет на чтение страниц
Infinite Scroll	❌ Не обнаружен
Shadow DOM	❌ Не обнаружен
iframe	❌ Не обнаружен
WebSocket	❓ Неизвестно
GraphQL API	❌ Не обнаружен
Частые изменения DOM	⚠ Возможны (Magento)
JavaScript Rendering	❌ Не требуется
6. Порядок реализации
parser.py — написать первым, так как его можно полностью протестировать на сохраненном HTML (page.html) без сетевых запросов.
scraper.py — реализовать после готовности парсера, ограничив ответственность загрузкой HTML и передачей его в функции парсинга.
Интеграция с main.py — подключить готовые функции без изменения существующего оркестратора.
Проверка экспорта — убедиться, что exporter.save_to_csv() корректно формирует CSV с отдельной колонкой для каждого поля и каждой характеристики.
Что останется неизвестным

Подтверждено отсутствуют или не предоставлены следующие сведения:

неизвестен точный механизм пагинации полной категории;
отсутствует содержимое HAR-файла, поэтому нельзя подтвердить наличие скрытого API;
неизвестно наличие защиты при массовом обходе (Cloudflare, rate limiting);
неизвестно, будут ли у разных товаров разные наборы характеристик и насколько они разнообразны;
неизвестно, содержит ли Google Sheet дополнительные поля сверх example.json (доступ к его содержимому не анализировался).

ПРЕДПОЛОЖЕНИЯ:

для полного обхода пагинация, вероятно, реализована через параметр URL (например, ?p=2), но это требует проверки;
структура страниц товаров внутри категории единообразна.
7. Краткое резюме
Выбранная технология: requests + BeautifulSoup (статический HTML).
Основные функции scraper.py: fetch_listing(), fetch_product(), collect_product_urls(), scrape_category().
Основные функции parser.py: parse_listing(), parse_product(), parse_specs(), extract_price().
Итоговая структура данных: list[dict], где каждый словарь соответствует одному товару, а каждая характеристика (Merk, Kleur, Breedte и др.) представлена отдельным ключом/колонкой.
Главные риски проекта: возможные изменения DOM, неизвестная структура полной пагинации, потенциальные ограничения по частоте запросов при полном парсинге и отсутствие подтвержденной информации о скрытом API или защитных механизмах.

---

# ТЕКУЩИЙ КОД



--- app/api_response_parser.py ---
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


--- app/browser.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Фабрика браузерного контекста Playwright.

Низкоуровневая функция, инкапсулирующая запуск Chromium и создание
изолированного `BrowserContext`. Используется Playwright Engine
(`app/playwright_engine.py`) как единственная точка, где реально
вызывается `playwright_instance.chromium.launch()` / `browser.new_context()` —
сам движок не дублирует эту логику.

Идентичность клиента (User-Agent, Accept-Language, locale, timezone,
viewport) берется из Request Profile Manager (`app/request_profile.py`),
который остается единственным источником правды об идентичности — как для
`requests` (`RequestProfile.to_headers()`), так и для Playwright
(`RequestProfile.to_playwright_context_kwargs()`). Прокси (если передан)
применяется "как есть" — ротацию и выбор прокси выполняет Proxy Manager
до вызова этой функции.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext

from app.config import (
    HEADLESS,
    BROWSER_VIEWPORT,
    BROWSER_LOCALE,
    BROWSER_TIMEZONE,
    BROWSER_LAUNCH_ARGS,
)
from app.cookie_manager import CookieManager
from app.request_profile import RequestProfile, RequestProfileManager


def get_browser_context(
    playwright_instance,
    headless: bool = None,
    user_agent: str = None,
    cookies_path: Path = None,
    profile: Optional[RequestProfile] = None,
    proxy: Optional[Dict[str, Any]] = None,
) -> BrowserContext:
    """
    Инициализирует настроенный браузер и возвращает изолированный контекст.

    Все дефолтные значения (headless, флаги запуска) берутся из
    единого источника правды — app/config.py. Идентичность клиента
    (user-agent, viewport, локаль, часовой пояс, Accept-Language, DNT)
    берется из Request Profile Manager (`profile`, либо профиль по
    умолчанию, если не передан). Явно переданный `user_agent` имеет
    приоритет над профилем (обратная совместимость).

    Args:
        playwright_instance: Запущенный драйвер Playwright
            (`sync_playwright().start()` или `with sync_playwright() as p`).
        headless (bool, optional): Режим headless. По умолчанию — `config.HEADLESS`.
        user_agent (str, optional): Явный User-Agent, переопределяющий профиль.
        cookies_path (Path, optional): Путь к файлу куки (Cookie Manager).
        profile (RequestProfile, optional): Профиль идентичности клиента.
            По умолчанию — `RequestProfileManager.default_profile()`.
        proxy (Dict[str, Any], optional): Kwargs прокси в формате Playwright
            (`{"server": ..., "username": ..., "password": ...}`), обычно
            полученные через `ProxyManager.to_playwright_proxy_kwargs()`.
            Проверка/ротация/выбор прокси НЕ выполняется здесь.

    Returns:
        BrowserContext: Готовый к использованию изолированный контекст браузера.
    """
    # 1. Режим headless определяется централизованно в config.py (.env / Docker)
    if headless is None:
        headless = HEADLESS

    # 2. Идентичность клиента — единый источник правды: Request Profile Manager
    active_profile = profile or RequestProfileManager.default_profile()
    profile_kwargs = active_profile.to_playwright_context_kwargs()

    # Явно переданный user_agent имеет приоритет над профилем (обратная совместимость)
    if user_agent:
        profile_kwargs["user_agent"] = user_agent

    print(f"[{__file__}] Запуск Chromium (Headless={headless})...")

    # 3. Запуск браузера с флагами против падений в Docker (централизованы в config.py)
    browser: Browser = playwright_instance.chromium.launch(
        headless=headless,
        args=BROWSER_LAUNCH_ARGS
    )

    # 4. Создание контекста с маскировкой параметров профиля идентичности
    new_context_kwargs: Dict[str, Any] = {
        "user_agent": profile_kwargs["user_agent"],
        "viewport": profile_kwargs.get("viewport") or BROWSER_VIEWPORT,
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": profile_kwargs.get("locale") or BROWSER_LOCALE,
        "timezone_id": profile_kwargs.get("timezone_id") or BROWSER_TIMEZONE,
        "extra_http_headers": profile_kwargs.get("extra_http_headers"),
    }

    # 5. Прокси применяется "как есть" — Proxy Manager уже выбрал/проверил его
    if proxy:
        new_context_kwargs["proxy"] = proxy

    context: BrowserContext = browser.new_context(**new_context_kwargs)

    # 6. Подкладываем куки через Cookie Manager (единая точка загрузки куки)
    if cookies_path:
        CookieManager.apply_to_playwright_context(context, cookies=CookieManager.load(cookies_path))

    return context



# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    # Локальный тест
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    test_cookies = ROOT_DIR / "AI_INPUT" / "cookies.json"
    
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False, cookies_path=test_cookies)
        page = ctx.new_page()
        page.goto("https://bot.sannysoft.com/") # Хороший сайт для проверки детекта
        page.wait_for_timeout(5000)
        ctx.browser.close()


--- app/checkpoint_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Checkpoint Manager.

Централизованный компонент, отвечающий ТОЛЬКО за периодическое
сохранение прогресса скрапинга на диск (см. `framework/ROADMAP.md`,
Milestone 6, и `tasks/TASK.md`).

Checkpoint Manager:

* записывает текущий прогресс (номер страницы, URL, количество
  обработанных/экспортированных записей, статус, метаданные) в JSON-файл;
* решает, КОГДА нужно создать новый чекпоинт, на основе настраиваемых
  условий (число страниц / число записей / прошедшее время / ручной запрос);
* безопасно перезаписывает файл чекпоинта (запись во временный файл +
  атомарная замена), чтобы никогда не оставить частично записанный файл;
* предоставляет статический `load()` для будущего Resume Support —
  сам Checkpoint Manager чекпоинты НЕ читает и НЕ использует для
  восстановления, это ответственность отдельного будущего компонента.

Checkpoint Manager НЕ выполняет HTTP-запросы, НЕ парсит HTML/JSON, НЕ
экспортирует записи и НЕ знает о селекторах/логике конкретного сайта —
он полностью независим от scraper-специфичного кода (см. `app/scraper.py`,
`app/pagination.py`, `app/exporter.py`), что позволяет использовать его
в любом скрапере фреймворка без изменений.

Пример использования (см. интеграцию в `app/main.py::_run_incremental()`):

    from app.checkpoint_manager import CheckpointManager

    checkpoint = CheckpointManager(run_id="olx_cars_2024")
    checkpoint.start(status="running")

    for page_number, html in enumerate(raw_pages_content, 1):
        records = parse_listing(html)
        batch_writer.add_records(records)

        # save() решает сам, нужно ли реально писать на диск в этот
        # момент, основываясь на CHECKPOINT_INTERVAL_PAGES/RECORDS/SECONDS
        checkpoint.record_page(
            page_number=page_number,
            url=None,
            processed_count=len(records),
            exported_count=batch_writer.total_flushed,
        )

    checkpoint.finish(status="completed")
"""

import json
import os
import tempfile
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.config import (
    CHECKPOINT_ENABLED,
    CHECKPOINT_FILE,
    CHECKPOINT_INTERVAL_PAGES,
    CHECKPOINT_INTERVAL_RECORDS,
    CHECKPOINT_INTERVAL_SECONDS,
    CHECKPOINT_OVERWRITE_POLICY,
)
from app.utils import log_message


@dataclass
class CheckpointState:
    """
    Снимок прогресса скрапинга на момент создания чекпоинта.

    架构 намеренно оставляет дверь открытой для новых полей: любой
    дополнительный параметр, переданный через `extra_metadata`,
    сохраняется как есть в результирующем JSON без изменения структуры
    класса — старые чекпоинты остаются читаемыми (совместимость вперед).

    Атрибуты:
        run_id (str): Идентификатор конкретного запуска скрапинга
            (позволяет различать чекпоинты разных запусков/заказов).
        status (str): Текущий статус ("running", "completed", "failed").
        current_page (int): Номер последней обработанной страницы.
        current_url (str, optional): URL последней обработанной страницы.
        processed_count (int): Общее количество обработанных (спарсенных) записей.
        exported_count (int): Общее количество записей, реально сброшенных
            на диск (например, через BatchWriter.total_flushed).
        timestamp (str): ISO 8601 UTC-таймстамп момента создания чекпоинта.
        extra_metadata (dict): Произвольные дополнительные поля
            (например, имя сайта, параметры запуска) — расширяемость
            без изменения схемы.
    """

    run_id: str
    status: str = "running"
    current_page: int = 0
    current_url: Optional[str] = None
    processed_count: int = 0
    exported_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует состояние в словарь, готовый для json.dump()."""
        return asdict(self)


class CheckpointManager:
    """
    Отвечает за принятие решения "нужно ли сохранять чекпоинт сейчас" и
    за безопасную запись результата на диск.

    Не хранит зависимостей от scraper-специфичного кода — принимает
    только простые значения (номер страницы, URL, счётчики) через
    `record_page()`/`record_records()`, вызываемые из цикла скрапинга.
    """

    def __init__(
        self,
        run_id: str,
        *,
        enabled: Optional[bool] = None,
        file_path: Optional[Path] = None,
        interval_pages: Optional[int] = None,
        interval_records: Optional[int] = None,
        interval_seconds: Optional[float] = None,
        overwrite_policy: Optional[str] = None,
    ) -> None:
        """
        Args:
            run_id: Идентификатор запуска (используется в самом
                чекпоинте и в имени timestamped-файлов).
            enabled: Включает/выключает создание чекпоинтов.
                По умолчанию — config.CHECKPOINT_ENABLED.
            file_path: Путь к файлу чекпоинта.
                По умолчанию — config.CHECKPOINT_FILE.
            interval_pages: Раз в сколько страниц сохранять чекпоинт.
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_PAGES.
            interval_records: Раз в сколько записей сохранять чекпоинт.
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_RECORDS.
            interval_seconds: Минимальный интервал между чекпоинтами (сек).
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_SECONDS.
            overwrite_policy: "overwrite" или "timestamped".
                По умолчанию — config.CHECKPOINT_OVERWRITE_POLICY.
        """
        self.run_id = run_id
        self.enabled = enabled if enabled is not None else CHECKPOINT_ENABLED
        self.file_path = Path(file_path) if file_path is not None else CHECKPOINT_FILE
        self.interval_pages = interval_pages if interval_pages is not None else CHECKPOINT_INTERVAL_PAGES
        self.interval_records = interval_records if interval_records is not None else CHECKPOINT_INTERVAL_RECORDS
        self.interval_seconds = interval_seconds if interval_seconds is not None else CHECKPOINT_INTERVAL_SECONDS
        self.overwrite_policy = (overwrite_policy or CHECKPOINT_OVERWRITE_POLICY).strip().lower()

        self._state = CheckpointState(run_id=run_id)
        self._last_saved_page = 0
        self._last_saved_records = 0
        self._last_saved_monotonic: Optional[float] = None
        self._total_saves = 0

        if self.enabled:
            log_message(
                "info",
                f"CheckpointManager: инициализирован (run_id={run_id}, "
                f"file={self.file_path.name}, policy={self.overwrite_policy})",
            )

    # =====================================================================
    # ПУБЛИЧНОЕ API
    # =====================================================================

    def start(self, status: str = "running", **extra_metadata: Any) -> None:
        """
        Отмечает начало скрапинга и сразу сохраняет первичный чекпоинт
        (независимо от интервалов) — гарантирует, что файл чекпоинта
        существует с самого начала запуска, а не только после первого
        сработавшего интервала.

        Args:
            status: Начальный статус (по умолчанию "running").
            **extra_metadata: Произвольные дополнительные поля
                (например, source_url="...", site="olx").
        """
        self._state.status = status
        self._state.extra_metadata.update(extra_metadata)
        self._save(force=True)

    def record_page(
        self,
        page_number: int,
        *,
        url: Optional[str] = None,
        processed_count: Optional[int] = None,
        exported_count: Optional[int] = None,
        **extra_metadata: Any,
    ) -> bool:
        """
        Обновляет прогресс после обработки очередной страницы и
        сохраняет чекпоинт, если сработало хотя бы одно из условий
        интервала (страницы/записи/время).

        Args:
            page_number: Номер обработанной страницы (текущий прогресс).
            url: URL обработанной страницы (опционально).
            processed_count: Текущее суммарное количество обработанных записей.
            exported_count: Текущее суммарное количество экспортированных записей.
            **extra_metadata: Дополнительные поля, объединяются с уже
                накопленными (перезапись по ключу).

        Returns:
            bool: True, если чекпоинт был реально записан на диск.
        """
        self._state.current_page = page_number
        if url is not None:
            self._state.current_url = url
        if processed_count is not None:
            self._state.processed_count = processed_count
        if exported_count is not None:
            self._state.exported_count = exported_count
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)

        pages_since_save = page_number - self._last_saved_page
        should_save = self.interval_pages > 0 and pages_since_save >= self.interval_pages

        return self._maybe_save(should_save)

    def record_records(self, processed_count: int, *, exported_count: Optional[int] = None) -> bool:
        """
        Обновляет счётчики записей независимо от страниц и сохраняет
        чекпоинт, если сработало условие интервала по записям (или по
        времени — оно проверяется всегда в `_maybe_save`).

        Args:
            processed_count: Текущее суммарное количество обработанных записей.
            exported_count: Текущее суммарное количество экспортированных записей.

        Returns:
            bool: True, если чекпоинт был реально записан на диск.
        """
        self._state.processed_count = processed_count
        if exported_count is not None:
            self._state.exported_count = exported_count

        records_since_save = processed_count - self._last_saved_records
        should_save = self.interval_records > 0 and records_since_save >= self.interval_records

        return self._maybe_save(should_save)

    def save_now(self, **extra_metadata: Any) -> bool:
        """
        Принудительно сохраняет чекпоинт немедленно, игнорируя все
        интервалы (ручной запрос — см. TASK.md "manual checkpoint requests").

        Returns:
            bool: True, если чекпоинт был записан (False только при
                CHECKPOINT_ENABLED=False или сбое записи).
        """
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)
        return self._save(force=True)

    def finish(self, status: str = "completed", **extra_metadata: Any) -> bool:
        """
        Отмечает завершение скрапинга (успешное или с ошибкой) и
        принудительно сохраняет финальный чекпоинт независимо от
        интервалов — гарантирует, что последнее состояние всегда
        зафиксировано на диске.

        Args:
            status: Финальный статус ("completed" или "failed").
            **extra_metadata: Дополнительные поля для финального чекпоинта.

        Returns:
            bool: True, если чекпоинт был записан.
        """
        self._state.status = status
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)
        return self._save(force=True)

    @property
    def state(self) -> CheckpointState:
        """Текущее состояние прогресса (для инспекции/тестов)."""
        return self._state

    @property
    def total_saves(self) -> int:
        """Общее количество реально выполненных записей чекпоинта на диск."""
        return self._total_saves

    # =====================================================================
    # ЗАГРУЗКА ЧЕКПОИНТА (для будущего Resume Support)
    # =====================================================================

    @staticmethod
    def load(file_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """
        Читает последний сохранённый чекпоинт с диска.

        Checkpoint Manager сам эти данные никогда не использует — метод
        предоставлен исключительно для будущего Resume Support, чтобы
        тот не реализовывал собственный механизм отслеживания прогресса
        (см. `tasks/TASK.md`, раздел "Integration").

        Args:
            file_path: Путь к файлу чекпоинта. По умолчанию — config.CHECKPOINT_FILE.

        Returns:
            dict, optional: Содержимое чекпоинта, либо None, если файл
                отсутствует, пуст или повреждён.
        """
        path = Path(file_path) if file_path is not None else CHECKPOINT_FILE
        if not path.exists() or path.stat().st_size == 0:
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_message("error", f"CheckpointManager: не удалось загрузить чекпоинт {path.name}: {e}")
            return None

    # =====================================================================
    # ВНУТРЕННЯЯ ЛОГИКА
    # =====================================================================

    def _maybe_save(self, should_save: bool) -> bool:
        """
        Проверяет условие по времени (оно всегда учитывается как
        дополнительное ограничение сверху условий pages/records — не
        даёт сохранять чекпоинты слишком часто) и выполняет сохранение,
        если хотя бы одно из условий (переданное `should_save` ИЛИ
        отсутствие ограничения по времени) выполнено.
        """
        if not should_save:
            return False

        if self.interval_seconds > 0 and self._last_saved_monotonic is not None:
            elapsed = time.monotonic() - self._last_saved_monotonic
            if elapsed < self.interval_seconds:
                return False

        return self._save(force=False)

    def _save(self, *, force: bool) -> bool:
        """
        Выполняет фактическую запись чекпоинта на диск, если
        `self.enabled`. При `overwrite_policy == "timestamped"`
        дополнительно сохраняет копию с суффиксом-таймстампом.

        Запись выполняется через временный файл в той же директории +
        `os.replace()` (атомарная операция на POSIX и Windows) — исключает
        ситуацию, когда процесс прерывается посреди записи и оставляет
        частично записанный/повреждённый JSON-файл чекпоинта.

        Args:
            force: Если True — запись выполняется независимо от
                состояния интервалов (используется start()/finish()/save_now()).

        Returns:
            bool: True при успешной записи, False если чекпоинт
                отключен либо запись завершилась ошибкой.
        """
        if not self.enabled:
            return False

        self._state.timestamp = datetime.now(timezone.utc).isoformat()
        payload = self._state.to_dict()

        try:
            self._atomic_write(self.file_path, payload)

            if self.overwrite_policy == "timestamped":
                ts_suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
                timestamped_path = self.file_path.with_name(
                    f"{self.file_path.stem}_{ts_suffix}{self.file_path.suffix}"
                )
                self._atomic_write(timestamped_path, payload)

            self._last_saved_page = self._state.current_page
            self._last_saved_records = self._state.processed_count
            self._last_saved_monotonic = time.monotonic()
            self._total_saves += 1

            log_message(
                "debug" if not force else "info",
                f"CheckpointManager: чекпоинт сохранён (страница={self._state.current_page}, "
                f"записей={self._state.processed_count}, статус={self._state.status})",
            )
            return True

        except Exception as e:
            # Требование TASK.md: сбой чекпоинта никогда не должен
            # прерывать скрапинг — только логируется как ошибка.
            log_message("error", f"CheckpointManager: не удалось сохранить чекпоинт: {e}")
            return False

    @staticmethod
    def _atomic_write(path: Path, payload: Dict[str, Any]) -> None:
        """
        Записывает JSON атомарно: пишет во временный файл в той же
        директории, принудительно сбрасывает буферы ОС на диск
        (`flush()` + `os.fsync()`), затем атомарно переименовывает
        (`os.replace()`) во целевой путь. Если процесс будет прерван
        в любой момент до `os.replace()`, целевой файл чекпоинта
        останется нетронутым (старая валидная версия).

        Args:
            path: Итоговый путь файла чекпоинта.
            payload: Сериализуемые данные для записи.
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), prefix=f".{path.stem}_", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        except Exception:
            # Гарантируем, что временный файл не остаётся мусором при сбое.
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import shutil
    import time as _time

    test_file = Path(tempfile.gettempdir()) / "checkpoint_manager_selftest.json"
    if test_file.exists():
        test_file.unlink()

    print(f"[{__file__}] Тест CheckpointManager (файл: {test_file})")

    checkpoint = CheckpointManager(
        run_id="selftest",
        enabled=True,
        file_path=test_file,
        interval_pages=2,
        interval_records=0,
        interval_seconds=0,
        overwrite_policy="overwrite",
    )

    checkpoint.start(status="running", site="example.com")

    for page in range(1, 6):
        saved = checkpoint.record_page(
            page_number=page,
            url=f"https://example.com/page/{page}",
            processed_count=page * 10,
            exported_count=page * 10,
        )
        print(f"  Страница {page}: сохранено={saved}")

    checkpoint.finish(status="completed")

    print(f"Всего сохранений: {checkpoint.total_saves}")
    print(f"Итоговое содержимое файла: {json.dumps(CheckpointManager.load(test_file), ensure_ascii=False, indent=2)}")

    test_file.unlink(missing_ok=True)


--- app/config.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Централизованный менеджер конфигурации проекта.

Единый источник правды для всех настраиваемых параметров: путей проекта,
поведения запуска (Docker/Headless), таймаутов и повторов, а также
настроек идентификации клиента (User-Agent, локаль, часовой пояс, viewport),
которые используются как модулем Playwright (app/browser.py), так и любым
кодом на базе requests/httpx.

Все значения читаются из переменных окружения (.env) с безопасными
дефолтами, поэтому изменение поведения парсера не требует правок кода —
достаточно поменять .env.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

# Загружаем переменные из .env (в корне starter-project) в окружение процесса
# ДО того, как ниже будут читаться os.getenv(...). Без этого вызова значения
# из .env не подхватываются при обычном запуске (python -m app...), только
# если переменные заданы вручную в самой ОС/оболочке.
# override=False — переменные, уже заданные в реальном окружении (например,
# в Docker/CI), имеют приоритет над файлом .env.
load_dotenv(Path(__file__).parent.parent / ".env", override=False)


# =====================================================================
# 0. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ЧТЕНИЯ ОКРУЖЕНИЯ
# =====================================================================


def _get_bool(name: str, default: str = "0") -> bool:
    """Читает булево значение из переменной окружения ("1"/"true"/"yes" -> True)."""
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes")


def _get_int(name: str, default: int) -> int:
    """Читает целочисленное значение из переменной окружения с безопасным фолбэком."""
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


# =====================================================================
# 1. ПУТИ К ПАПКАМ СТРУКТУРЫ (Абсолютные)
# =====================================================================
APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent.resolve()

# Папки для работы с ИИ
AI_INPUT_DIR = ROOT_DIR / "AI_INPUT"
AI_OUTPUT_DIR = ROOT_DIR / "AI_OUTPUT"

# Входные и выходные данные для скрипта
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"

# Файлы окружения и зависимостей
COOKIES_FILE = AI_INPUT_DIR / "cookies.json"
HEADERS_FILE = AI_INPUT_DIR / "headers.json"
PAGE_HTML_FILE = AI_INPUT_DIR / "page.html"

# Гарантируем, что рабочие папки проекта существуют
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 2. НАСТРОЙКИ ЗАПУСКА, ТАЙМАУТЫ И ПОВТОРЫ
#    (общие для Requests и Playwright, .env / Окружение)
# =====================================================================

# Если переменная IS_DOCKER установлена, принудительно включаем headless
IS_DOCKER = _get_bool("IS_DOCKER", "0")
HEADLESS = _get_bool("HEADLESS", "1") or IS_DOCKER

# Таймауты и повторы применимы как к HTTP-запросам (requests), так и к Playwright
TIMEOUT = _get_int("SCRAPER_TIMEOUT", 30)  # в секундах
RETRY_COUNT = _get_int("SCRAPER_RETRY", 3)

# Множитель экспоненциальной задержки между повторами (используется Retry Manager).
# Задержка между попытками растет как: backoff_factor * (2 ** (попытка - 1))
RETRY_BACKOFF_FACTOR = float(os.getenv("SCRAPER_RETRY_BACKOFF", "0.5"))

# Добавлять случайный джиттер к задержке повтора, чтобы избежать
# синхронных всплесков запросов при параллельном скрапинге.
RETRY_JITTER = _get_bool("SCRAPER_RETRY_JITTER", "1")

# HTTP-статусы, которые считаются временными сбоями и подлежат повтору.
RETRYABLE_STATUS_CODES: List[int] = [
    int(code.strip())
    for code in os.getenv("SCRAPER_RETRYABLE_STATUS_CODES", "429,500,502,503,504").split(",")
    if code.strip()
]

# Политика задержек между запросами (используется Delay Manager).
# Режим: "fixed" — постоянная пауза, "random" — случайная пауза в диапазоне.
DELAY_MODE = os.getenv("SCRAPER_DELAY_MODE", "random").strip().lower()
DELAY_FIXED_SECONDS = float(os.getenv("SCRAPER_DELAY_FIXED", "2.0"))
DELAY_MIN_SECONDS = float(os.getenv("SCRAPER_DELAY_MIN", "1.0"))
DELAY_MAX_SECONDS = float(os.getenv("SCRAPER_DELAY_MAX", "3.0"))

# --- Requests Engine (app/requests_engine.py) ---
REQUESTS_VERIFY_SSL = _get_bool("REQUESTS_VERIFY_SSL", "1")
REQUESTS_ALLOW_REDIRECTS = _get_bool("REQUESTS_ALLOW_REDIRECTS", "1")
REQUESTS_MAX_REDIRECTS = _get_int("REQUESTS_MAX_REDIRECTS", 30)




# Настройки сети и прокси
PROXY_URL: Optional[str] = os.getenv("PROXY_URL") or None  # Формат: http://username:password@host:port

# Путь к файлу со списком прокси для File Proxy Provider (app/file_proxy_provider.py).
# Формат файла — по одной записи в строке, поддерживаются: ip:port,
# ip:port:username:password, а также готовые URL (http://..., socks5://...).
PROXY_FILE = Path(os.getenv("PROXY_FILE_PATH", str(AI_INPUT_DIR / "proxies.txt")))

# Схема (http/https/socks5), используемая File Proxy Provider для записей без
# явной схемы (ip:port или ip:port:username:password).
PROXY_FILE_DEFAULT_SCHEME = os.getenv("PROXY_FILE_DEFAULT_SCHEME", "http")

# --- Webshare Proxy Provider (app/webshare_proxy_provider.py) ---
# API-ключ Webshare. Никогда не хардкодится — только через окружение (.env).
WEBSHARE_API_KEY: Optional[str] = os.getenv("WEBSHARE_API_KEY") or None

# Базовый URL официального Webshare Proxy List API.
WEBSHARE_API_URL = os.getenv("WEBSHARE_API_URL", "https://proxy.webshare.io/api/v2/proxy/list/")

# Сколько секунд переиспользовать закэшированный список прокси до повторного
# запроса к API (снижает нагрузку на API и риск упереться в rate limit).
WEBSHARE_CACHE_TTL_SECONDS = _get_int("WEBSHARE_CACHE_TTL_SECONDS", 300)

# Таймаут запроса к Webshare API (секунды). По умолчанию — общий TIMEOUT проекта.
WEBSHARE_API_TIMEOUT = _get_int("WEBSHARE_API_TIMEOUT", TIMEOUT)

# --- Proxy Cache (app/proxy_cache.py) ---
# Локальный файл, в котором Proxy Cache хранит последний успешно
# загруженный список прокси (provider-независимо: Webshare, File и т.д.).
PROXY_CACHE_FILE = Path(os.getenv("PROXY_CACHE_FILE_PATH", str(AI_INPUT_DIR / "proxy_cache.json")))

# Сколько секунд считать закэшированный список прокси актуальным до
# необходимости обновления через провайдер (не путать с
# WEBSHARE_CACHE_TTL_SECONDS — это TTL персистентного файлового кэша,
# который переживает перезапуск процесса).
PROXY_CACHE_TTL_SECONDS = _get_int("PROXY_CACHE_TTL_SECONDS", 300)

# --- Proxy Selection (app/proxy_selector.py) ---
# Активная стратегия выбора прокси из пула: "first" (первый доступный)
# или "random" (случайный). Новые стратегии регистрируются через
# `ProxySelector.register_strategy()` без изменения кода.
PROXY_SELECTION_STRATEGY = os.getenv("PROXY_SELECTION_STRATEGY", "first").strip().lower()

# --- Proxy Rotation (app/proxy_rotation.py) ---
# Активная политика ротации прокси: "never", "every_request",
# "every_n_requests" или "after_failure". Новые политики регистрируются
# через `ProxyRotation.register_policy()` без изменения кода.
# "every_request" — политика по умолчанию, воспроизводящая поведение
# Proxy Manager до появления Proxy Rotation (обратная совместимость).
PROXY_ROTATION_POLICY = os.getenv("PROXY_ROTATION_POLICY", "every_request").strip().lower()

# Количество запросов между ротациями для политики "every_n_requests".
PROXY_ROTATION_EVERY_N = _get_int("PROXY_ROTATION_EVERY_N", 5)

# --- Proxy Health Check (app/health_check.py) ---
# Все пороги настраиваются через .env; смена любого порога не требует правок кода.
# URL для активной проверки прокси (лёгкий GET, проверяющий доступность прокси).
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", "https://httpbin.org/ip")
# Таймаут активной проверки (секунды).
HEALTH_CHECK_TIMEOUT = _get_int("HEALTH_CHECK_TIMEOUT", 10)
# Максимальное число последовательных сбоев, после которого прокси
# автоматически DISABLED на `HEALTH_DISABLE_DURATION_SECONDS`.
HEALTH_MAX_CONSECUTIVE_FAILURES = _get_int("HEALTH_MAX_CONSECUTIVE_FAILURES", 5)
# Число последовательных сбоев, после которого прокси переходит в статус
# UNHEALTHY (более серьёзная деградация, чем WARNING, но ещё не DISABLED).
# По умолчанию — половина от HEALTH_MAX_CONSECUTIVE_FAILURES, чтобы
# обеспечить промежуточную ступень предупреждения перед автоотключением.
HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES = _get_int(
    "HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES",
    max(1, HEALTH_MAX_CONSECUTIVE_FAILURES // 2),
)

# Минимальная допустимая доля успешных запросов (0.0–1.0). При падении ниже
# этого порога (и наличии хотя бы `HEALTH_MIN_REQUESTS_FOR_RATE` запросов
# для достоверности) статус прокси становится WARNING.
HEALTH_MIN_SUCCESS_RATE = float(os.getenv("HEALTH_MIN_SUCCESS_RATE", "0.5"))
# Минимальное количество запросов, необходимое для учёта порога success rate
# (при малой выборке порог не применяется во избежание ложно-негативных статусов).
HEALTH_MIN_REQUESTS_FOR_RATE = _get_int("HEALTH_MIN_REQUESTS_FOR_RATE", 10)
# Максимально допустимое среднее время ответа (миллисекунды). При превышении —
# WARNING. Применяется только при наличии хотя бы одного успешного запроса.
HEALTH_MAX_RESPONSE_TIME_MS = _get_int("HEALTH_MAX_RESPONSE_TIME_MS", 5000)
# Длительность отключения прокси при достижении порога последовательных
# сбоев (секунды). По истечении этого окна прокси автоматически
# перепроверяется и может вернуться в строй.
HEALTH_DISABLE_DURATION_SECONDS = _get_int("HEALTH_DISABLE_DURATION_SECONDS", 300)

# --- Sticky Sessions (app/sticky_sessions.py) ---
# Все параметры настраиваются через .env; смена любого значения не требует правок кода.
# Включает/выключает привязку прокси к логической сессии в Proxy Manager.
STICKY_SESSIONS_ENABLED = _get_bool("STICKY_SESSIONS_ENABLED", "1")
# Максимальная длительность привязки сессии к прокси (секунды). 0 — без ограничения по времени.
STICKY_SESSION_TIMEOUT_SECONDS = _get_int("STICKY_SESSION_TIMEOUT_SECONDS", 600)
# Максимальное количество запросов в рамках одной сессии. 0 — без ограничения.
STICKY_SESSION_MAX_REQUESTS = _get_int("STICKY_SESSION_MAX_REQUESTS", 100)
# Поведение при отказе привязанного прокси: "replace" — сессия продолжается
# с новым прокси при следующем запросе, "terminate" — сессия помечается
# терминированной (вызывающий код должен начать новую логическую сессию).
STICKY_SESSION_ON_FAILURE = os.getenv("STICKY_SESSION_ON_FAILURE", "replace").strip().lower()



# =====================================================================
# 3. МАСКИРОВКА И КЛИЕНТСКИЕ ДАННЫЕ
#    (используются и в headers для requests, и в контексте Playwright)
# =====================================================================

# Реалистичный дефолтный User-Agent, если не передан кастомный в headers.json
DEFAULT_USER_AGENT = os.getenv(
    "SCRAPER_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
)

# Локаль и часовой пояс браузерного контекста / заголовков запросов
BROWSER_LOCALE = os.getenv("BROWSER_LOCALE", "en-US")
BROWSER_TIMEZONE = os.getenv("BROWSER_TIMEZONE", "America/New_York")

# Размер окна браузера (viewport). Ранее было захардкожено внутри browser.py
BROWSER_VIEWPORT: Dict[str, int] = {
    "width": _get_int("BROWSER_VIEWPORT_WIDTH", 1920),
    "height": _get_int("BROWSER_VIEWPORT_HEIGHT", 1080),
}

# Флаги запуска Chromium, снижающие типовые признаки автоматизации.
# Централизованы здесь, чтобы не дублировать список в разных местах кода.
BROWSER_LAUNCH_ARGS: List[str] = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
]


# =====================================================================
# 3.1 ЗАГОЛОВКИ ЗАПРОСОВ (сырые дефолты для Request Profile Manager)
#     Эти значения — единственный источник правды для HTTP-заголовков.
#     Используются app/request_profile.py для сборки полного профиля
#     идентичности (Requests + Playwright).
# =====================================================================

DEFAULT_ACCEPT = os.getenv(
    "SCRAPER_ACCEPT",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
)
DEFAULT_ACCEPT_LANGUAGE = os.getenv("SCRAPER_ACCEPT_LANGUAGE", "en-US,en;q=0.9")
DEFAULT_ACCEPT_ENCODING = os.getenv("SCRAPER_ACCEPT_ENCODING", "gzip, deflate, br")
DEFAULT_CONNECTION = os.getenv("SCRAPER_CONNECTION", "keep-alive")
DEFAULT_UPGRADE_INSECURE_REQUESTS = os.getenv("SCRAPER_UPGRADE_INSECURE_REQUESTS", "1")
DEFAULT_SEC_FETCH_DEST = os.getenv("SCRAPER_SEC_FETCH_DEST", "document")
DEFAULT_SEC_FETCH_MODE = os.getenv("SCRAPER_SEC_FETCH_MODE", "navigate")
DEFAULT_SEC_FETCH_SITE = os.getenv("SCRAPER_SEC_FETCH_SITE", "none")
DEFAULT_DNT = os.getenv("SCRAPER_DNT", "1")



# =====================================================================
# 3.2 PLAYWRIGHT ENGINE (app/playwright_engine.py, app/browser.py)
#     Настройки движка браузерной автоматизации. Идентичность клиента
#     (User-Agent, viewport, locale, timezone) уже берется из Request
#     Profile Manager (см. раздел 3 выше) — здесь только специфичные
#     для Playwright параметры навигации, не дублирующие эти значения.
# =====================================================================

# Таймаут навигации/ожидания селекторов Playwright (миллисекунды).
# По умолчанию — общий TIMEOUT проекта (секунды), переведенный в мс,
# чтобы не дублировать еще одно значение по умолчанию.
PLAYWRIGHT_TIMEOUT_MS = _get_int("PLAYWRIGHT_TIMEOUT_MS", TIMEOUT * 1000)

# Условие, при котором навигация (`page.goto()`) считается завершенной:
# "load", "domcontentloaded", "networkidle" или "commit".
PLAYWRIGHT_WAIT_UNTIL = os.getenv("PLAYWRIGHT_WAIT_UNTIL", "load").strip().lower()


# =====================================================================
# 3.3 INFINITE SCROLL (app/infinite_scroll.py)
#     Настройки централизованного компонента бесконечного скроллинга.
#     Не хранит селекторы конкретных сайтов — только поведение скроллинга
#     и условия остановки, полностью настраиваемые через .env.
# =====================================================================

# Включает/выключает бесконечный скроллинг. Если выключен,
# `InfiniteScroll.scroll()` сразу возвращается без единой прокрутки.
INFINITE_SCROLL_ENABLED = _get_bool("INFINITE_SCROLL_ENABLED", "1")

# Максимальное количество итераций скроллинга. 0 — без ограничения
# (в этом случае должно быть настроено хотя бы одно другое условие
# остановки, иначе цикл может выполняться до timeout/no_new_content).
INFINITE_SCROLL_MAX_SCROLLS = _get_int("INFINITE_SCROLL_MAX_SCROLLS", 20)

# Общий таймаут цикла скроллинга (секунды). 0 — без ограничения.
INFINITE_SCROLL_TIMEOUT_SECONDS = float(os.getenv("INFINITE_SCROLL_TIMEOUT_SECONDS", "60"))

# Высота страницы (px), при достижении которой скроллинг останавливается.
# 0 — без ограничения по высоте.
INFINITE_SCROLL_MAX_PAGE_HEIGHT = _get_int("INFINITE_SCROLL_MAX_PAGE_HEIGHT", 0)

# Число последовательных прокруток без увеличения высоты страницы, после
# которого считается, что новый контент больше не подгружается.
INFINITE_SCROLL_MAX_NO_NEW_CONTENT = _get_int("INFINITE_SCROLL_MAX_NO_NEW_CONTENT", 3)

# Шаг прокрутки в пикселях. 0 — скроллить сразу к текущему низу страницы
# (`document.body.scrollHeight`) на каждой итерации.
INFINITE_SCROLL_STEP_PX = _get_int("INFINITE_SCROLL_STEP_PX", 0)

# Плавная (smooth) прокрутка вместо мгновенной.
INFINITE_SCROLL_SMOOTH = _get_bool("INFINITE_SCROLL_SMOOTH", "0")

# Ожидать состояние "networkidle" после каждого скролла — полезно для
# сайтов, подгружающих контент через задержанные XHR/fetch запросы.
INFINITE_SCROLL_WAIT_NETWORK_IDLE = _get_bool("INFINITE_SCROLL_WAIT_NETWORK_IDLE", "0")

# Политика паузы между итерациями скроллинга (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
INFINITE_SCROLL_DELAY_MODE = os.getenv("INFINITE_SCROLL_DELAY_MODE", "random").strip().lower()
INFINITE_SCROLL_DELAY_FIXED_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_FIXED_SECONDS", "1.0"))
INFINITE_SCROLL_DELAY_MIN_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MIN_SECONDS", "0.5"))
INFINITE_SCROLL_DELAY_MAX_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MAX_SECONDS", "1.5"))


# =====================================================================
# 3.4 PAGINATION (app/pagination.py)
#     Настройки централизованного компонента пагинации.
#     Не хранит селекторы конкретных сайтов — только стратегию
#     пагинации, лимиты и поведение, полностью настраиваемые через .env.
# =====================================================================

# Максимальное количество страниц. 0 — без ограничения.
PAGINATION_MAX_PAGES = _get_int("PAGINATION_MAX_PAGES", 0)

# Общий таймаут цикла пагинации (секунды). 0 — без ограничения.
PAGINATION_TIMEOUT_SECONDS = float(os.getenv("PAGINATION_TIMEOUT_SECONDS", "0"))

# Включает обнаружение дублирующихся страниц (по dedupe_key из fetch_callback).
PAGINATION_DUPLICATE_DETECTION = _get_bool("PAGINATION_DUPLICATE_DETECTION", "0")

# --- URL-пагинация ---
# Имя query-параметра для номера страницы (например, "page").
PAGINATION_PAGE_PARAM = os.getenv("PAGINATION_PAGE_PARAM", "page").strip().lower()
# Начальное значение счётчика страниц.
PAGINATION_START_PAGE = _get_int("PAGINATION_START_PAGE", 1)
# Шаг счётчика страниц.
PAGINATION_PAGE_STEP = _get_int("PAGINATION_PAGE_STEP", 1)

# --- Offset-пагинация ---
# Имя query-параметра для offset (например, "offset").
PAGINATION_OFFSET_PARAM = os.getenv("PAGINATION_OFFSET_PARAM", "offset").strip().lower()
# Начальное значение offset.
PAGINATION_START_OFFSET = _get_int("PAGINATION_START_OFFSET", 0)
# Шаг offset.
PAGINATION_OFFSET_STEP = _get_int("PAGINATION_OFFSET_STEP", 20)

# Политика паузы между страницами (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
PAGINATION_DELAY_MODE = os.getenv("PAGINATION_DELAY_MODE", "random").strip().lower()
PAGINATION_DELAY_FIXED_SECONDS = float(os.getenv("PAGINATION_DELAY_FIXED_SECONDS", "2.0"))
PAGINATION_DELAY_MIN_SECONDS = float(os.getenv("PAGINATION_DELAY_MIN_SECONDS", "1.0"))
PAGINATION_DELAY_MAX_SECONDS = float(os.getenv("PAGINATION_DELAY_MAX_SECONDS", "3.0"))


# =====================================================================
# 3.5 LOGIN SUPPORT (app/login_manager.py)
#     Настройки централизованного компонента аутентификации.
#     Не хранит учетные данные/URL/селекторы конкретных сайтов — только
#     лимиты, тайм-ауты и имена заголовков, полностью настраиваемые
#     через .env.
# =====================================================================

# Максимальное количество попыток логина (см. LoginManager.login()).
# Повтор пропускается автоматически при "окончательных" причинах сбоя
# (invalid_credentials, captcha_detected, missing_form) независимо от
# этого значения — см. _NON_RETRYABLE_REASONS в app/login_manager.py.
LOGIN_MAX_ATTEMPTS = _get_int("LOGIN_MAX_ATTEMPTS", 3)

# Тайм-аут одной попытки логина (секунды). В текущей реализации
# используется как рекомендованное значение для передачи в
# RequestsEngine/PlaywrightEngine вызывающим кодом (сами движки уже
# имеют собственный TIMEOUT/PLAYWRIGHT_TIMEOUT_MS — это отдельная,
# более узкая настройка именно для операции логина).
LOGIN_TIMEOUT_SECONDS = _get_int("LOGIN_TIMEOUT_SECONDS", TIMEOUT)

# Срок жизни аутентифицированной логической сессии (секунды) в памяти
# LoginManager (`ensure_login()` выполнит повторный логин по истечении).
# 0 — без ограничения по времени (сессия считается валидной, пока не
# инвалидирована явно через `LoginManager.invalidate_session()`).
LOGIN_SESSION_LIFETIME_SECONDS = _get_int("LOGIN_SESSION_LIFETIME_SECONDS", 1800)

# Сохранять ли куки после успешного логина через Cookie Manager
# (для восстановления сессии в будущих запусках через CookieSessionStrategy).
LOGIN_COOKIE_PERSISTENCE = _get_bool("LOGIN_COOKIE_PERSISTENCE", "1")

# Имя HTTP-заголовка для BearerTokenStrategy.
LOGIN_BEARER_HEADER_NAME = os.getenv("LOGIN_BEARER_HEADER_NAME", "Authorization")

# Имя HTTP-заголовка для ApiKeyStrategy.
LOGIN_API_KEY_HEADER_NAME = os.getenv("LOGIN_API_KEY_HEADER_NAME", "X-API-Key")

# Ключевые слова для обнаружения CAPTCHA в HTML (LoginDetector.contains_captcha()),
# через запятую, регистронезависимо.
LOGIN_CAPTCHA_KEYWORDS: List[str] = [
    keyword.strip().lower()
    for keyword in os.getenv("LOGIN_CAPTCHA_KEYWORDS", "captcha,recaptcha,hcaptcha,are you a robot").split(",")
    if keyword.strip()
]


# =====================================================================
# 3.6 HTML PARSER (app/html_parser.py)
#     Настройки централизованного слоя обработки HTML через BeautifulSoup.
#     Не хранит селекторы конкретных сайтов — только бэкенд-парсер,
#     полностью настраиваемый через .env.
# =====================================================================

# Парсер-бэкенд BeautifulSoup: "html.parser" (встроенный, без доп. зависимостей),
# "lxml" (быстрее, требует пакет lxml) или "html5lib" (максимально терпимый к
# невалидной разметке, требует пакет html5lib). По умолчанию — "html.parser",
# так как lxml/html5lib не входят в requirements.txt проекта по умолчанию.
HTML_PARSER_BACKEND = os.getenv("HTML_PARSER_BACKEND", "html.parser").strip().lower()


# =====================================================================
# 3.7 DATA VALIDATION (app/data_validator.py)
#     Настройки централизованного компонента валидации спарсенных
#     записей перед экспортом. Не хранит правила полей конкретного
#     сайта/заказа (это программный API `FieldRule`) — только поведение
#     встроенных type-валидаторов, полностью настраиваемое через .env.
# =====================================================================

# Включает обнаружение дублирующихся записей по умолчанию в
# `DataValidator.validate_records()` (можно переопределить явным
# аргументом `detect_duplicates` при вызове).
DATA_VALIDATION_DUPLICATE_DETECTION = _get_bool("DATA_VALIDATION_DUPLICATE_DETECTION", "0")

# Требовать ли обязательную схему (http:// или https://) для полей типа URL.
DATA_VALIDATION_URL_REQUIRE_SCHEME = _get_bool("DATA_VALIDATION_URL_REQUIRE_SCHEME", "1")

# Допустимый диапазон количества цифр для полей типа PHONE (после удаления
# всех нецифровых символов — пробелов, дефисов, скобок, кода страны "+").
DATA_VALIDATION_PHONE_MIN_DIGITS = _get_int("DATA_VALIDATION_PHONE_MIN_DIGITS", 7)
DATA_VALIDATION_PHONE_MAX_DIGITS = _get_int("DATA_VALIDATION_PHONE_MAX_DIGITS", 15)

# Список допустимых форматов даты (Python `strptime`), через запятую.
# Значение считается валидной датой, если совпадает хотя бы с одним форматом.
DATA_VALIDATION_DATE_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv("DATA_VALIDATION_DATE_FORMATS", "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%Y-%m-%dT%H:%M:%S").split(",")
    if fmt.strip()
]


# =====================================================================
# 3.8 DATA NORMALIZATION (app/data_normalizer.py)
#     Настройки централизованного слоя приведения спарсенных значений
#     к консистентному формату (числа, bool, даты, валюта, URL, страны).
#     Не хранит правила полей конкретного сайта/заказа (это программный
#     API `NormalizationRule`) — только словари/списки распознаваемых
#     значений и форматы вывода, полностью настраиваемые через .env.
# =====================================================================

# Текстовые представления, распознаваемые `DataNormalizer.normalize_bool()`
# как True/False (через запятую, регистронезависимо, сравнение по .lower()).
DATA_NORMALIZATION_BOOL_TRUE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_TRUE_VALUES",
        "true,1,yes,y,in stock,instock,available,да,есть,в наличии",
    ).split(",")
    if value.strip()
]
DATA_NORMALIZATION_BOOL_FALSE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_FALSE_VALUES",
        "false,0,no,n,out of stock,outofstock,unavailable,нет,отсутствует,нет в наличии",
    ).split(",")
    if value.strip()
]

# Список форматов даты (Python `strptime`), которые пробует
# `DataNormalizer.normalize_date()`/`normalize_timestamp()` по порядку,
# через запятую. Первый успешно разобранный формат используется.
DATA_NORMALIZATION_DATE_INPUT_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv(
        "DATA_NORMALIZATION_DATE_INPUT_FORMATS",
        "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%d/%m/%Y,%Y-%m-%dT%H:%M:%S,%B %d, %Y,%d %B %Y",
    ).split(",")
    if fmt.strip()
]

# Единый выходной формат даты для `DataNormalizer.normalize_date()`.
DATA_NORMALIZATION_DATE_OUTPUT_FORMAT = os.getenv("DATA_NORMALIZATION_DATE_OUTPUT_FORMAT", "%Y-%m-%d")

# Соответствия символ/название валюты -> ISO-код, для
# `DataNormalizer.normalize_currency()`. Формат: "символ:КОД", записи через
# запятую (например, "$:USD,€:EUR,₴:UAH"). Порядок важен только для
# читаемости — поиск в тексте выполняется по всем ключам.
DATA_NORMALIZATION_CURRENCY_SYMBOLS: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip().upper()
    for pair in os.getenv(
        "DATA_NORMALIZATION_CURRENCY_SYMBOLS",
        "$:USD,€:EUR,£:GBP,₴:UAH,₽:RUB,zł:PLN,грн:UAH,руб:RUB",
    ).split(",")
    if ":" in pair
}

# Схема по умолчанию, добавляемая `DataNormalizer.normalize_url()` к
# protocol-relative ("//example.com/...") и бесхема ("example.com/...") URL.
DATA_NORMALIZATION_URL_DEFAULT_SCHEME = os.getenv("DATA_NORMALIZATION_URL_DEFAULT_SCHEME", "https").strip().lower()

# Сохранять ли ведущий "+" (код страны) в `DataNormalizer.normalize_phone()`.
DATA_NORMALIZATION_PHONE_KEEP_PLUS = _get_bool("DATA_NORMALIZATION_PHONE_KEEP_PLUS", "1")

# Псевдонимы названий/кодов стран -> каноническое название, для
# `DataNormalizer.normalize_country()`. Формат: "псевдоним:Каноническое",
# записи через запятую (сравнение псевдонимов регистронезависимо).
DATA_NORMALIZATION_COUNTRY_ALIASES: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip()
    for pair in os.getenv(
        "DATA_NORMALIZATION_COUNTRY_ALIASES",
        "US:United States,USA:United States,U.S.:United States,U.S.A.:United States,"
        "UK:United Kingdom,U.K.:United Kingdom,GB:United Kingdom,"
        "UA:Ukraine,Ukraine:Ukraine,Украина:Ukraine,"
        "RU:Russia,Russian Federation:Russia,"
        "PL:Poland,Poland:Poland,"
        "DE:Germany,Germany:Germany",
    ).split(",")
    if ":" in pair
}


# =====================================================================
# 3.9 INCREMENTAL SAVING (app/exporter.py)
#     Настройки централизованного механизма прогрессивного сохранения
#     спарсенных записей во время скрапинга (вместо накопления всего
#     набора данных в памяти и экспорта единым вызовом в самом конце).
#     Не хранит формат/структуру записей конкретного сайта/заказа —
#     только поведение самого механизма записи, полностью настраиваемое
#     через .env.
# =====================================================================

# Включает/выключает Incremental Saving в `app/main.py`. При выключении
# сохраняется прежнее (batch) поведение: все записи копятся в памяти и
# экспортируются одним вызовом `save_to_csv`/`save_to_json` после
# завершения скрапинга — обратная совместимость с поведением до появления
# Incremental Saving.
EXPORT_INCREMENTAL_ENABLED = _get_bool("EXPORT_INCREMENTAL_ENABLED", "1")

# Принудительно сбрасывать буфер ОС на диск (`file.flush()` + `os.fsync()`)
# после каждой записи/пачки записей. Повышает устойчивость к потере данных
# при сбое (данные гарантированно физически на диске), но снижает
# производительность на очень больших объёмах — поэтому настраивается,
# а не хардкодится.
EXPORT_INCREMENTAL_FLUSH_ON_WRITE = _get_bool("EXPORT_INCREMENTAL_FLUSH_ON_WRITE", "1")


# =====================================================================
# 3.10 BATCH WRITER (app/exporter.py)
#      Настройки централизованного буферизующего слоя, оборачивающего
#      писатели Incremental Saving (IncrementalCSVWriter/JSONWriter).
#      Вместо записи на диск при каждом вызове write_records(), записи
#      копятся в памяти и сбрасываются пачками — уменьшая количество
#      операций записи на диск на больших объёмах данных. Не хранит
#      формат/структуру записей конкретного сайта/заказа — только
#      поведение самого буфера, полностью настраиваемое через .env.
# =====================================================================

# Максимальное количество записей, накапливаемых в буфере до
# автоматического сброса на диск (см. BatchWriter.add_records()).
BATCH_WRITER_BATCH_SIZE = _get_int("BATCH_WRITER_BATCH_SIZE", 100)

# Включает автоматический сброс буфера при достижении BATCH_WRITER_BATCH_SIZE.
# При выключении буфер растет неограниченно до явного вызова flush()/close() —
# использовать с осторожностью только под контролем вызывающего кода.
BATCH_WRITER_AUTO_FLUSH_ENABLED = _get_bool("BATCH_WRITER_AUTO_FLUSH_ENABLED", "1")

# Сбрасывать оставшиеся в буфере записи при завершении работы
# (BatchWriter.close() / выход из контекстного менеджера), чтобы
# ни одна накопленная запись не была потеряна при штатном завершении.
BATCH_WRITER_FLUSH_ON_SHUTDOWN = _get_bool("BATCH_WRITER_FLUSH_ON_SHUTDOWN", "1")


# =====================================================================
# 3.11 CHECKPOINT MANAGER (app/checkpoint_manager.py)
#      Настройки централизованного механизма периодического сохранения
#      прогресса скрапинга на диск (см. `tasks/TASK.md` и
#      `framework/ROADMAP.md`, Milestone 6). Checkpoint Manager только
#      ЗАПИСЫВАЕТ прогресс — он не восстанавливает и не продолжает
#      скрапинг (это будущий Resume Support, потребляющий сохраненные
#      здесь checkpoint-файлы). Не хранит логику конкретного
#      сайта/заказа — только поведение самого механизма чекпоинтинга,
#      полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает создание чекпоинтов. При выключении вызовы
# `CheckpointManager.record_page()`/`record_records()` становятся no-op —
# обратная совместимость с поведением до появления Checkpoint Manager.
CHECKPOINT_ENABLED = _get_bool("CHECKPOINT_ENABLED", "1")

# Путь к файлу чекпоинта. По умолчанию — рядом с cookies.json/proxy_cache.json
# в AI_INPUT_DIR, по аналогии с уже существующими персистентными файлами
# состояния (COOKIES_FILE, PROXY_CACHE_FILE).
CHECKPOINT_FILE = Path(os.getenv("CHECKPOINT_FILE_PATH", str(AI_INPUT_DIR / "checkpoint.json")))

# Создавать новый чекпоинт раз в N обработанных страниц. 0 — не учитывать
# количество страниц как условие сохранения.
CHECKPOINT_INTERVAL_PAGES = _get_int("CHECKPOINT_INTERVAL_PAGES", 1)

# Создавать новый чекпоинт раз в N обработанных записей. 0 — не учитывать
# количество записей как условие сохранения.
CHECKPOINT_INTERVAL_RECORDS = _get_int("CHECKPOINT_INTERVAL_RECORDS", 0)

# Создавать новый чекпоинт не чаще, чем раз в N секунд (даже если условия
# по страницам/записям сработали раньше — не даёт чекпоинтингу создавать
# избыточную нагрузку на диск при очень частых страницах/записях). 0 —
# не учитывать время как условие (полагаться только на pages/records).
CHECKPOINT_INTERVAL_SECONDS = float(os.getenv("CHECKPOINT_INTERVAL_SECONDS", "0"))

# Политика хранения файлов чекпоинта:
#   "overwrite"   — всегда перезаписывать один и тот же файл (CHECKPOINT_FILE);
#   "timestamped" — дополнительно сохранять с суффиксом-таймстампом,
#                   сохраняя историю чекпоинтов (полезно для отладки/аудита).
CHECKPOINT_OVERWRITE_POLICY = os.getenv("CHECKPOINT_OVERWRITE_POLICY", "overwrite").strip().lower()


# =====================================================================
# 3.12 RESUME SUPPORT (app/resume_manager.py)
#      Настройки централизованного механизма автоматического продолжения
#      прерванной сессии скрапинга на основе чекпоинтов, сохраненных
#      Checkpoint Manager'ом (см. `tasks/TASK.md` и `framework/ROADMAP.md`,
#      Milestone 6). Resume Support только ЧИТАЕТ и валидирует чекпоинты —
#      он не создает их сам (это ответственность Checkpoint Manager) и не
#      знает о логике конкретного сайта/заказа — только поведение самого
#      механизма восстановления, полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает автоматическое обнаружение и восстановление
# прерванной сессии при старте. При выключении сохраняется прежнее
# поведение: скрапинг всегда начинается "с нуля" — обратная
# совместимость с поведением до появления Resume Support.
RESUME_ENABLED = _get_bool("RESUME_ENABLED", "1")

# Максимальный "возраст" чекпоинта (в секундах), при котором он ещё
# считается пригодным для восстановления. 0 — не ограничивать возраст
# (восстанавливать независимо от давности последнего сохранения).
RESUME_MAX_AGE_SECONDS = _get_int("RESUME_MAX_AGE_SECONDS", 0)

# Резервируется для будущего интерактивного подтверждения перед
# восстановлением (см. TASK.md, "Future versions may optionally ask
# the user whether to resume or restart"). Пока не используется в коде —
# уже присутствует в конфигурации, чтобы включение такого режима в
# будущем не требовало правок app/config.py.
RESUME_CONFIRMATION_REQUIRED = _get_bool("RESUME_CONFIRMATION_REQUIRED", "0")


# =====================================================================
# 4. ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ПУТЕЙ

# =====================================================================



if __name__ == "__main__":
    print(f"[{__file__}] Проверка путей конфигурации:")
    print(f"  Корень проекта (ROOT_DIR): {ROOT_DIR}")
    print(f"  Папка вывода (OUTPUT_DIR): {OUTPUT_DIR}")
    print(f"  Файл кук (COOKIES_FILE):   {COOKIES_FILE}")
    print(f"  Тестовый HTML (PAGE_HTML_FILE): {PAGE_HTML_FILE}")
    print(f"  Режим Headless:            {HEADLESS}")
    print(f"  Запуск в Docker:           {IS_DOCKER}")
    print(f"  Таймаут:                   {TIMEOUT}s, Повторы: {RETRY_COUNT}")
    print(f"  Viewport:                  {BROWSER_VIEWPORT}")
    print(f"  Locale/Timezone:           {BROWSER_LOCALE} / {BROWSER_TIMEZONE}")


--- app/cookie_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cookie Manager.

Единый компонент, отвечающий за загрузку, сохранение, обновление и очистку
HTTP-куки для всего фреймворка.

Cookie Manager:

* хранит куки в простом JSON-файле (по умолчанию `app/config.py::COOKIES_FILE`);
* валидирует формат куки перед применением;
* предоставляет куки для `requests.Session` (Session Manager);
* предоставляет куки для контекста Playwright (готово для будущей интеграции).

Формат хранения — список словарей вида Playwright/Puppeteer:
    {"name": str, "value": str, "domain": str, "path": str, ...}
Это универсальный, широко используемый формат, легко конвертируемый как в
`requests.cookies.RequestsCookieJar`, так и в `BrowserContext.add_cookies()`.

Cookie Manager НЕ создает HTTP-сессии, НЕ выполняет запросы, НЕ управляет
прокси/повторами/задержками и НЕ содержит логики скрапинга.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import COOKIES_FILE

# Минимально обязательные поля, без которых куки считаются невалидными.
_REQUIRED_COOKIE_FIELDS = ("name", "value")


class CookieManager:
    """
    Централизованный менеджер персистентных HTTP-куки.

    Хранилище по умолчанию — JSON-файл (`COOKIES_FILE`). Для миграции на
    другое хранилище (например, БД) достаточно переопределить методы
    `load`/`save`/`clear` — остальные методы (`apply_to_session`,
    `apply_to_playwright_context`, `_validate`) не зависят от способа хранения.
    """

    @staticmethod
    def _validate(cookies: Any) -> List[Dict[str, Any]]:
        """
        Проверяет, что куки представлены списком словарей с обязательными
        полями `name` и `value`. Невалидные записи отбрасываются с
        предупреждением, чтобы не блокировать работу всего фреймворка.

        Args:
            cookies (Any): Сырые данные, прочитанные из хранилища.

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список валидных куки.
        """
        if not isinstance(cookies, list):
            print(f"[{__file__}] Ошибка формата: ожидался список куки, получено {type(cookies)}")
            return []

        valid_cookies = []
        for cookie in cookies:
            if isinstance(cookie, dict) and all(field in cookie for field in _REQUIRED_COOKIE_FIELDS):
                valid_cookies.append(cookie)
            else:
                print(f"[{__file__}] Предупреждение: пропущена невалидная запись куки: {cookie}")

        return valid_cookies

    @classmethod
    def load(cls, path: Path = COOKIES_FILE) -> List[Dict[str, Any]]:
        """
        Загружает и валидирует куки из JSON-файла.

        Args:
            path (Path): Путь к файлу хранения куки.

        Returns:
            List[Dict[str, Any]]: Список валидных куки (пустой, если файл
                отсутствует, пуст или содержит некорректные данные).
        """
        if not path.exists() or path.stat().st_size == 0:
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_cookies = json.load(f)
        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке куки из {path.name}: {e}")
            return []

        return cls._validate(raw_cookies)

    @classmethod
    def save(cls, cookies: List[Dict[str, Any]], path: Path = COOKIES_FILE) -> None:
        """
        Сохраняет куки в JSON-файл, перезаписывая предыдущее содержимое.

        Args:
            cookies (List[Dict[str, Any]]): Список куки для сохранения.
            path (Path): Путь к файлу хранения куки.
        """
        valid_cookies = cls._validate(cookies)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(valid_cookies, f, ensure_ascii=False, indent=2)
            print(f"[{__file__}] Куки сохранены в {path.name} (Всего: {len(valid_cookies)})")
        except Exception as e:
            print(f"[{__file__}] Ошибка при сохранении куки в {path.name}: {e}")

    @classmethod
    def update(cls, new_cookies: List[Dict[str, Any]], path: Path = COOKIES_FILE) -> List[Dict[str, Any]]:
        """
        Обновляет существующие куки новыми значениями (по совпадению
        `name` + `domain`) и добавляет отсутствующие, затем сохраняет результат.

        Args:
            new_cookies (List[Dict[str, Any]]): Новые/обновленные куки
                (например, полученные после успешного запроса).
            path (Path): Путь к файлу хранения куки.

        Returns:
            List[Dict[str, Any]]: Итоговый объединенный список куки.
        """
        existing = cls.load(path)
        valid_new = cls._validate(new_cookies)

        index = {(c.get("name"), c.get("domain")): i for i, c in enumerate(existing)}
        for cookie in valid_new:
            key = (cookie.get("name"), cookie.get("domain"))
            if key in index:
                existing[index[key]] = cookie
            else:
                existing.append(cookie)

        cls.save(existing, path)
        return existing

    @classmethod
    def clear(cls, path: Path = COOKIES_FILE) -> None:
        """
        Очищает хранилище куки (перезаписывает файл пустым списком).

        Args:
            path (Path): Путь к файлу хранения куки.
        """
        cls.save([], path)
        print(f"[{__file__}] Куки очищены: {path.name}")

    @staticmethod
    def apply_to_session(session, cookies: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Применяет куки к `requests.Session`, предоставляя их Session Manager.

        Args:
            session (requests.Session): Сессия, к которой будут применены куки.
            cookies (List[Dict[str, Any]], optional): Список куки. Если не
                передан, куки загружаются из хранилища по умолчанию.
        """
        active_cookies = cookies if cookies is not None else CookieManager.load()
        for cookie in active_cookies:
            session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain", ""),
                path=cookie.get("path", "/"),
            )

        if active_cookies:
            print(f"[{__file__}] Куки применены к сессии (Всего: {len(active_cookies)})")

    @staticmethod
    def apply_to_playwright_context(context, cookies: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Применяет куки к контексту Playwright (`BrowserContext.add_cookies`).

        Args:
            context (BrowserContext): Контекст браузера Playwright.
            cookies (List[Dict[str, Any]], optional): Список куки. Если не
                передан, куки загружаются из хранилища по умолчанию.
        """
        active_cookies = cookies if cookies is not None else CookieManager.load()
        if not active_cookies:
            return

        try:
            context.add_cookies(active_cookies)
            print(f"[{__file__}] Куки применены к контексту Playwright (Всего: {len(active_cookies)})")
        except Exception as e:
            print(f"[{__file__}] Ошибка при применении куки к контексту Playwright: {e}")


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    sample_cookies = [
        {"name": "session_id", "value": "abc123", "domain": "example.com", "path": "/"},
        {"name": "invalid_entry"},  # будет отбракован при валидации
    ]

    print(f"[{__file__}] Сохранение тестовых куки...")
    CookieManager.save(sample_cookies)

    loaded = CookieManager.load()
    print(f"[{__file__}] Загружено куки: {loaded}")

    CookieManager.update([{"name": "session_id", "value": "updated456", "domain": "example.com", "path": "/"}])
    print(f"[{__file__}] После обновления: {CookieManager.load()}")

    CookieManager.clear()
    print(f"[{__file__}] После очистки: {CookieManager.load()}")


--- app/data_normalizer.py ---
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


--- app/data_validator.py ---
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


--- app/delay_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Delay Manager.

Единый компонент, отвечающий за паузы между запросами — помогает
имитировать естественное поведение пользователя и снижать риск блокировок
по Rate Limiting.

Delay Manager:

* поддерживает фиксированные и случайные (в диапазоне) задержки;
* берет политику задержек (режим, диапазон, фиксированное значение) из
  Configuration Manager (`app/config.py`);
* переиспользует существующую функцию `random_delay()` из `app/utils.py`
  вместо повторной реализации `random.uniform` + `time.sleep`.

Delay Manager НЕ выполняет HTTP-запросы, НЕ выполняет повторы, НЕ управляет
куками/прокси/User-Agent и НЕ содержит логики скрапинга — это ответственность
других компонентов (Session Manager, Retry Manager, Cookie Manager,
будущий Proxy Manager).
"""

import time
from typing import Optional

from app import config
from app.utils import random_delay


class DelayManager:
    """
    Централизованная политика пауз между запросами.

    Поддерживает два режима, конфигурируемых через `app/config.py`:
    * "fixed"  — постоянная пауза длительностью `config.DELAY_FIXED_SECONDS`;
    * "random" — случайная пауза в диапазоне
      [`config.DELAY_MIN_SECONDS`, `config.DELAY_MAX_SECONDS`].
    """

    @staticmethod
    def wait_fixed(seconds: Optional[float] = None) -> None:
        """
        Выполняет фиксированную паузу.

        Args:
            seconds (float, optional): Длительность паузы в секундах.
                По умолчанию — `config.DELAY_FIXED_SECONDS`.
        """
        delay = seconds if seconds is not None else config.DELAY_FIXED_SECONDS
        time.sleep(delay)

    @staticmethod
    def wait_random(min_seconds: Optional[float] = None, max_seconds: Optional[float] = None) -> None:
        """
        Выполняет случайную паузу в заданном диапазоне.

        Переиспользует `app.utils.random_delay()` — не дублирует логику
        генерации случайной задержки.

        Args:
            min_seconds (float, optional): Минимум паузы.
                По умолчанию — `config.DELAY_MIN_SECONDS`.
            max_seconds (float, optional): Максимум паузы.
                По умолчанию — `config.DELAY_MAX_SECONDS`.
        """
        low = min_seconds if min_seconds is not None else config.DELAY_MIN_SECONDS
        high = max_seconds if max_seconds is not None else config.DELAY_MAX_SECONDS
        random_delay(low, high)

    @classmethod
    def wait(cls, mode: Optional[str] = None) -> None:
        """
        Выполняет паузу согласно текущей политике задержек
        (`config.DELAY_MODE`, если `mode` не передан явно).

        Это основная точка входа, которую должны использовать будущие
        компоненты (Requests Engine, Playwright Engine) между запросами.

        Args:
            mode (str, optional): "fixed" или "random". По умолчанию —
                `config.DELAY_MODE`.
        """
        active_mode = (mode or config.DELAY_MODE).strip().lower()

        if active_mode == "fixed":
            cls.wait_fixed()
        elif active_mode == "random":
            cls.wait_random()
        else:
            print(f"[{__file__}] Предупреждение: неизвестный режим задержки '{active_mode}', "
                  f"используется 'random' по умолчанию.")
            cls.wait_random()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Текущая политика: mode={config.DELAY_MODE}, "
          f"fixed={config.DELAY_FIXED_SECONDS}s, "
          f"random=[{config.DELAY_MIN_SECONDS}s, {config.DELAY_MAX_SECONDS}s]")

    print(f"[{__file__}] Тест wait_fixed(0.2)...")
    start = time.time()
    DelayManager.wait_fixed(0.2)
    print(f"  Прошло: {time.time() - start:.2f}с")

    print(f"[{__file__}] Тест wait_random(0.1, 0.3)...")
    start = time.time()
    DelayManager.wait_random(0.1, 0.3)
    print(f"  Прошло: {time.time() - start:.2f}с")

    print(f"[{__file__}] Тест wait() согласно политике из конфигурации...")
    start = time.time()
    DelayManager.wait()
    print(f"  Прошло: {time.time() - start:.2f}с")


--- app/exporter.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export Layer.

Содержит три режима сохранения результатов скрапинга:

1. Batch-экспорт (`save_to_csv`, `save_to_json`) — исходное поведение
   проекта. Принимает уже полностью собранный список записей и
   записывает его в файл одним вызовом. Подходит для небольших
   датасетов, оставлен без изменений для обратной совместимости.

2. Incremental Saving (`IncrementalCSVWriter`, `IncrementalJSONWriter`) —
   механизм из Milestone 6 (см. `framework/ROADMAP.md`). Вместо
   накопления всех записей в памяти и одного финального вызова
   экспорта, писатель открывается один раз в начале скрапинга и
   постепенно дозаписывает порции записей на диск по мере их появления
   (`write_records()`), после чего явно закрывается (`close()`) для
   корректного завершения файла.

   Это минимизирует потерю данных при сбоях/прерываниях (уже записанные
   записи остаются на диске) и уменьшает потребление памяти на больших
   объёмах данных (сотни тысяч записей не нужно держать в списке).

3. Batch Writer (`BatchWriter`) — буферизующий слой (см. `tasks/TASK.md`
   и `framework/ROADMAP.md`, Milestone 6), оборачивающий один или
   несколько писателей Incremental Saving. Вместо записи на диск при
   каждом вызове `write_records()` отдельного писателя, `BatchWriter`
   накапливает записи в памяти и сбрасывает их пачками — либо
   автоматически при достижении настроенного размера батча
   (`add_records()`), либо явно (`flush()`), либо при завершении работы
   (`close()`). Это значительно уменьшает количество операций записи на
   диск на больших датасетах, сохраняя устойчивость к сбоям Incremental
   Saving для уже сброшенных данных.

Поведение управляется через Configuration Manager (`app/config.py`,
секции 3.9 INCREMENTAL SAVING и 3.10 BATCH WRITER) — без хардкода в коде:
    EXPORT_INCREMENTAL_ENABLED         — включает Incremental Saving в main.py
    EXPORT_INCREMENTAL_FLUSH_ON_WRITE  — принудительный flush+fsync после записи
    BATCH_WRITER_BATCH_SIZE            — размер батча для автоматического сброса
    BATCH_WRITER_AUTO_FLUSH_ENABLED    — включает автосброс при достижении размера батча
    BATCH_WRITER_FLUSH_ON_SHUTDOWN     — сбрасывать остаток буфера при close()
"""

import csv
import json
import os
from typing import Any, Dict, List, Optional, Protocol

from app.config import (
    OUTPUT_DIR,
    EXPORT_INCREMENTAL_FLUSH_ON_WRITE,
    BATCH_WRITER_BATCH_SIZE,
    BATCH_WRITER_AUTO_FLUSH_ENABLED,
    BATCH_WRITER_FLUSH_ON_SHUTDOWN,
)
from app.utils import log_message


# =========================================================================
# BATCH EXPORT (исходное поведение проекта — не изменялось)
# =========================================================================


def save_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Сохраняет список словарей в CSV файл.
    Автоматически берет ключи первого словаря в качестве заголовков.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в CSV.")
        return ""

    # Если расширение не указано, добавляем его
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = OUTPUT_DIR / filename

    # Берем заголовки из ключей первого элемента
    fieldnames = list(data[0].keys())

    try:
        # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"[{__file__}] Данные успешно сохранены в CSV: {filepath.name} (Строк: {len(data)})")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в CSV: {e}")
        return ""


def save_to_json(data: List[Dict[str, Any]], filename: str, indent: int = 4) -> str:
    """
    Сохраняет данные в формате JSON с красивыми отступами.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в JSON.")
        return ""

    if not filename.endswith(".json"):
        filename += ".json"

    filepath = OUTPUT_DIR / filename

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        print(f"[{__file__}] Данные успешно сохранены в JSON: {filepath.name}")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в JSON: {e}")
        return ""


# =========================================================================
# INCREMENTAL SAVING
# =========================================================================


class IncrementalCSVWriter:
    """
    Прогрессивно дозаписывает записи в CSV-файл во время скрапинга.

    В отличие от `save_to_csv()`, который получает готовый список и пишет
    его одним вызовом, `IncrementalCSVWriter` открывает файл один раз
    (`open(..., mode="w")`) и держит его открытым на протяжении всей
    сессии скрапинга, дописывая новые записи по мере их появления через
    `write_records()`.

    CSV — построчный формат, поэтому он естественно устойчив к сбоям:
    каждая успешно записанная строка независима, и обрыв процесса просто
    обрезает файл на последней завершённой строке, не повреждая уже
    сохранённые данные.

    Заголовки CSV определяются по ключам первой переданной записи
    (аналогично `save_to_csv`) — на всех последующих вызовах
    `write_records()` ожидаются записи с тем же набором полей.

    Пример использования:

        writer = IncrementalCSVWriter("output_results.csv")
        try:
            for page_records in scrape_pages():
                writer.write_records(page_records)
        finally:
            writer.close()

        # либо как контекстный менеджер:
        with IncrementalCSVWriter("output_results.csv") as writer:
            for page_records in scrape_pages():
                writer.write_records(page_records)
    """

    def __init__(self, filename: str, flush_on_write: Optional[bool] = None, append: bool = False):
        """
        Args:
            filename: Имя выходного файла (относительно `OUTPUT_DIR`).
                Расширение ".csv" добавляется автоматически, если
                отсутствует.
            flush_on_write: Принудительно сбрасывать буфер ОС на диск
                (`flush()` + `os.fsync()`) после каждого вызова
                `write_records()`. По умолчанию —
                `config.EXPORT_INCREMENTAL_FLUSH_ON_WRITE`.
            append: Открыть существующий файл в режиме дозаписи вместо
                перезаписи ("w"). Используется Resume Support
                (`app/resume_manager.py`) для продолжения прерванной
                сессии без потери уже экспортированных строк. Если файл
                не существует или пуст, поведение идентично `append=False`
                (заголовок CSV записывается как обычно). По умолчанию —
                False (полная обратная совместимость с поведением до
                появления Resume Support).
        """
        if not filename.endswith(".csv"):
            filename += ".csv"

        self.filepath = OUTPUT_DIR / filename
        self._flush_on_write = (
            flush_on_write if flush_on_write is not None else EXPORT_INCREMENTAL_FLUSH_ON_WRITE
        )

        self._file = None
        self._writer: Optional[csv.DictWriter] = None
        self._fieldnames: Optional[List[str]] = None
        self._total_written = 0
        self._closed = False

        # Дозапись возможна только если файл реально существует и не пуст —
        # иначе (первый запуск/файл отсутствует) ведём себя как при
        # обычном создании нового файла (пишем заголовок).
        resume_append = append and self.filepath.exists() and self.filepath.stat().st_size > 0

        try:
            # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
            mode = "a" if resume_append else "w"
            self._file = open(self.filepath, mode=mode, encoding="utf-8-sig", newline="")
            if resume_append:
                # Заголовок уже присутствует в существующем файле — писатель
                # переходит прямо в режим дозаписи строк без повторного
                # `writeheader()`. Fieldnames будут определены по первой
                # переданной порции записей (как и при обычном режиме),
                # но `writeheader()` для неё пропускается через `_header_written`.
                self._header_written = True
            else:
                self._header_written = False
            log_message(
                "info",
                f"IncrementalCSVWriter: инициализирован ({self.filepath.name}, "
                f"режим={'дозапись' if resume_append else 'новый файл'})",
            )
        except Exception as exc:
            log_message("error", f"IncrementalCSVWriter: не удалось открыть файл {self.filepath}: {exc}")
            self._file = None
            self._header_written = False


    def write_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Дозаписывает порцию записей в CSV-файл.

        Заголовки CSV фиксируются по первому вызову (по ключам первой
        записи в первой непустой порции) и записываются один раз.

        Если запись какой-либо отдельной строки завершилась ошибкой,
        она логируется, а остальные записи в порции продолжают
        обрабатываться — сбой одной строки не должен обрывать весь
        процесс скрапинга и не затрагивает уже сохранённые данные.

        Args:
            records: Список словарей (одна страница/порция результатов).

        Returns:
            int: Количество успешно записанных строк из этой порции.
        """
        if not records:
            return 0

        if self._file is None or self._closed:
            log_message("error", "IncrementalCSVWriter: попытка записи в закрытый/неоткрытый файл")
            return 0

        written = 0
        try:
            if self._writer is None:
                self._fieldnames = list(records[0].keys())
                self._writer = csv.DictWriter(self._file, fieldnames=self._fieldnames)
                # При дозаписи (Resume Support) заголовок уже существует в
                # файле — повторный writeheader() испортил бы CSV.
                if not self._header_written:
                    self._writer.writeheader()
                    self._header_written = True

            for record in records:
                try:
                    self._writer.writerow(record)
                    written += 1
                except Exception as row_exc:
                    log_message("error", f"IncrementalCSVWriter: сбой записи строки: {row_exc}")

            if self._flush_on_write:
                self._file.flush()
                os.fsync(self._file.fileno())

            self._total_written += written
            log_message("debug", f"IncrementalCSVWriter: записано строк={written} (всего={self._total_written})")
        except Exception as exc:
            log_message("error", f"IncrementalCSVWriter: непредвиденная ошибка записи: {exc}")

        return written


    def close(self) -> None:
        """Закрывает файл. Безопасно вызывать несколько раз."""
        if self._file is not None and not self._closed:
            try:
                self._file.close()
                log_message(
                    "info",
                    f"IncrementalCSVWriter: закрыт ({self.filepath.name}, всего строк={self._total_written})",
                )
            except Exception as exc:
                log_message("error", f"IncrementalCSVWriter: ошибка при закрытии файла: {exc}")
            finally:
                self._closed = True

    @property
    def total_written(self) -> int:
        """Общее количество успешно записанных строк за время жизни писателя."""
        return self._total_written

    def __enter__(self) -> "IncrementalCSVWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


class IncrementalJSONWriter:
    """
    Прогрессивно дозаписывает записи в JSON-файл во время скрапинга.

    JSON-массив не поддерживает построчное дозаписывание "из коробки"
    (в отличие от CSV), поэтому писатель вручную управляет структурой
    файла: открывающая "[" пишется при инициализации, каждая новая
    запись добавляется с корректной запятой-разделителем, а закрывающая
    "]" дописывается при явном `close()`.

    Важный риск: если процесс прерывается до вызова `close()`
    (крах/Ctrl+C/сбой питания), файл останется без завершающей "]" и
    будет невалидным JSON, при этом содержащиеся в нём записи не
    теряются и не повреждаются — файл можно восстановить, дописав "]"
    вручную. Это ограничение самого формата JSON, а не реализации;
    corruption (испорченные незакрытые записи) исключается тем, что
    запись каждого элемента атомарна.

    Пример использования:

        writer = IncrementalJSONWriter("output_results.json")
        try:
            for page_records in scrape_pages():
                writer.write_records(page_records)
        finally:
            writer.close()

        # либо как контекстный менеджер:
        with IncrementalJSONWriter("output_results.json") as writer:
            for page_records in scrape_pages():
                writer.write_records(page_records)
    """

    def __init__(
        self,
        filename: str,
        indent: int = 4,
        flush_on_write: Optional[bool] = None,
        append: bool = False,
    ):
        """
        Args:
            filename: Имя выходного файла (относительно `OUTPUT_DIR`).
                Расширение ".json" добавляется автоматически, если
                отсутствует.
            indent: Отступ для читаемого форматирования каждой записи.
            flush_on_write: Принудительно сбрасывать буфер ОС на диск
                (`flush()` + `os.fsync()`) после каждого вызова
                `write_records()`. По умолчанию —
                `config.EXPORT_INCREMENTAL_FLUSH_ON_WRITE`.
            append: Продолжить дозапись в существующий JSON-массив вместо
                создания нового файла. Используется Resume Support
                (`app/resume_manager.py`) для продолжения прерванной
                сессии без потери уже экспортированных записей.

                Реализация: у существующего файла отыскивается последняя
                закрывающая скобка "]" (независимо от того, успел ли
                предыдущий запуск вызвать `close()` — при аварийном
                завершении её может не быть) и файл обрезается
                (`truncate()`) до этой позиции, чтобы новые записи можно
                было дописать через запятую как продолжение массива.
                Если файл не существует, пуст или в нём нет ни одной
                записи — поведение идентично `append=False` (создаётся
                новый файл). По умолчанию — False (полная обратная
                совместимость с поведением до появления Resume Support).
        """
        if not filename.endswith(".json"):
            filename += ".json"

        self.filepath = OUTPUT_DIR / filename
        self._indent = indent
        self._flush_on_write = (
            flush_on_write if flush_on_write is not None else EXPORT_INCREMENTAL_FLUSH_ON_WRITE
        )

        self._file = None
        self._total_written = 0
        self._closed = False
        self._wrote_any = False

        resume_append = append and self._prepare_append_target()

        try:
            if resume_append:
                self._file = open(self.filepath, mode="a", encoding="utf-8")
                self._wrote_any = True  # файл уже содержит хотя бы одну запись
            else:
                self._file = open(self.filepath, mode="w", encoding="utf-8")
                self._file.write("[\n")
            log_message(
                "info",
                f"IncrementalJSONWriter: инициализирован ({self.filepath.name}, "
                f"режим={'дозапись' if resume_append else 'новый файл'})",
            )
        except Exception as exc:
            log_message("error", f"IncrementalJSONWriter: не удалось открыть файл {self.filepath}: {exc}")
            self._file = None

    def _prepare_append_target(self) -> bool:
        """
        Готовит существующий JSON-файл для дозаписи: находит последнюю
        закрывающую скобку "]" и обрезает файл до этой позиции (удаляет
        завершающую "]" и всё, что после неё, включая случай, когда её
        вовсе нет из-за аварийного завершения предыдущего запуска).

        Returns:
            bool: True, если файл пригоден для дозаписи (существует,
                не пуст, содержит валидную структуру массива с хотя бы
                одной записью). False — вызывающий код должен создать
                новый файл с нуля.
        """
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            return False

        try:
            with open(self.filepath, "r+", encoding="utf-8") as f:
                content = f.read()
                stripped = content.rstrip()

                if not stripped.startswith("["):
                    return False

                # Файл содержит только "[" (или "[\n") без единой записи —
                # нет смысла дозаписывать через запятую, начинаем с чистого листа.
                inner = stripped[1:].rstrip()
                if inner.endswith("]"):
                    inner = inner[:-1].rstrip()
                if not inner:
                    return False

                # Обрезаем до последней закрывающей "]" (если она есть) —
                # это гарантирует корректную дозапись независимо от того,
                # был ли файл штатно закрыт предыдущим запуском.
                cutoff = stripped.rfind("]")
                truncated = (stripped[:cutoff] if cutoff != -1 else stripped).rstrip()

                f.seek(0)
                f.write(truncated)
                f.truncate()
            return True
        except Exception as exc:
            log_message(
                "error",
                f"IncrementalJSONWriter: не удалось подготовить файл {self.filepath.name} для дозаписи: {exc}",
            )
            return False


    def write_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Дозаписывает порцию записей в JSON-массив.

        Каждая запись сериализуется отдельно, поэтому сбой сериализации
        одной записи (например, несериализуемый тип) логируется и
        пропускается, не прерывая запись остальных записей в порции.

        Args:
            records: Список словарей (одна страница/порция результатов).

        Returns:
            int: Количество успешно записанных записей из этой порции.
        """
        if not records:
            return 0

        if self._file is None or self._closed:
            log_message("error", "IncrementalJSONWriter: попытка записи в закрытый/неоткрытый файл")
            return 0

        written = 0
        try:
            for record in records:
                try:
                    serialized = json.dumps(record, ensure_ascii=False, indent=self._indent)
                    # Отступ каждой вложенной записи для читаемости общего массива
                    serialized = "\n".join("  " + line for line in serialized.splitlines())

                    if self._wrote_any:
                        self._file.write(",\n")
                    self._file.write(serialized)
                    self._wrote_any = True
                    written += 1
                except (TypeError, ValueError) as row_exc:
                    log_message("error", f"IncrementalJSONWriter: сбой сериализации записи: {row_exc}")

            if self._flush_on_write:
                self._file.flush()
                os.fsync(self._file.fileno())

            self._total_written += written
            log_message("debug", f"IncrementalJSONWriter: записано записей={written} (всего={self._total_written})")
        except Exception as exc:
            log_message("error", f"IncrementalJSONWriter: непредвиденная ошибка записи: {exc}")

        return written

    def close(self) -> None:
        """
        Дописывает закрывающую "]" и закрывает файл.
        Безопасно вызывать несколько раз.
        """
        if self._file is not None and not self._closed:
            try:
                self._file.write("\n]\n")
                self._file.close()
                log_message(
                    "info",
                    f"IncrementalJSONWriter: закрыт ({self.filepath.name}, всего записей={self._total_written})",
                )
            except Exception as exc:
                log_message("error", f"IncrementalJSONWriter: ошибка при закрытии файла: {exc}")
            finally:
                self._closed = True

    @property
    def total_written(self) -> int:
        """Общее количество успешно записанных записей за время жизни писателя."""
        return self._total_written

    def __enter__(self) -> "IncrementalJSONWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


# =========================================================================
# BATCH WRITER
# =========================================================================


class RecordSink(Protocol):
    """
    Минимальный протокол, который должен реализовывать любой писатель,
    оборачиваемый `BatchWriter`. `IncrementalCSVWriter` и
    `IncrementalJSONWriter` уже удовлетворяют этому протоколу без
    каких-либо изменений — `BatchWriter` не заменяет их, а лишь
    буферизует вызовы `write_records()`.
    """

    def write_records(self, records: List[Dict[str, Any]]) -> int: ...


class BatchWriter:
    """
    Буферизующий слой поверх одного или нескольких писателей Incremental
    Saving (`IncrementalCSVWriter`, `IncrementalJSONWriter` или любого
    другого объекта с методом `write_records()`).

    Проблема, которую решает `BatchWriter`: при "чистом" Incremental
    Saving каждый вызов `write_records()` — это отдельная операция
    записи на диск (в CSV — построчная дозапись + опциональный
    flush/fsync, в JSON — дозапись сериализованных записей +
    опциональный flush/fsync). На большом количестве мелких порций
    (например, по одной странице пагинации) это создает избыточное
    количество операций I/O.

    `BatchWriter` не открывает и не закрывает файлы сам — этим
    продолжают заниматься сами `Incremental*Writer` (их жизненный цикл
    остается на стороне вызывающего кода, как и раньше). `BatchWriter`
    только решает, **когда** передать накопленные записи нижестоящим
    писателям:

        Record → Memory Buffer → (буфер заполнен?) → передать батч
        нижестоящим писателям → очистить буфер → продолжить скрапинг

    Поддерживает:
      - автоматический сброс при достижении `batch_size`
        (`BATCH_WRITER_AUTO_FLUSH_ENABLED` / `BATCH_WRITER_BATCH_SIZE`);
      - явный ручной сброс (`flush()`);
      - сброс остатка буфера при завершении работы (`close()` /
        выход из контекстного менеджера, управляется
        `BATCH_WRITER_FLUSH_ON_SHUTDOWN`).

    Обработка ошибок: если вызов `write_records()` нижестоящего писателя
    завершается исключением, ошибка логируется, буфер **не очищается**
    (чтобы не потерять ещё не сохранённые на диск записи и оставить
    возможность повторной попытки), и `flush()` возвращает 0 для этого
    сброса. Уже успешно записанные ранее батчи не затрагиваются —
    `BatchWriter` работает только с текущим содержимым буфера.

    Пример использования (замена прямых вызовов write_records()):

        csv_writer = IncrementalCSVWriter("output_results.csv")
        json_writer = IncrementalJSONWriter("output_results.json")

        with BatchWriter([csv_writer, json_writer]) as batch_writer:
            for page_records in scrape_pages():
                batch_writer.add_records(page_records)
        # remaining buffered records are flushed automatically on exit

        csv_writer.close()
        json_writer.close()
    """

    def __init__(
        self,
        sinks: List[RecordSink],
        batch_size: Optional[int] = None,
        auto_flush_enabled: Optional[bool] = None,
        flush_on_shutdown: Optional[bool] = None,
    ):
        """
        Args:
            sinks: Список нижестоящих писателей (любой объект с методом
                `write_records(records) -> int`, например
                `IncrementalCSVWriter`/`IncrementalJSONWriter`). Их
                открытие/закрытие остается на стороне вызывающего кода.
            batch_size: Максимальный размер буфера до автоматического
                сброса. По умолчанию — `config.BATCH_WRITER_BATCH_SIZE`.
            auto_flush_enabled: Включает автоматический сброс при
                достижении `batch_size`. По умолчанию —
                `config.BATCH_WRITER_AUTO_FLUSH_ENABLED`.
            flush_on_shutdown: Сбрасывать остаток буфера в `close()`.
                По умолчанию — `config.BATCH_WRITER_FLUSH_ON_SHUTDOWN`.
        """
        self._sinks: List[RecordSink] = list(sinks)
        self._batch_size = batch_size if batch_size is not None else BATCH_WRITER_BATCH_SIZE
        self._auto_flush_enabled = (
            auto_flush_enabled if auto_flush_enabled is not None else BATCH_WRITER_AUTO_FLUSH_ENABLED
        )
        self._flush_on_shutdown = (
            flush_on_shutdown if flush_on_shutdown is not None else BATCH_WRITER_FLUSH_ON_SHUTDOWN
        )

        self._buffer: List[Dict[str, Any]] = []
        self._total_buffered = 0  # всего когда-либо добавлено в буфер (включая уже сброшенное)
        self._total_flushed = 0   # всего успешно передано нижестоящим писателям
        self._flush_count = 0     # количество выполненных сбросов (авто + ручных)
        self._closed = False

        log_message(
            "info",
            f"BatchWriter: инициализирован (sinks={len(self._sinks)}, "
            f"batch_size={self._batch_size}, auto_flush={self._auto_flush_enabled})",
        )

    def add_records(self, records: List[Dict[str, Any]]) -> None:
        """
        Добавляет записи в буфер. Не выполняет запись сама — только
        накапливает записи в памяти.

        Если авто-сброс включен (`auto_flush_enabled`) и после
        добавления размер буфера достиг `batch_size`, автоматически
        вызывает `flush()`. Буфер никогда не растет бесконечно при
        включенном авто-сбросе.

        Args:
            records: Список словарей для добавления в буфер (например,
                результаты парсинга одной страницы).
        """
        if not records:
            return

        if self._closed:
            log_message("error", "BatchWriter: попытка добавить записи в закрытый writer")
            return

        self._buffer.extend(records)
        self._total_buffered += len(records)

        if self._auto_flush_enabled and len(self._buffer) >= self._batch_size:
            self.flush(reason="auto")

    def flush(self, reason: str = "manual") -> int:
        """
        Немедленно передает все записи из буфера нижестоящим писателям
        (`sinks`) и очищает буфер при успехе.

        Если один из писателей выбрасывает исключение при записи, ошибка
        логируется, а буфер **сохраняется** (не очищается), чтобы данные
        не потерялись и сброс можно было повторить позже. Уже успешно
        записанные писатели за этот вызов не откатываются (частичная
        запись в другие sinks не считается поводом для полной отмены —
        KISS: избегаем сложной транзакционной логики между независимыми
        форматами экспорта).

        Args:
            reason: Только для логирования — "auto" (авто-сброс по
                размеру батча), "manual" (явный вызов) или "shutdown"
                (сброс при закрытии).

        Returns:
            int: Количество записей, успешно переданных писателям за
                этот вызов (0, если буфер был пуст или сброс не удался).
        """
        if not self._buffer:
            return 0

        batch = self._buffer
        batch_len = len(batch)

        had_failure = False
        for sink in self._sinks:
            try:
                sink.write_records(batch)
            except Exception as exc:
                had_failure = True
                log_message("error", f"BatchWriter: сбой записи батча ({reason}) в {sink!r}: {exc}")

        if had_failure:
            # Буфер сохраняем целиком, чтобы вызывающий код мог повторить
            # попытку (например, следующим вызовом flush()) без потери данных.
            log_message(
                "error",
                f"BatchWriter: сброс ({reason}) завершился с ошибками, буфер сохранён "
                f"(записей в буфере: {batch_len})",
            )
            return 0

        self._buffer = []
        self._total_flushed += batch_len
        self._flush_count += 1
        log_message(
            "info",
            f"BatchWriter: батч сброшен ({reason}), записей={batch_len} "
            f"(всего сброшено={self._total_flushed}, сбросов={self._flush_count})",
        )
        return batch_len

    def close(self) -> None:
        """
        Завершает работу `BatchWriter`. Если `flush_on_shutdown` включен
        и в буфере остались записи — сбрасывает их перед закрытием, чтобы
        ни одна накопленная запись не была потеряна при штатном
        завершении. Безопасно вызывать несколько раз.

        Не закрывает сами нижестоящие писатели (`sinks`) — их закрытие
        остается на стороне вызывающего кода.
        """
        if self._closed:
            return

        if self._buffer:
            if self._flush_on_shutdown:
                self.flush(reason="shutdown")
            else:
                log_message(
                    "error",
                    f"BatchWriter: закрытие с непустым буфером и выключенным "
                    f"flush_on_shutdown — {len(self._buffer)} записей будут потеряны",
                )

        log_message(
            "info",
            f"BatchWriter: закрыт (всего добавлено={self._total_buffered}, "
            f"всего сброшено={self._total_flushed}, сбросов={self._flush_count})",
        )
        self._closed = True

    @property
    def buffered_count(self) -> int:
        """Текущее количество записей в буфере, ещё не сброшенных на диск."""
        return len(self._buffer)

    @property
    def total_flushed(self) -> int:
        """Общее количество записей, успешно переданных писателям за время жизни объекта."""
        return self._total_flushed

    def __enter__(self) -> "BatchWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    test_data = [
        {"id": 1, "title": "Ноутбук", "price": 1200.50, "in_stock": True},
        {"id": 2, "title": "Смартфон", "price": 550.00, "in_stock": False},
    ]
    print(f"[{__file__}] Запуск теста экспортера (batch)...")
    save_to_csv(test_data, "test_products")
    save_to_json(test_data, "test_products.json")

    print(f"[{__file__}] Запуск теста Incremental Saving...")
    with IncrementalCSVWriter("test_incremental") as csv_writer:
        csv_writer.write_records(test_data[:1])
        csv_writer.write_records(test_data[1:])
    print(f"  CSV: записано всего {csv_writer.total_written} строк")

    with IncrementalJSONWriter("test_incremental") as json_writer:
        json_writer.write_records(test_data[:1])
        json_writer.write_records(test_data[1:])
    print(f"  JSON: записано всего {json_writer.total_written} записей")

    print(f"[{__file__}] Запуск теста Batch Writer...")
    csv_writer2 = IncrementalCSVWriter("test_batch_writer")
    json_writer2 = IncrementalJSONWriter("test_batch_writer")
    with BatchWriter([csv_writer2, json_writer2], batch_size=2) as batch_writer:
        batch_writer.add_records(test_data[:1])  # не достигнут batch_size=2, буфер=1
        print(f"  После 1-й записи: buffered={batch_writer.buffered_count}, flushed={batch_writer.total_flushed}")
        batch_writer.add_records(test_data[1:])  # достигнут batch_size=2, авто-сброс
        print(f"  После 2-й записи: buffered={batch_writer.buffered_count}, flushed={batch_writer.total_flushed}")
    csv_writer2.close()
    json_writer2.close()
    print(f"  Итого сброшено через BatchWriter: {batch_writer.total_flushed} записей")


--- app/file_proxy_provider.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Proxy Provider.

Эталонная реализация `ProxyProvider` (см. `app/proxy_manager.py`),
загружающая список прокси из локального текстового файла.

Назначение этого модуля — подтвердить, что архитектура Proxy Manager
действительно провайдер-независима: Proxy Manager работает с
`FileProxyProvider` точно так же, как и с `EnvProxyProvider`, не зная
ничего о том, что прокси читаются из файла.

File Proxy Provider:

* берет путь к файлу и схему по умолчанию из Configuration Manager
  (`config.PROXY_FILE`, `config.PROXY_FILE_DEFAULT_SCHEME`);
* поддерживает несколько распространенных форматов записи прокси
  (см. `_parse_line()`);
* пропускает пустые строки, комментарии (`#`) и некорректные записи без
  падения всего приложения — только с предупреждением в лог;
* возвращает нормализованный список прокси в виде готовых URL
  (`http://[user:pass@]host:port`), из которого `get_proxy()` отдает
  первый доступный (без ротации/выбора — это ответственность будущих
  задач Proxy Rotation / Proxy Selection, см. `framework/ROADMAP.md`).

File Proxy Provider НЕ выбирает, НЕ ротирует, НЕ валидирует и НЕ проверяет
здоровье прокси, НЕ выполняет HTTP-запросы и ничего не знает о других
провайдерах (Webshare, BrightData и т.д.) — вся эта логика вне его
ответственности.
"""

from pathlib import Path
from typing import List, Optional

from app import config
from app.proxy_manager import ProxyProvider

# Схемы, которые считаются уже полными URL и не требуют достройки
# (запись используется как есть, без подстановки PROXY_FILE_DEFAULT_SCHEME).
_KNOWN_SCHEMES = ("http://", "https://", "socks5://", "socks4://")


def _parse_line(line: str, default_scheme: str) -> Optional[str]:
    """
    Разбирает одну строку файла прокси и возвращает нормализованный URL.

    Поддерживаемые форматы:
        ip:port
        ip:port:username:password
        http://ip:port
        http://username:password@ip:port
        socks5://username:password@ip:port
        (и другие схемы из `_KNOWN_SCHEMES`, переданные как есть)

    Args:
        line (str): Сырая строка из файла (без завершающего перевода строки).
        default_scheme (str): Схема, подставляемая для записей без схемы
            (`ip:port` / `ip:port:username:password`).

    Returns:
        Optional[str]: Нормализованный URL прокси, либо `None`, если строка
            пуста, является комментарием или не удалось разобрать формат.
    """
    entry = line.strip()
    if not entry or entry.startswith("#"):
        return None

    # Уже полный URL — используем как есть.
    if entry.startswith(_KNOWN_SCHEMES):
        return entry

    # ip:port или ip:port:username:password
    parts = entry.split(":")
    if len(parts) == 2:
        host, port = parts
        if not (host and port.isdigit()):
            return None
        return f"{default_scheme}://{host}:{port}"

    if len(parts) == 4:
        host, port, username, password = parts
        if not (host and port.isdigit() and username and password):
            return None
        return f"{default_scheme}://{username}:{password}@{host}:{port}"

    return None


class FileProxyProvider(ProxyProvider):
    """
    Провайдер, читающий список прокси из локального файла.

    Хранит загруженные прокси в памяти (список) и последовательно
    возвращает первый из них через `get_proxy()`. Выбор/ротация конкретного
    прокси из списка — задача будущего компонента Proxy Rotation, а не
    этого провайдера.
    """

    def __init__(self, path: Path = None, default_scheme: str = None):
        """
        Args:
            path (Path, optional): Путь к файлу со списком прокси.
                По умолчанию — `config.PROXY_FILE`.
            default_scheme (str, optional): Схема для записей без явной
                схемы (`ip:port`). По умолчанию — `config.PROXY_FILE_DEFAULT_SCHEME`.
        """
        self.path = path or config.PROXY_FILE
        self.default_scheme = default_scheme or config.PROXY_FILE_DEFAULT_SCHEME
        self._proxies: List[str] = self._load()

    def _load(self) -> List[str]:
        """
        Загружает и парсит файл прокси.

        Returns:
            List[str]: Список успешно распознанных прокси (пустой, если
                файл отсутствует, пуст или не содержит валидных записей).
        """
        if not self.path.exists():
            print(f"[{__file__}] Файл прокси не найден: {self.path}")
            return []

        if self.path.stat().st_size == 0:
            print(f"[{__file__}] Файл прокси пуст: {self.path}")
            return []

        try:
            raw_lines = self.path.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            print(f"[{__file__}] Ошибка при чтении файла прокси {self.path.name}: {e}")
            return []

        proxies: List[str] = []
        for line_number, raw_line in enumerate(raw_lines, start=1):
            parsed = _parse_line(raw_line, self.default_scheme)
            if parsed:
                proxies.append(parsed)
            elif raw_line.strip() and not raw_line.strip().startswith("#"):
                print(f"[{__file__}] Предупреждение: пропущена невалидная строка "
                      f"{line_number} в {self.path.name}: '{raw_line.strip()}'")

        print(f"[{__file__}] Загружено прокси из {self.path.name}: {len(proxies)}")
        return proxies

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый прокси из загруженного списка, либо `None`,
        если список пуст.
        """
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный список успешно загруженных прокси. Полезно для
        будущего Proxy Rotation, чтобы не парсить файл повторно.

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        return list(self._proxies)

    def reload(self) -> List[str]:
        """
        Повторно читает файл прокси с диска и обновляет внутренний список.

        Returns:
            List[str]: Обновленный список загруженных прокси.
        """
        self._proxies = self._load()
        return self.get_all_proxies()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    provider = FileProxyProvider()
    print(f"[{__file__}] Путь к файлу прокси: {provider.path}")
    print(f"[{__file__}] Все загруженные прокси: {provider.get_all_proxies()}")
    print(f"[{__file__}] Активный прокси (get_proxy): {provider.get_proxy()}")

    # Демонстрация интеграции с Proxy Manager без изменения его кода/API.
    from app.proxy_manager import ProxyManager

    ProxyManager.set_provider(provider)
    print(f"[{__file__}] ProxyManager.get_proxy() после смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] ProxyManager.to_requests_dict(): {ProxyManager.to_requests_dict()}")


--- app/health_check.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Health Check.

Централизованный компонент, отвечающий ТОЛЬКО за мониторинг доступности и
качества прокси. Он собирает и поддерживает метрики для каждого прокси
(успехи/сбои/время ответа/статус), но НЕ выбирает, какой прокси использовать
(это Proxy Selection), и НЕ решает, когда менять (это Proxy Rotation).

Proxy Health Check:

* НЕ скачивает прокси;
* НЕ выбирает прокси;
* НЕ ротирует прокси;
* НЕ содержит provider-specific логики;
* НЕ выполняет логику скрапинга (единственный HTTP-запрос — легковесная
  активная проверка `check_proxy()` на настраиваемый тестовый URL).

Интегрируется с:
* Configuration Manager (`app/config.py`) — все пороги конфигурируются
  через `.env`, смена порогов не требует правок кода;
* Proxy Manager (`app/proxy_manager.py`) — пассивный мониторинг через
  `record_success()`/`record_failure()`, фильтрация пула через
  `filter_healthy()`, активная проверка доступна через `check_proxy()`;
* Proxy Selection — косвенно, только в том смысле, что Health Check
  фильтрует пул ДО передачи в `ProxySelector.select()`, но сам не
  выбирает конкретный прокси;
* Proxy Rotation — косвенно, через общий `ProxyManager.report_proxy_failure()`
  hook.

Метрики и состояния хранятся в памяти (in-memory), без персистентности —
аналогично Proxy Selection и Proxy Rotation, это осознанное упрощение
для текущей версии фреймворка.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests

from app import config


class HealthStatus(str, Enum):
    """Статус здоровья прокси."""

    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"


@dataclass
class ProxyStats:
    """Метрики одного прокси."""

    proxy: str

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0

    _total_response_time_ms: float = 0.0  # накопительная сумма для вычисления среднего

    last_success_at: Optional[float] = None
    last_failure_at: Optional[float] = None
    status: HealthStatus = HealthStatus.HEALTHY
    disabled_until: Optional[float] = None

    @property
    def success_rate(self) -> float:
        """Доля успешных запросов от общего числа (0.0–1.0)."""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def avg_response_time_ms(self) -> float:
        """Среднее время ответа в миллисекундах."""
        if self.successful_requests == 0:
            return 0.0
        return self._total_response_time_ms / self.successful_requests

    def record_success(self, response_time_ms: Optional[float] = None) -> None:
        """Записывает успешный запрос с этим прокси."""
        self.total_requests += 1
        self.successful_requests += 1
        self.consecutive_failures = 0
        self.last_success_at = time.monotonic()
        if response_time_ms is not None:
            self._total_response_time_ms += response_time_ms

    def record_failure(self) -> None:
        """Записывает сбой при использовании этого прокси."""
        self.total_requests += 1
        self.failed_requests += 1
        self.consecutive_failures += 1
        self.last_failure_at = time.monotonic()

    def as_dict(self) -> Dict[str, object]:
        """Возвращает словарь метрик для отладки/логирования (все поля кроме `proxy`)."""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.success_rate, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 1),
            "consecutive_failures": self.consecutive_failures,
            "last_success_at": self.last_success_at,
            "last_failure_at": self.last_failure_at,
            "status": self.status.value,
            "disabled_until": self.disabled_until,
        }


class HealthCheck:
    """
    Централизованная точка доступа к мониторингу здоровья прокси.

    Proxy Manager вызывает `record_success()`/`record_failure()` при
    каждом исходе реального запроса (пассивный мониторинг), а также
    `filter_healthy()` перед тем, как передать пул в Proxy Selection.
    Активная проверка доступна через `check_proxy()`.

    Все пороговые значения берутся из Configuration Manager и могут быть
    изменены через `.env` без правок кода.
    """

    _stats: Dict[str, ProxyStats] = {}

    @classmethod
    def _get_or_create(cls, proxy_url: str) -> ProxyStats:
        """Возвращает (или создаёт) статистику для URL прокси."""
        stats = cls._stats.get(proxy_url)
        if stats is None:
            stats = ProxyStats(proxy=proxy_url)
            cls._stats[proxy_url] = stats
        return stats

    @classmethod
    def _recalc_status(cls, stats: ProxyStats) -> None:
        """
        Пересчитывает `stats.status` по текущим порогам из Configuration
        Manager. Вызывается после каждого `record_success()`/`record_failure()`.

        Логика (от самого строгого состояния к самому мягкому):
        * DISABLED: если `disabled_until` ещё не истёк — остаётся DISABLED.
          Если истёк — сбрасываем `disabled_until` и `consecutive_failures`,
          давая прокси шанс на восстановление (Recovery, см. TASK.md).
        * DISABLED (переход): если
          `consecutive_failures >= HEALTH_MAX_CONSECUTIVE_FAILURES`, то
          прокси автоматически DISABLED на `HEALTH_DISABLE_DURATION_SECONDS`.
        * UNHEALTHY: промежуточная (более серьёзная, чем WARNING, но ещё не
          DISABLED) деградация — если
          `consecutive_failures >= HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES`.
          Не блокирует использование прокси (в отличие от DISABLED) — это
          лишь сигнал для Proxy Selection на будущее.
        * WARNING: если `success_rate < HEALTH_MIN_SUCCESS_RATE` ТОЛЬКО
          при наличии хотя бы `config.HEALTH_MIN_REQUESTS_FOR_RATE` запросов
          (чтобы маленькая выборка не давала ложно-негативный статус), либо
          если среднее время ответа превышает `HEALTH_MAX_RESPONSE_TIME_MS`.
        * Иначе — HEALTHY.

        Restoring/Recovery: любой успешный запрос сбрасывает
        `consecutive_failures` в 0 (см. `ProxyStats.record_success()`), поэтому
        UNHEALTHY/WARNING статусы автоматически снимаются при следующем же
        успешном passive-запросе или активной проверке (`check_proxy()`) —
        отдельного фонового планировщика для них не требуется. Для DISABLED
        восстановление происходит по истечении `disabled_until` (см. выше).
        """
        now = time.monotonic()

        # Проверка окна DISABLED
        if stats.disabled_until is not None:
            if now < stats.disabled_until:
                stats.status = HealthStatus.DISABLED
                return
            # Окно истекло — сбрасываем счётчик и даём шанс на восстановление
            stats.disabled_until = None
            stats.consecutive_failures = 0

        # Порог последовательных сбоев → DISABLED
        if stats.consecutive_failures >= config.HEALTH_MAX_CONSECUTIVE_FAILURES:
            stats.status = HealthStatus.DISABLED
            stats.disabled_until = now + config.HEALTH_DISABLE_DURATION_SECONDS
            return

        # Промежуточный порог последовательных сбоев → UNHEALTHY
        if stats.consecutive_failures >= config.HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES:
            stats.status = HealthStatus.UNHEALTHY
            return

        # Порог success rate → WARNING (только при достаточной выборке)
        if (
            stats.total_requests >= config.HEALTH_MIN_REQUESTS_FOR_RATE
            and stats.success_rate < config.HEALTH_MIN_SUCCESS_RATE
        ):
            stats.status = HealthStatus.WARNING
            return

        # Порог времени ответа → WARNING
        if (
            stats.successful_requests > 0
            and stats.avg_response_time_ms > config.HEALTH_MAX_RESPONSE_TIME_MS
        ):
            stats.status = HealthStatus.WARNING
            return

        stats.status = HealthStatus.HEALTHY


    @classmethod
    def record_success(
        cls, proxy_url: str, response_time_ms: Optional[float] = None
    ) -> None:
        """
        Записывает успешный запрос через указанный прокси (пассивный мониторинг).

        Вызывается Proxy Manager через `report_proxy_success()`.

        Args:
            proxy_url (str): URL прокси, через который был выполнен запрос.
            response_time_ms (float, optional): Время ответа в миллисекундах
                (если доступно — для вычисления среднего).
        """
        stats = cls._get_or_create(proxy_url)
        stats.record_success(response_time_ms)
        cls._recalc_status(stats)

    @classmethod
    def record_failure(cls, proxy_url: str) -> None:
        """
        Записывает сбой при использовании указанного прокси (пассивный мониторинг).

        Вызывается Proxy Manager через `report_proxy_failure()`.

        Args:
            proxy_url (str): URL прокси, через который произошёл сбой.
        """
        stats = cls._get_or_create(proxy_url)
        stats.record_failure()
        cls._recalc_status(stats)

    @classmethod
    def get_status(cls, proxy_url: str) -> HealthStatus:
        """
        Возвращает текущий статус здоровья прокси.

        Если статистики для прокси ещё нет, он считается HEALTHY (ни один
        запрос не был сделан — нет данных, чтобы считать иначе).
        """
        stats = cls._stats.get(proxy_url)
        if stats is None:
            return HealthStatus.HEALTHY
        # Проверяем, не истекло ли окно DISABLED — если истекло, пересчитываем
        if (
            stats.status == HealthStatus.DISABLED
            and stats.disabled_until is not None
            and time.monotonic() >= stats.disabled_until
        ):
            cls._recalc_status(stats)
        return stats.status

    @classmethod
    def is_usable(cls, proxy_url: str) -> bool:
        """
        Считается ли прокси пригодным для использования сейчас.

        Непригодны: DISABLED прокси. UNHEALTHY/WARNING прокси по-прежнему
        считаются пригодными — их низкое качество может быть временным, и
        полное исключение привело бы к слишком агрессивной фильтрации.
        """
        return cls.get_status(proxy_url) != HealthStatus.DISABLED

    @classmethod
    def filter_healthy(cls, proxies: List[str]) -> List[str]:
        """
        Возвращает отфильтрованный список прокси, исключая DISABLED.

        Если ВСЕ прокси отфильтрованы (пустой результат), возвращает
        исходный список с предупреждением в лог — это гарантирует, что
        фреймворк не остановится полностью из-за временного всплеска сбоев.

        Args:
            proxies (List[str]): Исходный пул прокси.

        Returns:
            List[str]: Отфильтрованный пул (или исходный, если все нездоровы).
        """
        healthy = [p for p in proxies if cls.is_usable(p)]
        if not healthy and proxies:
            print(
                f"[{__file__}] Предупреждение: все прокси ({len(proxies)}) "
                f"непригодны (DISABLED). Используется нефильтрованный пул "
                f"для сохранения работоспособности."
            )
            return proxies
        return healthy

    @classmethod
    def get_stats(cls, proxy_url: str) -> Optional[ProxyStats]:
        """Возвращает статистику для указанного прокси, либо None."""
        return cls._stats.get(proxy_url)

    @classmethod
    def get_all_stats(cls) -> Dict[str, ProxyStats]:
        """Возвращает всю собранную статистику (для отладки/логирования)."""
        return cls._stats

    @classmethod
    def check_proxy(cls, proxy_url: str) -> bool:
        """
        Активная проверка: выполняет легковесный HTTP GET-запрос через
        указанный прокси на настраиваемый тестовый URL
        (`config.HEALTH_CHECK_URL`).

        Это ЕДИНСТВЕННЫЙ метод в Health Check, который выполняет реальный
        HTTP-запрос. Он не вызывается автоматически внутри `get_proxy()` —
        доступен как API для будущего фонового вызова (например, из
        Health Check scheduler или перед добавлением прокси в ротацию).

        Результат проверки автоматически обновляет пассивную статистику
        (`record_success`/`record_failure`).

        Args:
            proxy_url (str): URL прокси для проверки.

        Returns:
            bool: `True`, если прокси успешно ответил на тестовый запрос.
        """
        try:
            start = time.monotonic()
            response = requests.get(
                config.HEALTH_CHECK_URL,
                proxies={"http": proxy_url, "https": proxy_url},
                timeout=config.HEALTH_CHECK_TIMEOUT,
            )
            elapsed = (time.monotonic() - start) * 1000.0  # в миллисекундах
            cls.record_success(proxy_url, response_time_ms=elapsed)
            return True
        except Exception:
            cls.record_failure(proxy_url)
            return False

    @classmethod
    def reset(cls, proxy_url: Optional[str] = None) -> None:
        """
        Сбрасывает статистику: для одного прокси (если указан) или полностью.

        Args:
            proxy_url (str, optional): URL прокси для сброса. Если `None`,
                сбрасывается вся статистика.
        """
        if proxy_url is not None:
            cls._stats.pop(proxy_url, None)
        else:
            cls._stats.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    proxy = "http://demo_user:demo_pass@10.0.0.1:8000"

    print(f"[{__file__}] Начальный статус (без данных): {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] is_usable(): {HealthCheck.is_usable(proxy)}")

    print(f"[{__file__}] Симулируем 5 успешных запросов...")
    for i in range(5):
        HealthCheck.record_success(proxy, response_time_ms=150.0 + i * 10)
    print(f"[{__file__}] Статус после успехов: {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] Статистика: {HealthCheck.get_stats(proxy).as_dict()}")

    print(f"[{__file__}] Симулируем {config.HEALTH_MAX_CONSECUTIVE_FAILURES} "
          f"последовательных сбоев...")
    for _ in range(config.HEALTH_MAX_CONSECUTIVE_FAILURES):
        HealthCheck.record_failure(proxy)
    print(f"[{__file__}] Статус после сбоев: {HealthCheck.get_status(proxy).value}")
    print(f"[{__file__}] is_usable(): {HealthCheck.is_usable(proxy)}")

    print(f"[{__file__}] filter_healthy() на пуле из 3 прокси (1 DISABLED):")
    pool = ["http://1.1.1.1:1111", proxy, "http://3.3.3.3:3333"]
    filtered = HealthCheck.filter_healthy(pool)
    print(f"[{__file__}]   Исходный: {pool}")
    print(f"[{__file__}]   Отфильтрованный: {filtered}")

    print(f"[{__file__}] filter_healthy() на пуле, где ВСЕ DISABLED:")
    all_disabled = [proxy]
    filtered = HealthCheck.filter_healthy(all_disabled)
    print(f"[{__file__}]   Исходный: {all_disabled}")
    print(f"[{__file__}]   Отфильтрованный (fallback): {filtered}")

    print(f"[{__file__}] Активная проверка реального недоступного прокси:")
    result = HealthCheck.check_proxy("http://192.0.2.1:9999")
    print(f"[{__file__}]   Результат: {result}")

    # Сброс статистики после тестов
    HealthCheck.reset()

--- app/html_parser.py ---
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


--- app/infinite_scroll.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Infinite Scroll.

Централизованный компонент бесконечного скроллинга для JS-сайтов,
подгружающих контент динамически при прокрутке страницы (см.
`framework/ROADMAP.md`, Milestone 4).

Infinite Scroll — единственная точка, через которую скрапер-модули
должны запускать цикл прокрутки страницы. Он НЕ содержит логики
парсинга/экспорта/логина/пагинации и НЕ знает о селекторах конкретных
сайтов — единственное, что он умеет, это скроллить страницу и
останавливаться по одному из настраиваемых условий:

    Infinite Scroll
            │
            ▼
    PlaywrightEngine.evaluate() / .wait_for_load()  ─────────────┐
            │                                                     │
     ┌──────┼─────────┐                                           │
     ▼      ▼          ▼                                          ▼
    Delay  Logging  Configuration                          (PlaywrightEngine
    Manager          Manager                                 остаётся единственной
                                                               точкой навигации/JS)

Infinite Scroll:

* выполняет прокрутку страницы через `PlaywrightEngine.evaluate()` —
  не дублирует логику запуска браузера/навигации (это ответственность
  Playwright Engine, `app/playwright_engine.py`);
* делает паузу между скроллами через `DelayManager.wait_fixed()`/
  `wait_random()` (Delay Manager, `app/delay_manager.py`) — не реализует
  собственный `time.sleep()`;
* поддерживает несколько независимых условий остановки одновременно
  (срабатывает то, которое выполнилось первым): отсутствие нового
  контента, лимит итераций, лимит высоты страницы, целевое количество
  элементов, таймаут, пользовательский callback;
* использует централизованную функцию логирования `app.utils.log_message`
  для старта/завершения цикла, числа итераций и причины остановки
  (без избыточного лога на каждой итерации);
* оборачивает все ожидаемые сбои Playwright (полученные как
  `PlaywrightEngineError` от Playwright Engine) — одна неудачная
  прокрутка не прерывает весь процесс скрапинга, цикл просто
  останавливается с причиной `error`, а вызывающий код продолжает
  работу с уже загруженным контентом;
* берет все параметры поведения (лимиты, задержки, флаги) из
  Configuration Manager (`app/config.py`) с возможностью точечного
  переопределения аргументами метода — без хардкода значений.

Infinite Scroll НЕ парсит HTML, НЕ извлекает данные, НЕ выполняет логин,
НЕ экспортирует данные и НЕ содержит селекторов конкретных сайтов —
опциональный `item_selector`/`count_callback` передается вызывающим
кодом извне и используется исключительно для подсчета количества
элементов (для условия остановки "target_item_count"), а не для
извлечения самих данных.
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

from app import config
from app.delay_manager import DelayManager
from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError
from app.utils import log_message


class InfiniteScrollError(Exception):
    """
    Единое исключение Infinite Scroll для непредвиденных сбоев конфигурации
    (например, некорректных аргументов), не связанных с ожидаемыми
    условиями остановки цикла скроллинга.

    Сбои самого Playwright во время скроллинга НЕ поднимаются как это
    исключение — они обрабатываются graceful (см. `ScrollStopReason.ERROR`),
    чтобы одна неудачная прокрутка не прерывала весь процесс скрапинга.
    """


class ScrollStopReason(str, Enum):
    """Причина остановки цикла бесконечного скроллинга."""

    DISABLED = "disabled"
    NO_NEW_CONTENT = "no_new_content"
    MAX_SCROLLS = "max_scrolls"
    MAX_HEIGHT = "max_height"
    TARGET_COUNT = "target_count"
    TIMEOUT = "timeout"
    CUSTOM_CALLBACK = "custom_callback"
    ERROR = "error"


@dataclass
class ScrollState:
    """
    Снимок состояния текущей итерации скроллинга.

    Передается в пользовательский `stop_callback`, чтобы вызывающий код
    мог реализовать произвольную логику остановки без необходимости
    иметь доступ к внутренностям `InfiniteScroll`.
    """

    engine: PlaywrightEngine
    iteration: int
    elapsed_seconds: float
    page_height: int
    item_count: Optional[int] = None


@dataclass
class ScrollResult:
    """Итоговый результат выполнения `InfiniteScroll.scroll()`."""

    scrolls_performed: int
    stop_reason: str
    elapsed_seconds: float
    final_height: int
    final_item_count: Optional[int] = None


class InfiniteScroll:
    """
    Централизованный исполнитель цикла бесконечного скроллинга.

    Работает с любым объектом, предоставляющим интерфейс Playwright Engine
    (`evaluate()`, `wait_for_load()`) — на практике это экземпляр
    `PlaywrightEngine` (`app/playwright_engine.py`). Сам компонент не
    запускает браузер и не выполняет навигацию — предполагается, что
    вызывающий код уже открыл нужную страницу через
    `PlaywrightEngine.goto()`.

    Пример использования:

        with PlaywrightEngine() as engine:
            engine.goto("https://example.com/feed")
            result = InfiniteScroll.scroll(engine, max_scrolls=20)
            html = engine.content()
    """

    # =====================================================================
    # НИЗКОУРОВНЕВЫЕ ОПЕРАЦИИ (скролл / замер высоты / подсчет элементов)
    # =====================================================================

    @staticmethod
    def _get_page_height(engine: PlaywrightEngine) -> int:
        """Возвращает текущую высоту документа (`document.body.scrollHeight`)."""
        return int(engine.evaluate("document.body.scrollHeight"))

    @staticmethod
    def _perform_scroll(engine: PlaywrightEngine, step_px: int, smooth: bool) -> None:
        """
        Выполняет одну прокрутку страницы.

        Args:
            step_px (int): Шаг прокрутки в пикселях. Если <= 0, страница
                скроллится сразу к текущему низу (`scrollHeight`).
            smooth (bool): Использовать плавную прокрутку вместо мгновенной.
        """
        behavior = "smooth" if smooth else "auto"
        if step_px and step_px > 0:
            script = f"window.scrollBy({{top: {step_px}, left: 0, behavior: '{behavior}'}})"
        else:
            script = (
                f"window.scrollTo({{top: document.body.scrollHeight, left: 0, "
                f"behavior: '{behavior}'}})"
            )
        engine.evaluate(script)

    @staticmethod
    def _count_items(
        engine: PlaywrightEngine,
        item_selector: Optional[str],
        count_callback: Optional[Callable[[PlaywrightEngine], int]],
        previous_count: Optional[int],
    ) -> Optional[int]:
        """
        Подсчитывает текущее количество загруженных элементов, если
        передан `count_callback` или `item_selector`. Иначе возвращает `None`.

        Сбой подсчета (например, элемент временно отсутствует в DOM) не
        прерывает цикл скроллинга — возвращается предыдущее известное
        значение, а сбой попадает в лог.
        """
        if count_callback is None and not item_selector:
            return None
        try:
            if count_callback is not None:
                return int(count_callback(engine))
            return int(engine.evaluate(f"document.querySelectorAll('{item_selector}').length"))
        except Exception as exc:
            log_message("error", f"Infinite Scroll: не удалось подсчитать элементы: {exc}")
            return previous_count

    @staticmethod
    def _wait_between_scrolls(delay_mode: str, fixed_seconds: float, min_seconds: float, max_seconds: float) -> None:
        """Пауза между итерациями скроллинга, делегированная Delay Manager."""
        if delay_mode == "fixed":
            DelayManager.wait_fixed(fixed_seconds)
        else:
            DelayManager.wait_random(min_seconds, max_seconds)

    # =====================================================================
    # ОСНОВНАЯ ТОЧКА ВХОДА
    # =====================================================================

    @classmethod
    def scroll(
        cls,
        engine: PlaywrightEngine,
        *,
        enabled: Optional[bool] = None,
        max_scrolls: Optional[int] = None,
        timeout_seconds: Optional[float] = None,
        max_page_height: Optional[int] = None,
        max_no_new_content_attempts: Optional[int] = None,
        target_item_count: Optional[int] = None,
        item_selector: Optional[str] = None,
        count_callback: Optional[Callable[[PlaywrightEngine], int]] = None,
        stop_callback: Optional[Callable[[ScrollState], bool]] = None,
        scroll_step_px: Optional[int] = None,
        smooth: Optional[bool] = None,
        wait_for_network_idle: Optional[bool] = None,
    ) -> ScrollResult:
        """
        Выполняет цикл прокрутки текущей страницы `engine` до срабатывания
        одного из настроенных условий остановки.

        Все условия остановки проверяются одновременно — цикл завершается
        по первому сработавшему условию. Любой аргумент, не переданный
        явно, берется из Configuration Manager (`app/config.py`).

        Args:
            engine (PlaywrightEngine): Активный движок с уже открытой
                страницей (после `engine.goto(...)`).
            enabled (bool, optional): Включает/выключает скроллинг.
                По умолчанию — `config.INFINITE_SCROLL_ENABLED`. Если
                `False`, метод сразу возвращает результат с
                `stop_reason="disabled"` без единой прокрутки.
            max_scrolls (int, optional): Максимум итераций скроллинга.
                `0` — без ограничения. По умолчанию —
                `config.INFINITE_SCROLL_MAX_SCROLLS`.
            timeout_seconds (float, optional): Общий таймаут цикла (секунды).
                `0` — без ограничения. По умолчанию —
                `config.INFINITE_SCROLL_TIMEOUT_SECONDS`.
            max_page_height (int, optional): Высота страницы (px), при
                достижении которой скроллинг останавливается. `0` — без
                ограничения. По умолчанию — `config.INFINITE_SCROLL_MAX_PAGE_HEIGHT`.
            max_no_new_content_attempts (int, optional): Число
                последовательных прокруток без увеличения высоты страницы,
                после которого считается, что новый контент больше не
                подгружается. По умолчанию —
                `config.INFINITE_SCROLL_MAX_NO_NEW_CONTENT`.
            target_item_count (int, optional): Целевое количество
                элементов — требует `item_selector` или `count_callback`.
            item_selector (str, optional): CSS-селектор для подсчета
                текущего количества загруженных элементов (передается
                вызывающим кодом — компонент не хранит селекторы сам).
            count_callback (Callable[[PlaywrightEngine], int], optional):
                Альтернатива `item_selector` — произвольная функция подсчета
                элементов. Имеет приоритет над `item_selector`, если оба переданы.
            stop_callback (Callable[[ScrollState], bool], optional):
                Пользовательская функция остановки — вызывается на каждой
                итерации, получает `ScrollState`, возвращает `True` для
                немедленной остановки.
            scroll_step_px (int, optional): Шаг прокрутки в пикселях.
                `0`/`None` — скроллить сразу к низу страницы на каждой
                итерации. По умолчанию — `config.INFINITE_SCROLL_STEP_PX`.
            smooth (bool, optional): Плавная прокрутка вместо мгновенной.
                По умолчанию — `config.INFINITE_SCROLL_SMOOTH`.
            wait_for_network_idle (bool, optional): Ожидать `networkidle`
                после каждого скролла (для сайтов с задержкой подгрузки
                через XHR/fetch). По умолчанию —
                `config.INFINITE_SCROLL_WAIT_NETWORK_IDLE`.

        Returns:
            ScrollResult: Итоговая статистика цикла (число итераций,
                причина остановки, затраченное время, финальная высота
                страницы и, если применимо, финальное количество элементов).
        """
        effective_enabled = enabled if enabled is not None else config.INFINITE_SCROLL_ENABLED
        if not effective_enabled:
            log_message("info", "Infinite Scroll: отключен конфигурацией — скроллинг не выполняется")
            return ScrollResult(0, ScrollStopReason.DISABLED.value, 0.0, 0)

        effective_max_scrolls = max_scrolls if max_scrolls is not None else config.INFINITE_SCROLL_MAX_SCROLLS
        effective_timeout = timeout_seconds if timeout_seconds is not None else config.INFINITE_SCROLL_TIMEOUT_SECONDS
        effective_max_height = max_page_height if max_page_height is not None else config.INFINITE_SCROLL_MAX_PAGE_HEIGHT
        effective_no_new_content = (
            max_no_new_content_attempts
            if max_no_new_content_attempts is not None
            else config.INFINITE_SCROLL_MAX_NO_NEW_CONTENT
        )
        effective_step = scroll_step_px if scroll_step_px is not None else config.INFINITE_SCROLL_STEP_PX
        effective_smooth = smooth if smooth is not None else config.INFINITE_SCROLL_SMOOTH
        effective_wait_network_idle = (
            wait_for_network_idle if wait_for_network_idle is not None else config.INFINITE_SCROLL_WAIT_NETWORK_IDLE
        )

        start_time = time.monotonic()

        try:
            last_height = cls._get_page_height(engine)
        except PlaywrightEngineError as exc:
            log_message("error", f"Infinite Scroll: не удалось получить высоту страницы: {exc}")
            return ScrollResult(0, ScrollStopReason.ERROR.value, 0.0, 0)

        current_item_count = cls._count_items(engine, item_selector, count_callback, None)

        log_message("info", "Infinite Scroll: скроллинг начат")

        iteration = 0
        no_new_content_streak = 0
        stop_reason = ScrollStopReason.MAX_SCROLLS  # запасное значение, переопределяется ниже

        while True:
            elapsed = time.monotonic() - start_time

            if effective_timeout > 0 and elapsed >= effective_timeout:
                stop_reason = ScrollStopReason.TIMEOUT
                break
            if effective_max_scrolls > 0 and iteration >= effective_max_scrolls:
                stop_reason = ScrollStopReason.MAX_SCROLLS
                break
            if effective_max_height > 0 and last_height >= effective_max_height:
                stop_reason = ScrollStopReason.MAX_HEIGHT
                break
            if (
                target_item_count is not None
                and target_item_count > 0
                and current_item_count is not None
                and current_item_count >= target_item_count
            ):
                stop_reason = ScrollStopReason.TARGET_COUNT
                break
            if stop_callback is not None:
                state = ScrollState(engine, iteration, elapsed, last_height, current_item_count)
                try:
                    should_stop = stop_callback(state)
                except Exception as exc:
                    log_message("error", f"Infinite Scroll: ошибка в пользовательском stop_callback: {exc}")
                    stop_reason = ScrollStopReason.ERROR
                    break
                if should_stop:
                    stop_reason = ScrollStopReason.CUSTOM_CALLBACK
                    break

            try:
                cls._perform_scroll(engine, effective_step, effective_smooth)
                cls._wait_between_scrolls(
                    config.INFINITE_SCROLL_DELAY_MODE,
                    config.INFINITE_SCROLL_DELAY_FIXED_SECONDS,
                    config.INFINITE_SCROLL_DELAY_MIN_SECONDS,
                    config.INFINITE_SCROLL_DELAY_MAX_SECONDS,
                )
                if effective_wait_network_idle:
                    engine.wait_for_load("networkidle")
                new_height = cls._get_page_height(engine)
            except PlaywrightEngineError as exc:
                log_message("error", f"Infinite Scroll: сбой во время прокрутки: {exc}")
                stop_reason = ScrollStopReason.ERROR
                break
            except Exception as exc:
                log_message("error", f"Infinite Scroll: непредвиденная ошибка во время прокрутки: {exc}")
                stop_reason = ScrollStopReason.ERROR
                break

            current_item_count = cls._count_items(engine, item_selector, count_callback, current_item_count)

            iteration += 1
            if new_height <= last_height:
                no_new_content_streak += 1
            else:
                no_new_content_streak = 0
            last_height = new_height

            if no_new_content_streak >= effective_no_new_content:
                stop_reason = ScrollStopReason.NO_NEW_CONTENT
                break

        elapsed_total = time.monotonic() - start_time
        log_message(
            "info",
            f"Infinite Scroll: завершено (итераций={iteration}, "
            f"причина={stop_reason.value}, время={elapsed_total:.1f}с)",
        )
        return ScrollResult(iteration, stop_reason.value, elapsed_total, last_height, current_item_count)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    with PlaywrightEngine(headless=False) as engine:
        engine.goto("https://infinite-scroll.com/demo/full-page/")
        result = InfiniteScroll.scroll(engine, max_scrolls=5, timeout_seconds=30)
        print(f"[{__file__}] Результат: {result}")


--- app/json_parser.py ---
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


--- app/login_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login Manager (Login Support).

Централизованный компонент аутентификации фреймворка (см.
`framework/ROADMAP.md`, Milestone 4 — Login Support).

Login Manager — единственная точка, через которую скрапер-модули должны
выполнять аутентификацию на сайтах, требующих логин. Он НЕ дублирует
существующие менеджеры, а координирует их вокруг единого понятия
"аутентификация":

    Login Manager
            │
     ┌──────┼────────────┬─────────────────┐
     ▼      ▼             ▼                 ▼
    Requests  Playwright  Cookie Manager   Configuration
    Engine    Engine      (persist/restore) Manager

* Requests Engine / Playwright Engine — Login Manager использует уже
  созданный вызывающим кодом движок (сессию/браузер) для выполнения
  логина; он НЕ создает `requests.Session`/браузер самостоятельно —
  идентичность клиента (User-Agent, headers, locale, timezone) уже
  применена этими движками через Request Profile Manager;
* Cookie Manager — после успешного логина куки сохраняются/обновляются
  через `CookieManager.update()`/`CookieManager.save()`
  (Requests) или `PlaywrightEngine.update_cookies()` (Playwright,
  который сам делегирует Cookie Manager) — Login Manager не хранит
  куки самостоятельно;
* Configuration Manager — лимит попыток, тайм-аут, срок жизни
  аутентифицированной сессии и заголовки Bearer/API Key берутся из
  `app/config.py` (.env), без хардкода;
* Logging — используется `app.utils.log_message()`, как и во всех
  остальных менеджерах. Пароли/токены/куки никогда не логируются.

Архитектура основана на паттерне Strategy (аналогично `ProxyProvider` в
`app/proxy_manager.py`): `AuthStrategy` — абстрактный интерфейс
аутентификации, конкретные стратегии (`RequestsFormLoginStrategy`,
`PlaywrightFormLoginStrategy`, `CookieSessionStrategy`,
`BearerTokenStrategy`, `ApiKeyStrategy`) реализуют конкретные методы.
Добавление нового способа аутентификации (например, OAuth) в будущем —
это просто новый класс, реализующий `AuthStrategy.authenticate()`, без
изменения `LoginManager` или других стратегий.

Login Manager НЕ парсит HTML в бизнес-объекты, НЕ извлекает данные, НЕ
экспортирует данные, НЕ управляет пагинацией и НЕ содержит логики,
специфичной для конкретного сайта (URL/селекторы форм передаются
вызывающим кодом при создании стратегии).
"""

import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse

from app import config
from app.cookie_manager import CookieManager
from app.utils import log_message

# Причины неуспеха/сбоя логина, при которых повтор попытки НЕ выполняется
# (неверные учетные данные, CAPTCHA, отсутствующая форма — повтор не поможет
# и может усилить риск блокировки/лишних попыток входа).
_NON_RETRYABLE_REASONS = frozenset({"invalid_credentials", "captcha_detected", "missing_form"})


class LoginError(Exception):
    """
    Единое исключение Login Support для сбоев, возникших во время
    аутентификации (сетевые ошибки движка, таймаут навигации/запроса,
    отсутствие ожидаемой формы логина).

    Args:
        message (str): Человекочитаемое описание ошибки.
        reason (str): Машиночитаемая причина — одна из: "invalid_credentials",
            "timeout", "missing_form", "captcha_detected", "expired_session",
            "unexpected_redirect", "unknown".
    """

    def __init__(self, message: str, reason: str = "unknown") -> None:
        super().__init__(message)
        self.reason = reason


@dataclass
class AuthCredentials:
    """
    Универсальный (не привязанный к конкретному сайту) набор данных для
    аутентификации. Каждая стратегия использует только нужные ей поля.
    """

    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    api_key: Optional[str] = None
    # Дополнительные поля формы логина (например, CSRF-токен, "remember_me").
    extra_fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class AuthResult:
    """Результат попытки аутентификации."""

    success: bool
    reason: Optional[str] = None
    session_id: Optional[str] = None


# =====================================================================
# LOGIN DETECTION
#     Переиспользуемая, не зависящая от конкретного сайта логика
#     обнаружения ситуаций, требующих (пере-)аутентификации.
# =====================================================================


class LoginDetector:
    """
    Набор статических, не хранящих состояние проверок для обнаружения
    ситуаций логина (см. `tasks/TASK.md`, раздел Login Detection).

    Не содержит селекторов/URL конкретных сайтов — только структурные
    проверки (HTTP-статус, наличие пароля в форме, совпадение URL с
    известным URL страницы логина, ключевые слова CAPTCHA).
    """

    @staticmethod
    def is_unauthorized(status_code: int) -> bool:
        """True, если ответ сигнализирует об отсутствии/истечении авторизации (401/403)."""
        return status_code in (401, 403)

    @staticmethod
    def was_redirected_to_login(current_url: str, login_url: str) -> bool:
        """
        True, если текущий URL страницы совпадает с URL страницы логина
        (сравнение по пути, без query/fragment — типичный признак редиректа
        неавторизованного запроса на страницу входа).
        """
        if not current_url or not login_url:
            return False
        return urlparse(current_url).path.rstrip("/") == urlparse(login_url).path.rstrip("/")

    @staticmethod
    def contains_login_form(html: str) -> bool:
        """True, если HTML содержит поле пароля (`<input type="password">`)."""
        if not html:
            return False
        return bool(re.search(r'type=["\']password["\']', html, re.IGNORECASE))

    @staticmethod
    def contains_captcha(html: str) -> bool:
        """
        True, если HTML содержит одно из ключевых слов CAPTCHA
        (`config.LOGIN_CAPTCHA_KEYWORDS`, регистронезависимо).
        """
        if not html:
            return False
        lowered = html.lower()
        return any(keyword in lowered for keyword in config.LOGIN_CAPTCHA_KEYWORDS)


# =====================================================================
# AUTH STRATEGIES
#     Паттерн Strategy: LoginManager не знает, КАК выполняется логин —
#     эта логика инкапсулирована в конкретных реализациях AuthStrategy.
# =====================================================================


class AuthStrategy(ABC):
    """
    Абстрактный способ аутентификации.

    Любой новый метод аутентификации (OAuth, MFA и т.д.) должен
    реализовать этот интерфейс. `LoginManager` работает только через него
    и никогда не содержит специфичной для конкретной стратегии логики.
    """

    @abstractmethod
    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """
        Выполняет один шаг аутентификации.

        Args:
            credentials (AuthCredentials): Учетные данные для этой попытки.

        Returns:
            AuthResult: Результат попытки (успех/неуспех + причина).

        Raises:
            LoginError: При технических сбоях (таймаут, сеть, отсутствие
                ожидаемой формы) — вызывающий код (`LoginManager`) решает,
                стоит ли повторять попытку, на основе `LoginError.reason`.
        """
        raise NotImplementedError


def _requests_session_cookies_to_list(session: Any) -> List[Dict[str, Any]]:
    """
    Конвертирует куки `requests.Session.cookies` (RequestsCookieJar) в
    универсальный формат Cookie Manager (список словарей
    `{"name", "value", "domain", "path"}`).
    """
    return [
        {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain or "",
            "path": cookie.path or "/",
        }
        for cookie in session.cookies
    ]


class RequestsFormLoginStrategy(AuthStrategy):
    """
    Аутентификация через HTML-форму логина (username/password) с
    использованием `RequestsEngine` (без браузера).

    После успешного логина куки сессии сохраняются через Cookie Manager
    (если `config.LOGIN_COOKIE_PERSISTENCE` включен), чтобы сессия могла
    быть восстановлена в будущих запусках через `CookieSessionStrategy`.
    """

    def __init__(
        self,
        engine: Any,
        login_url: str,
        username_field: str = "username",
        password_field: str = "password",
        extra_data: Optional[Dict[str, str]] = None,
        success_check: Optional[Callable[[Any], bool]] = None,
        failure_check: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """
        Args:
            engine (RequestsEngine): Движок, через который отправляется
                POST-запрос логина (уже несет применённые Request Profile/
                Cookie/Proxy Manager настройки).
            login_url (str): URL, на который отправляется форма логина.
            username_field (str): Имя поля формы для логина/email.
            password_field (str): Имя поля формы для пароля.
            extra_data (Dict[str, str], optional): Дополнительные
                статические поля формы (например, CSRF-токен, "remember_me").
            success_check (Callable[[Response], bool], optional): Кастомная
                проверка успеха по `requests.Response` (переопределяет
                дефолтную эвристику "нет формы логина в ответе").
            failure_check (Callable[[Response], bool], optional): Кастомная
                проверка неуспеха по `requests.Response` (например, наличие
                текста "Invalid password" на странице).
        """
        self.engine = engine
        self.login_url = login_url
        self.username_field = username_field
        self.password_field = password_field
        self.extra_data = extra_data or {}
        self.success_check = success_check
        self.failure_check = failure_check

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        from app.requests_engine import RequestsEngineError  # локальный импорт: избегаем циклической зависимости

        data = {
            self.username_field: credentials.username or "",
            self.password_field: credentials.password or "",
            **self.extra_data,
            **credentials.extra_fields,
        }

        try:
            response = self.engine.post(self.login_url, data=data)
        except RequestsEngineError as exc:
            raise LoginError(f"Запрос логина завершился ошибкой: {exc}", reason="timeout") from exc

        if LoginDetector.is_unauthorized(response.status_code):
            return AuthResult(success=False, reason="invalid_credentials")

        html = response.text

        if LoginDetector.contains_captcha(html):
            return AuthResult(success=False, reason="captcha_detected")

        if self.failure_check is not None and self.failure_check(response):
            return AuthResult(success=False, reason="invalid_credentials")

        if self.success_check is not None:
            if not self.success_check(response):
                return AuthResult(success=False, reason="invalid_credentials")
        elif LoginDetector.contains_login_form(html):
            # Дефолтная эвристика: форма логина всё еще на странице -> вход не удался.
            return AuthResult(success=False, reason="invalid_credentials")

        if config.LOGIN_COOKIE_PERSISTENCE:
            CookieManager.update(_requests_session_cookies_to_list(self.engine.session))

        return AuthResult(success=True)


class PlaywrightFormLoginStrategy(AuthStrategy):
    """
    Аутентификация через HTML-форму логина с использованием
    `PlaywrightEngine` (заполнение полей и клик по кнопке отправки в
    реальном браузере — для сайтов с JS-защитой/динамическими формами).

    После успешного логина куки браузерного контекста сохраняются через
    `PlaywrightEngine.update_cookies()` (который сам делегирует Cookie
    Manager) — Login Manager не дублирует эту логику.
    """

    def __init__(
        self,
        engine: Any,
        login_url: str,
        username_selector: str,
        password_selector: str,
        submit_selector: str,
        failure_selector: Optional[str] = None,
        success_check: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """
        Args:
            engine (PlaywrightEngine): Движок, через который выполняется
                навигация и заполнение формы.
            login_url (str): URL страницы логина.
            username_selector (str): CSS/text-селектор поля логина/email.
            password_selector (str): CSS/text-селектор поля пароля.
            submit_selector (str): CSS/text-селектор кнопки отправки формы.
            failure_selector (str, optional): Селектор, появляющийся только
                при неудачном логине (например, ".error-message").
            success_check (Callable[[PlaywrightEngine], bool], optional):
                Кастомная проверка успеха (переопределяет дефолтную
                эвристику "нет формы логина в HTML после отправки").
        """
        self.engine = engine
        self.login_url = login_url
        self.username_selector = username_selector
        self.password_selector = password_selector
        self.submit_selector = submit_selector
        self.failure_selector = failure_selector
        self.success_check = success_check

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        from app.playwright_engine import PlaywrightEngineError  # локальный импорт: избегаем циклической зависимости

        try:
            self.engine.goto(self.login_url)
            self.engine.wait_for_selector(self.username_selector)
            self.engine.page.fill(self.username_selector, credentials.username or "")
            self.engine.page.fill(self.password_selector, credentials.password or "")
            self.engine.page.click(self.submit_selector)
            self.engine.wait_for_load("networkidle")
        except PlaywrightEngineError as exc:
            raise LoginError(f"Навигация/заполнение формы логина завершилось ошибкой: {exc}", reason="timeout") from exc

        html = self.engine.content()

        if LoginDetector.contains_captcha(html):
            return AuthResult(success=False, reason="captcha_detected")

        if self.failure_selector is not None:
            try:
                self.engine.page.wait_for_selector(self.failure_selector, timeout=1000)
                return AuthResult(success=False, reason="invalid_credentials")
            except Exception:
                pass  # селектор ошибки не появился — логин, вероятно, успешен

        if self.success_check is not None:
            if not self.success_check(self.engine):
                return AuthResult(success=False, reason="invalid_credentials")
        elif LoginDetector.contains_login_form(html):
            return AuthResult(success=False, reason="invalid_credentials")

        if config.LOGIN_COOKIE_PERSISTENCE:
            self.engine.update_cookies()

        return AuthResult(success=True)


class CookieSessionStrategy(AuthStrategy):
    """
    Восстанавливает аутентифицированную сессию исключительно из ранее
    сохраненных куки (Cookie Manager), без учетных данных — используется,
    когда логин уже был выполнен в прошлом запуске и куки еще валидны.
    """

    def __init__(self, validate: Optional[Callable[[], bool]] = None) -> None:
        """
        Args:
            validate (Callable[[], bool], optional): Дополнительная проверка
                валидности восстановленной сессии (например, тестовый запрос
                к защищенной странице). Если не передана, сессия считается
                валидной при наличии хотя бы одной сохраненной куки.
        """
        self.validate = validate

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        cookies = CookieManager.load()
        if not cookies:
            return AuthResult(success=False, reason="expired_session")

        if self.validate is not None and not self.validate():
            return AuthResult(success=False, reason="expired_session")

        return AuthResult(success=True)


class BearerTokenStrategy(AuthStrategy):
    """
    Аутентификация через Bearer Token — токен добавляется как заголовок
    к переданной сессии/движку без выполнения HTTP-запроса логина.
    """

    def __init__(self, session: Any, header_name: Optional[str] = None) -> None:
        """
        Args:
            session (requests.Session): Сессия, к которой применяется заголовок.
            header_name (str, optional): Имя заголовка.
                По умолчанию — `config.LOGIN_BEARER_HEADER_NAME`.
        """
        self.session = session
        self.header_name = header_name or config.LOGIN_BEARER_HEADER_NAME

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        if not credentials.token:
            return AuthResult(success=False, reason="invalid_credentials")

        self.session.headers[self.header_name] = f"Bearer {credentials.token}"
        return AuthResult(success=True)


class ApiKeyStrategy(AuthStrategy):
    """
    Аутентификация через статический API Key — добавляется как заголовок
    к переданной сессии без выполнения HTTP-запроса логина.
    """

    def __init__(self, session: Any, header_name: Optional[str] = None) -> None:
        """
        Args:
            session (requests.Session): Сессия, к которой применяется заголовок.
            header_name (str, optional): Имя заголовка.
                По умолчанию — `config.LOGIN_API_KEY_HEADER_NAME`.
        """
        self.session = session
        self.header_name = header_name or config.LOGIN_API_KEY_HEADER_NAME

    def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        if not credentials.api_key:
            return AuthResult(success=False, reason="invalid_credentials")

        self.session.headers[self.header_name] = credentials.api_key
        return AuthResult(success=True)


# =====================================================================
# LOGIN MANAGER
#     Единая точка входа: оркестрирует выбранную стратегию, повторы,
#     логирование и переиспользование уже аутентифицированных сессий.
# =====================================================================


class LoginManager:
    """
    Централизованная точка входа для аутентификации.

    Хранит только факт "сессия X аутентифицирована в момент времени T"
    (`_authenticated_sessions`) — сам процесс логина полностью делегирован
    переданной `AuthStrategy`. Это позволяет `ensure_login()` избегать
    повторного логина для уже аутентифицированной логической сессии.
    """

    # session_id -> monotonic-время последней успешной аутентификации.
    _authenticated_sessions: Dict[str, float] = {}

    @classmethod
    def login(
        cls,
        strategy: AuthStrategy,
        credentials: Optional[AuthCredentials] = None,
        session_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
    ) -> AuthResult:
        """
        Выполняет аутентификацию через переданную стратегию, повторяя
        попытку только при технических сбоях (`LoginError`, отличных от
        "invalid_credentials"/"captcha_detected"/"missing_form") — эти три
        причины считаются окончательными и никогда не повторяются, чтобы
        не спровоцировать блокировку аккаунта/IP.

        Args:
            strategy (AuthStrategy): Реализация способа аутентификации.
            credentials (AuthCredentials, optional): Учетные данные.
                По умолчанию — пустые (валидно для `CookieSessionStrategy`).
            session_id (str, optional): Идентификатор логической сессии —
                при успехе помечается как аутентифицированная для
                последующего переиспользования через `ensure_login()`.
            max_attempts (int, optional): Максимум попыток.
                По умолчанию — `config.LOGIN_MAX_ATTEMPTS`.

        Returns:
            AuthResult: Результат последней попытки.
        """
        active_credentials = credentials or AuthCredentials()
        attempts = max_attempts if max_attempts is not None else config.LOGIN_MAX_ATTEMPTS

        session_suffix = f" (session={session_id})" if session_id else ""
        log_message("info", f"Попытка логина начата{session_suffix}")

        last_result = AuthResult(success=False, reason="unknown")

        for attempt in range(1, max(attempts, 1) + 1):
            try:
                result = strategy.authenticate(active_credentials)
            except LoginError as exc:
                log_message("error", f"Ошибка логина{session_suffix}: {exc} (причина={exc.reason})")
                last_result = AuthResult(success=False, reason=exc.reason)
                if exc.reason in _NON_RETRYABLE_REASONS:
                    return last_result
                continue

            if result.success:
                log_message("info", f"Логин успешен{session_suffix}")
                if session_id:
                    cls._authenticated_sessions[session_id] = time.monotonic()
                    result.session_id = session_id
                return result

            log_message("error", f"Логин не удался{session_suffix} (причина={result.reason})")
            last_result = result
            if result.reason in _NON_RETRYABLE_REASONS:
                return last_result

        return last_result

    @classmethod
    def is_session_authenticated(cls, session_id: str) -> bool:
        """
        Проверяет, аутентифицирована ли логическая сессия и не истек ли
        срок её жизни (`config.LOGIN_SESSION_LIFETIME_SECONDS`, 0 — без
        ограничения). Истекшая запись автоматически удаляется.
        """
        authenticated_at = cls._authenticated_sessions.get(session_id)
        if authenticated_at is None:
            return False

        lifetime = config.LOGIN_SESSION_LIFETIME_SECONDS
        if lifetime > 0 and (time.monotonic() - authenticated_at) >= lifetime:
            cls._authenticated_sessions.pop(session_id, None)
            log_message("info", f"Сессия '{session_id}' истекла (превышен срок жизни логина)")
            return False

        return True

    @classmethod
    def ensure_login(
        cls,
        strategy: AuthStrategy,
        credentials: Optional[AuthCredentials] = None,
        session_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
    ) -> AuthResult:
        """
        Переиспользует уже аутентифицированную сессию, если она
        существует и не истекла (`is_session_authenticated()`), иначе
        выполняет полный логин через `login()`.

        Это основной метод для вызывающего кода (скрапер-модулей) —
        избавляет от необходимости самостоятельно проверять, нужен ли
        повторный вход перед каждым скрапинг-джобом.

        Args:
            strategy (AuthStrategy): Реализация способа аутентификации.
            credentials (AuthCredentials, optional): Учетные данные.
            session_id (str, optional): Идентификатор логической сессии.
            max_attempts (int, optional): Максимум попыток логина.

        Returns:
            AuthResult: Результат (успех переиспользования или нового логина).
        """
        if session_id and cls.is_session_authenticated(session_id):
            log_message("info", f"Сессия '{session_id}' переиспользована (уже аутентифицирована)")
            return AuthResult(success=True, session_id=session_id)

        return cls.login(strategy, credentials, session_id=session_id, max_attempts=max_attempts)

    @classmethod
    def invalidate_session(cls, session_id: str) -> None:
        """Явно помечает сессию как неаутентифицированную (например, после 401 в середине скрапинга)."""
        if cls._authenticated_sessions.pop(session_id, None) is not None:
            log_message("info", f"Сессия '{session_id}' помечена как неаутентифицированная")

    @classmethod
    def reset(cls) -> None:
        """Сбрасывает состояние всех аутентифицированных сессий (используется в тестах)."""
        cls._authenticated_sessions.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()
    strategy = RequestsFormLoginStrategy(
        engine=engine,
        login_url="https://httpbin.org/post",  # демо-эндпоинт, не реальная форма логина
        username_field="username",
        password_field="password",
        success_check=lambda response: response.status_code == 200,
    )

    result = LoginManager.login(strategy, AuthCredentials(username="demo", password="demo"), session_id="demo-job")
    print(f"[{__file__}] Результат логина: {result}")
    print(f"[{__file__}] Сессия аутентифицирована: {LoginManager.is_session_authenticated('demo-job')}")

    engine.close()


--- app/main.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Добавляет starter-project в пути Python

from app.checkpoint_manager import CheckpointManager
from app.config import EXPORT_INCREMENTAL_ENABLED

from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError
from app.resume_manager import ResumeManager
from app.scraper import fetch_page_data
from app.parser import parse_listing, parse_html_data
from app.exporter import save_to_csv, save_to_json, IncrementalCSVWriter, IncrementalJSONWriter, BatchWriter
from app.utils import log_message


def _run_incremental(raw_pages_content) -> int:
    """
    Incremental Saving + Batch Writer: парсит каждую страницу по
    отдельности и передает полученные записи в `BatchWriter`, который
    буферизует их в памяти и сбрасывает на диск (через
    `IncrementalCSVWriter`/`IncrementalJSONWriter`) пачками, а не при
    каждом вызове — это уменьшает количество операций записи на диск по
    сравнению с прямым вызовом `write_records()` на каждой странице,
    сохраняя устойчивость к сбоям уже сброшенных данных (Incremental
    Saving).

    Дополнительно интегрирован Checkpoint Manager (см. `tasks/TASK.md`,
    `framework/ROADMAP.md` Milestone 6): после обработки каждой страницы
    прогресс (номер страницы, количество обработанных/сброшенных на диск
    записей) передается в `CheckpointManager.record_page()`, который сам
    решает, нужно ли реально записать чекпоинт на диск в этот момент
    (на основе `CHECKPOINT_INTERVAL_PAGES/RECORDS/SECONDS`). Checkpoint
    Manager только записывает прогресс — он не влияет на сам цикл
    парсинга/экспорта и не может его прервать (см. Error Handling в
    `app/checkpoint_manager.py`).

    Resume Support (см. `app/resume_manager.py`, `tasks/TASK.md`
    Milestone 6): перед началом обработки `ResumeManager` проверяет,
    есть ли валидный чекпоинт от прерванной сессии. Если да —
    восстанавливает `run_id`/счётчики в тот же `CheckpointManager`, а
    CSV/JSON writer'ы открываются в режиме дозаписи (`append=True`),
    чтобы уже экспортированные записи не были перезаписаны/потеряны.
    Страницы, номер которых `<= decision.start_page`, пропускаются —
    это предотвращает повторную обработку уже завершённой работы.

    Память используется только под записи текущего буфера (максимум
    `BATCH_WRITER_BATCH_SIZE` записей) — предыдущие сброшенные батчи уже
    высвобождены сборщиком мусора. Это позволяет обрабатывать очень
    большие датасеты (сотни тысяч записей) без пропорционального роста
    потребления RAM.

    Args:
        raw_pages_content: Список строк HTML страниц (от `fetch_page_data`).

    Returns:
        int: Общее количество записей, успешно сброшенных на диск через BatchWriter.
    """
    # Resume Support: ищем чекпоинт от прерванной сессии ДО создания
    # нового run_id — если восстановление удастся, ResumeManager сам
    # перезапишет run_id в checkpoint.state значением из чекпоинта.
    fallback_run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    checkpoint = CheckpointManager(run_id=fallback_run_id)

    decision = ResumeManager().resume(checkpoint)

    if decision.resumed:
        log_message(
            "info",
            f"[{__file__}] Resume Support: восстановлена сессия '{checkpoint.state.run_id}' "
            f"(страница={decision.start_page}, экспортировано={decision.exported_count})",
        )
    else:
        checkpoint.start(status="running", total_pages=len(raw_pages_content))

    processed_total = decision.processed_count
    checkpoint_failed = False

    # Resume Support Integration с Incremental Saving (см. tasks/TASK.md,
    # "Integration with Incremental Saving"): при восстановленной сессии
    # writer'ы открываются в режиме дозаписи (append=True), чтобы уже
    # экспортированные ранее записи оставались нетронутыми — никогда не
    # перезаписываются. При отсутствии восстановления (append=False)
    # поведение полностью идентично поведению до появления Resume Support.
    with IncrementalCSVWriter("output_results.csv", append=decision.resumed) as csv_writer, \
            IncrementalJSONWriter("output_results.json", append=decision.resumed) as json_writer:

        with BatchWriter([csv_writer, json_writer]) as batch_writer:
            for idx, html in enumerate(raw_pages_content, 1):
                # Duplicate Protection (см. tasks/TASK.md, "Duplicate
                # Protection"): страницы, уже обработанные и сброшенные
                # на диск в прошлой (прерванной) сессии, пропускаются —
                # восстановленное состояние продолжает строго ПОСЛЕ
                # последнего успешно зафиксированного чекпоинта.
                if idx <= decision.start_page:
                    continue

                try:
                    page_records = parse_listing(html)
                except Exception as e:
                    log_message("error", f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
                    continue

                if not page_records:
                    continue

                batch_writer.add_records(page_records)
                processed_total += len(page_records)

                # Checkpoint Manager сам решает (на основе настроенных
                # интервалов), нужно ли реально записать чекпоинт сейчас.
                # Сбой сохранения чекпоинта НИКОГДА не должен прерывать
                # скрапинг (см. TASK.md, раздел "Error Handling") —
                # CheckpointManager сам это гарантирует, здесь только
                # защита на случай непредвиденного исключения самого вызова.
                try:
                    checkpoint.record_page(
                        page_number=idx,
                        processed_count=processed_total,
                        exported_count=batch_writer.total_flushed + decision.exported_count,
                    )
                except Exception as cp_exc:
                    if not checkpoint_failed:
                        log_message("error", f"[{__file__}] Checkpoint Manager: непредвиденная ошибка: {cp_exc}")
                        checkpoint_failed = True

        # Integration with Batch Writer (см. tasks/TASK.md, "Integration
        # with Batch Writer"): к этому моменту `with BatchWriter(...)` уже
        # завершился, и BatchWriter.close() выполнил shutdown-сброс
        # оставшихся в буфере записей (если BATCH_WRITER_FLUSH_ON_SHUTDOWN
        # включен) — весь ещё не сброшенный "хвост" гарантированно попал
        # на диск ДО финальной записи чекпоинта ниже, поэтому чекпоинт
        # никогда не укажет на страницу, чьи записи реально не сохранены.
        total_records = batch_writer.total_flushed + decision.exported_count

    checkpoint.finish(status="completed", processed_count=processed_total, exported_count=total_records)

    return total_records




def main() -> None:
    """
    Главная точка входа. Управляет жизненным циклом парсера.

    Поддерживает два режима экспорта (см. `app/config.py`,
    `EXPORT_INCREMENTAL_ENABLED`):
      - Incremental Saving + Batch Writer (по умолчанию) — каждая
        страница парсится, записи буферизуются в памяти и сбрасываются
        в CSV/JSON пачками (см. `_run_incremental()`).
      - Batch-режим (обратная совместимость) — все страницы парсятся,
        результаты копятся в памяти и экспортируются одним вызовом
        `save_to_csv`/`save_to_json` после завершения скрапинга —
        поведение, идентичное поведению проекта до появления
        Incremental Saving.
    """
    print("=" * 70)
    print(f"[{__file__}] ЗАПУСК ПАРСЕРА")
    print("=" * 70)

    try:
        # 1. Запуск браузерной автоматизации через централизованный Playwright Engine
        # (идентичность, куки и прокси применяются автоматически)
        with PlaywrightEngine() as engine:

            # 2. Сбор данных (Scraping)
            # Передаем движок в scraper.py для обхода страниц
            try:
                raw_pages_content = fetch_page_data(engine)
            except PlaywrightEngineError as e:
                print(f"[{__file__}] Критическая ошибка браузера: {e}")
                sys.exit(1)

            if not raw_pages_content:
                print(f"[{__file__}] Критическая ошибка: Нечего парсить (список страниц пуст).")
                sys.exit(1)

            # 3. Обработка данных (Parsing) + 4. Экспорт результатов (Export)
            if EXPORT_INCREMENTAL_ENABLED:
                print(f"[{__file__}] Incremental Saving + Batch Writer включены: обработка {len(raw_pages_content)} страниц(ы)...")
                total_records = _run_incremental(raw_pages_content)

                if total_records:
                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО (Всего записей: {total_records})")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат.")
            else:
                # Batch-режим — прежнее поведение (обратная совместимость)
                print(f"[{__file__}] Начало парсинга контента (batch-режим)...")
                scraped_results = parse_html_data(raw_pages_content)

                if scraped_results:
                    print(f"[{__file__}] Экспорт данных (Всего элементов: {len(scraped_results)})...")
                    save_to_csv(scraped_results, "output_results.csv")
                    save_to_json(scraped_results, "output_results.json")

                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат. Файлы не созданы.")

    except KeyError as ke:
        print(f"[{__file__}] Ошибка конфигурации или структуры: {ke}")
        sys.exit(1)
    except Exception as e:
        print(f"[{__file__}] Критический сбой в главном потоке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


--- app/pagination.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pagination.

Централизованный компонент пагинации для скрапинга многостраничных
сайтов (см. `framework/ROADMAP.md`, Milestone 4).

Pagination — единственная точка, через которую скрапер-модули должны
выполнять навигацию между страницами. Он НЕ содержит логики парсинга/
экспорта/логина/бесконечного скролла и НЕ знает о селекторах конкретных
сайтов — единственное, что он умеет, это итерировать страницы по одной
из настраиваемых стратегий и останавливаться по одному из настраиваемых
условий.

Pagination engine-независим: он никогда не вызывает `engine.get()` или
`engine.goto()` сам. Вместо этого вызывающий код передаёт `fetch_callback`
— функцию, которая принимает `PageContext` и возвращает `PageFetchResult`.
Это позволяет использовать Paginator как с Requests Engine, так и с
Playwright Engine без изменения самих движков.

    Paginator.paginate(fetch_callback, pagination_type, ...)
            │
            ▼
      loop: build PageContext (url/params for url/offset/ajax;
                               None for next_button/custom)
            │
            ▼
      fetch_callback(context) -> PageFetchResult
            │           (caller internally uses RequestsEngine.get()
            │            OR PlaywrightEngine.goto()+content())
            ▼
      Paginator evaluates stop conditions
      (last_page / no_items / max_pages / duplicate / custom_callback / error)
            │
            ▼
      DelayManager.wait(...) between pages (reused, not reimplemented)

Поддерживаемые стратегии (PaginationType):
    URL         — генерация URL с меняющимся query-параметром (?page=2,3,4...)
    OFFSET      — генерация URL с меняющимся offset-параметром (?offset=20,40,60...)
    NEXT_BUTTON — Playwright: клик по кнопке "Next" (требует selector).
    AJAX        — то же, что URL/Offset, но подразумевает API-запрос;
                  генерация URL/params идентична, вызывающий код решает,
                  как выполнять запрос (Requests GET или Playwright goto).
    CUSTOM      — полностью делегирована вызывающему коду через
                  `custom_context_generator`; для самых сложных сайтов.

Пример использования (Requests Engine):

    from app.pagination import Paginator, PaginationType, PageContext, PageFetchResult
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()
    results = []

    def fetch(ctx: PageContext) -> PageFetchResult:
        resp = engine.get(ctx.url, params=ctx.params)
        items = resp.json() if ctx.pagination_type == PaginationType.AJAX else resp.text
        return PageFetchResult(
            content=items,
            item_count=len(items) if isinstance(items, list) else None,
            dedupe_key=resp.url,
        )

    for page_result in Paginator.paginate(
        fetch, PaginationType.URL, max_pages=5,
        url="https://api.example.com/items",
        page_param="page", start_page=1, page_step=1,
    ):
        results.append(page_result.content)

Пример использования (Playwright Engine + Next Button):

    from app.pagination import Paginator, PaginationType, PageContext, PageFetchResult
    from app.playwright_engine import PlaywrightEngine

    with PlaywrightEngine() as engine:
        engine.goto("https://example.com/items")

        def fetch(ctx: PageContext) -> PageFetchResult:
            if ctx.use_next_button:
                success = Paginator.click_next_button(engine, "a.next, button.next")
                if not success:
                    return PageFetchResult(content=engine.content(), has_next=False)
            return PageFetchResult(content=engine.content())

        for page_result in Paginator.paginate(
            fetch, PaginationType.NEXT_BUTTON,
            next_button_selector="a.next, button.next",
            max_pages=10,
        ):
            pass  # page_result.content содержит HTML очередной страницы
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from app import config
from app.delay_manager import DelayManager
from app.utils import log_message


class PaginationError(Exception):
    """
    Единое исключение Pagination для непредвиденных сбоев конфигурации
    (например, некорректных аргументов), не связанных с ожидаемыми
    условиями остановки цикла пагинации.

    Сбои самого fetch_callback во время запроса НЕ поднимаются как это
    исключение — они обрабатываются graceful (см. `PaginationStopReason.ERROR`),
    чтобы одна неудачная страница не прерывала весь процесс скрапинга.
    """


class PaginationType(str, Enum):
    """Стратегия пагинации."""

    URL = "url"
    OFFSET = "offset"
    NEXT_BUTTON = "next_button"
    AJAX = "ajax"
    CUSTOM = "custom"


class PaginationStopReason(str, Enum):
    """Причина остановки цикла пагинации."""

    LAST_PAGE = "last_page"
    NO_ITEMS = "no_items"
    MAX_PAGES = "max_pages"
    DUPLICATE_PAGE = "duplicate_page"
    CUSTOM_CALLBACK = "custom_callback"
    ERROR = "error"


@dataclass
class PageContext:
    """
    Контекст очередной страницы, передаваемый в `fetch_callback`.

    Атрибуты:
        url (str): URL страницы (для URL/Offset/AJAX/CUSTOM).
        params (dict, optional): Query-параметры для запроса.
        page_number (int): Номер текущей страницы (1-based).
        pagination_type (PaginationType): Текущая стратегия.
        use_next_button (bool): True, если стратегия NEXT_BUTTON
            (в этом случае fetch_callback должен сам кликнуть кнопку
            и вернуть контент).
        custom_data (Any, optional): Произвольные данные от
            `custom_context_generator` (только для CUSTOM).
    """

    url: str
    page_number: int
    pagination_type: PaginationType
    params: Optional[Dict[str, Any]] = None
    use_next_button: bool = False
    custom_data: Any = None


@dataclass
class PageFetchResult:
    """
    Результат, возвращаемый `fetch_callback` после получения одной страницы.

    Атрибуты:
        content (Any): HTML/JSON/текст страницы (может быть любым —
            Paginator не парсит его, а просто передаёт в итератор).
        item_count (int, optional): Количество элементов на странице
            (для условия остановки NO_ITEMS). Если None — не проверяется.
        has_next (bool, optional): Явный признак наличия следующей страницы
            (для сайтов, где это можно определить до следующего запроса).
            По умолчанию True (если не указано иное).
        dedupe_key (str, optional): Уникальный ключ для обнаружения
            дублирующихся страниц (например, URL ответа, заголовок, hash).
            Если None — не проверяется.
    """

    content: Any
    item_count: Optional[int] = None
    has_next: Optional[bool] = None
    dedupe_key: Optional[str] = None


@dataclass
class PageResult:
    """
    Итоговый результат одной итерации пагинации, возвращаемый
    генератором `Paginator.paginate()`.

    Атрибуты:
        page_number (int): Номер страницы (1-based).
        content (Any): Содержимое страницы (как вернул fetch_callback).
        stop_reason (str, optional): Причина остановки (только в
            последнем элементе итератора; для всех остальных — None).
        pages_fetched (int, optional): Общее число успешно загруженных
            страниц (только в последнем элементе).
        elapsed_seconds (float, optional): Общее время пагинации
            (только в последнем элементе).
    """

    page_number: int
    content: Any
    stop_reason: Optional[str] = None
    pages_fetched: Optional[int] = None
    elapsed_seconds: Optional[float] = None


class Paginator:
    """
    Централизованный исполнитель цикла пагинации.

    Не зависит от конкретного движка: вызывающий код передаёт
    `fetch_callback`, который использует Requests Engine или
    Playwright Engine по своему усмотрению.

    Пагинация — не Infinite Scroll, она не выполняется на уже
    открытой странице. Для каждой новой страницы (кроме NEXT_BUTTON)
    требуется новый запрос/навигация через fetch_callback.
    """

    # =====================================================================
    # ГЕНЕРАТОРЫ URL/ПАРАМЕТРОВ (для URL, OFFSET, AJAX)
    # =====================================================================

    @staticmethod
    def _build_url_params(
        base_url: str,
        param_name: str,
        value: int,
        existing_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Строит query-параметры для URL/Offset/AJAX пагинации.

        Args:
            base_url: Базовый URL (без параметров).
            param_name: Имя параметра (например, "page" или "offset").
            value: Значение параметра.
            existing_params: Дополнительные статические параметры.

        Returns:
            Dict[str, Any]: Query-параметры для запроса.
        """
        params = dict(existing_params or {})
        params[param_name] = value
        return params

    # =====================================================================
    # ПОМОЩНИК ДЛЯ NEXT BUTTON (Playwright)
    # =====================================================================

    @staticmethod
    def click_next_button(
        engine: Any,
        selector: str,
        timeout_ms: Optional[float] = None,
    ) -> bool:
        """
        Пытается кликнуть по кнопке "Next" на текущей странице Playwright.

        Вызывается из fetch_callback при стратегии NEXT_BUTTON.

        Args:
            engine: Экземпляр PlaywrightEngine (с уже открытой страницей).
            selector: CSS-селектор кнопки перехода на следующую страницу.
            timeout_ms: Таймаут ожидания селектора (мс).
                По умолчанию — config.PLAYWRIGHT_TIMEOUT_MS.

        Returns:
            bool: True, если кнопка найдена и кликнута (страница перешла);
                  False, если кнопка не найдена (считается последней
                  страницей — без исключения).
        """
        from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError

        effective_timeout = timeout_ms if timeout_ms is not None else config.PLAYWRIGHT_TIMEOUT_MS

        try:
            element = engine.page.wait_for_selector(selector, timeout=effective_timeout)
            if element is None:
                return False
            # Проверяем, что кнопка не disabled
            is_disabled = engine.page.evaluate(
                f"document.querySelector('{selector}')?.disabled ?? false"
            )
            if is_disabled:
                return False
            element.click()
            engine.wait_for_load("networkidle")
            return True
        except PlaywrightEngineError:
            # Селектор не появился — считаем последней страницей
            return False
        except Exception:
            # Любая другая ошибка клика — тоже graceful
            return False

    # =====================================================================
    # ОСНОВНАЯ ТОЧКА ВХОДА
    # =====================================================================

    @classmethod
    def paginate(
        cls,
        fetch_callback: Callable[[PageContext], PageFetchResult],
        pagination_type: Union[PaginationType, str],
        *,
        # --- Общие параметры ---
        url: Optional[str] = None,
        existing_params: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        timeout_seconds: Optional[float] = None,
        stop_callback: Optional[Callable[[int, Any], bool]] = None,
        detect_duplicates: Optional[bool] = None,
        # --- URL / Offset ---
        page_param: Optional[str] = None,
        start_page: Optional[int] = None,
        page_step: Optional[int] = None,
        offset_param: Optional[str] = None,
        start_offset: Optional[int] = None,
        offset_step: Optional[int] = None,
        # --- Next Button ---
        next_button_selector: Optional[str] = None,
        # --- Custom ---
        custom_context_generator: Optional[Callable[[int, "PageContext"], Optional[PageContext]]] = None,
        # --- Delay ---
        delay_mode: Optional[str] = None,
        delay_fixed_seconds: Optional[float] = None,
        delay_min_seconds: Optional[float] = None,
        delay_max_seconds: Optional[float] = None,
    ) -> List[PageResult]:
        """
        Выполняет цикл пагинации, вызывая `fetch_callback` для каждой
        страницы, пока не сработает одно из условий остановки.

        Все условия остановки проверяются одновременно — цикл завершается
        по первому сработавшему. Любой аргумент, не переданный явно,
        берётся из Configuration Manager (`app/config.py`).

        Args:
            fetch_callback: Функция, принимающая `PageContext` и
                возвращающая `PageFetchResult`. Вызывается один раз
                на страницу. Должна быть чистой (без побочных эффектов,
                кроме самого запроса) — Paginator сам управляет
                количеством вызовов и паузами между ними.
            pagination_type: Стратегия пагинации ("url", "offset",
                "next_button", "ajax", "custom").

        --- Общие параметры ---
            url: Базовый URL (обязателен для URL/Offset/AJAX/CUSTOM).
            existing_params: Статические query-параметры, добавляемые
                к каждому запросу.
            max_pages: Максимальное количество страниц. 0 — без
                ограничения. По умолчанию — config.PAGINATION_MAX_PAGES.
            timeout_seconds: Общий таймаут цикла пагинации (секунды).
                0 — без ограничения. По умолчанию —
                config.PAGINATION_TIMEOUT_SECONDS.
            stop_callback: Пользовательская функция остановки.
                Принимает (page_number, content), возвращает True
                для немедленной остановки.
            detect_duplicates: Включает обнаружение дублирующихся
                страниц (по dedupe_key из fetch_callback).
                По умолчанию — config.PAGINATION_DUPLICATE_DETECTION.

        --- Параметры URL/Offset пагинации ---
            page_param: Имя query-параметра для URL-пагинации
                (например, "page"). По умолчанию —
                config.PAGINATION_PAGE_PARAM.
            start_page: Начальное значение счётчика страниц
                (например, 1). По умолчанию —
                config.PAGINATION_START_PAGE.
            page_step: Шаг счётчика страниц (например, 1).
                По умолчанию — config.PAGINATION_PAGE_STEP.
            offset_param: Имя query-параметра для offset-пагинации
                (например, "offset"). По умолчанию —
                config.PAGINATION_OFFSET_PARAM.
            start_offset: Начальное значение offset (например, 0
                или 20). По умолчанию —
                config.PAGINATION_START_OFFSET.
            offset_step: Шаг offset (например, 20).
                По умолчанию — config.PAGINATION_OFFSET_STEP.

        --- Параметры Next Button ---
            next_button_selector: CSS-селектор кнопки "Next"
                (обязателен для NEXT_BUTTON).

        --- Параметры Custom ---
            custom_context_generator: Функция, принимающая
                (page_number, предыдущий PageContext) и возвращающая
                новый PageContext для следующей страницы, либо None
                для остановки. Обязательна для CUSTOM.

        --- Параметры задержки ---
            delay_mode: "fixed" или "random".
            delay_fixed_seconds: Фиксированная задержка (сек).
            delay_min_seconds / delay_max_seconds: Диапазон
                случайной задержки.

        Returns:
            List[PageResult]: Список результатов всех страниц.
                Последний элемент содержит stop_reason,
                pages_fetched, elapsed_seconds.

        Raises:
            PaginationError: При некорректных аргументах (например,
                не указан обязательный параметр для выбранной стратегии).
        """
        # --- Нормализация типа пагинации ---
        if isinstance(pagination_type, str):
            pagination_type = PaginationType(pagination_type)

        # --- Валидация аргументов ---
        if pagination_type in (PaginationType.URL, PaginationType.OFFSET, PaginationType.AJAX, PaginationType.CUSTOM):
            if not url:
                raise PaginationError(
                    f"Параметр 'url' обязателен для стратегии '{pagination_type.value}'"
                )
        if pagination_type == PaginationType.NEXT_BUTTON and not next_button_selector:
            raise PaginationError("Параметр 'next_button_selector' обязателен для стратегии 'next_button'")
        if pagination_type == PaginationType.CUSTOM and not custom_context_generator:
            raise PaginationError("Параметр 'custom_context_generator' обязателен для стратегии 'custom'")

        # --- Значения по умолчанию из Configuration Manager ---
        effective_max_pages = max_pages if max_pages is not None else config.PAGINATION_MAX_PAGES
        effective_timeout = timeout_seconds if timeout_seconds is not None else config.PAGINATION_TIMEOUT_SECONDS
        effective_detect_duplicates = (
            detect_duplicates if detect_duplicates is not None else config.PAGINATION_DUPLICATE_DETECTION
        )
        effective_page_param = page_param or config.PAGINATION_PAGE_PARAM
        effective_start_page = start_page if start_page is not None else config.PAGINATION_START_PAGE
        effective_page_step = page_step if page_step is not None else config.PAGINATION_PAGE_STEP
        effective_offset_param = offset_param or config.PAGINATION_OFFSET_PARAM
        effective_start_offset = start_offset if start_offset is not None else config.PAGINATION_START_OFFSET
        effective_offset_step = offset_step if offset_step is not None else config.PAGINATION_OFFSET_STEP

        # --- Задержки ---
        eff_delay_mode = delay_mode if delay_mode is not None else config.PAGINATION_DELAY_MODE
        eff_delay_fixed = delay_fixed_seconds if delay_fixed_seconds is not None else config.PAGINATION_DELAY_FIXED_SECONDS
        eff_delay_min = delay_min_seconds if delay_min_seconds is not None else config.PAGINATION_DELAY_MIN_SECONDS
        eff_delay_max = delay_max_seconds if delay_max_seconds is not None else config.PAGINATION_DELAY_MAX_SECONDS

        # --- Инициализация цикла ---
        results: List[PageResult] = []
        seen_dedupe_keys: set = set()
        start_time = time.monotonic()
        stop_reason: Optional[PaginationStopReason] = None
        current_value = effective_start_page
        current_offset = effective_start_offset

        # --- Первый PageContext ---
        if pagination_type == PaginationType.NEXT_BUTTON:
            context = PageContext(
                url=url or "",
                page_number=1,
                pagination_type=pagination_type,
                use_next_button=True,
            )
        elif pagination_type == PaginationType.CUSTOM:
            context = custom_context_generator(1, None) if custom_context_generator else None
            if context is None:
                return [
                    PageResult(0, None, PaginationStopReason.LAST_PAGE.value, 0, 0.0)
                ]
        elif pagination_type in (PaginationType.URL, PaginationType.AJAX):
            params = cls._build_url_params(url, effective_page_param, current_value, existing_params)
            context = PageContext(url=url, page_number=1, pagination_type=pagination_type, params=params)
        else:  # OFFSET
            params = cls._build_url_params(url, effective_offset_param, current_offset, existing_params)
            context = PageContext(url=url, page_number=1, pagination_type=pagination_type, params=params)

        log_message("info", f"Pagination: начата (тип={pagination_type.value})")

        # --- Цикл ---
        while True:
            # --- Таймаут ---
            elapsed = time.monotonic() - start_time
            if effective_timeout > 0 and elapsed >= effective_timeout:
                stop_reason = PaginationStopReason.ERROR  # timeout как ошибка
                log_message("error", "Pagination: таймаут цикла")
                break

            # --- Выполняем запрос ---
            try:
                fetch_result = fetch_callback(context)
            except Exception as exc:
                log_message("error", f"Pagination: сбой на странице {context.page_number}: {exc}")
                stop_reason = PaginationStopReason.ERROR
                break

            if not isinstance(fetch_result, PageFetchResult):
                log_message("error", "Pagination: fetch_callback должен возвращать PageFetchResult")
                stop_reason = PaginationStopReason.ERROR
                break

            content = fetch_result.content
            item_count = fetch_result.item_count
            has_next = fetch_result.has_next if fetch_result.has_next is not None else True
            dedupe_key = fetch_result.dedupe_key

            page_number = context.page_number

            # --- Сохраняем результат ---
            results.append(PageResult(page_number=page_number, content=content))

            log_message("info", f"Pagination: страница {page_number} загружена")

            # --- Остановка по last_page (has_next == False) ---
            if not has_next:
                stop_reason = PaginationStopReason.LAST_PAGE
                break

            # --- Остановка по no_items ---
            if item_count is not None and item_count == 0:
                stop_reason = PaginationStopReason.NO_ITEMS
                break

            # --- Остановка по max_pages ---
            if effective_max_pages > 0 and page_number >= effective_max_pages:
                stop_reason = PaginationStopReason.MAX_PAGES
                break

            # --- Остановка по duplicate ---
            if effective_detect_duplicates and dedupe_key is not None:
                if dedupe_key in seen_dedupe_keys:
                    stop_reason = PaginationStopReason.DUPLICATE_PAGE
                    break
                seen_dedupe_keys.add(dedupe_key)

            # --- Остановка по custom_callback ---
            if stop_callback is not None:
                try:
                    should_stop = stop_callback(page_number, content)
                except Exception as exc:
                    log_message("error", f"Pagination: ошибка в stop_callback: {exc}")
                    stop_reason = PaginationStopReason.ERROR
                    break
                if should_stop:
                    stop_reason = PaginationStopReason.CUSTOM_CALLBACK
                    break

            # --- Пауза перед следующей страницей ---
            if eff_delay_mode == "fixed":
                DelayManager.wait_fixed(eff_delay_fixed)
            else:
                DelayManager.wait_random(eff_delay_min, eff_delay_max)

            # --- Генерируем контекст следующей страницы ---
            next_page_number = page_number + 1

            if pagination_type == PaginationType.NEXT_BUTTON:
                context = PageContext(
                    url=url or "",
                    page_number=next_page_number,
                    pagination_type=pagination_type,
                    use_next_button=True,
                )
            elif pagination_type == PaginationType.CUSTOM:
                if custom_context_generator is not None:
                    context = custom_context_generator(next_page_number, context)
                    if context is None:
                        stop_reason = PaginationStopReason.LAST_PAGE
                        break
                else:
                    stop_reason = PaginationStopReason.LAST_PAGE
                    break
            elif pagination_type in (PaginationType.URL, PaginationType.AJAX):
                current_value += effective_page_step
                params = cls._build_url_params(url, effective_page_param, current_value, existing_params)
                context = PageContext(url=url, page_number=next_page_number, pagination_type=pagination_type, params=params)
            else:  # OFFSET
                current_offset += effective_offset_step
                params = cls._build_url_params(url, effective_offset_param, current_offset, existing_params)
                context = PageContext(url=url, page_number=next_page_number, pagination_type=pagination_type, params=params)

        # --- Завершение ---
        elapsed_total = time.monotonic() - start_time
        stop_reason_str = stop_reason.value if stop_reason else PaginationStopReason.LAST_PAGE.value
        log_message(
            "info",
            f"Pagination: завершено (страниц={len(results)}, "
            f"причина={stop_reason_str}, время={elapsed_total:.1f}с)",
        )

        # Добавляем мета-информацию в последний элемент
        if results:
            results[-1].stop_reason = stop_reason_str
            results[-1].pages_fetched = len(results)
            results[-1].elapsed_seconds = elapsed_total

        return results


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.requests_engine import RequestsEngine

    engine = RequestsEngine()

    def mock_fetch(ctx: PageContext) -> PageFetchResult:
        resp = engine.get(ctx.url, params=ctx.params)
        return PageFetchResult(content=resp.text, dedupe_key=resp.url)

    results = Paginator.paginate(
        mock_fetch,
        PaginationType.URL,
        url="https://httpbin.org/get",
        max_pages=3,
        page_param="page",
        start_page=1,
        page_step=1,
    )
    print(f"Загружено страниц: {len(results)}")
    if results:
        last = results[-1]
        print(f"Причина остановки: {last.stop_reason}")

--- app/parser.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Парсер товаров с сайта professionele-koeling.nl.

Модуль отвечает за извлечение структурированных данных из HTML-кода:
1. Извлечение ссылок на товары из HTML категории (parse_listing)
2. Парсинг отдельных страниц товаров (parse_product)
3. Разворачивание характеристик (Extra informatie) в отдельные колонки
4. Нормализация цен, текста, URL через централизованные утилиты

Сигнатура parse_html_data(html_contents) сохраняется для совместимости
с main.py, который передаёт список сырых HTML-строк.
"""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.html_parser import HtmlParser
from app.data_normalizer import DataNormalizer
from app.utils import log_message, clean_price


def parse_listing(html: str) -> List[str]:
    """
    Извлекает URL первых двух товаров из HTML-кода страницы категории.

    Args:
        html: Строка сырого HTML-кода страницы категории.

    Returns:
        List[str]: Список URL первых двух товаров.
                   Возвращает пустой список, если товары не найдены.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        log_message("error", f"[{__file__}] parse_listing: невалидный HTML")
        return []

    # Найти все карточки товаров
    cards = HtmlParser.find_all(soup, "li", class_="item")
    
    if not cards:
        log_message("warning", f"[{__file__}] parse_listing: карточки товаров не найдены")
        return []

    log_message("info", f"[{__file__}] parse_listing: найдено карточек: {len(cards)}")

    product_urls = []
    for card in cards[:2]:  # Берём только первые два товара
        link = HtmlParser.find(card, "a", class_="product-image")
        if link:
            href = HtmlParser.get_attr(link, "href")
            if href:
                product_urls.append(href)

    log_message("info", f"[{__file__}] parse_listing: извлечено URL: {len(product_urls)}")
    return product_urls


def parse_specs(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Извлекает характеристики товара из таблицы Extra informatie.

    Args:
        soup: BeautifulSoup объект HTML-кода страницы товара.

    Returns:
        Dict[str, Any]: Словарь с характеристиками {название: значение}.
    """
    specs = {}

    # Найти таблицу характеристик
    specs_table = HtmlParser.find(soup, "table", id="product-attribute-specs-table")
    if not specs_table:
        log_message("warning", f"[{__file__}] parse_specs: таблица характеристик не найдена")
        return specs

    # Извлечь все строки таблицы
    rows = HtmlParser.find_all(specs_table, "tr")
    for row in rows:
        th = HtmlParser.find(row, "th", class_="label")
        td = HtmlParser.find(row, "td", class_="data")
        
        if th and td:
            key = HtmlParser.get_text(th, default="").strip()
            value = HtmlParser.get_text(td, default="").strip()
            if key and value:
                specs[key] = value

    log_message("debug", f"[{__file__}] parse_specs: извлечено характеристик: {len(specs)}")
    return specs


def parse_product(html: str, url: str) -> Dict[str, Any]:
    """
    Извлекает все данные из HTML-кода страницы товара.

    Args:
        html: Строка сырого HTML-кода страницы товара.
        url: URL страницы товара.

    Returns:
        Dict[str, Any]: Словарь с данными товара.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        log_message("error", f"[{__file__}] parse_product: невалидный HTML для {url}")
        return {}

    result = {"URL": url}

    # 1. Breadcrumb (хлебные крошки)
    breadcrumb_items = []
    breadcrumb = HtmlParser.find(soup, "div", class_="breadcrumbs")
    if breadcrumb:
        links = HtmlParser.find_all(breadcrumb, "a")
        for link in links:
            text = HtmlParser.get_text(link, default="").strip()
            if text:
                breadcrumb_items.append(text)
        # Добавляем последний элемент (текущая страница) если есть
        last_crumb = HtmlParser.find(breadcrumb, "span", class_="last-crumb")
        if last_crumb:
            breadcrumb_items.append(HtmlParser.get_text(last_crumb, default="").strip())
    
    result["Breadcrumb"] = " > ".join(breadcrumb_items) if breadcrumb_items else ""

    # 2. Title (заголовок)
    title_elem = HtmlParser.find(soup, "h1", itemprop="name")
    result["Title"] = HtmlParser.get_text(title_elem, default="").strip()

    # 3. Short description (краткое описание)
    short_desc = HtmlParser.find(soup, "div", class_="short-description")
    if short_desc:
        desc_elem = HtmlParser.find(short_desc, "div", class_="std")
        result["Short description"] = HtmlParser.get_text(desc_elem, default="").strip()
    else:
        result["Short description"] = ""

    # 4. Image URL (изображение)
    # Ищем оригинальное изображение через zoom-inside или cloud-zoom
    img_url = ""
    image_container = HtmlParser.find(soup, "p", class_="product-image")
    if image_container:
        zoom_link = HtmlParser.find(image_container, "a", class_="cloud-zoom")
        if zoom_link:
            img_url = HtmlParser.get_attr(zoom_link, "href")
    
    if not img_url:
        # Fallback: ищем любую картинку в product-image
        img_elem = HtmlParser.find(soup, "img", class_="gallery-image")
        if img_elem:
            img_url = HtmlParser.get_attr(img_elem, "src")
    
    result["imageurl"] = img_url or ""

    # 5. Image name (имя файла)
    if img_url:
        result["image_name"] = img_url.split("/")[-1] if "/" in img_url else ""
    else:
        result["image_name"] = ""

    # 6. Price (старая цена) и Sale price (скидочная цена)
    price_box = HtmlParser.find(soup, "div", class_="price-box")
    result["Price"] = None
    result["Sale price"] = None

    if price_box:
        # Обычная цена
        old_price_elem = HtmlParser.find(price_box, "span", class_="old-price")
        if old_price_elem:
            price_span = HtmlParser.find(old_price_elem, "span", class_="price")
            if price_span:
                price_text = HtmlParser.get_text(price_span, default="").strip()
                if price_text:
                    cleaned = DataNormalizer.normalize_price(price_text)
                    result["Price"] = cleaned if cleaned is not None else price_text

        # Скидочная цена
        special_price_elem = HtmlParser.find(price_box, "span", class_="special-price")
        if special_price_elem:
            price_span = HtmlParser.find(special_price_elem, "span", class_="price")
            if price_span:
                price_text = HtmlParser.get_text(price_span, default="").strip()
                if price_text:
                    cleaned = DataNormalizer.normalize_price(price_text)
                    result["Sale price"] = cleaned if cleaned is not None else price_text

    # 7. Description (полное описание из вкладки Productbeschrijving)
    description = ""
    description_panel = HtmlParser.find(soup, "div", id="product-tabs")
    if description_panel:
        # Ищем панель с описанием (скрыта по умолчанию, но HTML присутствует)
        panels = HtmlParser.find_all(description_panel, "div", class_="panel")
        for panel in panels:
            # Проверяем, что это панель описания (может содержать заголовок h2)
            if panel.get("style") == "display: block;" or panel.find("h2"):
                desc_elem = HtmlParser.find(panel, "div", class_="std")
                if desc_elem:
                    description = HtmlParser.get_text(desc_elem, default="").strip()
                    break
    
    if not description:
        # Fallback: ищем любой блок с описанием
        desc_block = HtmlParser.find(soup, "div", class_="product-description")
        if desc_block:
            description = HtmlParser.get_text(desc_block, default="").strip()
    
    result["Description"] = description

    # 8. Specs (характеристики) - разворачиваем в отдельные поля
    specs = parse_specs(soup)
    
    # Добавляем все характеристики в результат
    for key, value in specs.items():
        result[key] = value

    # 9. Дополнительно: извлекаем наличие (availability) из страницы
    availability_elem = HtmlParser.find(soup, "p", class_="availability")
    if availability_elem:
        availability_text = HtmlParser.get_text(availability_elem, default="").strip()
        result["Availability"] = availability_text
    else:
        result["Availability"] = ""

    return result


def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Точка интеграции с главным оркестратором main.py.
    Принимает список сырых HTML-строк, извлекает URL товаров из первой страницы
    и парсит все переданные страницы товаров.

    Args:
        html_contents: Список строк сырого HTML-кода.
                      Ожидается, что первый элемент — HTML категории,
                      остальные — HTML страниц товаров.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными товаров.
    """
    if not html_contents:
        log_message("warning", f"[{__file__}] parse_html_data: список HTML пуст")
        return []

    log_message("info", f"[{__file__}] parse_html_data: обработка {len(html_contents)} HTML-строк")

    # Первая строка — HTML категории, извлекаем URL товаров
    category_html = html_contents[0]
    product_urls = parse_listing(category_html)
    
    if not product_urls:
        log_message("error", f"[{__file__}] parse_html_data: не удалось извлечь URL товаров")
        return []

    log_message("info", f"[{__file__}] parse_html_data: найдено URL товаров: {len(product_urls)}")

    results = []
    # Остальные HTML-строки — страницы товаров (может быть 1 или 2)
    # Используем их последовательно для парсинга каждого товара
    for idx, html in enumerate(html_contents[1:], 0):
        if idx >= len(product_urls):
            break
        
        try:
            url = product_urls[idx]
            product_data = parse_product(html, url)
            if product_data:
                results.append(product_data)
                log_message("debug", f"[{__file__}] parse_html_data: успешно спарсен товар #{idx+1}: {product_data.get('Title', 'N/A')}")
        except Exception as e:
            log_message("error", f"[{__file__}] parse_html_data: ошибка парсинга товара #{idx+1}: {e}")

    log_message("info", f"[{__file__}] parse_html_data: завершено, получено товаров: {len(results)}")
    return results


# Алиас для совместимости с другими частями кода
# (parse_html_data уже используется в main.py)

--- app/playwright_engine.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Playwright Engine.

Централизованный слой браузерной автоматизации фреймворка для всех
JavaScript-зависимых сайтов (см. `framework/ROADMAP.md`, Milestone 4).

Playwright Engine — единственная точка, через которую скрапер-модули
должны запускать браузер, открывать страницы и получать их содержимое.
Он НЕ содержит собственной логики куки/прокси/задержек/идентичности —
вся эта логика уже инкапсулирована в существующих менеджерах и
применяется автоматически, аналогично тому, как Requests Engine
использует Session Manager для HTTP-запросов:

    Playwright Engine
            │
            ▼
    app/browser.py (get_browser_context)  ──────────────────┐
            │                                                │
     ┌──────┼─────────┬─────────┬─────────┐                  │
     ▼      ▼          ▼         ▼         ▼                 ▼
    Request Cookie    Proxy    Delay   Configuration     (Retry остаётся
    Profile Manager   Manager  Manager Manager           централизованным,
    Manager                                               см. ниже)

Playwright Engine:

* делегирует запуск браузера и создание контекста функции
  `app.browser.get_browser_context()` — единственному месту, где
  реально вызывается `playwright.chromium.launch()` / `browser.new_context()`,
  чтобы не дублировать эту логику (см. `app/browser.py`);
* автоматически применяет идентичность клиента через Request Profile
  Manager (`app/request_profile.py`), куки — через Cookie Manager
  (`app/cookie_manager.py`), прокси — через Proxy Manager
  (`app/proxy_manager.py`) — вызывающий код ничего не настраивает вручную;
* делает паузу перед каждой навигацией через `SessionManager.wait_before_request()`
  (Delay Manager) — как и Requests Engine, не реализует собственную политику пауз;
* сообщает Proxy Manager об успехе/сбое каждой навигации
  (`ProxyManager.report_proxy_success()`/`report_proxy_failure()`), что
  прозрачно питает Proxy Health Check/Rotation/Sticky Sessions, если
  движку передан `session_id` — идентично Requests Engine;
* НЕ реализует собственный цикл повторов при навигации — как и Requests
  Engine, Playwright Engine оставляет retry-политику централизованной
  (вызывающий код может обернуть `goto()` в `RetryManager.call_with_retry()`
  при необходимости — сам движок только сообщает об исходе через Proxy Manager);
* оборачивает все ожидаемые сбои Playwright (таймаут, навигация, отсутствие
  селектора, ошибка запуска браузера, падение страницы) в единое понятное
  исключение `PlaywrightEngineError` — вызывающему коду не нужно знать о
  внутренних исключениях Playwright;
* использует централизованную функцию логирования `app.utils.log_message`
  для запуска/закрытия браузера, навигации и ошибок (без избыточного лога).

Playwright Engine НЕ парсит HTML (это Milestone 5 — Parsing), НЕ
экспортирует данные, НЕ содержит селекторов конкретных сайтов, НЕ
реализует пагинацию/infinite scroll/логин — эти возможности будут
реализованы отдельными задачами (см. `tasks/TASK.md`, раздел Scope) на
основе этого движка.
"""

from pathlib import Path
from typing import Any, List, Optional

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from app import config
from app.browser import get_browser_context
from app.cookie_manager import CookieManager
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile, RequestProfileManager
from app.session_manager import SessionManager
from app.utils import log_message


class PlaywrightEngineError(Exception):
    """
    Единое исключение Playwright Engine для всех сбоев браузерной
    автоматизации (запуск браузера, навигация, таймаут, отсутствие
    селектора, выполнение JS), оставшихся после обработки движком.

    Позволяет вызывающему коду (будущим скрапер-модулям) обрабатывать
    ошибки браузера без необходимости импортировать и знать про
    исключения `playwright.sync_api`.
    """


class PlaywrightEngine:
    """
    Централизованный исполнитель браузерной автоматизации для JS-сайтов.

    Каждый инстанс управляет одним запущенным Playwright-драйвером, одним
    браузером и одним изолированным `BrowserContext`. Все компоненты слоя
    автоматизации (Configuration/Request Profile/Cookie/Proxy/Delay Manager)
    подключаются автоматически — вызывающий код не настраивает их вручную.

    Используется как контекстный менеджер (рекомендуемый способ):

        with PlaywrightEngine() as engine:
            engine.goto("https://example.com")
            html = engine.content()

    либо через явные `start()`/`close()`.
    """

    def __init__(
        self,
        profile: Optional[RequestProfile] = None,
        session_id: Optional[str] = None,
        cookies_path: Optional[Path] = None,
        headless: Optional[bool] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Args:
            profile (RequestProfile, optional): Профиль идентичности клиента
                (User-Agent, locale, timezone, viewport, Accept-Language).
                По умолчанию — `RequestProfileManager.default_profile()`.
            session_id (str, optional): Идентификатор логической сессии для
                Sticky Sessions/Proxy Rotation/Health Check
                (см. `ProxyManager.get_proxy(session_id=...)`). Если не
                передан — прокси выбирается без привязки к сессии.
            cookies_path (Path, optional): Путь к файлу куки (Cookie Manager).
                По умолчанию — `config.COOKIES_FILE`.
            headless (bool, optional): Режим headless. По умолчанию — `config.HEADLESS`.
            user_agent (str, optional): Явный User-Agent, переопределяющий профиль.
        """
        self.profile = profile
        self.session_id = session_id
        self.cookies_path = cookies_path or config.COOKIES_FILE
        self.headless = headless
        self.user_agent = user_agent

        self._playwright = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    # =====================================================================
    # ЖИЗНЕННЫЙ ЦИКЛ БРАУЗЕРА
    # =====================================================================

    def start(self) -> "PlaywrightEngine":
        """
        Запускает драйвер Playwright, браузер Chromium и создает изолированный
        контекст с автоматически примененными идентичностью/куки/прокси.

        Returns:
            PlaywrightEngine: self (для удобного чейнинга).

        Raises:
            PlaywrightEngineError: При сбое запуска браузера.
        """
        proxy_url = ProxyManager.get_proxy(session_id=self.session_id)
        proxy_kwargs = ProxyManager.to_playwright_proxy_kwargs(proxy_url) if proxy_url else None

        try:
            self._playwright = sync_playwright().start()
            self._context = get_browser_context(
                self._playwright,
                headless=self.headless,
                user_agent=self.user_agent,
                cookies_path=self.cookies_path,
                profile=self.profile,
                proxy=proxy_kwargs,
            )
        except Exception as exc:
            self._teardown_playwright()
            log_message("error", f"Не удалось запустить браузер: {exc}")
            raise PlaywrightEngineError(f"Ошибка запуска браузера: {exc}") from exc

        self._context.set_default_timeout(config.PLAYWRIGHT_TIMEOUT_MS)
        log_message("info", f"Браузер запущен (headless={self.headless if self.headless is not None else config.HEADLESS})")
        return self

    def close(self) -> None:
        """
        Сохраняет актуальные куки сессии и закрывает браузер/драйвер Playwright.

        Безопасна к повторному вызову и к вызову без предварительного `start()`.
        """
        if self._context is not None:
            try:
                self.save_cookies()
            except Exception as exc:
                log_message("error", f"Не удалось сохранить куки при закрытии: {exc}")

            try:
                browser: Optional[Browser] = self._context.browser
                self._context.close()
                if browser is not None:
                    browser.close()
            except Exception as exc:
                log_message("error", f"Ошибка при закрытии браузера: {exc}")
            finally:
                self._context = None
                self._page = None

        self._teardown_playwright()
        log_message("info", "Браузер закрыт")

    def _teardown_playwright(self) -> None:
        """Останавливает драйвер Playwright, если он был запущен."""
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
            finally:
                self._playwright = None

    def __enter__(self) -> "PlaywrightEngine":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # =====================================================================
    # СТРАНИЦЫ И НАВИГАЦИЯ
    # =====================================================================

    @property
    def context(self) -> BrowserContext:
        """Возвращает активный `BrowserContext` (после `start()`)."""
        if self._context is None:
            raise PlaywrightEngineError("Контекст браузера не инициализирован — вызовите start() перед использованием.")
        return self._context

    @property
    def page(self) -> Page:
        """Возвращает текущую страницу, создавая её при первом обращении."""
        if self._page is None:
            self._page = self.new_page()
        return self._page

    def new_page(self) -> Page:
        """
        Создает новую страницу в текущем контексте и делает её активной.

        Returns:
            Page: Новая страница Playwright.
        """
        try:
            self._page = self.context.new_page()
        except Exception as exc:
            raise PlaywrightEngineError(f"Не удалось создать страницу: {exc}") from exc
        return self._page

    def goto(
        self,
        url: str,
        wait_until: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Открывает URL на текущей странице.

        Перед навигацией выполняется пауза согласно Delay Manager
        (`SessionManager.wait_before_request()`) — как и в Requests Engine.
        После навигации сообщает Proxy Manager об успехе/сбое.

        Args:
            url (str): Целевой URL.
            wait_until (str, optional): Условие завершения навигации
                ("load", "domcontentloaded", "networkidle", "commit").
                По умолчанию — `config.PLAYWRIGHT_WAIT_UNTIL`.
            timeout (float, optional): Таймаут навигации (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            Response Playwright (или None, если навигация не создала документ).

        Raises:
            PlaywrightEngineError: При таймауте или сбое навигации.
        """
        effective_wait_until = wait_until or config.PLAYWRIGHT_WAIT_UNTIL
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS

        SessionManager.wait_before_request()

        log_message("info", f"Навигация: {url}")
        try:
            response = self.page.goto(
                url,
                wait_until=effective_wait_until,
                timeout=effective_timeout,
            )
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Таймаут навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Таймаут при открытии {url}: {exc}") from exc
        except PlaywrightError as exc:
            log_message("error", f"Сбой навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Не удалось открыть {url}: {exc}") from exc

        ProxyManager.report_proxy_success(session_id=self.session_id)
        self.update_cookies()
        return response

    def wait_for_load(self, state: str = "load", timeout: Optional[float] = None) -> None:
        """
        Ожидает завершения загрузки страницы.

        Args:
            state (str): Состояние загрузки ("load", "domcontentloaded", "networkidle").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Raises:
            PlaywrightEngineError: При таймауте ожидания.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            self.page.wait_for_load_state(state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            raise PlaywrightEngineError(f"Таймаут ожидания состояния загрузки '{state}': {exc}") from exc

    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Ожидает появления селектора на странице.

        Args:
            selector (str): CSS/text-селектор Playwright.
            state (str): Ожидаемое состояние элемента
                ("attached", "detached", "visible", "hidden").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            ElementHandle: Найденный элемент.

        Raises:
            PlaywrightEngineError: Если селектор не появился до истечения таймаута.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            return self.page.wait_for_selector(selector, state=state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Селектор не найден: {selector}")
            raise PlaywrightEngineError(f"Селектор '{selector}' не появился: {exc}") from exc

    def content(self) -> str:
        """
        Возвращает полный HTML текущей страницы (без какого-либо парсинга).

        Returns:
            str: Сырой HTML страницы.

        Raises:
            PlaywrightEngineError: При сбое получения содержимого (например,
                падении страницы).
        """
        try:
            return self.page.content()
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось получить содержимое страницы: {exc}") from exc

    def evaluate(self, script: str, *args: Any) -> Any:
        """
        Выполняет JavaScript в контексте текущей страницы.

        Args:
            script (str): JS-выражение или функция (`page.evaluate()`).
            *args: Аргументы, передаваемые в скрипт.

        Returns:
            Any: Результат выполнения скрипта.

        Raises:
            PlaywrightEngineError: При сбое выполнения скрипта.
        """
        try:
            return self.page.evaluate(script, *args)
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось выполнить JavaScript: {exc}") from exc

    # =====================================================================
    # ИНТЕГРАЦИЯ С COOKIE MANAGER
    # =====================================================================

    def update_cookies(self) -> List[dict]:
        """
        Забирает текущие куки контекста браузера и обновляет ими персистентное
        хранилище через Cookie Manager (`CookieManager.update()`), не
        затирая куки, установленные вне текущей сессии.

        Returns:
            List[dict]: Итоговый объединенный список куки.
        """
        current_cookies = self.context.cookies()
        return CookieManager.update(current_cookies, path=self.cookies_path)

    def save_cookies(self) -> None:
        """
        Полностью перезаписывает файл куки текущим состоянием контекста
        браузера (`CookieManager.save()`).
        """
        current_cookies = self.context.cookies()
        CookieManager.save(current_cookies, path=self.cookies_path)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    with PlaywrightEngine(headless=False) as engine:
        engine.goto("https://bot.sannysoft.com/")
        engine.wait_for_load("networkidle")
        print(f"[{__file__}] Длина HTML: {len(engine.content())}")


--- app/proxy_cache.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Cache.

Централизованный, provider-независимый кэш списка прокси, снижающий
количество ненужных обращений к провайдерам (Webshare API, File Provider
и т.д.) за счет хранения последнего успешно загруженного списка прокси в
локальном JSON-файле.

Состоит из двух частей:

* `ProxyCache` — низкоуровневое файловое хранилище. Не знает о
  провайдерах, ProxyManager или формате прокси-URL — просто
  читает/пишет список строк + timestamp в JSON-файл и умеет проверять,
  истек ли TTL. Может быть заменен другим механизмом хранения (Redis,
  БД) в будущем без изменения остального кода — этим и обусловлено
  выделение его в отдельный класс (см. TASK.md, "Storage").

* `CachedProxyProvider` — прозрачная обертка (декоратор) вокруг ЛЮБОГО
  существующего `ProxyProvider` (Webshare, File, будущий BrightData).
  Сама реализует интерфейс `ProxyProvider`, поэтому Proxy Manager
  продолжает работать без единого изменения — просто оборачиваем
  провайдер при регистрации:

      ProxyManager.set_provider(CachedProxyProvider(WebshareProxyProvider()))

  `CachedProxyProvider` не содержит provider-specific логики — он вызывает
  `wrapped_provider.get_proxy()` только тогда, когда файловый кэш пуст
  или истек, и сохраняет результат обратно в кэш. Если провайдер
  недоступен (сеть, невалидный ключ и т.д.), но в кэше есть валидные
  (даже просроченные) данные — используются они, чтобы не терять список
  прокси из-за временного сбоя провайдера.

Proxy Cache НЕ ротирует, НЕ валидирует и НЕ выбирает прокси, НЕ проверяет
их здоровье — вся эта логика вне его ответственности (Proxy Rotation /
Health Check / Proxy Selection, см. `framework/ROADMAP.md`).
"""

import json
import time
from pathlib import Path
from typing import List, Optional

from app import config
from app.proxy_manager import ProxyProvider


class ProxyCache:
    """
    Файловое хранилище последнего успешно загруженного списка прокси.

    Формат файла — простой JSON:
        {"proxies": ["http://...", "http://..."], "cached_at": 1719999999.123}

    `ProxyCache` не знает, откуда взялись прокси (Webshare, File Provider
    и т.д.) — он просто хранит список строк и время последнего сохранения.
    """

    def __init__(self, path: Path = None, ttl_seconds: int = None):
        """
        Args:
            path (Path, optional): Путь к файлу кэша. По умолчанию —
                `config.PROXY_CACHE_FILE`.
            ttl_seconds (int, optional): Время жизни кэша в секундах.
                По умолчанию — `config.PROXY_CACHE_TTL_SECONDS`.
        """
        self.path = path or config.PROXY_CACHE_FILE
        self.ttl_seconds = ttl_seconds if ttl_seconds is not None else config.PROXY_CACHE_TTL_SECONDS

    def load(self) -> Optional[dict]:
        """
        Читает содержимое файла кэша.

        Обрабатывает отсутствующий, пустой и поврежденный (невалидный JSON)
        файл без падения приложения.

        Returns:
            Optional[dict]: Словарь `{"proxies": [...], "cached_at": float}`,
                либо `None`, если файл отсутствует, пуст или поврежден.
        """
        if not self.path.exists():
            return None

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[{__file__}] Ошибка чтения файла кэша прокси {self.path.name}: {e}")
            return None

        if not raw.strip():
            return None

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[{__file__}] Предупреждение: кэш прокси поврежден "
                  f"({self.path.name}): {e}. Кэш будет перезаписан при следующем обновлении.")
            return None

        if not isinstance(data, dict) or "proxies" not in data or "cached_at" not in data:
            print(f"[{__file__}] Предупреждение: неожиданный формат файла кэша прокси "
                  f"{self.path.name}. Кэш будет перезаписан при следующем обновлении.")
            return None

        return data

    def get_proxies(self) -> List[str]:
        """
        Возвращает список прокси из кэша независимо от того, истек ли TTL.

        Returns:
            List[str]: Список закэшированных прокси (пустой, если кэша нет).
        """
        data = self.load()
        if not data:
            return []
        return list(data.get("proxies") or [])

    def is_expired(self) -> bool:
        """
        Проверяет, истек ли TTL кэша (или кэш вовсе отсутствует/поврежден/пуст).

        Returns:
            bool: `True`, если кэш нужно обновить через провайдер.
        """
        data = self.load()
        if not data or not data.get("proxies"):
            return True
        cached_at = data.get("cached_at", 0)
        return (time.time() - cached_at) >= self.ttl_seconds

    def save(self, proxies: List[str]) -> None:
        """
        Сохраняет список прокси в файл кэша с текущей временной меткой.

        Пустой список НЕ сохраняется — это защищает уже закэшированные
        валидные данные от затирания при временном сбое провайдера
        (см. `CachedProxyProvider.get_proxy()`).

        Args:
            proxies (List[str]): Список нормализованных URL прокси.
        """
        if not proxies:
            return

        payload = {"proxies": proxies, "cached_at": time.time()}
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError as e:
            print(f"[{__file__}] Ошибка записи файла кэша прокси {self.path.name}: {e}")

    def clear(self) -> None:
        """Удаляет файл кэша, если он существует."""
        if self.path.exists():
            try:
                self.path.unlink()
                print(f"[{__file__}] Кэш прокси очищен: {self.path.name}")
            except OSError as e:
                print(f"[{__file__}] Ошибка удаления файла кэша прокси {self.path.name}: {e}")


class CachedProxyProvider(ProxyProvider):
    """
    Прозрачная обертка над любым `ProxyProvider`, добавляющая персистентный
    файловый кэш (см. `ProxyCache`).

    Использование (без изменения Proxy Manager):

        from app.proxy_manager import ProxyManager
        from app.webshare_proxy_provider import WebshareProxyProvider
        from app.proxy_cache import CachedProxyProvider

        ProxyManager.set_provider(CachedProxyProvider(WebshareProxyProvider()))

    Proxy Manager продолжает вызывать только `get_proxy()` — он не знает
    и не должен знать, что результат кэшируется.
    """

    def __init__(self, provider: ProxyProvider, cache: ProxyCache = None):
        """
        Args:
            provider (ProxyProvider): Оборачиваемый провайдер (Webshare,
                File или любой другой, реализующий `ProxyProvider`).
            cache (ProxyCache, optional): Экземпляр файлового кэша.
                По умолчанию создается новый `ProxyCache()` с настройками
                из Configuration Manager.
        """
        self.provider = provider
        self.cache = cache or ProxyCache()
        self._proxies: List[str] = []

    def _refresh_from_provider(self) -> List[str]:
        """
        Запрашивает актуальный список прокси у оборачиваемого провайдера
        и сохраняет его в файловый кэш.

        Если провайдер поддерживает `get_all_proxies()` (как
        `FileProxyProvider`/`WebshareProxyProvider`), используется он —
        это позволяет закэшировать весь список, а не только один прокси.
        Иначе используется единственный результат `get_proxy()`.

        Returns:
            List[str]: Свежий список прокси от провайдера (может быть
                пустым, если провайдер недоступен).
        """
        get_all = getattr(self.provider, "get_all_proxies", None)
        if callable(get_all):
            proxies = get_all()
        else:
            proxy = self.provider.get_proxy()
            proxies = [proxy] if proxy else []

        if proxies:
            self.cache.save(proxies)

        return proxies

    def _ensure_loaded(self) -> None:
        """
        Гарантирует, что `self._proxies` заполнен: сначала пробует кэш
        (если не истек), иначе запрашивает провайдер. Если провайдер
        недоступен, но в кэше есть хоть просроченные данные — используются
        они (graceful degradation, см. TASK.md "Error Handling").
        """
        if self._proxies:
            return

        if not self.cache.is_expired():
            self._proxies = self.cache.get_proxies()
            if self._proxies:
                return

        fresh = self._refresh_from_provider()
        if fresh:
            self._proxies = fresh
            return

        # Провайдер недоступен/вернул пусто — используем то, что есть в
        # кэше, даже если оно просрочено, лучше устаревшие прокси, чем ничего.
        stale = self.cache.get_proxies()
        if stale:
            print(f"[{__file__}] Провайдер недоступен — используются устаревшие "
                  f"данные из кэша прокси ({len(stale)} шт.).")
        self._proxies = stale

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый доступный прокси (из кэша либо от провайдера).

        Returns:
            Optional[str]: URL прокси, либо `None`, если ни кэш, ни
                провайдер не смогли предоставить ни одного прокси.
        """
        self._ensure_loaded()
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный список прокси (из кэша либо от провайдера).

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        self._ensure_loaded()
        return list(self._proxies)

    def refresh(self) -> List[str]:
        """
        Принудительно обновляет кэш через оборачиваемый провайдер,
        игнорируя текущий TTL.

        Returns:
            List[str]: Обновленный список прокси (может быть пустым,
                если провайдер недоступен и кэш также пуст).
        """
        fresh = self._refresh_from_provider()
        self._proxies = fresh or self.cache.get_proxies()
        return list(self._proxies)

    def clear_cache(self) -> None:
        """Полностью очищает файловый кэш и внутреннее состояние обертки."""
        self.cache.clear()
        self._proxies = []


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.file_proxy_provider import FileProxyProvider
    from app.proxy_manager import ProxyManager

    cached = CachedProxyProvider(FileProxyProvider())
    print(f"[{__file__}] Файл кэша: {cached.cache.path}")
    print(f"[{__file__}] Кэш истек: {cached.cache.is_expired()}")
    print(f"[{__file__}] get_all_proxies(): {cached.get_all_proxies()}")
    print(f"[{__file__}] get_proxy(): {cached.get_proxy()}")

    # Интеграция с Proxy Manager без изменения его кода.
    ProxyManager.set_provider(cached)
    print(f"[{__file__}] ProxyManager.get_proxy(): {ProxyManager.get_proxy()}")


--- app/proxy_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Manager.

Единый компонент, отвечающий за предоставление прокси для HTTP-запросов
(`requests.Session`) и, в будущем, для браузерной автоматизации (Playwright,
см. Milestone 4 — Browser Manager).

Proxy Manager:

* НЕ скачивает, НЕ валидирует, НЕ ротирует и НЕ проверяет здоровье прокси —
  это ответственность будущих компонентов (Proxy Providers, Rotation,
  Health Check, см. `framework/ROADMAP.md`, Milestone 3), которые будут
  реализованы отдельными задачами;
* абстрагирует источник прокси через простой интерфейс `ProxyProvider`,
  поэтому смена провайдера (Webshare, BrightData, Oxylabs, SmartProxy,
  File Provider и т.д.) НЕ требует изменения публичного API Proxy Manager —
  достаточно зарегистрировать новый провайдер через `ProxyManager.set_provider()`;
* если провайдер предоставляет пул прокси (`get_all_proxies()`), выбор
  одного прокси из пула делегируется отдельному компоненту Proxy Selection
  (`app/proxy_selector.py`, `ProxySelector.select()`) — Proxy Manager не
  содержит и не должен содержать логики выбора (round robin/random/и т.д.),
  это ответственность Proxy Selection;
* момент, когда нужно выбрать новый прокси вместо повторного использования
  текущего, определяется отдельным компонентом Proxy Rotation
  (`app/proxy_rotation.py`, `ProxyRotation.should_rotate()`) — Proxy
  Manager хранит только текущий выбранный прокси (`_current_proxy`) и не
  содержит и не должен содержать логики принятия решения "когда менять";


* по умолчанию использует `EnvProxyProvider` — адаптер к единственному
  источнику прокси, существовавшему до этой задачи (`config.PROXY_URL`),
  сохраняя обратную совместимость;
* предоставляет прокси в формате, готовом для `requests.Session`
  (`ProxyManager.apply_to_session()`), и — на будущее — для контекста
  Playwright (`ProxyManager.to_playwright_proxy_kwargs()`).

Proxy Manager НЕ выполняет HTTP-запросы и НЕ содержит логики скрапинга.
Как и Cookie/Retry/Delay Manager, он зависит только от Configuration
Manager и НЕ вызывает и ничего не знает о других менеджерах напрямую —
это сохраняет слабую связанность компонентов вокруг Session Manager
(см. `app/session_manager.py`).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from app import config


class ProxyProvider(ABC):
    """
    Абстрактный источник прокси.

    Любой провайдер (Webshare, BrightData, File Provider и т.д.) должен
    реализовать этот интерфейс. Proxy Manager работает только через него
    и никогда не содержит специфичной для конкретного провайдера логики.
    """

    @abstractmethod
    def get_proxy(self) -> Optional[str]:
        """
        Возвращает URL прокси в формате
        `http://[username:password@]host:port`, либо `None`, если прокси
        не настроен/недоступен.
        """
        raise NotImplementedError


class EnvProxyProvider(ProxyProvider):
    """
    Провайдер по умолчанию — берет единственный прокси из переменной
    окружения `PROXY_URL` (Configuration Manager, `app/config.py`).

    Это не полноценный провайдер вроде Webshare/BrightData, а простой
    адаптер к уже существовавшей настройке `config.PROXY_URL`,
    обеспечивающий обратную совместимость до появления настоящих
    провайдеров (см. рекомендации в конце файла / TASK.md deliverable 5).
    """

    def get_proxy(self) -> Optional[str]:
        return config.PROXY_URL


class ProxyManager:
    """
    Централизованная точка доступа к прокси для всего фреймворка.

    Работает с текущим провайдером (`ProxyProvider`), не зная о его
    внутренней реализации. Провайдер можно заменить в рантайме через
    `set_provider()` — например, на будущий `WebshareProxyProvider` —
    без изменения кода, использующего `ProxyManager` (Session Manager
    и в будущем Browser Manager).
    """

    _provider: ProxyProvider = EnvProxyProvider()

    # Текущий выбранный прокси для провайдеров с пулом (`get_all_proxies()`).
    # Proxy Manager хранит только сам факт "текущего" прокси — решение о
    # том, когда его заменить, принимает Proxy Rotation, а решение о том,
    # каким именно прокси заменить — Proxy Selection.
    _current_proxy: Optional[str] = None

    @classmethod
    def set_provider(cls, provider: ProxyProvider) -> None:
        """
        Заменяет текущий источник прокси на новый провайдер.

        Сбрасывает `_current_proxy` и состояние активной политики ротации,
        чтобы не вернуть устаревший прокси от предыдущего провайдера.

        Args:
            provider (ProxyProvider): Новая реализация источника прокси
                (например, будущий WebshareProxyProvider или FileProvider).
        """
        cls._provider = provider
        cls._current_proxy = None

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        ProxyRotation.reset()


    @classmethod
    def get_provider(cls) -> ProxyProvider:
        """Возвращает текущий активный провайдер прокси."""
        return cls._provider

    @classmethod
    def _select_from_pool(cls, get_all) -> Optional[str]:
        """
        Выбирает один прокси из пула провайдера, используя Proxy Health
        Check (фильтрация) и Proxy Selection (выбор). Общая логика для
        обычного (`get_proxy()`) и sticky (`get_proxy(session_id=...)`)
        путей — вынесена сюда, чтобы не дублировать её в обоих местах.

        Args:
            get_all (Callable[[], List[str]]): `provider.get_all_proxies`.

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        from app.health_check import HealthCheck    # локальный импорт: избегаем циклической зависимости
        from app.proxy_selector import ProxySelector  # локальный импорт: избегаем циклической зависимости

        # Фильтрация пула перед выбором: исключаем DISABLED прокси.
        # Если все прокси отфильтрованы, HealthCheck.filter_healthy()
        # вернёт исходный пул с предупреждением в лог — фреймворк
        # продолжит работу без полной остановки.
        healthy_pool = HealthCheck.filter_healthy(get_all())
        return ProxySelector.select(healthy_pool)

    @classmethod
    def get_proxy(cls, session_id: Optional[str] = None) -> Optional[str]:
        """
        Возвращает прокси-URL для использования сейчас.

        Если передан `session_id` и включены Sticky Sessions
        (`config.STICKY_SESSIONS_ENABLED`), Proxy Manager делегирует выбор
        `StickySessionManager` (`app/sticky_sessions.py`): пока привязка
        сессии активна и не истекла, всегда возвращается один и тот же
        прокси, независимо от активной политики Proxy Rotation. Если
        привязки нет или она истекла (тайм-аут/лимит запросов/прокси стал
        DISABLED) — выбирается новый прокси обычным способом (см. ниже) и
        привязывается к сессии.

        Без `session_id` (или при выключенных Sticky Sessions) поведение
        полностью прежнее — обратная совместимость сохраняется:

        Если активный провайдер предоставляет пул прокси (реализует
        `get_all_proxies()` — как `WebshareProxyProvider`, `FileProxyProvider`
        или `CachedProxyProvider`), Proxy Manager хранит текущий выбранный
        прокси (`_current_proxy`) и переиспользует его до тех пор, пока
        Proxy Rotation (`app/proxy_rotation.py`, `ProxyRotation.should_rotate()`)
        не решит, что пора выбрать новый — тогда выбор нового прокси из
        пула делегируется Proxy Selection (`app/proxy_selector.py`).

        Это единственное место, где Proxy Manager взаимодействует с Proxy
        Rotation, Proxy Selection и Sticky Sessions — сам он не содержит
        ни логики "когда менять", ни логики "какой выбрать", ни логики
        "как долго привязывать".

        Если у провайдера нет пула (например, `EnvProxyProvider`, у
        которого есть только единственное значение `config.PROXY_URL`),
        поведение остается прежним — используется `provider.get_proxy()`
        напрямую, что сохраняет полную обратную совместимость.

        Args:
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions). Если не передан — привязка не используется.

        Returns:
            Optional[str]: Прокси-URL, либо `None`, если прокси не настроен
                или пул провайдера пуст.
        """
        get_all = getattr(cls._provider, "get_all_proxies", None)

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            if StickySessionManager.is_enabled():
                sticky_proxy = StickySessionManager.get_proxy(session_id)
                if sticky_proxy is not None:
                    return sticky_proxy

                new_proxy = (
                    cls._select_from_pool(get_all)
                    if callable(get_all)
                    else cls._provider.get_proxy()
                )
                if new_proxy is not None:
                    StickySessionManager.bind(session_id, new_proxy)
                return new_proxy

        if not callable(get_all):
            return cls._provider.get_proxy()

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        # Первый выбор всегда происходит независимо от политики ротации —
        # без него Proxy Manager не смог бы отдать вообще ничего.
        if cls._current_proxy is None or ProxyRotation.should_rotate():
            cls._current_proxy = cls._select_from_pool(get_all)
            ProxyRotation.reset()

        return cls._current_proxy

    @classmethod
    def report_proxy_failure(cls, session_id: Optional[str] = None) -> None:
        """
        Сообщает Proxy Rotation и Proxy Health Check о сбое при
        использовании текущего прокси.

        Если передан `session_id` и для него есть активная привязка
        (Sticky Sessions), обновляется здоровье именно привязанного
        прокси, а сама привязка обрабатывается через
        `StickySessionManager.report_failure()` (Failure Handling,
        см. TASK.md Sticky Sessions) — политика Proxy Rotation в этом
        случае не затрагивается, так как ротация вне сессии не имеет
        смысла для привязанного прокси.

        Без `session_id` поведение прежнее — обратная совместимость
        сохраняется. Proxy Manager сам не определяет, что считать сбоем —
        это решает вызывающий код (например, будущая интеграция с Retry
        Manager). Используется политикой `RotateAfterFailurePolicy`
        (`app/proxy_rotation.py`) и пассивным мониторингом здоровья
        (`app/health_check.py`).

        Args:
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions).
        """
        from app.health_check import HealthCheck   # локальный импорт: избегаем циклической зависимости

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            sticky_proxy = StickySessionManager.peek_proxy(session_id)
            if sticky_proxy is not None:
                HealthCheck.record_failure(sticky_proxy)
                StickySessionManager.report_failure(session_id)
                return

        if cls._current_proxy is None:
            return

        from app.proxy_rotation import ProxyRotation  # локальный импорт: избегаем циклической зависимости

        HealthCheck.record_failure(cls._current_proxy)
        ProxyRotation.record_failure()

    @classmethod
    def report_proxy_success(
        cls, response_time_ms: Optional[float] = None, session_id: Optional[str] = None
    ) -> None:
        """
        Сообщает Proxy Health Check об успешном запросе через текущий
        прокси (пассивный мониторинг).

        Если передан `session_id` и для него есть активная привязка
        (Sticky Sessions), обновляется здоровье именно привязанного прокси.

        Proxy Manager сам не определяет успешность — это решает
        вызывающий код (будущий Session Manager / Requests Engine).

        Args:
            response_time_ms (float, optional): Время ответа в миллисекундах
                (если доступно — для вычисления среднего времени ответа).
            session_id (str, optional): Идентификатор логической сессии
                (Sticky Sessions).
        """
        from app.health_check import HealthCheck  # локальный импорт: избегаем циклической зависимости

        if session_id is not None:
            from app.sticky_sessions import StickySessionManager  # локальный импорт: избегаем циклической зависимости

            sticky_proxy = StickySessionManager.peek_proxy(session_id)
            if sticky_proxy is not None:
                HealthCheck.record_success(sticky_proxy, response_time_ms)
                return

        if cls._current_proxy is None:
            return

        HealthCheck.record_success(cls._current_proxy, response_time_ms)




    @classmethod
    def to_requests_dict(cls, proxy: Optional[str] = None) -> Dict[str, str]:
        """
        Формирует словарь прокси в формате `requests`
        (`{"http": proxy, "https": proxy}`), готовый для
        `session.proxies = ...` или `requests.get(url, proxies=...)`.

        Args:
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера (`get_proxy()`).

        Returns:
            Dict[str, str]: Словарь прокси для `requests`
                (пустой, если прокси не настроен).
        """
        active_proxy = proxy if proxy is not None else cls.get_proxy()
        if not active_proxy:
            return {}
        return {"http": active_proxy, "https": active_proxy}

    @classmethod
    def apply_to_session(cls, session, proxy: Optional[str] = None) -> None:
        """
        Применяет прокси к `requests.Session`. Используется Session
        Manager при создании сессии — аналогично Cookie Manager и
        Retry Manager, независимо от них.

        Args:
            session (requests.Session): Сессия, к которой применяется прокси.
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера.
        """
        proxies = cls.to_requests_dict(proxy)
        if proxies:
            session.proxies.update(proxies)
            print(f"[{__file__}] Прокси применен к сессии: {cls._mask(proxies['http'])}")

    @classmethod
    def to_playwright_proxy_kwargs(cls, proxy: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Формирует словарь, готовый для передачи в
        `browser.new_context(proxy=...)` в будущей интеграции с Playwright
        (Milestone 4 — Browser Manager).

        Args:
            proxy (str, optional): URL прокси. Если не передан,
                берется у текущего провайдера.

        Returns:
            Optional[Dict[str, Any]]: `{"server": ..., "username": ...,
                "password": ...}`, либо `None`, если прокси не настроен.
        """
        active_proxy = proxy if proxy is not None else cls.get_proxy()
        if not active_proxy:
            return None

        parsed = urlparse(active_proxy)
        server = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
        kwargs: Dict[str, Any] = {"server": server}
        if parsed.username:
            kwargs["username"] = parsed.username
        if parsed.password:
            kwargs["password"] = parsed.password
        return kwargs

    @staticmethod
    def _mask(proxy_url: str) -> str:
        """Маскирует учетные данные в URL прокси для безопасного логирования."""
        parsed = urlparse(proxy_url)
        if parsed.username or parsed.password:
            netloc = f"***:***@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return parsed._replace(netloc=netloc).geturl()
        return proxy_url


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import requests

    print(f"[{__file__}] Текущий прокси (из config.PROXY_URL): {ProxyManager.get_proxy()}")
    print(f"[{__file__}] Словарь для requests: {ProxyManager.to_requests_dict()}")
    print(f"[{__file__}] Kwargs для Playwright: {ProxyManager.to_playwright_proxy_kwargs()}")

    session = requests.Session()
    ProxyManager.apply_to_session(session)
    print(f"[{__file__}] session.proxies: {session.proxies}")

    class DummyProxyProvider(ProxyProvider):
        """Пример альтернативного провайдера для проверки замены без изменения ProxyManager."""

        def get_proxy(self) -> Optional[str]:
            return "http://demo_user:demo_pass@10.0.0.1:8000"

    ProxyManager.set_provider(DummyProxyProvider())
    print(f"[{__file__}] После смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] Замаскированный лог: {ProxyManager._mask(ProxyManager.get_proxy())}")
    print(f"[{__file__}] Playwright kwargs с учетными данными: {ProxyManager.to_playwright_proxy_kwargs()}")

    class PoolProxyProvider(ProxyProvider):
        """Пример провайдера с пулом — демонстрирует Sticky Sessions."""

        def get_proxy(self) -> Optional[str]:
            return self.get_all_proxies()[0]

        def get_all_proxies(self):
            return ["http://1.1.1.1:1111", "http://2.2.2.2:2222", "http://3.3.3.3:3333"]

    ProxyManager.set_provider(PoolProxyProvider())
    print(f"[{__file__}] Sticky Sessions — сессия 'job-1':")
    for _ in range(3):
        print(f"[{__file__}]   get_proxy(session_id='job-1'): {ProxyManager.get_proxy(session_id='job-1')}")

    from app.sticky_sessions import StickySessionManager
    StickySessionManager.reset()

    # Возвращаем провайдер по умолчанию, чтобы не влиять на другие запуски модуля
    ProxyManager.set_provider(EnvProxyProvider())




--- app/proxy_rotation.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Rotation.

Централизованный компонент, отвечающий ТОЛЬКО за то, КОГДА текущий прокси
должен быть заменен новым. Он НЕ решает, КАКОЙ прокси выбрать следующим
(это ответственность Proxy Selection, `app/proxy_selector.py`) и НЕ знает,
откуда прокси берутся (Webshare/File Provider/Proxy Cache и т.д.).

Proxy Rotation:

* НЕ выбирает следующий прокси;
* НЕ скачивает и НЕ валидирует прокси;
* НЕ проверяет здоровье прокси (Health Check — будущий компонент);
* НЕ выполняет HTTP-запросы;
* НЕ содержит provider-specific логики.

Интегрируется только с:
* Configuration Manager (`app/config.py`) — активная политика конфигурируется
  через `.env`, смена политики не требует правок кода;
* Proxy Manager (`app/proxy_manager.py`) — единственный вызывающий код,
  который спрашивает `ProxyRotation.should_rotate()` перед тем, как
  запросить новый выбор у Proxy Selection;
* Proxy Selection — косвенно, только в том смысле, что Rotation определяет
  МОМЕНТ вызова `ProxySelector.select()`, но сам его не вызывает.

Поддерживает несколько политик ротации через реестр
(`ProxyRotation.register_policy()`), что позволяет добавлять будущие
политики (Rotate Every X Minutes, Adaptive Rotation, Manual Rotation и
т.д.) без изменения существующего кода.
"""

from abc import ABC, abstractmethod
from typing import Dict

from app import config


class RotationPolicy(ABC):
    """
    Абстрактная политика ротации.

    Каждый вызов `Proxy Manager.get_proxy()` соответствует одному
    "запросу" в терминах политики. Политика решает, нужно ли сменить
    текущий прокси ПЕРЕД тем, как он будет использован для этого запроса.

    Любая новая политика (Rotate Every X Minutes, Adaptive Rotation и
    т.д.) должна реализовать этот интерфейс и быть зарегистрирована через
    `ProxyRotation.register_policy()` — сам `ProxyRotation` при этом не
    меняется.
    """

    @abstractmethod
    def should_rotate(self) -> bool:
        """
        Определяет, нужно ли заменить текущий прокси перед следующим
        использованием.

        Вызывается Proxy Manager перед каждым `get_proxy()` (после того,
        как уже есть хотя бы один выбранный прокси — самый первый выбор
        всегда происходит независимо от политики, это ответственность
        Proxy Manager, а не Rotation).

        Returns:
            bool: `True`, если Proxy Manager должен запросить новый выбор
                у Proxy Selection.
        """
        raise NotImplementedError

    def record_failure(self) -> None:
        """
        Уведомляет политику о сбое при использовании текущего прокси.

        Базовая реализация — no-op. Переопределяется политиками, которым
        это важно (например, `RotateAfterFailurePolicy`). Вызывается
        через `ProxyManager.report_proxy_failure()` — сам Rotation никогда
        не узнает о сбое иначе, чем через явный вызов извне (Retry Manager
        или будущий Health Check).
        """
        return

    def reset(self) -> None:
        """
        Сбрасывает внутреннее состояние политики (счетчики и т.д.).

        Вызывается Proxy Manager каждый раз, когда фактически происходит
        смена прокси — большинство политик считают именно "запросы с
        текущим прокси", поэтому счетчик должен обнуляться при ротации.
        Базовая реализация — no-op (например, у `NeverRotatePolicy` и
        `RotateEveryRequestPolicy` нет состояния для сброса).
        """
        return


class NeverRotatePolicy(RotationPolicy):
    """Прокси никогда не меняется автоматически после первого выбора."""

    def should_rotate(self) -> bool:
        return False


class RotateEveryRequestPolicy(RotationPolicy):
    """
    Прокси меняется перед каждым запросом.

    Это политика по умолчанию (`config.PROXY_ROTATION_POLICY == "every_request"`),
    воспроизводящая поведение Proxy Manager до появления Proxy Rotation —
    свежий выбор из пула при каждом вызове `get_proxy()`. Гарантирует
    полную обратную совместимость.
    """

    def should_rotate(self) -> bool:
        return True


class RotateEveryNRequestsPolicy(RotationPolicy):
    """Прокси меняется каждый N-й запрос (счетчик сбрасывается при ротации)."""

    def __init__(self, n: int = None):
        """
        Args:
            n (int, optional): Количество запросов между ротациями.
                По умолчанию — `config.PROXY_ROTATION_EVERY_N`.
        """
        self.n = n if n is not None else config.PROXY_ROTATION_EVERY_N
        self._request_count = 0

    def should_rotate(self) -> bool:
        self._request_count += 1
        return self._request_count >= self.n

    def reset(self) -> None:
        self._request_count = 0


class RotateAfterFailurePolicy(RotationPolicy):
    """
    Прокси меняется только после явного сигнала о сбое
    (`ProxyManager.report_proxy_failure()` -> `record_failure()`).

    Сама политика НЕ выполняет HTTP-запросы и НЕ проверяет здоровье прокси —
    она лишь реагирует на внешний сигнал, источник которого (Retry Manager,
    будущий Health Check и т.д.) не является ее заботой.
    """

    def __init__(self):
        self._failed = False

    def record_failure(self) -> None:
        self._failed = True

    def should_rotate(self) -> bool:
        return self._failed

    def reset(self) -> None:
        self._failed = False


class ProxyRotation:
    """
    Централизованная точка доступа к логике ротации прокси.

    Proxy Manager вызывает только `ProxyRotation.should_rotate()` (и,
    при сбоях, `record_failure()`) — он не знает, какая политика активна
    и как она устроена. Активная политика настраивается через
    Configuration Manager (`config.PROXY_ROTATION_POLICY`) и может быть
    переключена в рантайме через `set_policy()`.
    """

    # Реестр доступных политик: имя -> экземпляр. Новые политики
    # добавляются через `register_policy()` без изменения этого класса.
    _policies: Dict[str, RotationPolicy] = {
        "never": NeverRotatePolicy(),
        "every_request": RotateEveryRequestPolicy(),
        "every_n_requests": RotateEveryNRequestsPolicy(),
        "after_failure": RotateAfterFailurePolicy(),
    }

    _active_policy_name: str = config.PROXY_ROTATION_POLICY

    @classmethod
    def register_policy(cls, name: str, policy: RotationPolicy) -> None:
        """
        Регистрирует новую политику ротации без изменения существующего кода.

        Args:
            name (str): Уникальное имя политики (используется в
                `config.PROXY_ROTATION_POLICY` и `set_policy()`).
            policy (RotationPolicy): Экземпляр политики.
        """
        cls._policies[name] = policy

    @classmethod
    def set_policy(cls, name: str) -> None:
        """
        Переключает активную политику ротации в рантайме.

        Args:
            name (str): Имя зарегистрированной политики.

        Raises:
            ValueError: Если политика с таким именем не зарегистрирована.
        """
        if name not in cls._policies:
            raise ValueError(
                f"Неизвестная политика ротации прокси: '{name}'. "
                f"Доступные: {list(cls._policies.keys())}"
            )
        cls._active_policy_name = name

    @classmethod
    def get_policy_name(cls) -> str:
        """Возвращает имя текущей активной политики."""
        return cls._active_policy_name

    @classmethod
    def _get_active_policy(cls) -> RotationPolicy:
        """
        Возвращает экземпляр активной политики.

        Если сконфигурированная политика неизвестна (например, опечатка
        в `.env`), не падает — откатывается на `RotateEveryRequestPolicy`
        (эквивалент прежнего поведения) с предупреждением в лог.
        """
        policy = cls._policies.get(cls._active_policy_name)
        if policy is None:
            print(f"[{__file__}] Предупреждение: политика ротации прокси "
                  f"'{cls._active_policy_name}' не зарегистрирована. "
                  f"Используется 'every_request'.")
            policy = cls._policies["every_request"]
        return policy

    @classmethod
    def should_rotate(cls) -> bool:
        """
        Определяет, нужно ли заменить текущий прокси перед следующим
        использованием, используя текущую активную политику.

        Returns:
            bool: `True`, если Proxy Manager должен запросить новый выбор
                у Proxy Selection.
        """
        return cls._get_active_policy().should_rotate()

    @classmethod
    def record_failure(cls) -> None:
        """
        Уведомляет активную политику о сбое при использовании текущего
        прокси (см. `ProxyManager.report_proxy_failure()`).
        """
        cls._get_active_policy().record_failure()

    @classmethod
    def reset(cls) -> None:
        """
        Сбрасывает состояние активной политики. Вызывается Proxy Manager
        каждый раз, когда фактически происходит смена прокси.
        """
        cls._get_active_policy().reset()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Активная политика (из config): {ProxyRotation.get_policy_name()}")

    ProxyRotation.set_policy("every_request")
    print(f"[{__file__}] every_request x3: "
          f"{[ProxyRotation.should_rotate() for _ in range(3)]}")

    ProxyRotation.set_policy("never")
    print(f"[{__file__}] never x3: {[ProxyRotation.should_rotate() for _ in range(3)]}")

    ProxyRotation.set_policy("every_n_requests")
    policy = ProxyRotation._get_active_policy()
    policy.n = 3
    policy.reset()
    results = []
    for _ in range(7):
        rotate = ProxyRotation.should_rotate()
        results.append(rotate)
        if rotate:
            ProxyRotation.reset()
    print(f"[{__file__}] every_n_requests (n=3) за 7 вызовов: {results}")

    ProxyRotation.set_policy("after_failure")
    print(f"[{__file__}] after_failure до сбоя: {ProxyRotation.should_rotate()}")
    ProxyRotation.record_failure()
    print(f"[{__file__}] after_failure после сбоя: {ProxyRotation.should_rotate()}")
    ProxyRotation.reset()
    print(f"[{__file__}] after_failure после reset(): {ProxyRotation.should_rotate()}")

    # Демонстрация расширения без изменения ProxyRotation/RotationPolicy
    class RotateEveryXMinutesPolicy(RotationPolicy):
        """Пример будущей политики — заглушка, всегда возвращает False."""

        def should_rotate(self) -> bool:
            return False

    ProxyRotation.register_policy("every_x_minutes", RotateEveryXMinutesPolicy())
    ProxyRotation.set_policy("every_x_minutes")
    print(f"[{__file__}] Новая политика 'every_x_minutes' (пример расширения): "
          f"{ProxyRotation.should_rotate()}")

    # Возвращаем политику по умолчанию, чтобы не влиять на другие запуски модуля
    ProxyRotation.set_policy(config.PROXY_ROTATION_POLICY)


--- app/proxy_selector.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Selection.

Централизованный компонент, отвечающий ТОЛЬКО за выбор одного прокси из
уже готового пула (`List[str]`), полученного от Proxy Manager.

Proxy Selection:

* НЕ знает, откуда взялся пул прокси (Webshare, File Provider, Proxy Cache
  и т.д.) — работает исключительно со списком строк, который ему передают;
* НЕ скачивает, НЕ валидирует и НЕ проверяет здоровье прокси;
* НЕ ротирует прокси после сбоев и НЕ поддерживает sticky-сессии — это
  ответственность будущих компонентов (Proxy Rotation, Health Check,
  Sticky Sessions, см. `framework/ROADMAP.md`, Milestone 3);
* НЕ выполняет HTTP-запросы.

Поддерживает несколько стратегий выбора через простой реестр
(`ProxySelector.register_strategy()`), что позволяет добавлять новые
стратегии (Round Robin, LRU, Fastest Proxy, Priority Based и т.д.) в
будущем без изменения существующего кода — достаточно зарегистрировать
новый класс `SelectionStrategy` и переключить `PROXY_SELECTION_STRATEGY`
в Configuration Manager.
"""

import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app import config


class SelectionStrategy(ABC):
    """
    Абстрактная стратегия выбора одного прокси из пула.

    Любая новая стратегия (Round Robin, LRU, Fastest Proxy и т.д.) должна
    реализовать этот интерфейс и быть зарегистрирована через
    `ProxySelector.register_strategy()` — сам `ProxySelector` при этом не
    меняется.
    """

    @abstractmethod
    def select(self, proxies: List[str]) -> Optional[str]:
        """
        Выбирает один прокси из переданного пула.

        Args:
            proxies (List[str]): Пул доступных прокси (может быть пустым).

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        raise NotImplementedError


class FirstAvailableStrategy(SelectionStrategy):
    """Всегда выбирает первый прокси из пула (самая простая, детерминированная стратегия)."""

    def select(self, proxies: List[str]) -> Optional[str]:
        return proxies[0] if proxies else None


class RandomStrategy(SelectionStrategy):
    """Выбирает случайный прокси из пула — простое равномерное распределение нагрузки."""

    def select(self, proxies: List[str]) -> Optional[str]:
        return random.choice(proxies) if proxies else None


class ProxySelector:
    """
    Централизованная точка доступа к логике выбора прокси.

    Proxy Manager вызывает только `ProxySelector.select(pool)` — он не
    знает, какая стратегия активна и как она устроена. Активная стратегия
    настраивается через Configuration Manager (`config.PROXY_SELECTION_STRATEGY`)
    и может быть переключена в рантайме через `set_strategy()`.
    """

    # Реестр доступных стратегий: имя -> экземпляр. Новые стратегии
    # добавляются через `register_strategy()` без изменения этого класса.
    _strategies: Dict[str, SelectionStrategy] = {
        "first": FirstAvailableStrategy(),
        "random": RandomStrategy(),
    }

    _active_strategy_name: str = config.PROXY_SELECTION_STRATEGY

    @classmethod
    def register_strategy(cls, name: str, strategy: SelectionStrategy) -> None:
        """
        Регистрирует новую стратегию выбора без изменения существующего кода.

        Args:
            name (str): Уникальное имя стратегии (используется в
                `config.PROXY_SELECTION_STRATEGY` и `set_strategy()`).
            strategy (SelectionStrategy): Экземпляр стратегии.
        """
        cls._strategies[name] = strategy

    @classmethod
    def set_strategy(cls, name: str) -> None:
        """
        Переключает активную стратегию выбора в рантайме.

        Args:
            name (str): Имя зарегистрированной стратегии.

        Raises:
            ValueError: Если стратегия с таким именем не зарегистрирована.
        """
        if name not in cls._strategies:
            raise ValueError(
                f"Неизвестная стратегия выбора прокси: '{name}'. "
                f"Доступные: {list(cls._strategies.keys())}"
            )
        cls._active_strategy_name = name

    @classmethod
    def get_strategy_name(cls) -> str:
        """Возвращает имя текущей активной стратегии."""
        return cls._active_strategy_name

    @classmethod
    def select(cls, proxies: List[str]) -> Optional[str]:
        """
        Выбирает один прокси из пула, используя текущую активную стратегию.

        Если сконфигурированная стратегия неизвестна (например, опечатка в
        `.env`), не падает — откатывается на `FirstAvailableStrategy` с
        предупреждением в лог, чтобы не ломать работу фреймворка.

        Args:
            proxies (List[str]): Пул доступных прокси.

        Returns:
            Optional[str]: Выбранный прокси, либо `None`, если пул пуст.
        """
        strategy = cls._strategies.get(cls._active_strategy_name)
        if strategy is None:
            print(f"[{__file__}] Предупреждение: стратегия выбора прокси "
                  f"'{cls._active_strategy_name}' не зарегистрирована. "
                  f"Используется 'first'.")
            strategy = cls._strategies["first"]
        return strategy.select(proxies)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    pool = ["http://1.1.1.1:1111", "http://2.2.2.2:2222", "http://3.3.3.3:3333"]

    print(f"[{__file__}] Активная стратегия (из config): {ProxySelector.get_strategy_name()}")
    print(f"[{__file__}] select() с текущей стратегией: {ProxySelector.select(pool)}")

    ProxySelector.set_strategy("first")
    print(f"[{__file__}] FirstAvailable: {ProxySelector.select(pool)}")

    ProxySelector.set_strategy("random")
    print(f"[{__file__}] Random (3 выбора): "
          f"{[ProxySelector.select(pool) for _ in range(3)]}")

    print(f"[{__file__}] select() на пустом пуле: {ProxySelector.select([])}")

    # Демонстрация расширения без изменения ProxySelector/SelectionStrategy
    class LastAvailableStrategy(SelectionStrategy):
        """Пример будущей стратегии — выбирает последний прокси в пуле."""

        def select(self, proxies: List[str]) -> Optional[str]:
            return proxies[-1] if proxies else None

    ProxySelector.register_strategy("last", LastAvailableStrategy())
    ProxySelector.set_strategy("last")
    print(f"[{__file__}] Новая стратегия 'last' (пример расширения): {ProxySelector.select(pool)}")

    # Возвращаем стратегию по умолчанию, чтобы не влиять на другие запуски модуля
    ProxySelector.set_strategy(config.PROXY_SELECTION_STRATEGY)


--- app/request_profile.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Request Profile Manager.

Централизует понятие "браузерная идентичность" (Request Profile) —
набор HTTP-заголовков и клиентских параметров (locale, timezone, viewport),
которые описывают, "кем представляется" скрапер при обращении к сайту.

Профиль является ЕДИНСТВЕННЫМ источником правды об идентичности клиента
и может быть переиспользован:

* модулем на базе `requests`/`httpx` — через `RequestProfile.to_headers()`;
* модулем Playwright (`app/browser.py`) — через
  `RequestProfile.to_playwright_context_kwargs()`.

Этот модуль НЕ выполняет запросы, НЕ управляет сессиями, куками,
прокси или повторами — это ответственность будущих компонентов
(Session Manager, Cookie Manager, Proxy Manager, Retry Manager).
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from app import config


@dataclass(frozen=True)
class RequestProfile:
    """
    Неизменяемое описание полной браузерной идентичности клиента.

    Содержит как HTTP-заголовки, так и клиентские параметры окружения
    (locale, timezone, viewport), общие для Requests и Playwright.
    """

    user_agent: str
    accept: str
    accept_language: str
    accept_encoding: str
    connection: str
    upgrade_insecure_requests: str
    sec_fetch_dest: str
    sec_fetch_mode: str
    sec_fetch_site: str
    dnt: str
    locale: str
    timezone: str
    viewport: Dict[str, int] = field(default_factory=dict)

    def to_headers(self) -> Dict[str, str]:
        """
        Формирует словарь HTTP-заголовков, готовый для передачи в
        `requests`/`httpx` (например, `requests.get(url, headers=profile.to_headers())`).
        """
        return {
            "User-Agent": self.user_agent,
            "Accept": self.accept,
            "Accept-Language": self.accept_language,
            "Accept-Encoding": self.accept_encoding,
            "Connection": self.connection,
            "Upgrade-Insecure-Requests": self.upgrade_insecure_requests,
            "Sec-Fetch-Dest": self.sec_fetch_dest,
            "Sec-Fetch-Mode": self.sec_fetch_mode,
            "Sec-Fetch-Site": self.sec_fetch_site,
            "DNT": self.dnt,
        }

    def to_playwright_context_kwargs(self) -> Dict[str, Any]:
        """
        Формирует словарь именованных аргументов, готовый для передачи
        в `browser.new_context(**kwargs)` в будущей интеграции с Playwright.

        Заголовки Accept/Sec-Fetch-* здесь не передаются, так как Playwright
        сам управляет частью низкоуровневых заголовков навигации; при
        необходимости их можно точечно докинуть через `extra_http_headers`.
        """
        return {
            "user_agent": self.user_agent,
            "locale": self.locale,
            "timezone_id": self.timezone,
            "viewport": self.viewport,
            "extra_http_headers": {
                "Accept-Language": self.accept_language,
                "DNT": self.dnt,
            },
        }


class RequestProfileManager:
    """
    Фабрика/реестр Request Profile.

    Предоставляет один переиспользуемый профиль по умолчанию, собранный из
    централизованной конфигурации (`app/config.py`), а также позволяет
    создавать кастомные профили с точечным переопределением полей —
    без дублирования дефолтных значений.
    """

    @staticmethod
    def default_profile() -> RequestProfile:
        """Возвращает профиль идентичности, собранный из app/config.py."""
        return RequestProfile(
            user_agent=config.DEFAULT_USER_AGENT,
            accept=config.DEFAULT_ACCEPT,
            accept_language=config.DEFAULT_ACCEPT_LANGUAGE,
            accept_encoding=config.DEFAULT_ACCEPT_ENCODING,
            connection=config.DEFAULT_CONNECTION,
            upgrade_insecure_requests=config.DEFAULT_UPGRADE_INSECURE_REQUESTS,
            sec_fetch_dest=config.DEFAULT_SEC_FETCH_DEST,
            sec_fetch_mode=config.DEFAULT_SEC_FETCH_MODE,
            sec_fetch_site=config.DEFAULT_SEC_FETCH_SITE,
            dnt=config.DEFAULT_DNT,
            locale=config.BROWSER_LOCALE,
            timezone=config.BROWSER_TIMEZONE,
            viewport=dict(config.BROWSER_VIEWPORT),
        )

    @classmethod
    def create_profile(cls, **overrides: Any) -> RequestProfile:
        """
        Создает профиль на основе дефолтного, переопределяя только
        указанные поля. Позволяет получать кастомные идентичности
        (например, мобильный User-Agent) без дублирования остальных полей.

        Args:
            **overrides: Поля `RequestProfile` для переопределения.

        Returns:
            RequestProfile: Новый профиль с примененными переопределениями.
        """
        base = cls.default_profile()
        return RequestProfile(**{**base.__dict__, **overrides})


# Готовый к использованию профиль по умолчанию (ленивая точка доступа).
def get_default_profile() -> RequestProfile:
    """Возвращает профиль идентичности по умолчанию (удобный шорткат)."""
    return RequestProfileManager.default_profile()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    profile = RequestProfileManager.default_profile()
    print(f"[{__file__}] Профиль идентичности по умолчанию:")
    print("  Headers:", profile.to_headers())
    print("  Playwright kwargs:", profile.to_playwright_context_kwargs())

    mobile_profile = RequestProfileManager.create_profile(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
    )
    print(f"[{__file__}] Кастомный (мобильный) профиль:")
    print("  Headers:", mobile_profile.to_headers())


--- app/requests_engine.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Requests Engine.

Централизованный HTTP-исполнительный слой фреймворка для всех
не-браузерных задач скрапинга (см. `framework/ROADMAP.md`, Milestone 4).

Requests Engine — единственная точка, через которую скрапер-модули должны
выполнять HTTP GET/POST запросы. Он НЕ содержит собственной логики
куки/повторов/задержек/прокси — вся эта логика уже инкапсулирована в
существующих менеджерах и автоматически применяется через Session Manager
(`app/session_manager.py`), который остается единственным компонентом,
координирующим Cookie/Retry/Delay/Proxy Manager вокруг `requests.Session`.

Архитектура (см. `app/session_manager.py` для полной схемы HTTP-слоя):

    Requests Engine
            │
            ▼
    Session Manager  ──────────────────────────────┐
            │                                       │
     ┌──────┼────────┬────────┐                     │
     ▼      ▼         ▼        ▼                     ▼
    Cookie  Retry    Delay    Proxy            Configuration
    Manager Manager  Manager  Manager               Manager

Requests Engine:

* создает (через `SessionManager.create_session()`) и хранит одну
  `requests.Session` на инстанс — это обеспечивает переиспользование
  TCP-соединений (keep-alive) и куки между вызовами одного скрапинг-джоба,
  при этом сама сессия уже полностью настроена (профиль идентичности,
  куки, retry-адаптер, прокси) без единой строчки дополнительного кода;
* делает паузу перед каждым запросом через
  `SessionManager.wait_before_request()` (Delay Manager) — вызывающий код
  не должен думать о задержках между запросами;
* НЕ реализует собственный цикл повторов — повторы транспортного уровня
  (сетевые сбои, HTTP 429/500/502/503/504) уже покрыты retry-адаптером,
  смонтированным Session Manager через Retry Manager
  (`RetryManager.apply_to_session()`), поэтому добавление еще одного слоя
  повторов здесь привело бы к дублированию логики и непредсказуемому
  умножению количества попыток — что запрещено `framework/AI_RULES.md`
  (DRY, avoid overengineering);
* сообщает Proxy Manager об успехе/сбое каждого запроса
  (`ProxyManager.report_proxy_success()`/`report_proxy_failure()`), что
  прозрачно питает Proxy Health Check и Proxy Rotation/Sticky Sessions,
  если движку передан `session_id`;
* оборачивает все ожидаемые сетевые сбои (таймаут, соединение, DNS, SSL),
  оставшиеся после исчерпания повторов Retry Manager, в единое понятное
  исключение `RequestsEngineError` — вызывающему коду не нужно знать о
  внутренних исключениях `requests`;
* возвращает "сырой" `requests.Response` из `get()`/`post()`/`request()`
  (по требованию задачи), а также предоставляет удобные шорткаты
  `get_json()`/`post_json()`/`get_text()` и `download_file()` для
  скачивания бинарного содержимого — без парсинга HTML/JSON в бизнес-объекты
  (это ответственность будущего Parsing-слоя, Milestone 5).

Requests Engine НЕ парсит HTML, НЕ парсит JSON в бизнес-объекты, НЕ
экспортирует данные, ничего не знает о BeautifulSoup или Playwright.
"""

import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests

from app import config
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile
from app.session_manager import SessionManager

# Размер буфера чтения при потоковом скачивании файлов (байт). Стандартное
# для requests значение — используется как единственная точка правды,
# чтобы не хардкодить "магическое число" в нескольких местах.
DEFAULT_DOWNLOAD_CHUNK_SIZE = 8192

# HTTP-статус, начиная с которого ответ считается серверной ошибкой.
_HTTP_SERVER_ERROR_THRESHOLD = 500
# HTTP-статус, начиная с которого ответ считается клиентской/серверной
# ошибкой (используется только для логирования уровня warning).
_HTTP_CLIENT_ERROR_THRESHOLD = 400

# Исключения `requests`, которые считаются "ожидаемыми" сетевыми сбоями
# (таймаут, соединение, DNS-резолвинг, SSL, слишком много редиректов) и
# оборачиваются в `RequestsEngineError` вместо падения с трассировкой
# внутренностей `requests`/`urllib3`.
_HANDLED_REQUEST_EXCEPTIONS = (
    requests.exceptions.ConnectionError,  # покрывает также DNS-сбои и SSLError (см. requests.exceptions)
    requests.exceptions.Timeout,
    requests.exceptions.TooManyRedirects,
)


class RequestsEngineError(Exception):
    """
    Единое исключение Requests Engine для всех сбоев HTTP-запроса,
    оставшихся после исчерпания повторов Retry Manager.

    Позволяет вызывающему коду (будущим скрапер-модулям) обрабатывать
    ошибки сети без необходимости импортировать и знать про исключения
    `requests`/`urllib3`.
    """


class RequestsEngine:
    """
    Централизованный исполнитель HTTP-запросов для скрапинга без браузера.

    Каждый инстанс хранит одну настроенную `requests.Session`, что позволяет
    переиспользовать соединения и куки между запросами одного логического
    джоба. Все компоненты HTTP-слоя (Configuration/Request Profile/Session/
    Cookie/Retry/Delay/Proxy Manager) подключаются автоматически — вызывающий
    код не настраивает их вручную.
    """

    def __init__(
        self,
        profile: Optional[RequestProfile] = None,
        session_id: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        """
        Args:
            profile (RequestProfile, optional): Профиль идентичности для
                новой сессии. Игнорируется, если передан готовый `session`.
                По умолчанию — профиль из `RequestProfileManager.default_profile()`
                (применяется внутри `SessionManager.create_session()`).
            session_id (str, optional): Идентификатор логической сессии для
                Sticky Sessions/Proxy Rotation/Health Check
                (см. `ProxyManager.get_proxy(session_id=...)`). Если не
                передан — прокси выбирается без привязки к сессии
                (обратная совместимость, поведение как раньше).
            session (requests.Session, optional): Готовая сессия для
                переиспользования (например, между несколькими движками).
                Если не передана, создается новая через
                `SessionManager.create_session()`.
        """
        self.session_id = session_id
        self.session: requests.Session = session or SessionManager.create_session(profile=profile)
        # Максимальная длина цепочки редиректов централизована в Configuration Manager.
        self.session.max_redirects = config.REQUESTS_MAX_REDIRECTS

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        allow_redirects: Optional[bool] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Выполняет один HTTP-запрос через настроенную сессию.

        Перед запросом выполняется пауза согласно Delay Manager
        (`SessionManager.wait_before_request()`). Повторы при временных
        сбоях выполняются прозрачно retry-адаптером, смонтированным Session
        Manager через Retry Manager — эта функция не реализует собственный
        цикл повторов.

        Args:
            method (str): HTTP-метод ("GET", "POST" и т.д.).
            url (str): Целевой URL.
            params (dict, optional): Query-параметры.
            data (dict | str | bytes, optional): Тело запроса
                (form-encoded, если передан словарь).
            json (Any, optional): Тело запроса, сериализуемое в JSON
                (устанавливает `Content-Type: application/json`).
            headers (dict, optional): Дополнительные заголовки,
                дополняющие (и переопределяющие при совпадении имени)
                заголовки профиля идентичности сессии.
            files (dict, optional): Файлы для multipart-запроса
                (например, `{"file": open(path, "rb")}`).
            timeout (float, optional): Таймаут запроса (секунды).
                По умолчанию — `SessionManager.timeout` (Configuration Manager).
            allow_redirects (bool, optional): Следовать ли редиректам.
                По умолчанию — `config.REQUESTS_ALLOW_REDIRECTS`.
            stream (bool): Не загружать содержимое ответа немедленно
                (используется `download_file()` для потокового скачивания).
            **kwargs: Дополнительные именованные аргументы, передаваемые
                напрямую в `requests.Session.request()`.

        Returns:
            requests.Response: "Сырой" объект ответа.

        Raises:
            RequestsEngineError: При сетевом сбое (таймаут, соединение,
                DNS, SSL, слишком много редиректов), оставшемся после
                исчерпания повторов Retry Manager.
        """
        SessionManager.wait_before_request()

        effective_timeout = timeout if timeout is not None else SessionManager.timeout
        effective_redirects = (
            allow_redirects if allow_redirects is not None else config.REQUESTS_ALLOW_REDIRECTS
        )

        start = time.monotonic()
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                files=files,
                timeout=effective_timeout,
                allow_redirects=effective_redirects,
                verify=config.REQUESTS_VERIFY_SSL,
                stream=stream,
                **kwargs,
            )
        except _HANDLED_REQUEST_EXCEPTIONS as exc:
            print(f"[{__file__}] Сбой запроса {method} {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise RequestsEngineError(f"{method} {url} завершился ошибкой: {exc}") from exc

        elapsed_ms = (time.monotonic() - start) * 1000.0

        if response.status_code >= _HTTP_SERVER_ERROR_THRESHOLD:
            print(f"[{__file__}] Предупреждение: HTTP {response.status_code} для {method} {url}")
            # Серверная ошибка (после исчерпания повторов Retry Manager) —
            # сигнализируем Proxy Manager как сбой, чтобы Health Check/Rotation
            # учли деградацию именно этого прокси.
            ProxyManager.report_proxy_failure(session_id=self.session_id)
        else:
            if response.status_code >= _HTTP_CLIENT_ERROR_THRESHOLD:
                print(f"[{__file__}] Предупреждение: HTTP {response.status_code} для {method} {url}")
            # Соединение через прокси отработало (даже если сайт вернул 4xx) —
            # это успех с точки зрения Proxy Health Check.
            ProxyManager.report_proxy_success(response_time_ms=elapsed_ms, session_id=self.session_id)

        return response

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Выполняет HTTP GET-запрос. См. `request()` для описания аргументов."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        """Выполняет HTTP POST-запрос. См. `request()` для описания аргументов."""
        return self.request("POST", url, **kwargs)

    def get_text(self, url: str, **kwargs: Any) -> str:
        """Выполняет GET и возвращает тело ответа как декодированный текст."""
        return self.get(url, **kwargs).text

    def get_json(self, url: str, **kwargs: Any) -> Optional[Any]:
        """
        Выполняет GET и декодирует тело ответа как JSON.

        Returns:
            Optional[Any]: Декодированный JSON, либо `None`, если ответ
                не является валидным JSON (невалидный ответ обрабатывается
                гарантированно, без падения вызывающего кода).
        """
        return self._safe_json(self.get(url, **kwargs))

    def post_json(self, url: str, **kwargs: Any) -> Optional[Any]:
        """Выполняет POST и декодирует тело ответа как JSON. См. `get_json()`."""
        return self._safe_json(self.post(url, **kwargs))

    @staticmethod
    def _safe_json(response: requests.Response) -> Optional[Any]:
        """Декодирует JSON из ответа, гарантированно обрабатывая невалидный формат."""
        try:
            return response.json()
        except ValueError as exc:
            print(f"[{__file__}] Предупреждение: невалидный JSON в ответе {response.url}: {exc}")
            return None

    def download_file(
        self,
        url: str,
        destination: Union[str, Path],
        chunk_size: int = DEFAULT_DOWNLOAD_CHUNK_SIZE,
        **kwargs: Any,
    ) -> Path:
        """
        Скачивает бинарное содержимое по URL и сохраняет его в файл,
        не загружая весь ответ в память сразу (потоковое чтение).

        Args:
            url (str): URL файла для скачивания.
            destination (str | Path): Путь для сохранения файла.
                Родительские директории создаются автоматически.
            chunk_size (int): Размер буфера чтения в байтах.
                По умолчанию — `DEFAULT_DOWNLOAD_CHUNK_SIZE`.
            **kwargs: Дополнительные аргументы, передаваемые в `get()`
                (например, `headers`, `params`).

        Returns:
            Path: Путь к сохраненному файлу.

        Raises:
            RequestsEngineError: При сетевом сбое во время скачивания.
        """
        destination_path = Path(destination)
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        kwargs.pop("stream", None)  # stream=True принудительно для скачивания файлов
        response = self.get(url, stream=True, **kwargs)

        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        print(f"[{__file__}] Файл сохранен: {destination_path} ({url})")
        return destination_path

    def close(self) -> None:
        """Закрывает внутреннюю HTTP-сессию (освобождает соединения)."""
        self.session.close()

    def __enter__(self) -> "RequestsEngine":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# =====================================================================
# Модульные шорткаты на общем движке по умолчанию — удобны для простых
# скриптов, где не требуется явное управление сессией/session_id
# (аналогично `get_default_profile()` в app/request_profile.py).
# =====================================================================

_default_engine: Optional[RequestsEngine] = None


def get_default_engine() -> RequestsEngine:
    """Возвращает общий (ленивая инициализация) движок по умолчанию."""
    global _default_engine
    if _default_engine is None:
        _default_engine = RequestsEngine()
    return _default_engine


def get(url: str, **kwargs: Any) -> requests.Response:
    """Шорткат: GET-запрос через движок по умолчанию."""
    return get_default_engine().get(url, **kwargs)


def post(url: str, **kwargs: Any) -> requests.Response:
    """Шорткат: POST-запрос через движок по умолчанию."""
    return get_default_engine().post(url, **kwargs)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    engine = RequestsEngine()
    print(f"[{__file__}] Тестовый GET-запрос...")
    try:
        resp = engine.get("https://httpbin.org/get")
        print(f"[{__file__}] Статус: {resp.status_code}")
        print(f"[{__file__}] JSON: {engine.get_json('https://httpbin.org/get')}")
    except RequestsEngineError as e:
        print(f"[{__file__}] Ошибка запроса (ожидаемо без интернета в CI): {e}")
    finally:
        engine.close()


--- app/resume_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resume Support.

Централизованный компонент, отвечающий ТОЛЬКО за обнаружение,
валидацию и восстановление прогресса прерванной сессии скрапинга на
основе чекпоинтов, сохранённых Checkpoint Manager'ом (см.
`framework/ROADMAP.md`, Milestone 6, и `tasks/TASK.md`).

Resume Support:

* обнаруживает существующий чекпоинт через уже существующий
  `CheckpointManager.load()` (не реализует собственный механизм чтения
  состояния — переиспользует Checkpoint Manager, как того требует
  `tasks/TASK.md`, раздел "Do not duplicate checkpoint logic");
* валидирует чекпоинт (обязательные поля, статус, "свежесть" по
  `RESUME_MAX_AGE_SECONDS`, совместимость версии схемы);
* "засеивает" уже существующий `CheckpointManager` восстановленным
  состоянием через его публичное свойство `state` — не добавляет новую
  персистентность, только переиспользует объект, который сам же
  продолжит сохранять чекпоинты дальше в течение новой сессии;
* сообщает вызывающему коду (`app/main.py`), сколько страниц уже было
  обработано ранее, чтобы цикл скрапинга мог их пропустить.

Resume Support НЕ создаёт чекпоинты (это делает Checkpoint Manager), НЕ
пишет файлы экспорта (это делают `IncrementalCSVWriter`/`JSONWriter` в
режиме `append=True`, см. `app/exporter.py`) и НЕ выполняет парсинг —
он полностью независим от scraper-специфичного кода, как и Checkpoint
Manager, и может использоваться с любым скрапером фреймворка без
изменений.

Пример использования (см. интеграцию в `app/main.py::_run_incremental()`):

    from app.checkpoint_manager import CheckpointManager
    from app.resume_manager import ResumeManager

    checkpoint = CheckpointManager(run_id="olx_cars_2024")
    decision = ResumeManager().resume(checkpoint)

    if decision.resumed:
        print(f"Продолжаем с страницы {decision.start_page + 1}")
    else:
        checkpoint.start(status="running")

    for page_number, html in enumerate(raw_pages_content, 1):
        if page_number <= decision.start_page:
            continue  # уже обработано в прошлой сессии — не дублируем
        ...
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.checkpoint_manager import CheckpointManager
from app.config import RESUME_ENABLED, RESUME_MAX_AGE_SECONDS
from app.utils import log_message

# Статусы чекпоинта, которые считаются "прерванными" и подлежат
# восстановлению. "completed" сознательно НЕ входит в этот список —
# завершённую сессию не нужно "продолжать" (см. TASK.md, требование не
# путать полностью выполненную работу с прерванной).
_RESUMABLE_STATUSES = ("running", "failed")

# Обязательные поля, без которых чекпоинт считается повреждённым/неполным
# (см. TASK.md, "Error Handling" -> "incomplete checkpoint data").
_REQUIRED_FIELDS = ("run_id", "status", "current_page", "timestamp")


@dataclass
class ResumeDecision:
    """
    Результат попытки восстановления, возвращаемый `ResumeManager.resume()`.

    Атрибуты:
        resumed (bool): True, если сессия была успешно восстановлена из
            валидного чекпоинта; False — начата новая сессия "с нуля"
            (нет чекпоинта, он невалиден/устарел, либо Resume Support
            отключен через `RESUME_ENABLED`).
        start_page (int): Номер последней уже обработанной страницы.
            Вызывающий код должен пропустить страницы с номером
            `<= start_page` (см. TASK.md, "avoid reprocessing already
            completed work"). При `resumed=False` всегда 0.
        processed_count (int): Количество записей, обработанных в
            прошлой сессии (для информации/логирования). 0, если не
            восстановлено.
        exported_count (int): Количество записей, реально
            экспортированных в прошлой сессии — именно это значение
            должно совпадать с фактическим содержимым файлов вывода,
            открытых в режиме `append=True`. 0, если не восстановлено.
        reason (str): Причина решения — "no_checkpoint", "disabled",
            "invalid_checkpoint", "expired_checkpoint",
            "already_completed" или "resumed".
        checkpoint_data (dict, optional): Сырые данные восстановленного
            чекпоинта (для расширенного использования вызывающим кодом,
            например восстановления `current_url`/`extra_metadata`).
    """

    resumed: bool
    start_page: int = 0
    processed_count: int = 0
    exported_count: int = 0
    reason: str = "no_checkpoint"
    checkpoint_data: Optional[Dict[str, Any]] = None


class ResumeManager:
    """
    Принимает решение "можно ли и нужно ли восстанавливать сессию" и
    передаёт восстановленное состояние в уже существующий
    `CheckpointManager`, не создавая собственного хранилища состояния.
    """

    def __init__(
        self,
        *,
        enabled: Optional[bool] = None,
        max_age_seconds: Optional[int] = None,
    ) -> None:
        """
        Args:
            enabled: Включает/выключает автоматическое восстановление.
                По умолчанию — `config.RESUME_ENABLED`.
            max_age_seconds: Максимальный возраст чекпоинта (секунды),
                при котором он ещё пригоден для восстановления. 0 — не
                ограничивать. По умолчанию — `config.RESUME_MAX_AGE_SECONDS`.
        """
        self.enabled = enabled if enabled is not None else RESUME_ENABLED
        self.max_age_seconds = max_age_seconds if max_age_seconds is not None else RESUME_MAX_AGE_SECONDS

    def resume(self, checkpoint: CheckpointManager) -> ResumeDecision:
        """
        Пытается обнаружить и восстановить прогресс из чекпоинта,
        связанного с переданным `CheckpointManager` (используется его
        `file_path`, чтобы Resume Support не хранил собственный путь —
        единый источник правды остаётся в Checkpoint Manager).

        При успешном восстановлении "засеивает" `checkpoint.state`
        восстановленными значениями через публичное свойство `state` —
        сам `checkpoint` после этого продолжает работать как обычно
        (`record_page()`, `finish()` и т.д.), просто не с нулевого, а с
        восстановленного состояния. Явно НЕ вызывает `checkpoint.start()`
        здесь — это оставлено на решение вызывающего кода (`app/main.py`),
        чтобы Resume Support не диктовал момент первой записи на диск.

        Args:
            checkpoint: Экземпляр `CheckpointManager`, чей `file_path`
                используется для поиска чекпоинта, и чьё состояние
                будет обновлено при успешном восстановлении.

        Returns:
            ResumeDecision: Итоговое решение (см. докстринг класса).
        """
        if not self.enabled:
            log_message("info", "ResumeManager: восстановление отключено (RESUME_ENABLED=0) — новая сессия")
            return ResumeDecision(resumed=False, reason="disabled")

        data = CheckpointManager.load(checkpoint.file_path)
        if data is None:
            log_message("info", "ResumeManager: чекпоинт не найден — начинается новая сессия")
            return ResumeDecision(resumed=False, reason="no_checkpoint")

        log_message("info", f"ResumeManager: обнаружен чекпоинт ({checkpoint.file_path.name})")

        validation_error = self._validate(data)
        if validation_error is not None:
            log_message(
                "error",
                f"ResumeManager: чекпоинт невалиден ({validation_error}) — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="invalid_checkpoint")

        if data["status"] not in _RESUMABLE_STATUSES:
            # status == "completed" — работа уже была полностью
            # завершена в прошлый раз, восстанавливать нечего.
            log_message(
                "info",
                f"ResumeManager: чекпоинт со статусом '{data['status']}' не подлежит "
                f"восстановлению — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="already_completed")

        if self._is_expired(data):
            log_message(
                "error",
                f"ResumeManager: чекпоинт устарел (старше {self.max_age_seconds}с) — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="expired_checkpoint")

        # Восстановление состояния: "засеиваем" уже существующий
        # CheckpointManager, а не создаём параллельное хранилище.
        checkpoint.state.run_id = data.get("run_id", checkpoint.state.run_id)
        checkpoint.state.status = "running"
        checkpoint.state.current_page = int(data.get("current_page", 0))
        checkpoint.state.current_url = data.get("current_url")
        checkpoint.state.processed_count = int(data.get("processed_count", 0))
        checkpoint.state.exported_count = int(data.get("exported_count", 0))
        checkpoint.state.extra_metadata = dict(data.get("extra_metadata") or {})

        log_message(
            "info",
            f"ResumeManager: сессия восстановлена (страница={checkpoint.state.current_page}, "
            f"обработано={checkpoint.state.processed_count}, экспортировано={checkpoint.state.exported_count})",
        )

        return ResumeDecision(
            resumed=True,
            start_page=checkpoint.state.current_page,
            processed_count=checkpoint.state.processed_count,
            exported_count=checkpoint.state.exported_count,
            reason="resumed",
            checkpoint_data=data,
        )

    # =====================================================================
    # ВНУТРЕННЯЯ ЛОГИКА
    # =====================================================================

    @staticmethod
    def _validate(data: Dict[str, Any]) -> Optional[str]:
        """
        Проверяет наличие обязательных полей и базовую консистентность
        типов чекпоинта (см. TASK.md, "Error Handling" -> "incomplete
        checkpoint data" / "corrupted checkpoint").

        Returns:
            str, optional: Текст ошибки, если чекпоинт невалиден,
                либо None, если валиден.
        """
        if not isinstance(data, dict):
            return "чекпоинт не является объектом"

        missing = [field for field in _REQUIRED_FIELDS if field not in data]
        if missing:
            return f"отсутствуют обязательные поля: {', '.join(missing)}"

        if not isinstance(data.get("run_id"), str) or not data["run_id"]:
            return "поле run_id пустое или некорректного типа"

        if not isinstance(data.get("status"), str):
            return "поле status некорректного типа"

        try:
            int(data.get("current_page", 0))
        except (TypeError, ValueError):
            return "поле current_page некорректного типа"

        if not isinstance(data.get("timestamp"), str):
            return "поле timestamp некорректного типа"

        return None

    def _is_expired(self, data: Dict[str, Any]) -> bool:
        """
        Проверяет "возраст" чекпоинта относительно `max_age_seconds`.
        При `max_age_seconds == 0` возраст не ограничивается.
        """
        if self.max_age_seconds <= 0:
            return False

        try:
            checkpoint_time = datetime.fromisoformat(data["timestamp"])
            if checkpoint_time.tzinfo is None:
                checkpoint_time = checkpoint_time.replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            # Не удалось разобрать timestamp — считаем чекпоинт
            # невалидным для целей возраста, но это уже отловлено
            # в _validate() раньше в общем потоке resume().
            return True

        age_seconds = (datetime.now(timezone.utc) - checkpoint_time).total_seconds()
        return age_seconds > self.max_age_seconds


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    test_file = Path(tempfile.gettempdir()) / "resume_manager_selftest.json"
    test_file.unlink(missing_ok=True)

    print(f"[{__file__}] Тест ResumeManager (файл: {test_file})")

    # --- Сценарий 1: нет чекпоинта -> новая сессия ---
    checkpoint = CheckpointManager(run_id="selftest", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(checkpoint)
    print(f"  Без чекпоинта: resumed={decision.resumed}, reason={decision.reason}")
    assert decision.resumed is False

    # --- Симулируем прерванную сессию: 3 страницы обработаны, status=running ---
    checkpoint.start(status="running", site="example.com")
    checkpoint.record_page(page_number=3, processed_count=30, exported_count=30)

    # --- Сценарий 2: новый CheckpointManager (новый запуск процесса) -> восстановление ---
    fresh_checkpoint = CheckpointManager(run_id="selftest-new", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(fresh_checkpoint)
    print(
        f"  С чекпоинтом (running, стр.3): resumed={decision.resumed}, "
        f"start_page={decision.start_page}, exported={decision.exported_count}"
    )
    assert decision.resumed is True
    assert decision.start_page == 3

    # --- Сценарий 3: сессия завершена (completed) -> не восстанавливать ---
    fresh_checkpoint.finish(status="completed")
    another_checkpoint = CheckpointManager(run_id="selftest-completed", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(another_checkpoint)
    print(f"  С чекпоинтом (completed): resumed={decision.resumed}, reason={decision.reason}")
    assert decision.resumed is False
    assert decision.reason == "already_completed"

    test_file.unlink(missing_ok=True)
    print(f"[{__file__}] Все проверки пройдены успешно.")


--- app/retry_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retry Manager.

Единый компонент, отвечающий за повторные попытки при временных сбоях
HTTP-операций (сетевые ошибки, таймауты, HTTP 429/500/502/503/504).

Retry Manager:

* строит настроенный `requests.adapters.HTTPAdapter` на базе `urllib3.Retry`
  для автоматических повторов транспортного уровня (используется Session
  Manager при монтировании адаптера на сессию);
* предоставляет `call_with_retry()` — универсальную обертку с экспоненциальным
  backoff и опциональным джиттером для повтора произвольных вызовов, которые
  выбрасывают "временные" исключения (например, до создания HTTP-сессии);
* берет всю политику повторов (лимит попыток, backoff, retryable-статусы)
  из Configuration Manager (`app/config.py`) — без хардкода значений.

Retry Manager НЕ выполняет скрапинг, НЕ управляет куками/прокси/User-Agent
и НЕ вводит намеренные задержки между обычными запросами — паузы существуют
исключительно как часть повторной попытки после сбоя (Delay Manager будет
отвечать за паузы между успешными запросами).
"""

import random
import time
from typing import Any, Callable, Iterable, Tuple, Type

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app import config

# Исключения, которые считаются временными и подлежат повтору в call_with_retry.
DEFAULT_RETRYABLE_EXCEPTIONS: Tuple[Type[BaseException], ...] = (
    ConnectionError,
    TimeoutError,
)


class RetryManager:
    """
    Централизованная политика повторов для HTTP-операций фреймворка.
    """

    @staticmethod
    def build_retry_adapter(
        total: int = None,
        backoff_factor: float = None,
        status_forcelist: Iterable[int] = None,
    ) -> HTTPAdapter:
        """
        Создает `HTTPAdapter`, настроенный политикой повторов `urllib3.Retry`.

        Адаптер монтируется на `requests.Session` (см. Session Manager) и
        прозрачно повторяет запросы при сетевых сбоях и указанных HTTP-статусах,
        без необходимости оборачивать каждый вызов `session.get(...)` вручную.

        Args:
            total (int, optional): Максимальное количество повторов.
                По умолчанию — `config.RETRY_COUNT`.
            backoff_factor (float, optional): Множитель экспоненциальной
                задержки. По умолчанию — `config.RETRY_BACKOFF_FACTOR`.
            status_forcelist (Iterable[int], optional): HTTP-статусы,
                считающиеся временным сбоем. По умолчанию —
                `config.RETRYABLE_STATUS_CODES`.

        Returns:
            HTTPAdapter: Адаптер, готовый к монтированию через
                `session.mount("http://", adapter)` / `mount("https://", adapter)`.
        """
        retry_policy = Retry(
            total=total if total is not None else config.RETRY_COUNT,
            backoff_factor=backoff_factor if backoff_factor is not None else config.RETRY_BACKOFF_FACTOR,
            status_forcelist=list(status_forcelist) if status_forcelist is not None else config.RETRYABLE_STATUS_CODES,
            allowed_methods=None,  # повторяем для всех методов, включая POST
            raise_on_status=False,
        )
        return HTTPAdapter(max_retries=retry_policy)

    @staticmethod
    def apply_to_session(session, **overrides: Any) -> None:
        """
        Монтирует настроенный retry-адаптер на все схемы (`http://`, `https://`)
        переданной сессии. Используется Session Manager при создании сессии.

        Args:
            session (requests.Session): Сессия, на которую монтируется адаптер.
            **overrides: Необязательные переопределения для `build_retry_adapter`
                (`total`, `backoff_factor`, `status_forcelist`).
        """
        adapter = RetryManager.build_retry_adapter(**overrides)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    @staticmethod
    def call_with_retry(
        func: Callable[[], Any],
        retries: int = None,
        backoff_factor: float = None,
        jitter: bool = None,
        retryable_exceptions: Tuple[Type[BaseException], ...] = DEFAULT_RETRYABLE_EXCEPTIONS,
    ) -> Any:
        """
        Выполняет `func()` с повторными попытками при временных сбоях, используя
        экспоненциальный backoff и опциональный джиттер.

        Полезно для операций, не проходящих через `requests.Session`
        (например, точечных вызовов, где адаптер не применим).

        Args:
            func (Callable[[], Any]): Вызываемый без аргументов callable
                (используйте `functools.partial` или lambda для передачи аргументов).
            retries (int, optional): Максимум повторов. По умолчанию — `config.RETRY_COUNT`.
            backoff_factor (float, optional): Множитель задержки.
                По умолчанию — `config.RETRY_BACKOFF_FACTOR`.
            jitter (bool, optional): Добавлять случайный джиттер к задержке.
                По умолчанию — `config.RETRY_JITTER`.
            retryable_exceptions (Tuple[Type[BaseException], ...]): Классы
                исключений, при которых выполняется повтор.

        Returns:
            Any: Результат успешного вызова `func()`.

        Raises:
            BaseException: Последнее пойманное исключение, если все попытки исчерпаны.
        """
        max_retries = retries if retries is not None else config.RETRY_COUNT
        factor = backoff_factor if backoff_factor is not None else config.RETRY_BACKOFF_FACTOR
        use_jitter = jitter if jitter is not None else config.RETRY_JITTER

        last_exception: BaseException = None
        for attempt in range(1, max_retries + 2):  # +1 — первая (не повторная) попытка
            try:
                return func()
            except retryable_exceptions as e:
                last_exception = e
                if attempt > max_retries:
                    break

                delay = factor * (2 ** (attempt - 1))
                if use_jitter:
                    delay += random.uniform(0, factor)

                print(
                    f"[{__file__}] Попытка {attempt}/{max_retries} не удалась ({e}). "
                    f"Повтор через {delay:.2f}с..."
                )
                time.sleep(delay)

        raise last_exception


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import requests

    session = requests.Session()
    RetryManager.apply_to_session(session)
    print(f"[{__file__}] Retry-адаптер смонтирован на сессию (лимит={config.RETRY_COUNT}, "
          f"статусы={config.RETRYABLE_STATUS_CODES})")

    counter = {"attempts": 0}

    def flaky_call():
        counter["attempts"] += 1
        if counter["attempts"] < 3:
            raise ConnectionError("Симуляция временного сбоя сети")
        return "OK"

    result = RetryManager.call_with_retry(flaky_call, retries=3, backoff_factor=0.1)
    print(f"[{__file__}] Результат call_with_retry: {result} (попыток: {counter['attempts']})")


--- app/scraper.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scraper Module — сетевой слой для сбора HTML-контента.

Отвечает только за HTTP-запросы и получение HTML-кода страниц.
Не выполняет парсинг DOM — это задача parser.py.

Поток данных:
1. fetch_page_data() — точка входа из main.py
2. Загружает страницу категории
3. Извлекает URL первых двух товаров через parser.parse_listing()
4. Загружает страницы товаров
5. Возвращает [HTML категории, HTML товара1, HTML товара2]
"""

import time
from typing import List, Optional

import requests

from app.config import (
    TIMEOUT,
    RETRY_COUNT,
    RETRYABLE_STATUS_CODES,
    REQUESTS_VERIFY_SSL,
    REQUESTS_ALLOW_REDIRECTS,
    DEFAULT_USER_AGENT,
    DEFAULT_ACCEPT,
    DEFAULT_ACCEPT_LANGUAGE,
    DEFAULT_ACCEPT_ENCODING,
    DEFAULT_CONNECTION,
    DEFAULT_UPGRADE_INSECURE_REQUESTS,
    DEFAULT_SEC_FETCH_DEST,
    DEFAULT_SEC_FETCH_MODE,
    DEFAULT_SEC_FETCH_SITE,
    DEFAULT_DNT,
)
from app.utils import log_message, random_delay


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def _get_headers() -> dict:
    """
    Возвращает базовые HTTP-заголовки для имитации реального браузера.
    """
    return {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": DEFAULT_ACCEPT,
        "Accept-Language": DEFAULT_ACCEPT_LANGUAGE,
        "Accept-Encoding": DEFAULT_ACCEPT_ENCODING,
        "Connection": DEFAULT_CONNECTION,
        "Upgrade-Insecure-Requests": DEFAULT_UPGRADE_INSECURE_REQUESTS,
        "Sec-Fetch-Dest": DEFAULT_SEC_FETCH_DEST,
        "Sec-Fetch-Mode": DEFAULT_SEC_FETCH_MODE,
        "Sec-Fetch-Site": DEFAULT_SEC_FETCH_SITE,
        "DNT": DEFAULT_DNT,
    }


def _fetch_with_retry(url: str, headers: Optional[dict] = None) -> Optional[str]:
    """
    Выполняет HTTP GET-запрос с повторными попытками при временных сбоях.

    Args:
        url: Целевой URL.
        headers: Дополнительные заголовки (переопределяют базовые).

    Returns:
        HTML-код страницы или None при ошибке.
    """
    base_headers = _get_headers()
    if headers:
        base_headers.update(headers)

    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(
                url,
                headers=base_headers,
                timeout=TIMEOUT,
                verify=REQUESTS_VERIFY_SSL,
                allow_redirects=REQUESTS_ALLOW_REDIRECTS,
            )

            if response.status_code == 200:
                return response.text

            if response.status_code in RETRYABLE_STATUS_CODES:
                log_message(
                    "warning",
                    f"[{__file__}] Временная ошибка {response.status_code} для {url}, "
                    f"попытка {attempt + 1}/{RETRY_COUNT}"
                )
                random_delay(1.0, 3.0)
                continue

            log_message("error", f"[{__file__}] Ошибка {response.status_code} для {url}")
            return None

        except requests.exceptions.Timeout:
            log_message(
                "warning",
                f"[{__file__}] Таймаут для {url}, попытка {attempt + 1}/{RETRY_COUNT}"
            )
            random_delay(1.0, 3.0)
            continue

        except requests.exceptions.ConnectionError as e:
            log_message(
                "warning",
                f"[{__file__}] Ошибка соединения для {url}: {e}, "
                f"попытка {attempt + 1}/{RETRY_COUNT}"
            )
            random_delay(1.0, 3.0)
            continue

        except Exception as e:
            log_message("error", f"[{__file__}] Непредвиденная ошибка для {url}: {e}")
            return None

    log_message("error", f"[{__file__}] Не удалось получить {url} после {RETRY_COUNT} попыток")
    return None


# ============================================================================
# ПУБЛИЧНОЕ API
# ============================================================================

def fetch_page(url: str, headers: Optional[dict] = None) -> Optional[str]:
    """
    Загружает HTML-код страницы по URL.

    Args:
        url: URL для запроса.
        headers: Дополнительные заголовки.

    Returns:
        HTML-код страницы или None при ошибке.
    """
    log_message("debug", f"[{__file__}] Запрос: {url}")
    return _fetch_with_retry(url, headers)


def fetch_listing(category_url: str) -> Optional[str]:
    """
    Загружает HTML-код страницы категории.

    Args:
        category_url: URL страницы категории.

    Returns:
        HTML-код категории или None при ошибке.
    """
    log_message("info", f"[{__file__}] Загрузка категории: {category_url}")
    return fetch_page(category_url)


def fetch_product(product_url: str) -> Optional[str]:
    """
    Загружает HTML-код страницы товара.

    Args:
        product_url: URL страницы товара.

    Returns:
        HTML-код товара или None при ошибке.
    """
    log_message("debug", f"[{__file__}] Загрузка товара: {product_url}")
    return fetch_page(product_url)


def collect_product_urls(category_url: str, limit: int = 2) -> List[str]:
    """
    Загружает категорию и извлекает ссылки на товары.

    Args:
        category_url: URL страницы категории.
        limit: Максимальное количество ссылок.

    Returns:
        Список URL товаров (не более limit).
    """
    from app.parser import parse_listing  # локальный импорт, чтобы избежать циклической зависимости

    html = fetch_listing(category_url)
    if not html:
        log_message("error", f"[{__file__}] Не удалось загрузить категорию: {category_url}")
        return []

    urls = parse_listing(html)
    if limit and len(urls) > limit:
        urls = urls[:limit]

    log_message("info", f"[{__file__}] Найдено {len(urls)} URL товаров")
    return urls


def scrape_category(category_url: str, limit: int = 2) -> List[dict]:
    """
    Полный цикл: загружает категорию, извлекает URL товаров,
    загружает страницы товаров и передаёт их в парсер.

    Args:
        category_url: URL страницы категории.
        limit: Максимальное количество товаров.

    Returns:
        Список словарей с данными товаров.
    """
    from app.parser import parse_product  # локальный импорт

    log_message("info", f"[{__file__}] scrape_category: начало, limit={limit}")

    # 1. Загружаем категорию
    category_html = fetch_listing(category_url)
    if not category_html:
        log_message("error", f"[{__file__}] scrape_category: не удалось загрузить категорию")
        return []

    # 2. Извлекаем URL товаров (используем тот же HTML, что уже загрузили)
    from app.parser import parse_listing
    product_urls = parse_listing(category_html)
    if limit and len(product_urls) > limit:
        product_urls = product_urls[:limit]

    if not product_urls:
        log_message("error", f"[{__file__}] scrape_category: не найдено товаров в категории")
        return []

    # 3. Загружаем страницы товаров и парсим их
    results = []
    for idx, url in enumerate(product_urls, 1):
        log_message("debug", f"[{__file__}] scrape_category: загрузка товара {idx}/{len(product_urls)}")
        product_html = fetch_product(url)

        if product_html:
            try:
                product_data = parse_product(product_html, url)
                if product_data:
                    results.append(product_data)
                    log_message(
                        "debug",
                        f"[{__file__}] scrape_category: товар {idx} спарсен: "
                        f"{product_data.get('Title', 'N/A')}"
                    )
            except Exception as e:
                log_message("error", f"[{__file__}] scrape_category: ошибка парсинга {url}: {e}")
        else:
            log_message("error", f"[{__file__}] scrape_category: не удалось загрузить {url}")

        # Пауза между запросами товаров
        if idx < len(product_urls):
            random_delay(1.0, 2.0)

    log_message("info", f"[{__file__}] scrape_category: завершено, получено {len(results)} товаров")
    return results


def fetch_page_data(context=None) -> List[str]:
    """
    Главная точка входа для main.py.

    Загружает категорию, извлекает URL первых двух товаров,
    загружает их страницы и возвращает список HTML-кодов.

    Формат возврата:
        [HTML категории, HTML товара 1, HTML товара 2]

    Args:
        context: Игнорируется (совместимость с main.py).

    Returns:
        Список HTML-кодов страниц.
    """
    category_url = "https://www.professionele-koeling.nl/koelkasten-kisten.html"

    log_message("info", f"[{__file__}] fetch_page_data: начало")

    # 1. Загружаем категорию
    category_html = fetch_listing(category_url)
    if not category_html:
        log_message("error", f"[{__file__}] fetch_page_data: не удалось загрузить категорию")
        return []

    # 2. Извлекаем URL товаров
    from app.parser import parse_listing
    product_urls = parse_listing(category_html)
    product_urls = product_urls[:2]  # Только первые два

    if not product_urls:
        log_message("error", f"[{__file__}] fetch_page_data: не найдено товаров в категории")
        return []

    log_message("info", f"[{__file__}] fetch_page_data: найдено {len(product_urls)} товаров")

    # 3. Загружаем страницы товаров
    product_htmls = []
    for idx, url in enumerate(product_urls, 1):
        log_message("debug", f"[{__file__}] fetch_page_data: загрузка товара {idx}/{len(product_urls)}")
        html = fetch_product(url)
        if html:
            product_htmls.append(html)
        else:
            log_message("error", f"[{__file__}] fetch_page_data: не удалось загрузить {url}")

        if idx < len(product_urls):
            random_delay(1.0, 2.0)

    result = [category_html] + product_htmls
    log_message(
        "info",
        f"[{__file__}] fetch_page_data: завершено, получено {len(result)} страниц "
        f"(категория + {len(product_htmls)} товаров)"
    )
    return result


# ============================================================================
# ТЕСТОВЫЙ ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(f"[{__file__}] ТЕСТОВЫЙ ЗАПУСК SCRAPER")
    print("=" * 70)

    # Тест 1: fetch_page_data()
    print("\n--- Тест 1: fetch_page_data() ---")
    pages = fetch_page_data()
    print(f"Получено страниц: {len(pages)}")
    if pages:
        print(f"Категория: {len(pages[0])} символов")
        for i, html in enumerate(pages[1:], 1):
            print(f"Товар {i}: {len(html)} символов")

    print("\n" + "=" * 70)
    print(f"[{__file__}] Тест завершён")

--- app/session_manager.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session Manager.

Единая точка входа для создания и настройки `requests.Session`, а также
координатор HTTP-слоя фреймворка.

Архитектура HTTP-слоя (см. framework/ROADMAP.md, Milestone 2 и 3):

    Configuration Manager
            │
            ▼
    Request Profile Manager
            │
            ▼
    Session Manager
            │
     ┌──────┼────────┬────────┐
     ▼      ▼         ▼        ▼
    Cookie  Retry    Delay    Proxy
    Manager Manager  Manager  Manager

Session Manager — единственный компонент, который знает обо всех четырех
менеджерах (Cookie/Retry/Delay/Proxy) и координирует их вокруг сессии.

Важно: Cookie Manager, Retry Manager, Delay Manager и Proxy Manager
НЕ вызывают друг друга напрямую и ничего не знают друг о друге — каждый
зависит только от Configuration Manager. Это сохраняет их слабую
связанность и позволяет свободно добавлять новые компоненты
(Browser Manager) без риска затронуть уже существующие.

Session Manager:

* берет таймауты из Configuration Manager (`app/config.py`);
* берет браузерную идентичность из Request Profile Manager
  (`app/request_profile.py`) и применяет её заголовки к каждой новой сессии;
* делегирует куки — Cookie Manager, повторы — Retry Manager,
  задержки между запросами — Delay Manager, прокси — Proxy Manager
  (каждому — независимо от других);
* возвращает готовую к использованию сессию.

Session Manager НЕ реализует куки/повторы/задержки/прокси самостоятельно и
НЕ содержит логики скрапинга — вся реализация инкапсулирована в
соответствующих менеджерах.
"""

import requests

from app import config
from app.cookie_manager import CookieManager
from app.delay_manager import DelayManager
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile, RequestProfileManager
from app.retry_manager import RetryManager


class SessionManager:
    """
    Фабрика HTTP-сессий (`requests.Session`).

    Централизует создание сессий, чтобы вызывающий код никогда не создавал
    `requests.Session()` напрямую и не настраивал заголовки/куки/повторы вручную.
    """

    @staticmethod
    def create_session(
        profile: RequestProfile = None,
        load_cookies: bool = True,
        apply_retries: bool = True,
        apply_proxy: bool = True,
    ) -> requests.Session:
        """
        Создает новую `requests.Session`, настроенную выбранным профилем
        идентичности, таймаутом из конфигурации, куки из Cookie Manager,
        политикой повторов из Retry Manager и прокси из Proxy Manager.

        Args:
            profile (RequestProfile, optional): Профиль идентичности для
                применения к сессии. Если не передан, используется
                профиль по умолчанию (`RequestProfileManager.default_profile()`).
            load_cookies (bool): Если True (по умолчанию), сессия получает
                куки из Cookie Manager (`CookieManager.load()`).
            apply_retries (bool): Если True (по умолчанию), на сессию
                монтируется retry-адаптер из Retry Manager
                (`RetryManager.apply_to_session()`).
            apply_proxy (bool): Если True (по умолчанию), на сессию
                применяется прокси из Proxy Manager
                (`ProxyManager.apply_to_session()`). Если прокси не
                настроен (нет активного провайдера), сессия остается
                без изменений.

        Returns:
            requests.Session: Готовая к использованию HTTP-сессия с
                предустановленными заголовками, куки, повторами и прокси.
                Таймаут не хранится в самой сессии (`requests` не
                поддерживает это нативно) — используйте
                `SessionManager.timeout` при вызове
                `session.get(url, timeout=...)`.
        """
        session = requests.Session()

        active_profile = profile or RequestProfileManager.default_profile()
        session.headers.update(active_profile.to_headers())

        if load_cookies:
            CookieManager.apply_to_session(session)

        if apply_retries:
            RetryManager.apply_to_session(session)

        if apply_proxy:
            ProxyManager.apply_to_session(session)

        return session

    @staticmethod
    def wait_before_request(mode: str = None) -> None:
        """
        Выполняет паузу перед следующим запросом согласно политике
        Delay Manager (`DelayManager.wait()`).

        Это единая точка, через которую вызывающий код (будущие Requests
        Engine / Playwright Engine) может делать паузы между запросами,
        не импортируя Delay Manager напрямую — Session Manager выступает
        координатором HTTP-слоя, а сама логика задержки остается
        полностью в Delay Manager.

        Args:
            mode (str, optional): "fixed" или "random". По умолчанию —
                политика из `config.DELAY_MODE`.
        """
        DelayManager.wait(mode)

    # Таймаут запросов централизован в Configuration Manager.
    # Вызывающий код должен передавать его явно при выполнении запроса,
    # например: session.get(url, timeout=SessionManager.timeout)
    timeout: int = config.TIMEOUT


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    session = SessionManager.create_session()
    print(f"[{__file__}] Сессия создана. Заголовки:")
    for key, value in session.headers.items():
        print(f"  {key}: {value}")
    print(f"[{__file__}] Таймаут по умолчанию: {SessionManager.timeout}s")

    custom_profile = RequestProfileManager.create_profile(user_agent="TEST-UA/1.0")
    custom_session = SessionManager.create_session(profile=custom_profile)
    print(f"[{__file__}] Сессия с кастомным профилем, User-Agent: {custom_session.headers['User-Agent']}")


--- app/sticky_sessions.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sticky Sessions.

Централизованный компонент, отвечающий ТОЛЬКО за привязку одного прокси к
одной логической сессии (`session_id`), чтобы связанные запросы (один
скрапинг-джоб, одна сессия сайта, один авторизованный логин, одна сессия
браузера, одна сессия API) продолжали использовать один и тот же прокси.

Sticky Sessions:

* НЕ скачивает, НЕ валидирует и НЕ выбирает "лучший" прокси — выбор нового
  прокси для сессии всегда делегируется `ProxyManager` (который, в свою
  очередь, использует Proxy Selection/Proxy Rotation/Health Check);
* НЕ ротирует прокси самостоятельно — пока сессия активна и не истекла,
  прокси не меняется, независимо от активной политики Proxy Rotation;
* НЕ выполняет HTTP-запросы и НЕ содержит provider-specific логики;
* НЕ знает, откуда прокси взялся (Webshare/File Provider/Proxy Cache).

Интегрируется с:

* Configuration Manager (`app/config.py`) — вкл/выкл, тайм-аут сессии,
  лимит запросов на сессию и поведение при отказе прокси конфигурируются
  через `.env`, без правок кода;
* Proxy Manager (`app/proxy_manager.py`) — единственная точка входа,
  которая знает о Sticky Sessions. `ProxyManager.get_proxy(session_id=...)`
  сначала спрашивает `StickySessionManager.get_proxy()`, и только если
  привязки нет/она истекла — запрашивает новый прокси обычным способом
  (Proxy Rotation + Proxy Selection + Health Check) и привязывает его к
  сессии через `bind()`. Если `session_id` не передан — поведение Proxy
  Manager полностью прежнее (обратная совместимость);
* Proxy Health Check (`app/health_check.py`) — привязка считается
  истекшей, если прокси стал `DISABLED` (см. `_is_expired()`), а
  `ProxyManager.report_proxy_success()/report_proxy_failure()` с
  `session_id` обновляют пассивную статистику именно привязанного прокси;
* Proxy Rotation/Proxy Selection — косвенно: пока сессия активна, Sticky
  Sessions полностью перекрывает их вызов внутри `ProxyManager.get_proxy()`
  для данного `session_id`.

Состояние хранится в памяти (in-memory), без персистентности — аналогично
Proxy Selection/Rotation/Health Check, это осознанное упрощение для
текущей версии фреймворка (см. рекомендации в конце файла).
"""

import time
from dataclasses import dataclass
from typing import Dict, Optional, Set

from app import config


@dataclass
class StickySessionState:
    """Состояние одной привязки сессии к прокси."""

    proxy: str
    created_at: float
    last_used_at: float
    request_count: int = 0


class StickySessionManager:
    """
    Централизованная точка доступа к привязке прокси к логическим сессиям.

    Proxy Manager вызывает `get_proxy()`/`bind()` для получения/установки
    привязки, `report_failure()` — при сбое привязанного прокси, `release()`
    — при явном завершении сессии вызывающим кодом (Requests Engine,
    Playwright Engine, Login Support и т.д. — будущие компоненты).
    """

    _sessions: Dict[str, StickySessionState] = {}
    # Сессии, терминированные из-за отказа прокси при
    # `config.STICKY_SESSION_ON_FAILURE == "terminate"`. Хранится отдельно от
    # `_sessions`, чтобы вызывающий код мог отличить "сессии никогда не было"
    # от "сессия была явно закрыта из-за отказа" через `is_terminated()`.
    _terminated: Set[str] = set()

    @classmethod
    def is_enabled(cls) -> bool:
        """Включены ли Sticky Sessions согласно Configuration Manager."""
        return config.STICKY_SESSIONS_ENABLED

    @classmethod
    def _is_expired(cls, state: StickySessionState) -> bool:
        """
        Проверяет, истекла ли привязка сессии по любому из настраиваемых
        критериев (Session Expiration, см. TASK.md):

        * максимальная длительность сессии (`STICKY_SESSION_TIMEOUT_SECONDS`,
          0 — без ограничения по времени);
        * максимальное количество запросов
          (`STICKY_SESSION_MAX_REQUESTS`, 0 — без ограничения);
        * привязанный прокси стал непригоден для использования согласно
          Proxy Health Check (`HealthCheck.is_usable()` -> `False`, то есть
          прокси `DISABLED`) — это связывает Failure Handling с пассивным
          мониторингом здоровья без дублирования его логики здесь.
        """
        now = time.monotonic()

        if (
            config.STICKY_SESSION_TIMEOUT_SECONDS > 0
            and (now - state.created_at) >= config.STICKY_SESSION_TIMEOUT_SECONDS
        ):
            return True

        if (
            config.STICKY_SESSION_MAX_REQUESTS > 0
            and state.request_count >= config.STICKY_SESSION_MAX_REQUESTS
        ):
            return True

        from app.health_check import HealthCheck  # локальный импорт: избегаем циклической зависимости

        if not HealthCheck.is_usable(state.proxy):
            return True

        return False

    @classmethod
    def get_proxy(cls, session_id: str) -> Optional[str]:
        """
        Возвращает прокси, привязанный к сессии, если привязка существует
        и не истекла. Каждый вызов считается одним запросом в рамках
        сессии — увеличивает `request_count` и обновляет `last_used_at`.

        Если привязки нет или она истекла — истекшая привязка удаляется, и
        возвращается `None`. Вызывающий код (`ProxyManager.get_proxy()`)
        в этом случае должен запросить новый прокси обычным способом и
        вызвать `bind()`.

        Args:
            session_id (str): Идентификатор логической сессии.

        Returns:
            Optional[str]: Привязанный прокси, либо `None`.
        """
        state = cls._sessions.get(session_id)
        if state is None:
            return None

        if cls._is_expired(state):
            print(
                f"[{__file__}] Сессия '{session_id}' истекла "
                f"(запросов: {state.request_count}) — привязка снята."
            )
            cls._sessions.pop(session_id, None)
            return None

        state.request_count += 1
        state.last_used_at = time.monotonic()
        return state.proxy

    @classmethod
    def peek_proxy(cls, session_id: str) -> Optional[str]:
        """
        Возвращает привязанный прокси без побочных эффектов (не увеличивает
        `request_count`, не проверяет истечение). Используется Proxy
        Manager в `report_proxy_success()`/`report_proxy_failure()`, чтобы
        узнать, какой именно прокси обновлять в Health Check.

        Args:
            session_id (str): Идентификатор логической сессии.

        Returns:
            Optional[str]: Привязанный прокси, либо `None`, если привязки нет.
        """
        state = cls._sessions.get(session_id)
        return state.proxy if state is not None else None

    @classmethod
    def bind(cls, session_id: str, proxy: str) -> None:
        """
        Создает (или пересоздает) привязку сессии к прокси. Вызывается
        Proxy Manager сразу после того, как для сессии без активной
        привязки был выбран новый прокси обычным способом.

        Снимает возможную отметку "terminated" — новая привязка означает
        новый жизненный цикл сессии.

        Args:
            session_id (str): Идентификатор логической сессии.
            proxy (str): URL прокси для привязки.
        """
        now = time.monotonic()
        cls._sessions[session_id] = StickySessionState(
            proxy=proxy, created_at=now, last_used_at=now
        )
        cls._terminated.discard(session_id)

    @classmethod
    def release(cls, session_id: str, reason: str = "manual") -> None:
        """
        Явно завершает сессию и освобождает привязанный прокси
        (Explicit Session Termination).

        Args:
            session_id (str): Идентификатор логической сессии.
            reason (str): Причина завершения — попадает в лог
                (например, "manual", "job_finished").
        """
        state = cls._sessions.pop(session_id, None)
        if state is not None:
            print(f"[{__file__}] Сессия '{session_id}' завершена ({reason}).")

    @classmethod
    def report_failure(cls, session_id: str) -> None:
        """
        Реагирует на отказ прокси, привязанного к сессии (Failure Handling,
        см. TASK.md): освобождает текущую привязку и, в зависимости от
        `config.STICKY_SESSION_ON_FAILURE`, либо позволяет сессии
        продолжиться со свежим прокси при следующем вызове `get_proxy()`
        ("replace" — поведение по умолчанию), либо помечает сессию как
        терминированную ("terminate") — тогда вызывающий код должен начать
        новую логическую сессию (новый `session_id`).

        Сам метод не выбирает и не запрашивает новый прокси — это остается
        ответственностью Proxy Manager при следующем обращении с тем же
        `session_id`.

        Args:
            session_id (str): Идентификатор логической сессии, чей прокси отказал.
        """
        state = cls._sessions.pop(session_id, None)
        if state is None:
            return

        behavior = config.STICKY_SESSION_ON_FAILURE
        if behavior == "terminate":
            cls._terminated.add(session_id)
            print(
                f"[{__file__}] Сессия '{session_id}': прокси отказал — "
                f"сессия терминирована (STICKY_SESSION_ON_FAILURE=terminate)."
            )
        else:
            print(
                f"[{__file__}] Сессия '{session_id}': прокси отказал — "
                f"будет назначен новый прокси при следующем запросе "
                f"(STICKY_SESSION_ON_FAILURE=replace)."
            )

    @classmethod
    def is_terminated(cls, session_id: str) -> bool:
        """
        Была ли сессия терминирована из-за отказа прокси при
        `STICKY_SESSION_ON_FAILURE=terminate`.

        Позволяет будущему вызывающему коду (Requests Engine, Login
        Support) отличить "сессию нужно начать заново" от обычного
        отсутствия привязки.
        """
        return session_id in cls._terminated

    @classmethod
    def get_stats(cls, session_id: str) -> Optional[Dict[str, object]]:
        """Возвращает информацию о сессии для отладки/логирования, либо None."""
        state = cls._sessions.get(session_id)
        if state is None:
            return None
        return {
            "proxy": state.proxy,
            "created_at": state.created_at,
            "last_used_at": state.last_used_at,
            "request_count": state.request_count,
        }

    @classmethod
    def get_all_sessions(cls) -> Dict[str, StickySessionState]:
        """Возвращает все активные привязки (для отладки/логирования)."""
        return cls._sessions

    @classmethod
    def reset(cls, session_id: Optional[str] = None) -> None:
        """
        Сбрасывает состояние: для одной сессии (если указана) или полностью.

        Args:
            session_id (str, optional): Идентификатор сессии для сброса.
                Если `None`, сбрасывается всё (все привязки и отметки
                terminated).
        """
        if session_id is not None:
            cls._sessions.pop(session_id, None)
            cls._terminated.discard(session_id)
        else:
            cls._sessions.clear()
            cls._terminated.clear()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    session = "job-42"


    print(f"[{__file__}] Sticky Sessions включены: {StickySessionManager.is_enabled()}")
    print(f"[{__file__}] get_proxy() без привязки: {StickySessionManager.get_proxy(session)}")

    StickySessionManager.bind(session, "http://demo_user:demo_pass@10.0.0.1:8000")
    print(f"[{__file__}] После bind(): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] Повторный вызов (тот же прокси): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] Статистика сессии: {StickySessionManager.get_stats(session)}")

    print(f"[{__file__}] Симулируем отказ прокси (behavior=replace по умолчанию)...")
    StickySessionManager.report_failure(session)
    print(f"[{__file__}] После отказа, get_proxy(): {StickySessionManager.get_proxy(session)}")
    print(f"[{__file__}] is_terminated(): {StickySessionManager.is_terminated(session)}")

    StickySessionManager.bind(session, "http://2.2.2.2:2222")
    StickySessionManager.release(session, reason="job_finished")
    print(f"[{__file__}] После release(): {StickySessionManager.get_proxy(session)}")

    StickySessionManager.reset()


--- app/utils.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from datetime import datetime

def log_message(level: str, message: str) -> None:
    """
    Универсальный форматированный логгер для вывода в консоль.
    Заменяет тяжелые библиотеки логирования простым и понятным для ИИ кодом.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """
    Генерирует случайную паузу. Помогает имитировать поведение 
    реального пользователя и обходить базовые лимиты запросов (Rate Limiting).
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def clean_price(price_string: str) -> float:
    """
    Утилита очистки строки цены (например, '$1,299.99' или '150.00 €') 
    и конвертации её в чистое число с плавающей точкой (float).
    Очень частый запрос от клиентов на Upwork.
    """
    if not price_string:
        return 0.0
        
    try:
        # Удаляем все пробельные символы
        cleaned = re.sub(r"\s+", "", price_string)
        # Оставляем только цифры, точки и запятые
        cleaned = re.sub(r"[^\d.,]", "", cleaned)
        
        # Если в цене есть и точка, и запятая (например, 1,250.50)
        if "," in cleaned and "." in cleaned:
            # Если запятая идет первой, это разделитель тысяч (US стиль) -> просто убираем её
            if cleaned.find(",") < cleaned.find("."):
                cleaned = cleaned.replace(",", "")
            # Если точка идет первой (EU стиль, например, 1.250,50) -> убираем точку, запятую меняем на точку
            else:
                cleaned = cleaned.replace(".", "").replace(",", ".")
        # Если есть только запятая (EU стиль без копеек или с копейками через запятую: '150,50')
        elif "," in cleaned and "." not in cleaned:
            cleaned = cleaned.replace(",", ".")
            
        return float(cleaned)
    except Exception:
        # Если очистить не удалось, возвращаем 0.0, чтобы скрипт не падал
        return 0.0


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тест утилит:")
    
    log_message("info", "Запуск теста очистки цен...")
    
    # Тестируем разные форматы валют, которые могут прилететь с сайтов
    prices_to_test = ["$1,249.99", "350,00 €", " 1.500,75 руб ", "99"]
    
    for p in prices_to_test:
        print(f"  Исходная: {p:<15} -> Результат: {clean_price(p)}")

--- app/webshare_proxy_provider.py ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Webshare Proxy Provider.

Реализация `ProxyProvider` (см. `app/proxy_manager.py`), получающая список
прокси из официального Webshare Proxy List API
(https://proxy.webshare.io/api/v2/proxy/list/).

Как и `FileProxyProvider` (`app/file_proxy_provider.py`), этот модуль
подтверждает провайдер-независимость Proxy Manager: Proxy Manager работает
с `WebshareProxyProvider` через тот же интерфейс `ProxyProvider`, не зная
ничего об API Webshare, аутентификации или формате его ответа.

Webshare Proxy Provider:

* аутентифицируется через API-ключ (`config.WEBSHARE_API_KEY`), который
  берется ИСКЛЮЧИТЕЛЬНО из Configuration Manager (переменные окружения /
  .env) — ключ никогда не хардкодится и не появляется в логах;
* нормализует ответ API в тот же формат URL-строк
  (`http://[user:pass@]host:port`), который использует File Provider —
  Proxy Manager получает данные в едином виде независимо от источника;
* кэширует загруженный список прокси в памяти на `config.WEBSHARE_CACHE_TTL_SECONDS`
  секунд, чтобы не дергать API при каждом обращении (`get_proxy()`) и не
  упереться в rate limit;
* корректно обрабатывает сетевые ошибки, таймауты, невалидный API-ключ,
  HTTP 401/403/429, а также некорректный/пустой ответ API — во всех
  случаях возвращает пустой список вместо падения приложения.

Webshare Proxy Provider НЕ выбирает и НЕ ротирует прокси из списка, НЕ
валидирует их и НЕ проверяет здоровье, НЕ выполняет retry-логику (это
ответственность Retry Manager, а не провайдера) и ничего не знает о других
провайдерах (File Provider, BrightData и т.д.).
"""

import time
from typing import Any, Dict, List, Optional

import requests

from app import config
from app.proxy_manager import ProxyProvider


class WebshareProxyProvider(ProxyProvider):
    """
    Провайдер, получающий список прокси из Webshare Proxy List API.

    Хранит нормализованный список прокси в памяти и обновляет его не
    чаще, чем раз в `cache_ttl_seconds` — простой TTL-кэш без внешних
    зависимостей (БД/Redis не требуются для этой задачи).
    """

    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        cache_ttl_seconds: int = None,
        timeout: int = None,
    ):
        """
        Args:
            api_key (str, optional): API-ключ Webshare. По умолчанию —
                `config.WEBSHARE_API_KEY` (переменная окружения `WEBSHARE_API_KEY`).
            api_url (str, optional): URL Webshare Proxy List API.
                По умолчанию — `config.WEBSHARE_API_URL`.
            cache_ttl_seconds (int, optional): Время жизни кэша в секундах.
                По умолчанию — `config.WEBSHARE_CACHE_TTL_SECONDS`.
            timeout (int, optional): Таймаут HTTP-запроса к API (секунды).
                По умолчанию — `config.WEBSHARE_API_TIMEOUT`.
        """
        self.api_key = api_key if api_key is not None else config.WEBSHARE_API_KEY
        self.api_url = api_url or config.WEBSHARE_API_URL
        self.cache_ttl_seconds = (
            cache_ttl_seconds if cache_ttl_seconds is not None else config.WEBSHARE_CACHE_TTL_SECONDS
        )
        self.timeout = timeout if timeout is not None else config.WEBSHARE_API_TIMEOUT

        self._proxies: List[str] = []
        self._last_fetched_at: float = 0.0

    def _is_cache_valid(self) -> bool:
        """Проверяет, не истек ли TTL текущего закэшированного списка прокси."""
        if not self._proxies:
            return False
        return (time.time() - self._last_fetched_at) < self.cache_ttl_seconds

    @staticmethod
    def _normalize_entry(entry: Dict[str, Any]) -> Optional[str]:
        """
        Приводит одну запись прокси из ответа Webshare API к единому
        формату URL (`http://[user:pass@]host:port`), совпадающему с
        форматом File Provider.

        Webshare возвращает записи вида:
            {
                "proxy_address": "1.2.3.4",
                "port": 8080,
                "username": "user",
                "password": "pass",
                ...
            }

        Args:
            entry (Dict[str, Any]): Одна запись из `results` ответа API.

        Returns:
            Optional[str]: Нормализованный URL прокси, либо `None`, если
                запись не содержит обязательных полей `proxy_address`/`port`.
        """
        host = entry.get("proxy_address")
        port = entry.get("port")
        if not host or not port:
            return None

        username = entry.get("username")
        password = entry.get("password")
        if username and password:
            return f"http://{username}:{password}@{host}:{port}"
        return f"http://{host}:{port}"

    def _fetch_from_api(self) -> List[str]:
        """
        Выполняет запрос к Webshare Proxy List API и нормализует ответ.

        Обрабатывает все ожидаемые сбои (нет ключа, сетевые ошибки,
        таймаут, неавторизован, rate limit, невалидный JSON) без падения
        приложения — во всех случаях возвращает пустой список с понятным
        сообщением в лог. API-ключ никогда не попадает в лог.

        Returns:
            List[str]: Нормализованный список прокси (пустой при любой ошибке).
        """
        if not self.api_key:
            print(f"[{__file__}] Ошибка: WEBSHARE_API_KEY не задан в конфигурации "
                  f"(Configuration Manager) — запрос к Webshare API не выполнен.")
            return []

        headers = {"Authorization": f"Token {self.api_key}"}
        # Webshare Proxy List API v2 требует обязательный query-параметр "mode".
        # "direct" — прямое подключение к прокси (стандартный режим для большинства планов).
        params = {"mode": "direct", "page_size": 100}

        try:
            response = requests.get(self.api_url, headers=headers, params=params, timeout=self.timeout)

        except requests.exceptions.Timeout:
            print(f"[{__file__}] Ошибка: превышен таймаут запроса к Webshare API "
                  f"({self.timeout}с).")
            return []
        except requests.exceptions.ConnectionError as e:
            print(f"[{__file__}] Ошибка сети при запросе к Webshare API: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[{__file__}] Непредвиденная ошибка запроса к Webshare API: {e}")
            return []

        if response.status_code in (401, 403):
            print(f"[{__file__}] Ошибка авторизации Webshare API "
                  f"(HTTP {response.status_code}): проверьте WEBSHARE_API_KEY.")
            return []

        if response.status_code == 429:
            print(f"[{__file__}] Webshare API вернул HTTP 429 (превышен лимит запросов). "
                  f"Попробуйте позже или увеличьте WEBSHARE_CACHE_TTL_SECONDS.")
            return []

        if response.status_code != 200:
            print(f"[{__file__}] Webshare API вернул неожиданный статус "
                  f"HTTP {response.status_code}: {response.text[:200]}")
            return []

        try:
            payload = response.json()
        except ValueError as e:
            print(f"[{__file__}] Ошибка: невалидный JSON в ответе Webshare API: {e}")
            return []

        results = payload.get("results")
        if not isinstance(results, list):
            print(f"[{__file__}] Ошибка: неожиданный формат ответа Webshare API "
                  f"(отсутствует список 'results').")
            return []

        proxies: List[str] = []
        for entry in results:
            normalized = self._normalize_entry(entry) if isinstance(entry, dict) else None
            if normalized:
                proxies.append(normalized)

        if not proxies:
            print(f"[{__file__}] Предупреждение: Webshare API вернул пустой список прокси.")

        print(f"[{__file__}] Загружено прокси из Webshare API: {len(proxies)}")
        return proxies

    def _ensure_fresh(self) -> None:
        """Обновляет кэш прокси из API, если TTL истек или кэш пуст."""
        if self._is_cache_valid():
            return

        self._proxies = self._fetch_from_api()
        self._last_fetched_at = time.time()

    def get_proxy(self) -> Optional[str]:
        """
        Возвращает первый прокси из (при необходимости обновленного) кэша,
        либо `None`, если список пуст или запрос к API не удался.
        """
        self._ensure_fresh()
        return self._proxies[0] if self._proxies else None

    def get_all_proxies(self) -> List[str]:
        """
        Возвращает полный закэшированный список прокси (обновляя кэш при
        необходимости). Полезно для будущего Proxy Rotation.

        Returns:
            List[str]: Список нормализованных URL прокси.
        """
        self._ensure_fresh()
        return list(self._proxies)

    def reload(self) -> List[str]:
        """
        Принудительно обновляет список прокси из API, игнорируя TTL кэша.

        Returns:
            List[str]: Обновленный список загруженных прокси.
        """
        self._proxies = self._fetch_from_api()
        self._last_fetched_at = time.time()
        return list(self._proxies)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    from app.proxy_manager import ProxyManager

    provider = WebshareProxyProvider()
    print(f"[{__file__}] Webshare API URL: {provider.api_url}")
    print(f"[{__file__}] API-ключ задан: {bool(provider.api_key)}")
    print(f"[{__file__}] Все загруженные прокси: {provider.get_all_proxies()}")
    print(f"[{__file__}] Активный прокси (get_proxy): {provider.get_proxy()}")

    # Демонстрация интеграции с Proxy Manager без изменения его кода/API —
    # тот же паттерн, что и для FileProxyProvider.
    ProxyManager.set_provider(provider)
    print(f"[{__file__}] ProxyManager.get_proxy() после смены провайдера: {ProxyManager.get_proxy()}")
    print(f"[{__file__}] ProxyManager.to_requests_dict(): {ProxyManager.to_requests_dict()}")


---

# ОШИБКА / TRACEBACK

(Ни traceback, ни лог выполнения не найдены.
 Сохрани вывод консоли в AI_INPUT/log.txt или реальный traceback в AI_INPUT/traceback.txt перед запуском debug.)

---

# ЗАДАЧА

1. **Диагноз** — что именно сломалось и почему (2–5 предложений).
2. **Исправление** — покажи только изменённые файлы с полным содержимым.
3. **Проверка** — как убедиться, что исправление работает.

## Ограничения

- Меняй **только** файлы, где реальная ошибка.
- Не рефактори код «заодно».
- Не меняй `main.py`, `config.py`, `exporter.py`, `browser.py`, `utils.py` без крайней необходимости.
- Не добавляй новые зависимости без объяснения.

## Типичные причины

- Неверный CSS-селектор (сайт изменил разметку)
- Timeout (страница грузится дольше ожидаемого)
- Cloudflare / 403
- Пустой ответ API
- Неверный формат cookies.json
- Playwright: элемент не найден / не кликабелен

---

# ФОРМАТ ОТВЕТА

### Диагноз
...

### Исправление

```python
# app/scraper.py (или другой файл) — полный исправленный код
```

### Как проверить
...
