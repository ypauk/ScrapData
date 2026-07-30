# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/scraper.py`.

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

Я посмотрел файл промпта 01_analysis_prompt.md в репозитории. В нём роль — Python Web Scraping Engineer, задача — проанализировать проект клиента, выбрать простое и надёжное решение, без написания кода на этом этапе. Входные данные: нужно собрать данные товаров с сайта professionele-koeling.nl, сначала сделать тестовый CSV на 2 товара, затем полный scrape.

Результат выполнения такого промпта:

Анализ проекта клиента
1. Цель проекта

Необходимо разработать scraper для сайта каталога товаров:

Источник:

Website: https://www.professionele-koeling.nl/koelkasten-kisten.html

Задача:

собрать информацию по всем товарам;
сохранить результат в CSV;
каждая характеристика должна находиться в отдельной колонке;
сначала предоставить тестовый файл с 2 товарами для проверки структуры.
2. Требуемые поля CSV

На основе Google Sheet клиента требуется получить:

Поле	Источник
URL	ссылка товара
Breadcrumb	категория/хлебные крошки
Title	название товара
Short description	краткое описание
imageurl	URL изображения
image_name	имя изображения
Price	обычная цена
Sale price	цена со скидкой
Description	полное описание
Specs	список характеристик
Spec_detail	детальные характеристики

Каждый элемент должен быть отдельной колонкой. Нельзя объединять разные типы данных в одну колонку.

3. Анализ структуры сайта

Предварительная структура:

Категория

Страница категории:

/koelkasten-kisten.html

На ней находятся карточки товаров:

название;
ссылка;
изображение;
краткая информация.

Алгоритм:

Открыть страницу категории.
Собрать ссылки всех товаров.
Перейти на страницы товаров.
Извлечь детальную информацию.
4. Страница товара

Пример товара:

Polar GE579

Доступные данные:

название:
Polar GE579
краткое описание:
De Polar GE579 is een zwarte minibar koelkast...
цена:
259
sale price:
229
описание:
полный HTML/text блок.
характеристики:

Пример:

Exterieur: zwart
Interieur: roestvrijstaal
Werking: absorptie koelsysteem
Verlichting: LED
Roosters: 2x
Artikelnummer: GE579
Inhoud: 29 liter
Gewicht: 13 kg
5. Предлагаемая стратегия разработки
Самый простой вариант

Использовать:

Python
requests
BeautifulSoup
pandas

Без Selenium.

Причина:

сайт выглядит как обычный HTML каталог;
данные доступны в HTML;
нет признаков сложного JavaScript;
браузерная автоматизация добавит ненужную сложность.
6. Pipeline
Category URLs
      |
      ↓
Collect product URLs
      |
      ↓
Visit product pages
      |
      ↓
Extract fields
      |
      ↓
Normalize data
      |
      ↓
Export CSV
7. Обработка характеристик

Проблема:

На странице характеристики представлены текстом:

Название:
значение

Решение:

Разделять по:

:

Пример:

До:

Inhoud: 29 liter
Gewicht: 13 kg

После:

Spec	Value
Inhoud	29 liter
Gewicht	13 kg

Для CSV:

вариант A:

Specs
"Inhoud, Gewicht"

Spec_detail
"29 liter, 13 kg"

или лучше:

spec_Inhoud
spec_Gewicht

если клиент требует строгую структуру.

8. Риски
1. Пагинация категорий

Нужно проверить:

есть ли страницы 2,3,4...
сколько товаров всего.
2. Изображения

Проверить:

оригинальный URL картинки;
thumbnail или full image;
формат имени файла.
3. Цена

Нужно учитывать:

товары без скидки;
товары с несколькими ценами;
формат европейской цены:
€ 259,00

нужно привести к:

259.00
4. Характеристики

Самый сложный участок.

Возможны:

разные наборы характеристик;
отсутствующие поля;
разные названия параметров.

Нужна нормализация.

9. План тестового этапа

Перед полным scrape:

Собрать 2 товара.
Создать CSV.
Проверить:

✅ все колонки присутствуют
✅ нет смешанных данных
✅ изображения корректные
✅ цены корректные
✅ характеристики читаемые

После подтверждения клиента:

запустить полный сбор.

10. Оценка сложности

Сложность: низкая / средняя

Оценка:

анализ сайта: 1–2 часа
scraper: 3–5 часов
очистка данных: 2–4 часа
тестовый CSV: 30 минут

Общий срок:

1 рабочий день для MVP + тестовый файл

Итоговое решение

Использовать простой Python scraper:

requests
BeautifulSoup
pandas

Не использовать:

Selenium
Playwright
сложные фреймворки

Сначала сделать:

2 products → CSV → client approval

после подтверждения:

full catalog scrape

Это минимальное решение с наименьшим риском и соответствует требованиям клиента.

---

## План проекта (этап 2)

Техническое решение проекта: Product Scraper для professionelle-koeling.nl
1. Цель проекта

Необходимо разработать scraper для каталога товаров сайта:

Источник:
professionele-koeling.nl

Задача:

собрать все товары из каталога;
получить данные каждого товара;
сформировать CSV;
каждая характеристика должна находиться в отдельной колонке;
сначала подготовить тестовый CSV на 2 товара;
после подтверждения клиента выполнить полный scrape.
2. Формат выходного CSV

Обязательные колонки:

Column	Description
URL	ссылка на товар
Breadcrumb	категория товара
Title	название
Short description	короткое описание
imageurl	URL изображения
image_name	имя изображения
Price	обычная цена
Sale price	цена со скидкой
Description	полное описание
Specs	список характеристик
Spec_detail	значения характеристик

Каждое поле должно быть отдельной колонкой.

Нельзя:

объединять цену и скидку;
смешивать описание и характеристики;
хранить несколько типов данных в одном поле.
3. Анализ структуры сайта

Предполагаемая структура:

Category page
      |
      |
      ↓
Product URLs
      |
      |
      ↓
Product pages
      |
      |
      ↓
Extract data
      |
      |
      ↓
Normalize
      |
      |
      ↓
CSV export
4. Архитектура решения

Использовать простой стек:

Python
requests
BeautifulSoup
pandas

Не использовать:

Selenium
Playwright
браузерную автоматизацию

Причина:

сайт является обычным HTML каталогом;
данные доступны в разметке;
JavaScript rendering не является обязательным.
5. Pipeline обработки
Шаг 1 — Получение категорий

Парсер открывает страницы категорий:

/koelkasten-kisten.html

На странице собирает:

название товара;
URL товара;
изображение;
краткую информацию.
Шаг 2 — Сбор ссылок товаров

Создается список:

[
 product_url_1,
 product_url_2,
 product_url_3,
 ...
]

Дополнительно проверить:

pagination;
количество страниц;
скрытые категории.
Шаг 3 — Парсинг страницы товара

Для каждого товара получить:

Title

Пример:

Polar GE579
Short description

Пример:

De Polar GE579 is een zwarte minibar koelkast...
Price

Нормализовать:

Было:

€ 259,00

Стало:

259.00
Sale price

Например:

229.00
Description

Сохранить полный текст описания.

Images

Получить:

imageurl
image_name

Проверить:

оригинальное изображение;
не thumbnail;
корректное имя файла.
6. Обработка характеристик

Основная сложность — блок Specs.

Исходный формат:

Inhoud: 29 liter
Gewicht: 13 kg
Artikelnummer: GE579
Energieklasse: F

Нужно преобразовать:

spec	value
Inhoud	29 liter
Gewicht	13 kg
Artikelnummer	GE579
Energieklasse	F

В CSV возможно два варианта.

Вариант 1

Колонки:

Specs
Spec_detail

Пример:

Specs:
Inhoud, Gewicht, Artikelnummer

Spec_detail:
29 liter, 13 kg, GE579
Вариант 2 (лучший)

Динамические колонки:

spec_Inhoud
spec_Gewicht
spec_Energieklasse

Это предпочтительно, если клиент хочет строгую структуру данных.

7. Нормализация данных
Цена

Привести:

€ 259,00

к:

259.00
Текст

Очистить:

лишние пробелы;
переносы строк;
HTML теги.
Изображения

Проверить:

URL доступен;
изображение существует;
имя файла корректное.
8. Обработка ошибок

Необходимо добавить:

Ошибки страницы товара

Если товар недоступен:

status = failed

и продолжить scrape.

Ошибки цены

Если цена отсутствует:

Price = empty

Не подставлять значения.

Ошибки характеристик

Если параметр отсутствует:

empty cell
9. Тестовый этап

Перед полным запуском:

Собрать:

2 products

Проверить CSV:

✅ все колонки присутствуют
✅ нет смешанных данных
✅ изображения открываются
✅ цены корректные
✅ характеристики разделены

После подтверждения клиента:

запустить полный каталог.

10. Структура проекта

Предлагаемая структура:

project/

├── scraper/
│   ├── category_parser.py
│   ├── product_parser.py
│   ├── extractor.py
│   └── normalizer.py
│
├── output/
│   ├── test_products.csv
│   └── full_products.csv
│
├── config/
│   └── settings.py
│
├── logs/
│
└── main.py
11. План разработки
Этап 1

Анализ HTML:

1–2 часа

Этап 2

Создание scraper:

3–5 часов

Этап 3

Очистка данных:

2–4 часа

Этап 4

Тестовый CSV:

30 минут

12. Итоговое техническое решение

Использовать:

Python
+
requests
+
BeautifulSoup
+
pandas

Алгоритм:

Category pages
      ↓
Collect product URLs
      ↓
Open product pages
      ↓
Extract fields
      ↓
Normalize data
      ↓
Export CSV

Первый deliverable:

test_products.csv

с 2 товарами.

После проверки:

full_products.csv

со всем каталогом.

Финальное решение

Проект имеет низкую/среднюю сложность.

Оптимальная реализация:

без браузерной автоматизации;
без сложных scraping framework;
с обычным HTML parsing;
с четкой CSV схемой;
с отдельной обработкой характеристик.

Это соответствует требованиям клиента: сначала тестовый файл на 2 товара, затем полный сбор данных.

---

## Данные клиента



--- ФАЙЛ: description.txt ---

Задание от клиента, для теста собирем 2 шт товаров и скину емку файл csv
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

Данные с файла spreadsheet:
URL	Breadcrumb	Title 	Short description	imageurl	image_name	Price	Sale price	Description 	Specs	Spec_detail
https://www.professionele-koeling.nl/koelkasten-kisten.html	Home	Polar GE579	"De Polar GE579 is een zwarte minibar koelkast met
29 liter inhoud voor gebruik in hotelkamers, B&B's of ver-
gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken."	if multipli seperated by comma	if multiple seperated by comma	259	229	"Polar GE579: Zwarte 30 liter minibar koelkast voor de hotelkamer
De Polar GE579 is een zwarte minibar koelkast met een capaciteit van 29 liter. Deze koelkast maakt gebruik van het absorptie
koelsysteem i.p.v. een compressor. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor
toepassingen in hotelkamers, B&B 's en vergaderzalen.

Uitvoering:

Exterieur: zwaart
Interieur: roestvrijstaal
Werking: Werkt met warmtepomp in plaats van ventilatoren
Verwisselbare en afsluitbare deur
Verlichting: LED
Roosters (2x)
Vrijwel geruisloos
Vrijstaand of inbouw
Absorptie koelsysteem
Automatische ontdooiing
Specificaties:

Artikelnummer: GE579
Inhoud: 29 liter
Temperatuurbereik:  3-5°C bij een omgevingstemperatuur van 16°C
Temperatuurbereik: 5-8°C bij een omgevingstemperatuur van 25°C
Temperatuurbereik: 8-12°C bij een omgevingstemperatuur van 32°C
Afmetingen BxDxH: 400 x 430 x 530 mm
Energieklasse: F
Aansluitwaarde: 220-240 Volt, 60 watt
Klimaatklasse: N (omgevingstemperatuur tussen +16°C en +32°)
Koelmiddel: R600a
Gewicht: 13 kg
Bij het absorptiesysteem, dat geheel zonder bewegende delen kan worden uitgevoerd, wordt gebruik gemaakt van het verschijnsel dat sommige vloeistoffen (bijvoorbeeld water) sommige koelmiddelen (bijvoorbeeld ammoniak) bij lage temperatuur absorberen en bij hogere weer afgeven. De in het vrieslichaam ontstane damp van het koelmiddel wordt door de absorberende vloeistof opgenomen in een absorptievat, waar de aanvankelijk verdunde oplossing tot een geconcentreerde wordt verdicht. Deze laatste oplossing komt in een ruimte waar het koelmiddel door een gasvlam of een andere dan gasvormige warmtebron uit de vloeistof wordt verdreven. Het koelmiddel wordt vervolgens in een condensor gekoeld en gecondenseerd en treedt daarna in het vrieslichaam, waarmee de kringloop gesloten is. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor toepassingen in hotelkamers en vergaderzalen.

Gebruikertips:
De kast kan de temperatuur bij normaal gebruik ca. 15 graden terug koelen.
Men moet zich bij inbouw aan de inbouwvoorschriften houden.
Als dit niet gebeurd en de kast draait in zijn eigen warmte, dan kan deze niet naar behoren functioneren."	https://www.awesomescreenshot.com/image/62286448?key=8b032d4304d185282fd860cfb3c858bb each own colom	evertything before the : is the header 

--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]

