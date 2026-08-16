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


Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает данные о товарах из категории `koelkasten-kisten.html`.


На текущем этапе нужен **тестовый результат только для 2 товаров**. Каждый атрибут должен находиться в отдельном поле/колонке, строго в соответствии с `DS-PRK-Scraper.json`. Изображения нужно **скачивать**, а не только сохранять URL.


Важное ограничение: `DS-PRK-Scraper.json` является финальной спецификацией, поэтому нельзя самостоятельно менять состав или порядок полей.


Сам сайт сейчас показывает 429 товаров в категории, по 36 товаров на странице, с обычной пагинацией. Professionele Koeling


**Уверенность: высокая.**



## 2. Какой конечный результат нужен


**JSON.**


Для каждого товара необходимо сохранить поля строго в порядке, заданном спецификацией:



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


Дополнительно из предоставленных инструкций:



- несколько изображений — через запятую;

- несколько имён изображений — через запятую;

- при отсутствии скидки `Sale price` оставлять пустым;

- отсутствующие характеристики оставлять пустыми;

- описание сохранять как чистый текст, без HTML;

- товары без наличия также включать;

- порядок полей не менять.



## 3. Как лучше решить задачу


### Рекомендация: Playwright + HTML-парсинг


Использовать **Playwright** как основной способ получения страниц, после чего разбирать полученный HTML.


Это наиболее подходящий вариант по нескольким причинам:



- В предоставленных notes прямо указано, что сайт работает с JavaScript.

- В проекте уже зафиксировано использование `PlaywrightEngine` для `scraper.py`, поэтому переход на `requests` в качестве основного механизма здесь не соответствует существующему framework.

- В категории присутствуют прямые ссылки на страницы товаров.

- Структура HTML достаточно хорошо определена: карточка товара содержит URL, название, цену и sale price; товарная страница содержит описание и дополнительные характеристики. Professionele Koeling+1

- Playwright позволяет сохранить наиболее надёжный вариант на случай, если отдельные данные действительно появляются только после выполнения JavaScript.


При этом **не нужно усложнять scraper полноценной браузерной автоматизацией**, если после загрузки страницы нужные данные уже находятся в DOM. Браузер здесь нужен прежде всего как надёжный механизм получения страницы.


Для двух тестовых товаров я бы сначала проверил именно такой минимальный pipeline:


**category page → product URLs → product pages → extraction → image download → JSON validation.**


**Уверенность: высокая.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Как самостоятельный основной подход не рекомендую из-за зафиксированного требования использовать `PlaywrightEngine`.


Кроме того, сайт явно сообщает, что JavaScript должен быть включён для полной функциональности. Professionele Koeling


Однако **BeautifulSoup-подобный HTML parsing как часть обработки уже полученного Playwright HTML** вполне уместен.


### Scrapy


Для 2 тестовых товаров это избыточно. Даже для последующего scrape всего каталога в 429 товаров сложность Scrapy не даёт очевидного преимущества перед уже предусмотренным PlaywrightEngine.


### Selenium


Не вижу причины использовать Selenium вместо уже выбранного в framework Playwright.


### Прямой API


По предоставленным материалам API не обнаружен, а в `notes.txt` прямо указано: `API нет`.


`network.har` при этом пуст, поэтому оснований проектировать API-интеграцию нет.


### GraphQL


Доказательств наличия GraphQL нет.


### Отдельная база данных


Не нужна: конечный формат — JSON, а объём на текущем этапе всего 2 товара.


**Уверенность: высокая, кроме утверждения об отсутствии скрытого API — здесь уверенность средняя, поскольку HAR пуст.**



## 5. Анализ сайта


