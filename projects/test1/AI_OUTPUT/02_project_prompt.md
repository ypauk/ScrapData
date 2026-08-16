# РОЛЬ

Ты — Senior Python Developer / Web Scraping Engineer. Твоя цель — спроектировать техническое решение для конкретного сайта клиента **БЕЗ написания самого кода**. 

Ты должен распределить логику по существующей функциональной структуре проекта.

---

# ВХОДНЫЕ ДАННЫЕ
- **Описание задачи клиента:** Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing


The Google Sheet has already been fully converted into:

DS-PRK-Scraper.json
IMPORTANT

DS-PRK-Scraper.json is the complete and authoritative specification of the required output structure.

Do NOT try to access, retrieve, or reconstruct the Google Sheet.

Do NOT make assumptions about the required fields.

Do NOT add, remove, rename, merge, split, or reinterpret output columns unless explicitly instructed to do so.

Everything required from the Google Sheet that is relevant to the scraper output has already been transferred to DS-PRK-Scraper.json.

- **Утвержденная стратегия (Шаг 1):** ## 1. Краткое описание задачи


Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает информацию о товарах и сохраняет её в **JSON**.


На текущем этапе требуется **не полный scrape**, а тестовый результат только для **2 товаров**. Перед дальнейшим расширением клиент ожидает проверочный файл.


Главное требование — **каждое поле должно находиться в собственной колонке/поле JSON**, без смешивания нескольких типов данных.


Авторитетная спецификация структуры находится в `DS-PRK-Scraper.json`. Её необходимо соблюдать буквально: порядок, названия и состав полей менять нельзя. GitHub


При этом:



- товары без скидки включаются;

- `Sale price` для товара без скидки оставляется пустым;

- отсутствующие характеристики пока оставляются пустыми;

- описание сохраняется как **чистый текст**, без HTML;

- изображения нужно **скачивать**, а не только сохранять URL;

- ожидаемый результат сейчас — 2 товара;

- товары out-of-stock также должны включаться;

- порядок полей должен соответствовать спецификации.


**Уверенность: высокая.**



## 2. Какой конечный результат нужен


Нужен:



- **JSON-файл**;

- содержащий данные для 2 тестовых товаров;

- со структурой строго по `DS-PRK-Scraper.json`;

- с отдельными полями для:



- URL;

- Breadcrumb;

- Title;

- Short description;

- imageurl;

- image_name;

- Price;

- Sale price;

- Description;

- Specs;

- Spec_detail.


Для `imageurl` и `image_name`, если изображений несколько, они должны разделяться запятыми согласно инструкции спецификации.


`Spec_detail` должен содержать характеристики, где текст до `:` становится названием характеристики, а значение после `:` — её значением. GitHub


Также изображения должны быть физически скачаны.


**Уверенность: высокая.**



## 3. Как лучше решить задачу


Рекомендую **Playwright + парсинг HTML**, с использованием уже существующего `PlaywrightEngine` проекта.


Оптимальная последовательность:



- Открыть категорию.

- Получить ссылки на товары.

- Для теста выбрать первые/нужные 2 товара.

- Открыть страницы товаров.

- Извлечь данные из HTML.

- Отдельно обработать характеристики.

- Скачать изображения.

- Сформировать JSON строго в заданном порядке.


Причина выбора Playwright — проект уже зафиксирован на `PlaywrightEngine`, поэтому менять его на другой транспортный механизм нецелесообразно. Сам сайт также имеет признаки JavaScript/browser-зависимого поведения, а в предоставленных notes прямо указано: `API нет, и сайт на JS`. Кроме того, cookies и Cloudflare clearance присутствуют в предоставленных данных. GitHub


При этом **не требуется усложнять решение дополнительным API-слоем**.


Есть важный нюанс: по доступному HTML сайт способен отдавать существенную часть информации непосредственно в странице. Например, карточка `Polar DM071` содержит ссылку, название и цены, а product page содержит описание и характеристики. Professionele Koeling+1


**Уверенность: высокая.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Как основной подход не рекомендую.


Причина не в том, что HTML невозможно получить обычным HTTP-запросом, а в том, что согласно условиям проекта `scraper.py` уже работает через `PlaywrightEngine`. Замена транспорта даст лишнюю сложность и не соответствует зафиксированной инфраструктуре.


### Selenium


Рабочий вариант, но хуже Playwright в данном проекте: Playwright уже является предусмотренным движком.


### Scrapy


Избыточен для текущего масштаба — сейчас требуется всего 2 товара, а не сложный распределённый crawler.


