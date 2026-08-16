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

- **Утвержденная стратегия (Шаг 1):** Провёл полный анализ prompt и предоставленных артефактов. Дополнительно проверил актуальную страницу категории: сейчас сайт отдаёт 429 товаров, по 36 на страницу, с обычной пагинацией; карточки товаров содержат URL, название и цены непосредственно в HTML. Professionele Koeling


## 1. Краткое описание задачи


Клиент хочет получить **JSON-выгрузку товаров с professionele-koeling.nl** по структуре, заданной в `DS-PRK-Scraper.json`.


На первом этапе требуется собрать **только 2 товара** как тестовый результат. После проверки клиентом предполагается полноценный scrape.


Для каждого товара необходимо собрать:



- URL;

- Breadcrumb;

- Title;

- Short description;

- URL всех изображений;

- имена изображений;

- обычную цену;

- Sale price;

- полное текстовое описание;

- характеристики;

- отдельные поля характеристик согласно инструкции `Spec_detail`.


Дополнительно зафиксировано:



- отсутствующие значения оставлять пустыми;

- если скидки нет — `Sale price` пустой;

- HTML описания не сохранять, только текст;

- товары out-of-stock также включать;

- изображения **скачивать**, а не только сохранять URL;

- порядок полей должен строго соответствовать спецификации;

- Google Sheet повторно получать не нужно — JSON считается окончательной спецификацией. GitHub


**Уверенность: высокая.**



## 2. Какой конечный результат нужен


Основной результат — **JSON**.


На тестовом этапе:



- 2 товара;

- все требуемые поля;

- каждое поле/характеристика в своей колонке/структурном поле;

- отсутствующие данные — пустые;

- изображения — скачанные локально + соответствующие `imageurl`/`image_name`;

- порядок полей — строго по спецификации.


Здесь есть важный нюанс: пример `DS-PRK-Scraper.json` фактически показывает **образец записи**, а не формальную JSON Schema. При этом инструкция `Spec_detail` говорит, что текст до `:` является названием отдельного поля характеристики. Это нужно сохранить именно так, а не самостоятельно нормализовывать названия.


**Уверенность: высокая относительно требований клиента; средняя относительно механического представления Specs, поскольку формальной JSON Schema не предоставлено.**



## 3. Как лучше решить задачу


### Рекомендация: PlaywrightEngine + парсинг HTML


Использовать предоставляемый проектом **PlaywrightEngine** для навигации по сайту и получения DOM/HTML, после чего извлекать данные из уже загруженной страницы.


Причины:



- В проекте прямо зафиксировано, что `scraper.py` получает готовый `PlaywrightEngine`; поэтому переходить на `requests` как основной механизм не имеет смысла.

- В notes указано, что сайт использует JavaScript.

- Актуальная страница действительно сообщает, что для полной функциональности требуется JavaScript. Professionele Koeling

- При этом существенная часть данных товаров уже присутствует в HTML, поэтому **не требуется строить сложную browser automation-логику**.

- На странице присутствует обычная пагинация, а не infinite scroll. Сейчас сайт показывает 36 товаров на странице и 429 всего. Professionele Koeling

- Страница товара содержит необходимые элементы: breadcrumb, title, short description и price.

- Изображения можно получать из DOM и скачивать отдельно.


Оптимальная стратегия поэтому выглядит как:


**Playwright → открыть категорию → получить ссылки нужных товаров → открыть страницы товаров → извлечь поля → скачать изображения → сформировать JSON.**


Для теста ограничиться двумя товарами.


Не вижу необходимости в API-интеграции или сложном reverse engineering.



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Технически часть данных может быть получена таким способом, потому что HTML содержит данные товаров. Но в рамках данного проекта это не лучший основной вариант: проект уже предоставляет `PlaywrightEngine`, а исходные требования указывают на JS-сайт.


Можно было бы использовать requests только после подтверждения, что все необходимые страницы стабильно доступны без browser execution, но это лишняя оптимизация для текущего этапа.


**Вывод:** проще и надёжнее оставить PlaywrightEngine.


### Selenium


Не нужен.


Playwright уже предусмотрен проектом и лучше соответствует существующей инфраструктуре.


### Scrapy


Избыточен для текущей задачи из 2 товаров и не даёт преимущества, которое оправдывало бы замену существующего browser engine.


### API


По предоставленным данным API не обнаружен; `network.har` пустой, а notes прямо говорят `API нет`.


Искать и строить отдельную API-интеграцию сейчас нецелесообразно.


### GraphQL


Признаков GraphQL нет.


### Полноценная сложная browser automation


Тоже не нужна. JavaScript действительно используется, но из имеющегося HTML видно, что основные данные доступны в DOM. Поэтому браузер должен быть **транспортом/рендерером**, а не объектом сложной автоматизации.


**Уверенность: высокая.**



## 5. Анализ сайта


