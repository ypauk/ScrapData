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

Клиент хочет получить scraper для сайта **professionele-koeling.nl**, который собирает данные о товарах из категории холодильного оборудования.

На текущем этапе требуется **не полный scrape**, а тестовая выгрузка только **2 товаров**. Для каждого товара необходимо собрать все поля, определённые в `DS-PRK-Scraper.json`, причём каждое поле должно находиться в отдельном JSON-поле и иметь стабильное имя.

Обязательные особенности:

- собрать URL товара и breadcrumb;
- название;
- короткое описание;
- изображения и их имена;
- обычную цену;
- цену со скидкой;
- полное текстовое описание без HTML;
- характеристики;
- отдельные значения характеристик;
- отсутствующие значения оставлять пустыми;
- товары без скидки не дублировать: `Sale price` должен быть пустым;
- включать товары, даже если они отсутствуют в наличии;
- изображения необходимо **скачивать**, а не только сохранять URL;
- порядок и названия полей должны строго соответствовать `DS-PRK-Scraper.json`.
`DS-PRK-Scraper.json` явно обозначен в исходном prompt как окончательная и авторитетная спецификация, поэтому его структуру нельзя самостоятельно изменять.

**Уверенность: высокая.**

## 2. Какой конечный результат нужен

Конечный результат — **JSON**.

На текущем этапе:

- JSON с данными 2 товаров.
- Скачанные изображения этих товаров.
- Поля JSON должны соответствовать структуре `DS-PRK-Scraper.json`.
В спецификации присутствуют следующие поля:

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
Особое внимание нужно уделить пробелам в названиях `Title ` и `Description `: поскольку спецификация объявлена авторитетной, **переименовывать их нельзя**.

**Уверенность: высокая.**

## 3. Как лучше решить задачу

Рекомендуемый подход — **Playwright + существующий PlaywrightEngine проекта + парсинг HTML средствами Python**.

Основная последовательность:

**категория → ссылки товаров → страницы товаров → извлечение данных → скачивание изображений → JSON.**

Почему именно так:

- в `notes.txt` прямо указано, что сайт работает с JavaScript;
- в prompt зафиксировано, что `scraper.py` уже получает готовый `PlaywrightEngine` из framework;
- поэтому использование браузера уже является частью инфраструктуры проекта и не требует добавления отдельной Selenium-архитектуры;
- HTML категории содержит ссылки на страницы товаров;
- HTML товара содержит breadcrumb, название, short description и цены;
- пагинация явно присутствует;
- для полного scrape потребуется обход страниц категории;
- для теста достаточно обработать первые 2 подходящих товара.
При этом не следует автоматически усложнять решение поиском API: в предоставленных материалах указано `API нет`, а `network.har` пустой. Поэтому на основании имеющихся данных наиболее простой путь — получать HTML через уже предоставленный PlaywrightEngine и извлекать данные из DOM.

**Уверенность: высокая для тестового scrape; средняя для полного сайта**, поскольку фактическая структура остальных товарных страниц не представлена.

## 4. Почему остальные варианты хуже

### Requests + BeautifulSoup

Не рекомендую как основной способ.

Причина: в материалах проекта прямо указано, что сайт использует JavaScript, а framework уже построен вокруг `PlaywrightEngine`. Кроме того, prompt отдельно запрещает считать рекомендацию `requests вместо Playwright` применимой в этом проекте.

### Selenium

Технически способен решить задачу, но не даёт преимуществ перед уже существующим PlaywrightEngine. Это будет ненужное усложнение.

### Scrapy

Для большого статического сайта мог бы быть хорошим вариантом, но здесь уже есть browser engine, а часть сайта потенциально зависит от JS. Введение Scrapy ради 429 товаров не выглядит оправданным.

### API

Предоставленные материалы не показывают доступного API. `network.har` пустой, а в `notes.txt` указано, что API нет.

Искать API специально можно было бы только при появлении новых доказательств его существования.

### GraphQL

Признаков GraphQL в предоставленных данных нет.

### Selenium/Playwright + отдельная API-архитектура

Избыточно: сейчас нет подтверждения, что API вообще существует.

**Вывод:** использовать уже имеющийся PlaywrightEngine и максимально простой DOM parsing.