--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---
{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "WebInspector",
      "version": "537.36"
    },
    "pages": [
      {
        "startedDateTime": "2026-07-30T10:49:10.852Z",
        "id": "page_2",
        "title": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
        "pageTimings": {
          "onContentLoad": 2386.9999999988067,
          "onLoad": 6349.00000000016
        }
      }
    ],
    "entries": [
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 238,
                "columnNumber": 390
              },
              {
                "functionName": "lo",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 413,
                "columnNumber": 1283
              },
              {
                "functionName": "",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 564,
                "columnNumber": 292
              },
              {
                "functionName": "f",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 564,
                "columnNumber": 175
              },
              {
                "functionName": "lv",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 564,
                "columnNumber": 276
              },
              {
                "functionName": "mv",
                "scriptId": "413",
                "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                "lineNumber": 563,
                "columnNumber": 399
              }
            ],
            "parent": {
              "description": "setTimeout",
              "callFrames": [
                {
                  "functionName": "ed",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 233,
                  "columnNumber": 220
                },
                {
                  "functionName": "FE.bind",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 740,
                  "columnNumber": 313
                },
                {
                  "functionName": "OU",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1010,
                  "columnNumber": 491
                },
                {
                  "functionName": "Im",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1014,
                  "columnNumber": 303
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1018,
                  "columnNumber": 312
                },
                {
                  "functionName": "c",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1016,
                  "columnNumber": 129
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1018,
                  "columnNumber": 276
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1018,
                  "columnNumber": 281
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 1020,
                  "columnNumber": 2
                }
              ],
              "parent": {
                "description": "PendingScript",
                "callFrames": [
                  {
                    "functionName": "",
                    "scriptId": "398",
                    "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                    "lineNumber": 96,
                    "columnNumber": 64
                  },
                  {
                    "functionName": "",
                    "scriptId": "398",
                    "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                    "lineNumber": 97,
                    "columnNumber": 2
                  }
                ]
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.google.com/ccm/collect?rcb=8&frm=0&ae=g&auid=2132767939.1785405308&dt=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&en=page_view&dl=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&dr=www.professionele-koeling.nl&scrsrc=www.googletagmanager.com&rnd=1166332829.1785408554&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He67s1v9243950528za200zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115616985~115938466~115938469~118395335~118897920~118897930~119896803&apvc=1&tft=1785408553742&tfd=2920&fmt=8",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            }
          ],
          "queryString": [
            {
              "name": "rcb",
              "value": "8"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "ae",
              "value": "g"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "dt",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "en",
              "value": "page_view"
            },
            {
              "name": "dl",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "dr",
              "value": "www.professionele-koeling.nl"
            },
            {
              "name": "scrsrc",
              "value": "www.googletagmanager.com"
            },
            {
              "name": "rnd",
              "value": "1166332829.1785408554"
            },
            {
              "name": "navt",
              "value": "n"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "ep.ads_data_redaction",
              "value": "0"
            },
            {
              "name": "gtm",
              "value": "45He67s1v9243950528za200zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115616985~115938466~115938469~118395335~118897920~118897930~119896803"
            },
            {
              "name": "apvc",
              "value": "1"
            },
            {
              "name": "tft",
              "value": "1785408553742"
            },
            {
              "name": "tfd",
              "value": "2920"
            },
            {
              "name": "fmt",
              "value": "8"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/plain"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 21,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:13.743Z",
        "time": 1148.9999999994325,
        "timings": {
          "blocked": 580.9999999996799,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 1,
          "wait": 35.00000000050932,
          "receive": 531.9999999992433,
          "_blocked_queueing": 51.99999999967986,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "Ep.K",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 352,
                "columnNumber": 33
              },
              {
                "functionName": "Bp.sendRequest",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 350,
                "columnNumber": 736
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 479,
                "columnNumber": 466
              },
              {
                "functionName": "ry.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 544,
                "columnNumber": 125
              },
              {
                "functionName": "cv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 480,
                "columnNumber": 389
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1749
              },
              {
                "functionName": "bv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1798
              },
              {
                "functionName": "fv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 326
              },
              {
                "functionName": "gv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 746
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 303
              },
              {
                "functionName": "e",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 137
              },
              {
                "functionName": "gx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 478
              },
              {
                "functionName": "gA",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 182
              },
              {
                "functionName": "OL",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 789,
                "columnNumber": 102
              },
              {
                "functionName": "PN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 819,
                "columnNumber": 280
              },
              {
                "functionName": "f",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 820,
                "columnNumber": 441
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 428
              },
              {
                "functionName": "Sl",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 318,
                "columnNumber": 75
              },
              {
                "functionName": "op",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 347,
                "columnNumber": 240
              },
              {
                "functionName": "RN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 414
              },
              {
                "functionName": "u",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 269
              },
              {
                "functionName": "vo",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 337,
                "columnNumber": 647
              },
              {
                "functionName": "pD",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 368
              },
              {
                "functionName": "nD.flush",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 627,
                "columnNumber": 80
              },
              {
                "functionName": "nD.register",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 624,
                "columnNumber": 311
              },
              {
                "functionName": "GT",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 836,
                "columnNumber": 49
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 252,
                "columnNumber": 186
              },
              {
                "functionName": "l.apply",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 176,
                "columnNumber": 464
              },
              {
                "functionName": "gb",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 710
              },
              {
                "functionName": "Md.evaluate",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 178,
                "columnNumber": 71
              },
              {
                "functionName": "Ne",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 205,
                "columnNumber": 124
              },
              {
                "functionName": "l.apply",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 176,
                "columnNumber": 464
              },
              {
                "functionName": "gb",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 710
              },
              {
                "functionName": "Md.evaluate",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 178,
                "columnNumber": 71
              },
              {
                "functionName": "Fe",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 203,
                "columnNumber": 215
              },
              {
                "functionName": "l.apply",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 176,
                "columnNumber": 464
              },
              {
                "functionName": "gb",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 710
              },
              {
                "functionName": "fb",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 461
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 200,
                "columnNumber": 472
              },
              {
                "functionName": "l.apply",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 176,
                "columnNumber": 464
              },
              {
                "functionName": "gb",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 710
              },
              {
                "functionName": "l.Sq",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 139,
                "columnNumber": 1276
              },
              {
                "functionName": "sf",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 211,
                "columnNumber": 959
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 681,
                "columnNumber": 6
              },
              {
                "functionName": "pA",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 571,
                "columnNumber": 495
              },
              {
                "functionName": "wA.evaluate",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 577,
                "columnNumber": 288
              },
              {
                "functionName": "e",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 597,
                "columnNumber": 169
              },
              {
                "functionName": "VB",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 598,
                "columnNumber": 741
              },
              {
                "functionName": "YB",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 602,
                "columnNumber": 217
              },
              {
                "functionName": "NE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 658,
                "columnNumber": 244
              },
              {
                "functionName": "OE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 659,
                "columnNumber": 188
              },
              {
                "functionName": "Im",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 895,
                "columnNumber": 0
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 312
              },
              {
                "functionName": "c",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 896,
                "columnNumber": 129
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 276
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 281
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 900,
                "columnNumber": 2
              }
            ],
            "parent": {
              "description": "PendingScript",
              "callFrames": [
                {
                  "functionName": "Ls",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 241,
                  "columnNumber": 251
                },
                {
                  "functionName": "Xc",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 231,
                  "columnNumber": 406
                },
                {
                  "functionName": "mo",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 413,
                  "columnNumber": 1368
                },
                {
                  "functionName": "GA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 656,
                  "columnNumber": 1735
                },
                {
                  "functionName": "bH",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 773,
                  "columnNumber": 302
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 326,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 274,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 285,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 759,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 649,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 655,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 675,
                  "columnNumber": 169
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 218,
                  "columnNumber": 124
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 359
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 99
                },
                {
                  "functionName": "VB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 680,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 736,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 737,
                  "columnNumber": 188
                },
                {
                  "functionName": "QE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 742,
                  "columnNumber": 320
                }
              ],
              "parent": {
                "description": "setTimeout",
                "callFrames": [
                  {
                    "functionName": "ed",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 233,
                    "columnNumber": 220
                  },
                  {
                    "functionName": "FE.bind",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 740,
                    "columnNumber": 313
                  },
                  {
                    "functionName": "OU",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1010,
                    "columnNumber": 491
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1014,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1016,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1020,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 96,
                      "columnNumber": 64
                    },
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 97,
                      "columnNumber": 2
                    }
                  ]
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.google.com/rmkt/collect/1026069724/?random=1785408555135&cv=11&fst=1785408555135&fmt=8&bg=ffffff&guid=ON&async=1&en=gtag.config&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xec&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&data=event%3Dgtag.config&ept=68&gcp=5",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1785408555135"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555135"
            },
            {
              "name": "fmt",
              "value": "8"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "gtag.config"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xec"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "data",
              "value": "event%3Dgtag.config"
            },
            {
              "name": "ept",
              "value": "68"
            },
            {
              "name": "gcp",
              "value": "5"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/html"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 20,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:15.264Z",
        "time": 677.9999999998836,
        "timings": {
          "blocked": 100.00000000016007,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0,
          "wait": 54.00000000029104,
          "receive": 523.9999999994325,
          "_blocked_queueing": 99.00000000016007,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "Ep.K",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 352,
                "columnNumber": 33
              },
              {
                "functionName": "Bp.sendRequest",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 350,
                "columnNumber": 736
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 479,
                "columnNumber": 466
              },
              {
                "functionName": "ry.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 544,
                "columnNumber": 125
              },
              {
                "functionName": "cv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 480,
                "columnNumber": 389
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1749
              },
              {
                "functionName": "bv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1798
              },
              {
                "functionName": "fv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 326
              },
              {
                "functionName": "gv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 746
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 303
              },
              {
                "functionName": "e",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 137
              },
              {
                "functionName": "gx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 478
              },
              {
                "functionName": "gA",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 182
              },
              {
                "functionName": "OL",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 789,
                "columnNumber": 102
              },
              {
                "functionName": "PN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 819,
                "columnNumber": 280
              },
              {
                "functionName": "f",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 820,
                "columnNumber": 441
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 428
              },
              {
                "functionName": "Sl",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 318,
                "columnNumber": 75
              },
              {
                "functionName": "op",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 347,
                "columnNumber": 240
              },
              {
                "functionName": "RN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 414
              },
              {
                "functionName": "u",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 269
              },
              {
                "functionName": "vo",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 337,
                "columnNumber": 647
              },
              {
                "functionName": "pD",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 368
              },
              {
                "functionName": "nD.flush",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 627,
                "columnNumber": 80
              },
              {
                "functionName": "nD.push",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 625,
                "columnNumber": 378
              },
              {
                "functionName": "xD",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 629,
                "columnNumber": 626
              },
              {
                "functionName": "YD.event",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 645,
                "columnNumber": 309
              },
              {
                "functionName": "NE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 657,
                "columnNumber": 384
              },
              {
                "functionName": "OE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 659,
                "columnNumber": 188
              },
              {
                "functionName": "Im",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 895,
                "columnNumber": 0
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 312
              },
              {
                "functionName": "c",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 896,
                "columnNumber": 129
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 276
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 281
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 900,
                "columnNumber": 2
              }
            ],
            "parent": {
              "description": "PendingScript",
              "callFrames": [
                {
                  "functionName": "Ls",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 241,
                  "columnNumber": 251
                },
                {
                  "functionName": "Xc",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 231,
                  "columnNumber": 406
                },
                {
                  "functionName": "mo",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 413,
                  "columnNumber": 1368
                },
                {
                  "functionName": "GA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 656,
                  "columnNumber": 1735
                },
                {
                  "functionName": "bH",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 773,
                  "columnNumber": 302
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 326,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 274,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 285,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 759,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 649,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 655,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 675,
                  "columnNumber": 169
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 218,
                  "columnNumber": 124
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 359
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 99
                },
                {
                  "functionName": "VB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 680,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 736,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 737,
                  "columnNumber": 188
                },
                {
                  "functionName": "QE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 742,
                  "columnNumber": 320
                }
              ],
              "parent": {
                "description": "setTimeout",
                "callFrames": [
                  {
                    "functionName": "ed",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 233,
                    "columnNumber": 220
                  },
                  {
                    "functionName": "FE.bind",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 740,
                    "columnNumber": 313
                  },
                  {
                    "functionName": "OU",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1010,
                    "columnNumber": 491
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1014,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1016,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1020,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 96,
                      "columnNumber": 64
                    },
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 97,
                      "columnNumber": 2
                    }
                  ]
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.google.com/rmkt/collect/1026069724/?random=1785408555272&cv=11&fst=1785408555272&fmt=8&bg=ffffff&guid=ON&async=1&en=gtm.js&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&_tu=CA&data=event%3Dgtm.js%3Becomm_pagetype%3Dother&ept=68&gcp=5",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1785408555272"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555272"
            },
            {
              "name": "fmt",
              "value": "8"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "gtm.js"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "_tu",
              "value": "CA"
            },
            {
              "name": "data",
              "value": "event%3Dgtm.js%3Becomm_pagetype%3Dother"
            },
            {
              "name": "ept",
              "value": "68"
            },
            {
              "name": "gcp",
              "value": "5"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/html"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 20,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:15.287Z",
        "time": 779.0000000004511,
        "timings": {
          "blocked": 148.00000000064028,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0,
          "wait": 48.99999999947613,
          "receive": 582.0000000003347,
          "_blocked_queueing": 146.00000000064028,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "Hx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 536,
                "columnNumber": 191
              },
              {
                "functionName": "Ix.K",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 537,
                "columnNumber": 558
              },
              {
                "functionName": "Bp.sendRequest",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 350,
                "columnNumber": 736
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 479,
                "columnNumber": 466
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 348
              },
              {
                "functionName": "e",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 137
              },
              {
                "functionName": "gx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 451
              },
              {
                "functionName": "Kx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 538,
                "columnNumber": 239
              },
              {
                "functionName": "Lx.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 451
              },
              {
                "functionName": "cv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 480,
                "columnNumber": 389
              },
              {
                "functionName": "t",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1749
              },
              {
                "functionName": "bv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 477,
                "columnNumber": 1798
              },
              {
                "functionName": "fv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 256
              },
              {
                "functionName": "gv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 482,
                "columnNumber": 746
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 303
              },
              {
                "functionName": "e",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 137
              },
              {
                "functionName": "gx",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 524,
                "columnNumber": 451
              },
              {
                "functionName": "gA",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 566,
                "columnNumber": 182
              },
              {
                "functionName": "OL",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 790,
                "columnNumber": 195
              },
              {
                "functionName": "PN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 819,
                "columnNumber": 280
              },
              {
                "functionName": "f",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 820,
                "columnNumber": 441
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 428
              },
              {
                "functionName": "Sl",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 318,
                "columnNumber": 75
              },
              {
                "functionName": "op",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 347,
                "columnNumber": 240
              },
              {
                "functionName": "RN",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 822,
                "columnNumber": 414
              },
              {
                "functionName": "u",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 269
              },
              {
                "functionName": "vo",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 337,
                "columnNumber": 647
              },
              {
                "functionName": "pD",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 623,
                "columnNumber": 368
              },
              {
                "functionName": "nD.flush",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 627,
                "columnNumber": 80
              },
              {
                "functionName": "nD.push",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 625,
                "columnNumber": 378
              },
              {
                "functionName": "xD",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 629,
                "columnNumber": 626
              },
              {
                "functionName": "YD.event",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 645,
                "columnNumber": 309
              },
              {
                "functionName": "NE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 657,
                "columnNumber": 384
              },
              {
                "functionName": "OE",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 659,
                "columnNumber": 188
              },
              {
                "functionName": "Im",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 895,
                "columnNumber": 0
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 312
              },
              {
                "functionName": "c",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 896,
                "columnNumber": 129
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 276
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 898,
                "columnNumber": 281
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 900,
                "columnNumber": 2
              }
            ],
            "parent": {
              "description": "PendingScript",
              "callFrames": [
                {
                  "functionName": "Ls",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 241,
                  "columnNumber": 251
                },
                {
                  "functionName": "Xc",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 231,
                  "columnNumber": 406
                },
                {
                  "functionName": "mo",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 413,
                  "columnNumber": 1368
                },
                {
                  "functionName": "GA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 656,
                  "columnNumber": 1735
                },
                {
                  "functionName": "bH",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 773,
                  "columnNumber": 302
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 326,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 274,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 285,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 759,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 649,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 655,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 675,
                  "columnNumber": 169
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 218,
                  "columnNumber": 124
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 359
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 99
                },
                {
                  "functionName": "VB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 680,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 736,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 737,
                  "columnNumber": 188
                },
                {
                  "functionName": "QE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 742,
                  "columnNumber": 320
                }
              ],
              "parent": {
                "description": "setTimeout",
                "callFrames": [
                  {
                    "functionName": "ed",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 233,
                    "columnNumber": 220
                  },
                  {
                    "functionName": "FE.bind",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 740,
                    "columnNumber": 313
                  },
                  {
                    "functionName": "OU",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1010,
                    "columnNumber": 491
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1014,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1016,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1020,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 96,
                      "columnNumber": 64
                    },
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 97,
                      "columnNumber": 2
                    }
                  ]
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "GET",
          "url": "https://www.googleadservices.com/pagead/conversion/1026069724/?random=1785408555295&cv=11&fst=1785408555295&fmt=7&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&bttype=purchase&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oid=1434303132.1785408555&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5",
          "httpVersion": "h3",
          "headers": [
            {
              "name": ":authority",
              "value": "www.googleadservices.com"
            },
            {
              "name": ":method",
              "value": "GET"
            },
            {
              "name": ":path",
              "value": "/pagead/conversion/1026069724/?random=1785408555295&cv=11&fst=1785408555295&fmt=7&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&bttype=purchase&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oid=1434303132.1785408555&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5"
            },
            {
              "name": ":scheme",
              "value": "https"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br, zstd"
            },
            {
              "name": "accept-language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "attribution-reporting-eligible",
              "value": "trigger=navigation-source;event-source"
            },
            {
              "name": "attribution-reporting-support",
              "value": "web"
            },
            {
              "name": "cache-control",
              "value": "no-cache"
            },
            {
              "name": "origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "cross-site"
            },
            {
              "name": "sec-fetch-storage-access",
              "value": "none"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "x-browser-channel",
              "value": "stable"
            },
            {
              "name": "x-browser-copyright",
              "value": "Copyright 2026 Google LLC. All Rights Reserved."
            },
            {
              "name": "x-browser-validation",
              "value": "aIITHrVCZCAqILmQej28NTv6cPs="
            },
            {
              "name": "x-browser-year",
              "value": "2026"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1785408555295"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555295"
            },
            {
              "name": "fmt",
              "value": "7"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "conversion"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "label",
              "value": "xmdjCPnKxf4bENypoukD"
            },
            {
              "name": "capi",
              "value": "1"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "bttype",
              "value": "purchase"
            },
            {
              "name": "value",
              "value": "190"
            },
            {
              "name": "currency_code",
              "value": "EUR"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "ec_mode",
              "value": "a"
            },
            {
              "name": "oid",
              "value": "1434303132.1785408555"
            },
            {
              "name": "oidsrc",
              "value": "3"
            },
            {
              "name": "ecsid2",
              "value": "1820811871.1785408188"
            },
            {
              "name": "_tu",
              "value": "CBA"
            },
            {
              "name": "gcl_ctr",
              "value": "2~0~0~0"
            },
            {
              "name": "category",
              "value": "acrcp_v1_512"
            },
            {
              "name": "em",
              "value": "tv.1"
            },
            {
              "name": "emd",
              "value": "tvd.1"
            },
            {
              "name": "ept",
              "value": "5"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "access-control-allow-credentials",
              "value": "true"
            },
            {
              "name": "access-control-allow-origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "alt-svc",
              "value": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000"
            },
            {
              "name": "cache-control",
              "value": "no-cache, must-revalidate"
            },
            {
              "name": "content-disposition",
              "value": "attachment; filename=\"f.txt\""
            },
            {
              "name": "content-encoding",
              "value": "br"
            },
            {
              "name": "content-length",
              "value": "1331"
            },
            {
              "name": "content-type",
              "value": "application/json; charset=UTF-8"
            },
            {
              "name": "cross-origin-resource-policy",
              "value": "cross-origin"
            },
            {
              "name": "date",
              "value": "Thu, 30 Jul 2026 10:49:15 GMT"
            },
            {
              "name": "expires",
              "value": "Fri, 01 Jan 1990 00:00:00 GMT"
            },
            {
              "name": "p3p",
              "value": "policyref=\"https://www.googleadservices.com/pagead/p3p.xml\", CP=\"NOI DEV PSA PSD IVA IVD OTP OUR OTR IND OTC\""
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "server",
              "value": "cafe"
            },
            {
              "name": "timing-allow-origin",
              "value": "*"
            },
            {
              "name": "x-content-type-options",
              "value": "nosniff"
            },
            {
              "name": "x-xss-protection",
              "value": "0"
            }
          ],
          "cookies": [],
          "content": {
            "size": 3784,
            "mimeType": "application/json",
            "text": "event: message\ndata: {\"fetch\":[\"https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCFxZYTfnbhBxurkybJ2bBTygKGDpQspqJtg&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA\"],\"options\":{\"fallback_url\":\"https://www.google.com/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCFxZYTfnbhBxurkybJ2bBTygKGDpQspqJtg&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA&gcp=3\",\"fallback_url_method\":\"fetch\"}}\n\n"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 1357,
          "_error": null,
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.98.157",
        "startedDateTime": "2026-07-30T10:49:15.349Z",
        "time": 530.0000000008004,
        "timings": {
          "blocked": 321.00000000080036,
          "dns": 35,
          "ssl": 116,
          "connect": 151,
          "send": 0,
          "wait": 0.9999999991559889,
          "receive": 22.00000000084401,
          "_blocked_queueing": 245.00000000080036,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "144648",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 164,
                "columnNumber": 390
              },
              {
                "functionName": "lo",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 335,
                "columnNumber": 1283
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 292
              },
              {
                "functionName": "f",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 175
              },
              {
                "functionName": "lv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 276
              },
              {
                "functionName": "mv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 485,
                "columnNumber": 399
              }
            ],
            "parent": {
              "description": "PendingScript",
              "callFrames": [
                {
                  "functionName": "Ls",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 241,
                  "columnNumber": 251
                },
                {
                  "functionName": "Xc",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 231,
                  "columnNumber": 406
                },
                {
                  "functionName": "mo",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 413,
                  "columnNumber": 1368
                },
                {
                  "functionName": "GA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 656,
                  "columnNumber": 1735
                },
                {
                  "functionName": "bH",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 773,
                  "columnNumber": 302
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 326,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 274,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 285,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 759,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 649,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 655,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 675,
                  "columnNumber": 169
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 218,
                  "columnNumber": 124
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 359
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 99
                },
                {
                  "functionName": "VB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 680,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 736,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 737,
                  "columnNumber": 188
                },
                {
                  "functionName": "QE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 742,
                  "columnNumber": 320
                }
              ],
              "parent": {
                "description": "setTimeout",
                "callFrames": [
                  {
                    "functionName": "ed",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 233,
                    "columnNumber": 220
                  },
                  {
                    "functionName": "FE.bind",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 740,
                    "columnNumber": 313
                  },
                  {
                    "functionName": "OU",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1010,
                    "columnNumber": 491
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1014,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1016,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1020,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 96,
                      "columnNumber": 64
                    },
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 97,
                      "columnNumber": 2
                    }
                  ]
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.google.com/ccm/collect?rcb=5&frm=0&auid=2132767939.1785405308&dt=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&en=page_view&dl=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&dr=www.professionele-koeling.nl&scrsrc=www.googletagmanager.com&rnd=1166332829.1785408554&navt=n&npa=0&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xec&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&apvc=0&tids=AW-1026069724&tid=AW-1026069724&tft=1785408555353&tfd=4531&fmt=8",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            }
          ],
          "queryString": [
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "dt",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "en",
              "value": "page_view"
            },
            {
              "name": "dl",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "dr",
              "value": "www.professionele-koeling.nl"
            },
            {
              "name": "scrsrc",
              "value": "www.googletagmanager.com"
            },
            {
              "name": "rnd",
              "value": "1166332829.1785408554"
            },
            {
              "name": "navt",
              "value": "n"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xec"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "apvc",
              "value": "0"
            },
            {
              "name": "tids",
              "value": "AW-1026069724"
            },
            {
              "name": "tid",
              "value": "AW-1026069724"
            },
            {
              "name": "tft",
              "value": "1785408555353"
            },
            {
              "name": "tfd",
              "value": "4531"
            },
            {
              "name": "fmt",
              "value": "8"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/plain"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 21,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:15.354Z",
        "time": 713.000000001557,
        "timings": {
          "blocked": 313.50000000068394,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0,
          "wait": 134.99999999973807,
          "receive": 264.50000000113505,
          "_blocked_queueing": 235.50000000068394,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 164,
                "columnNumber": 390
              },
              {
                "functionName": "lo",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 335,
                "columnNumber": 1283
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 292
              },
              {
                "functionName": "f",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 175
              },
              {
                "functionName": "lv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 486,
                "columnNumber": 276
              },
              {
                "functionName": "mv",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 485,
                "columnNumber": 399
              }
            ],
            "parent": {
              "description": "PendingScript",
              "callFrames": [
                {
                  "functionName": "Ls",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 241,
                  "columnNumber": 251
                },
                {
                  "functionName": "Xc",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 231,
                  "columnNumber": 406
                },
                {
                  "functionName": "mo",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 413,
                  "columnNumber": 1368
                },
                {
                  "functionName": "GA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 656,
                  "columnNumber": 1735
                },
                {
                  "functionName": "bH",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 773,
                  "columnNumber": 302
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 326,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 274,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 250,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 213,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 285,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 759,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 649,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 655,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 675,
                  "columnNumber": 169
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 218,
                  "columnNumber": 124
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 359
                },
                {
                  "functionName": "",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 99
                },
                {
                  "functionName": "VB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 676,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 680,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 736,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 737,
                  "columnNumber": 188
                },
                {
                  "functionName": "QE",
                  "scriptId": "413",
                  "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                  "lineNumber": 742,
                  "columnNumber": 320
                }
              ],
              "parent": {
                "description": "setTimeout",
                "callFrames": [
                  {
                    "functionName": "ed",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 233,
                    "columnNumber": 220
                  },
                  {
                    "functionName": "FE.bind",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 740,
                    "columnNumber": 313
                  },
                  {
                    "functionName": "OU",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1010,
                    "columnNumber": 491
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1014,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1016,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1018,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 1020,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 96,
                      "columnNumber": 64
                    },
                    {
                      "functionName": "",
                      "scriptId": "398",
                      "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                      "lineNumber": 97,
                      "columnNumber": 2
                    }
                  ]
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.google.com/ccm/collect?rcb=5&frm=0&ae=g&auid=2132767939.1785405308&dt=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&en=gtm.js&dl=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&dr=www.professionele-koeling.nl&scrsrc=www.googletagmanager.com&rnd=1166332829.1785408554&navt=n&npa=0&ep.ecomm_prodid=&ep.ecomm_pagetype=other&_tu=CA&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&apvc=0&tids=AW-1026069724&tid=AW-1026069724&tft=1785408555355&tfd=4533&fmt=8",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            }
          ],
          "queryString": [
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "ae",
              "value": "g"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "dt",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "en",
              "value": "gtm.js"
            },
            {
              "name": "dl",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "dr",
              "value": "www.professionele-koeling.nl"
            },
            {
              "name": "scrsrc",
              "value": "www.googletagmanager.com"
            },
            {
              "name": "rnd",
              "value": "1166332829.1785408554"
            },
            {
              "name": "navt",
              "value": "n"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "ep.ecomm_prodid",
              "value": ""
            },
            {
              "name": "ep.ecomm_pagetype",
              "value": "other"
            },
            {
              "name": "_tu",
              "value": "CA"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "apvc",
              "value": "0"
            },
            {
              "name": "tids",
              "value": "AW-1026069724"
            },
            {
              "name": "tid",
              "value": "AW-1026069724"
            },
            {
              "name": "tft",
              "value": "1785408555355"
            },
            {
              "name": "tfd",
              "value": "4533"
            },
            {
              "name": "fmt",
              "value": "8"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/plain"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 21,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:15.355Z",
        "time": 712.0000000013533,
        "timings": {
          "blocked": 285.00000000062573,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 1,
          "wait": 132.9999999992433,
          "receive": 293.0000000014843,
          "_blocked_queueing": 262.00000000062573,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 164,
                "columnNumber": 390
              },
              {
                "functionName": "Tx.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1030
              },
              {
                "functionName": "Ux.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1153
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 248,
                "columnNumber": 30
              },
              {
                "functionName": "ch",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 441
              },
              {
                "functionName": "ah",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 672
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 537,
                "columnNumber": 144
              }
            ],
            "parent": {
              "description": "Promise.then",
              "callFrames": [
                {
                  "functionName": "q",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 335
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 537,
                  "columnNumber": 261
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 289
                }
              ],
              "parent": {
                "description": "Promise.then",
                "callFrames": [
                  {
                    "functionName": "Hx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 536,
                    "columnNumber": 202
                  },
                  {
                    "functionName": "Ix.K",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 537,
                    "columnNumber": 558
                  },
                  {
                    "functionName": "Bp.sendRequest",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 350,
                    "columnNumber": 736
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 479,
                    "columnNumber": 466
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 348
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "Kx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 538,
                    "columnNumber": 239
                  },
                  {
                    "functionName": "Lx.H",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "cv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 480,
                    "columnNumber": 389
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1749
                  },
                  {
                    "functionName": "bv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1798
                  },
                  {
                    "functionName": "fv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 256
                  },
                  {
                    "functionName": "gv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 746
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "gA",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 182
                  },
                  {
                    "functionName": "OL",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 790,
                    "columnNumber": 195
                  },
                  {
                    "functionName": "PN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 819,
                    "columnNumber": 280
                  },
                  {
                    "functionName": "f",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 820,
                    "columnNumber": 441
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 428
                  },
                  {
                    "functionName": "Sl",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 318,
                    "columnNumber": 75
                  },
                  {
                    "functionName": "op",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 347,
                    "columnNumber": 240
                  },
                  {
                    "functionName": "RN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 414
                  },
                  {
                    "functionName": "u",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 269
                  },
                  {
                    "functionName": "vo",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 337,
                    "columnNumber": 647
                  },
                  {
                    "functionName": "pD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 368
                  },
                  {
                    "functionName": "nD.flush",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 627,
                    "columnNumber": 80
                  },
                  {
                    "functionName": "nD.push",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 625,
                    "columnNumber": 378
                  },
                  {
                    "functionName": "xD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 629,
                    "columnNumber": 626
                  },
                  {
                    "functionName": "YD.event",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 645,
                    "columnNumber": 309
                  },
                  {
                    "functionName": "NE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 657,
                    "columnNumber": 384
                  },
                  {
                    "functionName": "OE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 659,
                    "columnNumber": 188
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 895,
                    "columnNumber": 0
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 896,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 900,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "Ls",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 241,
                      "columnNumber": 251
                    },
                    {
                      "functionName": "Xc",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 231,
                      "columnNumber": 406
                    },
                    {
                      "functionName": "mo",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 413,
                      "columnNumber": 1368
                    },
                    {
                      "functionName": "GA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 656,
                      "columnNumber": 1735
                    },
                    {
                      "functionName": "bH",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 773,
                      "columnNumber": 302
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 326,
                      "columnNumber": 186
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "fb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 461
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 274,
                      "columnNumber": 472
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "l.Sq",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 1276
                    },
                    {
                      "functionName": "sf",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 285,
                      "columnNumber": 959
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 759,
                      "columnNumber": 6
                    },
                    {
                      "functionName": "pA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 649,
                      "columnNumber": 495
                    },
                    {
                      "functionName": "wA.evaluate",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 655,
                      "columnNumber": 288
                    },
                    {
                      "functionName": "e",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 675,
                      "columnNumber": 169
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 218,
                      "columnNumber": 124
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 359
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 99
                    },
                    {
                      "functionName": "VB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 741
                    },
                    {
                      "functionName": "YB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 680,
                      "columnNumber": 217
                    },
                    {
                      "functionName": "NE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 736,
                      "columnNumber": 244
                    },
                    {
                      "functionName": "OE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 737,
                      "columnNumber": 188
                    },
                    {
                      "functionName": "QE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 742,
                      "columnNumber": 320
                    }
                  ],
                  "parent": {
                    "description": "setTimeout",
                    "callFrames": [
                      {
                        "functionName": "ed",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 233,
                        "columnNumber": 220
                      },
                      {
                        "functionName": "FE.bind",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 740,
                        "columnNumber": 313
                      },
                      {
                        "functionName": "OU",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1010,
                        "columnNumber": 491
                      },
                      {
                        "functionName": "Im",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1014,
                        "columnNumber": 303
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 312
                      },
                      {
                        "functionName": "c",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1016,
                        "columnNumber": 129
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 276
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 281
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1020,
                        "columnNumber": 2
                      }
                    ],
                    "parent": {
                      "description": "PendingScript",
                      "callFrames": [
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 96,
                          "columnNumber": 64
                        },
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 97,
                          "columnNumber": 2
                        }
                      ]
                    }
                  }
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://googleads.g.doubleclick.net/pagead/viewthroughconversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCFxZYTfnbhBxurkybJ2bBTygKGDpQspqJtg&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA",
          "httpVersion": "h3",
          "headers": [
            {
              "name": ":authority",
              "value": "googleads.g.doubleclick.net"
            },
            {
              "name": ":method",
              "value": "POST"
            },
            {
              "name": ":path",
              "value": "/pagead/viewthroughconversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCFxZYTfnbhBxurkybJ2bBTygKGDpQspqJtg&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA"
            },
            {
              "name": ":scheme",
              "value": "https"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br, zstd"
            },
            {
              "name": "accept-language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "cache-control",
              "value": "no-cache"
            },
            {
              "name": "content-length",
              "value": "0"
            },
            {
              "name": "origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "no-cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "cross-site"
            },
            {
              "name": "sec-fetch-storage-access",
              "value": "none"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "x-browser-channel",
              "value": "stable"
            },
            {
              "name": "x-browser-copyright",
              "value": "Copyright 2026 Google LLC. All Rights Reserved."
            },
            {
              "name": "x-browser-validation",
              "value": "aIITHrVCZCAqILmQej28NTv6cPs="
            },
            {
              "name": "x-browser-year",
              "value": "2026"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1944658571"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555295"
            },
            {
              "name": "fmt",
              "value": "8"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "conversion"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "label",
              "value": "xmdjCPnKxf4bENypoukD"
            },
            {
              "name": "capi",
              "value": "1"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "value",
              "value": "190"
            },
            {
              "name": "currency_code",
              "value": "EUR"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "ec_mode",
              "value": "a"
            },
            {
              "name": "oidsrc",
              "value": "3"
            },
            {
              "name": "ecsid2",
              "value": "1820811871.1785408188"
            },
            {
              "name": "_tu",
              "value": "CBA"
            },
            {
              "name": "gcl_ctr",
              "value": "2~0~0~0"
            },
            {
              "name": "category",
              "value": "acrcp_v1_512"
            },
            {
              "name": "em",
              "value": "tv.1"
            },
            {
              "name": "emd",
              "value": "tvd.1"
            },
            {
              "name": "ept",
              "value": "5"
            },
            {
              "name": "ct_cookie_present",
              "value": "false"
            },
            {
              "name": "eoid",
              "value": "CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE"
            },
            {
              "name": "crd",
              "value": "CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM"
            },
            {
              "name": "cerd",
              "value": "Cgzr370tpqe-Lf-vvi0"
            },
            {
              "name": "eitems",
              "value": "ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCFxZYTfnbhBxurkybJ2bBTygKGDpQspqJtg"
            },
            {
              "name": "fsk",
              "value": "ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4"
            },
            {
              "name": "pscrd",
              "value": "IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 302,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "access-control-allow-credentials",
              "value": "true"
            },
            {
              "name": "access-control-allow-origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "alt-svc",
              "value": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000"
            },
            {
              "name": "cache-control",
              "value": "no-cache, must-revalidate"
            },
            {
              "name": "content-length",
              "value": "0"
            },
            {
              "name": "content-type",
              "value": "text/html; charset=UTF-8"
            },
            {
              "name": "cross-origin-resource-policy",
              "value": "cross-origin"
            },
            {
              "name": "date",
              "value": "Thu, 30 Jul 2026 10:49:16 GMT"
            },
            {
              "name": "expires",
              "value": "Fri, 01 Jan 1990 00:00:00 GMT"
            },
            {
              "name": "location",
              "value": "https://www.google.com/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205"
            },
            {
              "name": "p3p",
              "value": "policyref=\"https://googleads.g.doubleclick.net/pagead/gcn_p3p_.xml\", CP=\"CURa ADMa DEVa TAIo PSAo PSDo OUR IND UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR\""
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "server",
              "value": "cafe"
            },
            {
              "name": "timing-allow-origin",
              "value": "*"
            },
            {
              "name": "x-content-type-options",
              "value": "nosniff"
            },
            {
              "name": "x-xss-protection",
              "value": "0"
            }
          ],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/html"
          },
          "redirectURL": "https://www.google.com/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 23,
          "_error": null,
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.250.109.157",
        "startedDateTime": "2026-07-30T10:49:16.068Z",
        "time": 457.0000000003347,
        "timings": {
          "blocked": 184.0000000000873,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0,
          "wait": 72.99999999951979,
          "receive": 200.0000000007276,
          "_blocked_queueing": 179.0000000000873,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143517",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 164,
                "columnNumber": 390
              },
              {
                "functionName": "Tx.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1030
              },
              {
                "functionName": "Ux.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1153
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 248,
                "columnNumber": 30
              },
              {
                "functionName": "ch",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 441
              },
              {
                "functionName": "ah",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 672
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 537,
                "columnNumber": 144
              }
            ],
            "parent": {
              "description": "Promise.then",
              "callFrames": [
                {
                  "functionName": "q",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 335
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 537,
                  "columnNumber": 261
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 289
                }
              ],
              "parent": {
                "description": "Promise.then",
                "callFrames": [
                  {
                    "functionName": "Hx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 536,
                    "columnNumber": 202
                  },
                  {
                    "functionName": "Ix.K",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 537,
                    "columnNumber": 558
                  },
                  {
                    "functionName": "Bp.sendRequest",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 350,
                    "columnNumber": 736
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 479,
                    "columnNumber": 466
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 348
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "Kx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 538,
                    "columnNumber": 239
                  },
                  {
                    "functionName": "Lx.H",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "cv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 480,
                    "columnNumber": 389
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1749
                  },
                  {
                    "functionName": "bv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1798
                  },
                  {
                    "functionName": "fv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 256
                  },
                  {
                    "functionName": "gv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 746
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "gA",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 182
                  },
                  {
                    "functionName": "OL",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 790,
                    "columnNumber": 195
                  },
                  {
                    "functionName": "PN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 819,
                    "columnNumber": 280
                  },
                  {
                    "functionName": "f",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 820,
                    "columnNumber": 441
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 428
                  },
                  {
                    "functionName": "Sl",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 318,
                    "columnNumber": 75
                  },
                  {
                    "functionName": "op",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 347,
                    "columnNumber": 240
                  },
                  {
                    "functionName": "RN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 414
                  },
                  {
                    "functionName": "u",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 269
                  },
                  {
                    "functionName": "vo",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 337,
                    "columnNumber": 647
                  },
                  {
                    "functionName": "pD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 368
                  },
                  {
                    "functionName": "nD.flush",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 627,
                    "columnNumber": 80
                  },
                  {
                    "functionName": "nD.push",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 625,
                    "columnNumber": 378
                  },
                  {
                    "functionName": "xD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 629,
                    "columnNumber": 626
                  },
                  {
                    "functionName": "YD.event",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 645,
                    "columnNumber": 309
                  },
                  {
                    "functionName": "NE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 657,
                    "columnNumber": 384
                  },
                  {
                    "functionName": "OE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 659,
                    "columnNumber": 188
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 895,
                    "columnNumber": 0
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 896,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 900,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "Ls",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 241,
                      "columnNumber": 251
                    },
                    {
                      "functionName": "Xc",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 231,
                      "columnNumber": 406
                    },
                    {
                      "functionName": "mo",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 413,
                      "columnNumber": 1368
                    },
                    {
                      "functionName": "GA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 656,
                      "columnNumber": 1735
                    },
                    {
                      "functionName": "bH",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 773,
                      "columnNumber": 302
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 326,
                      "columnNumber": 186
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "fb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 461
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 274,
                      "columnNumber": 472
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "l.Sq",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 1276
                    },
                    {
                      "functionName": "sf",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 285,
                      "columnNumber": 959
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 759,
                      "columnNumber": 6
                    },
                    {
                      "functionName": "pA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 649,
                      "columnNumber": 495
                    },
                    {
                      "functionName": "wA.evaluate",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 655,
                      "columnNumber": 288
                    },
                    {
                      "functionName": "e",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 675,
                      "columnNumber": 169
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 218,
                      "columnNumber": 124
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 359
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 99
                    },
                    {
                      "functionName": "VB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 741
                    },
                    {
                      "functionName": "YB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 680,
                      "columnNumber": 217
                    },
                    {
                      "functionName": "NE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 736,
                      "columnNumber": 244
                    },
                    {
                      "functionName": "OE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 737,
                      "columnNumber": 188
                    },
                    {
                      "functionName": "QE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 742,
                      "columnNumber": 320
                    }
                  ],
                  "parent": {
                    "description": "setTimeout",
                    "callFrames": [
                      {
                        "functionName": "ed",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 233,
                        "columnNumber": 220
                      },
                      {
                        "functionName": "FE.bind",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 740,
                        "columnNumber": 313
                      },
                      {
                        "functionName": "OU",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1010,
                        "columnNumber": 491
                      },
                      {
                        "functionName": "Im",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1014,
                        "columnNumber": 303
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 312
                      },
                      {
                        "functionName": "c",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1016,
                        "columnNumber": 129
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 276
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 281
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1020,
                        "columnNumber": 2
                      }
                    ],
                    "parent": {
                      "description": "PendingScript",
                      "callFrames": [
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 96,
                          "columnNumber": 64
                        },
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 97,
                          "columnNumber": 2
                        }
                      ]
                    }
                  }
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "GET",
          "url": "https://www.google.com/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205",
          "httpVersion": "h3",
          "headers": [
            {
              "name": ":authority",
              "value": "www.google.com"
            },
            {
              "name": ":method",
              "value": "GET"
            },
            {
              "name": ":path",
              "value": "/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205"
            },
            {
              "name": ":scheme",
              "value": "https"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br, zstd"
            },
            {
              "name": "accept-language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "cache-control",
              "value": "no-cache"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "no-cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "cross-site"
            },
            {
              "name": "sec-fetch-storage-access",
              "value": "none"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "x-browser-channel",
              "value": "stable"
            },
            {
              "name": "x-browser-copyright",
              "value": "Copyright 2026 Google LLC. All Rights Reserved."
            },
            {
              "name": "x-browser-validation",
              "value": "aIITHrVCZCAqILmQej28NTv6cPs="
            },
            {
              "name": "x-browser-year",
              "value": "2026"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1944658571"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555295"
            },
            {
              "name": "fmt",
              "value": "8"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "conversion"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "label",
              "value": "xmdjCPnKxf4bENypoukD"
            },
            {
              "name": "capi",
              "value": "1"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "value",
              "value": "190"
            },
            {
              "name": "currency_code",
              "value": "EUR"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "ec_mode",
              "value": "a"
            },
            {
              "name": "oidsrc",
              "value": "3"
            },
            {
              "name": "ecsid2",
              "value": "1820811871.1785408188"
            },
            {
              "name": "_tu",
              "value": "CBA"
            },
            {
              "name": "gcl_ctr",
              "value": "2~0~0~0"
            },
            {
              "name": "category",
              "value": "acrcp_v1_512"
            },
            {
              "name": "em",
              "value": "tv.1"
            },
            {
              "name": "emd",
              "value": "tvd.1"
            },
            {
              "name": "ept",
              "value": "5"
            },
            {
              "name": "ct_cookie_present",
              "value": "false"
            },
            {
              "name": "eoid",
              "value": "CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE"
            },
            {
              "name": "crd",
              "value": "CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM"
            },
            {
              "name": "cerd",
              "value": "Cgzr370tpqe-Lf-vvi0"
            },
            {
              "name": "fsk",
              "value": "ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4"
            },
            {
              "name": "pscrd",
              "value": "IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAA"
            },
            {
              "name": "is_vtc",
              "value": "1"
            },
            {
              "name": "cid",
              "value": "CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz"
            },
            {
              "name": "eitems",
              "value": "ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg"
            },
            {
              "name": "random",
              "value": "2245041205"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 302,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "alt-svc",
              "value": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000"
            },
            {
              "name": "cache-control",
              "value": "no-cache, no-store, must-revalidate"
            },
            {
              "name": "content-length",
              "value": "0"
            },
            {
              "name": "content-security-policy",
              "value": "script-src 'none'; object-src 'none'"
            },
            {
              "name": "content-type",
              "value": "text/html; charset=UTF-8"
            },
            {
              "name": "cross-origin-resource-policy",
              "value": "cross-origin"
            },
            {
              "name": "date",
              "value": "Thu, 30 Jul 2026 10:49:16 GMT"
            },
            {
              "name": "expires",
              "value": "Fri, 01 Jan 1990 00:00:00 GMT"
            },
            {
              "name": "location",
              "value": "https://www.google.com.ua/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205&ipr=y&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAIIBBXABiAEB"
            },
            {
              "name": "p3p",
              "value": "policyref=\"https://www.googleadservices.com/pagead/p3p.xml\", CP=\"NOI DEV PSA PSD IVA IVD OTP OUR OTR IND OTC\""
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "server",
              "value": "cafe"
            },
            {
              "name": "timing-allow-origin",
              "value": "*"
            },
            {
              "name": "x-content-type-options",
              "value": "nosniff"
            },
            {
              "name": "x-xss-protection",
              "value": "0"
            }
          ],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/html"
          },
          "redirectURL": "https://www.google.com.ua/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205&ipr=y&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAIIBBXABiAEB",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 22,
          "_error": null,
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.251.157.119",
        "startedDateTime": "2026-07-30T10:49:16.546Z",
        "time": 0.6339999995260732,
        "timings": {
          "blocked": -0.996,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0.009,
          "wait": 0.5979999994805548,
          "receive": 0.02700000004551839,
          "_blocked_queueing": -1,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "143483",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 164,
                "columnNumber": 390
              },
              {
                "functionName": "Tx.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1030
              },
              {
                "functionName": "Ux.H",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 539,
                "columnNumber": 1153
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 248,
                "columnNumber": 30
              },
              {
                "functionName": "ch",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 441
              },
              {
                "functionName": "ah",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 247,
                "columnNumber": 672
              },
              {
                "functionName": "",
                "scriptId": "438",
                "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                "lineNumber": 537,
                "columnNumber": 144
              }
            ],
            "parent": {
              "description": "Promise.then",
              "callFrames": [
                {
                  "functionName": "q",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 335
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 537,
                  "columnNumber": 261
                },
                {
                  "functionName": "",
                  "scriptId": "438",
                  "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                  "lineNumber": 536,
                  "columnNumber": 289
                }
              ],
              "parent": {
                "description": "Promise.then",
                "callFrames": [
                  {
                    "functionName": "Hx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 536,
                    "columnNumber": 202
                  },
                  {
                    "functionName": "Ix.K",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 537,
                    "columnNumber": 558
                  },
                  {
                    "functionName": "Bp.sendRequest",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 350,
                    "columnNumber": 736
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 479,
                    "columnNumber": 466
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 348
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "Kx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 538,
                    "columnNumber": 239
                  },
                  {
                    "functionName": "Lx.H",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 539,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "cv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 480,
                    "columnNumber": 389
                  },
                  {
                    "functionName": "t",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1749
                  },
                  {
                    "functionName": "bv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 477,
                    "columnNumber": 1798
                  },
                  {
                    "functionName": "fv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 256
                  },
                  {
                    "functionName": "gv",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 482,
                    "columnNumber": 746
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 303
                  },
                  {
                    "functionName": "e",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 137
                  },
                  {
                    "functionName": "gx",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 524,
                    "columnNumber": 451
                  },
                  {
                    "functionName": "gA",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 566,
                    "columnNumber": 182
                  },
                  {
                    "functionName": "OL",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 790,
                    "columnNumber": 195
                  },
                  {
                    "functionName": "PN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 819,
                    "columnNumber": 280
                  },
                  {
                    "functionName": "f",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 820,
                    "columnNumber": 441
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 428
                  },
                  {
                    "functionName": "Sl",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 318,
                    "columnNumber": 75
                  },
                  {
                    "functionName": "op",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 347,
                    "columnNumber": 240
                  },
                  {
                    "functionName": "RN",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 822,
                    "columnNumber": 414
                  },
                  {
                    "functionName": "u",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 269
                  },
                  {
                    "functionName": "vo",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 337,
                    "columnNumber": 647
                  },
                  {
                    "functionName": "pD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 623,
                    "columnNumber": 368
                  },
                  {
                    "functionName": "nD.flush",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 627,
                    "columnNumber": 80
                  },
                  {
                    "functionName": "nD.push",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 625,
                    "columnNumber": 378
                  },
                  {
                    "functionName": "xD",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 629,
                    "columnNumber": 626
                  },
                  {
                    "functionName": "YD.event",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 645,
                    "columnNumber": 309
                  },
                  {
                    "functionName": "NE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 657,
                    "columnNumber": 384
                  },
                  {
                    "functionName": "OE",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 659,
                    "columnNumber": 188
                  },
                  {
                    "functionName": "Im",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 895,
                    "columnNumber": 0
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 312
                  },
                  {
                    "functionName": "c",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 896,
                    "columnNumber": 129
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 276
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 898,
                    "columnNumber": 281
                  },
                  {
                    "functionName": "",
                    "scriptId": "438",
                    "url": "https://www.googletagmanager.com/gtag/js?id=AW-1026069724&cx=c&gtm=4e67s1",
                    "lineNumber": 900,
                    "columnNumber": 2
                  }
                ],
                "parent": {
                  "description": "PendingScript",
                  "callFrames": [
                    {
                      "functionName": "Ls",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 241,
                      "columnNumber": 251
                    },
                    {
                      "functionName": "Xc",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 231,
                      "columnNumber": 406
                    },
                    {
                      "functionName": "mo",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 413,
                      "columnNumber": 1368
                    },
                    {
                      "functionName": "GA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 656,
                      "columnNumber": 1735
                    },
                    {
                      "functionName": "bH",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 773,
                      "columnNumber": 302
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 326,
                      "columnNumber": 186
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "fb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 461
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 274,
                      "columnNumber": 472
                    },
                    {
                      "functionName": "l.apply",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 250,
                      "columnNumber": 464
                    },
                    {
                      "functionName": "gb",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 710
                    },
                    {
                      "functionName": "l.Sq",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 213,
                      "columnNumber": 1276
                    },
                    {
                      "functionName": "sf",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 285,
                      "columnNumber": 959
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 759,
                      "columnNumber": 6
                    },
                    {
                      "functionName": "pA",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 649,
                      "columnNumber": 495
                    },
                    {
                      "functionName": "wA.evaluate",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 655,
                      "columnNumber": 288
                    },
                    {
                      "functionName": "e",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 675,
                      "columnNumber": 169
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 218,
                      "columnNumber": 124
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 359
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 99
                    },
                    {
                      "functionName": "VB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 676,
                      "columnNumber": 741
                    },
                    {
                      "functionName": "YB",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 680,
                      "columnNumber": 217
                    },
                    {
                      "functionName": "NE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 736,
                      "columnNumber": 244
                    },
                    {
                      "functionName": "OE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 737,
                      "columnNumber": 188
                    },
                    {
                      "functionName": "QE",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 742,
                      "columnNumber": 320
                    }
                  ],
                  "parent": {
                    "description": "setTimeout",
                    "callFrames": [
                      {
                        "functionName": "ed",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 233,
                        "columnNumber": 220
                      },
                      {
                        "functionName": "FE.bind",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 740,
                        "columnNumber": 313
                      },
                      {
                        "functionName": "OU",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1010,
                        "columnNumber": 491
                      },
                      {
                        "functionName": "Im",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1014,
                        "columnNumber": 303
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 312
                      },
                      {
                        "functionName": "c",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1016,
                        "columnNumber": 129
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 276
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1018,
                        "columnNumber": 281
                      },
                      {
                        "functionName": "",
                        "scriptId": "413",
                        "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                        "lineNumber": 1020,
                        "columnNumber": 2
                      }
                    ],
                    "parent": {
                      "description": "PendingScript",
                      "callFrames": [
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 96,
                          "columnNumber": 64
                        },
                        {
                          "functionName": "",
                          "scriptId": "398",
                          "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                          "lineNumber": 97,
                          "columnNumber": 2
                        }
                      ]
                    }
                  }
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "GET",
          "url": "https://www.google.com.ua/pagead/1p-conversion/1026069724/?random=1944658571&cv=11&fst=1785408555295&fmt=8&bg=ffffff&guid=ON&async=1&en=conversion&gtm=45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=115938466~115938469~118897920~118897930~119896803&u_w=1536&u_h=864&url=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&ref=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&rcb=5&label=xmdjCPnKxf4bENypoukD&capi=1&frm=0&tiba=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&value=190&currency_code=EUR&hn=www.googleadservices.com&npa=0&pscdl=noapi&auid=2132767939.1785405308&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uamb=0&uam=&uap=Windows&uapv=10.0.0&uaw=0&ec_mode=a&oidsrc=3&ecsid2=1820811871.1785408188&_tu=CBA&gcl_ctr=2~0~0~0&category=acrcp_v1_512&em=tv.1&emd=tvd.1&ept=5&ct_cookie_present=false&eoid=CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE&crd=CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM&cerd=Cgzr370tpqe-Lf-vvi0&fsk=ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4&is_vtc=1&cid=CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz&eitems=ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg&random=2245041205&ipr=y&pscrd=IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAIIBBXABiAEB",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "Referer",
              "value": "https://www.professionele-koeling.nl/"
            }
          ],
          "queryString": [
            {
              "name": "random",
              "value": "1944658571"
            },
            {
              "name": "cv",
              "value": "11"
            },
            {
              "name": "fst",
              "value": "1785408555295"
            },
            {
              "name": "fmt",
              "value": "8"
            },
            {
              "name": "bg",
              "value": "ffffff"
            },
            {
              "name": "guid",
              "value": "ON"
            },
            {
              "name": "async",
              "value": "1"
            },
            {
              "name": "en",
              "value": "conversion"
            },
            {
              "name": "gtm",
              "value": "45be67s1v9200365167z89243950528za20gzb9243950528zd9243950528xea"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "tag_exp",
              "value": "115938466~115938469~118897920~118897930~119896803"
            },
            {
              "name": "u_w",
              "value": "1536"
            },
            {
              "name": "u_h",
              "value": "864"
            },
            {
              "name": "url",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "ref",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "rcb",
              "value": "5"
            },
            {
              "name": "label",
              "value": "xmdjCPnKxf4bENypoukD"
            },
            {
              "name": "capi",
              "value": "1"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "tiba",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "value",
              "value": "190"
            },
            {
              "name": "currency_code",
              "value": "EUR"
            },
            {
              "name": "hn",
              "value": "www.googleadservices.com"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "auid",
              "value": "2132767939.1785405308"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "ec_mode",
              "value": "a"
            },
            {
              "name": "oidsrc",
              "value": "3"
            },
            {
              "name": "ecsid2",
              "value": "1820811871.1785408188"
            },
            {
              "name": "_tu",
              "value": "CBA"
            },
            {
              "name": "gcl_ctr",
              "value": "2~0~0~0"
            },
            {
              "name": "category",
              "value": "acrcp_v1_512"
            },
            {
              "name": "em",
              "value": "tv.1"
            },
            {
              "name": "emd",
              "value": "tvd.1"
            },
            {
              "name": "ept",
              "value": "5"
            },
            {
              "name": "ct_cookie_present",
              "value": "false"
            },
            {
              "name": "eoid",
              "value": "CkQKEAjw7KvTBhD58vbYs-z4mzgSMAA7v4J3wpp2sxxZRbFh5Ar5DOIVOhqDVk6vR9mB-WqslSR9Cu-RldZh7hApcQNwBvD_BwE"
            },
            {
              "name": "crd",
              "value": "CLTesQII8t-xAgit4bECCK_hsQIIobixAgixwbECCLDBsQIIscOxAgiKxbECCMLJsQII1-ixAgi0xrECCJPasQII29yxAgiH27ECCNPFsQII68yxAgjtzrECCNXPsQII9NqxAgjJ47ECCJfUsQIIyduxAgjN5rECCLHhsQIIs-GxAgim3bECCLDesQIIgNuxAgjN4bECSiZ0cmlnZ2VyPW5hdmlnYXRpb24tc291cmNlO2V2ZW50LXNvdXJjZVoDCgEBYgMKAQM"
            },
            {
              "name": "cerd",
              "value": "Cgzr370tpqe-Lf-vvi0"
            },
            {
              "name": "fsk",
              "value": "ChAI8Oyr0wYQ39iQzMiKl_J6EiwAd30lAQSaiHVcu49cs65tUSOTQfJAU24Usb6SrIAolhssqoz0QAxLaSCb3xoC8W4"
            },
            {
              "name": "is_vtc",
              "value": "1"
            },
            {
              "name": "cid",
              "value": "CAQS0wEAEQoqgTnkjVAoppJLWTE8i2zVL9RX13abLWwE5z899DkJ8As11HLtzI30R06TubyAqPAA8KA8N58ksE3djwdHHhKCOVdY1EeZRBkTcdllGqii73FblbaRFjyz9lVhqx_1M7hJIMYPVMS5T6lh1mFHDNiThdJN2EJDE6s6UHBASb6IwPaFLvNp9BSuOWy96HWe9OB-gQ2jI3ADwy2q4g2ZsZowpfHPWU3_37NTx5KalsB-mIWL2E9crbh0Q0lb8r6Xu1bMVtPQOIibQqAOeGyO9NIz"
            },
            {
              "name": "eitems",
              "value": "ChAI8Oyr0wYQy_Lp7pWcieJzEh0AZLDCF8Ml7_K2C7JeDZ7cekkBd4QpqIHFNvNSMg"
            },
            {
              "name": "random",
              "value": "2245041205"
            },
            {
              "name": "ipr",
              "value": "y"
            },
            {
              "name": "pscrd",
              "value": "IhMIncnqlZ36lQMVaNm-CB3HhitfOiVodHRwczovL3d3dy5wcm9mZXNzaW9uZWxlLWtvZWxpbmcubmwvQldDaEFJOE95cjB3WVEycjNKbDV5TjJ2TXdFaTBBZ0gySGo4ZzJNaTlqNmZXOTUyRDN5d3psV1E4ZHMzVFhQNnNtcVFQcmd6d2Fodmo0dVFiemphb29oV016DAgJYggIABAAGAAgAIIBBXABiAEB"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/html"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 20,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.250.109.94",
        "startedDateTime": "2026-07-30T10:49:16.548Z",
        "time": 3.0000000006111804,
        "timings": {
          "blocked": 1.805999999366235,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 0.002999999999999999,
          "wait": 0.18699999968707562,
          "receive": 1.0040000015578698,
          "_blocked_queueing": 1.781999999366235,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "142864",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "e.sendObjectBeacon",
                "scriptId": "393",
                "url": "https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496",
                "lineNumber": 0,
                "columnNumber": 12456
              },
              {
                "functionName": "S",
                "scriptId": "393",
                "url": "https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496",
                "lineNumber": 0,
                "columnNumber": 28716
              },
              {
                "functionName": "L",
                "scriptId": "393",
                "url": "https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496",
                "lineNumber": 0,
                "columnNumber": 29594
              }
            ],
            "parent": {
              "description": "setTimeout",
              "callFrames": [
                {
                  "functionName": "",
                  "scriptId": "393",
                  "url": "https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496",
                  "lineNumber": 0,
                  "columnNumber": 29740
                }
              ]
            }
          }
        },
        "_priority": "High",
        "_resourceType": "xhr",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://www.professionele-koeling.nl/cdn-cgi/rum?",
          "httpVersion": "h3",
          "headers": [
            {
              "name": ":authority",
              "value": "www.professionele-koeling.nl"
            },
            {
              "name": ":method",
              "value": "POST"
            },
            {
              "name": ":path",
              "value": "/cdn-cgi/rum?"
            },
            {
              "name": ":scheme",
              "value": "https"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br, zstd"
            },
            {
              "name": "accept-language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "cache-control",
              "value": "no-cache"
            },
            {
              "name": "content-length",
              "value": "893"
            },
            {
              "name": "content-type",
              "value": "application/json"
            },
            {
              "name": "origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "referer",
              "value": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "same-origin"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            }
          ],
          "queryString": [],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 893,
          "postData": {
            "mimeType": "application/json",
            "text": "{\"memory\":{\"totalJSHeapSize\":50088391,\"usedJSHeapSize\":40854271,\"jsHeapSizeLimit\":3320315904},\"resources\":[],\"referrer\":\"https://www.professionele-koeling.nl/koelkasten-kisten.html\",\"eventType\":1,\"firstPaint\":2004,\"firstContentfulPaint\":2004,\"startTime\":1785408550822.3,\"versions\":{\"fl\":\"2024.11.0\",\"js\":\"2026.6.0\",\"timings\":2},\"pageloadId\":\"c10bba6a-eab5-49f1-b4f4-33ee94f59d61\",\"location\":\"https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html\",\"nt\":\"navigate\",\"timingsV2\":{\"nextHopProtocol\":\"h3\",\"domainLookupStart\":0,\"domainLookupEnd\":0,\"connectStart\":0,\"connectEnd\":0,\"requestStart\":32,\"responseStart\":736,\"responseEnd\":749,\"domInteractive\":2362,\"domComplete\":6377,\"loadEventStart\":6377,\"loadEventEnd\":6379,\"finalResponseHeadersStart\":736,\"firstInterimResponseStart\":0,\"transferSize\":23555,\"decodedBodySize\":101115},\"dt\":\"\",\"siteToken\":\"64dd5d21de4b4abf92cf382f7ea8ec9a\",\"st\":2}"
          }
        },
        "response": {
          "status": 204,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "access-control-allow-credentials",
              "value": "true"
            },
            {
              "name": "access-control-allow-methods",
              "value": "POST,OPTIONS"
            },
            {
              "name": "access-control-allow-origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "access-control-max-age",
              "value": "86400"
            },
            {
              "name": "alt-svc",
              "value": "h3=\":443\"; ma=86400"
            },
            {
              "name": "cf-ray",
              "value": "a233cbb929ff722d-VIE"
            },
            {
              "name": "content-type",
              "value": "text/plain"
            },
            {
              "name": "date",
              "value": "Thu, 30 Jul 2026 10:49:16 GMT"
            },
            {
              "name": "nel",
              "value": "{\"report_to\":\"cf-nel\",\"success_fraction\":0.0,\"max_age\":604800}"
            },
            {
              "name": "priority",
              "value": "u=1,i"
            },
            {
              "name": "report-to",
              "value": "{\"group\":\"cf-nel\",\"max_age\":604800,\"endpoints\":[{\"url\":\"https://a.nel.cloudflare.com/report/v4?s=70FAGxG5YyoIsiaceA%2F812ei6N33JeO1v0MNRoxMhv4ok5DNA73qWEExcHUSk8cB%2FlSgGrV4lY3jYwWCYkrbJhP%2BnlI%2Fxmrc9YDzRNBnxNJ4x8HQsshFIcpcYGXKUHLKpu%2BHlOH1ftRENrXj7aeb\"}]}"
            },
            {
              "name": "server",
              "value": "cloudflare"
            },
            {
              "name": "server-timing",
              "value": "cfExtPri"
            },
            {
              "name": "vary",
              "value": "Origin"
            }
          ],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/plain",
            "text": ""
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 473,
          "_error": null,
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "104.21.39.80",
        "startedDateTime": "2026-07-30T10:49:17.207Z",
        "time": 58.99999999746797,
        "timings": {
          "blocked": 6.999999998995918,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 1,
          "wait": 50.00000000008731,
          "receive": 0.9999999983847374,
          "_blocked_queueing": 3.999999998995918,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "142784",
        "pageref": "page_2"
      },
      {
        "_initiator": {
          "type": "script",
          "stack": {
            "callFrames": [
              {
                "functionName": "pd",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 217,
                "columnNumber": 390
              },
              {
                "functionName": "lo",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 396,
                "columnNumber": 1283
              },
              {
                "functionName": "$Q",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 903,
                "columnNumber": 182
              },
              {
                "functionName": "bR",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 904,
                "columnNumber": 36
              },
              {
                "functionName": "hR.flush",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 912,
                "columnNumber": 81
              },
              {
                "functionName": "",
                "scriptId": "449",
                "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                "lineNumber": 910,
                "columnNumber": 340
              }
            ],
            "parent": {
              "description": "setTimeout",
              "callFrames": [
                {
                  "functionName": "hR.O",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 910,
                  "columnNumber": 320
                },
                {
                  "functionName": "hR.add",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 911,
                  "columnNumber": 499
                },
                {
                  "functionName": "l.Un",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 932,
                  "columnNumber": 366
                },
                {
                  "functionName": "l.ot",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 932,
                  "columnNumber": 288
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 930,
                  "columnNumber": 81
                },
                {
                  "functionName": "Sl",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 378,
                  "columnNumber": 75
                },
                {
                  "functionName": "op",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 408,
                  "columnNumber": 240
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 930,
                  "columnNumber": 65
                },
                {
                  "functionName": "d",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 848,
                  "columnNumber": 493
                },
                {
                  "functionName": "$M.fa",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 849,
                  "columnNumber": 16
                },
                {
                  "functionName": "l.nt",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 930,
                  "columnNumber": 51
                },
                {
                  "functionName": "b",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 934,
                  "columnNumber": 724
                },
                {
                  "functionName": "u",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 684,
                  "columnNumber": 269
                },
                {
                  "functionName": "vo",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 398,
                  "columnNumber": 647
                },
                {
                  "functionName": "pD",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 684,
                  "columnNumber": 368
                },
                {
                  "functionName": "nD.flush",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 688,
                  "columnNumber": 80
                },
                {
                  "functionName": "nD.register",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 685,
                  "columnNumber": 311
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 934,
                  "columnNumber": 572
                },
                {
                  "functionName": "FS",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 934,
                  "columnNumber": 463
                },
                {
                  "functionName": "GS",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 934,
                  "columnNumber": 196
                },
                {
                  "functionName": "HS",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 934,
                  "columnNumber": 492
                },
                {
                  "functionName": "GT",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 941,
                  "columnNumber": 1688
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 312,
                  "columnNumber": 186
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 229,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 192,
                  "columnNumber": 710
                },
                {
                  "functionName": "fb",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 192,
                  "columnNumber": 461
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 253,
                  "columnNumber": 472
                },
                {
                  "functionName": "l.apply",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 229,
                  "columnNumber": 464
                },
                {
                  "functionName": "gb",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 192,
                  "columnNumber": 710
                },
                {
                  "functionName": "l.Sq",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 192,
                  "columnNumber": 1276
                },
                {
                  "functionName": "sf",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 264,
                  "columnNumber": 959
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 743,
                  "columnNumber": 6
                },
                {
                  "functionName": "pA",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 632,
                  "columnNumber": 495
                },
                {
                  "functionName": "wA.evaluate",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 638,
                  "columnNumber": 288
                },
                {
                  "functionName": "e",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 658,
                  "columnNumber": 169
                },
                {
                  "functionName": "VB",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 659,
                  "columnNumber": 741
                },
                {
                  "functionName": "YB",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 663,
                  "columnNumber": 217
                },
                {
                  "functionName": "NE",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 719,
                  "columnNumber": 244
                },
                {
                  "functionName": "OE",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 720,
                  "columnNumber": 188
                },
                {
                  "functionName": "Im",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1003,
                  "columnNumber": 0
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1006,
                  "columnNumber": 312
                },
                {
                  "functionName": "c",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1004,
                  "columnNumber": 129
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1006,
                  "columnNumber": 276
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1006,
                  "columnNumber": 281
                },
                {
                  "functionName": "",
                  "scriptId": "449",
                  "url": "https://www.googletagmanager.com/gtag/js?id=G-3X7F7CBMN7&cx=c&gtm=4e67s1",
                  "lineNumber": 1008,
                  "columnNumber": 2
                }
              ],
              "parent": {
                "description": "PendingScript",
                "callFrames": [
                  {
                    "functionName": "Ls",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 241,
                    "columnNumber": 251
                  },
                  {
                    "functionName": "Xc",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 231,
                    "columnNumber": 406
                  },
                  {
                    "functionName": "mo",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 413,
                    "columnNumber": 1368
                  },
                  {
                    "functionName": "GA",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 656,
                    "columnNumber": 1735
                  },
                  {
                    "functionName": "bH",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 773,
                    "columnNumber": 302
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 326,
                    "columnNumber": 186
                  },
                  {
                    "functionName": "l.apply",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 250,
                    "columnNumber": 464
                  },
                  {
                    "functionName": "gb",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 213,
                    "columnNumber": 710
                  },
                  {
                    "functionName": "fb",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 213,
                    "columnNumber": 461
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 274,
                    "columnNumber": 472
                  },
                  {
                    "functionName": "l.apply",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 250,
                    "columnNumber": 464
                  },
                  {
                    "functionName": "gb",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 213,
                    "columnNumber": 710
                  },
                  {
                    "functionName": "l.Sq",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 213,
                    "columnNumber": 1276
                  },
                  {
                    "functionName": "sf",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 285,
                    "columnNumber": 959
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 759,
                    "columnNumber": 6
                  },
                  {
                    "functionName": "pA",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 649,
                    "columnNumber": 495
                  },
                  {
                    "functionName": "wA.evaluate",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 655,
                    "columnNumber": 288
                  },
                  {
                    "functionName": "e",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 675,
                    "columnNumber": 169
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 218,
                    "columnNumber": 124
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 676,
                    "columnNumber": 359
                  },
                  {
                    "functionName": "",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 676,
                    "columnNumber": 99
                  },
                  {
                    "functionName": "VB",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 676,
                    "columnNumber": 741
                  },
                  {
                    "functionName": "YB",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 680,
                    "columnNumber": 217
                  },
                  {
                    "functionName": "NE",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 736,
                    "columnNumber": 244
                  },
                  {
                    "functionName": "OE",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 737,
                    "columnNumber": 188
                  },
                  {
                    "functionName": "QE",
                    "scriptId": "413",
                    "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                    "lineNumber": 742,
                    "columnNumber": 320
                  }
                ],
                "parent": {
                  "description": "setTimeout",
                  "callFrames": [
                    {
                      "functionName": "ed",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 233,
                      "columnNumber": 220
                    },
                    {
                      "functionName": "FE.bind",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 740,
                      "columnNumber": 313
                    },
                    {
                      "functionName": "OU",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1010,
                      "columnNumber": 491
                    },
                    {
                      "functionName": "Im",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1014,
                      "columnNumber": 303
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1018,
                      "columnNumber": 312
                    },
                    {
                      "functionName": "c",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1016,
                      "columnNumber": 129
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1018,
                      "columnNumber": 276
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1018,
                      "columnNumber": 281
                    },
                    {
                      "functionName": "",
                      "scriptId": "413",
                      "url": "https://www.googletagmanager.com/gtm.js?id=GTM-T5RSJRCW",
                      "lineNumber": 1020,
                      "columnNumber": 2
                    }
                  ],
                  "parent": {
                    "description": "PendingScript",
                    "callFrames": [
                      {
                        "functionName": "",
                        "scriptId": "398",
                        "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                        "lineNumber": 96,
                        "columnNumber": 64
                      },
                      {
                        "functionName": "",
                        "scriptId": "398",
                        "url": "https://www.professionele-koeling.nl/cavanova-wijnkoeler-2.html",
                        "lineNumber": 97,
                        "columnNumber": 2
                      }
                    ]
                  }
                }
              }
            }
          }
        },
        "_priority": "High",
        "_resourceType": "fetch",
        "cache": {},
        "connection": "443",
        "request": {
          "method": "POST",
          "url": "https://analytics.google.com/g/collect?v=2&tid=G-3X7F7CBMN7&gtm=45je67s1v9116206509z89243950528za20gzb9243950528zd9243950528&_p=1785408552654&gcd=13l3l3l3l1l1&npa=0&dma=0&_eu=AAAAACQC&are=1&cid=1139218666.1785405308&frm=0&ibt=1&ngs=1&pscdl=noapi&rcb=0&sr=1536x864&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uam=&uamb=0&uap=Windows&uapv=10.0.0&uaw=0&ul=ru-ru&tag_exp=115616986~115938466~115938469~118897920~118897930~119896802&sid=1785407240&sct=2&seg=1&dl=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&dr=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&dt=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&_s=1&tfd=10097",
          "httpVersion": "h3",
          "headers": [
            {
              "name": ":authority",
              "value": "analytics.google.com"
            },
            {
              "name": ":method",
              "value": "POST"
            },
            {
              "name": ":path",
              "value": "/g/collect?v=2&tid=G-3X7F7CBMN7&gtm=45je67s1v9116206509z89243950528za20gzb9243950528zd9243950528&_p=1785408552654&gcd=13l3l3l3l1l1&npa=0&dma=0&_eu=AAAAACQC&are=1&cid=1139218666.1785405308&frm=0&ibt=1&ngs=1&pscdl=noapi&rcb=0&sr=1536x864&uaa=x86&uab=64&uafvl=Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187&uam=&uamb=0&uap=Windows&uapv=10.0.0&uaw=0&ul=ru-ru&tag_exp=115616986~115938466~115938469~118897920~118897930~119896802&sid=1785407240&sct=2&seg=1&dl=https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html&dr=https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html&dt=Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu&_s=1&tfd=10097"
            },
            {
              "name": ":scheme",
              "value": "https"
            },
            {
              "name": "accept",
              "value": "*/*"
            },
            {
              "name": "accept-encoding",
              "value": "gzip, deflate, br, zstd"
            },
            {
              "name": "accept-language",
              "value": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            {
              "name": "cache-control",
              "value": "no-cache"
            },
            {
              "name": "content-length",
              "value": "97"
            },
            {
              "name": "content-type",
              "value": "text/plain;charset=UTF-8"
            },
            {
              "name": "origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "priority",
              "value": "u=1, i"
            },
            {
              "name": "referer",
              "value": "https://www.professionele-koeling.nl/"
            },
            {
              "name": "sec-ch-ua",
              "value": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            },
            {
              "name": "sec-fetch-dest",
              "value": "empty"
            },
            {
              "name": "sec-fetch-mode",
              "value": "no-cors"
            },
            {
              "name": "sec-fetch-site",
              "value": "cross-site"
            },
            {
              "name": "sec-fetch-storage-access",
              "value": "none"
            },
            {
              "name": "user-agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            },
            {
              "name": "x-browser-channel",
              "value": "stable"
            },
            {
              "name": "x-browser-copyright",
              "value": "Copyright 2026 Google LLC. All Rights Reserved."
            },
            {
              "name": "x-browser-validation",
              "value": "aIITHrVCZCAqILmQej28NTv6cPs="
            },
            {
              "name": "x-browser-year",
              "value": "2026"
            }
          ],
          "queryString": [
            {
              "name": "v",
              "value": "2"
            },
            {
              "name": "tid",
              "value": "G-3X7F7CBMN7"
            },
            {
              "name": "gtm",
              "value": "45je67s1v9116206509z89243950528za20gzb9243950528zd9243950528"
            },
            {
              "name": "_p",
              "value": "1785408552654"
            },
            {
              "name": "gcd",
              "value": "13l3l3l3l1l1"
            },
            {
              "name": "npa",
              "value": "0"
            },
            {
              "name": "dma",
              "value": "0"
            },
            {
              "name": "_eu",
              "value": "AAAAACQC"
            },
            {
              "name": "are",
              "value": "1"
            },
            {
              "name": "cid",
              "value": "1139218666.1785405308"
            },
            {
              "name": "frm",
              "value": "0"
            },
            {
              "name": "ibt",
              "value": "1"
            },
            {
              "name": "ngs",
              "value": "1"
            },
            {
              "name": "pscdl",
              "value": "noapi"
            },
            {
              "name": "rcb",
              "value": "0"
            },
            {
              "name": "sr",
              "value": "1536x864"
            },
            {
              "name": "uaa",
              "value": "x86"
            },
            {
              "name": "uab",
              "value": "64"
            },
            {
              "name": "uafvl",
              "value": "Not%253BA%253DBrand%3B8.0.0.0%7CChromium%3B150.0.7871.187%7CGoogle%2520Chrome%3B150.0.7871.187"
            },
            {
              "name": "uam",
              "value": ""
            },
            {
              "name": "uamb",
              "value": "0"
            },
            {
              "name": "uap",
              "value": "Windows"
            },
            {
              "name": "uapv",
              "value": "10.0.0"
            },
            {
              "name": "uaw",
              "value": "0"
            },
            {
              "name": "ul",
              "value": "ru-ru"
            },
            {
              "name": "tag_exp",
              "value": "115616986~115938466~115938469~118897920~118897930~119896802"
            },
            {
              "name": "sid",
              "value": "1785407240"
            },
            {
              "name": "sct",
              "value": "2"
            },
            {
              "name": "seg",
              "value": "1"
            },
            {
              "name": "dl",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fcavanova-wijnkoeler-2.html"
            },
            {
              "name": "dr",
              "value": "https%3A%2F%2Fwww.professionele-koeling.nl%2Fkoelkasten-kisten.html"
            },
            {
              "name": "dt",
              "value": "Mini%20wijnkoeler%20Cavanova%202%20flessen%20wijn%20%7C%20Professionele-koeling.nl%20is%20Onderdeel%20van%20Horecaplaats.nu"
            },
            {
              "name": "_s",
              "value": "1"
            },
            {
              "name": "tfd",
              "value": "10097"
            }
          ],
          "cookies": [],
          "headersSize": -1,
          "bodySize": 97,
          "postData": {
            "mimeType": "text/plain;charset=UTF-8",
            "text": "en=page_view\r\nen=view_item&pr1=id605002~nmCavanova%20605002~pr190~qt1&epn.value=190&_et=11&cu=EUR"
          }
        },
        "response": {
          "status": 204,
          "statusText": "",
          "httpVersion": "h3",
          "headers": [
            {
              "name": "access-control-allow-credentials",
              "value": "true"
            },
            {
              "name": "access-control-allow-origin",
              "value": "https://www.professionele-koeling.nl"
            },
            {
              "name": "alt-svc",
              "value": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000"
            },
            {
              "name": "cache-control",
              "value": "no-cache, no-store, must-revalidate"
            },
            {
              "name": "content-length",
              "value": "0"
            },
            {
              "name": "content-security-policy-report-only",
              "value": "script-src 'none'; form-action 'none'; frame-src 'none'; report-uri https://csp.withgoogle.com/csp/scaffolding/ascnsrsggc:197:0"
            },
            {
              "name": "content-type",
              "value": "text/plain"
            },
            {
              "name": "cross-origin-opener-policy-report-only",
              "value": "same-origin; report-to=ascnsrsggc:197:0"
            },
            {
              "name": "cross-origin-resource-policy",
              "value": "cross-origin"
            },
            {
              "name": "date",
              "value": "Thu, 30 Jul 2026 10:49:20 GMT"
            },
            {
              "name": "expires",
              "value": "Fri, 01 Jan 1990 00:00:00 GMT"
            },
            {
              "name": "pragma",
              "value": "no-cache"
            },
            {
              "name": "report-to",
              "value": "{\"group\":\"ascnsrsggc:197:0\",\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://csp.withgoogle.com/csp/report-to/scaffolding/ascnsrsggc:197:0\"}],}"
            },
            {
              "name": "server",
              "value": "Golfe2"
            }
          ],
          "cookies": [],
          "content": {
            "size": 0,
            "mimeType": "text/plain"
          },
          "redirectURL": "",
          "headersSize": -1,
          "bodySize": -1,
          "_transferSize": 20,
          "_error": "net::ERR_ABORTED",
          "_fetchedViaServiceWorker": false
        },
        "serverIPAddress": "142.250.130.113",
        "startedDateTime": "2026-07-30T10:49:20.921Z",
        "time": 118.0000000003929,
        "timings": {
          "blocked": 5.000000000814907,
          "dns": -1,
          "ssl": -1,
          "connect": -1,
          "send": 1,
          "wait": 77.99999999992724,
          "receive": 33.999999999650754,
          "_blocked_queueing": 4.000000000814907,
          "_workerStart": -1,
          "_workerReady": -1,
          "_workerFetchStart": -1,
          "_workerRespondWithSettled": -1
        },
        "_connectionId": "142863",
        "pageref": "page_2"
      }
    ]
  }
}

