# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/scraper.py`.

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

Ниже — полный анализ по инструкции из prompt. Я также проверил сайт и несколько реальных страниц, чтобы отделить то, что подтверждено предоставленными файлами, от того, что можно подтвердить непосредственно сейчас. GitHub+2Professionele Koeling+2


## 1. Краткое описание задачи


Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает информацию о товарах из категории холодильного оборудования.


На первом этапе нужен **тестовый JSON только с 2 товарами**. После проверки теста предполагается полный scrape сайта/целевой категории.


Для каждого товара необходимо сохранить строго заданный набор полей из `DS-PRK-Scraper.json`:



- URL

- Breadcrumb

- Title

- Short description

- imageurl

- image_name

- Price

- Sale price

- Description

- Specs

- Spec_detail


Причём **каждое поле должно оставаться отдельным полем**, без объединения разных характеристик в одну колонку/структуру вопреки спецификации.


Изображения необходимо не только найти, но и **скачать**.


Дополнительно зафиксированы правила:



- если скидки нет — `Sale price` оставлять пустым;

- отсутствующие характеристики оставлять пустыми;

- Description сохранять как чистый текст, без HTML;

- товары без наличия также включать;

- порядок полей сохранять строго по спецификации;

- пока собрать только 2 товара.


Уверенность: **высокая**, поскольку эти требования прямо присутствуют в исходном prompt.



## 2. Какой конечный результат нужен


Основной результат — **JSON**.


На первом этапе:


**JSON с 2 товарами + скачанные изображения.**


Формат полей должен соответствовать `DS-PRK-Scraper.json` без самостоятельного изменения названий, порядка или семантики.


Важный момент: в предоставленной спецификации есть инструкции внутри значений:



- `imageurl`: `"if multipli seperated by comma"`

- `image_name`: `"if multiple seperated by comma"`

- `Specs`: `"each own colom"`

- `Spec_detail`: `"evertything before the : is the header"`


Это не повреждённые данные, а инструкции по заполнению, как отдельно указано в prompt. Поэтому их нельзя трактовать как обычные значения товара. GitHub


Уверенность: **высокая**.



## 3. Как лучше решить задачу


### Рекомендуемый подход: PlaywrightEngine + HTML parsing


Поскольку в `main.py` зафиксировано использование `PlaywrightEngine`, а prompt прямо запрещает заменять его рекомендацией `requests`, оптимальный вариант — использовать уже предоставленный браузерный engine и извлекать данные из HTML.


Логика подхода на уровне стратегии:



- Открыть категорию через PlaywrightEngine.

- Получить список товарных карточек.

- Извлечь URL товаров.

- Перейти на страницы товаров.

- Извлечь необходимые поля.

- Отдельно собрать все изображения товара.

- Скачать изображения.

- Нормализовать текст и характеристики.

- Оставить отсутствующие значения пустыми.

- Сформировать JSON строго по спецификации.


Это наиболее надёжный вариант, потому что в предоставленных материалах прямо указано:



`API нет , и сайт на JS`



При этом реальная страница сейчас действительно сообщает, что JavaScript необходим для полной функциональности сайта. Одновременно сервер отдаёт достаточно HTML-контента, включая товарные карточки и ссылки. Professionele Koeling


На странице категории сейчас видны непосредственно URL товаров, названия и цены, например Polar DM071 и Polar GE579. Professionele Koeling


На странице товара дополнительно доступны описание, наличие, цены, характеристики и другие данные. Например, страница Polar DM071 содержит отдельные блоки `Productbeschrijving`, `Details` и `Extra informatie`. Professionele Koeling


### Нужно ли заходить на страницы товаров?


**Да.**


Просто scraping category page недостаточен для полной спецификации.


Категория позволяет получить как минимум:



- URL

- Title

- image

- Price

- Sale price


Но требуемые:



- Short description

- Description

- Specs

- Spec_detail


находятся на product page.


Это подтверждается предоставленным `product-page.html` и актуальной страницей товара. GitHub+1



## 4. Почему остальные варианты хуже


### Requests + BeautifulSoup


Не рекомендую как основной подход.


Причина не в том, что HTML невозможно получить обычным HTTP-запросом: фактически HTML сейчас доступен. Но проектный framework уже зафиксирован на `PlaywrightEngine`, а исходные материалы характеризуют сайт как JS-сайт.