## 5. Анализ сайта

### JavaScript Rendering

**Да, по предоставленной информации — вероятно.**

В `notes.txt` прямо указано: «сайт на JS». Однако конкретно определить, какие именно элементы требуют JS, по сжатому HTML невозможно.

**Уверенность: высокая.**

### React

Признаков React нет.

HTML и классы выглядят как традиционный серверный e-commerce frontend. Делать вывод о React нельзя.

**Уверенность: средняя.**

### Vue

Признаков Vue нет.

**Уверенность: средняя.**

### Angular

Признаков Angular нет.

**Уверенность: средняя.**

### API

В предоставленных материалах указано, что API нет.

`network.har` пустой, поэтому дополнительного подтверждения API через network trace нет.

**Уверенность: средняя/высокая.**

### GraphQL

Признаков нет.

**Уверенность: средняя.**

### Infinite Scroll

Не обнаружен.

На странице присутствует обычная пагинация:

`?p=2`, `?p=3`, `?p=4` и т. д.

Кроме того, страница сообщает:

`Artikelen 1 tot 36 van 429 in totaal`

То есть сейчас обнаружено **429 товаров**, по 36 товаров на страницу.

**Уверенность: высокая.**

### Pagination

**Да.**

Есть обычная pagination с параметром `p`.

**Уверенность: высокая.**

### Login

Признаков обязательной авторизации нет.

**Уверенность: высокая для предоставленного сценария.**

### Cookies

**Да.**

Предоставлен `cookies.json`. Среди cookies есть:

- Cloudflare-related cookie;
- Google Analytics cookies;
- frontend cookies.
Значения cookies не требуется включать в scraper-анализ или воспроизводить в результате.

**Уверенность: высокая.**

### JWT

Признаков JWT нет.

### Bearer Token

Признаков Bearer Token нет.

### CAPTCHA

Наличие CAPTCHA не подтверждено.

**Уверенность: низкая/средняя.**

### Cloudflare

**Да, признаки присутствуют.**

В `cookies.json` имеется cookie `cf_clearance`, что указывает на использование Cloudflare challenge/clearance-механизма.

Это не означает, что CAPTCHA будет появляться при каждом запросе, но Cloudflare следует считать потенциальным фактором блокировки.

**Уверенность: высокая.**

### Rate Limits

Явного rate limit в предоставленных материалах нет.

Но поскольку присутствует Cloudflare, агрессивный параллельный scraping потенциально может привести к challenge или блокировке.

**Уверенность: средняя.**

### Download Files

**Да, изображения необходимо скачивать.**

Это явно указано в ответах проекта.

### Upload Files

Не требуется.

### Lazy Loading

Не подтверждено.

В предоставленном HTML изображение товара находится непосредственно в `<img src="...">`, но это ещё не доказывает отсутствие lazy loading на других страницах.

**Уверенность: средняя.**

### WebSocket

Признаков нет.

### XHR/Fetch

По пустому `network.har` определить невозможно.

### Sitemap

Не предоставлен.

Наличие sitemap из имеющихся файлов определить нельзя.

### robots.txt

Не предоставлен.

Наличие и содержимое `robots.txt` определить нельзя.

## 6. Что необходимо собрать до начала разработки

Для **тестовой версии** критически необходимой дополнительной информации практически нет: материалы уже содержат:

- описание задачи;
- финальную спецификацию JSON;
- пример category HTML;
- пример product HTML;
- pagination;
- cookies;
- checkpoint;
- ответы на основные вопросы клиента.
Однако перед переходом к production/full scrape желательно получить или проверить:

- **HTML второй тестовой страницы товара**, чтобы убедиться, что структура характеристик стабильна.
- **Пример ожидаемого JSON именно для 2 товаров**, если клиент ожидает определённую структуру верхнего уровня — например массив объектов или другой контейнер.
- Подтверждение того, как именно должен выглядеть `imageurl` после скачивания изображения: исходный URL, локальный путь или оба значения.
- Подтверждение формата `Specs`, поскольку в спецификации значение содержит инструкцию `each own colom`, а не полноценный пример структуры JSON.
- Подтверждение, что скачанные изображения должны физически присутствовать рядом с JSON или в отдельном каталоге.
При этом **Google Sheet дополнительно получать не нужно**: prompt прямо запрещает его реконструировать и сообщает, что его содержимое уже полностью перенесено в `DS-PRK-Scraper.json`.

