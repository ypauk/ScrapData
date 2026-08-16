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

## 1. Краткое описание задачи


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

> **ВАЖНО:** Анализ выше мог содержать фразы вроде «переходить к написанию кода пока рано» или «нужно дождаться ответов клиента». Эти фразы относятся к моменту составления анализа и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — код писать нужно. Все данные уже предоставлены ниже.

---

## План проекта (этап 2)

Я прочитал prompt целиком, включая `DS-PRK-Scraper.json`, HTML-примеры, ограничения ядра и требования к формату ответа. Ниже — проектирование реализации **без готового Python-кода**, строго в рамках заданной архитектуры. GitHub+2GitHub+2


# 1. Полный поток данных


Для текущей задачи оптимален **Playwright + HTML + BeautifulSoup**.


Причины:



- framework уже принудительно использует `PlaywrightEngine`;

- сайт обозначен как JS-based;

- доступного API нет, `network.har` пустой;

- в category HTML есть ссылки на товары;

- необходимые `Description`, `Specs` и остальные детальные поля находятся на product page;

- обычная пагинация реализована через `?p=N`;

- тест требует только 2 товара. GitHub+1


Плюсы:



- JS выполняется браузером;

- используется уже существующая инфраструктура с cookies/proxy/user-agent;

- не требуется новая scraping-архитектура;

- легко перейти от тестовых 2 товаров к полному каталогу.


Минусы:



- Playwright тяжелее обычного HTTP-клиента;

- Cloudflare может вызвать challenge;

- HTML-селекторы зависят от текущего frontend;

- фактическая структура `Specs` и изображений не представлена полностью.


### Поток


professionele-koeling.nl/koelkasten-kisten.html        ↓PlaywrightEngine        ↓HTML category page        ↓scraper.py  ├─ определить ссылки product pages  ├─ определить следующую страницу  └─ открыть product pages        ↓HTML product pages        ↓main.py        ↓parser.py / BeautifulSoup        ↓list[dict]        ↓exporter.py        ↓JSON
Для тестового запуска обход должен остановиться после **2 уникальных product URLs**. Для production-режима тот же механизм должен продолжать pagination до последней страницы. В исходных материалах каталог содержит 429 товаров по 36 на страницу. GitHub



# 2. Проектирование app/scraper.py


Главный контракт менять нельзя:


`scrape_data(engine) → List[str]`


Каждый элемент результата — HTML отдельной страницы товара.


## 2.1. Функции


ФункцияНазначениеВходВозврат`scrape_data(engine)`Главный orchestration flow`PlaywrightEngine``List[str]``_fetch_listing_html(engine, url)`Открыть category page и получить готовый HTMLengine, URL`str``_fetch_product_html(engine, url)`Открыть product page и получить HTMLengine, URL`str``_extract_product_urls(html)`Извлечь URL товаров из listing HTMLHTML`List[str]``_get_next_page_url(html, current_url)`Определить следующую страницуHTML, URL`str | None`
Эти функции соответствуют зафиксированному контракту framework. `parser.py` в `scraper.py` импортировать нельзя. GitHub


## 2.2. Начальная страница


URL:


`https://www.professionele-koeling.nl/koelkasten-kisten.html`


На listing card уже подтверждён такой элемент:


li.item    └─ div.product-image-wrapper         └─ a.product-image[href]
Также ссылка присутствует здесь:


h2.product-name    └─ a[href]
Для URL товара предпочтительнее использовать:


li.item h2.product-name a[href]
а `a.product-image[href]` использовать как fallback.


**ПРЕДПОЛОЖЕНИЕ:** для всех карточек товара сохраняется тот же DOM-шаблон. Предоставлен только один пример карточки, поэтому это необходимо проверить на реальной второй карточке.


## 2.3. Алгоритм scrape_data



- Открыть category URL через `_fetch_listing_html()`.

- Получить product URLs через `_extract_product_urls()`.

- Удалить дубликаты с сохранением порядка.

- Для теста взять первые 2 URL.

- Для каждого URL:



- выполнить `random_delay()`;

- открыть product page;

- дождаться загрузки страницы;

- получить HTML;

- добавить HTML в результирующий список.

- Если реализуется full scrape:



- определить next URL через `_get_next_page_url()`;

- повторять процесс до отсутствия следующей страницы.

