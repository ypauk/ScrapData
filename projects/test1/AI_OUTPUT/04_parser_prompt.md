# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/parser.py`.

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

Редактировать
1. Краткое описание задачи

Клиенту нужен Python-скрейпер для сайта professionele-koeling.nl, который собирает данные о товарах из категории холодильного оборудования.

На текущем этапе требуется только тестовая выгрузка 2 товаров. После проверки клиентом предполагается полноценный scrape.

Ключевые требования:

использовать DS-PRK-Scraper.json как окончательную и авторитетную спецификацию полей;

строго сохранить заданные названия и порядок колонок;

итоговый формат — JSON;

каждый атрибут должен находиться в отдельном поле;

отсутствующие характеристики оставлять пустыми;

если скидки нет — Sale price оставлять пустым;

описание сохранять как чистый текст, без HTML;

товары без наличия также включать;

изображения необходимо скачивать, а не только сохранять URL;

сначала отдать клиенту файл с 2 товарами. 

Уровень уверенности: высокий — требования явно указаны в предоставленном prompt.

2. Какой конечный результат нужен

Основной результат:

JSON-файл с 2 товарами на тестовом этапе.

Структура должна соответствовать DS-PRK-Scraper.json без самостоятельного добавления, удаления, переименования, объединения или разделения полей.

В спецификации присутствуют, в частности:

URL

Breadcrumb

Title

Short description

imageurl

image_name

Price

Sale price

Description

Specs

Spec_detail

При этом Specs и Spec_detail имеют специальные правила заполнения: для характеристик необходимо выделять название характеристики и её значение согласно инструкции спецификации.

Изображения также должны быть скачаны. Сам JSON должен содержать соответствующие значения imageurl и image_name.

Уровень уверенности: высокий. 

3. Как лучше решить задачу
Рекомендация: Playwright + HTML parsing

Оптимальный подход — использовать уже предусмотренный проектом PlaywrightEngine для получения страниц, а затем парсить полученный HTML.

Это особенно важно, потому что prompt прямо фиксирует: scraper.py получает готовый PlaywrightEngine, поэтому переход на чистый requests как замену браузеру здесь не является подходящим решением. 

Рабочая стратегия на уровне концепции:

Открыть категорию через Playwright.

Получить список товаров.

Выбрать первые 2 товара для тестовой выгрузки.

Перейти на страницы этих товаров.

Извлечь требуемые поля из DOM.

Очистить HTML из текстовых полей.

Извлечь характеристики согласно правилам Specs / Spec_detail.

Найти изображения и скачать их.

Сформировать JSON строго по заданной спецификации.

Проверить, что у каждого товара все требуемые поля присутствуют и находятся в правильной структуре.

Для текущего теста переход со страницы категории на карточки товара оправдан: предоставленный HTML категории содержит название, URL, основное изображение и цены, но полноценные Description, Specs и другие требуемые поля показаны на product page. Например, в предоставленном product HTML находятся breadcrumb, название, short description и цены. 

Уровень уверенности: высокий.

4. Почему остальные варианты хуже
requests + BeautifulSoup

Не рекомендую как основной способ получения страниц.

Причина не в том, что HTML невозможно разобрать BeautifulSoup, а в том, что проект уже построен вокруг PlaywrightEngine, а в notes прямо указано, что сайт работает с JavaScript.

Кроме того, наличие действующего cf_clearance cookie показывает, что сайт использует Cloudflare-механизм защиты. Браузерный подход здесь надежнее.

При этом BeautifulSoup-подобный HTML parsing как логический этап обработки полученного браузером HTML вполне уместен.

Scrapy

Избыточен для текущей задачи.

Сейчас нужно получить всего 2 товара для теста, а инфраструктура проекта уже предоставляет PlaywrightEngine. Добавление полноценного Scrapy-стека усложнит решение без очевидной пользы.

Selenium

Не дает существенного преимущества перед уже используемым PlaywrightEngine.

API

В предоставленных материалах указано API нет, а network.har пуст. Поэтому оснований строить решение вокруг API нет.

GraphQL

Данных о GraphQL нет. Искать и строить отдельный GraphQL-клиент без evidence из HAR/network было бы неоправданным усложнением.

Уровень уверенности: высокий, кроме внутренней реализации сайта, которую невозможно определить только по предоставленным данным. 

5. Анализ сайта
Возможность	Вывод	Уверенность
JavaScript Rendering	Да, по notes сайт обозначен как JS-сайт; Playwright уже предусмотрен проектом	Высокая
React	Не установлено	Низкая
Vue	Не установлено	Низкая
Angular	Не установлено	Низкая
API	По предоставленным данным отсутствует	Высокая
GraphQL	Не обнаружен	Средняя
Infinite Scroll	Не обнаружен; присутствует обычная pagination	Высокая
Pagination	Да — 429 товаров, 36 на странице, страницы ?p=2, ?p=3 и т. д.	Высокая
Login	Не обнаружен	Средняя
Cookies	Да	Высокая
JWT	Не обнаружен	Средняя
Bearer Token	Не обнаружен	Средняя
CAPTCHA	Не подтверждена	Средняя
Cloudflare	Да, имеются cf_clearance cookies	Высокая
Rate Limits	Явных данных нет	Низкая
Download Files	Изображения необходимо скачивать	Высокая
Upload Files	Не требуется	Высокая
Lazy Loading	Не подтверждено	Низкая
WebSocket	Не обнаружен	Средняя
XHR/Fetch	Не подтвержден	Средняя
Sitemap	В предоставленных файлах нет информации	Низкая
robots.txt	В предоставленных файлах нет информации	Низкая

Категория содержит 429 товаров, по 36 товаров на страницу. Это означает, что при переходе к полноценному scrape потребуется обработка pagination. Для текущего теста достаточно ограничиться двумя товарами. 

Важный момент: предоставленный checkpoint.json показывает предыдущую обработку 49 товаров, но exported_count в верхнем уровне равен 0, тогда как в extra_metadata указан exported_count: 49. Это внутреннее несоответствие checkpoint-файла. Для текущей задачи оно не должно влиять на тестовую выгрузку 2 товаров, но при продолжении проекта checkpoint следует трактовать осторожно. 

6. Что необходимо собрать до начала разработки

На данный момент критически необходимой дополнительной информации для начала разработки не не хватает.

Уже предоставлены:

описание задачи;

авторитетная JSON-спецификация;

category HTML;

pagination HTML;

product HTML;

cookies;

headers;

HAR;

notes;

checkpoint;

правила обработки отсутствующих данных;

требования к изображениям;

требование тестовой выгрузки 2 товаров. 

Особенно важно не запрашивать оригинальную Google Sheet: prompt прямо запрещает это и указывает, что DS-PRK-Scraper.json является её окончательной конвертированной спецификацией.

Единственный момент, который желательно подтвердить у клиента перед полноценной выгрузкой, — что именно он подразумевает под «скачать изображения»: достаточно сохранить скачанные image files рядом с JSON, либо ожидается конкретная структура хранения/архив. Но это не блокирует разработку тестового scraper, поскольку сам факт необходимости скачивания уже подтвержден.

7. Возможные сложности
1. Cloudflare

Наличие cf_clearance означает, что сайт использует Cloudflare protection.

Это потенциально самая существенная техническая проблема при масштабировании.

Существующие cookies могут перестать быть действительными, а автоматизированные запросы могут получать challenge.

2. JavaScript

Сайт отмечен как JS-based, поэтому простой HTTP-fetch может не воспроизводить поведение реального браузера.

Playwright снижает этот риск.

3. Pagination

Полный scrape — это уже не 2 товара, а до 429 товаров согласно предоставленной странице категории.

Потребуется корректно пройти все страницы и не допустить пропусков/дубликатов.

4. Различия product pages

Не следует предполагать, что у всех товаров абсолютно одинаковая структура данных.

Отдельные характеристики, изображения, скидки или описания могут отсутствовать.

По требованиям такие отсутствующие значения должны оставаться пустыми.

5. Изображения

Необходимо не только извлечь URL, но и скачать изображения. Возможны:

несколько изображений на товар;

различные размеры/версии одного изображения;

ошибки скачивания;

повторяющиеся изображения.

6. Спецификации

Поле Specs требует специального преобразования: всё до : является названием характеристики.

Нельзя просто объединять весь блок характеристик в одно текстовое поле.

7. Изменение сайта

HTML-селекторы могут измениться в будущем, особенно если сайт будет обновлен.

8. Checkpoint

Предоставленный checkpoint содержит противоречие между exported_count на верхнем уровне и внутри extra_metadata. Это нужно учитывать при возможном resume-механизме.

Уровень уверенности: высокий для перечисленных рисков; точный уровень Cloudflare/rate limiting можно окончательно оценить только во время реального запуска. 

8. Что нужно уточнить у клиента

Для тестовой выгрузки 2 товаров блокирующих вопросов нет.

Перед полноценным scrape желательно уточнить только:

В каком виде клиент хочет получить скачанные изображения относительно JSON: отдельная папка, ZIP или другая структура?

Нужно ли после успешного теста автоматически переходить к выгрузке всех 429 товаров, или сначала обязательно получить подтверждение клиента на тестовый JSON?

Какой ожидается способ передачи финального JSON и изображений, если он не определен инфраструктурой Upwork/проекта?

Важно: остальные требования уже явно определены, поэтому задавать клиенту вопросы о названиях колонок, формате JSON, пустых значениях или Google Sheet не нужно.

9. Рекомендуемый стек технологий

Python

Playwright

HTML parsing

JSON

Этого достаточно.

Не требуется добавлять API-клиент, Scrapy, Selenium или отдельную сложную инфраструктуру.

10. План разработки
Этап 1 — проверка получения страницы

Цель: убедиться, что Playwright стабильно открывает категорию и product pages.

Результат: браузерный scraper получает ожидаемый HTML.

Зависимости: доступный PlaywrightEngine.

Этап 2 — извлечение 2 товаров

Цель: получить URLs двух товаров из категории.

Результат: две корректные product pages доступны для обработки.

Зависимости: этап 1.

Этап 3 — извлечение данных товара

Цель: заполнить все поля из DS-PRK-Scraper.json.

Результат: два полностью сформированных объекта товара.

Зависимости: этап 2.

Этап 4 — обработка текста и характеристик

Цель: убрать HTML и корректно разделить спецификации.

Результат: чистые Short description, Description, Specs и Spec_detail.

Зависимости: этап 3.

Этап 5 — изображения

Цель: скачать изображения каждого товара и сформировать значения imageurl / image_name.

Результат: изображения физически сохранены, JSON содержит соответствующие данные.

Зависимости: этап 3.

Этап 6 — JSON validation

Цель: проверить соответствие результата финальной спецификации.

Результат: тестовый JSON с двумя товарами без нарушения структуры.

Зависимости: этапы 4–5.

Этап 7 — передача тестового результата

Цель: предоставить клиенту 2 товара для проверки.

Результат: клиент подтверждает соответствие.

Зависимости: этап 6.

Этап 8 — масштабирование

Цель: после подтверждения обработать всю категорию.

Результат: полноценная выгрузка всех необходимых товаров с pagination.

Зависимости: подтверждение тестового результата.

11. Оценка сложности
Параметр	Оценка
Сложность	4/10
Разработка тестовой версии (2 товара)	2–4 часа
Разработка полного scraper	5–9 часов
Вероятность блокировок	Средняя
Вероятность необходимости браузера	Высокая
Вероятность изменения сайта в будущем	Средняя
Общий риск	Средний

Основной риск — не сложность извлечения данных, а устойчивость браузерного доступа к сайту с Cloudflare.

Для тестовой версии риск значительно ниже, поскольку требуется всего 2 товара.

Оценка времени является инженерной оценкой, а не гарантированным сроком: фактическое время зависит прежде всего от поведения Cloudflare при реальном запуске.

12. Можно ли решить проще

Да, но только в пределах уже заданной архитектуры.

Самое простое решение — не строить сложный scraper framework, а использовать существующий PlaywrightEngine и максимально простой процесс:

категория → 2 product pages → извлечение данных → скачивание изображений → JSON.

Для текущего теста нет необходимости:

обходить все 429 товаров;

строить сложную систему очередей;

внедрять API;

добавлять Scrapy;

проектировать database;

создавать сложную систему распределенного scraping.

Также нет необходимости переходить на requests вместо Playwright: prompt прямо фиксирует PlaywrightEngine как часть существующего проекта.

Возможное дальнейшее упрощение после проверки структуры сайта: если выяснится, что все требуемые поля присутствуют непосредственно в category listing, можно будет не заходить на product pages. Но предоставленные сейчас HTML-данные этого не подтверждают: category page показывает только часть необходимых полей, тогда как product page содержит дополнительные данные. Поэтому на текущем этапе переход на карточку товара является наиболее надежным вариантом. 

13. Итоговая рекомендация

Рекомендуется использовать существующий PlaywrightEngine + простой HTML parsing + JSON output, без API и без дополнительного scraping-фреймворка.

Это оптимально потому что:

сайт уже обозначен как JavaScript-based;

проект уже использует PlaywrightEngine;

API/HAR не предоставляют оснований для API-based решения;

полноценные данные находятся на product pages;

требуется только 2 товара на первом этапе;

структура результата уже полностью определена DS-PRK-Scraper.json;

отсутствующие значения и правила обработки уже заданы клиентом. 

До написания кода критически важных вопросов нет. Можно переходить к реализации тестового scraper на 2 товара.

При этом перед запуском полного scrape желательно получить подтверждение клиента на тестовый JSON и уточнить только способ хранения/передачи скачанных изображений.

Итоговая стратегия: не усложнять проект, использовать предоставленный PlaywrightEngine, сначала надежно получить 2 товара и проверить соответствие JSON-спецификации, затем масштабировать тот же подход на всю pagination.

Уровень уверенности в итоговой рекомендации: высокий.

Self-check

Код не написан.

Функции и классы не проектировались.

Архитектура каталогов не создавалась.

requirements.txt не создавался.

Основная технология выбрана.

Риски перечислены.

Недостающая информация указана.

Вопросы клиенту сформированы.

Более простый вариант рассмотрен.

