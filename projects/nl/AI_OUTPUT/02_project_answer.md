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