### API


Не рекомендую. В `network.har` ничего нет, а в notes явно указано отсутствие API. Доказательств существования необходимого публичного API нет. GitHub


### GraphQL


Доказательств GraphQL также нет.


### Только category listing


Для некоторых полей этого достаточно, но **для полного набора требуемых данных недостаточно**. В category listing видны название, URL, изображение и цены, тогда как подробное описание и характеристики находятся на product page. Это видно на примере `Polar DM071`. Professionele Koeling+1


Следовательно, для полного результата нужно переходить на страницы товаров.



## 5. Анализ сайта


ВозможностьВыводУверенностьJavaScript Rendering**Да / вероятно используется**ВысокаяReactНе обнаруженСредняяVueНе обнаруженСредняяAngularНе обнаруженСредняяAPI**Не обнаружен**ВысокаяGraphQLНе обнаруженСредняяInfinite ScrollНе обнаруженВысокаяPagination**Да**ВысокаяLoginДля товаров не требуетсяВысокаяCookies**Да**ВысокаяJWTНе обнаруженСредняяBearer TokenНе обнаруженСредняяCAPTCHA**Есть CAPTCHA на форме review**ВысокаяCloudflare**Да, есть cf_clearance cookie**ВысокаяRate limitsТочные лимиты неизвестныНизкая/средняяDownload filesИзображения товаров необходимо скачиватьВысокаяUpload filesНе требуетсяВысокаяLazy loadingНе подтвержденоНизкаяWebSocketНе обнаруженСредняяXHR/FetchНе подтвержденСредняяSitemapНе удалось надёжно проверить из предоставленных материаловВысокая
Сайт использует обычную пагинацию. На исходной категории указано **429 товаров**, по 36 на страницу; в HTML присутствуют ссылки на страницы `p=2`, `p=3` и далее. GitHub+1


Актуальный поисковый результат также подтверждает серверно доступный HTML category page с товарами и ценами. Professionele Koeling


Интересно, что доступный HTML показывает достаточно данных без необходимости выполнять сложный frontend-анализ. Например, product page `Polar DM071` содержит описание, характеристики, наличие и цены непосредственно в странице. Professionele Koeling


**Cloudflare:** наличие `cf_clearance` в предоставленных cookies говорит о том, что защита Cloudflare присутствует. Это не означает автоматически, что scraper будет блокироваться, но риск учитывать нужно. GitHub


**CAPTCHA:** она обнаружена в контексте отправки product review, поэтому сама по себе не является препятствием для чтения товарных страниц. Professionele Koeling



## 6. Что необходимо собрать до начала разработки


**Критически необходимой дополнительной информации сейчас не требуется.**


Уже предоставлены:



- `description.txt`;

- `DS-PRK-Scraper.json`;

- `page.html`;

- `category-page.html`;

- `pagination.html`;

- `product-page.html`;

- `cookies.json`;

- `headers.json`;

- `network.har`;

- `notes.txt`;

- `checkpoint.json`;

- `traceback.txt`;

- `answers.txt`;

- `proxies.txt`.


Причём спецификация прямо говорит, что `DS-PRK-Scraper.json` является окончательной и авторитетной структурой и не требует восстановления исходной Google Sheet. GitHub


Единственное, что понадобится непосредственно при реализации, — доступ браузера к реальным страницам товаров и возможность скачать оригинальные изображения.


**Уверенность: высокая.**



## 7. Возможные сложности


### 1. Cloudflare


Наиболее существенный риск. В cookies уже присутствует `cf_clearance`. При массовом scrape могут возникать challenge/blocking. GitHub


### 2. Большое количество товаров


Сейчас тест — 2 товара, но исходная категория содержит **429 товаров**. Полный scrape потребует обхода pagination. Professionele Koeling


### 3. Изменение HTML


Селекторы могут перестать работать после изменения Magento/theme.


### 4. Данные находятся в разных местах


Название/цена/изображение доступны в listing, но подробное описание и характеристики — на product page. Поэтому нельзя рассчитывать исключительно на category page. Professionele Koeling+1


### 5. Неодинаковая заполненность товаров


У разных товаров могут отсутствовать:



- скидочная цена;

- отдельные характеристики;

- изображения;

- некоторые значения спецификаций.


По условиям проекта такие поля нужно оставлять пустыми, а не пытаться восстанавливать значения.


### 6. Изображения


Нужно не просто сохранить URL, а скачать файлы. Возможны:



- несколько изображений;

- разные URL;