Переход к реализации отложен только на уровень анализа, как требовал исходный prompt.

Исходный полный prompt

> **ВАЖНО:** Анализ выше мог содержать фразы вроде «переходить к написанию кода пока рано» или «нужно дождаться ответов клиента». Эти фразы относятся к моменту составления анализа и НЕ являются инструкцией для тебя сейчас. Ты находишься на этапе генерации кода — код писать нужно. Все данные уже предоставлены ниже.

---

## План проекта (этап 2)

Редактировать
Проектирование решения
0. Выбранный способ

Основной вариант: PlaywrightEngine + HTML + BeautifulSoup.

API не выбирается: в предоставленных материалах API не обнаружен, network.har пустой. При этом сайт обозначен как JavaScript-based, а существующий framework уже фиксирует PlaywrightEngine как единственный механизм сетевого доступа. Поэтому requests/httpx добавлять не нужно и по архитектурному контракту нельзя.

HTML достаточно хорошо структурирован: листинг содержит карточки товаров, URL, названия и цены; product page содержит breadcrumb, title, short description и цены. Подробные description/specs должны извлекаться со страницы товара.

Плюсы:

полностью соответствует существующему framework;

браузер учитывает JavaScript и текущую сессию/cookies;

не требуется отдельная API-инфраструктура;

HTML можно детерминированно разбирать через BeautifulSoup;

обычная pagination через ?p=N хорошо подходит для последовательного обхода.

Минусы:

переходов будет больше, чем при чистом API;

Cloudflare может прерывать автоматизацию;

полный каталог потребует последовательного обхода product pages;

механизм непосредственного скачивания image URL нужно проверить относительно возможностей существующего PlaywrightEngine.

1. Полный поток данных

Для текущего теста нужен именно поток 2 товара:

https://www.professionele-koeling.nl/koelkasten-kisten.html

↓

PlaywrightEngine

↓

HTML страницы категории

↓

из HTML извлекаются URL первых двух product pages

↓

PlaywrightEngine открывает product page каждого товара

↓

HTML product pages

↓

main.py передаёт список HTML в parse_html_data()

↓

parser.py → BeautifulSoup

↓

dict для каждого товара

↓

list[dict]

↓

exporter.py → JSON

Параллельно на этапе scraper должны быть скачаны изображения товаров. Это остаётся сетевой обязанностью scraper.py; parser только получает из HTML URL/имена изображений и не выполняет сетевых операций. Такой раздел ответственности соответствует зафиксированному контракту проекта.

Важно: scrape_data(engine) → List[str] остаётся неизменным. В список целесообразно возвращать только HTML product pages, потому что именно они содержат все требуемые данные одного товара. Тогда parse_html_data() получает однозначный набор страниц товаров и не должен пытаться сопоставлять listing HTML с product HTML. Это соответствует описанному в prompt сценарию обхода product pages.

2. Проектирование app/scraper.py
2.1. Интерфейс функций
scrape_data(engine) → List[str]

Главная функция, обязательная существующим main.py.

Назначение:

открыть стартовую категорию;

пройти pagination;

получить URL товаров;

ограничить тестовый запуск двумя товарами;

открыть product pages;

получить HTML каждой product page;

инициировать скачивание изображений;

вернуть List[str] с HTML product pages.

Не должна:

извлекать title, price, description и specs;

формировать итоговые dictionaries;

импортировать parser;

выполнять экспорт JSON.

_fetch_listing_html(engine, url) → str

Открывает URL категории через предоставленный engine, ждёт появления товарной сетки и возвращает HTML страницы.

Ожидаемый элемент для ожидания:

ul.products-grid.category-products-grid

После загрузки достаточно получить текущий DOM/HTML.

Для первой страницы ожидается наличие:

li.item

Карточки в предоставленном HTML действительно находятся внутри li.item.

_extract_product_urls(html) → List[str]

Это допустимая логика scraper, потому что она определяет куда переходить, а не извлекает бизнес-поля товара.

Алгоритм:

найти ul.products-grid;

найти внутри li.item;

внутри карточки взять a.product-image[href];

дополнительно можно использовать h2.product-name a[href] как fallback;

нормализовать абсолютные URL;

удалить дубли;

сохранить порядок появления.

Для предоставленного HTML selector a.product-image[href] непосредственно содержит product URL.

_fetch_product_html(engine, url) → str

Открывает product URL, ждёт основной product content и возвращает HTML.

Для предоставленного примера обязательными признаками загрузившейся product page являются:

.breadcrumbs

.product-name h1

.short-description

.price-box

Product page действительно содержит эти блоки.

_get_next_page_url(html, current_url) → str | None

Определяет следующую страницу по существующей pagination.

Основной selector:

.pager .pages li.next a[href]

Fallback:

.pager .pages a[href]

с выбором ссылки, соответствующей следующей странице.

В предоставленном HTML pagination использует:

?p=2, ?p=3, ?p=4 и т. д.

Не следует строить бесконечный цикл только на увеличении p: лучше сначала проверить наличие реальной next-ссылки. Если её нет — пагинация закончена.

2.2. Алгоритм обхода
Тестовый запуск

Поскольку клиент сейчас требует ровно 2 товара, алгоритм должен завершиться сразу после получения двух уникальных product URL.

Псевдологика:

current_url = category_url
product_urls = []

пока есть current_url и количество product_urls < 2:
    listing_html = получить HTML current_url
    urls = извлечь product URLs
    добавить новые URLs
    если достигнуто 2:
        остановиться
    current_url = получить next URL

После этого:

для каждого из двух product URLs:
    сделать random_delay()
    получить product HTML
    добавить HTML в результат
    выполнить необходимое скачивание изображений

Возврат:

[product_html_1, product_html_2]
Full scrape после подтверждения теста

Ограничение 2 убирается.

Текущие предоставленные материалы показывают 429 товаров, 36 товаров на страницу и обычную pagination; следовательно, ожидается около 12 страниц категории. При full scrape нужно продолжать, пока _get_next_page_url() не вернёт None.

Lazy loading / scroll

Сейчас дополнительный scroll не нужен.

В предоставленном HTML товарные изображения уже находятся непосредственно в img[src], а pagination обычная. Lazy loading как обязательная часть сайта не подтверждён. Поэтому сначала использовать обычную загрузку страницы; scroll добавлять только если live-тест покажет, что часть карточек появляется только после прокрутки.

Tabs / «Показать ещё»

Не требуются по имеющимся материалам. Product page с необходимыми базовыми блоками уже представлена в HTML. Для specs нужно проверить полный HTML товара, поскольку сокращённый пример не содержит блока характеристик.

random_delay()

Использовать существующую функцию из app.utils, не создавать собственную.

Рекомендуемые точки:

между переходами на страницы категории;

между переходами на product pages;

перед повторным запросом после timeout;

перед продолжением после временной ошибки.

Не нужно ставить паузу между каждой внутренней операцией parser.

3. Проектирование app/parser.py

Parser работает только с уже полученным HTML и не делает никаких HTTP/network операций.

3.1. Интерфейс функций
Функция	Назначение	Входные параметры	Возвращаемое значение
parse_listing(html)	Разобрать HTML категории и извлечь карточки товаров	html: str	List[dict]
parse_single_item(card)	Разобрать одну карточку категории	card: bs4.element.Tag	dict
parse_product(html)	Извлечь полный набор данных product page	html: str	dict
parse_html_data(raw_pages)	Главная функция обработки списка HTML, вызываемая main.py	List[str]	List[dict]
_parse_breadcrumb(soup)	Извлечь breadcrumb	BeautifulSoup	str
_parse_images(soup)	Извлечь image URLs и имена	BeautifulSoup	значения для imageurl / image_name
_parse_specs(soup)	Извлечь характеристики	BeautifulSoup	значение для Specs
_parse_spec_details(soup)	Разобрать пары header: value	BeautifulSoup	значение для Spec_detail
_clean_text(node)	Удалить HTML и нормализовать текст	BS4 node/string	str

Последние функции являются внутренними helpers и не должны выполнять сетевых операций.

3.2. Извлечение полей

Ключи итогового словаря должны сохраняться буквально в соответствии с DS-PRK-Scraper.json, включая существующие пробелы в "Title " и "Description ". Нельзя самостоятельно переименовывать их в Title или Description. Спецификация прямо объявлена окончательной и запрещает добавление/удаление/переименование полей.

Порядок:

URL

Breadcrumb

Title

Short description

imageurl

image_name

Price

Sale price

Description

Specs

Spec_detail

URL

Источник:

PРЕДПОЛОЖЕНИЕ: URL берётся из текущей product page URL, но поскольку parser получает только HTML и не получает URL отдельным аргументом, точный способ передачи текущего URL в HTML неизвестен.

Это один из архитектурных моментов, который необходимо проверить до реализации.

Нельзя придумывать URL из title.

Breadcrumb

Selector:

.breadcrumbs

Внутри:

.last-crumb

Для примера результат:

Polar GE579

Если спецификация ожидает полную цепочку, нужно использовать все breadcrumb items в их исходном порядке. В предоставленном sample явно присутствуют Home → Koelkasten&Kisten → Polar GE579.

ПРЕДПОЛОЖЕНИЕ: поскольку пример authoritative JSON содержит "Breadcrumb": "Home", итоговое значение должно соответствовать точной трактовке существующей спецификации, а не автоматически расширяться до всей цепочки.

Это следует проверить на ожидаемом output.

Title

Selector:

.product-name h1

В sample:

Polar GE579.

Fallback для listing:

h2.product-name a

Short description

Selector:

.short-description .std

Извлекать только текст.

HTML-теги (p, br, h4, strong) не сохранять.

При этом рекламный блок:

Advies nodig, of meerdere stuks...

нельзя автоматически включать или исключать без явного правила спецификации.

ПРЕДПОЛОЖЕНИЕ: short description должна соответствовать основному описательному тексту товара и не должна включать служебный рекламный блок. Это необходимо подтвердить на полном HTML/ожидаемом тестовом JSON. Сам sample показывает, что такой блок находится внутри .short-description.

imageurl

Извлекать все изображения товара в порядке появления.

Для каждого изображения:

получить URL из src;

если в DOM существует более подходящий оригинальный источник изображения, его можно использовать только после проверки live HTML;

удалить дубли;

несколько URL хранить через запятую, как предписывает DS-PRK-Scraper.json.

Каталожный sample подтверждает наличие:

img[src=".../media/catalog/product/..."].

image_name

Для каждого image URL определить имя файла из последнего сегмента URL.

Например:

.../polar_dm071_glasdeurkoelkast_46_liter.jpg

→

polar_dm071_glasdeurkoelkast_46_liter.jpg

Если изображений несколько — сохранить имена в том же порядке и с тем же разделителем, что и imageurl.

Не следует генерировать новые имена без необходимости.

Price

На product page:

.price-box .old-price .price

В sample:

€ 255,99.

В category HTML аналогично используется .old-price .price.

Очистка числового значения должна использовать существующую app.utils.clean_price(), а не дублировать её в parser.

Sale price

Selector:

.price-box .special-price .price

В sample:

€ 229,00.

Если .special-price отсутствует:

пустое значение "", поскольку именно это требует клиентская спецификация. Не копировать обычную цену и не использовать её как fallback.

Description

Извлекать основной блок полного описания со страницы товара.

Не сохранять HTML-разметку.

Алгоритм:

найти основной description container
→ получить text
→ сохранить переносы между логическими блоками
→ удалить HTML tags
→ нормализовать лишние пробелы
→ сохранить текст

Критически важно не применять слишком агрессивную нормализацию: характеристики вроде

Temperatuurbereik: 3-5°C ...

должны остаться отдельными логическими строками.

Specs

Здесь есть принципиальная неопределённость.

В authoritative JSON поле записано как:

"Specs": "... each own colom"

а Spec_detail содержит инструкцию:

everything before the : is the header.

Это не следует трактовать как буквальные данные. Сам prompt специально предупреждает, что эти значения являются инструкциями по заполнению, а не повреждённым содержимым.

Поэтому:

не записывать screenshot URL как значение Specs;

не записывать строку each own colom;

не придумывать дополнительные поля.

ПРЕДПОЛОЖЕНИЕ: Specs представляет набор требуемых характеристик, а Spec_detail должен разбирать значения формата Header: Value.

Но точный физический формат этих двух полей в JSON/CSV невозможно надёжно определить только из переданного текста, потому что пример DS-PRK-Scraper.json не показывает реальные отдельные spec columns. Это нужно считать главным неизвестным.

Spec_detail

Для каждой строки характеристики:

"Artikelnummer: GE579"

разделять на:

header = "Artikelnummer"
value  = "GE579"

То есть двоеточие является разделителем, а всё до первого : — header. Это прямо задано спецификацией.

Аналогично:

"Inhoud: 29 liter"
"Temperatuurbereik: 3-5°C bij een omgevingstemperatuur van 16°C"
"Afmetingen BxDxH: 400 x 430 x 530 mm"
"Energieklasse: F"

Не следует делить значение повторно по последующим :.

Если характеристика отсутствует — соответствующее поле оставлять пустым, как требует клиент.

3.3. Финальная структура результата

С учётом запрета на изменение authoritative schema, логическая структура одного результата должна иметь именно эти поля и именно в этом порядке:

{
    "URL": "...",
    "Breadcrumb": "...",
    "Title ": "...",
    "Short description": "...",
    "imageurl": "...",
    "image_name": "...",
    "Price": ...,
    "Sale price": ...,
    "Description ": "...",
    "Specs": ...,
    "Spec_detail": ...
}

Это схема, а не готовый output товара. Конкретные значения должны быть получены scraper/parser из live HTML.

Не добавлять:

currency;

availability;

sku;

stock;

local_image_path;

любые другие поля.

Они не входят в authoritative specification.