--- ФАЙЛ: notes.txt ---


--- ФАЙЛ: page.html ---
<li class="item" style="height: 343.012px; padding-bottom: 75px;">
            
                <div class="product-image-wrapper" style="max-width:295px;">
                
                    <a href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html" title="Polar DM071" class="product-image">
                        <img id="product-collection-image-212" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" alt="Polar DM071">

                        
                                            </a>
                
                    <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover" style="display: none; opacity: 1;">
			<li><a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/RTXXHZVsWjqQoFjc/" title="Zet op verlanglijst">
					<span class="2 icon ib ic ic-heart"></span>
			</a></li>
			<li><a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/form_key/RTXXHZVsWjqQoFjc/" title="Voeg toe aan productvergelijking">
					<span class="2 icon ib ic ic-compare"></span>
			</a></li></ul>                
                </div> <!-- end: product-image-wrapper -->

                                    <h2 class="product-name"><a href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html" title="Polar DM071">Polar DM071</a></h2>
                
                                
                                
                                    

                        
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

                
                
                <div class="actions clearer" style="padding-left: 49.8687px; bottom: 30px;">

                    
                                                    <button type="button" title="In winkelwagen" class="button btn-cart" onclick="setLocation('https://www.professionele-koeling.nl/checkout/cart/add/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/product/212/form_key/RTXXHZVsWjqQoFjc/')"><span><span>In winkelwagen</span></span></button>
                        
                                        
                                    </div> <!-- end: actions -->
            </li>