- изменение CDN/media path;

- проблемы доступа к изображениям.


### 7. Формат характеристик


`Spec_detail` требует преобразования данных вида:


`Header: Value`


в отдельные поля/колонки согласно правилам спецификации. Это место требует аккуратного парсинга, чтобы не потерять характеристики, содержащие дополнительные `:`.


### 8. Актуальность cookies


Предоставленные cookies могут быть временными и со временем перестать работать. Их нельзя считать постоянным способом обхода Cloudflare.


**Уверенность: высокая.**



## 8. Что нужно уточнить у клиента


На данный момент **обязательных вопросов клиенту нет**.


В предоставленном prompt уже есть ответы на ключевые вопросы:



- формат — JSON;

- сейчас нужны 2 товара;

- изображения нужно скачивать;

- отсутствие sale price → пустое поле;

- отсутствие характеристик → пустые поля;

- описание → чистый текст;

- out-of-stock товары включаются;

- порядок полей сохраняется;

- `DS-PRK-Scraper.json` является окончательной спецификацией. GitHub


Единственное потенциальное уточнение, которое **можно задать**, но без него можно начать тестовую реализацию:



Какие именно 2 товара использовать для тестового файла — первые 2 товара категории или конкретные товары?



Однако это не блокирующий вопрос, поскольку в предоставленном `page.html` первый товар — `Polar DM071`, а клиент обозначил текущий объём как 2 товара. GitHub+1


**Уверенность: высокая.**



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **BeautifulSoup**


Этого достаточно.


Не нужен отдельный API-клиент, Scrapy или Selenium.



## 10. План разработки


### Этап 1 — Проверка доступа к сайту


**Цель:** убедиться, что Playwright может стабильно открыть category и product pages.


**Ожидаемый результат:** успешное получение HTML и отсутствие блокировки.


**Зависимости:** PlaywrightEngine, доступ к сайту.



### Этап 2 — Получение 2 товаров


**Цель:** получить ссылки двух тестовых товаров из категории.


**Ожидаемый результат:** 2 корректных product URL.


**Зависимости:** category page.



### Этап 3 — Извлечение основных данных


**Цель:** собрать URL, breadcrumb, title, short description, prices и изображения.


**Ожидаемый результат:** базовые поля двух товаров.


**Зависимости:** product pages.



### Этап 4 — Извлечение полного описания и характеристик


**Цель:** получить чистый текст Description и отдельные значения спецификаций.


**Ожидаемый результат:** все поля из `DS-PRK-Scraper.json`, включая отсутствующие значения как пустые.


**Зависимости:** product pages.



### Этап 5 — Загрузка изображений


**Цель:** скачать все изображения каждого товара.


**Ожидаемый результат:** локальные image files + соответствующие `imageurl` и `image_name`.


**Зависимости:** доступ к media URLs.



### Этап 6 — Формирование тестового JSON


**Цель:** собрать два товара строго по спецификации.


**Ожидаемый результат:** валидный JSON с правильными названиями и порядком полей.


**Зависимости:** этапы 3–5.



### Этап 7 — Проверка результата


**Цель:** сравнить результат с `DS-PRK-Scraper.json` и исходными страницами.


**Ожидаемый результат:** тестовый JSON без лишних/пропущенных полей и без смешивания данных.


**Зависимости:** готовый JSON.



### Этап 8 — Только после успешного теста — расширение


**Цель:** при одобрении клиента перейти от 2 товаров к полному scrape.


**Ожидаемый результат:** обработка всех товаров и pagination.


**Зависимости:** подтверждение тестового файла клиентом.



## 11. Оценка сложности


ПараметрОценкаСложность**4/10**Разработка тестовой версии**3–5 часов**Разработка полного scraper**6–10 часов**Вероятность блокировок**Средняя**Вероятность необходимости браузера**Высокая**Вероятность изменения сайта**Средняя**Общий риск**Средний**
### Почему не выше 4/10


Структура сайта относительно простая: category → product pages → HTML data. Pagination стандартная, а количество товаров не является экстремальным.


Главный фактор риска — не парсинг, а **Cloudflare/стабильность браузерного доступа**.


Также есть уже готовая спецификация выходных данных, поэтому не требуется самостоятельно проектировать структуру результата. GitHub



## 12. Можно ли решить проще


**Да.**


Самое простое решение — использовать уже предоставленный `PlaywrightEngine`, открыть category page, получить product links и перейти только на страницы товаров.


Не нужно:



- искать API;

- создавать отдельную API-интеграцию;