ВозможностьВыводОснование / уверенностьJavaScript Rendering**Да / вероятно используется**Сайт сам сообщает, что JS необходим для полной функциональности; notes также указывают JS. Высокая уверенность. Professionele KoelingReact**Не обнаружен**По предоставленному HTML признаков React нет. Средняя уверенность.Vue**Не обнаружен**Признаков нет. Средняя уверенность.Angular**Не обнаружен**Признаков нет. Средняя уверенность.API**Не обнаружен**`network.har` пуст; notes: «API нет». Высокая/средняя уверенность.GraphQL**Не обнаружен**Доказательств нет. Средняя уверенность.Infinite Scroll**Нет**Есть обычная pagination. Высокая уверенность.Pagination**Да**429 товаров, 36 на странице, имеются ссылки `?p=2`, `?p=3` и т.д. Professionele KoelingLogin**Не требуется для товаров**Страницы товаров доступны без авторизации. Высокая уверенность.Cookies**Да**Предоставлен `cookies.json`, включая cookies домена сайта. Высокая уверенность.JWT**Не обнаружен**В предоставленных данных отсутствует.Bearer Token**Не обнаружен**`headers.json` пуст.CAPTCHA**Есть на форме review**На странице товара присутствует reCAPTCHA, но она относится к отправке review, а не к scraping товара. Professionele KoelingCloudflare**Да, признаки есть**В cookies присутствует `cf_clearance`. Это сильный признак Cloudflare. Высокая уверенность.Rate Limits**Не определены**Явного лимита в предоставленных данных нет. Средняя/низкая уверенность.Download Files**Да**Необходимо скачивать изображения товаров.Upload Files**Не требуется**Для задачи scraping не нужен.Lazy Loading**Не подтверждено**В предоставленном HTML карточки есть обычный `img src`; доказательств lazy loading недостаточно.WebSocket**Не обнаружен**HAR отсутствует/пуст.XHR/Fetch**Не определено**Пустой HAR не позволяет подтвердить отсутствие.Sitemap**Ссылка на sitemap есть**, но содержимое `sitemap.xml` инструментом получить не удалось.Средняя уверенность.robots.txt**Не удалось определить содержимое**Прямое получение вернуло internal error.
Особенно важно, что реальная страница категории подтверждает предоставленную структуру: 36 товаров на странице, прямые product URLs и цены `Van`/`Voor`. Professionele Koeling


Страница товара также подтверждает, что необходимые данные находятся непосредственно на product page: название, short description, наличие, обычная цена, sale price, полное описание и extra information. Professionele Koeling



## 6. Что необходимо собрать до начала разработки


**Для начала разработки критически необходимой дополнительной информации практически нет.** Предоставленного материала достаточно, чтобы начать реализацию тестового scrape.


Уже имеются:



- финальная спецификация полей;

- URL категории;

- пример category HTML;

- пример product HTML;

- pagination;

- cookies;

- информация о JS;

- правила обработки отсутствующих данных;

- требуемый JSON;

- требование скачать изображения.


Но перед **полноценным scrape всего каталога** желательно получить/проверить:



- **Эталонный JSON для 2 товаров**, если клиент может его предоставить.

- Подтверждение того, что `Price` и `Sale price` должны сохраняться именно как числовые значения, а не с валютным символом.

- Проверить на тестовых товарах, как именно клиент ожидает содержимое `Specs` и `Spec_detail`.


Последние два пункта не блокируют технический анализ, поскольку текущий `DS-PRK-Scraper.json` объявлен authoritative specification.



## 7. Возможные сложности


### 1. Cloudflare


В cookies присутствует `cf_clearance`, поэтому защита Cloudflare явно присутствует или присутствовала. Это потенциальный источник блокировок при большом количестве запросов.


### 2. JavaScript


Сайт предупреждает о необходимости JavaScript. Поэтому браузерный слой проекта оправдан. Professionele Koeling


### 3. Изображения


Нужно не просто извлечь URL, а скачать изображения. Возможны:



- несколько изображений;

- разные URL/размеры;

- недоступные изображения;

- повторяющиеся изображения.


### 4. Изменение HTML


Текущая структура выглядит достаточно стабильной и похожей на классический Magento-style сайт, но CSS-классы и DOM могут измениться.


### 5. Pagination


Сейчас видно 429 товаров, 36 на странице. Это около **12 страниц** при текущем размере страницы. Professionele Koeling


Для текущего теста pagination фактически не является проблемой, поскольку нужны только 2 товара.


### 6. Различия между category и product pages


Не все поля из спецификации находятся на карточке категории. Например, полное описание и дополнительные характеристики находятся на product page. Страница `Polar DM071` это подтверждает. Professionele Koeling


### 7. Отсутствующие значения


Нельзя автоматически подставлять значения из других полей. По инструкции отсутствующие характеристики должны оставаться пустыми.


### 8. Цены


На сайте одновременно присутствуют `Van` и `Voor`. Например, для DM071 сейчас указано €179 и €175 соответственно. Professionele Koeling


Нужно сохранять их в `Price` и `Sale price` соответственно, не смешивая два значения.


**Общий уровень риска: средний.**



## 8. Что нужно уточнить у клиента


Я бы задал клиенту только вопросы, которые действительно могут повлиять на конечный результат:



- **Какой формат должен иметь скачанный файл изображения:** оригинальный формат/расширение сохранять как есть?

- **Нужно ли сохранять локальные пути к скачанным изображениям в imageurl, или там должны оставаться URL исходного сайта?**

- Для `Specs` и `Spec_detail`: правильно ли понимать, что все характеристики должны сохраняться строго по правилам из `DS-PRK-Scraper.json`, без дополнительной нормализации значений?


