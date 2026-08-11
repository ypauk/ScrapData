# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/scraper.py`.

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

Ниже — анализ только на основании предоставленного контекста и файлов. Я не буду восполнять отсутствующие данные предположениями. Там, где вывод нельзя подтвердить имеющимися материалами, это явно отмечено.

1. Краткое описание задачи

Клиент хочет получить scraper для сайта professionele-koeling.nl, который собирает товары и экспортирует их в CSV.

Требования клиента:

собрать данные по товарам;

каждая требуемая характеристика должна находиться в отдельной CSV-колонке;

названия и порядок колонок должны соответствовать финальной спецификации DS-PRK-Scraper.json;

сначала сделать тестовый CSV только с 2 товарами;

изображения необходимо скачивать, а не только сохранять их URL;

товары без скидки включать, при отсутствии sale price оставлять поле пустым;

отсутствующие характеристики оставлять пустыми;

описание сохранять как чистый текст, без HTML;

товары, которых нет в наличии, также включать;

на первом этапе требуется только 2 товара.

При этом предоставленный checkpoint показывает, что предыдущий запуск уже обработал 429 товаров на 12 страницах, однако это не означает, что текущая реализация корректно выполняет требования клиента: наличие checkpoint.json показывает факт предыдущего запуска, но не подтверждает корректность всех полей.

Уровень уверенности: высокий в отношении общей цели и формата результата; средний в отношении полного набора реально извлекаемых полей, поскольку HTML product page предоставлен только частично.

2. Какой конечный результат нужен

Основной результат:

CSV-файл

с:

фиксированными колонками;

строгим порядком колонок согласно DS-PRK-Scraper.json;

одной строкой на товар;

пустыми значениями там, где характеристика отсутствует;

URL изображений в соответствующих колонках согласно спецификации;

локальными файлами изображений, которые должны быть физически скачаны scraper'ом.

Важный момент: DS-PRK-Scraper.json является авторитетной спецификацией структуры CSV. Его нельзя самостоятельно изменять, переименовывать или интерпретировать иначе.

3. Как лучше решить задачу
Рекомендуемый подход: PlaywrightEngine + парсинг HTML

С учетом зафиксированного условия проекта, оптимальным является:

PlaywrightEngine → получение HTML → парсинг HTML → CSV + скачивание изображений

Причина проста: в main.py уже зафиксировано использование PlaywrightEngine, и scraper.py получает готовый PlaywrightEngine.

Поэтому переход на чистый requests как основной механизм здесь не является подходящим вариантом.

Что именно использовать

PlaywrightEngine

для:

открытия category pages;

обработки JavaScript;

перехода по pagination;

открытия product pages;

получения итогового HTML.

HTML parsing

для извлечения данных из уже загруженного HTML.

По предоставленным фрагментам HTML сайт имеет достаточно обычную HTML-структуру:

.products-grid;

li.item;

.product-name;

.price-box;

.old-price;

.special-price;

.breadcrumbs;

.product-name h1;

.short-description.

Поэтому после получения страницы браузером дополнительная сложная браузерная автоматизация, судя по имеющимся данным, не требуется.

Изображения

Изображения следует скачивать отдельно по найденным URL.

Это необходимо, потому что клиент прямо сказал:

надо

на вопрос о скачивании изображений.

4. Почему остальные варианты хуже
requests + BeautifulSoup

Как основной подход не рекомендую.

Причины:

в notes.txt прямо указано, что сайт работает на JS;

проект уже зафиксирован на PlaywrightEngine;

нельзя гарантировать, что requests получит тот же HTML, который доступен браузеру.

При этом BeautifulSoup-подобный HTML parsing как логика разбора полученного HTML — концептуально подходит. Проблема именно в использовании requests вместо существующего PlaywrightEngine.

Selenium

Не нужен.

Playwright уже является заданным механизмом браузерного доступа. Использование Selenium только увеличит сложность.

Scrapy

Избыточен для текущего объема задачи.

Есть всего 429 товаров согласно checkpoint, а на первом этапе вообще требуется только 2. Вводить полноценный Scrapy-пайплайн без необходимости нецелесообразно.

Прямой API

На данный момент не подтвержден.

notes.txt говорит:

API нет

Кроме того, network.har фактически не содержит данных.

Поэтому строить решение вокруг API сейчас оснований нет.

GraphQL

Не обнаружен и не подтвержден.

Selenium/Playwright + поиск API

Активный поиск API был бы полезен на этапе исследования, если бы имелся полноценный HAR или browser network data. Но предоставленный network.har пустой, поэтому сейчас такой путь не дает подтвержденного преимущества.

5. Анализ сайта
Возможность	Что известно
JavaScript Rendering	Да, заявлено в notes.txt
React	Не подтверждено
Vue	Не подтверждено
Angular	Не подтверждено
API	По notes.txt: нет
GraphQL	Не обнаружен
Infinite Scroll	Не обнаружен
Pagination	Да
Login	Не обнаружен
Cookies	Да
JWT	Не обнаружен
Bearer Token	Не обнаружен
CAPTCHA	Не подтверждена
Cloudflare	Да, cookie cf_clearance присутствует
Rate Limits	Неизвестны
Download Files	Да — изображения необходимо скачивать
Upload Files	Не требуется
Lazy Loading	Не подтверждено
WebSocket	Не подтвержден
XHR/Fetch	Неизвестно из предоставленных данных
Sitemap	Не предоставлен / не подтвержден
robots.txt	Не предоставлен / не проверен
Pagination