- Вернуть `List[str]`.


Listing HTML не обязательно возвращать в результат: бизнес-данные требуются с product pages, поэтому итоговый список может содержать только HTML товаров.


Это соответствует зафиксированному правилу: scraper занимается навигацией и сам находит product URLs, а parser затем получает product HTML. GitHub



# 3. Pagination


Здесь не нужен infinite scroll и не нужен клик по кнопке.


В HTML явно присутствует:


...?p=2...?p=3...?p=4
и:


a.next[href]
Поэтому основной вариант — использовать существующий `href` кнопки Next.


### _get_next_page_url()


Логика:



- найти `.pager .pages`;

- найти `a.next[href]`;

- получить `href`;

- преобразовать relative URL в absolute при необходимости;

- если `a.next` отсутствует — вернуть `None`.


Fallback:



- можно определить наличие следующей страницы по последнему номеру pagination;

- но это хуже, поскольку `next` уже явно предоставлен HTML.


**ПРЕДПОЛОЖЕНИЕ:** `a.next` корректно отражает последнюю страницу на всём каталоге. Это следует подтвердить при full scrape.


Для теста pagination вообще не требуется: после получения двух product URLs scraper останавливается.



# 4. Поведение Playwright


Перед получением HTML необходимо ждать появления основного содержимого страницы.


Для listing:


.products-grid
Для product:


.product-name h1
Эти селекторы подтверждены предоставленным HTML. GitHub


### Lazy loading


Подтверждения обязательного lazy loading нет.


Поэтому:



- сначала обычная загрузка;

- дополнительный scroll не делать;

- если тестовая страница покажет lazy-loaded product content/images, тогда добавить адресный scroll.


**ПРЕДПОЛОЖЕНИЕ:** весь необходимый текст product page доступен после обычного завершения загрузки.


### Tabs / "Показать ещё"


В предоставленном product HTML признаков необходимости кликов нет.


Следовательно, для теста:



- tabs не открывать;

- `Show more` не нажимать;

- accordion не раскрывать.



# 5. random_delay()


Использовать уже существующий `app.utils.random_delay()`.


Рекомендуемые места:



- между открытием category и product page;

- между двумя product pages;

- между страницами pagination.


Не создавать собственную функцию задержки.


Это особенно важно из-за обнаруженного `cf_clearance` и потенциального Cloudflare challenge. GitHub



# 6. Важная проблема с загрузкой изображений


Здесь есть **архитектурное противоречие**, которое нельзя скрывать.


Клиент требует:



- скачать изображения физически;

- сохранить `imageurl`;

- сохранить `image_name`.


При этом framework фиксирует:



- `scraper.py → List[str]`;

- `parser.py` не имеет права выполнять сеть;

- `main.py`, `exporter.py` и остальные core-модули изменять нельзя. GitHub


Самый чистый вариант — скачивание делать на уровне scraper как сетевую операцию, но scraper при этом не должен заниматься бизнес-парсингом HTML.


### Рекомендуемый вариант


`PlaywrightEngine` открывает product page и scraper на сетевом уровне отслеживает загружаемые image resources.


То есть:


product page    ↓Playwright network/resource events    ↓image response    ↓download/save
Scraper не должен искать `img`/CSS-селекторы ради бизнес-экстракции.


Однако остаётся проблема: страница загружает не только product images, но потенциально logo, icons, banners и другие изображения.


**ПРЕДПОЛОЖЕНИЕ:** необходимо дополнительно проверить реальные network resources product page, чтобы определить надёжный признак именно product images.


Если framework не предоставляет механизм сохранения таких resources, то требование "скачать изображения" **невозможно полностью выполнить только через два пустых модуля при неизменяемом main.py/exporter.py**. Это единственный существенный архитектурный блокер.



# 7. Проектирование app/parser.py


Parser работает исключительно в памяти:


HTML string   ↓BeautifulSoup   ↓dict
Никаких HTTP-запросов, Playwright или скачивания файлов.


## 7.1. Интерфейс


