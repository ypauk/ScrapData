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

## 1. Краткое описание задачи


Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает данные о товарах из категории холодильного оборудования и сохраняет результат в **JSON**.


На текущем этапе требуется собрать **только 2 товара** и передать тестовый результат клиенту перед полноценным scraping. При этом структура результата уже полностью определена в `DS-PRK-Scraper.json` и должна соблюдаться буквально: порядок и названия полей менять нельзя.


Также требуется **скачивать изображения**, а не только сохранять их URL. Обычная цена и цена со скидкой должны попадать в разные поля; если скидки нет — `Sale price` оставляется пустым. Отсутствующие характеристики также остаются пустыми. Описание сохраняется как **чистый текст**, без HTML.


По предоставленным материалам видно, что категория содержит 429 товаров и использует обычную постраничную навигацию по 36 товаров на страницу. Professionele Koeling


**Уверенность: высокая.**



## 2. Какой конечный результат нужен


Основной результат:



- **JSON**

- строго в структуре `DS-PRK-Scraper.json`;

- один товар — одна JSON-запись;

- каждый требуемый атрибут — отдельное поле;

- порядок полей сохраняется согласно спецификации;

- `imageurl` — URL изображений;

- `image_name` — имена соответствующих скачанных изображений;

- `Specs` — характеристики согласно инструкции в спецификации;

- `Spec_detail` — характеристики, где текст до `:` используется как название характеристики;

- отсутствующие значения — пустые;

- HTML из описаний не сохраняется.


На первом этапе — **2 товара**.



## 3. Как лучше решить задачу


### Рекомендация: PlaywrightEngine + HTML parsing


Оптимальный вариант — использовать уже предусмотренный проектом **PlaywrightEngine** для получения отрендеренной страницы, а затем разбирать полученный HTML.


Причины:



- В `notes.txt` прямо указано, что сайт работает с JavaScript.

- В инструкции проекта зафиксировано, что `scraper.py` получает готовый `PlaywrightEngine`, поэтому переходить на `requests` как основной механизм нельзя.

- Предоставленный HTML уже показывает, что необходимые данные находятся непосредственно в DOM: URL товара, название, цены и изображения доступны в карточке товара.

- Страница категории содержит полноценную pagination, поэтому обход страниц можно выполнять через URL вида `?p=2`, `?p=3` и т. д. Professionele Koeling

- Для полей `Description`, `Short description` и характеристик потребуется посещение product page, поскольку в карточке категории этих данных нет.


### Рекомендуемый workflow


**Категория → ссылки товаров → product pages → извлечение полей → скачивание изображений → JSON.**


Для теста достаточно обработать первые 2 товара.


**Уверенность: высокая** относительно общего подхода; точные CSS/XPath-селекторы необходимо валидировать на нескольких товарах перед полной обработкой.



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Не рекомендую как основной способ получения страниц.


Сайт явно сообщает, что JavaScript необходим для полной функциональности, а исходные материалы проекта также указывают на JS-сайт. Professionele Koeling


При этом BeautifulSoup вполне подходит **для разбора уже полученного HTML**, но не как замена браузерному движку.


### Selenium


Работоспособен, но здесь избыточен. Проект уже зафиксирован на PlaywrightEngine, поэтому добавление Selenium только усложнит решение.


### Scrapy


Для 429 товаров Scrapy технически подходит, но не дает преимущества, достаточного для оправдания смены предусмотренного проектом browser engine. Это увеличит сложность интеграции.


### Прямой API


Не рекомендуется. В предоставленных материалах указано `API нет`, а `network.har` пуст. Доступного API, на который можно надежно опереться, не обнаружено.


### GraphQL


Признаков GraphQL нет.


### Только category pages


Недостаточно. Категория дает название, URL, изображение и цены, но спецификация требует значительно больше данных — description, short description и характеристики. Поэтому для полного результата нужны product pages.



## 5. Анализ сайта


