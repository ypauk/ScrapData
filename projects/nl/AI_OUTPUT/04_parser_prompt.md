# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/parser.py`.

Не меняй другие файлы. Не создавай новые папки.

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

# КОНТЕКСТ ПРОЕКТА

## Анализ (этап 1)

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

## План проекта (этап 2)

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

## Данные клиента



--- ФАЙЛ: description.txt ---
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

example.json -содержит ожидаемую структуру ,нужно получить результат 2 продуктов в csv

Нужно собрать только категорию koelkasten-kisten или весь сайт? - сначала только 2 продуктов в csv
Нужно ли обходить все страницы пагинации?- - сначала только 2 продуктов в csv из одной категории
В каком формате нужен результат (JSON, CSV, Excel)? - CSV
Нужно ли скачивать изображения или достаточно ссылок? - ссылка
Если изображений несколько — сохранить все? - 1 
Нужно ли разворачивать характеристики (Specs) в отдельные колонки? - да 
Да будут отдельно колонки Merk, Kleur, Breedte ... и надо их брать значения Polar, Zwart.. Нмже подробнее
Merk	Polar
Kleur	Zwart
Breedte	400-500mm
Diepte	400-500mm
Hoogte	450-550mm
Inhoud	20-30 liter
Temperatuurbereik	+4 ºC / +8 ºC
Vermogen	Nee


Нужно ли собирать товары, которых нет в наличии? - нужно
Нужно ли сохранять HTML-разметку описания или только чистый текст? - чистый текст
Требуется ли регулярный запуск или это разовая выгрузка? - разовая

--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: example.json ---

 {
  "URL": "https:\/\/www.professionele-koeling.nl\/koelkasten-kisten.html",
  "Breadcrumb": "Home",
  "Title ": "Polar GE579",
  "Short description": "De Polar GE579 is een zwarte minibar koelkast met\n29 liter inhoud voor gebruik in hotelkamers, B&B's of ver-\ngaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken.",
  "imageurl": "if multipli seperated by comma",
  "image_name": "if multiple seperated by comma",
  "Price": 259,
  "Sale price": 229,
  "Description ": "Polar GE579: Zwarte 30 liter minibar koelkast voor de hotelkamer\nDe Polar GE579 is een zwarte minibar koelkast met een capaciteit van 29 liter. Deze koelkast maakt gebruik van het absorptie\nkoelsysteem i.p.v. een compressor. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor\ntoepassingen in hotelkamers, B&B 's en vergaderzalen.\n\nUitvoering:\n\nExterieur: zwaart\nInterieur: roestvrijstaal\nWerking: Werkt met warmtepomp in plaats van ventilatoren\nVerwisselbare en afsluitbare deur\nVerlichting: LED\nRoosters (2x)\nVrijwel geruisloos\nVrijstaand of inbouw\nAbsorptie koelsysteem\nAutomatische ontdooiing\nSpecificaties:\n\nArtikelnummer: GE579\nInhoud: 29 liter\nTemperatuurbereik:  3-5°C bij een omgevingstemperatuur van 16°C\nTemperatuurbereik: 5-8°C bij een omgevingstemperatuur van 25°C\nTemperatuurbereik: 8-12°C bij een omgevingstemperatuur van 32°C\nAfmetingen BxDxH: 400 x 430 x 530 mm\nEnergieklasse: F\nAansluitwaarde: 220-240 Volt, 60 watt\nKlimaatklasse: N (omgevingstemperatuur tussen +16°C en +32°)\nKoelmiddel: R600a\nGewicht: 13 kg\nBij het absorptiesysteem, dat geheel zonder bewegende delen kan worden uitgevoerd, wordt gebruik gemaakt van het verschijnsel dat sommige vloeistoffen (bijvoorbeeld water) sommige koelmiddelen (bijvoorbeeld ammoniak) bij lage temperatuur absorberen en bij hogere weer afgeven. De in het vrieslichaam ontstane damp van het koelmiddel wordt door de absorberende vloeistof opgenomen in een absorptievat, waar de aanvankelijk verdunde oplossing tot een geconcentreerde wordt verdicht. Deze laatste oplossing komt in een ruimte waar het koelmiddel door een gasvlam of een andere dan gasvormige warmtebron uit de vloeistof wordt verdreven. Het koelmiddel wordt vervolgens in een condensor gekoeld en gecondenseerd en treedt daarna in het vrieslichaam, waarmee de kringloop gesloten is. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor toepassingen in hotelkamers en vergaderzalen.\n\nGebruikertips:\nDe kast kan de temperatuur bij normaal gebruik ca. 15 graden terug koelen.\nMen moet zich bij inbouw aan de inbouwvoorschriften houden.\nAls dit niet gebeurd en de kast draait in zijn eigen warmte, dan kan deze niet naar behoren functioneren.",
  "Specs": "https:\/\/www.awesomescreenshot.com\/image\/62286448?key=8b032d4304d185282fd860cfb3c858bb each own colom",
  "Spec_detail": "evertything before the : is the header "
 },
 {
  "Breadcrumb": "Koelkasten&Kisten"
 }


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---


--- ФАЙЛ: page.html ---
На странице https://www.professionele-koeling.nl/koelkasten-kisten.html есть список товаров