- использовать базу данных;

- использовать Scrapy;

- строить сложную crawler-архитектуру;

- использовать Selenium;

- пытаться получать данные из Google Sheet;

- восстанавливать `DS-PRK-Scraper.json`.


Более того, нет необходимости обходить весь сайт на первом этапе: клиент прямо требует сначала **2 товара**. GitHub


После успешного теста можно просто расширить тот же механизм на pagination.


При этом вариант «парсить только category listing» недостаточен для финальной структуры: подробный `Description` и `Spec_detail` требуют product page. Это подтверждается сравнением category page и `Polar DM071` product page. Professionele Koeling+1


**Итого: PlaywrightEngine + HTML parsing + product pages — наиболее простое решение, соответствующее ограничениям проекта.**



## 13. Итоговая рекомендация


Рекомендую **не менять существующий PlaywrightEngine** и сделать простой двухступенчатый scraper:


**category → product URLs → product pages → parse → download images → JSON.**


Это оптимальный вариант, потому что:



- он соответствует зафиксированной инфраструктуре проекта;

- не требует поиска/разработки API;

- не требует сложного crawler framework;

- product pages содержат необходимые подробные данные; Professionele Koeling

- pagination уже существует и легко масштабируется после теста; Professionele Koeling

- структура JSON уже полностью определена клиентом.


**Что необходимо получить:** по сути, ничего дополнительного. Все критические требования уже присутствуют в предоставленном prompt и файлах.


**Можно ли переходить к коду:** **да, для тестового scrape двух товаров**. Вопрос с выбором конкретных двух товаров желательно уточнить, если клиент ожидает не первые два товара, но это не является техническим блокером.


**Код на данном этапе намеренно не привожу**, поскольку исходный prompt прямо запрещает переходить к реализации и требует сначала закончить анализ. GitHub


**Итоговая уверенность:** **высокая — около 90%**. Основная неопределённость связана не со структурой задачи, а с реальным поведением Cloudflare/JavaScript при запуске scraper и с тем, какие именно два товара клиент хочет видеть в тестовом файле.
- **Анализ разметки/API (из файлов в AI_INPUT):** 

--- ФАЙЛ: description.txt ---
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing


The Google Sheet has already been fully converted into:

DS-PRK-Scraper.json
IMPORTANT

DS-PRK-Scraper.json is the complete and authoritative specification of the required output structure.

Do NOT try to access, retrieve, or reconstruct the Google Sheet.

Do NOT make assumptions about the required fields.

Do NOT add, remove, rename, merge, split, or reinterpret output columns unless explicitly instructed to do so.

Everything required from the Google Sheet that is relevant to the scraper output has already been transferred to DS-PRK-Scraper.json.


--- ФАЙЛ: DS-PRK-Scraper.json ---

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
 }

--- ФАЙЛ: answers.txt ---


--- СЖАТЫЙ HTML: category-page.html ---
<ul class="products-grid category-products-grid itemgrid itemgrid-adaptive itemgrid-3col centered hover-effect equal-height">
 Здесь карточки в блоках li , пример page.html
</ul>


--- ФАЙЛ: checkpoint.json ---
{
  "run_id": "run_20260813_053013",
  "status": "completed",
  "current_page": 1,
  "current_url": null,
  "processed_count": 49,
  "exported_count": 0,
  "timestamp": "2026-08-13T02:30:14.073491+00:00",
  "extra_metadata": {
    "total_pages": 1,
    "processed_count": 49,
    "exported_count": 49
  }
}