4. Обработка ошибок
Сценарий	Действие
Timeout при загрузке listing	Повторить ограниченное число раз, например 2; между попытками использовать random_delay(). После исчерпания попыток записать ошибку через существующий logger и завершить/пропустить страницу.
Timeout product page	Повторить 2 раза; после неудачи залогировать URL и пропустить конкретный товар, не теряя остальные.
HTTP 403	Логировать; не делать агрессивные повторные запросы. При повторяющемся 403 остановить scrape.
Cloudflare challenge	Логировать и остановить автоматический обход, если существующий browser context не может пройти challenge. Не пытаться обходить защиту отдельным механизмом.
CAPTCHA	Логировать и остановить scraping для ручного вмешательства.
Нет li.item	Считать страницу пустой/невалидной, залогировать и завершить соответствующую ветку pagination.
Нет product URL	Логировать карточку и перейти к следующей.
Нет title	Вернуть пустое значение, не прерывать весь товар.
Нет price	Вернуть пустое значение согласно существующей схеме.
Нет Sale price	Вернуть "", не копировать Price.
Нет изображения	imageurl и image_name оставить пустыми.
Ошибка скачивания одного изображения	Логировать конкретный URL и продолжить остальные изображения.
Нет Specs	Оставить соответствующие значения пустыми.
Нет Spec detail	Оставить соответствующее значение пустым.
Некорректный HTML	BeautifulSoup всё равно попытаться обработать; если критический контейнер отсутствует — залогировать страницу.
Пустая category page	Логировать и завершить pagination.

JSON parsing здесь не является частью основного решения, поэтому сценарий «битый JSON» неактуален для текущего HTML pipeline.

5. Оценка рисков

Cloudflare — высокий приоритет риска. В cookies присутствует cf_clearance, что подтверждает использование Cloudflare-механизма.

Авторизация — для обычного каталога не требуется; login функционал на сайте есть, но scraper не должен его использовать без необходимости.

Rate limiting — точный лимит неизвестен; использовать random_delay() и последовательный, умеренный обход.

CAPTCHA — не подтверждена, но должна обрабатываться как стоп-условие.

Infinite Scroll — не обнаружен; используется pagination.

Shadow DOM — не обнаружен.

iframe — для требуемых данных не подтверждён.

WebSocket — не обнаружен.

GraphQL API — не обнаружен.

Изменение DOM/CSS — selectors могут измениться.

Изображения — требуется не только извлечь URL, но и физически скачать файлы.

Specs — точный формат конечного представления недостаточно определён предоставленным примером.

URL в parser — parse_product(html) не получает URL отдельным аргументом, поэтому способ надёжно получить исходный URL из одного HTML нужно подтвердить.

Полный product HTML — в prompt представлен сокращённый пример, в котором отсутствуют реальные блоки images/specs/full description.

6. Что останется неизвестным

Здесь важно не придумывать отсутствующую информацию.

1. Точный API PlaywrightEngine

В prompt подтверждено наличие PlaywrightEngine, cookies, proxy и user-agent, но не приведены конкретные методы его публичного интерфейса. Поэтому названия методов навигации/получения HTML нельзя фиксировать без просмотра app/browser.py.

2. Механизм скачивания изображений

Требование «изображения надо скачивать» однозначно, но предоставленный контракт scrape_data() → List[str] не содержит отдельного результата для скачанных файлов.

Следовательно, скачивание должно быть side effect scraper.py, а image_name parser получает из HTML/URL.

ПРЕДПОЛОЖЕНИЕ: существующий PlaywrightEngine позволяет получить binary response изображения или сохранить его локально. Это обязательно проверить до реализации.

3. Точный формат Specs / Spec_detail

Это главный неизвестный.

В prompt есть инструкции:

specs должны быть отдельными;

всё до : является header;

отсутствующие характеристики оставлять пустыми.

Но фактический пример конечных spec columns отсутствует. Поэтому нельзя честно придумать названия динамических колонок или формат JSON.

4. Полный product HTML

Дан сокращённый fragment product page. Он показывает breadcrumb, title, short description и price, но не показывает полный DOM images/specs/description.

5. Точная трактовка Breadcrumb

В sample есть полная breadcrumb chain, но authoritative JSON показывает "Home". Поэтому нельзя самостоятельно выбрать между Home и полной цепочкой без подтверждения ожидаемого output.

6. Точный источник URL

parse_product(html) получает только HTML. В HTML product page сам URL явно не показан в предоставленном fragment. Значит, либо framework добавляет его в HTML/context, либо scrape_data должен сохранять HTML с доступным canonical URL.

Это нужно проверить в реальном browser.py/main.py, но менять контракт функции нельзя.

7. Реальное количество товаров

Старый checkpoint содержит 49, а текущий анализ category page показывает 429. Поэтому checkpoint нельзя использовать как источник истины для full scrape.

7. Порядок реализации
1. parser.py

Первым реализовать parser, потому что его можно тестировать полностью офлайн на сохранённых HTML.

Последовательность:

parse_single_item();

parse_listing();

parse_product();

helpers для text/price/images/specs;

parse_html_data().

Особенно сначала нужно зафиксировать тесты на точное соответствие ключей и порядка полей.

2. scraper.py

После parser реализовать:

загрузку category;

извлечение product URLs;

pagination;

загрузку product pages;

ограничение теста двумя товарами;

image download;

timeout/retry/logging.

3. Интеграция через существующий main.py

main.py не менять.

Он должен продолжать использовать существующий контракт:

PlaywrightEngine
→ scrape_data(engine)
→ parse_html_data(raw_pages_content)
→ exporter

Это соответствует зафиксированной архитектуре проекта.

4. Тесты

Минимальный набор:

parsing category card;

parsing product title;

parsing prices;

отсутствие Sale price;

несколько images;

отсутствие images;

очистка description;

header: value для Spec_detail;

отсутствие отдельных specs;

duplicate product URLs;

pagination;

timeout/retry.

8. Итоговое резюме

Технология: PlaywrightEngine → HTML → BeautifulSoup → dict → list[dict] → exporter.

scraper.py:

scrape_data(engine)

_fetch_listing_html()

_extract_product_urls()

_fetch_product_html()

_get_next_page_url()

image download как сетевой side effect

pagination/retry/delay.

parser.py:

parse_html_data()

parse_listing()

parse_single_item()

parse_product()

helpers для breadcrumb, images, text, specs и spec details.

Итоговая структура: только 11 полей из DS-PRK-Scraper.json, без добавления новых полей; порядок и имена сохраняются буквально.

Тестовый объём: первые 2 уникальных товара.

Pagination: ?p=2, ?p=3 и далее, с остановкой по отсутствию next.

Главные риски: Cloudflare, неизвестный API конкретного PlaywrightEngine, скачивание изображений в рамках существующего контракта, неполный пример product HTML и недостаточно однозначная спецификация Specs/Spec_detail.