## 7. Возможные сложности

### 1. Cloudflare

Наличие `cf_clearance` означает потенциальную защиту от автоматизированного доступа.

Риск особенно возрастает при:

- высокой частоте запросов;
- большом количестве параллельных страниц;
- повторных запусках;
- отсутствии нормального browser context.
### 2. JavaScript

Некоторые данные могут появляться или изменяться после выполнения JS.

Поэтому HTML, полученный обычным HTTP-запросом, нельзя считать гарантированно достаточным для всех страниц.

### 3. Изменение HTML

Селекторы основаны на текущей структуре сайта. При изменении frontend потребуется адаптация scraper.

### 4. Характеристики

`Specs` и `Spec_detail` требуют аккуратного преобразования данных.

Особенно важно не смешивать несколько характеристик в одной колонке, поскольку клиент отдельно требует: **каждое поле в отдельной колонке**.

### 5. Разные шаблоны товаров

Предоставлен только один пример product page. Нельзя гарантировать, что все 429 товаров имеют абсолютно одинаковый HTML.

### 6. Изображения

У одного товара может быть несколько изображений. В спецификации явно указано разделять несколько значений запятыми.

Кроме того, изображения нужно не просто извлечь, но и скачать.

### 7. Pagination

Для полного scrape потребуется пройти все страницы категории. Сейчас обнаружено 429 товаров при 36 товарах на страницу, то есть объём уже значительно больше тестовых двух товаров.

### 8. Цены

Нужно корректно различать:

- обычную цену;
- sale price;
- отсутствие скидки.
По правилам проекта при отсутствии скидки `Sale price` должен оставаться пустым.

### 9. Товары без наличия

Такие товары **необходимо включать**, поэтому нельзя фильтровать каталог только по availability.

## 8. Что нужно уточнить у клиента

Большинство вопросов уже закрыты в `answers.txt`, поэтому не нужно повторно спрашивать клиента о категориях, количестве тестовых товаров, скидках, изображениях, HTML или отсутствии характеристик.

Остаются только вопросы, которые действительно не определены однозначно.

### Вопрос 1 — структура JSON

Нужно уточнить, должен ли итоговый JSON быть:

- массивом объектов товаров;
- объектом с массивом товаров;
- либо последовательностью отдельных JSON-объектов.
В предоставленной спецификации показан один объект товара, но формат контейнера для нескольких товаров явно не определён.

### Вопрос 2 — imageurl

Нужно уточнить, что именно должно находиться в `imageurl` после требования скачать изображения:

- исходный URL сайта;
- локальный путь;
- или URL + локальный путь в разных полях.
### Вопрос 3 — Specs

Нужно уточнить ожидаемую структуру `Specs` в JSON, если клиент ожидает именно отдельные значения, а не одно текстовое поле.

При этом `Spec_detail` явно описывает правило: всё до `:` является header. Это нужно сохранить без переинтерпретации.

**Если клиент подтверждает эти три пункта, дополнительных блокирующих вопросов для тестовой реализации нет.**

## 9. Рекомендуемый стек технологий

- **Python**
- **Playwright / существующий PlaywrightEngine проекта**
- **HTML parsing**
- **JSON**
- **HTTP/browser download для изображений**
Не требуется добавлять API, Selenium, Scrapy или отдельную базу данных.

## 10. План разработки

### Этап 1 — Проверка тестового сценария

**Цель:** получить две страницы товаров из категории.

**Ожидаемый результат:** корректно открываются страницы и извлекается HTML.

**Зависимости:** существующий PlaywrightEngine.

### Этап 2 — Извлечение основных полей

**Цель:** получить URL, breadcrumb, title, short description, цены и description.

**Ожидаемый результат:** все соответствующие поля заполнены согласно `DS-PRK-Scraper.json`.

**Зависимости:** HTML product page.

### Этап 3 — Извлечение характеристик

**Цель:** преобразовать характеристики в требуемый формат без смешивания разных данных.