КомпонентРезультатУверенностьJavaScript Rendering**Да / вероятно требуется**ВысокаяReactНе обнаруженСредняяVueНе обнаруженСредняяAngularНе обнаруженСредняяAPIНе обнаруженВысокаяGraphQLНе обнаруженВысокаяInfinite Scroll**Нет признаков**ВысокаяPagination**Да**ВысокаяLoginЕсть функция входа, для scraping не требуетсяВысокаяCookies**Да**ВысокаяJWTНе обнаруженВысокаяBearer TokenНе обнаруженВысокаяCAPTCHAНе подтвержденаСредняяCloudflare**Да, признаки подтверждены cookies cf_clearance**ВысокаяRate LimitsНеизвестноНизкаяDownload FilesТребуется для изображенийВысокаяUpload FilesНе требуетсяВысокаяLazy LoadingНе подтвержденоСредняяWebSocketНе обнаруженСредняяXHR/Fetch APIНе исследован из-за отсутствия HARНизкаяSitemapНа странице присутствует ссылка Sitemap, но `sitemap.xml` напрямую сейчас не удалось получитьСредняяrobots.txtПри проверке сейчас не удалось получить содержимоеНизкая
Живой category page подтверждает наличие 429 товаров, 36 товаров на странице и pagination. Также карточки содержат ссылки на product pages, названия и цены. Professionele Koeling


В предоставленном `cookies.json` действительно есть `cf_clearance`, а также cookies Magento/frontend. Это сильный признак использования Cloudflare перед сайтом.


Важно: наличие `cf_clearance` **не означает автоматически, что scraper будет заблокирован**. Но Cloudflare нужно считать одним из основных эксплуатационных рисков.



## 6. Что необходимо собрать до начала разработки


Для **самого начала разработки критически необходимой дополнительной информации почти нет**.


Уже предоставлены:



- `description.txt`;

- окончательная `DS-PRK-Scraper.json`;

- `category-page.html`;

- `page.html`;

- `product-page.html`;

- `pagination.html`;

- `cookies.json`;

- `headers.json`;

- `network.har`;

- `notes.txt`;

- `checkpoint.json`.


Особенно важно, что `DS-PRK-Scraper.json` объявлен авторитетной спецификацией. Его нельзя реконструировать или менять.


### Однако желательно получить



- **Точный ожидаемый JSON для двух тестовых товаров**, если у клиента есть пример финального файла.

- Уточнить, **куда должны сохраняться скачанные изображения** и как именно должен выглядеть `image_name`.

- Если `Specs` должен содержать URL screenshot, нужно подтвердить, что это именно ссылка на внешний screenshot, а не сами характеристики.


Последний пункт особенно важен: в спецификации:



`"Specs": "... each own colom"`



и



`"Spec_detail": "evertything before the : is the header"`



Это инструкции по заполнению, а не реальные значения. Само содержимое таблицы характеристик в предоставленных данных отсутствует.



## 7. Возможные сложности


### 1. Cloudflare


Наиболее существенный риск.


В cookies присутствует `cf_clearance`, поэтому автоматические запросы могут периодически сталкиваться с защитой.


**Риск: средний.**


### 2. JavaScript


Сайт требует/использует JavaScript, поэтому browser-based подход оправдан. Professionele Koeling


**Риск: средний.**


### 3. Изображения


Нужно не просто получить URL, а скачать изображения и согласованно записать URL/имя файла в JSON.


Нужно проверить:



- сколько изображений находится на product page;

- есть ли thumbnails и оригиналы;

- одинаково ли устроены страницы разных товаров.


**Риск: средний.**


### 4. Структура характеристик


Это наиболее существенный вопрос по данным.


В текущем сокращённом `product-page.html` характеристики не представлены. Поэтому невозможно со 100% уверенностью определить источник всех полей `Specs` и `Spec_detail`.


**Риск: средний / высокая вероятность уточнения структуры.**


### 5. Изменение HTML


Сайт выглядит как классический Magento-подобный storefront. Селекторы могут измениться при редизайне.


**Риск: средний в долгосрочной перспективе.**


### 6. 429 товаров


Сейчас категория содержит 429 товаров, при 36 товарах на страницу. Это около 12 страниц. Professionele Koeling


Для теста это практически не проблема, но при полном scraping потребуется аккуратно обрабатывать pagination и повторные попытки.



## 8. Что нужно уточнить у клиента


Перед написанием scraper я бы задал клиенту следующие вопросы:



- **Для поля Specs: где находится полный список характеристик, который соответствует этому полю?** В предоставленном `product-page.html` эта часть страницы отсутствует.

- **Что именно должно находиться в image_name?** Только имя файла (`polar_ge579_1.jpg`) или путь относительно output directory?

- **Нужно ли сохранять все изображения товара или только изображения из основной галереи?**

- **Как должен выглядеть JSON для нескольких товаров:** массив объектов или отдельный JSON-объект/файл на каждый товар?

- **Куда должны сохраняться скачанные изображения относительно JSON?**


При этом **не нужно спрашивать клиента о структуре колонок** — она уже окончательно задана `DS-PRK-Scraper.json`.