ФункцияНазначениеВходВозврат`parse_html_data(raw_pages_content)`Обработать все product HTML`List[str]``List[dict]``parse_product(html)`Извлечь один товар`str``dict``_parse_breadcrumb(soup)`Извлечь breadcrumbBeautifulSoup`str``_parse_title(soup)`Извлечь названиеBeautifulSoup`str``_parse_short_description(soup)`Извлечь short descriptionBeautifulSoup`str``_parse_prices(soup)`Извлечь обычную/sale ценуBeautifulSoup`(price, sale_price)``_parse_description(soup)`Извлечь полный descriptionBeautifulSoup`str``_parse_images(soup)`Извлечь image URL/nameBeautifulSoupсоответствующие значения`_parse_specs(soup)`Извлечь характеристикиBeautifulSoupзначение `Specs``_parse_spec_detail(soup)`Разложить характеристики согласно правиламBeautifulSoupзначение `Spec_detail`
`parse_html_data()` является адаптером между контрактом `main.py` и `parse_product()`.



# 8. Спецификация полей


Порядок **строго сохраняется**:


URLBreadcrumbTitle Short descriptionimageurlimage_namePriceSale priceDescription SpecsSpec_detail
Пробелы в `Title ` и `Description ` нельзя удалять. Это прямо зафиксировано как authoritative specification. GitHub


## URL


Источник:


product page URL
Поскольку HTML сам по себе не гарантирует исходный URL, наиболее надёжный вариант — передавать URL вместе с raw page либо извлекать canonical URL, если он присутствует.


Но текущий контракт `List[str]` не предусматривает отдельного URL.


**ПРЕДПОЛОЖЕНИЕ:** product page содержит canonical URL либо framework/HTML позволяет однозначно восстановить текущий URL.


Это нужно проверить.


## Breadcrumb


Селектор:


.breadcrumbs li
В предоставленном HTML:


HomeKoelkasten&KistenPolar GE579
Нужно сохранить breadcrumb как одну строку, используя фактическую структуру спецификации.


Не следует самостоятельно добавлять новые поля.


## Title


Селектор:


.product-name h1
Пример:


Polar GE579
Результат — очищенный текст.


## Short description


Селектор:


.short-description .std
Из HTML удалить:



- `<br>`;

- HTML-теги;

- лишние пробелы.


При этом рекламный блок внутри `.short-description`, содержащий телефон, требует отдельной проверки.


**ПРЕДПОЛОЖЕНИЕ:** short description должна соответствовать только основному описательному абзацу товара, а не рекламному CTA-блоку. Это нельзя считать окончательно подтверждённым предоставленным HTML.


## imageurl


Извлекаются URL всех product images.


Несколько значений:


url1,url2,url3
согласно authoritative instruction:



multiple — separated by comma. GitHub



Но точное соответствие `imageurl` после физического скачивания остаётся не определено: исходный URL или локальный путь.


## image_name


Для каждого изображения получить filename из URL.


Например концептуально:


polar_dm071_glasdeurkoelkast_46_liter.jpg
Несколько:


image1.jpg,image2.jpg
## Price


На текущем product HTML:


.price-box .old-price .price
содержит:


€ 255,99
Цена должна передаваться через уже существующий `utils.clean_price()`.


Не создавать собственный price cleaner.


## Sale price


Селектор:


.price-box .special-price .price
Пример:


€ 229,00
Если `.special-price` отсутствует — `""`.


Важно:


нет скидки → Sale price = ""
а не копирование обычной цены. Это явно подтверждено входными данным. GitHub


## Description


Это **полное текстовое описание**, без HTML.


Нужно найти основной контейнер description на product page, удалить HTML и нормализовать whitespace.


Предоставленный compressed HTML показывает только верхнюю часть страницы и **не содержит DOM полного description/specification section**.


Поэтому конкретный selector для него нельзя честно назвать подтверждённым.


**ПРЕДПОЛОЖЕНИЕ:** полный description находится в стандартном Magento product description container, но его фактический selector необходимо проверить на полном HTML.


Не следует придумывать selector до такой проверки.



# 9. Specs


Это наиболее неопределённое поле.


В `DS-PRK-Scraper.json` значение:


https://www.awesomescreenshot.com/... each own colom
является инструкцией, а не реальным значением поля. Это прямо уточнено в `notes.txt`. GitHub


Требование клиента:



каждое поле в собственной колонке.



Поэтому нельзя сделать:


Specs = "Artikelnummer: GE579; Inhoud: 29 liter; ..."
если это приводит к смешению отдельных характеристик.