**Ожидаемый результат:** `Specs` и `Spec_detail` соответствуют финальной спецификации.

**Зависимости:** подтверждение фактической структуры характеристик на тестовых товарах.

### Этап 4 — Изображения

**Цель:** найти все необходимые изображения и скачать их.

**Ожидаемый результат:** изображения физически сохранены, а `imageurl`/`image_name` заполнены согласно спецификации.

**Зависимости:** уточнение формата локальных ссылок/имён, если он не определён framework.

### Этап 5 — JSON для двух товаров

**Цель:** сформировать тестовую выгрузку.

**Ожидаемый результат:** JSON с двумя товарами, строго соответствующий структуре спецификации.

**Зависимости:** завершение предыдущих этапов.

### Этап 6 — Проверка

**Цель:** убедиться, что нет смешанных колонок/полей, пропущенных обязательных данных или неправильной обработки скидок.

**Ожидаемый результат:** готовый тестовый файл для отправки клиенту.

**Зависимости:** готовый JSON.

### Этап 7 — Full scrape после подтверждения теста

**Цель:** масштабировать проверенное решение на весь необходимый объём.

**Ожидаемый результат:** обработка всех требуемых товаров с pagination.

**Зависимости:** подтверждение клиентом тестового файла и отсутствие замечаний.

## 11. Оценка сложности

ПараметрОценкаСложность**4/10**Тестовая разработка (2 товара)**2–3 часа**Full scrape**4–7 часов**Вероятность блокировок**Средняя**Вероятность необходимости браузера**Высокая**Вероятность изменения сайта в будущем**Средняя**Общий риск**Средний**Основной технический риск — не parsing HTML, а стабильность browser access при наличии Cloudflare и возможные различия между шаблонами товаров.

Оценка времени предполагает, что framework с PlaywrightEngine уже работает и не требует дополнительной разработки инфраструктуры.

**Уверенность в оценке: средняя.**

## 12. Можно ли решить проще

**Да.**

Проект не требует сложной архитектуры.

Самое простое решение:

**существующий PlaywrightEngine → категория → ссылки на товары → страницы товаров → parsing → скачивание изображений → JSON.**

Не нужны:

- база данных;
- API;
- GraphQL;
- Scrapy;
- Selenium;
- отдельный backend;
- сложная система очередей;
- отдельная browser architecture.
Также стоит рассмотреть ещё более простой вариант: если после проверки окажется, что **вся требуемая информация действительно присутствует непосредственно в category listing**, можно минимизировать переходы на product pages.

Однако предоставленный пример category page показывает только URL, изображение, название и цены товара. Там нет полного описания и характеристик. Поэтому для текущей спецификации переход на product pages, скорее всего, потребуется.

**Уверенность: высокая.**

## 13. Итоговая рекомендация

Рекомендуется использовать **Python + существующий PlaywrightEngine + простой HTML parsing**, без API и без дополнительных scraping-фреймворков.

Это оптимальный вариант потому что:

- проект уже использует PlaywrightEngine;
- сайт обозначен как JS-based;
- доступного API в предоставленных материалах нет;
- обычная pagination хорошо определяется;
- HTML product page содержит основные требуемые данные;
- объём теста составляет всего 2 товара;
- архитектуру не нужно усложнять до подтверждения тестового результата.
Перед написанием кода желательно получить только недостающие уточнения:

- структура JSON для нескольких товаров;
- точный смысл `imageurl` после скачивания изображений;
- ожидаемая структура `Specs`, если она не очевидна из фактического HTML.
При этом **не нужно запрашивать Google Sheet или “оригинальный” **`DS-PRK-Scraper.json` — prompt прямо говорит, что имеющийся JSON является финальной спецификацией.

**Можно переходить к разработке тестового scraper после уточнения этих неоднозначных моментов. Код на данном этапе намеренно не приводится, поскольку исходный prompt прямо запрещает переходить к реализации.**

**Итог:** проект относительно простой по parsing, но имеет средний operational risk из-за JavaScript и Cloudflare. Для теста из 2 товаров оптимально не строить ничего сложного: сначала подтвердить корректность извлечения всех полей и изображений, затем масштабировать тот же подход на весь каталог.
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