## 9. Рекомендуемый стек технологий


Только основные технологии:



- **Python**

- **Playwright / предоставленный PlaywrightEngine**

- **BeautifulSoup**

- **JSON**

- файловая система Python для сохранения изображений


Отдельный API или Selenium не нужны.



## 10. План разработки


### Этап 1 — проверка доступа к сайту


**Цель:** убедиться, что PlaywrightEngine стабильно открывает category и product pages.


**Ожидаемый результат:** успешно получен DOM первой страницы категории и двух product pages.


**Зависимости:** PlaywrightEngine, доступ к сайту.



### Этап 2 — получение двух товаров


**Цель:** извлечь первые 2 product URLs из категории.


**Ожидаемый результат:** два корректных URL товаров.


**Зависимости:** этап 1.



### Этап 3 — сбор данных product pages


**Цель:** получить все поля, предусмотренные `DS-PRK-Scraper.json`.


**Ожидаемый результат:** две записи с корректными названиями полей и пустыми значениями там, где данных нет.


**Зависимости:** product pages, подтверждённая структура `Specs`.



### Этап 4 — обработка изображений


**Цель:** скачать требуемые изображения и сопоставить их с `imageurl` / `image_name`.


**Ожидаемый результат:** локально сохранённые изображения и корректные ссылки/имена в JSON.


**Зависимости:** успешное извлечение image URLs.



### Этап 5 — формирование тестового JSON


**Цель:** сформировать файл строго по `DS-PRK-Scraper.json`.


**Ожидаемый результат:** JSON с 2 товарами, без смешивания нескольких значений в неправильных колонках.


**Зависимости:** этапы 2–4.



### Этап 6 — валидация


**Цель:** проверить структуру и качество тестовых данных.


**Ожидаемый результат:** клиент получает тестовый файл с 2 товарами.


**Зависимости:** готовый JSON.



### Этап 7 — полный scraping


**Цель:** после подтверждения теста обработать остальные страницы категории.


**Ожидаемый результат:** полный JSON со всеми требуемыми товарами.


**Зависимости:** подтверждение клиентом тестового результата.



## 11. Оценка сложности


ПоказательОценкаСложность**4/10**Разработка тестовой версии**2–4 часа**Полная разработка scraper**4–7 часов**Вероятность блокировок**Средняя**Вероятность необходимости браузера**Высокая — ~90%**Вероятность изменения сайта в будущем**Средняя**Общий риск**Средний**
Оценка предполагает, что доступ к двум тестовым product pages стабилен и `Specs` действительно можно извлечь из DOM без дополнительного источника данных.



## 12. Можно ли решить проще


**Да.**


Самое простое решение в рамках ограничений проекта:


**PlaywrightEngine → category HTML → product URLs → product HTML → parsing → JSON.**


Не нужно добавлять:



- API;

- базу данных;

- Scrapy;

- Selenium;

- отдельную архитектуру для очередей;

- сложную систему распределённого scraping.


Также нет необходимости открывать каждую страницу категории каким-либо сложным способом: pagination уже явно представлена ссылками `?p=2`, `?p=3` и т. д. Professionele Koeling


При этом переходить только на category pages **нельзя**, потому что полного набора требуемых данных там нет.


**Упрощение возможно именно за счёт минимального browser workflow, а не отказа от PlaywrightEngine.**



## 13. Итоговая рекомендация


Рекомендуемое решение — **Python + предоставленный PlaywrightEngine + BeautifulSoup + JSON**.


Это оптимальный вариант, потому что:



- он соответствует уже зафиксированной архитектуре проекта;

- сайт использует JavaScript;

- API не предоставлен;

- данные доступны в HTML DOM;

- pagination простая и предсказуемая;

- объём относительно небольшой — сейчас 429 товаров;

- для теста требуется всего 2 товара. Professionele Koeling


Главный технический риск — **Cloudflare**, а главный информационный пробел — точная структура источника данных для `Specs` / `Spec_detail`.


### Можно ли уже писать код?


**Почти да, но перед реализацией желательно получить ответы на 2 критичных вопроса:**



- точная семантика `Specs` / `Spec_detail`;

- точный формат `image_name` и способ хранения скачанных изображений.


Если эти два момента уже определены внутри существующего проекта и не требуют клиентского решения, **можно переходить к написанию кода и сначала реализовать тест только на 2 товарах**.