Критический вывод: архитектура в целом однозначна и может быть реализована без изменения main.py, browser.py, config.py, utils.py и exporter.py. Но перед написанием кода необходимо проверить две вещи: фактический интерфейс PlaywrightEngine и точный формат Specs/Spec_detail. Всё остальное достаточно определено предоставленными материалами.

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

    # Resume Support Integration с Incremental Saving (см. tasks/TASK.md,
    # "Integration with Incremental Saving"): при восстановленной сессии
    # writer'ы открываются в режиме дозаписи (append=True), чтобы уже
    # экспортированные ранее записи оставались нетронутыми — никогда не
    # перезаписываются. При отсутствии восстановления (append=False)
    # поведение полностью идентично поведению до появления Resume Support.
    with IncrementalCSVWriter("output_results.csv", append=decision.resumed) as csv_writer, \
            IncrementalJSONWriter("output_results.json", append=decision.resumed) as json_writer:

        with BatchWriter([csv_writer, json_writer]) as batch_writer:
            for idx, html in enumerate(raw_pages_content, 1):
                # Duplicate Protection (см. tasks/TASK.md, "Duplicate
                # Protection"): страницы, уже обработанные и сброшенные
                # на диск в прошлой (прерванной) сессии, пропускаются —
                # восстановленное состояние продолжает строго ПОСЛЕ
                # последнего успешно зафиксированного чекпоинта.
                if idx <= decision.start_page:
                    continue

                try:
                    page_records = parse_listing(html)
                except Exception as e:
                    log_message("error", f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
                    continue

                if not page_records:
                    continue

                batch_writer.add_records(page_records)
                processed_total += len(page_records)

                # Checkpoint Manager сам решает (на основе настроенных
                # интервалов), нужно ли реально записать чекпоинт сейчас.
                # Сбой сохранения чекпоинта НИКОГДА не должен прерывать
                # скрапинг (см. TASK.md, раздел "Error Handling") —
                # CheckpointManager сам это гарантирует, здесь только
                # защита на случай непредвиденного исключения самого вызова.
                try:
                    checkpoint.record_page(
                        page_number=idx,
                        processed_count=processed_total,
                        exported_count=batch_writer.total_flushed + decision.exported_count,
                    )
                except Exception as cp_exc:
                    if not checkpoint_failed:
                        log_message("error", f"[{__file__}] Checkpoint Manager: непредвиденная ошибка: {cp_exc}")
                        checkpoint_failed = True

        # Integration with Batch Writer (см. tasks/TASK.md, "Integration
        # with Batch Writer"): к этому моменту `with BatchWriter(...)` уже
        # завершился, и BatchWriter.close() выполнил shutdown-сброс
        # оставшихся в буфере записей (если BATCH_WRITER_FLUSH_ON_SHUTDOWN
        # включен) — весь ещё не сброшенный "хвост" гарантированно попал
        # на диск ДО финальной записи чекпоинта ниже, поэтому чекпоинт
        # никогда не укажет на страницу, чьи записи реально не сохранены.
        total_records = batch_writer.total_flushed + decision.exported_count

    checkpoint.finish(status="completed", processed_count=processed_total, exported_count=total_records)

    return total_records




def main() -> None:
    """
    Главная точка входа. Управляет жизненным циклом парсера.

    Поддерживает два режима экспорта (см. `app/config.py`,
    `EXPORT_INCREMENTAL_ENABLED`):
      - Incremental Saving + Batch Writer (по умолчанию) — каждая
        страница парсится, записи буферизуются в памяти и сбрасываются
        в CSV/JSON пачками (см. `_run_incremental()`).
      - Batch-режим (обратная совместимость) — все страницы парсятся,
        результаты копятся в памяти и экспортируются одним вызовом
        `save_to_csv`/`save_to_json` после завершения скрапинга —
        поведение, идентичное поведению проекта до появления
        Incremental Saving.
    """
    print("=" * 70)
    print(f"[{__file__}] ЗАПУСК ПАРСЕРА")
    print("=" * 70)

    try:
        # 1. Запуск браузерной автоматизации через централизованный Playwright Engine
        # (идентичность, куки и прокси применяются автоматически)
        with PlaywrightEngine() as engine:

            # 2. Сбор данных (Scraping)
            # Передаем движок в scraper.py для обхода страниц
            try:
                raw_pages_content = scrape_data(engine)
            except PlaywrightEngineError as e:
                print(f"[{__file__}] Критическая ошибка браузера: {e}")
                sys.exit(1)

            if not raw_pages_content:
                print(f"[{__file__}] Критическая ошибка: Нечего парсить (список страниц пуст).")
                sys.exit(1)

            # 3. Обработка данных (Parsing) + 4. Экспорт результатов (Export)
            if EXPORT_INCREMENTAL_ENABLED:
                print(f"[{__file__}] Incremental Saving + Batch Writer включены: обработка {len(raw_pages_content)} страниц(ы)...")
                total_records = _run_incremental(raw_pages_content)

                if total_records:
                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО (Всего записей: {total_records})")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат.")
            else:
                # Batch-режим — прежнее поведение (обратная совместимость)
                print(f"[{__file__}] Начало парсинга контента (batch-режим)...")
                scraped_results = parse_html_data(raw_pages_content)

                if scraped_results:
                    print(f"[{__file__}] Экспорт данных (Всего элементов: {len(scraped_results)})...")
                    save_to_csv(scraped_results, "output_results.csv")
                    save_to_json(scraped_results, "output_results.json")

                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат. Файлы не созданы.")

    except KeyError as ke:
        print(f"[{__file__}] Ошибка конфигурации или структуры: {ke}")
        sys.exit(1)
    except Exception as e:
        print(f"[{__file__}] Критический сбой в главном потоке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


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


class PlaywrightEngineError(Exception):
    """
    Единое исключение Playwright Engine для всех сбоев браузерной
    автоматизации (запуск браузера, навигация, таймаут, отсутствие
    селектора, выполнение JS), оставшихся после обработки движком.

    Позволяет вызывающему коду (будущим скрапер-модулям) обрабатывать
    ошибки браузера без необходимости импортировать и знать про
    исключения `playwright.sync_api`.
    """


class PlaywrightEngine:
    """
    Централизованный исполнитель браузерной автоматизации для JS-сайтов.

    Каждый инстанс управляет одним запущенным Playwright-драйвером, одним
    браузером и одним изолированным `BrowserContext`. Все компоненты слоя
    автоматизации (Configuration/Request Profile/Cookie/Proxy/Delay Manager)
    подключаются автоматически — вызывающий код не настраивает их вручную.

    Используется как контекстный менеджер (рекомендуемый способ):

        with PlaywrightEngine() as engine:
            engine.goto("https://example.com")
            html = engine.content()

    либо через явные `start()`/`close()`.
    """

    def __init__(
        self,
        profile: Optional[RequestProfile] = None,
        session_id: Optional[str] = None,
        cookies_path: Optional[Path] = None,
        headless: Optional[bool] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Args:
            profile (RequestProfile, optional): Профиль идентичности клиента
                (User-Agent, locale, timezone, viewport, Accept-Language).
                По умолчанию — `RequestProfileManager.default_profile()`.
            session_id (str, optional): Идентификатор логической сессии для
                Sticky Sessions/Proxy Rotation/Health Check
                (см. `ProxyManager.get_proxy(session_id=...)`). Если не
                передан — прокси выбирается без привязки к сессии.
            cookies_path (Path, optional): Путь к файлу куки (Cookie Manager).
                По умолчанию — `config.COOKIES_FILE`.
            headless (bool, optional): Режим headless. По умолчанию — `config.HEADLESS`.
            user_agent (str, optional): Явный User-Agent, переопределяющий профиль.
        """
        self.profile = profile
        self.session_id = session_id
        self.cookies_path = cookies_path or config.COOKIES_FILE
        self.headless = headless
        self.user_agent = user_agent

        self._playwright = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    # =====================================================================
    # ЖИЗНЕННЫЙ ЦИКЛ БРАУЗЕРА
    # =====================================================================

    def start(self) -> "PlaywrightEngine":
        """
        Запускает драйвер Playwright, браузер Chromium и создает изолированный
        контекст с автоматически примененными идентичностью/куки/прокси.

        Returns:
            PlaywrightEngine: self (для удобного чейнинга).

        Raises:
            PlaywrightEngineError: При сбое запуска браузера.
        """
        proxy_url = ProxyManager.get_proxy(session_id=self.session_id)
        proxy_kwargs = ProxyManager.to_playwright_proxy_kwargs(proxy_url) if proxy_url else None

        try:
            self._playwright = sync_playwright().start()
            self._context = get_browser_context(
                self._playwright,
                headless=self.headless,
                user_agent=self.user_agent,
                cookies_path=self.cookies_path,
                profile=self.profile,
                proxy=proxy_kwargs,
            )
        except Exception as exc:
            self._teardown_playwright()
            log_message("error", f"Не удалось запустить браузер: {exc}")
            raise PlaywrightEngineError(f"Ошибка запуска браузера: {exc}") from exc

        self._context.set_default_timeout(config.PLAYWRIGHT_TIMEOUT_MS)
        log_message("info", f"Браузер запущен (headless={self.headless if self.headless is not None else config.HEADLESS})")
        return self

    def close(self) -> None:
        """
        Сохраняет актуальные куки сессии и закрывает браузер/драйвер Playwright.

        Безопасна к повторному вызову и к вызову без предварительного `start()`.
        """
        if self._context is not None:
            try:
                self.save_cookies()
            except Exception as exc:
                log_message("error", f"Не удалось сохранить куки при закрытии: {exc}")

            try:
                browser: Optional[Browser] = self._context.browser
                self._context.close()
                if browser is not None:
                    browser.close()
            except Exception as exc:
                log_message("error", f"Ошибка при закрытии браузера: {exc}")
            finally:
                self._context = None
                self._page = None

        self._teardown_playwright()
        log_message("info", "Браузер закрыт")

    def _teardown_playwright(self) -> None:
        """Останавливает драйвер Playwright, если он был запущен."""
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
            finally:
                self._playwright = None

    def __enter__(self) -> "PlaywrightEngine":
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # =====================================================================
    # СТРАНИЦЫ И НАВИГАЦИЯ
    # =====================================================================

    @property
    def context(self) -> BrowserContext:
        """Возвращает активный `BrowserContext` (после `start()`)."""
        if self._context is None:
            raise PlaywrightEngineError("Контекст браузера не инициализирован — вызовите start() перед использованием.")
        return self._context

    @property
    def page(self) -> Page:
        """Возвращает текущую страницу, создавая её при первом обращении."""
        if self._page is None:
            self._page = self.new_page()
        return self._page

    def new_page(self) -> Page:
        """
        Создает новую страницу в текущем контексте и делает её активной.

        Returns:
            Page: Новая страница Playwright.
        """
        try:
            self._page = self.context.new_page()
        except Exception as exc:
            raise PlaywrightEngineError(f"Не удалось создать страницу: {exc}") from exc
        return self._page

    def goto(
        self,
        url: str,
        wait_until: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Открывает URL на текущей странице.

        Перед навигацией выполняется пауза согласно Delay Manager
        (`SessionManager.wait_before_request()`) — как и в Requests Engine.
        После навигации сообщает Proxy Manager об успехе/сбое.

        Args:
            url (str): Целевой URL.
            wait_until (str, optional): Условие завершения навигации
                ("load", "domcontentloaded", "networkidle", "commit").
                По умолчанию — `config.PLAYWRIGHT_WAIT_UNTIL`.
            timeout (float, optional): Таймаут навигации (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            Response Playwright (или None, если навигация не создала документ).

        Raises:
            PlaywrightEngineError: При таймауте или сбое навигации.
        """
        effective_wait_until = wait_until or config.PLAYWRIGHT_WAIT_UNTIL
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS

        SessionManager.wait_before_request()

        log_message("info", f"Навигация: {url}")
        try:
            response = self.page.goto(
                url,
                wait_until=effective_wait_until,
                timeout=effective_timeout,
            )
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Таймаут навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Таймаут при открытии {url}: {exc}") from exc
        except PlaywrightError as exc:
            log_message("error", f"Сбой навигации {url}: {exc}")
            ProxyManager.report_proxy_failure(session_id=self.session_id)
            raise PlaywrightEngineError(f"Не удалось открыть {url}: {exc}") from exc

        ProxyManager.report_proxy_success(session_id=self.session_id)
        self.update_cookies()
        return response

    def wait_for_load(self, state: str = "load", timeout: Optional[float] = None) -> None:
        """
        Ожидает завершения загрузки страницы.

        Args:
            state (str): Состояние загрузки ("load", "domcontentloaded", "networkidle").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Raises:
            PlaywrightEngineError: При таймауте ожидания.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            self.page.wait_for_load_state(state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            raise PlaywrightEngineError(f"Таймаут ожидания состояния загрузки '{state}': {exc}") from exc

    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Ожидает появления селектора на странице.

        Args:
            selector (str): CSS/text-селектор Playwright.
            state (str): Ожидаемое состояние элемента
                ("attached", "detached", "visible", "hidden").
            timeout (float, optional): Таймаут (миллисекунды).
                По умолчанию — `config.PLAYWRIGHT_TIMEOUT_MS`.

        Returns:
            ElementHandle: Найденный элемент.

        Raises:
            PlaywrightEngineError: Если селектор не появился до истечения таймаута.
        """
        effective_timeout = timeout if timeout is not None else config.PLAYWRIGHT_TIMEOUT_MS
        try:
            return self.page.wait_for_selector(selector, state=state, timeout=effective_timeout)
        except PlaywrightTimeoutError as exc:
            log_message("error", f"Селектор не найден: {selector}")
            raise PlaywrightEngineError(f"Селектор '{selector}' не появился: {exc}") from exc

    def content(self) -> str:
        """
        Возвращает полный HTML текущей страницы (без какого-либо парсинга).

        Returns:
            str: Сырой HTML страницы.

        Raises:
            PlaywrightEngineError: При сбое получения содержимого (например,
                падении страницы).
        """
        try:
            return self.page.content()
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось получить содержимое страницы: {exc}") from exc

    def evaluate(self, script: str, *args: Any) -> Any:
        """
        Выполняет JavaScript в контексте текущей страницы.

        Args:
            script (str): JS-выражение или функция (`page.evaluate()`).
            *args: Аргументы, передаваемые в скрипт.

        Returns:
            Any: Результат выполнения скрипта.

        Raises:
            PlaywrightEngineError: При сбое выполнения скрипта.
        """
        try:
            return self.page.evaluate(script, *args)
        except PlaywrightError as exc:
            raise PlaywrightEngineError(f"Не удалось выполнить JavaScript: {exc}") from exc

    # =====================================================================
    # ИНТЕГРАЦИЯ С COOKIE MANAGER
    # =====================================================================

    def update_cookies(self) -> List[dict]:
        """
        Забирает текущие куки контекста браузера и обновляет ими персистентное
        хранилище через Cookie Manager (`CookieManager.update()`), не
        затирая куки, установленные вне текущей сессии.

        Returns:
            List[dict]: Итоговый объединенный список куки.
        """
        current_cookies = self.context.cookies()
        return CookieManager.update(current_cookies, path=self.cookies_path)

    def save_cookies(self) -> None:
        """
        Полностью перезаписывает файл куки текущим состоянием контекста
        браузера (`CookieManager.save()`).
        """
        current_cookies = self.context.cookies()
        CookieManager.save(current_cookies, path=self.cookies_path)


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    with PlaywrightEngine(headless=False) as engine:
        engine.goto("https://bot.sannysoft.com/")
        engine.wait_for_load("networkidle")
        print(f"[{__file__}] Длина HTML: {len(engine.content())}")


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
    if user_agent:
        profile_kwargs["user_agent"] = user_agent

    print(f"[{__file__}] Запуск Chromium (Headless={headless})...")

    # 3. Запуск браузера с флагами против падений в Docker (централизованы в config.py)
    browser: Browser = playwright_instance.chromium.launch(
        headless=headless,
        args=BROWSER_LAUNCH_ARGS
    )

    # 4. Создание контекста с маскировкой параметров профиля идентичности
    new_context_kwargs: Dict[str, Any] = {
        "user_agent": profile_kwargs["user_agent"],
        "viewport": profile_kwargs.get("viewport") or BROWSER_VIEWPORT,
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": profile_kwargs.get("locale") or BROWSER_LOCALE,
        "timezone_id": profile_kwargs.get("timezone_id") or BROWSER_TIMEZONE,
        "extra_http_headers": profile_kwargs.get("extra_http_headers"),
    }

    # 5. Прокси применяется "как есть" — Proxy Manager уже выбрал/проверил его
    if proxy:
        new_context_kwargs["proxy"] = proxy

    context: BrowserContext = browser.new_context(**new_context_kwargs)

    # 6. Подкладываем куки через Cookie Manager (единая точка загрузки куки)
    if cookies_path:
        CookieManager.apply_to_playwright_context(context, cookies=CookieManager.load(cookies_path))

    return context



# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    # Локальный тест
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    test_cookies = ROOT_DIR / "AI_INPUT" / "cookies.json"
    
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False, cookies_path=test_cookies)
        page = ctx.new_page()
        page.goto("https://bot.sannysoft.com/") # Хороший сайт для проверки детекта
        page.wait_for_timeout(5000)
        ctx.browser.close()


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
#    (общие для Requests и Playwright, .env / Окружение)
# =====================================================================

# Если переменная IS_DOCKER установлена, принудительно включаем headless
IS_DOCKER = _get_bool("IS_DOCKER", "0")
HEADLESS = _get_bool("HEADLESS", "1") or IS_DOCKER

# Таймауты и повторы применимы как к HTTP-запросам (requests), так и к Playwright
TIMEOUT = _get_int("SCRAPER_TIMEOUT", 30)  # в секундах
RETRY_COUNT = _get_int("SCRAPER_RETRY", 3)

# Множитель экспоненциальной задержки между повторами (используется Retry Manager).
# Задержка между попытками растет как: backoff_factor * (2 ** (попытка - 1))
RETRY_BACKOFF_FACTOR = float(os.getenv("SCRAPER_RETRY_BACKOFF", "0.5"))

# Добавлять случайный джиттер к задержке повтора, чтобы избежать
# синхронных всплесков запросов при параллельном скрапинге.
RETRY_JITTER = _get_bool("SCRAPER_RETRY_JITTER", "1")

# HTTP-статусы, которые считаются временными сбоями и подлежат повтору.
RETRYABLE_STATUS_CODES: List[int] = [
    int(code.strip())
    for code in os.getenv("SCRAPER_RETRYABLE_STATUS_CODES", "429,500,502,503,504").split(",")
    if code.strip()
]

# Политика задержек между запросами (используется Delay Manager).
# Режим: "fixed" — постоянная пауза, "random" — случайная пауза в диапазоне.
DELAY_MODE = os.getenv("SCRAPER_DELAY_MODE", "random").strip().lower()
DELAY_FIXED_SECONDS = float(os.getenv("SCRAPER_DELAY_FIXED", "2.0"))
DELAY_MIN_SECONDS = float(os.getenv("SCRAPER_DELAY_MIN", "1.0"))
DELAY_MAX_SECONDS = float(os.getenv("SCRAPER_DELAY_MAX", "3.0"))

# --- Requests Engine (app/requests_engine.py) ---
REQUESTS_VERIFY_SSL = _get_bool("REQUESTS_VERIFY_SSL", "1")
REQUESTS_ALLOW_REDIRECTS = _get_bool("REQUESTS_ALLOW_REDIRECTS", "1")
REQUESTS_MAX_REDIRECTS = _get_int("REQUESTS_MAX_REDIRECTS", 30)




# Базовый URL целевого сайта (используется для urljoin относительных ссылок)
BASE_URL: str = os.getenv("BASE_URL", "")

# Настройки сети и прокси
PROXY_URL: Optional[str] = os.getenv("PROXY_URL") or None  # Формат: http://username:password@host:port

# Путь к файлу со списком прокси для File Proxy Provider (app/file_proxy_provider.py).
# Формат файла — по одной записи в строке, поддерживаются: ip:port,
# ip:port:username:password, а также готовые URL (http://..., socks5://...).
PROXY_FILE = Path(os.getenv("PROXY_FILE_PATH", str(AI_INPUT_DIR / "proxies.txt")))

# Схема (http/https/socks5), используемая File Proxy Provider для записей без
# явной схемы (ip:port или ip:port:username:password).
PROXY_FILE_DEFAULT_SCHEME = os.getenv("PROXY_FILE_DEFAULT_SCHEME", "http")

# --- Webshare Proxy Provider (app/webshare_proxy_provider.py) ---
# API-ключ Webshare. Никогда не хардкодится — только через окружение (.env).
WEBSHARE_API_KEY: Optional[str] = os.getenv("WEBSHARE_API_KEY") or None

# Базовый URL официального Webshare Proxy List API.
WEBSHARE_API_URL = os.getenv("WEBSHARE_API_URL", "https://proxy.webshare.io/api/v2/proxy/list/")

# Сколько секунд переиспользовать закэшированный список прокси до повторного
# запроса к API (снижает нагрузку на API и риск упереться в rate limit).
WEBSHARE_CACHE_TTL_SECONDS = _get_int("WEBSHARE_CACHE_TTL_SECONDS", 300)

# Таймаут запроса к Webshare API (секунды). По умолчанию — общий TIMEOUT проекта.
WEBSHARE_API_TIMEOUT = _get_int("WEBSHARE_API_TIMEOUT", TIMEOUT)

# --- Proxy Cache (app/proxy_cache.py) ---
# Локальный файл, в котором Proxy Cache хранит последний успешно
# загруженный список прокси (provider-независимо: Webshare, File и т.д.).
PROXY_CACHE_FILE = Path(os.getenv("PROXY_CACHE_FILE_PATH", str(AI_INPUT_DIR / "proxy_cache.json")))

# Сколько секунд считать закэшированный список прокси актуальным до
# необходимости обновления через провайдер (не путать с
# WEBSHARE_CACHE_TTL_SECONDS — это TTL персистентного файлового кэша,
# который переживает перезапуск процесса).
PROXY_CACHE_TTL_SECONDS = _get_int("PROXY_CACHE_TTL_SECONDS", 300)

# --- Proxy Selection (app/proxy_selector.py) ---
# Активная стратегия выбора прокси из пула: "first" (первый доступный)
# или "random" (случайный). Новые стратегии регистрируются через
# `ProxySelector.register_strategy()` без изменения кода.
PROXY_SELECTION_STRATEGY = os.getenv("PROXY_SELECTION_STRATEGY", "first").strip().lower()

# --- Proxy Rotation (app/proxy_rotation.py) ---
# Активная политика ротации прокси: "never", "every_request",
# "every_n_requests" или "after_failure". Новые политики регистрируются
# через `ProxyRotation.register_policy()` без изменения кода.
# "every_request" — политика по умолчанию, воспроизводящая поведение
# Proxy Manager до появления Proxy Rotation (обратная совместимость).
PROXY_ROTATION_POLICY = os.getenv("PROXY_ROTATION_POLICY", "every_request").strip().lower()

# Количество запросов между ротациями для политики "every_n_requests".
PROXY_ROTATION_EVERY_N = _get_int("PROXY_ROTATION_EVERY_N", 5)

# --- Proxy Health Check (app/health_check.py) ---
# Все пороги настраиваются через .env; смена любого порога не требует правок кода.
# URL для активной проверки прокси (лёгкий GET, проверяющий доступность прокси).
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", "https://httpbin.org/ip")
# Таймаут активной проверки (секунды).
HEALTH_CHECK_TIMEOUT = _get_int("HEALTH_CHECK_TIMEOUT", 10)
# Максимальное число последовательных сбоев, после которого прокси
# автоматически DISABLED на `HEALTH_DISABLE_DURATION_SECONDS`.
HEALTH_MAX_CONSECUTIVE_FAILURES = _get_int("HEALTH_MAX_CONSECUTIVE_FAILURES", 5)
# Число последовательных сбоев, после которого прокси переходит в статус
# UNHEALTHY (более серьёзная деградация, чем WARNING, но ещё не DISABLED).
# По умолчанию — половина от HEALTH_MAX_CONSECUTIVE_FAILURES, чтобы
# обеспечить промежуточную ступень предупреждения перед автоотключением.
HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES = _get_int(
    "HEALTH_UNHEALTHY_CONSECUTIVE_FAILURES",
    max(1, HEALTH_MAX_CONSECUTIVE_FAILURES // 2),
)

# Минимальная допустимая доля успешных запросов (0.0–1.0). При падении ниже
# этого порога (и наличии хотя бы `HEALTH_MIN_REQUESTS_FOR_RATE` запросов
# для достоверности) статус прокси становится WARNING.
HEALTH_MIN_SUCCESS_RATE = float(os.getenv("HEALTH_MIN_SUCCESS_RATE", "0.5"))
# Минимальное количество запросов, необходимое для учёта порога success rate
# (при малой выборке порог не применяется во избежание ложно-негативных статусов).
HEALTH_MIN_REQUESTS_FOR_RATE = _get_int("HEALTH_MIN_REQUESTS_FOR_RATE", 10)
# Максимально допустимое среднее время ответа (миллисекунды). При превышении —
# WARNING. Применяется только при наличии хотя бы одного успешного запроса.
HEALTH_MAX_RESPONSE_TIME_MS = _get_int("HEALTH_MAX_RESPONSE_TIME_MS", 5000)
# Длительность отключения прокси при достижении порога последовательных
# сбоев (секунды). По истечении этого окна прокси автоматически
# перепроверяется и может вернуться в строй.
HEALTH_DISABLE_DURATION_SECONDS = _get_int("HEALTH_DISABLE_DURATION_SECONDS", 300)

# --- Sticky Sessions (app/sticky_sessions.py) ---
# Все параметры настраиваются через .env; смена любого значения не требует правок кода.
# Включает/выключает привязку прокси к логической сессии в Proxy Manager.
STICKY_SESSIONS_ENABLED = _get_bool("STICKY_SESSIONS_ENABLED", "1")
# Максимальная длительность привязки сессии к прокси (секунды). 0 — без ограничения по времени.
STICKY_SESSION_TIMEOUT_SECONDS = _get_int("STICKY_SESSION_TIMEOUT_SECONDS", 600)
# Максимальное количество запросов в рамках одной сессии. 0 — без ограничения.
STICKY_SESSION_MAX_REQUESTS = _get_int("STICKY_SESSION_MAX_REQUESTS", 100)
# Поведение при отказе привязанного прокси: "replace" — сессия продолжается
# с новым прокси при следующем запросе, "terminate" — сессия помечается
# терминированной (вызывающий код должен начать новую логическую сессию).
STICKY_SESSION_ON_FAILURE = os.getenv("STICKY_SESSION_ON_FAILURE", "replace").strip().lower()



# =====================================================================
# 3. МАСКИРОВКА И КЛИЕНТСКИЕ ДАННЫЕ
#    (используются и в headers для requests, и в контексте Playwright)
# =====================================================================

# Реалистичный дефолтный User-Agent, если не передан кастомный в headers.json
DEFAULT_USER_AGENT = os.getenv(
    "SCRAPER_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36",
)

# Локаль и часовой пояс браузерного контекста / заголовков запросов
BROWSER_LOCALE = os.getenv("BROWSER_LOCALE", "en-US")
BROWSER_TIMEZONE = os.getenv("BROWSER_TIMEZONE", "America/New_York")

# Размер окна браузера (viewport). Ранее было захардкожено внутри browser.py
BROWSER_VIEWPORT: Dict[str, int] = {
    "width": _get_int("BROWSER_VIEWPORT_WIDTH", 1920),
    "height": _get_int("BROWSER_VIEWPORT_HEIGHT", 1080),
}

# Флаги запуска Chromium, снижающие типовые признаки автоматизации.
# Централизованы здесь, чтобы не дублировать список в разных местах кода.
BROWSER_LAUNCH_ARGS: List[str] = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
]


# =====================================================================
# 3.1 ЗАГОЛОВКИ ЗАПРОСОВ (сырые дефолты для Request Profile Manager)
#     Эти значения — единственный источник правды для HTTP-заголовков.
#     Используются app/request_profile.py для сборки полного профиля
#     идентичности (Requests + Playwright).
# =====================================================================

DEFAULT_ACCEPT = os.getenv(
    "SCRAPER_ACCEPT",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
)
DEFAULT_ACCEPT_LANGUAGE = os.getenv("SCRAPER_ACCEPT_LANGUAGE", "en-US,en;q=0.9")
DEFAULT_ACCEPT_ENCODING = os.getenv("SCRAPER_ACCEPT_ENCODING", "gzip, deflate, br")
DEFAULT_CONNECTION = os.getenv("SCRAPER_CONNECTION", "keep-alive")
DEFAULT_UPGRADE_INSECURE_REQUESTS = os.getenv("SCRAPER_UPGRADE_INSECURE_REQUESTS", "1")
DEFAULT_SEC_FETCH_DEST = os.getenv("SCRAPER_SEC_FETCH_DEST", "document")
DEFAULT_SEC_FETCH_MODE = os.getenv("SCRAPER_SEC_FETCH_MODE", "navigate")
DEFAULT_SEC_FETCH_SITE = os.getenv("SCRAPER_SEC_FETCH_SITE", "none")
DEFAULT_DNT = os.getenv("SCRAPER_DNT", "1")



# =====================================================================
# 3.2 PLAYWRIGHT ENGINE (app/playwright_engine.py, app/browser.py)
#     Настройки движка браузерной автоматизации. Идентичность клиента
#     (User-Agent, viewport, locale, timezone) уже берется из Request
#     Profile Manager (см. раздел 3 выше) — здесь только специфичные
#     для Playwright параметры навигации, не дублирующие эти значения.
# =====================================================================

# Таймаут навигации/ожидания селекторов Playwright (миллисекунды).
# По умолчанию — общий TIMEOUT проекта (секунды), переведенный в мс,
# чтобы не дублировать еще одно значение по умолчанию.
PLAYWRIGHT_TIMEOUT_MS = _get_int("PLAYWRIGHT_TIMEOUT_MS", TIMEOUT * 1000)

# Условие, при котором навигация (`page.goto()`) считается завершенной:
# "load", "domcontentloaded", "networkidle" или "commit".
PLAYWRIGHT_WAIT_UNTIL = os.getenv("PLAYWRIGHT_WAIT_UNTIL", "load").strip().lower()


# =====================================================================
# 3.3 INFINITE SCROLL (app/infinite_scroll.py)
#     Настройки централизованного компонента бесконечного скроллинга.
#     Не хранит селекторы конкретных сайтов — только поведение скроллинга
#     и условия остановки, полностью настраиваемые через .env.
# =====================================================================

# Включает/выключает бесконечный скроллинг. Если выключен,
# `InfiniteScroll.scroll()` сразу возвращается без единой прокрутки.
INFINITE_SCROLL_ENABLED = _get_bool("INFINITE_SCROLL_ENABLED", "1")

# Максимальное количество итераций скроллинга. 0 — без ограничения
# (в этом случае должно быть настроено хотя бы одно другое условие
# остановки, иначе цикл может выполняться до timeout/no_new_content).
INFINITE_SCROLL_MAX_SCROLLS = _get_int("INFINITE_SCROLL_MAX_SCROLLS", 20)

# Общий таймаут цикла скроллинга (секунды). 0 — без ограничения.
INFINITE_SCROLL_TIMEOUT_SECONDS = float(os.getenv("INFINITE_SCROLL_TIMEOUT_SECONDS", "60"))

# Высота страницы (px), при достижении которой скроллинг останавливается.
# 0 — без ограничения по высоте.
INFINITE_SCROLL_MAX_PAGE_HEIGHT = _get_int("INFINITE_SCROLL_MAX_PAGE_HEIGHT", 0)

# Число последовательных прокруток без увеличения высоты страницы, после
# которого считается, что новый контент больше не подгружается.
INFINITE_SCROLL_MAX_NO_NEW_CONTENT = _get_int("INFINITE_SCROLL_MAX_NO_NEW_CONTENT", 3)

# Шаг прокрутки в пикселях. 0 — скроллить сразу к текущему низу страницы
# (`document.body.scrollHeight`) на каждой итерации.
INFINITE_SCROLL_STEP_PX = _get_int("INFINITE_SCROLL_STEP_PX", 0)

# Плавная (smooth) прокрутка вместо мгновенной.
INFINITE_SCROLL_SMOOTH = _get_bool("INFINITE_SCROLL_SMOOTH", "0")

# Ожидать состояние "networkidle" после каждого скролла — полезно для
# сайтов, подгружающих контент через задержанные XHR/fetch запросы.
INFINITE_SCROLL_WAIT_NETWORK_IDLE = _get_bool("INFINITE_SCROLL_WAIT_NETWORK_IDLE", "0")

# Политика паузы между итерациями скроллинга (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
INFINITE_SCROLL_DELAY_MODE = os.getenv("INFINITE_SCROLL_DELAY_MODE", "random").strip().lower()
INFINITE_SCROLL_DELAY_FIXED_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_FIXED_SECONDS", "1.0"))
INFINITE_SCROLL_DELAY_MIN_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MIN_SECONDS", "0.5"))
INFINITE_SCROLL_DELAY_MAX_SECONDS = float(os.getenv("INFINITE_SCROLL_DELAY_MAX_SECONDS", "1.5"))


# =====================================================================
# 3.4 PAGINATION (app/pagination.py)
#     Настройки централизованного компонента пагинации.
#     Не хранит селекторы конкретных сайтов — только стратегию
#     пагинации, лимиты и поведение, полностью настраиваемые через .env.
# =====================================================================

# Максимальное количество страниц. 0 — без ограничения.
PAGINATION_MAX_PAGES = _get_int("PAGINATION_MAX_PAGES", 0)

# Общий таймаут цикла пагинации (секунды). 0 — без ограничения.
PAGINATION_TIMEOUT_SECONDS = float(os.getenv("PAGINATION_TIMEOUT_SECONDS", "0"))

# Включает обнаружение дублирующихся страниц (по dedupe_key из fetch_callback).
PAGINATION_DUPLICATE_DETECTION = _get_bool("PAGINATION_DUPLICATE_DETECTION", "0")

# --- URL-пагинация ---
# Имя query-параметра для номера страницы (например, "page").
PAGINATION_PAGE_PARAM = os.getenv("PAGINATION_PAGE_PARAM", "page").strip().lower()
# Начальное значение счётчика страниц.
PAGINATION_START_PAGE = _get_int("PAGINATION_START_PAGE", 1)
# Шаг счётчика страниц.
PAGINATION_PAGE_STEP = _get_int("PAGINATION_PAGE_STEP", 1)

# --- Offset-пагинация ---
# Имя query-параметра для offset (например, "offset").
PAGINATION_OFFSET_PARAM = os.getenv("PAGINATION_OFFSET_PARAM", "offset").strip().lower()
# Начальное значение offset.
PAGINATION_START_OFFSET = _get_int("PAGINATION_START_OFFSET", 0)
# Шаг offset.
PAGINATION_OFFSET_STEP = _get_int("PAGINATION_OFFSET_STEP", 20)

# Политика паузы между страницами (переиспользует Delay Manager,
# см. app/delay_manager.py): "fixed" — постоянная пауза, "random" — случайная.
PAGINATION_DELAY_MODE = os.getenv("PAGINATION_DELAY_MODE", "random").strip().lower()
PAGINATION_DELAY_FIXED_SECONDS = float(os.getenv("PAGINATION_DELAY_FIXED_SECONDS", "2.0"))
PAGINATION_DELAY_MIN_SECONDS = float(os.getenv("PAGINATION_DELAY_MIN_SECONDS", "1.0"))
PAGINATION_DELAY_MAX_SECONDS = float(os.getenv("PAGINATION_DELAY_MAX_SECONDS", "3.0"))


# =====================================================================
# 3.5 LOGIN SUPPORT (app/login_manager.py)
#     Настройки централизованного компонента аутентификации.
#     Не хранит учетные данные/URL/селекторы конкретных сайтов — только
#     лимиты, тайм-ауты и имена заголовков, полностью настраиваемые
#     через .env.
# =====================================================================

# Максимальное количество попыток логина (см. LoginManager.login()).
# Повтор пропускается автоматически при "окончательных" причинах сбоя
# (invalid_credentials, captcha_detected, missing_form) независимо от
# этого значения — см. _NON_RETRYABLE_REASONS в app/login_manager.py.
LOGIN_MAX_ATTEMPTS = _get_int("LOGIN_MAX_ATTEMPTS", 3)

# Тайм-аут одной попытки логина (секунды). В текущей реализации
# используется как рекомендованное значение для передачи в
# RequestsEngine/PlaywrightEngine вызывающим кодом (сами движки уже
# имеют собственный TIMEOUT/PLAYWRIGHT_TIMEOUT_MS — это отдельная,
# более узкая настройка именно для операции логина).
LOGIN_TIMEOUT_SECONDS = _get_int("LOGIN_TIMEOUT_SECONDS", TIMEOUT)

# Срок жизни аутентифицированной логической сессии (секунды) в памяти
# LoginManager (`ensure_login()` выполнит повторный логин по истечении).
# 0 — без ограничения по времени (сессия считается валидной, пока не
# инвалидирована явно через `LoginManager.invalidate_session()`).
LOGIN_SESSION_LIFETIME_SECONDS = _get_int("LOGIN_SESSION_LIFETIME_SECONDS", 1800)

# Сохранять ли куки после успешного логина через Cookie Manager
# (для восстановления сессии в будущих запусках через CookieSessionStrategy).
LOGIN_COOKIE_PERSISTENCE = _get_bool("LOGIN_COOKIE_PERSISTENCE", "1")

# Имя HTTP-заголовка для BearerTokenStrategy.
LOGIN_BEARER_HEADER_NAME = os.getenv("LOGIN_BEARER_HEADER_NAME", "Authorization")

# Имя HTTP-заголовка для ApiKeyStrategy.
LOGIN_API_KEY_HEADER_NAME = os.getenv("LOGIN_API_KEY_HEADER_NAME", "X-API-Key")

# Ключевые слова для обнаружения CAPTCHA в HTML (LoginDetector.contains_captcha()),
# через запятую, регистронезависимо.
LOGIN_CAPTCHA_KEYWORDS: List[str] = [
    keyword.strip().lower()
    for keyword in os.getenv("LOGIN_CAPTCHA_KEYWORDS", "captcha,recaptcha,hcaptcha,are you a robot").split(",")
    if keyword.strip()
]


# =====================================================================
# 3.6 HTML PARSER (app/html_parser.py)
#     Настройки централизованного слоя обработки HTML через BeautifulSoup.
#     Не хранит селекторы конкретных сайтов — только бэкенд-парсер,
#     полностью настраиваемый через .env.
# =====================================================================

# Парсер-бэкенд BeautifulSoup: "html.parser" (встроенный, без доп. зависимостей),
# "lxml" (быстрее, требует пакет lxml) или "html5lib" (максимально терпимый к
# невалидной разметке, требует пакет html5lib). По умолчанию — "html.parser",
# так как lxml/html5lib не входят в requirements.txt проекта по умолчанию.
HTML_PARSER_BACKEND = os.getenv("HTML_PARSER_BACKEND", "html.parser").strip().lower()


# =====================================================================
# 3.7 DATA VALIDATION (app/data_validator.py)
#     Настройки централизованного компонента валидации спарсенных
#     записей перед экспортом. Не хранит правила полей конкретного
#     сайта/заказа (это программный API `FieldRule`) — только поведение
#     встроенных type-валидаторов, полностью настраиваемое через .env.
# =====================================================================

# Включает обнаружение дублирующихся записей по умолчанию в
# `DataValidator.validate_records()` (можно переопределить явным
# аргументом `detect_duplicates` при вызове).
DATA_VALIDATION_DUPLICATE_DETECTION = _get_bool("DATA_VALIDATION_DUPLICATE_DETECTION", "0")

# Требовать ли обязательную схему (http:// или https://) для полей типа URL.
DATA_VALIDATION_URL_REQUIRE_SCHEME = _get_bool("DATA_VALIDATION_URL_REQUIRE_SCHEME", "1")

# Допустимый диапазон количества цифр для полей типа PHONE (после удаления
# всех нецифровых символов — пробелов, дефисов, скобок, кода страны "+").
DATA_VALIDATION_PHONE_MIN_DIGITS = _get_int("DATA_VALIDATION_PHONE_MIN_DIGITS", 7)
DATA_VALIDATION_PHONE_MAX_DIGITS = _get_int("DATA_VALIDATION_PHONE_MAX_DIGITS", 15)

# Список допустимых форматов даты (Python `strptime`), через запятую.
# Значение считается валидной датой, если совпадает хотя бы с одним форматом.
DATA_VALIDATION_DATE_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv("DATA_VALIDATION_DATE_FORMATS", "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%Y-%m-%dT%H:%M:%S").split(",")
    if fmt.strip()
]