Кроме того, браузер даёт более надёжное поведение при:



- динамическом контенте;

- загрузке изображений;

- изменениях frontend;

- Cloudflare-защите.


Поэтому переход на другой транспорт не даёт достаточной выгоды.


### Selenium


Технически возможен, но бессмысленен: проект уже использует PlaywrightEngine.


Добавление Selenium увеличит сложность без функциональной необходимости.


### Scrapy


Для большого production scraping-проекта Scrapy был бы допустим, но здесь он избыточен.


Уже существует browser engine, а задача относительно прямолинейная: категория → product pages → extraction → images → JSON.


### API


API использовать не из чего: в предоставленных материалах прямо указано, что API нет, а `network.har` пуст.


Искать API всё равно можно было бы дополнительно при разработке, но на текущем этапе нет основания строить решение вокруг API.


### GraphQL


Доказательств наличия GraphQL нет.


### Только category page


Слишком простой вариант, но он **не покрывает требуемые поля**.



## 5. Анализ сайта



... (обрезано, analysis, всего 17568 символов) ...

> **ВАЖНО:** Анализ выше мог содержать фразы вроде «переходить к написанию кода пока рано» или «нужно дождаться ответов клиента». Эти фразы относятся к моменту составления анализа и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — код писать нужно. Все данные уже предоставлены ниже.

---

## План проекта (этап 2)

Прочитал prompt целиком, включая спецификацию `DS-PRK-Scraper.json`, HTML-примеры, ограничения ядра и требования к проектированию. Ниже — проектирование реализации **без готового Python-кода**, как прямо требует prompt. GitHub+2GitHub+2


## Почему выбран Playwright + HTML


Выбор: **существующий PlaywrightEngine + HTML/BeautifulSoup**.


Причины:



- framework уже передаёт готовый `PlaywrightEngine` в `scrape_data(engine)`;

- сайт обозначен как JS-based;

- в материалах проекта API не обнаружен, `network.har` пустой;

- нужные данные находятся в HTML товарной страницы;

- листинг содержит URL товаров и обычную пагинацию `?p=2`, `?p=3` и т. д.;

- для теста нужны только 2 товара. GitHub+1


**Плюсы:** минимальное изменение архитектуры, совместимость с существующим browser context/cookies, обработка JS, простая навигация.


**Минусы:** зависимость от DOM-селекторов, потенциальные Cloudflare challenges и изменения frontend.


API, Selenium, Scrapy, `requests`/`httpx` и отдельный browser layer добавлять не следует.



# 1. Полный поток данных


Для тестового scrape:


`professionele-koeling.nl/koelkasten-kisten.html`
↓
`PlaywrightEngine`
↓
HTML категории
↓
из HTML извлекаются URL первых подходящих товаров
↓
`PlaywrightEngine` открывает product pages
↓
HTML товарных страниц
↓
`main.py` передаёт HTML в `parse_html_data()`
↓
`BeautifulSoup`
↓
`dict` с точными полями из `DS-PRK-Scraper.json`
↓
`list[dict]` из 2 товаров
↓
`exporter.py → JSON`


Для полного scrape впоследствии поток тот же, но scraper продолжает переходить по `?p=N`, пока не закончится пагинация. В категории сейчас указано 429 товаров и 36 товаров на страницу. GitHub


**Важный архитектурный момент:** `scraper.py` может использовать BeautifulSoup только для извлечения **URL и навигационной информации** из листинга. Он не должен извлекать бизнес-поля товара. `parser.py` получает готовый HTML и занимается всей экстракцией данных. Это соответствует фиксированному контракту framework. GitHub



# 2. Проектирование app/scraper.py


## 2.1 Интерфейс функций


ФункцияНазначениеВходВозврат`scrape_data(engine)`Главная точка входа; собирает HTML необходимых страниц`PlaywrightEngine``List[str]``_fetch_listing_html(engine, url)`Открывает страницу категории и возвращает её HTMLengine, URL`str``_fetch_product_html(engine, url)`Открывает товарную страницу и возвращает HTMLengine, URL`str``_extract_product_urls(html)`Извлекает URL товаров из category HTMLHTML`List[str]``_get_next_page_url(html, current_url)`Находит ссылку следующей страницыHTML, текущий URL`str | None`
Эти функции не должны возвращать уже распарсенные товары.