**Итоговая уверенность: высокая — около 85–90%.**
Неопределённость в основном связана не со способом scraping, а с отсутствующим в предоставленных материалах HTML-фрагментом характеристик и правилами именования/хранения изображений.

> **ВАЖНО:** Анализ выше мог содержать фразы вроде «переходить к написанию кода пока рано» или «нужно дождаться ответов клиента». Эти фразы относятся к моменту составления анализа и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — код писать нужно. Все данные уже предоставлены ниже.

---

## План проекта (этап 2)

Прочитал полный prompt по ссылке и выполнил задачу проектирования с учетом всех его ограничений. В частности, решение ниже **не содержит готового Python-кода**, не предлагает менять `main.py`/`config.py` и разделяет ответственность `scraper.py` и `parser.py`. Спецификация `DS-PRK-Scraper.json` рассматривается как единственный источник истины по полям и их порядку. GitHub+2GitHub+2


# Проектирование реализации


## 0. Почему выбран HTML + Playwright


### Выбор


**PlaywrightEngine + HTML + BeautifulSoup.**


API использовать не следует: в исходных материалах прямо указано, что API отсутствует, а `network.har` пуст. Кроме того, фреймворк уже жестко предоставляет `PlaywrightEngine` и ожидает от `scrape_data(engine)` список HTML-страниц. GitHub+1


### Почему нужен Playwright


Playwright нужен как транспортный и браузерный слой:



- он уже является обязательной частью архитектуры;

- сайт имеет JavaScript-зависимость;

- существующий `browser.py` уже отвечает за browser context, cookies, proxy и user-agent;

- нет необходимости самостоятельно реализовывать HTTP-клиент.


### Почему BeautifulSoup


После получения HTML браузером извлечение данных проще и надежнее делать через BeautifulSoup:



- HTML обычной ecommerce-структуры;

- карточки товаров находятся в обычных DOM-элементах;

- product page содержит обычные заголовки, описания, цены и характеристики;

- нет необходимости превращать `parser.py` в набор Playwright-операций.


### Плюсы



- соответствует существующему framework contract;

- минимум архитектуры;

- легко тестировать parser на сохраненном HTML;

- не требуется API;

- можно получать полную информацию с product pages;

- легко поддержать будущую пагинацию.


### Минусы



- зависимость от HTML-селекторов;

- возможные изменения верстки;

- Cloudflare может мешать массовому обходу;

- срок действия `cf_clearance` ограничен.


Исходные материалы подтверждают пагинацию `?p=2`, `?p=3` и т. д., а категория на момент подготовки задания показывала 429 товаров при 36 товарах на странице. GitHub



# 1. Полный поток данных


Для текущего теста требуется ровно **2 товара**.


https://www.professionele-koeling.nl/koelkasten-kisten.html        ↓PlaywrightEngine        ↓scraper.scrape_data(engine)        ↓открытие category page        ↓получение HTML листинга        ↓извлечение product URLs        ↓открытие product page #1        ↓получение HTML товара #1        ↓открытие product page #2        ↓получение HTML товара #2        ↓List[str] с HTML product pages        ↓main.py        ↓parser.parse_html_data(raw_pages_content)        ↓BeautifulSoup        ↓parse_product(html)        ↓dict с точной структурой DS-PRK-Scraper.json        ↓List[dict]        ↓exporter.py        ↓
Для production-версии после теста к этому потоку добавляется переход по `?p=2`, `?p=3` и далее.


Важный момент: `parser.py` **не импортируется scraper'ом**. Извлечение URL товаров внутри `scraper.py` допустимо, потому что это навигационная логика, необходимая для определения следующих страниц, а не извлечение бизнес-полей товара. Это прямо соответствует контракту framework. GitHub



# 2. app/scraper.py


## 2.1. Интерфейс функций


ФункцияНазначениеВходВозврат`scrape_data(engine)`Главный orchestration network layer`PlaywrightEngine``List[str]``_fetch_listing_html(engine, url)`Открыть category page и получить HTMLengine, URL`str``_fetch_product_html(engine, url)`Открыть product page и получить HTMLengine, URL`str``_extract_product_urls(html)`Найти URL товаров в HTML листингаHTML`List[str]``_get_next_page_url(html, current_url)`Найти URL следующей страницыHTML, текущий URL`str
### scrape_data(engine)


Это единственная обязательная публичная функция.


Контракт:


`engine → List[str]`


На тестовом этапе она должна вернуть HTML ровно двух product pages.


Она не должна возвращать dict, не должна вызывать parser и не должна заниматься извлечением `Title`, `Price`, `Specs` и т. п.



## 2.2. Алгоритм scrape_data


### Шаг 1


Начальный URL:


`https://www.professionele-koeling.nl/koelkasten-kisten.html`


