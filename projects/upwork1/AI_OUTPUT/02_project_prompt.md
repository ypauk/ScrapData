# РОЛЬ

Ты — Senior Python Developer / Web Scraping Engineer. Твоя цель — спроектировать техническое решение для конкретного сайта клиента **БЕЗ написания самого кода**. 

Ты должен распределить логику по существующей функциональной структуре проекта.

---

# ВХОДНЫЕ ДАННЫЕ
- **Описание задачи клиента:** 
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
- **Утвержденная стратегия (Шаг 1):** Я посмотрел файл промпта 01_analysis_prompt.md в репозитории. В нём роль — Python Web Scraping Engineer, задача — проанализировать проект клиента, выбрать простое и надёжное решение, без написания кода на этом этапе. Входные данные: нужно собрать данные товаров с сайта professionele-koeling.nl, сначала сделать тестовый CSV на 2 товара, затем полный scrape.

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
- **Анализ разметки/API (из файлов в AI_INPUT):** 

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


--- СЖАТЫЙ HTML: page.html ---
<li class="item">
 <div class="product-image-wrapper">
  <a class="product-image" href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html">
   <img id="product-collection-image-212" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg"/>
  </a>
  <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover">
   <li>
    <a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/RTXXHZVsWjqQoFjc/">
     <span class="2 icon ib ic ic-heart">
     </span>
    </a>
   </li>
   <li>
    <a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/form_key/RTXXHZVsWjqQoFjc/">
     <span class="2 icon ib ic ic-compare">
     </span>
    </a>
   </li>
  </ul>
 </div>
 <!-- end: product-image-wrapper -->
 <h2 class="product-name">
  <a href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html">
   Polar DM071
  </a>
 </h2>
 <div class="price-box">
  <p class="old-price">
   <span class="price-label">
    Van:
   </span>
   <span class="price" id="old-price-212">
    € 179,00
   </span>
  </p>
  <p class="special-price">
   <span class="price-label">
    Voor
   </span>
   <span class="price" id="product-price-212">
    € 175,00
   </span>
   <span class="label">
    Excl. BTW
   </span>
  </p>
 </div>
 <div class="actions clearer">
  <button class="button btn-cart">
   <span>
    <span>
     In winkelwagen
    </span>
   </span>
  </button>
 </div>
 <!-- end: actions -->
</li>