Подтверждена непосредственно HTML:

?p=2
?p=3
?p=4
...

Также checkpoint сообщает:

total_pages = 12

processed_count = 429

И category HTML говорит:

Artikelen 1 tot 36 van 429 in totaal

То есть подтвержден каталог примерно на 429 товаров, по 36 товаров на страницу.

Cloudflare

Cookie:

cf_clearance

присутствует.

Это сильный сигнал о наличии Cloudflare-защиты, но само наличие cookie не доказывает, что scraper обязательно будет блокироваться.

Поэтому вероятность блокировок нельзя считать высокой только на этом основании.

6. Что необходимо собрать до начала разработки

Здесь находится главный блокер.

Критически необходимо получить полноценный HTML product page

Предоставленный product-page.html неполный.

Он заканчивается на:

<div class="price-box">
...

и содержит только:

breadcrumbs;

title;

short description;

price;

sale price.

Но спецификация требует дополнительные данные.

В частности, сейчас невозможно надежно определить структуру:

imageurl;

image_name;

Description;

Specs;

Spec_detail.

Особенно важно

В DS-PRK-Scraper.json указано:

Specs: URL screenshot + each own colom

и:

Spec_detail: evertything before the : is the header

Это инструкции по заполнению, но реальные HTML-элементы характеристик в предоставленном product page отсутствуют.

Поэтому сейчас нельзя честно определить CSS/XPath-селекторы для этих полей.

Что желательно получить

Нужно получить:

Полный product-page.html, включая конец страницы.

HTML блока галереи изображений.

HTML блока Description.

HTML блока Specs/характеристик.

HTML именно тех двух товаров, которые будут использоваться в тесте, если они отличаются по структуре.

Пример ожидаемого итогового CSV для 2 товаров — если у клиента он есть.

Что уже имеется

Уже достаточно данных для понимания:

category page;

pagination;

title в карточке;

URL товара;

thumbnail;

обычной цены;

sale price.

Но этого недостаточно для полной реализации всей спецификации.

7. Возможные сложности
1. Cloudflare

Наличие cf_clearance означает потенциальную защиту Cloudflare.

Возможные последствия:

блокировка при большом количестве запросов;

необходимость поддерживать browser session;

изменение clearance cookie;

challenge при подозрительном поведении.

Но фактическая вероятность блокировки сейчас не подтверждена.

2. JavaScript

Сайт заявлен как JS-based.

Значит, использование браузера оправдано.

Однако пока неизвестно, какие именно данные действительно требуют JS, а какие находятся непосредственно в HTML.

3. Неполная информация о product page

Это сейчас главная техническая проблема.

Нельзя надежно реализовать extraction для всех требуемых колонок без полного HTML.

4. Галерея изображений

В category HTML виден только один thumbnail:

<img ... src="...">

Но клиент требует скачать изображения, а спецификация предусматривает:

imageurl;

image_name;

multiple images.

Поэтому неизвестно, где находится полная галерея и сколько изображений может быть у одного товара.

5. Specs

В спецификации предусмотрено динамическое создание колонок из характеристик.

Пока не предоставлен реальный HTML блока характеристик, нельзя определить:

как отделены названия характеристик;

где находятся значения;

как обрабатываются повторяющиеся названия;

как обрабатываются характеристики без значения;

как формируются отдельные CSV columns.

6. Description

Нужно убедиться, где заканчивается основное описание и начинаются:

рекомендации;

телефоны;

дополнительные элементы;

related products;

прочие блоки страницы.

Просто взять весь текст страницы было бы неправильно.

7. Разные шаблоны товаров

Нужно проверить, одинаков ли HTML-шаблон у всех товаров.

Особенно:

sale/no sale;

наличие/отсутствие specs;

разное количество изображений;

отсутствие описания;

товары out-of-stock.

8. Изображения

Могут использоваться:

thumbnail URLs;

full-size URLs;

cached URLs.

Нужно определить, какой URL является правильным для скачивания.

9. Уже существующий checkpoint

checkpoint.json показывает 429 обработанных товаров.

Но из предоставленных данных нельзя определить:

каким кодом они обрабатывались;

корректны ли значения;

были ли реально скачаны изображения;

соответствует ли CSV финальной спецификации.

Поэтому нельзя считать существующий результат доказательством готовности scraper'а.

8. Что нужно уточнить у клиента

Здесь я бы не задавал клиенту много вопросов, потому что большая часть требований уже определена.

Нужны только вопросы, закрывающие реальные пробелы.

Вопрос 1 — полный HTML

Can you provide the complete HTML of a product page, including the image gallery, full description and specifications section?

Это главный вопрос.

Вопрос 2 — тестовые товары

Which exact 2 product URLs should be used for the initial test CSV?

Сейчас в материалах встречаются разные товары:

Polar DM071 — в category page;

Polar GE579 — в product page.

Нельзя самостоятельно решать, какие именно 2 товара клиент считает тестовыми.

Вопрос 3 — ожидаемый формат изображений

Should downloaded images be saved as separate files alongside the CSV, with the CSV containing their local filenames?

