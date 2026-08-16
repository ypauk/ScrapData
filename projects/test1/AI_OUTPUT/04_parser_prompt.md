# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/parser.py`.

**КРИТИЧЕСКИ ВАЖНО — ФОРМАТ ОТВЕТА:**
Ответь ТОЛЬКО одним блоком кода Python. Формат ответа строго:

```python
# весь код файла здесь
```

НЕ пиши пояснений, вопросов, анализов или текста ДО или ПОСЛЕ блока кода. Весь контекст уже предоставлен ниже — сразу пиши код. Если какие-то детали неясны — принимай разумное решение самостоятельно.

Не меняй другие файлы. Не создавай новые папки.

---

# ПРАВИЛА

ПРАВИЛА РАЗРАБОТКИ

1. Всегда использовать starter-project.

2. Не менять структуру каталогов.

3. Не создавать новые папки без необходимости.

4. Не писать код, который не требуется клиентом.

5. Предпочитать простое решение сложному.

6. scraper.py ВСЕГДА использует PlaywrightEngine (передаётся из main.py). НЕ использовать requests/httpx в scraper.py.

7. parser.py использует BeautifulSoup для парсинга HTML. НЕ делает сетевых запросов.

8. Если данные доступны через API — можно использовать engine.page.evaluate() для перехвата XHR/fetch внутри Playwright, но НЕ добавлять requests.

9. Код должен быть модульным.

10. Docker создавать только после успешного локального запуска.

---

# КОНТЕКСТ ПРОЕКТА

## Анализ (этап 1)

Провёл полный анализ prompt и предоставленных артефактов. Дополнительно проверил актуальную страницу категории: сейчас сайт отдаёт 429 товаров, по 36 на страницу, с обычной пагинацией; карточки товаров содержат URL, название и цены непосредственно в HTML. Professionele Koeling


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



... (обрезано, analysis, всего 14999 символов) ...

> **ВАЖНО:** Анализ выше мог содержать фразы вроде «переходить к написанию кода пока рано» или «нужно дождаться ответов клиента». Эти фразы относятся к моменту составления анализа и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — код писать нужно. Все данные уже предоставлены ниже.

---

## План проекта (этап 2)

# Проектирование реализации scraper для professionele-koeling.nl

## 0. Выбранный подход

**Технология:** существующий `PlaywrightEngine` + HTML + BeautifulSoup + JSON.

API не используется: в предоставленных материалах API отсутствует, `network.har` пуст, а `notes.txt` прямо указывает, что API нет. Playwright обязателен архитектурой существующего framework: `scrape_data(engine)` получает уже готовый `PlaywrightEngine` с browser context, cookies, proxy и user-agent.

Для теста нужны страницы первых двух товаров из категории.

**ПРЕДПОЛОЖЕНИЕ:** под «2 товара» понимаются первые два товарных элемента, найденные в категории. В prompt явно не указаны два конкретных SKU. Если клиент имеет в виду конкретные товары, это единственное требующее подтверждения место.

Почему не `requests`/`httpx`:

- framework запрещает менять способ получения данных;
- сайт обозначен как JS-based;
- уже существует `PlaywrightEngine`;
- использование другого HTTP-клиента нарушило бы контракт `scrape_data(engine)`;
- отдельный Selenium/Scrapy/API-слой не даёт преимуществ для текущего теста.
### Плюсы

- соответствует существующей архитектуре;
- JavaScript учитывается;
- cookies/Cloudflare context уже находится на стороне browser engine;
- можно получать полностью отрендеренный HTML;
- для теста достаточно минимального количества навигаций;
- не требуется новая инфраструктура.
### Минусы

- Playwright тяжелее обычного HTTP-клиента;
- Cloudflare может потребовать остановки или ручного вмешательства;
- изменение DOM может потребовать обновления селекторов;
- фактическая структура блока характеристик не предоставлена полностью.
# 1. Полный поток данных

```
https://www.professionele-koeling.nl/koelkasten-kisten.html
        ↓
PlaywrightEngine
        ↓
HTML категории
        ↓
извлечение URL первых 2 товаров
        ↓
PlaywrightEngine → product page #1
        ↓
HTML товара #1
        ↓
PlaywrightEngine → product page #2
        ↓
HTML товара #2
        ↓
scrape_data(engine) → List[str]
        ↓
main.py
        ↓
parse_html_data(raw_pages_content)
        ↓
BeautifulSoup
        ↓
dict для каждого товара
        ↓
list[dict]
        ↓
exporter.py
        ↓
JSON
```