--- СЖАТЫЙ HTML: product_page.html ---
<div class="product-primary-column product-shop grid12-5">
 <div class="product-name">
  <h1>
   Polar GE579
  </h1>
 </div>
 <div class="ratings no-rating">
  <div class="rating-box">
   <div class="rating">
   </div>
  </div>
  <p class="rating-links">
   <a href="#review-form" id="goto-reviews-form">
    Schrijf de eerste review over dit product
   </a>
  </p>
 </div>
 <div class="short-description">
  <div class="std">
   <p>
    De Polar GE579 is een zwarte minibar koelkast met
    <br/>
    29 liter inhoud voor gebruik in hotelkamers, B&amp;B's of ver-
    <br/>
    gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken.
   </p>
   <br/>
   <h4>
    <span>
     Advies nodig, of meerdere stuks tegen de scherpste prijs?
     <br/>
     Bel onze specialisten:
     <strong>
      036 5363782
     </strong>
    </span>
   </h4>
   <br/>
   <p>
   </p>
  </div>
 </div>
 <div>
  <div class="product-type-data">
   <p class="availability in-stock">
    Beschikbaarheid:
    <span>
     Op voorraad
    </span>
   </p>
   <div class="price-box">
    <p class="old-price">
     <span class="price-label">
      Van:
     </span>
     <span class="price" id="old-price-2526">
      € 255,99
     </span>
    </p>
    <p class="special-price">
     <span class="price-label">
      Voor
     </span>
     <span class="price" id="product-price-2526">
      € 229,00
     </span>
     <span class="label">
      Excl. BTW
     </span>
    </p>
   </div>
  </div>
 </div>
 <div class="add-to-box s">
  <div class="add-to-cart left-side">
   <div class="qty-wrapper">
    <label>
     Aantal:
    </label>
    <input class="input-text qty" id="qty" name="qty"/>
   </div>
   <button class="button btn-cart" id="product-addtocart-button">
    <span>
     <span>
      In winkelwagen
     </span>
    </span>
   </button>
  </div>
  <div class="paypal-wrapper">
  </div>
 </div>
 <div class="product-benefits">
  <ul>
   <li>
    Levering in de Benelux
   </li>
   <li>
    Zakelijk op rekening kopen
   </li>
   <li>
    2 jaar garantie
   </li>
   <li>
    Deskundig advies
   </li>
   <li>
    Officieel dealer van topmerken
   </li>
  </ul>
 </div>
 <div class="action-box clearer">
  <ul class="add-to-links">
   <li>
    <a class="link-wishlist feature feature-icon-hover first" href="https://www.professionele-koeling.nl/wishlist/index/add/product/2526/form_key/SWbw8G6S4uAWBovz/">
     <span class="ic ic-heart ib icon-color-productview">
     </span>
     <span class="label">
      Zet op verlanglijst
     </span>
    </a>
   </li>
   <li>
    <a class="link-compare feature feature-icon-hover first" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/2526/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL3BvbGFyLWdlNTc5LW1pbmktYmFyLmh0bWw,/form_key/SWbw8G6S4uAWBovz/">
     <span class="ic ic-compare ib icon-color-productview">
     </span>
     <span class="label">
      Voeg toe aan productvergelijking
     </span>
    </a>
   </li>
   <li>
    <a class="link-share feature feature-icon-hover first" href="https://www.professionele-koeling.nl/sendfriend/product/send/id/2526/cat_id/3/">
     <span class="ic ic-share ib icon-color-productview">
     </span>
     <span class="label">
      E-mail naar een vriend
     </span>
    </a>
   </li>
  </ul>
 </div>
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

# СУЩЕСТВУЮЩАЯ СТРУКТУРА ЯДРА (НЕИЗМЕНЯЕМАЯ)

В проекте **УЖЕ написаны, протестированы и не подлежат изменению** следующие файлы:
- `app/main.py` — Оркестратор. Запускает скрапер, закрывает браузер, передает контент в парсер, вызывает экспортер.
- `app/browser.py` — Функция `get_browser_context()`. browser.py предоставляет браузерный контекст, если выбран браузерный способ получения данных.
- `app/config.py` — Все абсолютные пути к папкам (`OUTPUT_DIR`, `AI_INPUT_DIR`), таймауты и настройки сети.
- `app/exporter.py` — Функции `save_to_csv()` и `save_to_json()` с поддержкой кодировки Excel (`utf-8-sig`).
- `app/utils.py` — Логгер, кастомная очистка цен `clean_price()` и случайные паузы `random_delay()`.

Твоя зона ответственности — **спроектировать наполнение для двух пустых модулей**: `app/scraper.py` и `app/parser.py`.

Перед проектированием проверь, может ли задача быть решена существующими возможностями ядра.

Не предлагай дублировать функции из:

browser.py
config.py
utils.py
exporter.py

---

# Архитектурные ограничения
1. **БЕЗ КЛАДОВЫХ КЛАССОВ:** Никакого ООП. Проектируй решение строго на базе изолированных функций.
2. **Единая ответственность:** - `scraper.py` отвечает *только* за сеть, навигацию, пагинацию, клики/скролл и сбор сырого контента. Он не должен знать, какие теги находятся внутри страницы.
   - `parser.py` отвечает *только* за обработку сырого контента (BS4/JSON) в памяти. Он не должен делать никаких сетевых запросов.

---