Из требований понятно, что изображения надо скачивать, но точный ожидаемый способ связывания CSV с локальными файлами явно не описан.

Вопрос 4 — Specs

Если после получения полного HTML структура всё равно неоднозначна:

Should every product specification become a separate CSV column, using the text before : as the column header?

Хотя DS-PRK-Scraper.json это уже практически говорит, этот вопрос стоит задавать только если реальный HTML покажет неоднозначность.

9. Рекомендуемый стек технологий

Основные технологии:

Python

Playwright / PlaywrightEngine

HTML parser

CSV

стандартные средства работы с файлами/изображениями

Дополнительный browser framework вроде Selenium не нужен.

Отдельный API layer также не нужен.

10. План разработки
Этап 1 — подтвердить структуру данных

Цель: получить полный HTML одной product page.

Результат: подтверждены реальные источники для всех обязательных колонок.

Зависимость: необходим полный product-page.html.

Этап 2 — тестовая обработка 2 товаров

Цель: проверить extraction на двух реальных товарах.

Результат:

2 строки CSV;

все требуемые колонки;

корректные цены;

корректный title;

description как текст;

specs по отдельным колонкам;

ссылки/имена изображений;

скачанные изображения.

Зависимость: полный HTML + определенные клиентом 2 товара.

Этап 3 — проверка CSV против спецификации

Цель: проверить структуру результата.

Результат:

нет лишних колонок;

нет отсутствующих колонок;

правильные названия;

правильный порядок;

отсутствие смешивания разных данных в одной колонке.

Зависимость: утвержденный формат тестового результата.

Этап 4 — масштабирование на каталог

Цель: перейти от 2 товаров ко всему каталогу.

Результат: обработка всех необходимых страниц каталога.

По checkpoint потенциальный объем — 429 товаров / 12 страниц, но это следует считать подтвержденным только для уже наблюдавшегося состояния сайта.

Зависимость: успешный тест на 2 товара.

Этап 5 — проверка устойчивости

Цель: проверить:

товары без скидки;

товары без характеристик;

товары без некоторых изображений;

out-of-stock;

разные варианты product pages;

Cloudflare behavior.

Результат: стабильный scraper с корректными пустыми значениями.

Зависимость: рабочий scraper и тестовые данные.

11. Оценка сложности
Параметр	Оценка
Общая сложность	5/10
Разработка тестовой версии на 2 товара	2–4 часа
Полная реализация после подтверждения HTML	6–10 часов
Вероятность блокировок	средняя
Вероятность необходимости браузера	высокая
Вероятность изменения сайта в будущем	средняя
Общий риск	средний
Почему не 8–9/10

Несмотря на JS и Cloudflare, сайт по имеющимся HTML выглядит достаточно структурированным.

Подтверждены:

category pages;

pagination;

product URLs;

title;

price;

sale price;

breadcrumbs;

short description.

То есть базовая структура scraper'а не выглядит сложной.

Основной риск сосредоточен не в navigation, а в получении полного HTML и точном извлечении всех требуемых полей.

12. Можно ли решить проще

Да.

И это желательно сделать.

Не нужно автоматически строить сложную систему из:

API;

Scrapy;

базы данных;

очередей;

нескольких browser engines;

сложной архитектуры retry;

отдельного backend.

Для данного проекта достаточно:

PlaywrightEngine → category/product HTML → parsing → CSV + image download

Потенциально еще проще

Нужно проверить, находятся ли все необходимые данные непосредственно на product page.

Если да, схема будет очень простой:

получить URL товара из category page;

открыть product page через PlaywrightEngine;

получить HTML;

извлечь данные;

скачать изображения;

записать строку CSV.

При этом category page используется в основном для обнаружения товаров и их URL.

Можно ли вообще не открывать product pages?

Сейчас нет оснований так утверждать.

Category HTML содержит:

URL;

title;

thumbnail;

price;

sale price.

Но не содержит подтвержденных:

полного Description;

Specs;

Spec_detail;

полной image gallery.

Следовательно, переход на product pages пока необходим.

Если полный category HTML в дальнейшем покажет, что все требуемые поля уже присутствуют в карточках, тогда можно будет упростить решение и отказаться от product-page requests.

Уровень уверенности: средний до получения полного HTML.

13. Итоговая рекомендация
Рекомендуемое решение

Использовать существующий PlaywrightEngine для получения страниц и обычный HTML parsing для извлечения данных, после чего формировать CSV и отдельно скачивать изображения.

Это оптимальный вариант, потому что:

он соответствует зафиксированному проектом PlaywrightEngine;

сайт заявлен как JavaScript;

API не обнаружен;

структура HTML уже частично подтверждена;

объем данных умеренный;

CSV не требует базы данных;

нет необходимости усложнять проект Scrapy/Selenium/API-инфраструктурой.

Главный блокер

Сейчас я бы не переходил к написанию production-кода.

Причина не в недостатке информации о самом scraper'е, а в том, что product-page.html предоставлен только частично.

Без оставшейся части нельзя надежно определить extraction для наиболее важных неподтвержденных полей:

gallery;

imageurl;

image_name;

Description;

Specs;

Spec_detail.

Что получить перед кодированием

Минимально:

полный product-page.html;

точные 2 URL для тестового scrape;