Для тестового режима scraper не должен обходить все 429 товаров. Категория содержит пагинацию `?p=2`, `?p=3` и т. д., но для теста достаточно первой страницы и первых двух product URLs.

Для будущего full scrape поток расширяется:

```
category page 1
    ↓
product URLs
    ↓
product pages
    ↓
next category page (?p=2)
    ↓
product URLs
    ↓
...
    ↓
последняя страница
```

Экспортер, `main.py`, `browser.py`, `config.py` и `utils.py` изменять не требуется.

# 2. Проектирование app/scraper.py

## 2.1. Интерфейс функций

### scrape_data(engine) → List[str]

**Назначение:** главная функция, вызываемая `main.py`.

**Вход:**

- `engine` — готовый `PlaywrightEngine`.
**Возвращает:**

- `List[str]`, где каждый элемент — HTML страницы товара.
**Ответственность:**

- открыть категорию;
- дождаться загрузки списка товаров;
- получить HTML категории;
- определить URL товаров;
- ограничить список двумя товарами в тестовом режиме;
- открыть каждую product page;
- получить HTML;
- вернуть список HTML.
`parser.py` внутри этой функции не вызывается.

### _fetch_listing_html(engine, url) → str

**Назначение:** открыть страницу категории и получить её HTML.

**Вход:**

- `engine`;
- URL категории.
**Возвращает:**

- HTML категории.
**Ожидаемая точка ожидания:**

```
ul.products-grid
```

В предоставленном HTML товарные карточки находятся внутри `ul.products-grid`, а сама карточка — `li.item`.

**Алгоритм:**

- `engine` открывает URL;
- ждёт появления контейнера товарного списка;
- после успешной загрузки получает HTML текущей страницы;
- возвращает HTML вызывающему коду.
Если engine/framework предоставляет собственный метод ожидания загрузки страницы, использовать его, а не создавать дополнительный механизм ожидания.

### _extract_product_urls(html) → List[str]

**Назначение:** получить URL товаров из HTML категории.

Это допустимо в `scraper.py`, потому что здесь выполняется **навигационное извлечение URL**, а не извлечение бизнес-полей товара. Именно такой подход предусмотрен контрактом framework.

**Известный селектор:**

```известный селектор:
li.item a.product-image[href]
```

В предоставленном HTML:

```
li.item
  → div.product-image-wrapper
  → a.product-image
  → href
```

Дополнительный подтверждённый URL находится также в:

```
li.item h2.product-name a[href]
```

Предпочтительно брать `a.product-image[href]`, а при отсутствии — `h2.product-name a[href]`.

**Алгоритм:**

```алгоритм:
найти все li.item
    ↓
для каждой карточки найти a.product-image[href]
    ↓
если URL найден — добавить в список
    ↓
удалить дубликаты, сохранив исходный порядок
    ↓
вернуть список
```

Для теста:

```для теста:
product_urls = первые 2 уникальных URL
```

### _fetch_product_html(engine, url) → str

**Назначение:** открыть страницу конкретного товара и получить HTML.

**Вход:**

- `engine`;
- URL товара.
**Возвращает:**

- HTML product page.
**Ожидаемый селектор готовности:**

```
div.product-name h1
```

Он подтверждён предоставленным product HTML.

**Дополнительная проверка загрузки:**

```
div.breadcrumbs
```

или

```или
div.price-box
```

Если основной элемент не найден, использовать timeout/error handling, а не считать страницу успешно загруженной.

### _get_next_page_url(html, current_url) → str | None

Для **тестовой реализации** функция фактически не нужна, поскольку обрабатываются только два товара первой страницы.

Для будущего full scrape её следует предусмотреть.

**Подтверждённый селектор:**

```
div.pager div.pages a.next[href]
```

В HTML ссылка `next` ведёт на:

```
...?p=2
```

Также подтверждены ссылки на `?p=2`, `?p=3`, `?p=4`, `?p=5`.

**Алгоритм:**

```алгоритм:
найти div.pager div.pages a.next
    ↓
получить href
    ↓
если href отсутствует → None
иначе → абсолютный URL следующей страницы
```

Останавливать обход также следует при:

- отсутствии `a.next`;
- отсутствии товарных карточек;
- повторении уже посещённого URL.
### _download_product_images(engine, image_urls, product_index)