Однако одновременно существующий JSON содержит **только одно имя Specs**, а не заранее перечисленные названия отдельных характеристик.


Поэтому:


**ПРЕДПОЛОЖЕНИЕ:** `Specs` должен содержать структуру/значение, предусмотренное конкретным exporter/framework, но его точный JSON-тип из имеющихся материалов не определён.


Самостоятельно добавлять:


ArtikelnummerInhoudEnergieklasseGewicht...
как новые поля нельзя — prompt прямо запрещает добавление output columns.



# 10. Spec_detail


Правило однозначно:



всё до `:` является header. GitHub



Например:


Artikelnummer: GE579
разбирается как:


header = "Artikelnummer"value = "GE579"
А:


Inhoud: 29 liter
как:


header = "Inhoud"value = "29 liter"
Особый случай:


Temperatuurbereik: 3-5°C ...Temperatuurbereik: 5-8°C ...Temperatuurbereik: 8-12°C ...
Нельзя терять повторяющиеся headers.


Следовательно, parser должен сохранять все пары, а не превращать их в обычный dict, где последующее значение перезапишет предыдущее.


**ПРЕДПОЛОЖЕНИЕ:** конкретный формат хранения повторяющихся `Spec_detail` должен быть подтверждён на фактическом `DS-PRK-Scraper.json`/exporter contract; исходные материалы этого не определяют.



# 11. Финальная структура одного результата


На уровне имен ключей структура должна быть именно такой:


{    "URL": ...,    "Breadcrumb": ...,    "Title ": ...,    "Short description": ...,    "imageurl": ...,    "image_name": ...,    "Price": ...,    "Sale price": ...,    "Description ": ...,    "Specs": ...,    "Spec_detail": ...}
Не добавлять:



- SKU;

- availability;

- currency;

- product ID;

- category;

- image count;

- timestamps;

- scrape status.


Их нет в authoritative output specification.



# 12. Обработка отсутствующих значений


Правило для parser:


ПолеЕсли отсутствует`URL``""` / значение, согласованное с существующим exporter`Breadcrumb``""``Title ``""``Short description``""``imageurl``""``image_name``""``Price``None``Sale price``""``Description ``""``Specs`пустое значение`Spec_detail`пустое значение
Для цены предпочтительно использовать существующий `clean_price()` и не создавать второй механизм очистки.



# 13. Обработка ошибок


СценарийДействиеTimeoutПовторить ограниченное число раз, затем записать ошибку и пропустить страницу403Записать в лог и остановить scrapingCloudflare challengeЗаписать в лог и остановить scraping для ручного вмешательстваCAPTCHAОстановить scraping, не пытаться обходить challengeProduct page без titleЗаписать warning, вернуть остальные поляНет цены`None`, продолжитьНет sale price`""`, продолжитьНет description`""`, продолжитьНет specsпустые поляНет изображенияпустые `imageurl`/`image_name`, продолжитьПустой listingзаписать в лог и завершить paginationДубликат product URLпропуститьНеожиданный HTMLwarning + сохранить страницу/ошибку в логах, не падать всем запуском
Для теста из двух товаров лучше **не продолжать агрессивно после Cloudflare/CAPTCHA**, поскольку повторные запросы могут только увеличить вероятность блокировки.



# 14. Риски



- **Cloudflare** — подтверждён `cf_clearance`; основной operational risk.

- **Login** — обязательная авторизация не обнаружена.

- **Rate limiting** — явного лимита нет, но Cloudflare делает агрессивный parallel scraping нежелательным.

- **CAPTCHA** — не подтверждена.

- **Infinite Scroll** — не обнаружен.

- **Shadow DOM** — признаков нет.

- **iframe** — признаков нет.

- **WebSocket** — признаков нет.

- **GraphQL API** — признаков нет.

- **Изменение DOM** — средний риск.

- **Различия product templates** — высокий риск для full scrape, поскольку предоставлен только один пример product page.

- **Specs** — фактическая DOM-структура не предоставлена.

- **Images** — требования к физическому скачиванию конфликтуют с текущим `List[str]`-контрактом.

- **URL** — текущий контракт scraper не передаёт URL вместе с HTML.

- **JSON container** — не определено, массив объектов это или другой верхнеуровневый формат.


Первые два риска особенно важны для production. Наличие Cloudflare подтверждено входными материалами, а API/GraphQL не подтверждены. GitHub+1