желательно подтверждение того, как клиент хочет связывать скачанные изображения с CSV.

После получения полного HTML можно сначала реализовать и проверить только 2 товара, сравнить результат со спецификацией DS-PRK-Scraper.json, и только после успешного теста масштабировать на весь каталог.

Итоговая оценка: проект технически выглядит вполне реализуемым и не требует сложной архитектуры, но на текущем наборе материалов начинать полноценную реализацию преждевременно. Главный следующий шаг — получить недостающий HTML product page и подтвердить два тестовых товара.

---

## План проекта (этап 2)

Ниже — проектирование без изменения существующего ядра и без готового Python-кода. Я исхожу только из переданного контекста и не заполняю неизвестные части предположениями.

1. Полный поток данных

Выбранный поток:

Клиент запускает main.py
↓
main.py → browser.py → PlaywrightEngine
↓
main.py вызывает scraper.fetch_page_data(engine)
↓
scraper.py открывает category URL через Playwright
↓
получает сырой HTML listing page
↓
parser.parse_listing(html)
↓
BeautifulSoup извлекает URL товаров и доступные данные карточек
↓
scraper.py получает URL каждого товара
↓
Playwright открывает product page
↓
получается сырой HTML product page
↓
parser.parse_product(html)
↓
BeautifulSoup извлекает детальные поля
↓
scraper.py скачивает найденные изображения
↓
scraper.py объединяет результат парсинга с результатами загрузки изображений
↓
list[dict]
↓
main.py
↓
exporter.save_to_csv()

Почему именно HTML + Playwright

API использовать не следует.

Причины:

main.py уже жестко построен вокруг PlaywrightEngine;

notes.txt прямо указывает, что API нет;

network.har пуст;

HTML реально предоставлен и уже содержит необходимые элементы listing;

сайт заявлен как JS-based;

переходы между страницами и товарами подтверждены обычными URL.

Плюсы

полностью соответствует существующему framework;

не требует изменения main.py;

не требует отдельного HTTP-клиента;

можно использовать текущие cookies / proxy / user-agent;

HTML уже частично подтверждает нужные селекторы;

для 2 товаров решение получается простым.

Минусы

Playwright тяжелее обычного HTTP-клиента;

Cloudflare потенциально может ограничивать автоматизированный доступ;

полный product HTML отсутствует, поэтому часть extraction пока нельзя подтвердить;

скачивание изображений добавляет отдельные сетевые операции.

ПРЕДПОЛОЖЕНИЕ: PlaywrightEngine предоставляет интерфейс получения итогового HTML страницы. Точное название метода получения HTML в переданных материалах не указано, поэтому его нельзя надежно назвать.

2. Проектирование app/scraper.py
2.1. Интерфейс функций

Предлагаю минимальный набор из трех основных функций.

Функция	Назначение	Входные параметры	Возвращаемое значение
fetch_page_data(engine)	Главная функция сбора	engine	list[dict]
fetch_listing_page(engine, url)	Открывает одну страницу каталога и получает HTML	engine, url	str
fetch_product_page(engine, url)	Открывает страницу товара и получает HTML	engine, url	str
download_images(...)	Скачивает изображения, найденные парсером	browser/network context + image URLs	list[str]

Здесь намеренно нет отдельного класса.

fetch_page_data(engine)

Это orchestration-функция самого scraper.

Она должна:

взять стартовый URL:
https://www.professionele-koeling.nl/koelkasten-kisten.html;

загрузить listing page;

передать HTML в parser.parse_listing();

получить URL товаров;

перейти на product pages;

получить product HTML;

передать его в parser.parse_product();

получить URLs изображений;

скачать изображения;

добавить локальные имена файлов;

собрать итоговые dict;

вернуть list[dict].

Она не должна искать CSS-селекторы сама.

То есть scraper не должен знать про .product-name, .price-box, .breadcrumbs и т. д. Эти знания принадлежат parser.py.

2.2. Алгоритм обхода
Стартовая страница

Подтвержден URL:

https://www.professionele-koeling.nl/koelkasten-kisten.html

Пагинация

Подтвержден формат:

?p=2

?p=3

?p=4

и т. д.

Также HTML содержит:

class="next"

и ссылку на следующую страницу.

При этом для текущего задания полный каталог обходить не нужно.

В notes.txt прямо указано:

сначала только 2 товара

Поэтому для первого запуска алгоритм должен остановиться после получения двух товаров.

Почему не цикл по 1..12

checkpoint.json показывает:

total_pages = 12

processed_count = 429

Но это результат предыдущего запуска, а не требование текущего теста.

Поэтому для тестового запуска правильнее:

page 1
  ↓
получить товары
  ↓
если собрано 2 → остановиться
  ↓
иначе перейти на следующую страницу

Это одновременно позволяет протестировать пагинацию, не запуская ненужный полный scrape.

Как определять следующую страницу

Предпочтительный вариант:

не конструировать URL вручную, а использовать href ссылки Next, найденной parser'ом.

То есть:

HTML listing
↓
parser.parse_listing()
↓
товары + next_page_url
↓
scraper открывает next_page_url

Это надежнее, чем самостоятельно предполагать формат pagination.

При этом фактический HTML уже подтверждает ?p=2, ?p=3 и т. д.

Поведение на listing page