ВозможностьВыводУверенностьJavaScript Rendering**Да / вероятно используется**ВысокаяReactНе подтвержденоНизкаяVueНе подтвержденоНизкаяAngularНе подтвержденоНизкаяAPIПо предоставленным данным нетСредняя/высокаяGraphQLНе обнаруженСредняяInfinite Scroll**Нет**, обычная пагинацияВысокаяPagination**Да**ВысокаяLoginДля scrape не требуетсяВысокаяCookies**Да**ВысокаяJWTНе обнаруженСредняяBearer TokenНе обнаруженСредняяCAPTCHAНе подтвержденаНизкаяCloudflare**Есть признаки Cloudflare**ВысокаяRate LimitsНеизвестноНизкаяDownload Files**Да — изображения нужно скачивать**ВысокаяUpload FilesНе требуетсяВысокаяLazy LoadingНе подтвержденоНизкаяWebSocketНе подтвержденНизкаяXHR/FetchИз предоставленных файлов определить нельзяСредняяSitemapНе предоставленНизкаяrobots.txtНе предоставленНизкая
### Что подтверждается особенно хорошо


На актуальной категории сейчас:



- 429 товаров;

- 36 товаров на странице;

- есть страницы `?p=2`, `?p=3` и т. д.;

- товары имеют отдельные product URLs;

- цена и sale price находятся непосредственно в HTML. Professionele Koeling


В предоставленном `cookies.json` также имеется cookie `cf_clearance`, поэтому **Cloudflare-защиту следует считать реальным риском**, хотя из имеющихся данных нельзя утверждать, что сайт обязательно будет блокировать scraper.


### Важная проблема с checkpoint


`checkpoint.json` содержит:



- `status: completed`;

- `processed_count: 49`;

- `exported_count: 49`;


но текущая задача говорит, что сейчас требуется только **2 товара**, а `total_pages` в checkpoint указан как 1.


Это выглядит как **результат предыдущего запуска**, а не актуальное состояние тестовой задачи. Его нельзя бездумно использовать как источник истины для текущей выгрузки.



## 6. Что необходимо собрать до начала разработки


В целом **критически необходимой дополнительной информации для начала разработки сейчас нет**.


Уже предоставлены:



- описание задачи;

- окончательная спецификация полей;

- пример HTML категории;

- пример HTML товара;

- pagination HTML;

- cookies;

- headers;

- checkpoint;

- notes;

- требуемый формат;

- правила обработки отсутствующих значений;

- требование скачивать изображения.


Особенно важно, что prompt прямо запрещает повторно запрашивать Google Sheet: `DS-PRK-Scraper.json` считается окончательной спецификацией. GitHub


### Что желательно получить


Желательно только подтвердить **какие именно два товара являются тестовыми**.


Сейчас есть небольшое расхождение:



- первый товар актуальной категории — `Polar DM071`;

- пример product page в предоставленном HTML — `Polar GE579`.


На актуальной странице `Polar GE579` также присутствует, но является уже седьмым товаром в списке, а не вторым. Professionele Koeling



## 7. Возможные сложности


### 1. Cloudflare


Наличие `cf_clearance` означает риск защиты/проверок.


**Риск: средний.**


### 2. Изменение HTML


Сайт выглядит как классический e-commerce frontend, поэтому CSS-классы и DOM-структура могут измениться.


**Риск: средний.**


### 3. Изображения


Нужно не просто получить URL, а скачать файлы и корректно заполнить:



- `imageurl`;

- `image_name`.


При наличии нескольких изображений их нужно разделять запятой согласно спецификации.


**Риск: средний.**


### 4. Характеристики


Это наиболее неоднозначная часть спецификации.


`Spec_detail` говорит:



всё до `:` является header.



Значит характеристики необходимо преобразовывать в отдельные поля, **не объединяя их в одну строку**.


При этом нельзя самостоятельно переименовывать или нормализовать headers.


**Риск: средний.**


### 5. Отсутствующие характеристики


Требование уже определено: оставлять пустыми.


### 6. Цена


На сайте одновременно присутствуют `Van` и `Voor`, то есть обычная и текущая цена. Например, актуальная категория показывает для первого товара €179 и €175. Professionele Koeling


Нужно строго сопоставить:



- `Price` → обычная цена;

- `Sale price` → текущая цена;

- если sale отсутствует → пусто.


### 7. Pagination


Сейчас заявлено 429 товаров, поэтому полноценный scrape потребует прохода по нескольким страницам. Professionele Koeling


Для теста это не проблема — ограничиваемся двумя товарами.


### 8. Изменение количества товаров


Нельзя полагаться на текущее количество 429 как на постоянное.


### 9. Checkpoint


Существующий checkpoint нельзя смешивать с новым тестовым запуском без чёткого правила возобновления.



## 8. Что нужно уточнить у клиента


Я бы задал клиенту **один основной вопрос**, прежде чем начинать тест:


**Какие именно 2 товара использовать для тестового файла?**


Например:



Should the 2-product test file contain the first 2 products from the category page, or do you want two specific products?



Это важно, потому что в материалах одновременно фигурируют `Polar DM071` и `Polar GE579`, причём `GE579` используется как пример полной product page.


### Дополнительное уточнение, которое желательно подтвердить


Нужно подтвердить, что `Specs` должны быть преобразованы в **отдельные JSON-поля с названиями, полученными из текста до :**, как указано в `Spec_detail`.