# =====================================================================
# 3.8 DATA NORMALIZATION (app/data_normalizer.py)
#     Настройки централизованного слоя приведения спарсенных значений
#     к консистентному формату (числа, bool, даты, валюта, URL, страны).
#     Не хранит правила полей конкретного сайта/заказа (это программный
#     API `NormalizationRule`) — только словари/списки распознаваемых
#     значений и форматы вывода, полностью настраиваемые через .env.
# =====================================================================

# Текстовые представления, распознаваемые `DataNormalizer.normalize_bool()`
# как True/False (через запятую, регистронезависимо, сравнение по .lower()).
DATA_NORMALIZATION_BOOL_TRUE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_TRUE_VALUES",
        "true,1,yes,y,in stock,instock,available,да,есть,в наличии",
    ).split(",")
    if value.strip()
]
DATA_NORMALIZATION_BOOL_FALSE_VALUES: List[str] = [
    value.strip().lower()
    for value in os.getenv(
        "DATA_NORMALIZATION_BOOL_FALSE_VALUES",
        "false,0,no,n,out of stock,outofstock,unavailable,нет,отсутствует,нет в наличии",
    ).split(",")
    if value.strip()
]

# Список форматов даты (Python `strptime`), которые пробует
# `DataNormalizer.normalize_date()`/`normalize_timestamp()` по порядку,
# через запятую. Первый успешно разобранный формат используется.
DATA_NORMALIZATION_DATE_INPUT_FORMATS: List[str] = [
    fmt.strip()
    for fmt in os.getenv(
        "DATA_NORMALIZATION_DATE_INPUT_FORMATS",
        "%Y-%m-%d,%d.%m.%Y,%m/%d/%Y,%d/%m/%Y,%Y-%m-%dT%H:%M:%S,%B %d, %Y,%d %B %Y",
    ).split(",")
    if fmt.strip()
]