# СТРАТЕГИЯ ОПРЕДЕЛЕНИЯ ТЕХНОЛОГИИ СБОРА

Перед проектированием проанализируй входные данные и выбери оптимальный способ получения данных. 
Приоритет выбора решения:

1. Минимальная сложность
2. Максимальная надежность
3. Минимальное количество зависимостей
4. Простота сопровождения
5. Производительность (если это не противоречит первым четырем пунктам)

1. **Есть API → использовать API.**
Если API покрывает все требования клиента —
используй API.
Если API не предоставляет необходимые данные —
объясни причину и переходи к следующему способу.   
2. **Есть готовый HTML без JavaScript → использовать requests + BeautifulSoup**   
3. **Контент появляется только после выполнения JavaScript, требуется авторизация через браузер, сложные взаимодействия или антибот → использовать Playwright.**
   
---

# "Что останется неизвестным"

После проектирования перечисли,

какая информация отсутствует.

Например:

- неизвестен селектор товара

- нет HAR

- отсутствует пример HTML

- неизвестна пагинация

- неизвестна авторизация

- неизвестно API

Не выдумывай недостающие данные.

Любое предположение явно помечай как:

ПРЕДПОЛОЖЕНИЕ:

---

# "Почему выбран именно этот способ"

Сначала объясни:

Почему выбран API

или

Почему выбран HTML

или

Почему нужен Playwright

Укажи плюсы и минусы выбранного варианта.

---

# ОЖИДАЕМЫЙ РЕЗУЛЬТАТ (ТВОЙ ОТВЕТ)

Выполни проектирование реализации и распиши структуру будущих функций в следующем формате:

### 1. Полный поток данных

Опиши путь данных от входа до выхода. Это помогает избежать путаницы и понять общую картину.

**Формат:**

URL
↓
[Технология: Playwright / requests]
↓
[Сырые данные: HTML / JSON]
↓
[Парсер: BeautifulSoup / json.loads]
↓
[Структура: dict]
↓
[Список: list[dict]]
↓
[Экспортер: exporter.py → CSV / JSON]

**Пример:**

Клиент запускает main.py

main.py инициализирует браузер через browser.py

main.py вызывает scraper.fetch_listing()

scraper.py загружает страницу со списком товаров через Playwright

scraper.py передает сырой HTML в parser.parse_listing()

parser.py использует BeautifulSoup для извлечения карточек товаров

parser.py вызывает parse_single_item() для каждой карточки

parser.py возвращает список словарей (list[dict]) в scraper.py

scraper.py возвращает список в main.py

main.py передает список в exporter.save_to_csv()

### 2. Проектирование `app/scraper.py` (Сетевой сбор)

* **2.1. Интерфейс функций

Опиши контракт каждой функции, которую будет содержать `scraper.py`.
Предложи необходимый набор функций.

* **2.2 Алгоритм обхода:- **Опиши логику пагинации:**
   - Будет ли это цикл по номерам страниц (`?page=2`)?
   - Или клик по кнопке "Next" через Playwright?
   - Или скроллинг (infinite scroll) с перехватом новых данных?
   - Как функция `get_next_page()` будет определять URL следующей страницы?
- **Поведение на странице:**
   - Какие селекторы необходимо дождаться перед началом парсинга?
   - Требуется ли скролл для подгрузки контента (Lazy Loading)?
   - Нужно ли раскрывать табы, кликать на кнопки "Показать еще"?
- **Используемые утилиты:**
   - В каких местах будет вызываться `random_delay()` из `app.utils` для защиты от банов? (Например, между страницами, перед кликом).

### 3. Проектирование `app/parser.py` (Экстракция данных)
* **3.1. Интерфейс функций**
Опиши контракт функций parser.py.

Предложи необходимый набор функций.

Для каждой функции укажи:

- назначение;
- входные параметры;
- возвращаемое значение.

Ниже приведён пример возможного интерфейса.