**Назначение:** физически скачать изображения, поскольку клиент требует не только URL.

Это сетевой аспект и поэтому находится в `scraper.py`, а не `parser.py`.

**Важно:** эта функция является вспомогательной операцией scraper и не меняет обязательный контракт:

```
scrape_data(engine) → List[str]
```

Скачивание выполняется как side effect, а HTML продолжает возвращаться через установленный framework-контракт.

**ПРЕДПОЛОЖЕНИЕ:** точный каталог для сохранения изображений должен браться из уже существующего `config.py`, а не задаваться новым абсолютным путём в `scraper.py`.

**Имена файлов:** использовать исходное имя файла из URL изображения, если оно уникально. При конфликте имён необходим детерминированный suffix, например по индексу товара.

Не следует создавать новый конфигурационный параметр, если существующий `config.py` уже предоставляет подходящий output directory.

## 2.2. Алгоритм обхода

### Тестовый режим

```тестовый режим
scrape_data(engine)
    ↓
открыть category URL
    ↓
дождаться ul.products-grid
    ↓
получить HTML категории
    ↓
извлечь product URLs
    ↓
взять первые 2 URL
    ↓
для каждого URL:
    ↓
    random_delay()
    ↓
    открыть product page
    ↓
    дождаться div.product-name h1
    ↓
    получить HTML
    ↓
    вернуть HTML
    ↓
List[str]
```

`random_delay()` следует использовать между последовательными навигациями, поскольку `utils.py` уже предоставляет эту функцию. Не нужно создавать собственную реализацию задержек. Наличие Cloudflare делает умеренное последовательное обращение предпочтительнее агрессивного параллельного обхода.

### Пагинация

Для теста:

```для теста:
НЕ переходить на ?p=2
```

Для full scrape:

```для full scrape:
current_url = category_url

while current_url:
    listing_html = fetch(current_url)
    product_urls = extract_product_urls(listing_html)


... (обрезано, project_plan, всего 24701 символов) ...

> **ВАЖНО:** План выше мог содержать фразы вроде «код сейчас писать не следует» или «необходимо закрыть блокирующие контракты». Эти фразы относятся к моменту составления плана и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — ПИШИ КОД. Принимай разумные решения по неопределённым моментам (формат Specs, скачивание изображений и т.д.) самостоятельно.

---

## Данные клиента



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


--- ФАЙЛ: category-page.html ---

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

... (обрезано, ai_input, всего 16234 символов) ...

---

# ЯДРО ПРОЕКТА (НЕ МЕНЯТЬ)

Следующие файлы уже написаны и протестированы. Используй их интерфейсы, не дублируй логику:



--- app/config.py (ключевые переменные) ---
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
COOKIES_FILE = AI_INPUT_DIR / "cookies.json"
HEADERS_FILE = AI_INPUT_DIR / "headers.json"
IMAGE_DIR = OUTPUT_DIR / "images"
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
HEADLESS = _get_bool("HEADLESS", "1") or IS_DOCKER
TIMEOUT = _get_int("SCRAPER_TIMEOUT", 30)  # в секундах
BASE_URL: str = os.getenv("BASE_URL", "")

--- app/playwright_engine.py (публичные методы) ---
class PlaywrightEngineError(Exception):
class PlaywrightEngine:
    def start(self) -> "PlaywrightEngine":
    def close(self) -> None:
    def context(self) -> BrowserContext:
    def page(self) -> Page:
    def new_page(self) -> Page:
    def goto(
    def wait_for_load(self, state: str = "load", timeout: Optional[float] = None) -> None:
    def wait_for_selector(
    def content(self) -> str:
    def evaluate(self, script: str, *args: Any) -> Any:
    def update_cookies(self) -> List[dict]:
    def save_cookies(self) -> None:

---

# ТЕКУЩИЙ ШАБЛОН МОДУЛЯ

Файл `app/parser.py` — перепиши его полностью под план проекта:



---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/parser.py` (модуль: **parser**).

---

## КОНТРАКТ main.py (НЕИЗМЕНЯЕМЫЙ, ВЫСШИЙ ПРИОРИТЕТ)

`main.py` уже написан, протестирован и НЕ ПОДЛЕЖИТ изменению. Он импортирует и вызывает:

```python
from app.scraper import scrape_data
from app.parser import parse_listing, parse_html_data

# main.py делает:
with PlaywrightEngine() as engine:
    raw_pages_content = scrape_data(engine)  # List[str]

# Затем:
page_records = parse_listing(html)         # один HTML → List[Dict]
scraped_results = parse_html_data(raw_pages_content)  # List[str] → List[Dict]
```

### Обязательные сигнатуры

**scraper.py:**
```python
def scrape_data(engine: PlaywrightEngine) -> List[str]:
    """
    Принимает ЗАПУЩЕННЫЙ PlaywrightEngine (браузер уже открыт, cookies/proxy применены).
    Выполняет навигацию, пагинацию, сбор HTML.
    Возвращает список HTML-строк (одна строка = одна страница категории ИЛИ товара).
    """
```

**parser.py:**
```python
def parse_listing(html: str) -> List[Dict[str, Any]]:
    """Парсит HTML одной страницы. Возвращает список записей (dict на каждый товар)."""

def parse_html_data(raw_contents: List[str]) -> List[Dict[str, Any]]:
    """Парсит список HTML-страниц. Вызывает parse_listing() для каждой. Возвращает объединённый список."""
```

### Критические правила

- **ИГНОРИРУЙ** рекомендации из analysis/plan по выбору HTTP-движка (requests, httpx и т.д.). Движок ВСЕГДА `PlaywrightEngine` — он передаётся в `scrape_data()` уже готовым.
- **НЕ ДОБАВЛЯЙ** `import requests` в scraper.py.
- Для навигации используй: `engine.goto(url)`, `engine.content()`, `engine.wait_for_selector(...)`, `engine.page`.
- Задержки между страницами выполняются АВТОМАТИЧЕСКИ внутри `engine.goto()` (через Delay Manager).
- parser.py МОЖЕТ использовать BeautifulSoup — это для парсинга HTML, не для сбора.
- Plan/analysis описывают ЛОГИКУ (селекторы, пагинация, поля) — используй её. Но выбор движка НЕ из плана.

---

## Требования

1. **Только функции** — без классов.
2. **Один файл** — весь код модуля в одном ответе.
3. **Сигнатуры строго из контракта выше** — они неизменяемы.
4. **Логику бери из plan** — какие селекторы, какая пагинация, какие поля, как обходить.
5. **Минимум зависимостей** — используй только то, что уже есть в проекте.
6. **Обработка ошибок** — try/except на уровне страниц/элементов, не падай на одной ошибке.
7. **Логирование** — `print(f"[{__file__}] ...")` как в шаблоне.

## Если модуль = scraper

- Принимает `engine: PlaywrightEngine` (уже запущен, cookies/proxy подключены).
- Использует `engine.goto(url)` для навигации.
- Использует `engine.content()` для получения HTML после загрузки.
- Использует `engine.wait_for_selector(css)` для ожидания элементов.
- Использует `engine.page` для JS (eval, click, scroll).
- Отвечает **только** за навигацию, пагинацию, скролл, клики.
- Возвращает `List[str]` — список сырого HTML.
- НЕ парсит DOM — это задача parser.py.
- Используй `app.config.BASE_URL` как стартовый URL.

## Если модуль = parser

- Отвечает **только** за извлечение данных из сырого HTML.
- ОБЯЗАТЕЛЬНО экспортирует ОБЕ функции: `parse_listing(html)` и `parse_html_data(raw_contents)`.
- `parse_html_data` = вызывает `parse_listing` для каждого HTML и объединяет результаты.
- Используй BeautifulSoup для парсинга.
- Поля результата — строго по DS-PRK-Scraper.json из AI_INPUT.

### Какой HTML получает parse_listing()

Это зависит от того, что возвращает scraper (смотри план проекта):

- **Если scraper возвращает HTML листинговых страниц** — `parse_listing(html)` парсит страницу категории и извлекает карточки товаров.
- **Если scraper возвращает HTML страниц товаров** — `parse_listing(html)` парсит страницу отдельного товара и возвращает один `[dict]` (список из одного элемента).
- **Если scraper возвращает оба типа** — используй признак в HTML (наличие `<ul class="products-grid">` vs `<div class="product-view">`) для выбора стратегии парсинга.

Убедись, что логика `parse_listing()` соответствует тому, какой именно HTML передаст scraper из плана проекта.

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
- Использовать `requests`/`httpx` в scraper.py.
- Менять сигнатуры из контракта.
- Использовать классы.
- Запрашивать дополнительные файлы (project_plan.md и т.п.) — всё нужное УЖЕ в этом промпте.