# Единый выходной формат даты для `DataNormalizer.normalize_date()`.
DATA_NORMALIZATION_DATE_OUTPUT_FORMAT = os.getenv("DATA_NORMALIZATION_DATE_OUTPUT_FORMAT", "%Y-%m-%d")

# Соответствия символ/название валюты -> ISO-код, для
# `DataNormalizer.normalize_currency()`. Формат: "символ:КОД", записи через
# запятую (например, "$:USD,€:EUR,₴:UAH"). Порядок важен только для
# читаемости — поиск в тексте выполняется по всем ключам.
DATA_NORMALIZATION_CURRENCY_SYMBOLS: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip().upper()
    for pair in os.getenv(
        "DATA_NORMALIZATION_CURRENCY_SYMBOLS",
        "$:USD,€:EUR,£:GBP,₴:UAH,₽:RUB,zł:PLN,грн:UAH,руб:RUB",
    ).split(",")
    if ":" in pair
}

# Схема по умолчанию, добавляемая `DataNormalizer.normalize_url()` к
# protocol-relative ("//example.com/...") и бесхема ("example.com/...") URL.
DATA_NORMALIZATION_URL_DEFAULT_SCHEME = os.getenv("DATA_NORMALIZATION_URL_DEFAULT_SCHEME", "https").strip().lower()

# Сохранять ли ведущий "+" (код страны) в `DataNormalizer.normalize_phone()`.
DATA_NORMALIZATION_PHONE_KEEP_PLUS = _get_bool("DATA_NORMALIZATION_PHONE_KEEP_PLUS", "1")

# Псевдонимы названий/кодов стран -> каноническое название, для
# `DataNormalizer.normalize_country()`. Формат: "псевдоним:Каноническое",
# записи через запятую (сравнение псевдонимов регистронезависимо).
DATA_NORMALIZATION_COUNTRY_ALIASES: Dict[str, str] = {
    pair.split(":", 1)[0].strip(): pair.split(":", 1)[1].strip()
    for pair in os.getenv(
        "DATA_NORMALIZATION_COUNTRY_ALIASES",
        "US:United States,USA:United States,U.S.:United States,U.S.A.:United States,"
        "UK:United Kingdom,U.K.:United Kingdom,GB:United Kingdom,"
        "UA:Ukraine,Ukraine:Ukraine,Украина:Ukraine,"
        "RU:Russia,Russian Federation:Russia,"
        "PL:Poland,Poland:Poland,"
        "DE:Germany,Germany:Germany",
    ).split(",")
    if ":" in pair
}


# =====================================================================
# 3.9 INCREMENTAL SAVING (app/exporter.py)
#     Настройки централизованного механизма прогрессивного сохранения
#     спарсенных записей во время скрапинга (вместо накопления всего
#     набора данных в памяти и экспорта единым вызовом в самом конце).
#     Не хранит формат/структуру записей конкретного сайта/заказа —
#     только поведение самого механизма записи, полностью настраиваемое
#     через .env.
# =====================================================================

# Включает/выключает Incremental Saving в `app/main.py`. При выключении
# сохраняется прежнее (batch) поведение: все записи копятся в памяти и
# экспортируются одним вызовом `save_to_csv`/`save_to_json` после
# завершения скрапинга — обратная совместимость с поведением до появления
# Incremental Saving.
EXPORT_INCREMENTAL_ENABLED = _get_bool("EXPORT_INCREMENTAL_ENABLED", "1")

# Принудительно сбрасывать буфер ОС на диск (`file.flush()` + `os.fsync()`)
# после каждой записи/пачки записей. Повышает устойчивость к потере данных
# при сбое (данные гарантированно физически на диске), но снижает
# производительность на очень больших объёмах — поэтому настраивается,
# а не хардкодится.
EXPORT_INCREMENTAL_FLUSH_ON_WRITE = _get_bool("EXPORT_INCREMENTAL_FLUSH_ON_WRITE", "1")


# =====================================================================
# 3.10 BATCH WRITER (app/exporter.py)
#      Настройки централизованного буферизующего слоя, оборачивающего
#      писатели Incremental Saving (IncrementalCSVWriter/JSONWriter).
#      Вместо записи на диск при каждом вызове write_records(), записи
#      копятся в памяти и сбрасываются пачками — уменьшая количество
#      операций записи на диск на больших объёмах данных. Не хранит
#      формат/структуру записей конкретного сайта/заказа — только
#      поведение самого буфера, полностью настраиваемое через .env.
# =====================================================================

# Максимальное количество записей, накапливаемых в буфере до
# автоматического сброса на диск (см. BatchWriter.add_records()).
BATCH_WRITER_BATCH_SIZE = _get_int("BATCH_WRITER_BATCH_SIZE", 100)

# Включает автоматический сброс буфера при достижении BATCH_WRITER_BATCH_SIZE.
# При выключении буфер растет неограниченно до явного вызова flush()/close() —
# использовать с осторожностью только под контролем вызывающего кода.
BATCH_WRITER_AUTO_FLUSH_ENABLED = _get_bool("BATCH_WRITER_AUTO_FLUSH_ENABLED", "1")

# Сбрасывать оставшиеся в буфере записи при завершении работы
# (BatchWriter.close() / выход из контекстного менеджера), чтобы
# ни одна накопленная запись не была потеряна при штатном завершении.
BATCH_WRITER_FLUSH_ON_SHUTDOWN = _get_bool("BATCH_WRITER_FLUSH_ON_SHUTDOWN", "1")


# =====================================================================
# 3.11 CHECKPOINT MANAGER (app/checkpoint_manager.py)
#      Настройки централизованного механизма периодического сохранения
#      прогресса скрапинга на диск (см. `tasks/TASK.md` и
#      `framework/ROADMAP.md`, Milestone 6). Checkpoint Manager только
#      ЗАПИСЫВАЕТ прогресс — он не восстанавливает и не продолжает
#      скрапинг (это будущий Resume Support, потребляющий сохраненные
#      здесь checkpoint-файлы). Не хранит логику конкретного
#      сайта/заказа — только поведение самого механизма чекпоинтинга,
#      полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает создание чекпоинтов. При выключении вызовы
# `CheckpointManager.record_page()`/`record_records()` становятся no-op —
# обратная совместимость с поведением до появления Checkpoint Manager.
CHECKPOINT_ENABLED = _get_bool("CHECKPOINT_ENABLED", "1")

# Путь к файлу чекпоинта. По умолчанию — рядом с cookies.json/proxy_cache.json
# в AI_INPUT_DIR, по аналогии с уже существующими персистентными файлами
# состояния (COOKIES_FILE, PROXY_CACHE_FILE).
CHECKPOINT_FILE = Path(os.getenv("CHECKPOINT_FILE_PATH", str(AI_INPUT_DIR / "checkpoint.json")))

# Создавать новый чекпоинт раз в N обработанных страниц. 0 — не учитывать
# количество страниц как условие сохранения.
CHECKPOINT_INTERVAL_PAGES = _get_int("CHECKPOINT_INTERVAL_PAGES", 1)

# Создавать новый чекпоинт раз в N обработанных записей. 0 — не учитывать
# количество записей как условие сохранения.
CHECKPOINT_INTERVAL_RECORDS = _get_int("CHECKPOINT_INTERVAL_RECORDS", 0)