Scraper должен дождаться наличия контейнера каталога.

Подтвержден:

.products-grid

После загрузки страницы scraper получает HTML.

ПРЕДПОЛОЖЕНИЕ: PlaywrightEngine должен иметь возможность дождаться CSS-селектора перед извлечением HTML.

Lazy Loading

Не подтвержден.

В предоставленном HTML карточки уже присутствуют полностью.

Поэтому:

не выполнять искусственный scroll без доказательства необходимости.

Это уменьшает время работы и количество действий браузера.

Infinite Scroll

Не обнаружен.

Есть обычная pagination.

Tabs / Show More

Не подтверждены.

Не выполнять клики без подтвержденной необходимости.

Поведение на product page

Scraper:

открывает URL товара;

ожидает загрузки страницы;

получает полный HTML;

передает HTML parser'у.

Минимально подтвержденные элементы:

.breadcrumbs
.product-name h1
.short-description
.price-box

Но product HTML предоставлен только частично.

Поэтому scraper не должен пытаться самостоятельно искать Description, Gallery или Specs.

random_delay()

Использовать существующую:

utils.random_delay()

Не создавать собственную реализацию.

Разумные места:

listing page
↓
random_delay()
↓
product page

product page
↓
random_delay()
↓
следующий product page

И дополнительно между переходами на следующие listing pages.

Для теста из двух товаров не нужен сложный механизм случайных пауз.

ПРЕДПОЛОЖЕНИЕ: диапазон задержки уже определен внутри utils.random_delay(), поэтому scraper не должен дублировать настройки.

3. Проектирование app/parser.py
3.1. Интерфейс функций

Минимальный набор:

Функция	Назначение	Входные параметры	Возвращаемое значение
parse_listing(html)	Разбирает listing page	html: str	dict с товарами и pagination
parse_single_item(card)	Извлекает данные одной карточки	bs4.element.Tag	dict
parse_product(html)	Разбирает product page	html: str	dict
parse_specs(...)	Преобразует характеристики в отдельные поля	HTML/текст блока характеристик	dict
normalize_text(...)	Убирает HTML и нормализует текст	строка/HTML	str
extract_image_urls(...)	Извлекает URLs галереи	HTML	list[str]

Здесь parse_listing() лучше возвращать не просто list[dict], а внутренний результат вида:

{
    "items": [...],
    "next_page_url": ...
}

Причина — scraper должен понимать, есть ли следующая страница, не разбирая HTML самостоятельно.

3.2. parse_listing(html)

Подтвержден основной контейнер:

CSS
.products-grid

Карточка:

CSS
li.item

Для каждой карточки вызывается:

parse_single_item(card)
Поля карточки

Подтверждены:

Поле	Источник
URL	a.product-image[href] или h2.product-name a[href]
Title	.product-name
Thumbnail	.product-image img[src]
Price	.old-price .price
Sale price	.special-price .price

Но listing является только вспомогательным источником.

Для финального результата при наличии product page предпочтительно использовать детальные данные product page.

parse_single_item(card)

Пример результата:

JSON
{
    "URL": "https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html",
    "Title": "Polar DM071",
    "imageurl": "https://www.professionele-koeling.nl/media/catalog/product/cache/...",
    "Price": 179.0,
    "Sale price": 175.0
}
Цена

Использовать существующую:

utils.clean_price()

Не создавать новый price parser.

Отсутствие скидки

Требование клиента:

если у товара нет скидки — пустое поле.

Следовательно:

Sale price отсутствует
→ ""

а не копирование обычной цены.

parse_product(html)

Это основной parser.

Он должен извлекать только данные из HTML product page.

Подтвержденные поля
Breadcrumb

Источник:

CSS
.breadcrumbs

В предоставленном HTML:

Home
Koelkasten&Kisten
Polar GE579

Однако DS-PRK-Scraper.json показывает:

Breadcrumb: "Home"

Поэтому нельзя самостоятельно менять семантику этого поля.

Финальное значение должно соответствовать спецификации, а не нашему предположению о том, что breadcrumb должен содержать всю цепочку.

Title

Подтвержден:

CSS
.product-name h1

Пример:

Polar GE579
Short description

Подтвержден:

CSS
.short-description

Необходимо:

удалить HTML;

сохранить текст;

сохранить смысловые переносы строк;

не сохранять HTML-теги.

При этом в .short-description присутствует рекламный блок:

Advies nodig...
Bel onze specialisten...

Нельзя автоматически считать, что весь текст .short-description является товарным описанием, если клиентская спецификация предполагает другое содержимое.

ПРЕДПОЛОЖЕНИЕ: если полного HTML не будет достаточно для определения границ short description, понадобится уточнить фактический контейнер.

Price

Подтвержден:

CSS
.old-price .price

Для Polar GE579:

€ 255,99
Sale price

Подтвержден:

CSS
.special-price .price

Для Polar GE579:

€ 229,00

Если .special-price отсутствует:

""
Изображения

Это отдельная важная часть.

В category HTML подтвержден только thumbnail:

CSS
.product-image img

Но клиент требует скачивать изображения, а DS-PRK-Scraper.json содержит:

imageurl
image_name

и явно говорит:

if multipli seperated by comma

Следовательно, parser должен вернуть:

image URLs → list[str]

а scraper уже должен физически скачать их.