<li class="item" style="height: 383.012px; padding-bottom: 75px;">
            
                <div class="product-image-wrapper" style="max-width:295px;">
                
                    <a href="https://www.professionele-koeling.nl/diamond-img15s-a1.html" title="Diamond IMG15/S-A1" class="product-image">
                        <img id="product-collection-image-1210" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/d/i/diamond_img15_s_a1_wandkoelmeubel_1500mm_met_glazen_schuifdeuren.jpg" alt="Diamond IMG15/S-A1">

                        
                                            </a>
                
                    <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover" style="display: none; opacity: 0.940681;">
			<li><a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/1210/form_key/p8EcxN2r4x0ikJzf/" title="Zet op verlanglijst">
					<span class="2 icon ib ic ic-heart"></span>
			</a></li>
			<li><a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/1210/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw_cD00Mw,,/form_key/p8EcxN2r4x0ikJzf/" title="Voeg toe aan productvergelijking">
					<span class="2 icon ib ic ic-compare"></span>
			</a></li></ul>                
                </div> <!-- end: product-image-wrapper -->

                                    <h2 class="product-name"><a href="https://www.professionele-koeling.nl/diamond-img15s-a1.html" title="Diamond IMG15/S-A1">Diamond IMG15/S-A1</a></h2>
                
                                
                                
                                    

                        
    <div class="price-box">
                                            
                    <p class="old-price">
                <span class="price-label">Van:</span>
                <span class="price" id="old-price-1210">
                    €&nbsp;4.607,00                </span>
            </p>

                            <p class="special-price">
                    <span class="price-label">Voor</span>
                <span class="price" id="product-price-1210">
                    €&nbsp;3.289,00                </span>
                        <span class="label">Excl. BTW</span>
                </p>
                    
    
        </div>

                
                
                <div class="actions clearer" style="padding-left: 49.8687px; bottom: 30px;">

                    
                                                    <button type="button" title="In winkelwagen" class="button btn-cart" onclick="setLocation('https://www.professionele-koeling.nl/checkout/cart/add/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw_cD00Mw,,/product/1210/form_key/p8EcxN2r4x0ikJzf/')"><span><span>In winkelwagen</span></span></button>
                        
                                        
                                    </div> <!-- end: actions -->
            </li>



Также страница товара:
<div class="inner-container">
                    <div class="breadcrumbs">
    <ul>
                                    <li class="home" itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb">
                    <a href="https://www.professionele-koeling.nl/" title="Ga naar Home" itemprop="url"><span itemprop="title">Home</span></a>
            
                                <span class="sep"></span>
                                
                </li>
                                    <li class="category3" itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb">
                    <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html" title="" itemprop="url"><span itemprop="title">Koelkasten&amp;Kisten</span></a>
            
                                <span class="sep"></span>
                                
                </li>
                                    <li class="product">
                    <span class="last-crumb">Polar DM071</span>
            
                                
                </li>
            </ul>
</div>
                    <div class="preface"></div>
                    <div class="col-main">
                                                
<script type="text/javascript">
	var optionsPrice = new Product.OptionsPrice([]);
</script>
<div id="messages_product_view"></div>
<div class="product-view nested-container" itemscope="" itemtype="http://schema.org/Product">

	<form action="https://www.professionele-koeling.nl/checkout/cart/add/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuL3BvbGFyLWRtMDcxLmh0bWw_X19fU0lEPVU,/product/212/form_key/TIOaSPgIeleEQ6nQ/" method="post" id="product_addtocart_form">

		<input name="form_key" type="hidden" value="TIOaSPgIeleEQ6nQ">
		<div class="no-display">
			<input type="hidden" name="product" value="212">
			<input type="hidden" name="related_product" id="related-products-field" value="">
		</div>

		<div class="product-img-column grid12-4">

			



<div class="img-box img-box-style1">


        
                
        <p class="product-image zoom-inside" style="max-width: 363px;">
        
            <div id="wrap" style="top:0px;z-index:9999;position:relative;"><a href="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" class="cloud-zoom product-image-gallery" id="zoom1" rel="position:'inside',showTitle:false,lensOpacity:0.5,smoothMove:3,zoomWidth:427,zoomHeight:275,adjustX:0,adjustY:0" style="position: relative; display: block;">

                <img id="image-main" class="gallery-image visible" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/363x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" alt="Polar DM071" title="Polar DM071" itemprop="image" style="display: block;">
            </a><div class="mousetrap" style="background-image: url(&quot;data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7&quot;); width: 363px; height: 363px; top: 0px; left: 0px; position: absolute; z-index: 9999; cursor: move;"></div></div>
            
                                            <a id="zoom-btn" class="lightbox-group zoom-btn-small cboxElement" href="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" title="Polar DM071">Zoom</a>
                
                    </p>
    
    