# Создавать новый чекпоинт не чаще, чем раз в N секунд (даже если условия
# по страницам/записям сработали раньше — не даёт чекпоинтингу создавать
# избыточную нагрузку на диск при очень частых страницах/записях). 0 —
# не учитывать время как условие (полагаться только на pages/records).
CHECKPOINT_INTERVAL_SECONDS = float(os.getenv("CHECKPOINT_INTERVAL_SECONDS", "0"))

# Политика хранения файлов чекпоинта:
#   "overwrite"   — всегда перезаписывать один и тот же файл (CHECKPOINT_FILE);
#   "timestamped" — дополнительно сохранять с суффиксом-таймстампом,
#                   сохраняя историю чекпоинтов (полезно для отладки/аудита).
CHECKPOINT_OVERWRITE_POLICY = os.getenv("CHECKPOINT_OVERWRITE_POLICY", "overwrite").strip().lower()


# =====================================================================
# 3.12 RESUME SUPPORT (app/resume_manager.py)
#      Настройки централизованного механизма автоматического продолжения
#      прерванной сессии скрапинга на основе чекпоинтов, сохраненных
#      Checkpoint Manager'ом (см. `tasks/TASK.md` и `framework/ROADMAP.md`,
#      Milestone 6). Resume Support только ЧИТАЕТ и валидирует чекпоинты —
#      он не создает их сам (это ответственность Checkpoint Manager) и не
#      знает о логике конкретного сайта/заказа — только поведение самого
#      механизма восстановления, полностью настраиваемое через .env.
# =====================================================================

# Включает/выключает автоматическое обнаружение и восстановление
# прерванной сессии при старте. При выключении сохраняется прежнее
# поведение: скрапинг всегда начинается "с нуля" — обратная
# совместимость с поведением до появления Resume Support.
RESUME_ENABLED = _get_bool("RESUME_ENABLED", "1")

# Максимальный "возраст" чекпоинта (в секундах), при котором он ещё
# считается пригодным для восстановления. 0 — не ограничивать возраст
# (восстанавливать независимо от давности последнего сохранения).
RESUME_MAX_AGE_SECONDS = _get_int("RESUME_MAX_AGE_SECONDS", 0)

# Резервируется для будущего интерактивного подтверждения перед
# восстановлением (см. TASK.md, "Future versions may optionally ask
# the user whether to resume or restart"). Пока не используется в коде —
# уже присутствует в конфигурации, чтобы включение такого режима в
# будущем не требовало правок app/config.py.
RESUME_CONFIRMATION_REQUIRED = _get_bool("RESUME_CONFIRMATION_REQUIRED", "0")


# =====================================================================
# 4. ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ПУТЕЙ

# =====================================================================



if __name__ == "__main__":
    print(f"[{__file__}] Проверка путей конфигурации:")
    print(f"  Корень проекта (ROOT_DIR): {ROOT_DIR}")
    print(f"  Папка вывода (OUTPUT_DIR): {OUTPUT_DIR}")
    print(f"  Файл кук (COOKIES_FILE):   {COOKIES_FILE}")
    print(f"  Тестовый HTML (PAGE_HTML_FILE): {PAGE_HTML_FILE}")
    print(f"  Режим Headless:            {HEADLESS}")
    print(f"  Запуск в Docker:           {IS_DOCKER}")
    print(f"  Таймаут:                   {TIMEOUT}s, Повторы: {RETRY_COUNT}")
    print(f"  Viewport:                  {BROWSER_VIEWPORT}")
    print(f"  Locale/Timezone:           {BROWSER_LOCALE} / {BROWSER_TIMEZONE}")


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

    # Берем заголовки из ключей первого элемента
    fieldnames = list(data[0].keys())

    try:
        # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"[{__file__}] Данные успешно сохранены в CSV: {filepath.name} (Строк: {len(data)})")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в CSV: {e}")
        return ""


def save_to_json(data: List[Dict[str, Any]], filename: str, indent: int = 4) -> str:
    """
    Сохраняет данные в формате JSON с красивыми отступами.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в JSON.")
        return ""

    if not filename.endswith(".json"):
        filename += ".json"

    filepath = OUTPUT_DIR / filename

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        print(f"[{__file__}] Данные успешно сохранены в JSON: {filepath.name}")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в JSON: {e}")
        return ""


# =========================================================================
# INCREMENTAL SAVING
# =========================================================================


class IncrementalCSVWriter:
    """
    Прогрессивно дозаписывает записи в CSV-файл во время скрапинга.

    В отличие от `save_to_csv()`, который получает готовый список и пишет
    его одним вызовом, `IncrementalCSVWriter` открывает файл один раз
    (`open(..., mode="w")`) и держит его открытым на протяжении всей
    сессии скрапинга, дописывая новые записи по мере их появления через
    `write_records()`.

    CSV — построчный формат, поэтому он естественно устойчив к сбоям:
    каждая успешно записанная строка независима, и обрыв процесса просто
    обрезает файл на последней завершённой строке, не повреждая уже
    сохранённые данные.

    Заголовки CSV определяются по ключам первой переданной записи
    (аналогично `save_to_csv`) — на всех последующих вызовах
    `write_records()` ожидаются записи с тем же набором полей.

    Пример использования:

        writer = IncrementalCSVWriter("output_results.csv")
        try:
            for page_records in scrape_pages():
                writer.write_records(page_records)
        finally:
            writer.close()

        # либо как контекстный менеджер:
        with IncrementalCSVWriter("output_results.csv") as writer:
            for page_records in scrape_pages():
                writer.write_records(page_records)
    """

    def __init__(self, filename: str, flush_on_write: Optional[bool] = None, append: bool = False):
        """
        Args:
            filename: Имя выходного файла (относительно `OUTPUT_DIR`).
                Расширение ".csv" добавляется автоматически, если
                отсутствует.
            flush_on_write: Принудительно сбрасывать буфер ОС на диск
                (`flush()` + `os.fsync()`) после каждого вызова
                `write_records()`. По умолчанию —
                `config.EXPORT_INCREMENTAL_FLUSH_ON_WRITE`.
            append: Открыть существующий файл в режиме дозаписи вместо
                перезаписи ("w"). Используется Resume Support
                (`app/resume_manager.py`) для продолжения прерванной
                сессии без потери уже экспортированных строк. Если файл
                не существует или пуст, поведение идентично `append=False`
                (заголовок CSV записывается как обычно). По умолчанию —
                False (полная обратная совместимость с поведением до
                появления Resume Support).
        """
        if not filename.endswith(".csv"):
            filename += ".csv"

        self.filepath = OUTPUT_DIR / filename
        self._flush_on_write = (
            flush_on_write if flush_on_write is not None else EXPORT_INCREMENTAL_FLUSH_ON_WRITE
        )

        self._file = None
        self._writer: Optional[csv.DictWriter] = None
        self._fieldnames: Optional[List[str]] = None
        self._total_written = 0
        self._closed = False

        # Дозапись возможна только если файл реально существует и не пуст —
        # иначе (первый запуск/файл отсутствует) ведём себя как при
        # обычном создании нового файла (пишем заголовок).
        resume_append = append and self.filepath.exists() and self.filepath.stat().st_size > 0

        try:
            # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
            mode = "a" if resume_append else "w"
            self._file = open(self.filepath, mode=mode, encoding="utf-8-sig", newline="")
            if resume_append:
                # Заголовок уже присутствует в существующем файле — писатель
                # переходит прямо в режим дозаписи строк без повторного
                # `writeheader()`. Fieldnames будут определены по первой
                # переданной порции записей (как и при обычном режиме),
                # но `writeheader()` для неё пропускается через `_header_written`.
                self._header_written = True
            else:
                self._header_written = False
            log_message(
                "info",
                f"IncrementalCSVWriter: инициализирован ({self.filepath.name}, "
                f"режим={'дозапись' if resume_append else 'новый файл'})",
            )
        except Exception as exc:
            log_message("error", f"IncrementalCSVWriter: не удалось открыть файл {self.filepath}: {exc}")
            self._file = None
            self._header_written = False


    def write_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Дозаписывает порцию записей в CSV-файл.

        Заголовки CSV фиксируются по первому вызову (по ключам первой
        записи в первой непустой порции) и записываются один раз.

        Если запись какой-либо отдельной строки завершилась ошибкой,
        она логируется, а остальные записи в порции продолжают
        обрабатываться — сбой одной строки не должен обрывать весь
        процесс скрапинга и не затрагивает уже сохранённые данные.

        Args:
            records: Список словарей (одна страница/порция результатов).

        Returns:
            int: Количество успешно записанных строк из этой порции.
        """
        if not records:
            return 0

        if self._file is None or self._closed:
            log_message("error", "IncrementalCSVWriter: попытка записи в закрытый/неоткрытый файл")
            return 0

        written = 0
        try:
            if self._writer is None:
                self._fieldnames = list(records[0].keys())
                self._writer = csv.DictWriter(self._file, fieldnames=self._fieldnames)
                # При дозаписи (Resume Support) заголовок уже существует в
                # файле — повторный writeheader() испортил бы CSV.
                if not self._header_written:
                    self._writer.writeheader()
                    self._header_written = True

            for record in records:
                try:
                    self._writer.writerow(record)
                    written += 1
                except Exception as row_exc:
                    log_message("error", f"IncrementalCSVWriter: сбой записи строки: {row_exc}")

            if self._flush_on_write:
                self._file.flush()
                os.fsync(self._file.fileno())

            self._total_written += written
            log_message("debug", f"IncrementalCSVWriter: записано строк={written} (всего={self._total_written})")
        except Exception as exc:
            log_message("error", f"IncrementalCSVWriter: непредвиденная ошибка записи: {exc}")

        return written


    def close(self) -> None:
        """Закрывает файл. Безопасно вызывать несколько раз."""
        if self._file is not None and not self._closed:
            try:
                self._file.close()
                log_message(
                    "info",
                    f"IncrementalCSVWriter: закрыт ({self.filepath.name}, всего строк={self._total_written})",
                )
            except Exception as exc:
                log_message("error", f"IncrementalCSVWriter: ошибка при закрытии файла: {exc}")
            finally:
                self._closed = True

    @property
    def total_written(self) -> int:
        """Общее количество успешно записанных строк за время жизни писателя."""
        return self._total_written

    def __enter__(self) -> "IncrementalCSVWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


