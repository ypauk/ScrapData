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