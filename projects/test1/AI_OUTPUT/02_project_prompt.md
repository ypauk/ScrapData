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


Клиент хочет получить scraper для сайта Professionele-koeling.nl, который собирает данные о товарах из категории `koelkasten-kisten.html`.


На текущем этапе требуется **только тестовая выгрузка 2 товаров**. После успешной проверки предполагается масштабирование на весь объём.


Ключевое требование — итоговый JSON должен строго соответствовать структуре `DS-PRK-Scraper.json`: нельзя переименовывать, добавлять, удалять, объединять или разделять поля.


Для каждого товара требуются:



- URL;

- Breadcrumb;

- Title;

- Short description;

- URL изображений;

- имена изображений;

- обычная цена;

- Sale price;

- полное описание как чистый текст;

- `Specs`;

- отдельные характеристики из `Spec_detail`.


При отсутствии скидки `Sale price` должен быть пустым. Отсутствующие характеристики также должны оставаться пустыми.


В предоставленных данных уже есть достаточное подтверждение структуры сайта: листинг содержит ссылки на товары и цены, а product page содержит описание, характеристики и дополнительные данные. Текущий сайт также показывает пагинацию и JavaScript-зависимость интерфейса. Professionele Koeling+1


**Уверенность: высокая (≈90%).**



## 2. Какой конечный результат нужен


**JSON.**


Причём структура каждого объекта должна следовать авторитетной спецификации `DS-PRK-Scraper.json` и сохранять порядок полей:



- `URL`

- `Breadcrumb`

- `Title `

- `Short description`

- `imageurl`

- `image_name`

- `Price`

- `Sale price`

- `Description `

- `Specs`

- `Spec_detail`


Изображения необходимо **скачивать**, а не только сохранять их URL.


На тестовом этапе — **2 товара**.



## 3. Как лучше решить задачу


### Рекомендация: PlaywrightEngine + парсинг HTML через BeautifulSoup


Это оптимальный вариант с учётом ограничения проекта: `scraper.py` получает готовый `PlaywrightEngine`, поэтому переходить на самостоятельный `requests`-scraper не нужно.


Логика должна быть максимально простой:



- Playwright открывает категорию.

- Из HTML листинга извлекаются URL товаров.

- Для двух тестовых товаров открываются product pages.

- Из HTML извлекаются нужные поля.

- HTML описания преобразуется в чистый текст.

- Характеристики разбираются по правилу из спецификации.

- Изображения скачиваются.

- Формируется JSON строго установленной структуры.


Это предпочтительнее сложного browser automation: на странице товары и их основные данные представлены обычными HTML-элементами. Например, листинг содержит название, ссылку и цены товара, а product page содержит описание и таблицу дополнительной информации. Professionele Koeling+1


При этом Playwright полезен как транспорт/браузерный слой, поскольку в исходных материалах явно указано, что сайт работает с JS и проект уже предоставляет `PlaywrightEngine`.


**Уверенность: высокая.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Как самостоятельный подход не рекомендую.


Во-первых, это противоречит зафиксированному устройству проекта: `scraper.py` уже получает `PlaywrightEngine`.


Во-вторых, сайт явно сообщает, что JavaScript должен быть включён для полной функциональности. Professionele Koeling


При этом **BeautifulSoup всё равно стоит использовать для разбора уже полученного HTML**, поскольку это существенно проще, чем извлекать каждое поле средствами Playwright.


### Selenium


Не даёт преимуществ перед уже предусмотренным PlaywrightEngine. Добавляет лишнюю сложность.


### Scrapy


Для двух тестовых товаров из одной категории — избыточен. Для будущих 429 товаров всё равно не требуется полноценная Scrapy-архитектура.


### API


Предоставленные материалы прямо говорят: `API нет`.


Также в `network.har` ничего не предоставлено. Поэтому строить решение вокруг API сейчас оснований нет.


### GraphQL


Признаков GraphQL нет.


### Только листинг


Для **полного** результата этого недостаточно: в карточке категории присутствуют название, URL, изображения и цены, но подробное описание и дополнительные характеристики находятся на product page. Это видно, например, по Polar DM071: дополнительные характеристики и полное описание присутствуют только на странице товара. Professionele Koeling


Поэтому переход на product pages необходим, если все поля спецификации должны быть заполнены.



## 5. Анализ сайта