Это принципиально важно для разделения ответственности:

parser.py
→ определяет URL изображения

scraper.py
→ выполняет сетевое скачивание

parser.py
→ не делает HTTP-запросов
imageurl

Финальное значение:

url1,url2,url3

если изображений несколько.

image_name

Финальное значение:

filename1,filename2,filename3

в том же порядке, что и imageurl.

Это позволяет установить соответствие:

imageurl[0] ↔ image_name[0]
imageurl[1] ↔ image_name[1]
...

ПРЕДПОЛОЖЕНИЕ: если клиент ожидает именно локальные имена файлов в image_name, это наиболее логичное соответствие требованию о физическом скачивании. Само требование не содержит отдельного подтвержденного примера итогового CSV.

Description

Это одно из главных неизвестных.

В предоставленном product-page.html отсутствует HTML блока полного Description.

При этом DS-PRK-Scraper.json показывает, что Description должен быть текстом, причем приведенный пример содержит:

основной текст;

Uitvoering;

Specificaties;

дополнительные абзацы;

Gebruikertips.

Поэтому parser должен концептуально делать:

HTML Description
↓
удалить HTML
↓
сохранить текст
↓
сохранить переносы
↓
Description

Но конкретный CSS-селектор нельзя достоверно указать на основании имеющегося HTML.

Нельзя просто брать:

body.get_text()

поскольку тогда в Description попадут:

меню;

телефон;

корзина;

related products;

footer;

другие элементы страницы.

Это было бы нарушением спецификации.

Specs / Spec_detail

Это наиболее важная динамическая часть.

DS-PRK-Scraper.json прямо определяет:

Specs = screenshot URL + each own column

и:

Spec_detail = everything before the :

То есть характеристики должны превращаться в отдельные CSV columns.

Например, если фактический HTML содержит:

Artikelnummer: GE579
Inhoud: 29 liter
Energieklasse: F
Gewicht: 13 kg

логика должна быть:

Artikelnummer → "GE579"
Inhoud → "29 liter"
Energieklasse → "F"
Gewicht → "13 kg"

а не одной объединенной колонкой.

Но это алгоритм, а не утверждение о конкретном HTML-селекторе.

Критическое ограничение

В переданном product-page.html блока Specs нет.

Поэтому пока невозможно достоверно определить:

selector блока;

selector строки;

selector header;

selector value;

формат повторяющихся характеристик;

наличие <table>;

наличие <dl>;

наличие обычных <div>;

наличие характеристик в изображении.

Следовательно, parse_specs() проектируется как отдельная функция, но ее конкретный DOM selector должен быть заполнен после получения полного product HTML.

3.3. Финальная структура результата

Фиксированные поля должны соответствовать DS-PRK-Scraper.json без переименования.

Концептуально одна запись:

JSON
{
    "URL": "https://www.professionele-koeling.nl/koelkasten-kisten/polar-ge579.html",
    "Breadcrumb": "Home",
    "Title": "Polar GE579",
    "Short description": "De Polar GE579 is een zwarte minibar koelkast...",
    "imageurl": "image1.jpg-url,image2.jpg-url",
    "image_name": "polar-ge579-1.jpg,polar-ge579-2.jpg",
    "Price": 255.99,
    "Sale price": 229.0,
    "Description": "Polar GE579: Zwarte 30 liter minibar koelkast...",
    "Artikelnummer": "GE579",
    "Inhoud": "29 liter",
    "Energieklasse": "F"
}

Последние динамические поля здесь только пример структуры. Нельзя считать, что именно эти три колонки должны быть добавлены независимо от фактического HTML.

Главное правило:

каждая характеристика становится отдельной колонкой, причем название колонки берется из текста до :.

Если характеристика отсутствует у конкретного товара:

""

а не 0 и не None, поскольку требования клиента говорят оставлять отсутствующие характеристики пустыми.

4. Обработка ошибок
Сценарий	Действие
Timeout listing page	Записать в лог, повторить ограниченное число раз; после исчерпания retry остановить/завершить сбор
Timeout product page	Записать URL товара в лог и пропустить этот товар
HTTP 403	Логировать и прекратить дальнейший автоматический обход
Cloudflare challenge	Логировать и остановить scraper, не пытаться обходить challenge
CAPTCHA	Логировать и остановить scraper
.products-grid отсутствует	Считать страницу некорректно загруженной, логировать и остановить пагинацию
Карточка без URL	Пропустить карточку
Цена отсутствует	""
Sale price отсутствует	""
Description отсутствует	""
Specs отсутствуют	Не создавать значения для отсутствующих характеристик; соответствующие поля оставить пустыми
Image URL отсутствует	imageurl="", image_name=""
Ошибка скачивания одной картинки	Логировать, продолжить остальные изображения
Ошибка product page	Не прерывать весь scrape, пропустить товар
Пустой listing	Логировать и завершить пагинацию
Неизвестная структура product page	Логировать конкретный URL и вернуть максимально доступные поля
Дубликат товара	Не создавать вторую запись, если URL уже был обработан
Retry

Для timeout разумен небольшой ограниченный retry.

ПРЕДПОЛОЖЕНИЕ: config.py уже содержит сетевые timeout-настройки, поэтому scraper.py не должен создавать собственные значения timeout.