</div> <!-- end: img-box -->



		<script type="text/javascript">
        jQuery(function($) {

        	//Zoom button for main image
        	$zoomButton = $("#zoom-btn");
            
            //Init lightbox
            $(".lightbox-group").colorbox({
			                rel:		'lightbox-group',
			                opacity:	0.5,
                speed:		300,
                current:	'image {current} of {total}',
                previous: '',
                next: '',
                close: '' //No comma here
				, maxWidth:'95%', maxHeight:'95%'			});
			
			//Product thumbnails - remove first one from gallery, it's already included in gallery by "zoom" button
							$(".cloud-zoom-gallery").first().removeClass("cboxElement");
						
			//Remove clicked thumbnail from gallery, it's already included in gallery by "zoom" button
			$(".cloud-zoom-gallery").click(function() {
				$zoomButton
					.attr('href', $(this).attr('href'))
					.attr('title', $(this).attr('title'));
			
									//First add gallery class to all thumbnails
					$(".cloud-zoom-gallery").each(function() {
						$(this).addClass("cboxElement");
					});
					$(this).removeClass("cboxElement");
							});

			//On image change
			$(document).on('product-media-manager-image-updated', function(e, data) {

				var img = data.img;

				//Add new image's URL to the zoom button's href attribute
				$zoomButton.attr('href', img.attr('src'));
				$zoomButton.attr('title', '');

									$(".cloud-zoom-gallery").each(function() {
						$(this).addClass("cboxElement");
					});
				
			}); //end: on event
            
        });
    </script>

<script type="text/javascript">
//<![CDATA[

    jQuery(function($) {

        var $cz = $('.cloud-zoom');
        var czInstance = $('.cloud-zoom').data('zoom');

        //On image change
        $(document).on('product-media-manager-image-updated', function(e, data) {

            var img = data.img;

            czInstance.destroy();

            //Add new image's URL to the CloudZoom element's href attribute
            $cz.attr('href', img.attr('src'));

            //Remove mousetrap
            var $mt = $('.mousetrap');
            $mt.unbind();
            $mt.remove();
            $mt = null;

            //Reinitialize CloudZoom
            $cz.CloudZoom();

        }); //end: on event

        //On resize
        var t;
        $(window).resize(function() {
            clearTimeout(t); 
            t = setTimeout(function() {

                czInstance.destroy();

                //Remove mousetrap and other elements
                var $mt = $('.mousetrap');
                $mt.unbind();
                $mt.remove();
                $mt = null;
                $('.cloud-zoom-lens').remove();
                $('#cloud-zoom-big').remove();

                //Reinitialize CloudZoom
                $cz.CloudZoom();

            }, 200);
        });

    
    });
//]]>
</script>

						
		</div>
		
		<div class="product-primary-column product-shop grid12-5">

			<div class="product-name">
				<h1 itemprop="name">Polar DM071</h1>
			</div>
			
			    <div class="ratings no-rating">
        <div class="rating-box">
            <div class="rating" style="width:0%"></div>
        </div>
        <p class="rating-links">
            <a id="goto-reviews-form" href="#review-form">Schrijf de eerste review over dit product</a>
        </p>
    </div>

							<div class="short-description"><div class="std" itemprop="description"><p>De Polar DM071 is een klein tafelmodel glasdeurkoelkast in witte uitvoering. <br>Deze voordelige compacte koeler heeft 46 liter capaciteit en weegt maar 18 kilo.</p><br>
<h4 style="color: blue;"><span style="background-color: yellow;">Advies nodig, of meerdere stuks tegen de scherpste prijs?<br>Bel onze specialisten: <strong>036 5363782</strong></span></h4><br>
<p>&nbsp;</p><br>
<p>&nbsp;</p></div></div>
			
			
			
											<meta itemprop="productID" content="sku: DM071">			
						
			
			<div itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
				<div class="product-type-data">
		    <p class="availability in-stock">Beschikbaarheid: <span>Op voorraad</span></p>
	    <meta itemprop="availability" content="http://schema.org/InStock">
	

                        
    <div class="price-box">
                                            
                    <p class="old-price">
                <span class="price-label">Van:</span>
                <span class="price" id="old-price-212">
                    €&nbsp;179,00                </span>
            </p>

                            <p class="special-price">
                    <span class="price-label">Voor</span>
                <span class="price" id="product-price-212">
                    €&nbsp;175,00                </span>
                        <span class="label">Excl. BTW</span>
                </p>
                    
    
        </div>

</div>
				
				<meta itemprop="priceCurrency" content="EUR"><meta itemprop="price" content="175">			</div> 
												<div class="add-to-box s">
						    <div class="add-to-cart left-side">
                    <div class="qty-wrapper">
                <label for="qty">Aantal:</label>
                <input type="text" name="qty" id="qty" maxlength="12" value="1" title="Aantal" class="input-text qty">
            </div>
                <button type="button" title="In winkelwagen" id="product-addtocart-button" class="button btn-cart" onclick="productAddToCartForm.submit(this)"><span><span>In winkelwagen</span></span></button>
    </div>
    <div class="paypal-wrapper"></div>
					</div>
					<div class="product-benefits">
						<ul>
							<li>Levering in de Benelux</li>
							<li>Zakelijk op rekening kopen</li>
							<li>2 jaar garantie</li>
							<li>Deskundig advies</li>
							<li>Officieel dealer van topmerken</li>
						</ul>
					</div>
											
						
							<div class="action-box clearer">
					<ul class="add-to-links">

	<li>
        <a class="link-wishlist feature feature-icon-hover first" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/TIOaSPgIeleEQ6nQ/" onclick="productAddToCartForm.submitLight(this, this.href); return false;" title="Zet op verlanglijst">
			<span class="ic ic-heart ib icon-color-productview"></span>
			<span class="label">Zet op verlanglijst</span>
		</a>
	</li>


	<li>
        <a class="link-compare feature feature-icon-hover first" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuL3BvbGFyLWRtMDcxLmh0bWw,/form_key/TIOaSPgIeleEQ6nQ/" title="Voeg toe aan productvergelijking">
			<span class="ic ic-compare ib icon-color-productview"></span>
			<span class="label">Voeg toe aan productvergelijking</span>
		</a>
	</li>


	<li>
    	<a class="link-share feature feature-icon-hover first" href="https://www.professionele-koeling.nl/sendfriend/product/send/id/212/cat_id/3/" title="E-mail naar een vriend">
			<span class="ic ic-share ib icon-color-productview"></span>
			<span class="label">E-mail naar een vriend</span>
		</a>
	</li>

