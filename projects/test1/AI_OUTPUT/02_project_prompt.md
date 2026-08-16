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


Клиент хочет получить структурированные данные о товарах с сайта Professionele-Koeling.nl в формате JSON.


На первом этапе требуется **собрать только 2 товара и отправить тестовый JSON**, после проверки которого можно выполнять полный сбор. Для каждого товара необходимо сохранить все поля строго в соответствии с `DS-PRK-Scraper.json`: URL, breadcrumb, название, short description, изображения и их имена, цены, полное описание, а также характеристики из блока `Specs`/`Spec_detail`. Каждое поле должно находиться в собственной колонке/ключе, без смешивания данных. GitHub


Важные правила клиента уже определены:



- отсутствующие характеристики оставлять пустыми;

- если скидочной цены нет — `Sale price` оставлять пустым;

- HTML из описания не сохранять, только текст;

- товары без наличия также включать;

- изображения **скачивать**, а не только сохранять URL;

- порядок полей сохранять строго по спецификации;

- `DS-PRK-Scraper.json` считать окончательной спецификацией и не менять её. GitHub


**Уверенность: высокая.**



## 2. Какой конечный результат нужен


Основной результат — **JSON**.


Для каждого товара нужен объект со строго заданным набором полей:



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


Изображения также должны быть скачаны локально.


Есть один важный момент, который пока **не определён однозначно**: должна ли итоговая JSON-структура быть массивом объектов, например `[{...}, {...}]`, либо другой формой контейнера. В предоставленной спецификации показан объект одного товара, но формат корневого JSON явно не описан. Это желательно уточнить до реализации.



## 3. Как лучше решить задачу


### Рекомендация: PlaywrightEngine + HTML parsing


Оптимальный вариант — использовать уже предусмотренный проектом **PlaywrightEngine** для загрузки страниц, а полученный HTML разбирать обычным HTML-парсером.


Логика на концептуальном уровне:


**категория → ссылки товаров → страницы товаров → извлечение полей → скачивание изображений → JSON**


Почему именно так:



- проект уже использует `PlaywrightEngine` для `scraper.py`, поэтому менять базовый механизм загрузки на `requests` не имеет смысла;

- предоставленные материалы прямо указывают, что сайт работает с JS;

- Playwright надёжнее обычного HTTP-клиента при возможном JS-rendering/Cloudflare;

- HTML уже содержит достаточно понятную структуру товара;

- карточки категории содержат ссылки на product pages;

- на странице товара находятся title, breadcrumb, short description и цены;

- изображения доступны через обычные `<img src=...>` URL;

- для характеристики `Spec_detail` формат определяется правилом клиента: **всё до : является названием характеристики**. GitHub


При этом не следует строить сложную browser automation-архитектуру. Браузер здесь нужен прежде всего как надёжный способ получить конечный HTML.


Текущий публичный сайт также показывает классическую структуру каталога: категория содержит пагинацию и товарные карточки с названиями и ценами. Например, актуальная страница `Koelkasten&Kisten` показывает 429 товаров и пагинацию. Professionele Koeling


**Уверенность: высокая.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Технически HTML можно было бы получать напрямую, но по имеющимся данным сайт использует JS, а в проекте уже зафиксирован `PlaywrightEngine`.


Поэтому `requests` как основной downloader добавляет риск получить не тот HTML, который видит браузер.


**Вердикт: не рекомендую как основной механизм.**


### Selenium


Может решить задачу, но здесь нет преимущества перед уже используемым Playwright.


**Вердикт: избыточная замена существующего решения.**


### Scrapy


Для большого crawler-проекта Scrapy был бы разумным, но здесь задача относительно простая: категория → товары → product pages → JSON.


Использование Scrapy добавило бы инфраструктурную сложность без очевидной выгоды.


**Вердикт: избыточно.**


### API


В предоставленных материалах указано: `API нет`, а `network.har` пустой. Никакого подтверждённого API/GraphQL endpoint нет. GitHub


**Вердикт: API сейчас использовать не из чего.**


### Только парсинг категории


Это потенциально более простой вариант, но **только если все требуемые поля присутствуют в карточках категории**.


Сейчас это не так: например, category HTML содержит название, URL, изображение и цены, тогда как `Short description`, `Description`, `Specs` и другие данные находятся на product page. Предоставленный `product-page.html` это подтверждает. GitHub


**Вердикт: для полного набора данных нужны страницы товаров.**



## 5. Анализ сайта