Для Cloudflare/403 retry не должен превращаться в бесконечный цикл.

5. Оценка рисков

 Cloudflare — подтвержден cf_clearance

 Требуется авторизация — не обнаружена

 Rate Limiting — потенциальный риск

 CAPTCHA — не подтверждена

 Infinite Scroll — не обнаружен

 Shadow DOM — не подтвержден

 iframe — не подтвержден

 WebSocket — не подтвержден

 GraphQL API — не обнаружен

 Сложная структура DOM с возможными изменениями — средний риск

 Неполный product HTML — главный текущий риск

 Галерея изображений неизвестна

 DOM блока Description неизвестен

 DOM блока Specs неизвестен

 Формат dynamic specification columns пока нельзя проверить

 Различия между товарами — нужно проверить

 Out-of-stock — требуется проверить на реальном HTML

Самый большой риск

Не Cloudflare.

Главный риск сейчас — отсутствие полного HTML product page.

Без него невозможно подтвердить extraction для:

image gallery
Description
Specs
Spec_detail

Поэтому проектировать эти части на основе догадок нельзя.

6. Порядок реализации
1. parser.py — первым

Это самый правильный первый шаг.

Причины:

parser не зависит от сети;

уже есть category-page.html;

уже есть page.html;

уже есть частичный product-page.html;

можно сразу проверить title, URL, prices, breadcrumbs и short description;

можно отдельно реализовать dynamic specs после получения полного HTML.

Особенно важно сначала установить точную структуру результата согласно DS-PRK-Scraper.json.

2. Получить полный product HTML

До финализации parse_product() нужно получить:

gallery;

полный Description;

Specs;

остальные элементы до конца страницы.

Это не изменение архитектуры, а устранение текущего информационного блокера.

3. scraper.py

После подтверждения parser:

category
→ product URLs
→ product pages
→ raw HTML
→ parser
→ image download
→ final list

Так scraper остается ответственным за сеть, а parser — за HTML.

4. Интеграция

main.py менять не нужно.

Существующий поток должен остаться:

PlaywrightEngine
→ fetch_page_data(engine)
→ exporter

browser.py, config.py, utils.py, exporter.py не дублируются.

5. Тест на 2 товара

Проверить минимум:

товар со скидкой;

товар без скидки;

title;

URL;

Breadcrumb;

short description;

Description;

gallery;

image names;

Price;

Sale price;

Specs;

пустые отсутствующие значения;

физическое наличие скачанных изображений;

соответствие количества imageurl и image_name.

6. Проверка CSV

Особенно проверить:

нет лишних колонок
нет отсутствующих обязательных колонок
порядок колонок соответствует DS-PRK-Scraper.json
каждая характеристика находится в отдельной колонке
нет смешивания характеристик

Только после успешного теста из 2 товаров имеет смысл масштабировать scraper.

7. Что остается неизвестным

Это важно отделить от подтвержденных фактов.

Подтверждено

используется PlaywrightEngine;

API не подтвержден;

network.har пуст;

category URL известен;

pagination через ?p=N подтверждена;

li.item подтвержден;

.product-name подтвержден;

.price-box подтвержден;

.old-price подтвержден;

.special-price подтвержден;

.breadcrumbs подтвержден;

.short-description подтвержден;

текущий каталог ранее показывал 429 товаров / 12 страниц;

изображения нужно физически скачивать;

первый запуск — 2 товара;

sale без скидки должен быть пустым;

отсутствующие характеристики должны быть пустыми;

описание должно быть текстом;

out-of-stock нужно включать;

порядок CSV-колонок фиксирован.

Не подтверждено

Полный DOM галереи изображений.

Как получить full-size image URL вместо thumbnail.

Точный DOM-селектор Description.

Точный DOM-селектор Specs.

Формат HTML отдельных строк Specs.

Как обрабатываются повторяющиеся имена характеристик.

Есть ли у всех товаров одинаковый product template.

Как представлен out-of-stock в HTML.

Как именно клиент ожидает локальные image filenames.

Точные два тестовых URL.

Точный API интерфейс PlaywrightEngine.

Точный контракт текущего main.py для fetch_page_data().

Что нельзя делать

Нельзя:

реконструировать Google Sheet;

менять DS-PRK-Scraper.json;

придумывать отсутствующие колонки;

придумывать CSS-селекторы для отсутствующих частей HTML;

считать checkpoint.json доказательством корректности старого CSV;

использовать requests/httpx;

добавлять Selenium;

добавлять Scrapy;

добавлять API layer;

менять main.py;

делать сетевые запросы из parser.py.

Краткое резюме
Технология

PlaywrightEngine → HTML → BeautifulSoup → dict → list[dict] → exporter.py → CSV

API не используется, поскольку он не подтвержден, а существующий framework уже фиксирует Playwright.

Основные функции scraper.py

fetch_page_data(engine) — основной orchestration;

fetch_listing_page(engine, url) — получение HTML категории;

fetch_product_page(engine, url) — получение HTML товара;

download_images(...) — физическое скачивание изображений.

random_delay() берется из utils.py, собственная реализация не нужна.

Основные функции parser.py

parse_listing(html);

parse_single_item(card);

parse_product(html);

parse_specs(...);

extract_image_urls(...);

normalize_text(...).

Итоговая структура