</ul>				</div>
			
			
			
			
		</div> <!-- end: product-shop -->
		
		
			<div class="product-secondary-column grid12-3 custom-sidebar-right">
				<div class="inner">

					
					
											<div class="feature-wrapper bottom-border">			
				
			<div class="box-brand">
									<a class="fade-on-hover" href="https://www.professionele-koeling.nl/catalogsearch/result/?q=Polar" title="Click to see more products from Polar"><img src="https://www.professionele-koeling.nl/media/wysiwyg/infortis/brands/polar.png" alt="Polar"></a>
								<meta itemprop="brand" content="Polar">
			</div>
		
			</div>
					
					
					<div class="container_product_secondary_2 std block_product_secondary_bottom"><p><strong>Let op:</strong></p>
<ul>
<li>Betreft het grote aantallen?</li>
<li>Is het orderbedrag hoger dan € 1500,-?</li>
</ul>
<p><strong><a class="fancybox" href="https://www.professionele-koeling.nl/offerte">Vraag dan een offerte aan</a></strong></p></div>
					
				</div>
			</div> <!-- end: product-secondary-column -->

		
		
	</form>
	<script type="text/javascript">
	//<![CDATA[
		var productAddToCartForm = new VarienForm('product_addtocart_form');
		productAddToCartForm.submit = function(button, url) {
			if (this.validator.validate()) {
				var form = this.form;
				var oldUrl = form.action;

				if (url) {
				   form.action = url;
				}
				var e = null;
				try {
					this.form.submit();
				} catch (e) {
				}
				this.form.action = oldUrl;
				if (e) {
					throw e;
				}

				if (button && button != 'undefined') {
					button.disabled = true;
				}
			}
		}.bind(productAddToCartForm);

		productAddToCartForm.submitLight = function(button, url){
			if(this.validator) {
				var nv = Validation.methods;
				delete Validation.methods['required-entry'];
				delete Validation.methods['validate-one-required'];
				delete Validation.methods['validate-one-required-by-name'];
				if (this.validator.validate()) {
					if (url) {
						this.form.action = url;
					}
					this.form.submit();
				}
				Object.extend(Validation.methods, nv);
			}
		}.bind(productAddToCartForm);
	//]]>
	</script>

		<div class="box-additional grid12-9">

		<div class="box-collateral collateral-container box-tabs">

    
                            

        <div id="product-tabs" class="gen-tabs gen-tabs--style1">

        <ul class="tabs clearer">
                                                <li id="tab-description"><a href="#" class="current">Productbeschrijving</a></li>
                                                                                            <li id="tab-additional"><a href="#">Extra informatie</a></li>
                                                                <li id="tab-tabreviews"><a href="#">Beoordelen</a></li>
                                                                <li id="tab-tags"><a href="#">Eigen tags</a></li>
                                    </ul>
        <div class="tabs-panels"><h2 class="acctab" id="acctab-description">Productbeschrijving</h2><div class="panel" style="display: block;">    <h2>Details</h2>
    <div class="std">
        <h2>Polar DM071: Witte glasdeurkoelkast tafelmodel<br> &nbsp;</h2>
<p>De<strong> Polar DM071</strong> is een kleine<strong> tafelmodel glasdeurkoelkast</strong> met een inhoud van 46 liter. Deze compacte<strong> witte</strong> koeler <br>heeft een draaideur voorzien van dubbel glas en is door zijn lage gewicht van 18kg zeer gemakkelijk te verplaatsen. <br>Kortom: een handige kleine glasdeurkoeler voor een net zo'n kleine prijs.<br> <br> <strong>Uitvoering:</strong></p>
<ul>
<li>Tafelmodel glasdeurkoelkast</li>
<li>Draaideur voorzien van dubbel glas</li>
<li>Kleur: wit</li>
<li>Voorzien van instelbare thermostaat</li>
</ul>
<p><strong>Specificaties:</strong></p>
<ul>
<li>Artikelnummer: DM071</li>
<li>Afmetingen BxDxH: 430 x 480 x 510 mm</li>
<li>Inhoud: 46 liter</li>
<li>Temperatuur: +4 ºC tot +18 ºC</li>
<li>Aansluitwaarde: 220 Volt, 85 Watt</li>
<li>Energieklasse: B</li>
<li>Gewicht: 18 kg</li>
</ul>
<h4 style="color: blue;"><span style="background-color: yellow;">Advies nodig, of meerdere stuks tegen de scherpste prijs?<br>Bel onze specialisten: <strong>036 5363782</strong></span></h4>
<p>&nbsp;</p>
<p>&nbsp;</p>    </div>
</div><h2 class="acctab" id="acctab-additional">Extra informatie</h2><div class="panel" style="display: none;">    <h2>Extra informatie</h2>
    <table class="data-table" id="product-attribute-specs-table">
        <colgroup><col width="25%">
        <col>
        </colgroup><tbody>
                    <tr class="first odd">
                <th class="label">Merk</th>
                <td class="data last">Polar</td>
            </tr>
                    <tr class="even">
                <th class="label">Kleur</th>
                <td class="data last">Wit</td>
            </tr>
                    <tr class="odd">
                <th class="label">Breedte</th>
                <td class="data last">400-500mm</td>
            </tr>
                    <tr class="even">
                <th class="label">Diepte</th>
                <td class="data last">400-500mm</td>
            </tr>
                    <tr class="odd">
                <th class="label">Hoogte</th>
                <td class="data last">   450-550mm</td>
            </tr>
                    <tr class="even">
                <th class="label">Inhoud</th>
                <td class="data last">Nee</td>
            </tr>
                    <tr class="odd">
                <th class="label">Temperatuurbereik</th>
                <td class="data last">+4 ºC / +18 ºC</td>
            </tr>
                    <tr class="last even">
                <th class="label">Vermogen</th>
                <td class="data last">Nee</td>
            </tr>
                </tbody>
    </table>
    <script type="text/javascript">decorateTable('product-attribute-specs-table')</script>