### Шаг 2


Вызвать `_fetch_listing_html()`.


Перед обработкой необходимо дождаться наличия элемента, характерного для списка товаров.


Подтвержденный селектор из входного HTML:


ul.products-grid.category-products-grid
Карточка:


li.item
### Шаг 3


Передать HTML в `_extract_product_urls()`.


В карточке подтверждены:


h2.product-name a
и


div.product-image-wrapper a.product-image
Оба варианта содержат URL товара.


Предпочтительный источник:


h2.product-name a[href]
Для приведенного HTML это дает:


`https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html`


GitHub


### Шаг 4


Удалить дубликаты URL, сохранив исходный порядок.


### Шаг 5


На тестовом этапе взять первые **2 уникальных product URL**.


Не нужно обходить остальные карточки и страницы.


### Шаг 6


Для каждого из двух URL:



- вызвать `random_delay()` из `app.utils`;

- открыть URL через переданный `PlaywrightEngine`;

- дождаться product page;

- получить HTML;

- добавить HTML в результирующий список.


### Шаг 7


Вернуть:


[    product_html_1,    product_html_2]
Это важно: список должен содержать именно HTML, поскольку таков неизменяемый контракт `main.py`. GitHub



# 2.3. Пагинация


На текущем тесте пагинация **не нужна**, поскольку требуется только 2 товара.


Для последующего полного scrape необходимо использовать обычную URL-пагинацию:


?p=2?p=3?p=4...
В предоставленном HTML также есть явная ссылка:


a.next
с URL следующей страницы. GitHub


Поэтому предпочтительный алгоритм:



- открыть текущую страницу;

- получить HTML;

- определить product URLs;

- проверить `a.next[href]`;

- если `a.next` отсутствует — завершить пагинацию;

- иначе перейти на указанный URL;

- повторять до конца.


Не следует хардкодить количество страниц или `429`: число товаров на сайте может измениться.



# 2.4. Ожидание контента


Для category page:


ul.products-grid.category-products-grid
или наличие:


li.item
Для product page предпочтительно дождаться:


div.product-name h1
Дополнительно можно проверять наличие:


div.price-box
Но отсутствие цены **не должно автоматически считаться невалидной страницей**, поскольку клиент требует включать товары без наличия/скидки.



# 2.5. Lazy loading / scroll / tabs


По предоставленным материалам:



- infinite scroll не обнаружен;

- используется обычная pagination;

- необходимость scroll не подтверждена;

- отдельные клики для получения основных данных не подтверждены;

- product data присутствует в HTML.


Следовательно:


**не делать scroll, клики и browser automation без фактической необходимости.**


Если при тесте выяснится, что реальные изображения загружаются только после lazy-loading, это будет отдельной реализационной проверкой.



# 2.6. random_delay()


Использовать существующий `app.utils.random_delay()`:



- между переходом category → product;

- между product page #1 → product page #2;

- между последующими страницами при масштабировании.


Не создавать собственный механизм случайных пауз.



# 3. app/parser.py


## 3.1. Интерфейс функций


ФункцияНазначениеВходВозврат`parse_html_data(raw_pages_content)`Обработать весь список HTML`List[str]``List[dict]``parse_product(html)`Извлечь один полный товар`str``dict``_parse_breadcrumbs(soup)`Извлечь BreadcrumbBS4 soup`str``_parse_title(soup)`Извлечь TitleBS4 soup`str``_parse_short_description(soup)`Извлечь short descriptionBS4 soup`str``_parse_prices(soup)`Извлечь обычную и sale priceBS4 soupпара значений`_parse_description(soup)`Получить полное описание как чистый текстBS4 soup`str``_parse_images(soup)`Извлечь URL и имена изображенийBS4 soupпара значений`_parse_specs(soup)`Извлечь `Specs`BS4 soup`str``_parse_spec_detail(soup)`Разобрать характеристикиBS4 soupнабор полей/значений
При этом `parser.py` не должен выполнять никаких HTTP-запросов.



# 3.2. Главная функция parse_html_data


Алгоритм:



- получить `List[str]`;

- каждый HTML передать в `parse_product()`;

- собрать результаты в исходном порядке;

- вернуть `List[dict]`.


Если один HTML поврежден или не содержит ожидаемой структуры, ошибка одного товара не должна уничтожать остальные результаты.