Финальный dict строится строго по DS-PRK-Scraper.json, а динамические характеристики превращаются в отдельные CSV-колонки по правилу:

текст до ":" → имя колонки
текст после ":" → значение

Отсутствующие значения — пустые строки.

Главные риски

Главный блокер — неполный product-page.html.

До получения полной product page нельзя достоверно зафиксировать extraction для:

gallery;

imageurl;

image_name;

Description;

Specs;

Spec_detail.

При этом архитектуру уже можно считать определенной: scraper.py занимается только браузером/навигацией/скачиванием, parser.py — только разбором полученного HTML, а существующее ядро проекта остается без изменений.

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
 },
 {
  "Breadcrumb": "Koelkasten&Kisten"
 }


--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: category-page.html ---

<ul class="products-grid category-products-grid itemgrid itemgrid-adaptive itemgrid-3col centered hover-effect equal-height">


    Здесь карточки в блоках li , пример page.html
</ul>

--- ФАЙЛ: checkpoint.json ---
{
  "run_id": "run_20260811_152654",
  "status": "completed",
  "current_page": 12,
  "current_url": null,
  "processed_count": 429,
  "exported_count": 429,
  "timestamp": "2026-08-11T12:27:02.144976+00:00",
  "extra_metadata": {
    "total_pages": 12,
    "processed_count": 429,
    "exported_count": 429
  }
}

--- ФАЙЛ: cookies.json ---
[
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
    "name": "_ga",
    "value": "GA1.1.1255001230.1786435293",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1821011213.678069,
    "httpOnly": false,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "frontend",
    "value": "u2g21sufdr9pv6kkecgqpcce73",
    "domain": ".www.professionele-koeling.nl",
    "path": "/",
    "expires": 1786454813.087062,
    "httpOnly": true,
    "secure": false,
    "sameSite": "Lax"
  },
  {
    "name": "frontend_cid",
    "value": "8H62gWeA6I6pbTqx",
    "domain": ".www.professionele-koeling.nl",
    "path": "/",
    "expires": 1786454813.08629,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  },
  {
    "name": "cf_clearance",
    "value": "vZo6dSsLrZ8MS9kNF0MwdB._Ov7TjTh0j2sjNfIrKsM-1786451127-1.2.1.1-E0Zp5oKbK6cmjL8EzrUTKapj4UuuHHpwSzJQh_qYVz1ftWC5l2Hdcyud5_GcSPtX4T2kWgIK1glfZn.bi6pxdTIaKLdmnHeNomgLZc1LLYPlfbJn5LvTXaX98eWuvEJ3xA1p5XHl2AtqkVIci3w.mK1P6hq1WEwopHXdjX_ryIx1iRvR2LFluf_KxxL8X9svj6H5eMkKieghj6NHyF.T8OOsRXSiCo3BgpONrp8as6k1wuYD8l7J06ZaEc971m5Etfju.Pxl7xncRZj5q_qmCWI8Cf6f0Ke6YOtL13b7jri0Z36QJcb9_Fq9HD8VHReBRlsH3uavQ9p8f5aeOMbrNwhbBoi2uA7fTFg5qJSVY5o",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1817987165.083069,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None",
    "partitionKey": "https://professionele-koeling.nl",
    "_crHasCrossSiteAncestor": false
  },
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
    "name": "_ga_3X7F7CBMN7",
    "value": "GS2.1.s1786451165$o2$g1$t1786451213$j12$l0$h0",
    "domain": ".professionele-koeling.nl",
    "path": "/",
    "expires": 1821011213.67736,
    "httpOnly": false,
    "secure": false,
    "sameSite": "Lax"
  }
]

--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---
API нет , и сайт на JS

ВАЖНО: DS-PRK-Scraper.json — это КОРРЕКТНАЯ и ФИНАЛЬНАЯ спецификация. Значения вроде "if multipli seperated by comma" и "evertything before the : is the header" — это инструкции по заполнению полей, а НЕ повреждённые данные. Файл валиден. Используй его как есть. НЕ запрашивай "оригинальную версию" и НЕ считай его повреждённым.


Какой итоговый формат нужен:CSV

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

Файл `app/scraper.py` — перепиши его полностью под план проекта:



---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/scraper.py` (модуль: **scraper**).

---

## КОНТРАКТ main.py (НЕИЗМЕНЯЕМЫЙ, ВЫСШИЙ ПРИОРИТЕТ)

`main.py` уже написан, протестирован и НЕ ПОДЛЕЖИТ изменению. Он импортирует и вызывает:

```python
from app.scraper import fetch_page_data
from app.parser import parse_listing, parse_html_data

# main.py делает:
with PlaywrightEngine() as engine:
    raw_pages_content = fetch_page_data(engine)  # List[str]

# Затем:
page_records = parse_listing(html)         # один HTML → List[Dict]
scraped_results = parse_html_data(raw_pages_content)  # List[str] → List[Dict]
```

### Обязательные сигнатуры

**scraper.py:**
```python
def fetch_page_data(engine: PlaywrightEngine) -> List[str]:
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

- **ИГНОРИРУЙ** рекомендации из analysis/plan по выбору HTTP-движка (requests, httpx и т.д.). Движок ВСЕГДА `PlaywrightEngine` — он передаётся в `fetch_page_data()` уже готовым.
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