--- ФАЙЛ: product_page.html ---
<div class="product-primary-column product-shop grid12-5">

			<div class="product-name">
				<h1 itemprop="name">Polar GE579</h1>
			</div>
			
			    <div class="ratings no-rating">
        <div class="rating-box">
            <div class="rating" style="width:0%"></div>
        </div>
        <p class="rating-links">
            <a id="goto-reviews-form" href="#review-form">Schrijf de eerste review over dit product</a>
        </p>
    </div>

							<div class="short-description"><div class="std" itemprop="description"><p>De Polar GE579 is een zwarte minibar koelkast met <br>29 liter inhoud voor gebruik in hotelkamers, B&amp;B's of ver-<br>gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken.</p><br>
<h4 style="color: blue;"><span style="background-color: yellow;">Advies nodig, of meerdere stuks tegen de scherpste prijs?<br>Bel onze specialisten: <strong>036 5363782</strong></span></h4><br>
<p>&nbsp;</p></div></div>
			
			
			
											<meta itemprop="productID" content="sku:GE579">			
						
			
			<div itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
				<div class="product-type-data">
		    <p class="availability in-stock">Beschikbaarheid: <span>Op voorraad</span></p>
	    <meta itemprop="availability" content="http://schema.org/InStock">
	

                        
    <div class="price-box">
                                            
                    <p class="old-price">
                <span class="price-label">Van:</span>
                <span class="price" id="old-price-2526">
                    €&nbsp;255,99                </span>
            </p>

                            <p class="special-price">
                    <span class="price-label">Voor</span>
                <span class="price" id="product-price-2526">
                    €&nbsp;229,00                </span>
                        <span class="label">Excl. BTW</span>
                </p>
                    
    
        </div>