# 3.3. Поля результата


Структура должна сохраняться **буквально в указанном порядке**:


URLBreadcrumbTitle Short descriptionimageurlimage_namePriceSale priceDescription SpecsSpec_detail
Нельзя:



- переименовывать поля;

- исправлять пробел в `Title `;

- исправлять пробел в `Description `;

- добавлять `currency`;

- добавлять `availability`;

- добавлять SKU как самостоятельное поле;

- объединять `Specs` и `Spec_detail`.


Это особенно важно, поскольку `DS-PRK-Scraper.json` объявлен авторитетной спецификацией. GitHub



# 3.4. URL


Источник — фактический URL product page.


Не строить URL из `Title`.


Например, из карточки:


h2.product-name a[href]
получается фактический URL:


https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html

# 3.5. Breadcrumb


В product HTML подтверждена структура:


div.breadcrumbs    ul        li.home        li.category3        li.product
В примере:


HomeKoelkasten&KistenPolar GE579
Но спецификация требует поле `Breadcrumb`, а пример `DS-PRK-Scraper.json` показывает:


"Breadcrumb": "Home"
Поэтому здесь нельзя самостоятельно выбирать другой формат.


**Рекомендуемое правило:** сохранять именно значение/формат, подтвержденный `DS-PRK-Scraper.json`, то есть `Home`, а не собирать произвольную строку из всех breadcrumb items.



# 3.6. Title


Источник:


div.product-name h1
Например:


Polar GE579
Лишние пробелы по краям удаляются.


Имя ключа остается:


Title 

# 3.7. Short description


Источник:


div.short-description
Внутри:


div.std
Нужно получить текст из содержательного описания.


При этом служебный рекламный блок:


Advies nodig, of meerdere stuks tegen de scherpste prijs?Bel onze specialisten:036 5363782
не следует смешивать с short description, **если в реальной странице он находится внутри того же блока как отдельный promotional element**.


Это место требует проверки на полном HTML, поскольку предоставленный prompt содержит только сжатый фрагмент.



# 3.8. imageurl


Необходимо собрать URL всех изображений товара.


Если одно изображение:


URL
Если несколько:


URL1, URL2, URL3
Именно запятая является разделителем согласно спецификации. GitHub


Источники следует искать в реальных image/gallery elements product page.


Не следует автоматически брать thumbnail из категории, если product page содержит оригинальные изображения.



# 3.9. image_name


Для каждого URL определить имя файла.


Например:


polar_dm071_glasdeurkoelkast_46_liter.jpg
Для нескольких:


image1.jpg, image2.jpg, image3.jpg
Порядок должен соответствовать `imageurl`.



# 3.10. Физическое скачивание изображений


Это единственный архитектурный момент, который требует особого внимания.


Клиент требует **не только URL, но и физически скачанные изображения**. GitHub


При этом:



- `parser.py` не имеет права делать network requests;

- `main.py`, `config.py`, `exporter.py` менять нельзя;

- `scrape_data()` возвращает только `List[str]`.


Следовательно, скачивание изображений должно происходить на стороне `scraper.py` как часть network collection.


### Рекомендуемая схема


scraper  ↓product HTML  ↓извлечение image URLs для навигационной/сетевой операции  ↓download image files  ↓сохранение файлов в существующий OUTPUT_DIR  ↓возврат product HTML
`parser.py` при этом только извлекает `imageurl` и `image_name` из уже полученного HTML.


**ПРЕДПОЛОЖЕНИЕ:** `scraper.py` имеет право использовать `OUTPUT_DIR` из `config.py` для сохранения бинарных файлов. Это необходимо для выполнения клиентского требования без изменения core API. Если существующий `PlaywrightEngine` уже предоставляет механизм download файлов, следует использовать его вместо создания собственного HTTP-клиента.


Не следует добавлять отдельный `requests/httpx` downloader: framework запрещает менять транспортный слой и требует использовать предоставленный `PlaywrightEngine`. GitHub



# 3.11. Price


В category/product HTML подтверждена структура:


div.price-box    p.old-price        span.price
и:


p.special-price    span.price
Для товара с акцией:


Price = old-priceSale price = special-price
Например в предоставленном HTML:


Price = 255.99Sale price = 229.00
`app.utils.clean_price()` необходимо использовать вместо создания собственного price cleaner.



# 3.12. Sale price


Правило клиента:



- есть скидка → значение sale price;

- скидки нет → `""`.


**Не копировать Price в Sale price.**