--- ФАЙЛ: cookies.json ---
[
  {
    "name": "IDE",
    "value": "AHWqTUkGXT_lYsWHDGRgB8smCsDlVHW2fgC8Xq9PSGudosZbHGO9wrmuJfcJ68Ku",
    "domain": ".doubleclick.net",
    "path": "/",
    "expires": 1821011169.764994,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  },
  {
    "name": "_ga",
    "value": "GA1.1.1255001230.1786435293",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1821198971.799038,
    "httpOnly": false,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "_gcl_au",
    "value": "1.1.1365411882.1786435292",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1794211292,
    "httpOnly": false,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "cf_clearance",
    "value": "Lio7gAuTnro0VUsn510AU9wwTNd8HP4uPIoaSW3iqcw-1786638972-1.2.1.1-pP8lOrnGEfxhJLAUgZmhSnilu78R1B0pLj5ctfMchYjDVf7gfdldmBq_jFoSi1oOkFovY0IP.hZn2LBH8uyKoK9AltZos3Gw4tQ9EczM.j7QE1BLgAsW2tWuJSe395.SAUMWNlZS6Ieg_kpYMnJoI7PYWEBbYLhs6Nqy4AuBHvpflmA4_vEl_5T5w9Im0SUQe_Zm.ZGve.AqyVCPZ8pVO93hK8qBrdhQj272n1XhAcrz2TcGvW6mljvgN2QbfKUK.Wn9KCCiBM681v0Gu0NFctMrpXyhbG9NyHlaDucpWMKnXO7JSuol2AJZQ_SsKQ13VK9w7hvYfqS6mOrNDlPmJWZ3HKhx1F12gPpwkmVVZdA",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1818174972.380038,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  },
  {
    "name": "_ga_3X7F7CBMN7",
    "value": "GS2.1.s1786638820$o5$g1$t1786638971$j60$l0$h0",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1821198971.797038,
    "httpOnly": false,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "frontend",
    "value": "r2vm916serog03f4a766gn5she",
    "domain": ".www.professionele-koeling.nl",
    "path": "/",
    "expires": 1786642571.290038,
    "httpOnly": true,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "frontend_cid",
    "value": "Q4B3fmBXdKCFmkrF",
    "domain": ".www.professionele-koeling.nl",
    "path": "/",
    "expires": 1786642571.290038,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  }
]

--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---
API нет , и сайт на JS

ВАЖНО: DS-PRK-Scraper.json — это КОРРЕКТНАЯ и ФИНАЛЬНАЯ спецификация. Значения вроде "if multipli seperated by comma" и "evertything before the : is the header" — это инструкции по заполнению полей, а НЕ повреждённые данные. Файл валиден. Используй его как есть. НЕ запрашивай "оригинальную версию" и НЕ считай его повреждённым.


Какой итоговый формат нужен: json

Нужно ли собирать весь сайт или только определённые категории? сначала только 2 товара
Нужно ли скачивать изображения или достаточно URL? надо
Если у товара нет скидки — оставлять пустое поле или копировать обычную, - пустое
Как обрабатывать отсутствующие характеристики? - пока пусты поля
Нужно ли сохранять HTML-разметку описания или только чистый текст? текст
Нужно ли включать товары, которых нет в наличии? - надо
Сколько примерно товаров ожидается? сейчас 2
Google Sheet содержит окончательный список всех колонок? да
Нужно ли сохранять порядок колонок строго как в Google Sheet? - да

--- СЖАТЫЙ HTML: page.html ---
https://www.professionele-koeling.nl/koelkasten-kisten.html - категория
<li class="item">
 <div class="product-image-wrapper">
  <a class="product-image" href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html">
   <img id="product-collection-image-212" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg"/>
  </a>
  <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover">
   <li>
    <a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/SiBQpy2rW3vTJnQQ/">
     <span class="2 icon ib ic ic-heart">
     </span>
    </a>
   </li>
   <li>
    <a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/form_key/SiBQpy2rW3vTJnQQ/">
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


--- СЖАТЫЙ HTML: pagination.html ---
<div class="toolbar-bottom">
 <div class="toolbar">
  <div class="sorter">
   <p class="amount">
    Artikelen 1 tot 36 van 429 in totaal
   </p>
   <div class="sort-by">
    <label>
     Sorteer op
    </label>
    <select>
     <option>
      Positie
     </option>
     <option>
      Naam
     </option>
     <option>
      Prijs
     </option>
     <option>
      Vermogen
     </option>
    </select>
    <a class="category-asc ic ic-arrow-down" href="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=desc&amp;order=price">
    </a>
   </div>
   <div class="limiter">
    <label>
     Toon
    </label>
    <select>
     <option>
      12
     </option>
     <option>
      24
     </option>
     <option>
      36
     </option>
    </select>
    <span class="per-page">
     per pagina
    </span>
   </div>
   <p class="view-mode">
    <label>
     Tonen als:
    </label>
    <span class="grid ic ic-grid">
    </span>
    <a class="list ic ic-list" href="https://www.professionele-koeling.nl/koelkasten-kisten.html?mode=list">
    </a>
   </p>
  </div>
  <!-- end: sorter -->
  <div class="pager">
   <div class="pages">
    <strong>
     Pagina:
    </strong>
    <ol>
     <li class="current">
      1
     </li>
     <li>
      <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=2">
       2
      </a>
     </li>
     <li>
      <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=3">
       3
      </a>
     </li>
     <li>
      <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=4">
       4
      </a>
     </li>
     <li>
      <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=5">
       5
      </a>
     </li>
     <li class="next">
      <a class="next ic ic-right" href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=2">
      </a>
     </li>
    </ol>
   </div>
  </div>
 </div>