ВозможностьСтатусВыводJavaScript Rendering**Есть / используется**Сайт предупреждает о необходимости JS; Playwright уже предусмотренReact**Не обнаружен**Признаков React в предоставленном HTML нетVue**Не обнаружен**Признаков нетAngular**Не обнаружен**Признаков нетAPI**Не обнаружен**В notes указано, что API нетGraphQL**Не обнаружен**Признаков нетInfinite Scroll**Не обнаружен**Используется обычная пагинацияPagination**Есть**`?p=2`, `?p=3` и т.д.Login**Есть как функция сайта, но scraper не требует login**Product pages доступны без авторизацииCookies**Есть**Предоставлен `cookies.json`JWT**Не обнаружен**Признаков нетBearer Token**Не обнаружен**Признаков нетCAPTCHA**Есть на форме review**Для scraping товаров несущественноCloudflare**Есть признаки**В cookies присутствует `cf_clearance`Rate Limits**Неизвестно**Надёжно определить по предоставленным данным нельзяDownload Files**Требуется для изображений**Изображения нужно скачиватьUpload Files**Не требуется**—Lazy Loading**Не подтверждено**Нужно проверить реальные image attributes во время реализацииWebSocket**Не обнаружен**Признаков нетXHR/Fetch**Неизвестно**HAR отсутствуетSitemap**Есть ссылка на sitemap в сайте**, но `robots.txt/sitemap.xml` напрямую через текущий доступ не удалось подтвердитьНе использовать как обязательный источник
Пагинация подтверждается непосредственно текущей страницей: сейчас сайт показывает `1–36 из 429` и ссылки на последующие страницы. Professionele Koeling


Интересный момент: поисковая индексация также показывает вариант подкатегории с `275` товарами, тогда как исходная категория сейчас показывает `429`. Это ещё одна причина **не хардкодить количество товаров** и ориентироваться на фактическую пагинацию сайта. Professionele Koeling+1


Product pages доступны без login; например, Polar DM071 содержит availability, цены, описание и дополнительные характеристики непосредственно в HTML. Professionele Koeling


**Уверенность:**



- HTML/pagination/product structure — высокая;

- Cloudflare — высокая по предоставленным cookies;

- React/Vue/Angular/GraphQL/WebSocket — средняя, поскольку отсутствие признаков в доступном HTML не доказывает абсолютное отсутствие технологий.



## 6. Что необходимо собрать до начала разработки


**Критически необходимой дополнительной информации сейчас нет.**


Предоставленных материалов достаточно, чтобы начать реализацию теста.


Уже имеются:



- `description.txt`;

- `DS-PRK-Scraper.json`;

- `category-page.html`;

- `page.html`;

- `product-page.html`;

- `pagination.html`;

- `cookies.json`;

- `headers.json`;

- `network.har` как файл, но он пуст;

- `checkpoint.json`;

- `notes.txt`.


Особенно важно, что `DS-PRK-Scraper.json` прямо объявлен финальной спецификацией. Поэтому **не нужно запрашивать оригинальную Google Sheet**.


Однако перед полноценным scrape желательно проверить:



- HTML реальных изображений на двух тестовых товарах;

- все варианты представления `Specs`/`Spec_detail`;

- наличие товаров без скидки;

- наличие товаров без отдельных характеристик;

- наличие товаров без изображений или с несколькими изображениями.


Это уже вопросы реализации/валидации, а не блокирующие вопросы к клиенту.



## 7. Возможные сложности


### 1. Cloudflare / блокировки


В `cookies.json` присутствует `cf_clearance`, поэтому Cloudflare действительно следует учитывать.


Риск для двух товаров небольшой, но при переходе к сотням страниц возрастёт.


### 2. Срок жизни cookies


`cf_clearance` и session cookies имеют срок действия. Нельзя рассчитывать, что предоставленные cookies будут работать бесконечно.


### 3. Изменение HTML


Сайт построен на старом ecommerce-шаблоне с CSS-классами вроде `product-name`, `price-box`, `special-price`, поэтому selectors достаточно понятны, но HTML всё равно может измениться.


### 4. 429 товаров


Текущая категория показывает 429 товаров и 36 товаров на странице. Professionele Koeling


Следовательно, для полного scrape потребуется корректно обработать пагинацию и не ограничиться первой страницей.


### 5. Несогласованность количества товаров


В предоставленном checkpoint указано `49` обработанных товаров, тогда как текущий сайт показывает 429 товаров. Это не следует считать актуальным количеством: checkpoint относится к предыдущему запуску.


### 6. Разные типы характеристик


На product page часть характеристик представлена в отдельном блоке `Extra informatie`, а подробные характеристики находятся внутри описания. Например, у DM071 отдельно присутствуют `Merk`, `Kleur`, `Breedte`, `Diepte`, `Hoogte`, `Temperatuurbereik` и т.д. Professionele Koeling


### 7. Изображения


Требуется не просто получить `imageurl`, а скачать изображения. Нужно учитывать несколько изображений одного товара и сохранять их через запятую в соответствии со спецификацией.


### 8. Изменение URL товаров


URL может отличаться от ожидаемого slug. Поэтому URL следует брать из фактической ссылки карточки категории, а не строить из названия товара.


### 9. Текстовое описание


Нужно удалить HTML-разметку, но при этом не потерять содержимое списков, переносы и значения характеристик.


### 10. CAPTCHA


CAPTCHA обнаружена на форме review, но эта функциональность scraper'у не нужна. Поэтому CAPTCHA не должна влиять на scraping product data.



## 8. Что нужно уточнить у клиента


Согласно предоставленному `answers.txt`, большинство вопросов уже закрыто.