Самостоятельно менять эту логику я бы не стал.


**До получения этих ответов код лучше не писать.**



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **BeautifulSoup** — для удобного разбора полученного HTML

- **JSON** для результата


Без API, Selenium, Scrapy и базы данных.



## 10. План разработки


### Этап 1 — тестовая навигация


**Цель:** убедиться, что PlaywrightEngine стабильно открывает категорию и product pages.


**Результат:** успешно полученные страницы и ссылки товаров.


**Зависимости:** существующий PlaywrightEngine.


### Этап 2 — получение двух товаров


**Цель:** выбрать согласованные клиентом два товара.


**Результат:** две product URLs.


**Зависимости:** ответ клиента о выборе двух товаров, если используются не первые два.


### Этап 3 — извлечение основных полей


**Цель:** собрать URL, breadcrumb, title, short description, prices и description.


**Результат:** заполненные базовые поля двух товаров.


**Зависимости:** корректный DOM product page.


### Этап 4 — извлечение характеристик


**Цель:** разобрать характеристики согласно `Spec_detail`.


**Результат:** отдельные поля характеристик без объединения разных значений.


**Зависимости:** подтверждение трактовки `Spec_detail`.


### Этап 5 — изображения


**Цель:** получить все изображения и скачать их.


**Результат:** локальные изображения + `imageurl` + `image_name`.


**Зависимости:** доступность image URLs.


### Этап 6 — формирование JSON


**Цель:** сформировать результат строго по `DS-PRK-Scraper.json`.


**Результат:** тестовый JSON с двумя товарами.


**Зависимости:** успешное извлечение предыдущих этапов.


### Этап 7 — валидация


**Цель:** проверить обязательные поля, порядок, пустые значения, цены, изображения и характеристики.


**Результат:** готовый тестовый файл для клиента.


**Зависимости:** готовый JSON.


### Этап 8 — расширение до полного scrape


После одобрения тестового файла:


**Цель:** пройти всю категорию/все требуемые страницы.


**Результат:** полный JSON.


**Зависимости:** approval тестовых двух товаров и подтверждение области полного scrape.



## 11. Оценка сложности


ПоказательОценкаСложность**4/10**Разработка тестовой версии**2–4 часа**Полный scraper после утверждения теста**4–8 часов**Вероятность блокировки**Средняя**Вероятность необходимости браузера**Высокая**Вероятность будущих изменений сайта**Средняя**Общий риск**Средний**
Почему не выше 4/10: структура сайта достаточно традиционная, pagination простая, product URLs присутствуют непосредственно в категориях, а основные данные находятся в HTML. Актуальная страница это подтверждает. Professionele Koeling


Основной фактор риска — не парсинг, а **Cloudflare/стабильность доступа + корректная интерпретация структуры характеристик**.



## 12. Можно ли решить проще


**Да.**


Самый простой вариант — использовать существующий **PlaywrightEngine только для навигации и получения страниц**, а не строить сложную автоматизацию.


В частности:



- Не искать API — предоставленные материалы не показывают его.

- Не использовать базу данных — конечный результат JSON.

- Не использовать Scrapy — для такого объёма он избыточен.

- Не использовать Selenium — Playwright уже встроен в проект.

- Не делать сложное взаимодействие с UI — ссылки товаров и pagination доступны непосредственно в HTML.

- Не переходить на все товары на первом этапе — сначала только 2.

- Не использовать отдельный механизм для JS, кроме уже предоставленного PlaywrightEngine.


Более того, актуальный HTML категории показывает, что product URLs и цены доступны прямо в странице, поэтому для **тестовых двух товаров** нет необходимости строить полноценный crawler. Professionele Koeling


Для полного scrape впоследствии достаточно расширить обход pagination.



## 13. Итоговая рекомендация


**Рекомендуемое решение: Python + существующий PlaywrightEngine + HTML parsing + JSON.**


Это оптимальный вариант, потому что:



- он соответствует уже существующей инфраструктуре проекта;

- JavaScript сайта учитывается;

- API не нужен;

- pagination простая;

- данные товара доступны в DOM;

- результат должен быть JSON;

- объём теста всего 2 товара;

- нет необходимости усложнять scraper архитектурой.


**Перед написанием кода необходимо получить только подтверждение двух моментов:**



- какие именно два товара являются тестовыми — первые два или конкретные товары;

- подтвердить трактовку `Spec_detail`: каждый текст до `:` становится отдельным полем.


После этого **можно переходить к реализации**. До ответа клиента на эти вопросы лучше не писать код, поскольку иначе есть риск корректно реализовать техническую часть, но получить неправильный тестовый output.


**Уровень уверенности в общей стратегии: высокий (~90%).**
**Уровень уверенности в деталях структуры Specs/Spec_detail: средний (~75%), пока клиент явно не подтвердит трактовку.**


Источник задания: полный предоставленный prompt и его артефакты. GitHub
Актуальная проверка сайта: категория содержит 429 товаров, 36 на страницу и стандартную пагинацию. Professionele Koeling
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