**Формат таблицы:**

| Функция | Назначение | Входные параметры | Возвращаемое значение |
| :--- | :--- | :--- | :--- |
| `parse_listing(html)` | Принимает сырой HTML страницы со списком, находит все карточки и вызывает `parse_single_item` для каждой. | `html: str` | `List[dict]` |
| `parse_product(html)` | Принимает сырой HTML страницы товара и извлекает детальную информацию. | `html: str` | `dict` |
| `parse_single_item(card)` | Извлекает данные из одного HTML-элемента (карточки) и возвращает словарь. | `card: bs4.element.Tag` | `dict` | 
* **3.2. Спецификация полей**
Опиши, как будут извлекаться данные. Если поле может отсутствовать, укажи значение по умолчанию (`None`, `""`, `0`).
Пример структуры результата. Адаптируй поля под требования клиента. Не добавляй поля, которые клиент не запрашивал.

* **3.3. Финальная структура результата**
Покажи, как будет выглядеть один элемент после парсинга (для `parse_single_item` и `parse_product`).

Это пример структуры. Адаптируй поля под требования клиента.

```json
{
    "title": "Пример товара",
    "price": 1250.50,
    "currency": "$",
    "url": "https://example.com/product/123",
    "image": "https://example.com/img.jpg",
    "availability": true,
    "sku": "SKU-12345"
}

### 4. Обработка ошибок
Опиши стратегию для каждого сценария. Это критически важно для стабильности скрапера.

Формат:

Сценарий	Действие
Timeout (страница не загрузилась)	Предложи стратегию обработки timeout, включая количество повторов и условия остановки.. Если не удалось — записать ошибку в лог и пропустить страницу.
HTTP 403 (Forbidden)	Записать в лог, остановить скрапер (или сделать длительную паузу).
CAPTCHA	Записать в лог, остановить скрапер (требуется ручное вмешательство).
Элемент не найден (отсутствует цена)	Записать None или значение по умолчанию в словарь. Не прерывать парсинг всей страницы.
Битый JSON (если работаем с API)	Попытаться спарсить через json.loads() в try/except. При ошибке — записать в лог и вернуть None.
Пустая страница (нет товаров)	Записать в лог и завершить пагинацию.

---

### 5. Оценка рисков
Отметь, с какими рисками может столкнуться проект. Это поможет на этапе тестирования и отладки.

Формат (чек-лист):

Cloudflare (защита)

Требуется авторизация (Login)

Rate Limiting (ограничение по частоте запросов)

CAPTCHA

Infinite Scroll (бесконечный скролл)

Shadow DOM

iframe

WebSocket (для обновления данных в реальном времени)

GraphQL API

Сложная структура DOM с частыми изменениями

### 6. Порядок реализации
Чтобы разработка шла последовательно, предложи порядок написания модулей. Обоснуй порядок, а не задавать его заранее.

Формат:

text
1. parser.py — Написать первым, так как он не зависит от сети. Можно тестировать на сохраненном HTML из AI_INPUT/page.html.
2. scraper.py — Написать вторым, используя готовый парсер для обработки полученных данных.
3. Интеграция в main.py — Подключить готовые модули к оркестратору.
4. Написание тестов — Создать тесты для парсера на фиксированных HTML-страницах.

# ОГРАНИЧЕНИЯ
- **ЗАПРЕЩЕНО генерировать готовый Python-код.** Пиши только псевдокод, селекторы и текстовое описание алгоритмов.
- Не предлагай изменять `main.py` или `config.py`. Твое решение должно идеально встроиться в текущие интерфейсы функций ядра.
- Не усложняй архитектуру. Выбирай самое простое решение, которое покрывает требования клиента.


### 7. "Краткое резюме"

В конце ответа кратко перечисли:

- выбранную технологию;
- основные функции scraper.py;
- основные функции parser.py;
- итоговую структуру данных;
- главные риски проекта.