# 15. Что останется неизвестным


Вот что **нельзя достоверно вывести** из предоставленных материалов:



- **Полный selector Description .** Доступен только фрагмент product HTML.

- **Полный selector/DOM Specs.**

- **Точный формат Specs в JSON.**

- **Точный формат Spec_detail при повторяющихся headers.**

- **Что именно должен содержать imageurl: исходный URL, локальный путь или оба значения.**

- **Как именно физически связывать скачанный image с конкретным JSON-record при неизменяемом контракте scrape_data() → List[str].**

- **Есть ли несколько product images и где именно они расположены в полном DOM.**

- **Есть ли canonical URL на product page.**

- **Одинаков ли product template у остальных 428 товаров.**

- **Как exporter ожидает верхнеуровневую структуру JSON для нескольких товаров.**


При этом **не нужно запрашивать Google Sheet**: prompt прямо говорит, что `DS-PRK-Scraper.json` является окончательной спецификацией. GitHub



# 16. Порядок реализации


Я бы поменял предложенный в prompt порядок таким образом, чтобы сначала зафиксировать реальные HTML-контракты.


### 1. parser.py


Сначала реализовать parsing на предоставленном product HTML.


Проверить:



- title;

- breadcrumb;

- short description;

- price;

- sale price;

- нормализацию текста;

- базовую обработку отсутствующих элементов.


Это не зависит от сети и позволяет быстро обнаружить несовпадение ожидаемой структуры.


### 2. Получить/проверить полный product HTML


До финализации parser необходимо увидеть:



- полный description;

- specs;

- все изображения;

- availability;

- возможные альтернативные шаблоны.


Это особенно важно, поскольку предоставленный HTML является **сжатым**, а не полноценной страницей.


### 3. scraper.py


После подтверждения selectors:


category → product URLs → product pages → HTML
Для теста — ровно 2 товара.


### 4. Проверка image pipeline


Отдельно подтвердить, что существующий `PlaywrightEngine` позволяет сохранить product images без изменения core-модулей.


Если нет — это нужно зафиксировать как архитектурный блокер, а не обходить изменением `main.py` вопреки требованиям.


### 5. Интеграционный тест


Проверить:


scrape_data(engine)        ↓List[str]        ↓parse_html_data()        ↓List[dict]        ↓save_to_json()
### 6. Тест на два товара


Обязательно проверить:



- ровно 2 товара;

- все 11 ключей;

- точный порядок ключей;

- `Sale price == ""` для товара без скидки;

- description без HTML;

- отсутствие смешанных характеристик;

- отсутствие дублей;

- наличие image metadata;

- наличие физических image files.


### 7. Только после подтверждения клиента — full scrape


Для полного каталога:


page 1 → page 2 → ... → last page
с дедупликацией product URLs и контролируемыми задержками.



# 17. Краткое резюме


**Технология:** существующий `PlaywrightEngine` + HTML + BeautifulSoup. API, Selenium, Scrapy и отдельная browser architecture не нужны.


**scraper.py:**



- `scrape_data(engine)`

- `_fetch_listing_html()`

- `_fetch_product_html()`

- `_extract_product_urls()`

- `_get_next_page_url()`


**parser.py:**



- `parse_html_data()`

- `parse_product()`

- отдельные функции для breadcrumb/title/description/prices/images/specs.


**Итоговая структура:** строго 11 полей из `DS-PRK-Scraper.json`, включая пробелы в `Title ` и `Description `. Никаких дополнительных полей. GitHub


**Главные риски:** Cloudflare, различия product templates, неизвестная полная DOM-структура `Specs`/`Description`, а также архитектурная неоднозначность физического скачивания изображений при неизменяемом контракте `scrape_data() → List[str]`.


**Главный вывод:** для теста из двух товаров решение простое и технически подходит. Но перед фактической реализацией необходимо проверить полный HTML хотя бы второго товара и механизм сохранения изображений. При этом **изменять main.py, config.py, browser.py, utils.py или exporter.py не следует** — это прямо запрещено исходным prompt. GitHub+1

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

--- ФАЙЛ: page.html ---
https://www.professionele-koeling.nl/koelkasten-kisten.html - категория