</div><h2 class="acctab" id="acctab-tabreviews">Beoordelen</h2><div class="panel" style="display: none;">
<div class="box-collateral box-reviews" id="customer-reviews">
            <!--<body onLoad="showcaptcha()">-->
<div class="form-add">
    <h2>Schrijf uw eigen review</h2>
            <form action="https://www.professionele-koeling.nl/review/product/post/id/212/" id="review-form" method="post" onsubmit="return validateRecaptcha()">
            <input name="form_key" type="hidden" value="TIOaSPgIeleEQ6nQ">
            <input type="hidden" name="form_key" value="TIOaSPgIeleEQ6nQ">
            <fieldset>
                                <h3>U plaatst een review over:                    <span>Polar DM071</span></h3>
                <div class="fieldset">
                                        <ul class="form-list">
                        <li>
                            <label for="nickname_field" class="required"><em>*</em>Uw naam                            </label>
                            <div class="input-box">
                                <input type="text" name="nickname" id="nickname_field" class="input-text required-entry" value="">
                            </div>
                        </li>
                        <li>
                            <label for="summary_field" class="required"><em>*</em>Titel van uw review</label>
                            <div class="input-box">
                                <input type="text" name="title" id="summary_field" class="input-text required-entry" value="">
                            </div>
                        </li>
                        <li>
                            <label for="review_field" class="required"><em>*</em>Beoordelen                            </label>
                            <div class="input-box">
                                <textarea name="detail" id="review_field" cols="5" rows="3" class="required-entry"></textarea>
                            </div>
                        </li>
                                                    <li id="rcode">
                                <div class="captcha">
                                    <div class="g-recaptcha" data-sitekey="6LejPHoUAAAAAIlhPgkpV53hhmCFsF7QPBTvAapB" data-theme="light"><div style="width: 304px; height: 78px;"><div><iframe title="reCAPTCHA" width="304" height="78" role="presentation" name="a-xvu1jid44yj4" frameborder="0" scrolling="no" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation" src="https://www.google.com/recaptcha/api2/anchor?ar=1&amp;k=6LejPHoUAAAAAIlhPgkpV53hhmCFsF7QPBTvAapB&amp;co=aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sOjQ0Mw..&amp;hl=ru&amp;v=A7KpaEASfhDcK0nXxgQEyyYv&amp;theme=light&amp;size=normal&amp;anchor-ms=20000&amp;execute-ms=30000&amp;cb=39bqq8hng205"></iframe></div><textarea id="g-recaptcha-response" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea></div><iframe style="display: none;"></iframe></div>
                                </div>
                                <span id="captcha-required" style="display:none; color:#ff0000">Please Fill Recaptcha To Continue</span>
                            </li>
                                            </ul>
                </div>
            </fieldset>
            <div class="buttons-set">
                <button type="submit" title="Review versturen" class="button">
                    <span><span>Review versturen</span></span></button>
            </div>
        </form>

        <script type="text/javascript">
            var code = "";
            var temp = 0;

            Validation.addAllThese(
                [
                    ['validate-rating', 'Vul alle bovenstaande waarderingen in', function (v) {
                        var trs = $('product-review-table').select('tr');
                        var inputs;
                        var error = 1;

                        for (var j = 0; j < trs.length; j++) {
                            var tr = trs[j];
                            if (j > 0) {
                                inputs = tr.select('input');

                                for (i in inputs) {
                                    if (inputs[i].checked == true) {
                                        error = 0;
                                    }
                                }

                                if (error == 1) {
                                    return false;
                                } else {
                                    error = 1;
                                }
                            }
                        }
                        return true;
                    }]
                ]
            );
        </script>
        <script type="text/javascript">
            var dataForm = new VarienForm('review-form', false);

            function validateRecaptcha() {
                                if (grecaptcha.getResponse() != "") {
                    document.getElementById("captcha-required").style.display = "none";
                    return true;
                } else {
                    document.getElementById("captcha-required").style.display = "block";
                    return false;
                }
                            }
        </script>
    