КомпонентОценкаОснованиеJavaScript Rendering**Вероятно да**указано в `notes.txt`; Playwright зафиксирован проектомReact**Не обнаружен**в предоставленном HTML нет признаков ReactVue**Не обнаружен**доказательств нетAngular**Не обнаружен**доказательств нетAPI**Не обнаружен**`notes.txt`: API нет; HAR пустGraphQL**Не обнаружен**доказательств нетInfinite Scroll**Нет признаков**присутствует обычная paginationPagination**Да**`?p=2`, `?p=3` и т.д.Login**Есть, но для публичного каталога не требуется**сайт содержит customer loginCookies**Да**предоставлен `cookies.json`JWT**Не обнаружен**нет соответствующих данныхBearer Token**Не обнаружен**`headers.json` пустCAPTCHA**Не подтверждена напрямую**явных CAPTCHA-элементов нетCloudflare**Вероятно да**в cookies присутствует `cf_clearance`Rate Limits**Неизвестно**данных недостаточноDownload Files**Да**необходимо скачать изображенияUpload Files**Не требуется / не обнаружен**задача только на scrapingLazy Loading**Неизвестно**предоставленного материала недостаточноWebSocket**Неизвестно**HAR пустXHR/Fetch**Неизвестно**HAR пустSitemap**Не подтверждено**ссылки на sitemap есть в footer, но содержимое sitemap не полученоServer-side HTML**Да, по крайней мере значительная часть**поисковая индексация показывает полноценные HTML-страницы
На актуальной странице категории поисковый индекс получает названия, цены и товарные карточки напрямую из HTML; это дополнительно снижает вероятность необходимости сложного browser interaction. Professionele Koeling+1


Также на сайте присутствует обычная система аккаунтов, но для просмотра каталога авторизация не нужна. Professionele Koeling


**Уверенность:** высокая для pagination/cookies/public catalog; средняя для Cloudflare; низкая для React/Vue/Angular/WebSocket/XHR/lazy loading, поскольку доступного HAR недостаточно.



## 6. Что необходимо собрать до начала разработки


Большая часть необходимой информации **уже предоставлена**, поэтому повторно запрашивать Google Sheet не нужно.


Уже имеются:



- окончательная спецификация `DS-PRK-Scraper.json`;

- пример category HTML;

- пример product HTML;

- pagination;

- cookies;

- headers;

- HAR;

- checkpoint;

- требования к отсутствующим данным;

- требования к изображениям;

- требования к JSON;

- информация о том, что нужно сначала обработать 2 товара. GitHub


### Что всё-таки желательно уточнить



- **Какой должен быть root JSON:** массив товаров или другая структура.

- Что именно должно записываться в `image_name`: имя скачанного файла (`polar_ge579.jpg`), исходное имя файла из URL или другое значение.

- Какой именно объём считать production scope после теста: только категория `Koelkasten&Kisten` или весь сайт.


Последний вопрос особенно важен: предоставленный URL указывает на категорию, а актуальная версия категории содержит **429 товаров**, поэтому "весь сайт" и "вся указанная категория" — существенно разные объёмы. Professionele Koeling



## 7. Возможные сложности


### 1. Cloudflare / блокировки


Наличие `cf_clearance` в предоставленных cookies говорит о том, что Cloudflare присутствует или присутствовал в цепочке доступа.


Это может привести к:



- challenge;

- временной блокировке;

- необходимости использовать browser context;

- нестабильности при слишком высокой скорости запросов.


### 2. Изменение HTML


Селекторы должны опираться на устойчивые признаки структуры страницы, а не на случайные autogenerated IDs.


Например, `old-price`, `special-price`, `product-name`, `short-description` выглядят существенно более подходящими для извлечения, чем конкретные ID вроде `product-price-2526`.


### 3. Несовпадение категории и product pages


Товарные данные распределены между страницами: category page даёт базовую информацию, а product page — подробное описание и характеристики. GitHub


### 4. Изображения


У товара может быть несколько изображений. Спецификация прямо говорит разделять несколько URL и имён через запятую.


Также нужно отдельно учитывать ошибки скачивания изображений.


### 5. Неструктурированные характеристики


`Description` содержит обычный текст, внутри которого есть блоки вроде:


`Artikelnummer: GE579`
`Inhoud: 29 liter`
`Afmetingen BxDxH: 400 x 430 x 530 mm`


Для `Spec_detail` необходимо придерживаться предоставленного правила, а не самостоятельно придумывать нормализацию названий. GitHub


### 6. Отсутствующие значения


Нельзя автоматически подставлять:



- `0`;

- `N/A`;

- цену вместо Sale price;

- значения из другого товара.


По требованиям клиента отсутствующие данные должны оставаться пустыми. GitHub


### 7. Текущая доступность сайта


При моей дополнительной проверке прямой запрос к category URL через web-инструмент завершился timeout, хотя поисковая индексация сайта доступна. Поэтому устойчивость прямого доступа необходимо проверить непосредственно через предоставленный PlaywrightEngine перед массовым запуском.



## 8. Что нужно уточнить у клиента


Я бы задал клиенту **три коротких вопроса**:



- **Для JSON:** подтвердите, пожалуйста, что итоговый файл должен иметь root-структуру массива товаров (`[{...}, {...}]`)?