<li class="item" style="height: 342.859px; padding-bottom: 75px;">
            
                <div class="product-image-wrapper" style="max-width:295px;">
                
                    <a href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html" title="Polar DM071" class="product-image">
                        <img id="product-collection-image-212" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" alt="Polar DM071">

                        
                                            </a>
                
                    <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover" style="opacity: 0.465749; display: none;">
			<li><a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/SiBQpy2rW3vTJnQQ/" title="Zet op verlanglijst">
					<span class="2 icon ib ic ic-heart"></span>
			</a></li>
			<li><a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/form_key/SiBQpy2rW3vTJnQQ/" title="Voeg toe aan productvergelijking">
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

                
                
                <div class="actions clearer" style="padding-left: 49.9062px; bottom: 30px;">

                    
                                                    <button type="button" title="In winkelwagen" class="button btn-cart" onclick="setLocation('https://www.professionele-koeling.nl/checkout/cart/add/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/product/212/form_key/SiBQpy2rW3vTJnQQ/')"><span><span>In winkelwagen</span></span></button>
                        
                                        
                                    </div> <!-- end: actions -->
            </li>

--- ФАЙЛ: pagination.html ---
<div class="toolbar-bottom">
            <div class="toolbar">

		<div class="sorter">
	
		<p class="amount">
							Artikelen 1 tot 36 van 429 in totaal					</p>
		
		<div class="sort-by">
			<label>Sorteer op</label>
			<select onchange="setLocation(this.value)">
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=asc&amp;order=position">
					Positie				</option>
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=asc&amp;order=name">
					Naam				</option>
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=asc&amp;order=price" selected="selected">
					Prijs				</option>
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=asc&amp;order=vermogen">
					Vermogen				</option>
						</select>
							<a class="category-asc ic ic-arrow-down" href="https://www.professionele-koeling.nl/koelkasten-kisten.html?dir=desc&amp;order=price" title="Van hoog naar laag sorteren"></a>
					</div>
		
		<div class="limiter">
			<label>Toon</label>
			<select onchange="setLocation(this.value)">
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?limit=12">
					12				</option>
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?limit=24">
					24				</option>
							<option value="https://www.professionele-koeling.nl/koelkasten-kisten.html?limit=36" selected="selected">
					36				</option>
						</select><span class="per-page"> per pagina</span>
		</div>
		
				<p class="view-mode">
										<label>Tonen als:</label>
								<span title="Foto-tabel" class="grid ic ic-grid"></span><a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?mode=list" title="Lijst" class="list ic ic-list"></a>					</p>
				
	</div> <!-- end: sorter -->
		
			<div class="pager">
		<div class="pages">
        <strong>Pagina:</strong>
        <ol>
        
        
        
                                    <li class="current">1</li>
                                                <li><a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=2">2</a></li>
                                                <li><a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=3">3</a></li>
                                                <li><a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=4">4</a></li>
                                                <li><a href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=5">5</a></li>
                    

        
        
                    <li class="next">
                <a class="next ic ic-right" href="https://www.professionele-koeling.nl/koelkasten-kisten.html?p=2" title="Volgende"></a>
            </li>
                </ol>

    </div>	</div>
		
</div>
        </div>

--- ФАЙЛ: product-page.html ---
<div class="breadcrumbs">
    <ul>
                                    <li class="home" itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb">
                    <a href="https://www.professionele-koeling.nl/" title="Ga naar Home" itemprop="url"><span itemprop="title">Home</span></a>
            
                                <span class="sep"></span>
                                
                </li>
                                    <li class="category3" itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb">
                    <a href="https://www.professionele-koeling.nl/koelkasten-kisten.html" title="" itemprop="url"><span itemprop="title">Koelkasten&amp;Kisten</span></a>
            
                                <span class="sep"></span>
                                
                </li>
                                    <li class="product">
                    <span class="last-crumb">Polar GE579</span>
            
                                
                </li>
            </ul>
</div>


<div class="product-name">
				<h1 itemprop="name">Polar GE579</h1>
			</div>

<div class="short-description"><div class="std" itemprop="description"><p>De Polar GE579 is een zwarte minibar koelkast met <br>29 liter inhoud voor gebruik in hotelkamers, B&amp;B's of ver-<br>gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken.</p><br>
<h4 style="color: blue;"><span style="background-color: yellow;">Advies nodig, of meerdere stuks tegen de scherpste prijs?<br>Bel onze specialisten: <strong>036 5363782</strong></span></h4><br>
<p>&nbsp;</p></div></div>


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