**Блокирующих вопросов нет.**


Есть один вопрос, который желательно уточнить перед полной выгрузкой:



После успешного теста из 2 товаров нужно ли автоматически переходить ко всем товарам категории (сейчас сайт показывает 429), или клиент сначала отдельно подтвердит тестовый результат?



Но это не препятствует текущей задаче.


Также желательно подтвердить, что под «надо [скачивать изображения]» клиент подразумевает физическое сохранение файлов изображений в рамках результата, а не только загрузку их в память во время scraping.


**Уверенность: высокая.**



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **BeautifulSoup**


Этого достаточно.


API, Selenium, Scrapy и отдельный frontend/browser framework не нужны.



## 10. План разработки


### Этап 1 — Проверка входной страницы


**Цель:** убедиться, что Playwright стабильно открывает категорию и получает необходимые HTML-элементы.


**Результат:** стабильное получение category HTML и списка product URLs.


**Зависимости:** `PlaywrightEngine`.


### Этап 2 — Извлечение двух товаров


**Цель:** получить ровно 2 товара для тестовой выгрузки.


**Результат:** два корректных product URL.


**Зависимости:** этап 1.


### Этап 3 — Парсинг product pages


**Цель:** извлечь все поля из `DS-PRK-Scraper.json`.


**Результат:** два полностью сформированных объекта с правильными названиями и порядком полей.


**Зависимости:** этап 2.


### Этап 4 — Обработка характеристик


**Цель:** преобразовать характеристики в требуемые отдельные поля.


**Результат:** каждый параметр до `:` становится header, значение после `:` — содержимым соответствующего поля, согласно инструкции спецификации.


**Зависимости:** этап 3.


### Этап 5 — Изображения


**Цель:** скачать изображения товаров.


**Результат:** физически сохранённые изображения + соответствующие `imageurl` и `image_name`.


**Зависимости:** этап 3.


### Этап 6 — Валидация JSON


**Цель:** проверить соответствие финальной спецификации.


**Результат:** валидный JSON с двумя товарами, без лишних/пропущенных полей.


**Зависимости:** этапы 3–5.


### Этап 7 — Масштабирование


**Цель:** после одобрения теста перейти ко всему набору товаров.


**Результат:** обработка всех страниц категории с checkpoint/retry и контролем блокировок.


**Зависимости:** одобрение тестового файла клиентом.



## 11. Оценка сложности


ПараметрОценкаСложность**5/10**Разработка тестовой версии**3–5 часов**Полная реализация**6–10 часов**Вероятность блокировок**Средняя**Вероятность необходимости браузера**Высокая**Вероятность изменения сайта**Средняя**Общий риск**Средний**
### Почему не выше


Сайт имеет достаточно традиционную ecommerce-структуру: category → product URL → product HTML → характеристики. Пагинация обычная, а данные находятся в HTML. Professionele Koeling+1


### Главный риск


Не сложность парсинга, а **стабильность доступа** при массовом scraping из-за Cloudflare и возможного rate limiting.



## 12. Можно ли решить проще


**Да.**


Самое простое решение — использовать существующий `PlaywrightEngine` только для получения страниц, а сам HTML разбирать BeautifulSoup.


Не нужно:



- строить API;

- создавать базу данных;

- использовать Scrapy;

- использовать Selenium;

- проектировать сложную browser automation;

- делать отдельную архитектуру для React/Vue;

- реализовывать обход JavaScript-событий, если данные уже доступны в HTML.


Более того, после проверки двух товаров стоит выяснить, какие именно поля можно получить непосредственно из category page. Сейчас очевидно, что **часть** данных там есть — URL, название, изображение и цены. Professionele Koeling


Но для текущей спецификации product pages всё равно нужны, потому что подробное описание и `Extra informatie` находятся там. Например, у DM071 product page содержит характеристики, которых нет в карточке категории. Professionele Koeling


Поэтому оптимальное упрощение — не отказ от Playwright, а **минимальное использование Playwright + HTML parsing**.



## 13. Итоговая рекомендация


Рекомендую **Python + существующий PlaywrightEngine + BeautifulSoup**, без API, Scrapy или Selenium.


Это оптимально потому что:



- проект уже предусматривает PlaywrightEngine;

- сайт имеет JS-зависимость;

- данные товаров доступны в HTML;

- категория имеет обычную пагинацию;

- product pages содержат необходимые подробные данные;

- структура выходного JSON уже полностью определена;

- тестовая задача ограничена двумя товарами.


На текущем этапе **можно переходить к написанию кода**: критически необходимой информации не хватает. Сначала нужно реализовать именно тестовую выгрузку двух товаров и проверить её против `DS-PRK-Scraper.json`.


После успешной проверки теста — масштабировать на весь каталог.


**Итоговая уверенность: высокая (≈90%).**


Источники текущего состояния сайта подтверждают обычную пагинацию, наличие товаров в категории, product URLs, цены и подробные product pages. Professionele Koeling+2Professionele Koeling+2
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