class IncrementalJSONWriter:
    """
    Прогрессивно дозаписывает записи в JSON-файл во время скрапинга.

    JSON-массив не поддерживает построчное дозаписывание "из коробки"
    (в отличие от CSV), поэтому писатель вручную управляет структурой
    файла: открывающая "[" пишется при инициализации, каждая новая
    запись добавляется с корректной запятой-разделителем, а закрывающая
    "]" дописывается при явном `close()`.

    Важный риск: если процесс прерывается до вызова `close()`
    (крах/Ctrl+C/сбой питания), файл останется без завершающей "]" и
    будет невалидным JSON, при этом содержащиеся в нём записи не
    теряются и не повреждаются — файл можно восстановить, дописав "]"
    вручную. Это ограничение самого формата JSON, а не реализации;
    corruption (испорченные незакрытые записи) исключается тем, что
    запись каждого элемента атомарна.

    Пример использования:

        writer = IncrementalJSONWriter("output_results.json")
        try:
            for page_records in scrape_pages():
                writer.write_records(page_records)
        finally:
            writer.close()

        # либо как контекстный менеджер:
        with IncrementalJSONWriter("output_results.json") as writer:
            for page_records in scrape_pages():
                writer.write_records(page_records)
    """

    def __init__(
        self,
        filename: str,
        indent: int = 4,
        flush_on_write: Optional[bool] = None,
        append: bool = False,
    ):
        """
        Args:
            filename: Имя выходного файла (относительно `OUTPUT_DIR`).
                Расширение ".json" добавляется автоматически, если
                отсутствует.
            indent: Отступ для читаемого форматирования каждой записи.
            flush_on_write: Принудительно сбрасывать буфер ОС на диск
                (`flush()` + `os.fsync()`) после каждого вызова
                `write_records()`. По умолчанию —
                `config.EXPORT_INCREMENTAL_FLUSH_ON_WRITE`.
            append: Продолжить дозапись в существующий JSON-массив вместо
                создания нового файла. Используется Resume Support
                (`app/resume_manager.py`) для продолжения прерванной
                сессии без потери уже экспортированных записей.

                Реализация: у существующего файла отыскивается последняя
                закрывающая скобка "]" (независимо от того, успел ли
                предыдущий запуск вызвать `close()` — при аварийном
                завершении её может не быть) и файл обрезается
                (`truncate()`) до этой позиции, чтобы новые записи можно
                было дописать через запятую как продолжение массива.
                Если файл не существует, пуст или в нём нет ни одной
                записи — поведение идентично `append=False` (создаётся
                новый файл). По умолчанию — False (полная обратная
                совместимость с поведением до появления Resume Support).
        """
        if not filename.endswith(".json"):
            filename += ".json"

        self.filepath = OUTPUT_DIR / filename
        self._indent = indent
        self._flush_on_write = (
            flush_on_write if flush_on_write is not None else EXPORT_INCREMENTAL_FLUSH_ON_WRITE
        )

        self._file = None
        self._total_written = 0
        self._closed = False
        self._wrote_any = False

        resume_append = append and self._prepare_append_target()

        try:
            if resume_append:
                self._file = open(self.filepath, mode="a", encoding="utf-8")
                self._wrote_any = True  # файл уже содержит хотя бы одну запись
            else:
                self._file = open(self.filepath, mode="w", encoding="utf-8")
                self._file.write("[\n")
            log_message(
                "info",
                f"IncrementalJSONWriter: инициализирован ({self.filepath.name}, "
                f"режим={'дозапись' if resume_append else 'новый файл'})",
            )
        except Exception as exc:
            log_message("error", f"IncrementalJSONWriter: не удалось открыть файл {self.filepath}: {exc}")
            self._file = None

    def _prepare_append_target(self) -> bool:
        """
        Готовит существующий JSON-файл для дозаписи: находит последнюю
        закрывающую скобку "]" и обрезает файл до этой позиции (удаляет
        завершающую "]" и всё, что после неё, включая случай, когда её
        вовсе нет из-за аварийного завершения предыдущего запуска).

        Returns:
            bool: True, если файл пригоден для дозаписи (существует,
                не пуст, содержит валидную структуру массива с хотя бы
                одной записью). False — вызывающий код должен создать
                новый файл с нуля.
        """
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            return False

        try:
            with open(self.filepath, "r+", encoding="utf-8") as f:
                content = f.read()
                stripped = content.rstrip()

                if not stripped.startswith("["):
                    return False

                # Файл содержит только "[" (или "[\n") без единой записи —
                # нет смысла дозаписывать через запятую, начинаем с чистого листа.
                inner = stripped[1:].rstrip()
                if inner.endswith("]"):
                    inner = inner[:-1].rstrip()
                if not inner:
                    return False

                # Обрезаем до последней закрывающей "]" (если она есть) —
                # это гарантирует корректную дозапись независимо от того,
                # был ли файл штатно закрыт предыдущим запуском.
                cutoff = stripped.rfind("]")
                truncated = (stripped[:cutoff] if cutoff != -1 else stripped).rstrip()

                f.seek(0)
                f.write(truncated)
                f.truncate()
            return True
        except Exception as exc:
            log_message(
                "error",
                f"IncrementalJSONWriter: не удалось подготовить файл {self.filepath.name} для дозаписи: {exc}",
            )
            return False


    def write_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Дозаписывает порцию записей в JSON-массив.

        Каждая запись сериализуется отдельно, поэтому сбой сериализации
        одной записи (например, несериализуемый тип) логируется и
        пропускается, не прерывая запись остальных записей в порции.

        Args:
            records: Список словарей (одна страница/порция результатов).

        Returns:
            int: Количество успешно записанных записей из этой порции.
        """
        if not records:
            return 0

        if self._file is None or self._closed:
            log_message("error", "IncrementalJSONWriter: попытка записи в закрытый/неоткрытый файл")
            return 0

        written = 0
        try:
            for record in records:
                try:
                    serialized = json.dumps(record, ensure_ascii=False, indent=self._indent)
                    # Отступ каждой вложенной записи для читаемости общего массива
                    serialized = "\n".join("  " + line for line in serialized.splitlines())

                    if self._wrote_any:
                        self._file.write(",\n")
                    self._file.write(serialized)
                    self._wrote_any = True
                    written += 1
                except (TypeError, ValueError) as row_exc:
                    log_message("error", f"IncrementalJSONWriter: сбой сериализации записи: {row_exc}")

            if self._flush_on_write:
                self._file.flush()
                os.fsync(self._file.fileno())

            self._total_written += written
            log_message("debug", f"IncrementalJSONWriter: записано записей={written} (всего={self._total_written})")
        except Exception as exc:
            log_message("error", f"IncrementalJSONWriter: непредвиденная ошибка записи: {exc}")

        return written

    def close(self) -> None:
        """
        Дописывает закрывающую "]" и закрывает файл.
        Безопасно вызывать несколько раз.
        """
        if self._file is not None and not self._closed:
            try:
                self._file.write("\n]\n")
                self._file.close()
                log_message(
                    "info",
                    f"IncrementalJSONWriter: закрыт ({self.filepath.name}, всего записей={self._total_written})",
                )
            except Exception as exc:
                log_message("error", f"IncrementalJSONWriter: ошибка при закрытии файла: {exc}")
            finally:
                self._closed = True

    @property
    def total_written(self) -> int:
        """Общее количество успешно записанных записей за время жизни писателя."""
        return self._total_written

    def __enter__(self) -> "IncrementalJSONWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


# =========================================================================
# BATCH WRITER
# =========================================================================


class RecordSink(Protocol):
    """
    Минимальный протокол, который должен реализовывать любой писатель,
    оборачиваемый `BatchWriter`. `IncrementalCSVWriter` и
    `IncrementalJSONWriter` уже удовлетворяют этому протоколу без
    каких-либо изменений — `BatchWriter` не заменяет их, а лишь
    буферизует вызовы `write_records()`.
    """

    def write_records(self, records: List[Dict[str, Any]]) -> int: ...


class BatchWriter:
    """
    Буферизующий слой поверх одного или нескольких писателей Incremental
    Saving (`IncrementalCSVWriter`, `IncrementalJSONWriter` или любого
    другого объекта с методом `write_records()`).

    Проблема, которую решает `BatchWriter`: при "чистом" Incremental
    Saving каждый вызов `write_records()` — это отдельная операция
    записи на диск (в CSV — построчная дозапись + опциональный
    flush/fsync, в JSON — дозапись сериализованных записей +
    опциональный flush/fsync). На большом количестве мелких порций
    (например, по одной странице пагинации) это создает избыточное
    количество операций I/O.

    `BatchWriter` не открывает и не закрывает файлы сам — этим
    продолжают заниматься сами `Incremental*Writer` (их жизненный цикл
    остается на стороне вызывающего кода, как и раньше). `BatchWriter`
    только решает, **когда** передать накопленные записи нижестоящим
    писателям:

        Record → Memory Buffer → (буфер заполнен?) → передать батч
        нижестоящим писателям → очистить буфер → продолжить скрапинг

    Поддерживает:
      - автоматический сброс при достижении `batch_size`
        (`BATCH_WRITER_AUTO_FLUSH_ENABLED` / `BATCH_WRITER_BATCH_SIZE`);
      - явный ручной сброс (`flush()`);
      - сброс остатка буфера при завершении работы (`close()` /
        выход из контекстного менеджера, управляется
        `BATCH_WRITER_FLUSH_ON_SHUTDOWN`).

    Обработка ошибок: если вызов `write_records()` нижестоящего писателя
    завершается исключением, ошибка логируется, буфер **не очищается**
    (чтобы не потерять ещё не сохранённые на диск записи и оставить
    возможность повторной попытки), и `flush()` возвращает 0 для этого
    сброса. Уже успешно записанные ранее батчи не затрагиваются —
    `BatchWriter` работает только с текущим содержимым буфера.

    Пример использования (замена прямых вызовов write_records()):

        csv_writer = IncrementalCSVWriter("output_results.csv")
        json_writer = IncrementalJSONWriter("output_results.json")

        with BatchWriter([csv_writer, json_writer]) as batch_writer:
            for page_records in scrape_pages():
                batch_writer.add_records(page_records)
        # remaining buffered records are flushed automatically on exit

        csv_writer.close()
        json_writer.close()
    """

    def __init__(
        self,
        sinks: List[RecordSink],
        batch_size: Optional[int] = None,
        auto_flush_enabled: Optional[bool] = None,
        flush_on_shutdown: Optional[bool] = None,
    ):
        """
        Args:
            sinks: Список нижестоящих писателей (любой объект с методом
                `write_records(records) -> int`, например
                `IncrementalCSVWriter`/`IncrementalJSONWriter`). Их
                открытие/закрытие остается на стороне вызывающего кода.
            batch_size: Максимальный размер буфера до автоматического
                сброса. По умолчанию — `config.BATCH_WRITER_BATCH_SIZE`.
            auto_flush_enabled: Включает автоматический сброс при
                достижении `batch_size`. По умолчанию —
                `config.BATCH_WRITER_AUTO_FLUSH_ENABLED`.
            flush_on_shutdown: Сбрасывать остаток буфера в `close()`.
                По умолчанию — `config.BATCH_WRITER_FLUSH_ON_SHUTDOWN`.
        """
        self._sinks: List[RecordSink] = list(sinks)
        self._batch_size = batch_size if batch_size is not None else BATCH_WRITER_BATCH_SIZE
        self._auto_flush_enabled = (
            auto_flush_enabled if auto_flush_enabled is not None else BATCH_WRITER_AUTO_FLUSH_ENABLED
        )
        self._flush_on_shutdown = (
            flush_on_shutdown if flush_on_shutdown is not None else BATCH_WRITER_FLUSH_ON_SHUTDOWN
        )

        self._buffer: List[Dict[str, Any]] = []
        self._total_buffered = 0  # всего когда-либо добавлено в буфер (включая уже сброшенное)
        self._total_flushed = 0   # всего успешно передано нижестоящим писателям
        self._flush_count = 0     # количество выполненных сбросов (авто + ручных)
        self._closed = False

        log_message(
            "info",
            f"BatchWriter: инициализирован (sinks={len(self._sinks)}, "
            f"batch_size={self._batch_size}, auto_flush={self._auto_flush_enabled})",
        )

    def add_records(self, records: List[Dict[str, Any]]) -> None:
        """
        Добавляет записи в буфер. Не выполняет запись сама — только
        накапливает записи в памяти.

        Если авто-сброс включен (`auto_flush_enabled`) и после
        добавления размер буфера достиг `batch_size`, автоматически
        вызывает `flush()`. Буфер никогда не растет бесконечно при
        включенном авто-сбросе.

        Args:
            records: Список словарей для добавления в буфер (например,
                результаты парсинга одной страницы).
        """
        if not records:
            return

        if self._closed:
            log_message("error", "BatchWriter: попытка добавить записи в закрытый writer")
            return

        self._buffer.extend(records)
        self._total_buffered += len(records)

        if self._auto_flush_enabled and len(self._buffer) >= self._batch_size:
            self.flush(reason="auto")

    def flush(self, reason: str = "manual") -> int:
        """
        Немедленно передает все записи из буфера нижестоящим писателям
        (`sinks`) и очищает буфер при успехе.

        Если один из писателей выбрасывает исключение при записи, ошибка
        логируется, а буфер **сохраняется** (не очищается), чтобы данные
        не потерялись и сброс можно было повторить позже. Уже успешно
        записанные писатели за этот вызов не откатываются (частичная
        запись в другие sinks не считается поводом для полной отмены —
        KISS: избегаем сложной транзакционной логики между независимыми
        форматами экспорта).

        Args:
            reason: Только для логирования — "auto" (авто-сброс по
                размеру батча), "manual" (явный вызов) или "shutdown"
                (сброс при закрытии).

        Returns:
            int: Количество записей, успешно переданных писателям за
                этот вызов (0, если буфер был пуст или сброс не удался).
        """
        if not self._buffer:
            return 0

        batch = self._buffer
        batch_len = len(batch)

        had_failure = False
        for sink in self._sinks:
            try:
                sink.write_records(batch)
            except Exception as exc:
                had_failure = True
                log_message("error", f"BatchWriter: сбой записи батча ({reason}) в {sink!r}: {exc}")

        if had_failure:
            # Буфер сохраняем целиком, чтобы вызывающий код мог повторить
            # попытку (например, следующим вызовом flush()) без потери данных.
            log_message(
                "error",
                f"BatchWriter: сброс ({reason}) завершился с ошибками, буфер сохранён "
                f"(записей в буфере: {batch_len})",
            )
            return 0

        self._buffer = []
        self._total_flushed += batch_len
        self._flush_count += 1
        log_message(
            "info",
            f"BatchWriter: батч сброшен ({reason}), записей={batch_len} "
            f"(всего сброшено={self._total_flushed}, сбросов={self._flush_count})",
        )
        return batch_len

    def close(self) -> None:
        """
        Завершает работу `BatchWriter`. Если `flush_on_shutdown` включен
        и в буфере остались записи — сбрасывает их перед закрытием, чтобы
        ни одна накопленная запись не была потеряна при штатном
        завершении. Безопасно вызывать несколько раз.

        Не закрывает сами нижестоящие писатели (`sinks`) — их закрытие
        остается на стороне вызывающего кода.
        """
        if self._closed:
            return

        if self._buffer:
            if self._flush_on_shutdown:
                self.flush(reason="shutdown")
            else:
                log_message(
                    "error",
                    f"BatchWriter: закрытие с непустым буфером и выключенным "
                    f"flush_on_shutdown — {len(self._buffer)} записей будут потеряны",
                )

        log_message(
            "info",
            f"BatchWriter: закрыт (всего добавлено={self._total_buffered}, "
            f"всего сброшено={self._total_flushed}, сбросов={self._flush_count})",
        )
        self._closed = True

    @property
    def buffered_count(self) -> int:
        """Текущее количество записей в буфере, ещё не сброшенных на диск."""
        return len(self._buffer)

    @property
    def total_flushed(self) -> int:
        """Общее количество записей, успешно переданных писателям за время жизни объекта."""
        return self._total_flushed

    def __enter__(self) -> "BatchWriter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    test_data = [
        {"id": 1, "title": "Ноутбук", "price": 1200.50, "in_stock": True},
        {"id": 2, "title": "Смартфон", "price": 550.00, "in_stock": False},
    ]
    print(f"[{__file__}] Запуск теста экспортера (batch)...")
    save_to_csv(test_data, "test_products")
    save_to_json(test_data, "test_products.json")

    print(f"[{__file__}] Запуск теста Incremental Saving...")
    with IncrementalCSVWriter("test_incremental") as csv_writer:
        csv_writer.write_records(test_data[:1])
        csv_writer.write_records(test_data[1:])
    print(f"  CSV: записано всего {csv_writer.total_written} строк")

    with IncrementalJSONWriter("test_incremental") as json_writer:
        json_writer.write_records(test_data[:1])
        json_writer.write_records(test_data[1:])
    print(f"  JSON: записано всего {json_writer.total_written} записей")

    print(f"[{__file__}] Запуск теста Batch Writer...")
    csv_writer2 = IncrementalCSVWriter("test_batch_writer")
    json_writer2 = IncrementalJSONWriter("test_batch_writer")
    with BatchWriter([csv_writer2, json_writer2], batch_size=2) as batch_writer:
        batch_writer.add_records(test_data[:1])  # не достигнут batch_size=2, буфер=1
        print(f"  После 1-й записи: buffered={batch_writer.buffered_count}, flushed={batch_writer.total_flushed}")
        batch_writer.add_records(test_data[1:])  # достигнут batch_size=2, авто-сброс
        print(f"  После 2-й записи: buffered={batch_writer.buffered_count}, flushed={batch_writer.total_flushed}")
    csv_writer2.close()
    json_writer2.close()
    print(f"  Итого сброшено через BatchWriter: {batch_writer.total_flushed} записей")


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