При этом **не нужно спрашивать клиента про Google Sheet, оригинальный JSON или структуру колонок** — prompt прямо говорит, что `DS-PRK-Scraper.json` является финальной спецификацией.



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **HTML parser / BeautifulSoup**

- **JSON**

- **PlaywrightEngine проекта**


Без отдельного API-клиента, базы данных или Selenium.



## 10. План разработки


### Этап 1 — Проверка доступа к категории


**Цель:** убедиться, что PlaywrightEngine стабильно открывает категорию.


**Результат:** получена корректная category page с product links.


**Зависимости:** PlaywrightEngine.


### Этап 2 — Выбор 2 тестовых товаров


**Цель:** получить ровно 2 товара для первого результата.


**Результат:** две уникальные product URLs.


**Зависимости:** этап 1.


### Этап 3 — Сбор product pages


**Цель:** получить страницы выбранных товаров.


**Результат:** HTML каждого товара содержит необходимые данные.


**Зависимости:** этап 2.


### Этап 4 — Извлечение данных


**Цель:** заполнить исключительно поля из `DS-PRK-Scraper.json`.


**Результат:** у каждого товара отдельные значения для каждого поля, отсутствующие значения — пустые.


**Зависимости:** этап 3.


### Этап 5 — Обработка изображений


**Цель:** скачать изображения каждого тестового товара.


**Результат:** локально сохранённые изображения и корректные значения соответствующих image-полей.


**Зависимости:** этап 3.


### Этап 6 — Формирование JSON


**Цель:** получить конечный файл в требуемой структуре и порядке.


**Результат:** JSON с двумя товарами.


**Зависимости:** этапы 4–5.


### Этап 7 — Валидация


**Цель:** проверить результат против authoritative specification.


**Результат:** ни одного лишнего/пропущенного/переименованного поля; корректный порядок; отсутствие смешанных данных.


**Зависимости:** этап 6.


### Этап 8 — После подтверждения клиента


**Цель:** перейти от тестовых 2 товаров к полному scrape.


**Результат:** полный JSON каталога.


**Зависимости:** подтверждение тестового результата клиентом.



## 11. Оценка сложности


ПараметрОценкаСложность**4/10**Разработка тестовой версии**3–5 часов**Полная версия каталога**5–8 часов**Вероятность блокировок**средняя**Вероятность необходимости браузера**высокая**Вероятность изменения сайта**средняя**Общая оценка риска**средняя**
Почему не выше: сайт уже предоставляет прямые product URLs, стандартную пагинацию и данные в HTML. Professionele Koeling+1


Почему не ниже: присутствуют JavaScript и признаки Cloudflare, а также требуется скачивание изображений.



## 12. Можно ли решить проще


**Да.**


Самое простое решение — использовать уже предусмотренный **PlaywrightEngine**, но максимально сократить браузерную логику.


Не нужно:



- строить отдельный API layer;

- использовать Selenium;

- добавлять Scrapy;

- создавать базу данных;

- разрабатывать сложную многослойную архитектуру;

- пытаться реконструировать Google Sheet.


Более того, если после проверки выяснится, что **все требуемые поля действительно доступны в HTML product page**, не нужно выполнять дополнительные действия в браузере после загрузки страницы.


Для категории достаточно использовать существующую pagination и брать product links. Для каждого продукта — открыть product page, извлечь поля и скачать изображения.


Это соответствует принципу из prompt: использовать PlaywrightEngine, но не усложнять scraper сверх необходимого.


**Уверенность: высокая.**



## 13. Итоговая рекомендация


**Рекомендуемое решение: Python + существующий PlaywrightEngine + HTML parsing + скачивание изображений + JSON.**


Это оптимальный вариант, потому что:



- framework уже требует PlaywrightEngine;

- сайт использует JavaScript;

- API не предоставлен;

- каталог имеет обычную pagination;

- product pages содержат необходимые данные;

- объём теста — всего 2 товара;

- конечный формат — простой JSON;

- не требуется база данных или сложная архитектура.


Текущая проверка реального сайта подтверждает ключевые предположения из предоставленного проекта: категория содержит 429 товаров и пагинацию, а product page содержит цену, sale price, описание и характеристики. Professionele Koeling+1


**Код сейчас писать можно с технической точки зрения**, поскольку спецификация и необходимые входные данные уже предоставлены. Но перед переходом к **полному scrape** разумно сначала выполнить тест на 2 товара и показать клиенту JSON + скачанные изображения.


Критически важно: **не начинать реализацию до проверки точной семантики imageurl, image_name, Specs и Spec_detail на тестовом результате**, если эти значения нельзя однозначно вывести из предоставленной спецификации.


**Итоговая уверенность в анализе: высокая (≈90%).**
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