</div>
				
				<meta itemprop="priceCurrency" content="EUR"><meta itemprop="price" content="229">			</div> 
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
        <a class="link-wishlist feature feature-icon-hover first" href="https://www.professionele-koeling.nl/wishlist/index/add/product/2526/form_key/SWbw8G6S4uAWBovz/" onclick="productAddToCartForm.submitLight(this, this.href); return false;" title="Zet op verlanglijst">
			<span class="ic ic-heart ib icon-color-productview"></span>
			<span class="label">Zet op verlanglijst</span>
		</a>
	</li>


	<li>
        <a class="link-compare feature feature-icon-hover first" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/2526/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL3BvbGFyLWdlNTc5LW1pbmktYmFyLmh0bWw,/form_key/SWbw8G6S4uAWBovz/" title="Voeg toe aan productvergelijking">
			<span class="ic ic-compare ib icon-color-productview"></span>
			<span class="label">Voeg toe aan productvergelijking</span>
		</a>
	</li>


	<li>
    	<a class="link-share feature feature-icon-hover first" href="https://www.professionele-koeling.nl/sendfriend/product/send/id/2526/cat_id/3/" title="E-mail naar een vriend">
			<span class="ic ic-share ib icon-color-productview"></span>
			<span class="label">E-mail naar een vriend</span>
		</a>
	</li>