</div>
<!--</body>-->
<script src="https://www.google.com/recaptcha/api.js"></script></div>
</div><h2 class="acctab" id="acctab-tags">Eigen tags</h2><div class="panel" style="display: none;"><div class="box-collateral box-tags">
    <h2>Eigen tags</h2>
            <form id="addTagForm" action="https://www.professionele-koeling.nl/tag/index/save/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuL3BvbGFyLWRtMDcxLmh0bWw,/" method="get">
        <div class="form-add">
            <label for="productTagName">Uw tags toevoegen</label>
            <div class="input-box">
                <input type="text" class="input-text required-entry" name="productTagName" id="productTagName">
            </div>
            <button type="button" title="Tags toevoegen" class="button" onclick="submitTagForm()">
                <span>
                    <span>Tags toevoegen</span>
                </span>
            </button>
        </div>
    </form>
    <p class="note">Gebruik spaties om tags te scheiden. Gebruik enkele aanhalingstekens (‘) voor woordgroepen.</p>
    <script type="text/javascript">
    //<![CDATA[
        var addTagFormJs = new VarienForm('addTagForm');
        function submitTagForm(){
            if(addTagFormJs.validator.validate()) {
                addTagFormJs.form.submit();
            }
        }
    //]]>
    </script>
</div>
</div></div>

    </div>
    <script type="text/javascript">
        //<![CDATA[
        jQuery(function($) {

            //Link to the reviews tab
            var tabOperator = {

                root : ''
                , $rootContainer : null
                , $tabsContainer : null
                , $panelsContainer : null

                //1 - tabs/accordion, 2 - accordion, 3 - tabs
                , mode : 1                , threshold : 1024                , initialAccIndex : 0
                , tabEffect : 'default'
                , accEffect : 'default'

                , init : function(root)
                {
                    //If no param, set default selector
                    tabOperator.root = root || '.gen-tabs';
                    tabOperator.$rootContainer      = $(tabOperator.root);
                    tabOperator.$tabsContainer      = tabOperator.$rootContainer.children('.tabs');
                    tabOperator.$panelsContainer    = tabOperator.$rootContainer.children('.tabs-panels');

                    //Activate tabs based on selected mode
                                            tabOperator.initialAccIndex = null;
                    
                    if (tabOperator.mode === 1)
                    {
                        //Initial value of the flag which indicates whether viewport was above the threshold
                        var previousAboveThreshold = $(window).width() >= tabOperator.threshold;

                        //Activate tabs or accordion
                        if (previousAboveThreshold)
                        {
                            //If above threshold - activate tabs
                            tabOperator.initTabs();
                        }
                        else
                        {
                            //If below threshold - activate accordion
                            tabOperator.initAccordion(tabOperator.initialAccIndex);
                        }

                        //On tab click
                        tabOperator.hookToAccordionOnClick();

                        //On window resize
                        $(window).on('themeResize', function (e, resizeEvent) {

                            if ($(window).width() < tabOperator.threshold)
                            {
                                if (previousAboveThreshold)
                                {
                                    //Now below threshold, previously above, so switch to accordion
                                    var api = tabOperator.$tabsContainer.data("tabs");
                                    var index = api.getIndex();
                                    api.destroy();

                                    tabOperator.initAccordion(index);
                                }
                                previousAboveThreshold = false;
                            }
                            else
                            {
                                if (!previousAboveThreshold)
                                {
                                    //Now above threshold, previously below, so switch to tabs
                                    var api = tabOperator.$panelsContainer.data("tabs");
                                    var index = api.getIndex();
                                    api.destroy();
                                    tabOperator.$rootContainer.removeClass("accor");

                                    tabOperator.initTabs(index);
                                }
                                previousAboveThreshold = true;
                            }

                        });
                    }
                    else if (tabOperator.mode === 2)
                    {
                        tabOperator.initAccordion(tabOperator.initialAccIndex);

                        //On tab click
                        tabOperator.hookToAccordionOnClick();
                    }
                    else
                    {
                        tabOperator.initTabs();
                    }

                } //end: init

                , initTabs : function(index)
                {
                    //If no param, set it to 0
                    if (typeof index === "undefined")
                    { 
                        index = 0;
                    }
                    tabOperator.$tabsContainer.tabs(".tabs-panels .panel", {effect: tabOperator.tabEffect, initialIndex: index});
                }

                , initAccordion : function(index)
                {
                    //If no param, set it to 0
                    if (typeof index === "undefined")
                    { 
                        index = 0;
                    }
                    tabOperator.$rootContainer.addClass("accor");
                    tabOperator.$panelsContainer.tabs(".tabs-panels .panel", {tabs: '.acctab', effect: tabOperator.accEffect, initialIndex: index});
                }

                , hookToAccordionOnClick : function()
                {
                    //Attach a handler to an event after a tab is clicked
                    tabOperator.$panelsContainer.bind("onClick", function(event, index) {

                        //Note: "this" is a reference to the DOM element of tabs
                        //var theTabs = this;
                        var target = event.target || event.srcElement || event.originalTarget;

                        //If viewport is lower than the item, scroll to that item
                        var itemOffsetTop = $(target).offset().top;
                        var viewportOffsetTop = jQuery(window).scrollTop();
                        if (itemOffsetTop < viewportOffsetTop)
                        {
                            $("html, body").delay(150).animate({scrollTop: (itemOffsetTop-50)}, 600, 'easeOutCubic');
                        }

                    }); //end: bind onClick
                }

                , openTab : function()
                {
                    if (tabOperator.$rootContainer.hasClass("accor"))
                    {
                        var $panels = tabOperator.$panelsContainer;
                        var indexOfTab = $panels.children(".acctab").index($("#acctab-tabreviews"));
                        $panels.data("tabs").click(indexOfTab);
                    }
                    else
                    {
                        var $tabs = tabOperator.$tabsContainer;
                        var indexOfTab = $tabs.children("#tab-tabreviews").index();
                        $tabs.data("tabs").click(indexOfTab);
                    }
                }

                , slideTo : function(target, offset)
                {
                    //Slide to tab (minus height of sticky menu)
                    var itemOffsetTop = $(target).offset().top - offset;
                    $("html, body").animate({scrollTop: itemOffsetTop}, 600, 'easeOutCubic');
                }

            };

            //Initialize tabs
            tabOperator.init('#product-tabs');

                
            $("#goto-reviews").click(function() {
                
                tabOperator.openTab();
                tabOperator.slideTo('#product-tabs', 50);

            }); //end: on click

            $("#goto-reviews-form").click(function() {

                tabOperator.openTab();
                tabOperator.slideTo('#review-form', 90);

            }); //end: on click

        
        });
        //]]>
    </script>


    