</div>


--- СЖАТЫЙ HTML: product-page.html ---
<div class="breadcrumbs">
 <ul>
  <li class="home">
   <a href="https://www.professionele-koeling.nl/">
    <span>
     Home
    </span>
   </a>
   <span class="sep">
   </span>
  </li>
  <li class="category3">
   <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html">
    <span>
     Koelkasten&amp;Kisten
    </span>
   </a>
   <span class="sep">
   </span>
  </li>
  <li class="product">
   <span class="last-crumb">
    Polar GE579
   </span>
  </li>
 </ul>
</div>
<div class="product-name">
 <h1>
  Polar GE579
 </h1>
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


--- ФАЙЛ: proxies.txt ---


--- ФАЙЛ: traceback.txt ---


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

# ТЕХНОЛОГИЯ СБОРА (ФИКСИРОВАНА ФРЕЙМВОРКОМ)

**ВАЖНО:** Фреймворк использует `PlaywrightEngine` для ВСЕХ проектов. Это зафиксировано в `main.py`:

```python
with PlaywrightEngine() as engine:
    raw_pages_content = scrape_data(engine)  # List[str] — список HTML страниц

# Затем main.py напрямую вызывает parser:
page_records = parse_listing(html)              # один HTML → List[Dict]
scraped_results = parse_html_data(raw_pages_content)  # List[str] → List[Dict]
```

**Контракт неизменяем:** `scrape_data(engine) → List[str]`. Каждый элемент списка — HTML одной страницы (листинг или страница товара). `main.py` вызывает `parser.parse_listing()` / `parse_html_data()` напрямую — scraper.py парсером не является и parser не вызывает.

`scraper.py` ВСЕГДА получает готовый `PlaywrightEngine` (с cookies, proxy, user-agent) и использует его для навигации. НЕ рекомендуй `requests` или `httpx` для scraper.py — это невозможно в данном фреймворке.

`parser.py` использует BeautifulSoup для парсинга HTML, полученного от scraper.

При проектировании сфокусируйся на:
- Какие URL обходить, какая пагинация (параметры, кнопки, скролл)
- Какие селекторы ожидать на странице
- Нужно ли заходить на отдельные страницы товаров или достаточно листинга
- Какие поля извлекать и откуда
   
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

**Пример (если нужны только листинговые страницы):**

Клиент запускает main.py → PlaywrightEngine
↓
scraper.scrape_data(engine) → [html_page1, html_page2, ...]  (List[str])
↓
main.py вызывает parse_html_data([html_page1, ...])
↓
parser.py → list[dict]
↓
exporter.py → CSV / JSON

**Пример (если нужно заходить на страницы товаров):**

Клиент запускает main.py → PlaywrightEngine
↓
scraper.scrape_data(engine):
    1. Открыть листинг → получить HTML листинга
    2. Внутри scraper из HTML листинга извлечь URL товаров (через BeautifulSoup или regex)
    3. Зайти на каждую страницу товара → получить HTML
    4. Вернуть List[str] — все собранные HTML (листинги + страницы товаров, или только страницы товаров)
↓
main.py вызывает parse_html_data([html_product1, html_product2, ...])
↓
parser.py → list[dict]
↓
exporter.py → CSV / JSON

**Ключевое правило:** если данные нужны со страниц товаров — scraper.py сам извлекает URL товаров из HTML листинга (это навигационная логика, не парсинг бизнес-данных) и обходит product pages. parser.py в scraper.py НЕ импортируется.

### 2. Проектирование `app/scraper.py` (Сетевой сбор)

* **2.1. Интерфейс функций

Опиши контракт каждой функции, которую будет содержать `scraper.py`.
Предложи необходимый набор функций.

**Обязательная главная функция:** `scrape_data(engine) → List[str]` — это зафиксировано в main.py и не может быть изменено.

Если сайт требует заходить на страницы товаров, вспомогательные функции могут быть:
- `_fetch_listing_html(engine, url) → str` — получить HTML листинга
- `_fetch_product_html(engine, url) → str` — получить HTML страницы товара
- `_extract_product_urls(html) → List[str]` — извлечь URL товаров из HTML листинга (навигационная логика, допустима в scraper.py)
- `_get_next_page_url(html, current_url) → str | None` — определить URL следующей страницы

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