</ul>				</div>
			
			
			
			
		</div>

--- ФАЙЛ: proxies.txt ---


--- ФАЙЛ: traceback.txt ---
$ python main.py
======================================================================
[C:\Users\user\Desktop\UPWORK-ALL\projects\upwork1\app\main.py] ЗАПУСК ПАРСЕРА
======================================================================
[C:\Users\user\Desktop\UPWORK-ALL\projects\upwork1\app\browser.py] Запуск Chromi
um (Headless=False)...
[2026-07-30 13:15:38] [INFO] Браузер запущен (headless=False)
[2026-07-30 13:15:38] [INFO] ===================================================
===================
[2026-07-30 13:15:38] [INFO] Запуск scraper: сбор данных с professionele-koeling
.nl
[2026-07-30 13:15:38] [INFO] ===================================================
===================
[2026-07-30 13:15:38] [INFO] Начало обхода категории: https://www.professionele-
koeling.nl/koelkasten-kisten.html
[2026-07-30 13:15:38] [INFO] Загрузка страницы категории #1: https://www.profess
ionele-koeling.nl/koelkasten-kisten.html
[2026-07-30 13:15:38] [DEBUG] Запрос к https://www.professionele-koeling.nl/koelkasten-kisten.html (попытка 1/3)
[2026-07-30 13:15:41] [WARNING] parse_listing: не найдены элементы с классом 'item'
[2026-07-30 13:15:41] [WARNING] На странице https://www.professionele-koeling.nl/koelkasten-kisten.html не найдено товаров
[2026-07-30 13:15:41] [INFO] Найдено 0 товаров на странице 1
C:\Users\user\AppData\Local\Programs\Python\Python313\Lib\site-packages\soupsieve\css_parser.py:876: FutureWarning: The pseudo class ':contains' is d
eprecated, ':-soup-contains' should be used moving forward.
  warnings.warn(  # noqa: B028
[2026-07-30 13:15:41] [INFO] Достигнут конец пагинации
[2026-07-30 13:15:41] [INFO] Обход завершён. Всего загружено 0 товаров
[2026-07-30 13:15:41] [INFO] ======================================================================
[2026-07-30 13:15:41] [INFO] Сбор данных завершён. Получено 0 страниц товаров
[2026-07-30 13:15:41] [INFO] ======================================================================
[C:\Users\user\Desktop\UPWORK-ALL\projects\upwork1\app\main.py] Критическая ошибка: Нечего парсить (список страниц пуст).
[C:\Users\user\Desktop\UPWORK-ALL\projects\upwork1\app\cookie_manager.py] Куки сохранены в cookies.json (Всего: 0)
[2026-07-30 13:15:42] [INFO] Браузер закрыт



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

Файл `app/scraper.py` — перепиши его полностью под план проекта:

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль scraper — сбор сырого HTML-контента с сайта professionele-koeling.nl.

Отвечает только за сетевые запросы, навигацию и пагинацию.
Использует requests + BeautifulSoup для обхода категории и получения HTML карточек товаров.

Не выполняет парсинг данных — только возвращает список HTML-строк для parser.py.
"""

import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from app.config import TIMEOUT, RETRY_COUNT, DEFAULT_USER_AGENT
from app.utils import random_delay


def fetch_listing_page(url: str) -> Optional[str]:
    """
    Получить HTML страницы категории.

    Args:
        url: URL страницы категории

    Returns:
        str: HTML страницы или None при ошибке
    """
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text

        except requests.exceptions.Timeout:
            print(f"[{__file__}] Таймаут при загрузке {url} (попытка {attempt + 1}/{RETRY_COUNT})")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"[{__file__}] Ошибка 403 (доступ запрещен) при загрузке {url}")
                return None
            print(f"[{__file__}] HTTP ошибка {e.response.status_code} при загрузке {url}")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке {url}: {e}")
            if attempt < RETRY_COUNT - 1:
                time.sleep(2 ** attempt)
            continue

    print(f"[{__file__}] Не удалось загрузить {url} после {RETRY_COUNT} попыток")
    return None


def fetch_product_page(url: str) -> Optional[str]:
    """
    Получить HTML страницы товара.

    Args:
        url: URL страницы товара

    Returns:
        str: HTML страницы товара или None при ошибке
    """
    return fetch_listing_page(url)


def get_product_urls_from_listing(html: str) -> List[str]:
    """
    Извлечь URL товаров из HTML страницы категории.

    Args:
        html: HTML страницы категории

    Returns:
        List[str]: Список URL товаров
    """
    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        product_urls = []

        # Ищем все элементы с классом "item" (как в предоставленном HTML)
        items = soup.find_all("li", class_="item")

        for item in items:
            # Ищем ссылку внутри блока product-image-wrapper или h2.product-name
            link = item.find("a", class_="product-image")
            if not link:
                # Пробуем найти ссылку в заголовке
                title_link = item.find("h2", class_="product-name")
                if title_link:
                    link = title_link.find("a")

            if link and link.get("href"):
                url = link.get("href")
                # Преобразуем относительный URL в абсолютный
                if url.startswith("/"):
                    url = "https://www.professionele-koeling.nl" + url
                product_urls.append(url)

        print(f"[{__file__}] Найдено {len(product_urls)} товаров на странице")
        return product_urls

    except Exception as e:
        print(f"[{__file__}] Ошибка при извлечении URL товаров: {e}")
        return []


def get_next_page_url(html: str, current_url: str) -> Optional[str]:
    """
    Определить URL следующей страницы пагинации.

    Args:
        html: HTML текущей страницы
        current_url: URL текущей страницы (для построения абсолютных ссылок)

    Returns:
        str: URL следующей страницы или None
    """
    if not html:
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")

        # Ищем ссылку "Next" или "Следующая"
        # На сайте могут быть разные варианты пагинации
        next_link = None

        # Вариант 1: пагинация с классом "next"
        next_link = soup.find("a", class_="next")
        if not next_link:
            # Вариант 2: любой элемент с текстом "Next" или "Следующая"
            for link in soup.find_all("a"):
                if link.get_text(strip=True).lower() in ["next", "следующая", "следующая страница", "›", "»"]:
                    next_link = link
                    break

        if next_link and next_link.get("href"):
            url = next_link.get("href")
            if url.startswith("/"):
                url = "https://www.professionele-koeling.nl" + url
            return url

        return None

    except Exception as e:
        print(f"[{__file__}] Ошибка при поиске следующей страницы: {e}")
        return None


def fetch_all_product_pages(start_url: str) -> List[str]:
    """
    Оркестрация обхода сайта: загружает все страницы категории и все карточки товаров.

    Алгоритм:
    1. Загрузить HTML страницы категории
    2. Извлечь URL товаров
    3. Для каждого URL товара загрузить HTML
    4. Если есть следующая страница категории, перейти на неё и повторить

    Args:
        start_url: URL начальной страницы категории

    Returns:
        List[str]: Список HTML страниц товаров
    """
    product_htmls = []
    current_url = start_url
    page_number = 1
    seen_urls = set()

    print(f"[{__file__}] Начало сбора данных с {start_url}")

    while current_url:
        print(f"[{__file__}] Загрузка страницы категории #{page_number}: {current_url}")

        # Загружаем страницу категории
        listing_html = fetch_listing_page(current_url)
        if not listing_html:
            print(f"[{__file__}] Не удалось загрузить страницу категории {current_url}")
            break

        # Извлекаем URL товаров
        product_urls = get_product_urls_from_listing(listing_html)

        if not product_urls:
            print(f"[{__file__}] На странице не найдено товаров")
            break

        print(f"[{__file__}] Найдено {len(product_urls)} товаров на странице #{page_number}")

        # Загружаем каждую карточку товара
        for idx, product_url in enumerate(product_urls, 1):
            if product_url in seen_urls:
                continue
            seen_urls.add(product_url)

            print(f"[{__file__}] Загрузка товара {idx}/{len(product_urls)}: {product_url}")

            # Задержка между запросами товаров
            if idx > 1:
                random_delay(1.0, 2.5)

            product_html = fetch_product_page(product_url)
            if product_html:
                product_htmls.append(product_html)
            else:
                print(f"[{__file__}] Не удалось загрузить товар {product_url}")

        # Ищем следующую страницу
        next_url = get_next_page_url(listing_html, current_url)
        if next_url and next_url != current_url:
            current_url = next_url
            page_number += 1

            # Задержка перед следующей страницей категории
            random_delay(1.5, 3.0)
        else:
            print(f"[{__file__}] Достигнут конец пагинации")
            break

    print(f"[{__file__}] Сбор данных завершен. Собрано {len(product_htmls)} карточек товаров")
    return product_htmls


def fetch_page_data(context=None) -> List[str]:
    """
    Главная точка входа для сбора данных, вызываемая из main.py.

    Args:
        context: Необязательный контекст браузера (для совместимости с main.py)

    Returns:
        List[str]: Список HTML страниц товаров
    """
    print(f"[{__file__}] Запуск сбора данных...")

    # Стартовый URL категории koelkasten-kisten
    start_url = "https://www.professionele-koeling.nl/koelkasten-kisten.html"

    try:
        product_htmls = fetch_all_product_pages(start_url)

        if not product_htmls:
            print(f"[{__file__}] Предупреждение: Не удалось собрать ни одной карточки товара")
            return []

        print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(product_htmls)}")
        return product_htmls

    except Exception as e:
        print(f"[{__file__}] Критическая ошибка при сборе данных: {e}")
        return []

---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/scraper.py` (модуль: **scraper**).

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
2. Полный код файла `app/scraper.py` в одном блоке:

```python
# полный код здесь
```

3. Как протестировать локально (1–2 команды).

**ЗАПРЕЩЕНО:**
- Писать код для других файлов.
- Добавлять GUI, CLI, меню.
- Добавлять функции, которых нет в project_plan.md.
- Использовать классы.