</div>		
		
		
	</div> <!-- end: box-tabs -->

		
			<div class="box-additional grid12-9"></div>
	
</div> <!-- end: product-view -->
<style>
	.product-benefits {
    margin-top: 20px;
}

.product-benefits ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.product-benefits li {
    margin-bottom: 8px;
    font-size: 14px;
    color: #333;
}

.product-benefits li:before {
    content: "✓";
    color: #28a745;
    font-weight: bold;
    margin-right: 10px;
}
</style>

<script type="text/javascript">
    var lifetime = 3600;
    var expireAt = Mage.Cookies.expires;
    if (lifetime > 0) {
        expireAt = new Date();
        expireAt.setTime(expireAt.getTime() + lifetime * 1000);
    }
    Mage.Cookies.set('external_no_cache', 1, expireAt);
</script>
                    </div>
                    <div class="postscript"></div>
                </div>




--- ФАЙЛ: proxies.txt ---


--- ФАЙЛ: traceback.txt ---


---

# ЯДРО ПРОЕКТА (НЕ МЕНЯТЬ)

Следующие файлы уже написаны и протестированы. Используй их интерфейсы, не дублируй логику:



--- app/main.py (НЕ МЕНЯТЬ) ---
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


--- app/browser.py (НЕ МЕНЯТЬ) ---
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


--- app/config.py (НЕ МЕНЯТЬ) ---
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


--- app/exporter.py (НЕ МЕНЯТЬ) ---
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


--- app/utils.py (НЕ МЕНЯТЬ) ---
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

---

# ТЕКУЩИЙ ШАБЛОН МОДУЛЯ

Файл `app/parser.py` — перепиши его полностью под план проекта:

"""
⚠️ ДЕМО-ПРИМЕР, А НЕ УНИВЕРСАЛЬНЫЙ ДЕФОЛТ ⚠️

Код ниже — рабочий сквозной пример парсинга объявлений OLX (авто: название,
цена, вид топлива), созданный для демонстрации полного цикла workflow
(`ai_workflow.py analyze/project/module scraper/module parser`) на реальном
сайте. Селекторы (`css-1sw7q4x`, `css-wlcw7o`, `data-testid="ad-price"` и т.д.)
специфичны именно для OLX и НЕ подходят для других сайтов "как есть".

Для нового заказа этот файл нужно заменить одним из способов:
  1. python ai_workflow.py module parser <project_name>
     (сгенерирует промпт для ИИ на основе анализа/плана нового сайта,
     ответ ИИ сохраняется в AI_OUTPUT/04_parser_answer.py и переносится сюда)
  2. Вручную переписать `parse_single_item`/`parse_listing` под структуру
     карточек нового сайта, сохранив сигнатуру `parse_html_data(html_contents)`,
     которую вызывает `app/main.py`.

Модуль `app/html_parser.py` (HtmlParser) — универсальный и НЕ требует правок,
используй его безопасные методы (`select_one`, `find`, `get_text`, `get_attr`
и т.д.) при написании парсера для нового сайта. Аналогично, для приведения
извлечённых значений к консистентному формату (числа, даты, bool, URL и т.д.)
используй `app/data_normalizer.py` (DataNormalizer) вместо ручного разбора
строк прямо здесь.
"""

from typing import List, Dict, Any
from app.html_parser import HtmlParser
from app.data_normalizer import DataNormalizer
from app.utils import log_message