### scrape_data(engine)


Алгоритм:



- Начальный URL:
`https://www.professionele-koeling.nl/koelkasten-kisten.html`

- Открыть category page.

- Дождаться появления `.products-grid`.

- Получить HTML.

- `_extract_product_urls()` извлекает ссылки товаров.

- Для теста взять первые **2 уникальные product URL**.

- Открыть каждую product page.

- Получить HTML каждой страницы.

- Вернуть `List[str]` с HTML двух product pages.

- Для production/full scrape вместо ограничения `2` продолжать pagination.


Для тестовой задачи **не требуется возвращать HTML категории**, поскольку конечный parser должен получить product pages, содержащие все необходимые поля.


### _extract_product_urls(html)


На основании предоставленного HTML ожидаемый навигационный селектор:



- `.products-grid li.item`

- внутри карточки: `a.product-image[href]`

- также подтверждён `h2.product-name a[href]`.


Предпочтительно брать `a.product-image[href]` либо `h2.product-name a[href]` и дедуплицировать URL.


Пример из предоставленного HTML: карточка содержит ссылку на `polar-dm071.html`. GitHub


**ПРЕДПОЛОЖЕНИЕ:** `.products-grid li.item` является стабильным селектором карточек для текущего сайта, поскольку именно эта структура дана в входном HTML. Для полного каталога это следует проверить на нескольких страницах.


### _get_next_page_url(html, current_url)


В предоставленном HTML присутствует:


`a.next[href]`


и ссылки:



- `?p=2`

- `?p=3`

- `?p=4`

- `?p=5`.


Поэтому основной вариант — **не кликать Next**, а получать URL из `a.next[href]`.


Для full scrape:


`current page → a.next[href] → следующий URL → повторить`


Остановки:



- `a.next` отсутствует;

- ссылка ведёт на уже обработанный URL;

- HTML страницы пустой;

- `.products-grid li.item` отсутствует/пуст;

- достигнут фактический конец pagination.


Это надёжнее, чем самостоятельно вычислять номера страниц.


### Ожидание страницы


Перед получением HTML:



- дождаться `.products-grid` для category page;

- дождаться `.product-name h1` для product page.


**ПРЕДПОЛОЖЕНИЕ:** этих селекторов достаточно как индикаторов загрузки контента, поскольку они присутствуют в предоставленных HTML.


Lazy loading, tabs и "load more" в имеющихся данных не подтверждены. Infinite scroll также не обнаружен; присутствует обычная pagination. GitHub+1


### random_delay()


Использовать существующий `app.utils.random_delay()`:



- между открытием category/product pages;

- между переходами pagination;

- после получения одной product page перед переходом к следующей.


Не создавать собственную функцию задержки.


Причина — наличие Cloudflare `cf_clearance`; агрессивная параллельная загрузка увеличивает operational risk. GitHub


**Параллельные product pages для этой задачи не нужны.** Последовательный обход двух товаров проще и безопаснее.



# 3. Проектирование app/parser.py


Parser работает **только с уже полученным HTML** и не выполняет никаких сетевых запросов.


## 3.1 Интерфейс


ФункцияНазначениеВходВозврат`parse_html_data(raw_pages_content)`Обрабатывает список product HTML`List[str]``List[dict]``parse_product(html)`Извлекает один товар`str``dict``_parse_breadcrumb(soup)`Извлекает breadcrumbBeautifulSoup`str``_parse_short_description(soup)`Извлекает short descriptionBeautifulSoup`str``_parse_prices(soup)`Извлекает Price/Sale priceBeautifulSoup`tuple``_parse_images(soup)`Извлекает URL и имена изображенийBeautifulSoup`tuple``_parse_description(soup)`Извлекает полное описание без HTMLBeautifulSoup`str``_parse_specs(soup)`Извлекает характеристикиBeautifulSoupтребуемая структура`_clean_text(element)`Приводит HTML-текст к чистому текстуTag/текст`str`
Главная функция `parse_html_data()` последовательно вызывает `parse_product()` для каждого HTML.



# 3.2 Спецификация полей


Финальные ключи **не переименовывать**. В частности, пробелы в `"Title "` и `"Description "` являются частью авторитетной спецификации. `DS-PRK-Scraper.json` прямо запрещает изменять названия/порядок полей. GitHub