- **Для image_name:** правильно ли сохранять имя скачанного изображения как имя исходного файла из URL?

- После тестовых 2 товаров полный scrape должен охватывать **все 429 товаров категории Koelkasten&Kisten**, или другой объём?


Других блокирующих вопросов на текущем этапе нет.



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **BeautifulSoup**

- **JSON**


Дополнительный crawler framework или API-слой не нужен.



## 10. План разработки


### Этап 1 — Проверка доступа


**Цель:** убедиться, что PlaywrightEngine стабильно открывает category и product pages.


**Результат:** подтверждённый рабочий доступ к сайту.


**Зависимости:** текущий PlaywrightEngine проекта.


### Этап 2 — Получение двух товаров


**Цель:** взять 2 товара из заданной категории и получить их product URLs.


**Результат:** две корректные страницы товаров.


**Зависимости:** успешный этап 1.


### Этап 3 — Извлечение данных


**Цель:** получить все поля из `DS-PRK-Scraper.json`.


**Результат:** два полностью заполненных объекта, при этом отсутствующие значения остаются пустыми.


**Зависимости:** HTML product pages.


### Этап 4 — Изображения


**Цель:** скачать все изображения двух товаров и связать их с `imageurl`/`image_name`.


**Результат:** изображения физически сохранены.


**Зависимости:** доступность image URLs.


### Этап 5 — Тестовый JSON


**Цель:** сформировать JSON только для 2 товаров в точном порядке полей.


**Результат:** тестовый файл для клиента.


**Зависимости:** этапы 3–4 и уточнение root JSON.


### Этап 6 — Проверка результата


**Цель:** сравнить каждый ключ с `DS-PRK-Scraper.json` и проверить отсутствие смешивания данных.


**Результат:** готовый тестовый deliverable.


**Зависимости:** тестовый JSON.


### Этап 7 — Полный scrape


**Цель:** после одобрения теста обработать согласованный объём товаров.


**Результат:** полный JSON + скачанные изображения.


**Зависимости:** подтверждение клиента и определение полного scope.



## 11. Оценка сложности


ПоказательОценкаСложность**4/10**Разработка тестовой версии**2–4 часа**Полный scrape после утверждения подхода**4–8 часов**Вероятность блокировок**Средняя, ~30%**Вероятность необходимости браузера**Высокая, ~80%**Вероятность изменения сайта в будущем**Средняя**Общий риск**Средний**
Оценка времени предполагает, что предоставленный PlaywrightEngine уже работает и не требует ремонта инфраструктуры.


Сам scraping не выглядит сложным: текущая категория имеет обычную pagination, а product pages имеют достаточно предсказуемую HTML-структуру. GitHub+1


Главный риск — не parsing, а **стабильность доступа к сайту/Cloudflare и корректность скачивания изображений**.


**Уверенность в оценке: средняя**, поскольку прямой live fetch сайта сейчас дал timeout.



## 12. Можно ли решить проще


**Да.**


Самое простое решение — не строить полноценный универсальный crawler.


Достаточно:


**PlaywrightEngine → category page → pagination → product URLs → product pages → parsing → images → JSON**


Не нужны:



- API;

- база данных;

- Scrapy;

- Selenium;

- отдельный backend;

- сложная очередь задач;

- GraphQL;

- отдельная система авторизации.


Особенно важно не пытаться извлекать всё только из category page: там отсутствуют значительная часть требуемых данных, например подробное описание и характеристики. Product page уже содержит эти данные. GitHub


При этом даже для полного сбора можно оставить решение линейным и простым: обрабатывать товары последовательно с контролируемой скоростью, а не строить сложную распределённую систему.



## 13. Итоговая рекомендация


**Рекомендуемое решение:** использовать существующий **PlaywrightEngine + BeautifulSoup/HTML parsing + JSON**, переходя с категории на страницы товаров и отдельно скачивая изображения.


Это оптимально потому что:



- Playwright уже является обязательной частью scraper-проекта;

- сайт имеет pagination;

- category page позволяет получить ссылки на товары;

- product pages содержат необходимые подробные данные;

- подтверждённого API нет;

- Scrapy/Selenium/API добавили бы ненужную сложность;

- объём задачи умеренный;

- структура HTML достаточно предсказуема. GitHub+1


**Перед началом разработки нужно уточнить только три вещи:** root-структуру JSON, правило формирования `image_name` и точный production scope после тестовых двух товаров.


### Можно ли уже писать код?


**Почти, но формально лучше сначала получить ответы на эти 3 вопроса.**


При этом **код сейчас писать не следует**, поскольку это прямо запрещено текущим этапом задания. После уточнений можно переходить к реализации.


**Итоговая уверенность: высокая.** Архитектурно задача понятна; неопределённости остались только вокруг нескольких деталей выходного формата и полного scope.
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