def parse_single_item(card) -> Dict[str, Any]:
    """
    Извлекает целевые поля (название, цена, топливо) из структуры одной карточки товара.

    Args:
        card (bs4.element.Tag): Объект тега одной карточки объявления.

    Returns:
        dict: Словарь с извлеченными данными объявления.
    """
    # 1. Извлечение названия (безопасно через HtmlParser: не бросает исключение,
    #    если элемент отсутствует, и нормализует пробелы/переносы строк).
    title_element = HtmlParser.find(card, "h4", class_="css-wlcw7o")
    title = HtmlParser.get_text(title_element, default="")

    # 2. Извлечение цены и её нормализация через централизованный
    #    Data Normalization слой (app/data_normalizer.py, Milestone 5) —
    #    вместо разбора строки цены прямо здесь (DataNormalizer.normalize_price
    #    переиспользует app.utils.clean_price, чтобы логика не дублировалась).
    price_element = HtmlParser.find(card, "p", attrs={"data-testid": "ad-price"})
    raw_price = HtmlParser.get_text(price_element, default="")
    if raw_price:
        price = DataNormalizer.normalize_price(raw_price)
        if price is None:
            log_message("error", f"[{__file__}] Не удалось нормализовать цену '{raw_price}'")
    else:
        log_message("warning", f"[{__file__}] Предупреждение: Элемент цены не найден в карточке с ID {HtmlParser.get_attr(card, 'id')}")
        price = None

    # 3. Извлечение вида топлива
    fuel = ""
    params_container = HtmlParser.find(card, "div", class_="css-13vv2xi")
    param_spans = HtmlParser.find_all(params_container, "span", class_="css-h59g4b")
    if len(param_spans) >= 3:
        fuel = HtmlParser.get_text(param_spans[2], default="")
    elif params_container is not None:
        log_message("warning", f"[{__file__}] Предупреждение: Недостаточно параметров для извлечения топлива в карточке с ID {HtmlParser.get_attr(card, 'id')}")
        fuel = "Не указано"

    return {
        "title": title,
        "price": price,
        "fuel": fuel
    }

def parse_listing(html: str) -> List[Dict[str, Any]]:
    """
    Инициализирует HTML Parser, находит коллекцию всех карточек автомобилей на странице
    и передает каждую в parse_single_item.

    Args:
        html (str): Строка сырого HTML-кода страницы.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными по автомобилям.
    """
    soup = HtmlParser.parse(html)
    if soup is None:
        # HtmlParser.parse() уже залогировал причину (пустой/невалидный HTML).
        return []

    cards = HtmlParser.find_all(soup, "div", class_="css-1sw7q4x")

    if not cards:
        log_message("warning", f"[{__file__}] Предупреждение: Карточки объявлений на странице не найдены.")
        return []

    log_message("info", f"[{__file__}] Найдено карточек для парсинга: {len(cards)}")

    results = []
    for card in cards:
        try:
            item_data = parse_single_item(card)
            results.append(item_data)
        except Exception as e:
            card_id = HtmlParser.get_attr(card, "id", "unknown")
            log_message("error", f"[{__file__}] Критическая ошибка при парсинге карточки ID {card_id}: {e}")
            continue

    return results

def parse_html_data(html_contents: List[str]) -> List[Dict[str, Any]]:
    """
    Точка интеграции с главным оркестратором main.py.
    Принимает список строк HTML и возвращает агрегированные результаты.

    Args:
        html_contents (List[str]): Список строк сырого HTML.

    Returns:
        List[Dict[str, Any]]: Общий список спарсенных данных.
    """
    all_results = []
    log_message("info", f"[{__file__}] Начало обработки {len(html_contents)} страниц(ы)...")

    for idx, html in enumerate(html_contents, 1):
        try:
            page_results = parse_listing(html)
            all_results.extend(page_results)
        except Exception as e:
            log_message("error", f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
            continue

    log_message("info", f"[{__file__}] Парсинг успешно завершен. Всего собрано элементов: {len(all_results)}")
    return all_results


---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/parser.py` (модуль: **parser**).

## Требования

1. **Только функции** — без классов.
2. **Один файл** — весь код модуля в одном ответе.
3. **Следуй project_plan.md** — имена функций, сигнатуры, алгоритм.
4. **Не трогай ядро** — `main.py` уже вызывает `fetch_page_data()` и `parse_html_data()`. Сохрани эти имена или обнови только если план явно требует другие.
5. **Минимум зависимостей** — используй только то, что уже есть в проекте.
6. **Обработка ошибок** — try/except на уровне страниц/элементов, не падай на одной ошибке.
7. **Логирование** — `print(f"[{__file__}] ...")` как в шаблоне.

## Если модуль = scraper

- Отвечает **только** за сеть, навигацию, пагинацию, скролл, клики.
- Возвращает `List[str]` — список сырого HTML (или JSON-строк).
- Не парсит DOM — это задача parser.py.
- Используй `app.config` для таймаутов и путей.
- Используй `random_delay()` из `app.utils` между запросами.

## Если модуль = parser

- Отвечает **только** за извлечение данных из сырого контента.
- Принимает `List[str]`, возвращает `List[Dict[str, Any]]`.
- Используй BeautifulSoup для HTML.
- Сохрани функцию `parse_single_item()` для парсинга одного элемента.
- Поля результата — строго по project_plan.md.

---

# ФОРМАТ ОТВЕТА

1. Кратко (3–5 строк): что делает модуль.
2. Полный код файла `app/parser.py` в одном блоке:

```python
# полный код здесь
```

3. Как протестировать локально (1–2 команды).

**ЗАПРЕЩЕНО:**
- Писать код для других файлов.
- Добавлять GUI, CLI, меню.
- Добавлять функции, которых нет в project_plan.md.
- Использовать классы.