Если `special-price` отсутствует, вернуть пустую строку.



# 3.13. Description


Источник — полный description block product page.


Не сохранять HTML.


Необходимо:



- удалить HTML-теги;

- сохранить текст;

- сохранить логические переносы;

- сохранить содержимое `<li>`;

- сохранить пары `ключ: значение`;

- убрать декоративные элементы;

- нормализовать лишние пробелы;

- не уничтожать значения характеристик.


Особенно важно не использовать просто грубый `get_text(strip=True)`, который может слить:


Artikelnummer: GE579Inhoud: 29 literTemperatuurbereik: ...
в одну строку.


Нужна нормализация whitespace с сохранением логических блоков.



# 3.14. Specs


Поле `Specs` в исходной спецификации содержит специальную инструкцию:



`if multipli seperated by comma`



Следовательно, если `Specs` представлен несколькими значениями, они должны сохраняться через запятую.


Но **не следует придумывать новые значения или преобразовывать Specs в словарь**.



# 3.15. Spec_detail


Это наиболее важная часть parser.


Правило из спецификации:



`evertything before the : is the header`



То есть строка:


Artikelnummer: GE579
преобразуется логически в:


header = Artikelnummervalue = GE579
А:


Inhoud: 29 liter
→


header = Inhoudvalue = 29 liter
### Обработка


Для каждой характеристики:



- найти первое `:`;

- часть слева — имя поля;

- часть справа — значение;

- trim обеих частей;

- сохранить исходное значение;

- если поле отсутствует — оставить пустым.


### Важный случай


У GE579 несколько строк:


Temperatuurbereik: 3-5°C ...Temperatuurbereik: 5-8°C ...Temperatuurbereik: 8-12°C ...
Нельзя молча перезаписать первое значение последним.


**ПРЕДПОЛОЖЕНИЕ:** если спецификация не предусматривает повторяющиеся header как отдельные колонки, одинаковые headers следует объединять через запятую в одном поле, сохраняя порядок появления.


Это предположение нужно проверить по реальному `DS-PRK-Scraper.json`/ожидаемому тестовому результату, потому что приведенный пример спецификации не содержит конкретного повторяющегося header.



# 3.16. Финальная структура одного объекта


Именно такая структура, без дополнительных ключей:


JSON{  "URL": "https://www.professionele-koeling.nl/koelkasten-kisten/polar-ge579.html",  "Breadcrumb": "Home",  "Title ": "Polar GE579",  "Short description": "De Polar GE579 is een zwarte minibar koelkast met 29 liter inhoud voor gebruik in hotelkamers, B&B's of vergaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken.",  "imageurl": "image-url-1, image-url-2",  "image_name": "image-1.jpg, image-2.jpg",  "Price": 255.99,  "Sale price": 229.0,  "Description ": "Полный текст описания без HTML...",  "Specs": "значение 1, значение 2",  "Spec_detail": "структура согласно правилам DS-PRK-Scraper.json"}
Это **схематичный пример**, а не готовый scraped result. Поля `Specs` и `Spec_detail` нельзя заполнять выдуманными значениями.



# 4. Обработка ошибок


СценарийДействиеTimeout categoryПовторить до **3 попыток**, между попытками использовать `random_delay()`; после неудачи записать ошибку и остановить текущий scrapeTimeout productДо **3 попыток**; после неудачи залогировать URL и пропустить товарHTTP 403Логировать и остановить scrape, не пытаться агрессивно повторятьCloudflare challengeЛогировать и остановить scrape для ручного вмешательстваCAPTCHAЛогировать и остановить scrapeProduct selector отсутствуетЛогировать проблему; не падать всем процессомPrice отсутствует`Price`/`Sale price` оставить согласно спецификации, при отсутствии sale — `""`Image отсутствует`imageurl`/`image_name` оставить пустымиХарактеристика отсутствуетСоответствующее поле оставить пустымBroken HTMLBS4 попытаться обработать; если товар невозможно идентифицировать — пропуститьПустой listingЛогировать и завершить пагинациюНет `next`Нормальное завершение пагинацииДубликат URLНе обрабатывать повторноНе удалось скачать изображениеЗалогировать URL, не удалять сам товар из JSONЧастично сломанный product pageСохранить доступные поля, отсутствующие оставить пустыми
Особенно важно: отсутствие одного поля не должно приводить к потере всего товара.



# 5. Риски



- **Cloudflare** — существенный риск, особенно при масштабировании.

- **Login** — не требуется; product pages доступны без авторизации по предоставленным данным.