--- ФАЙЛ: proxies.txt ---


--- ФАЙЛ: traceback.txt ---


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
from app.scraper import scrape_data
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

# ... (обрезано, всего 217 строк) ...

--- app/playwright_engine.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Playwright Engine.

Централизованный слой браузерной автоматизации фреймворка для всех
JavaScript-зависимых сайтов (см. `framework/ROADMAP.md`, Milestone 4).

Playwright Engine — единственная точка, через которую скрапер-модули
должны запускать браузер, открывать страницы и получать их содержимое.
Он НЕ содержит собственной логики куки/прокси/задержек/идентичности —
вся эта логика уже инкапсулирована в существующих менеджерах и
применяется автоматически, аналогично тому, как Requests Engine
использует Session Manager для HTTP-запросов:

    Playwright Engine
            │
            ▼
    app/browser.py (get_browser_context)  ──────────────────┐
            │                                                │
     ┌──────┼─────────┬─────────┬─────────┐                  │
     ▼      ▼          ▼         ▼         ▼                 ▼
    Request Cookie    Proxy    Delay   Configuration     (Retry остаётся
    Profile Manager   Manager  Manager Manager           централизованным,
    Manager                                               см. ниже)

Playwright Engine:

* делегирует запуск браузера и создание контекста функции
  `app.browser.get_browser_context()` — единственному месту, где
  реально вызывается `playwright.chromium.launch()` / `browser.new_context()`,
  чтобы не дублировать эту логику (см. `app/browser.py`);
* автоматически применяет идентичность клиента через Request Profile
  Manager (`app/request_profile.py`), куки — через Cookie Manager
  (`app/cookie_manager.py`), прокси — через Proxy Manager
  (`app/proxy_manager.py`) — вызывающий код ничего не настраивает вручную;
* делает паузу перед каждой навигацией через `SessionManager.wait_before_request()`
  (Delay Manager) — как и Requests Engine, не реализует собственную политику пауз;
* сообщает Proxy Manager об успехе/сбое каждой навигации
  (`ProxyManager.report_proxy_success()`/`report_proxy_failure()`), что
  прозрачно питает Proxy Health Check/Rotation/Sticky Sessions, если
  движку передан `session_id` — идентично Requests Engine;
* НЕ реализует собственный цикл повторов при навигации — как и Requests
  Engine, Playwright Engine оставляет retry-политику централизованной
  (вызывающий код может обернуть `goto()` в `RetryManager.call_with_retry()`
  при необходимости — сам движок только сообщает об исходе через Proxy Manager);
* оборачивает все ожидаемые сбои Playwright (таймаут, навигация, отсутствие
  селектора, ошибка запуска браузера, падение страницы) в единое понятное
  исключение `PlaywrightEngineError` — вызывающему коду не нужно знать о
  внутренних исключениях Playwright;
* использует централизованную функцию логирования `app.utils.log_message`
  для запуска/закрытия браузера, навигации и ошибок (без избыточного лога).

Playwright Engine НЕ парсит HTML (это Milestone 5 — Parsing), НЕ
экспортирует данные, НЕ содержит селекторов конкретных сайтов, НЕ
реализует пагинацию/infinite scroll/логин — эти возможности будут
реализованы отдельными задачами (см. `tasks/TASK.md`, раздел Scope) на
основе этого движка.
"""

from pathlib import Path
from typing import Any, List, Optional

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from app import config
from app.browser import get_browser_context
from app.cookie_manager import CookieManager
from app.proxy_manager import ProxyManager
from app.request_profile import RequestProfile, RequestProfileManager
from app.session_manager import SessionManager
from app.utils import log_message

# ... (обрезано, всего 419 строк) ...

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

# ... (обрезано, всего 129 строк) ...

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

# Папка для скачанных изображений
IMAGE_DIR = OUTPUT_DIR / "images"

# Гарантируем, что рабочие папки проекта существуют
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 2. НАСТРОЙКИ ЗАПУСКА, ТАЙМАУТЫ И ПОВТОРЫ

# ... (обрезано, всего 698 строк) ...

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


# ... (обрезано, всего 802 строк) ...

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