ПолеИсточникОбработкаЕсли отсутствует`URL`URL product pageабсолютный URL`""``Breadcrumb``.breadcrumbs`чистый текст, элементы breadcrumb разделяются выбранным стабильным разделителем`""``Title ``.product-name h1``.get_text(strip=True)``""``Short description``.short-description`HTML → чистый текст`""``imageurl`product image elementsвсе URL, несколько через запятую`""``image_name`URL/filename изображенияимена, несколько через запятую`""``Price``.old-price .price` при наличии скидки; иначе обычная цена`clean_price()``None`/`""` в зависимости от контракта exporter`Sale price``.special-price .price` только при наличии скидки`clean_price()``""``Description `основной блок полного описанияHTML → чистый текст`""``Specs`блок характеристиксогласно спецификациипустое значение`Spec_detail`значения характеристикheader = всё до `:`пустое значение
### URL


В отличие от category URL, `URL` должен представлять **конкретную product page**, потому что конечная запись относится к товару.


**ПРЕДПОЛОЖЕНИЕ:** использовать текущий canonical product URL/URL перехода scraper как значение `URL`, если отдельный canonical link не указан в спецификации HTML.


### Breadcrumb


В предоставленной странице:


`Home → Koelkasten&Kisten → Polar GE579`



... (обрезано, project_plan, всего 18111 символов) ...

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

Файл `app/scraper.py` — перепиши его полностью под план проекта:



---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/scraper.py` (модуль: **scraper**).

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

- Главная функция — `scrape_data(engine)`.
- Принимает `engine: PlaywrightEngine` (уже запущен, cookies/proxy подключены).
- Использует `engine.goto(url)` для навигации.
- Использует `engine.content()` для получения HTML после загрузки.
- Использует `engine.wait_for_selector(css)` для ожидания элементов.
- Использует `engine.page` для JS (eval, click, scroll).
- Отвечает **только** за навигацию, пагинацию, скролл, клики.
- Возвращает `List[str]` — список сырого HTML.
- НЕ парсит DOM с целью извлечения бизнес-данных — это задача parser.py.
- Используй `app.config.BASE_URL` как стартовый URL.

### Как обходить страницы товаров (product pages)

Если по плану нужны данные со страниц отдельных товаров — **scraper.py сам извлекает URL товаров из HTML листинга** (это навигационная логика, не бизнес-парсинг) и добавляет HTML каждой product page в результирующий список.

```python
def scrape_data(engine) -> List[str]:
    raw_contents = []

    # 1. Обход листинговых страниц
    current_url = BASE_URL
    while current_url:
        engine.goto(current_url)
        listing_html = engine.content()

        # 2. Извлечь URL товаров — допустимо в scraper через BeautifulSoup/regex
        product_urls = _extract_product_urls(listing_html)

        # 3. Зайти на каждую страницу товара
        for url in product_urls:
            engine.goto(url)
            raw_contents.append(engine.content())  # HTML товара → в список

        # 4. Пагинация листинга
        current_url = _get_next_page_url(listing_html, current_url)

    return raw_contents  # List[str] — HTML страниц товаров
```

`parse_html_data` в `main.py` затем вызовет `parse_listing()` для каждого из этих HTML. Значит `parse_listing()` должен уметь парсить HTML страницы товара (а не только листинга). Убедись, что логика `parse_listing()` в плане соответствует тому, какой именно HTML будет ему передан.

**Если достаточно листинговых страниц** (все нужные данные есть на странице категории) — добавляй в список HTML листинга, не заходи на product pages.

## Если модуль = parser

- Отвечает **только** за извлечение данных из сырого HTML.
- ОБЯЗАТЕЛЬНО экспортирует ОБЕ функции: `parse_listing(html)` и `parse_html_data(raw_contents)`.
- `parse_html_data` = вызывает `parse_listing` для каждого HTML и объединяет результаты.
- Используй BeautifulSoup для парсинга.
- Поля результата — строго по DS-PRK-Scraper.json из AI_INPUT.

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
- Использовать `requests`/`httpx` в scraper.py.
- Менять сигнатуры из контракта.
- Использовать классы.
- Запрашивать дополнительные файлы (project_plan.md и т.п.) — всё нужное УЖЕ в этом промпте.