- **Rate limiting** — точный лимит неизвестен.

- **CAPTCHA** — присутствует на review form, но не относится к scraping товаров.

- **Infinite Scroll** — не обнаружен.

- **Shadow DOM** — признаков нет.

- **iframe** — для необходимых данных не обнаружен.

- **WebSocket** — признаков нет.

- **GraphQL API** — признаков нет.

- **Изменение DOM** — средний риск.

- **Lazy-loaded images** — не подтверждены, требуют проверки на реальной странице.

- **Повторяющиеся Spec_detail headers** — требуют аккуратной обработки.

- **Физическое сохранение изображений** — требует согласования с текущим механизмом файлового вывода core.


Cloudflare особенно важен: во входных данных присутствует `cf_clearance`, а значит защита действительно была активна во время получения материалов. GitHub



# 6. Что остается неизвестным


Несмотря на то что данных достаточно для реализации теста, несколько деталей нельзя честно утверждать без дополнительной проверки:



- **Полная структура image gallery** product page — предоставленный HTML обрезан до price block.

- **Точный DOM блока Specs** — в сжатом HTML его содержимое отсутствует.

- **Точный DOM всех Spec_detail** — правило известно, но полный HTML блока не показан.

- **Точный механизм физического image download в существующем PlaywrightEngine**.

- **Lazy-loading изображений** — в исходных материалах не подтвержден.

- **Поведение повторяющихся Spec_detail headers** — например нескольких `Temperatuurbereik`.

- **Точное количество страниц при будущем полном scrape** — нельзя хардкодить 12 страниц только на основании текущих 429/36.

- **Актуальность предоставленного cf_clearance** — cookies имеют ограниченный срок жизни.


При этом отсутствие HAR и API не является блокирующим фактором: исходные материалы уже показывают HTML-структуру category/product pages и контракт framework. GitHub+1



# 7. Порядок реализации


### 1. parser.py


Сначала реализовать parser, потому что он полностью работает in-memory и не зависит от сети.


Тестировать на сохраненных HTML из `AI_INPUT`.


Минимальный тестовый набор:



- GE579;

- DM071;

- товар со скидкой;

- товар без скидки;

- несколько изображений;

- отсутствие изображения;

- повторяющийся `Spec_detail`;

- отсутствующая характеристика.


### 2. scraper.py


После стабилизации parser реализовать:



- category navigation;

- extraction product URLs;

- ограничение до 2 товаров;

- product navigation;

- retries;

- `random_delay()`;

- image downloading;

- возврат `List[str]`.


### 3. Интеграция


`main.py` **не изменять**.


Проверить только соответствие существующему контракту:


scrape_data(engine) → List[str]parse_html_data(List[str]) → List[dict]exporter.save_to_json(...)
### 4. Тесты


Проверить:



- ровно 2 товара;

- JSON валиден;

- нет лишних ключей;

- нет пропущенных ключей;

- порядок ключей соответствует спецификации;

- sale price пуст при отсутствии скидки;

- описание не содержит HTML;

- повторяющиеся характеристики не теряются;

- изображения скачиваются;

- `imageurl` и `image_name` имеют одинаковое количество элементов.


### 5. Только после этого — масштабирование


Перейти от:


2 products
к:


all category pages
с pagination, retry и контролем Cloudflare.



# 8. Краткое резюме


**Технология:** существующий `PlaywrightEngine` для navigation/network + BeautifulSoup для parsing HTML.


**scraper.py:**



- `scrape_data(engine)`

- `_fetch_listing_html()`

- `_fetch_product_html()`

- `_extract_product_urls()`

- `_get_next_page_url()`


**parser.py:**



- `parse_html_data()`

- `parse_product()`

- специализированные функции для breadcrumb, title, description, prices, images и specifications.


**Итог:** на тестовом запуске scraper получает category page, берет первые 2 уникальных product URL, открывает две product pages и возвращает их HTML. Parser преобразует их в `List[dict]` со **строго 11 полями из DS-PRK-Scraper.json и в том же порядке**. GitHub


**Главные риски:** Cloudflare/rate limiting, изменение DOM, неизвестная полная структура image gallery/specification blocks и необходимость физического сохранения изображений при неизменном core API.


**Критически важно:** я бы **не начинал с изменения scraper под весь каталог**. Сначала реализовать и проверить ровно 2 товара. После подтверждения JSON — включать пагинацию и масштабирование. Это соответствует исходному требованию клиента и архитектурному контракту проекта. GitHub+1

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
