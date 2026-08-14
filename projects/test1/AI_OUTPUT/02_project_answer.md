Проектирование реализации scraper.py и parser.py для Professionele-Koeling.nl

Источник требований: 02_project_prompt.md. Задача — спроектировать решение без написания Python-кода, встроенное в существующее ядро проекта. Согласно спецификации, ядро (main.py, browser.py, config.py, exporter.py, utils.py) менять нельзя; проектируются только app/scraper.py и app/parser.py. 
GitHub

1. Полный поток данных

Выбранный подход: HTML + PlaywrightEngine + BeautifulSoup.

API не выбран, потому что:

HAR пустой;

API в предоставленных материалах не найден;

сайт использует обычные HTML-страницы товаров;

данные присутствуют в DOM. 
GitHub

Плюсы:

соответствует существующему фреймворку;

не требует новой архитектуры;

работает с JS-сайтом через уже существующий PlaywrightEngine;

подходит для тестовой выгрузки 2 товаров.

Минусы:

зависит от стабильности HTML-разметки;

возможны проблемы при изменениях Magento-шаблона;

требуется учитывать Cloudflare.

Поток:

URL категории
https://www.professionele-koeling.nl/koelkasten-kisten.html


↓


main.py запускает PlaywrightEngine


↓


scraper.scrape_data(engine)


↓


PlaywrightEngine открывает category page


↓


Получение HTML категории


↓


Извлечение URL товаров из HTML карточек


↓


Открытие product pages


↓


Получение HTML страниц товаров


↓


List[str]
[
  product_html_1,

Контракт проекта сохраняется:

scrape_data(engine) → List[str]

main.py получает только HTML, а бизнес-логика извлечения данных остается в parser.py. 
GitHub

2. Проектирование app/scraper.py
Ответственность модуля

scraper.py отвечает только за:

открытие страниц;

навигацию;

переходы между страницами;

получение HTML;

поиск URL товаров;

обход product pages.

Не отвечает за:

поиск цен;

извлечение характеристик;

формирование JSON;

очистку текста.

2.1 Интерфейс функций
Функция	Назначение	Входные параметры	Возвращаемое значение
scrape_data(engine)	Главная функция сбора данных. Открывает категорию, получает товары, возвращает HTML страниц товаров	engine: PlaywrightEngine	List[str]
_fetch_listing_html(engine, url)	Открывает страницу категории и получает HTML	engine, URL	str
_extract_product_urls(html)	Находит ссылки товаров в карточках категории	HTML категории	List[str]
_fetch_product_html(engine, url)	Открывает страницу товара и получает HTML	engine, URL товара	str
_get_next_page_url(html, current_url)	Определяет следующую страницу категории	HTML, текущий URL	URL или None
2.2 Алгоритм обхода
Категория

Источник:

https://www.professionele-koeling.nl/koelkasten-kisten.html

HTML карточки содержит:

URL товара;

изображение;

название;

цену.

Пример структуры:

li.item


 ├── a.product-image[href]
 ├── h2.product-name a[href]
 ├── old-price
 └── special-price

GitHub

Логика тестовой выгрузки

Для текущей задачи:

Открыть категорию


↓


Получить HTML


↓


Извлечь первые URL товаров


↓


Ограничить количество = 2


↓


Открыть 2 product pages


↓


Вернуть HTML товаров

Полный каталог пока не обходится.

Pagination

Для будущего полного scrape:

Использовать существующую Magento pagination:

?p=2
?p=3
?p=4

Следующая страница определяется через:

div.pager
a.next[href]

В предоставленном HTML присутствует:

koelkasten-kisten.html?p=2

GitHub

Для теста двух товаров pagination не нужна.

Ожидание элементов

Перед чтением страницы ожидать:

Категория:

ul.products-grid
li.item

Товар:

div.product-name
div.price-box
Lazy loading

Не использовать.

Причина:

В предоставленных данных изображения находятся непосредственно в:

img[src]

GitHub

random_delay()

Использовать из существующего:

app.utils.random_delay()

Места вызова:

после открытия категории;

между переходами на страницы товаров;

между большим количеством страниц при полном scrape.

3. Проектирование app/parser.py
Ответственность модуля

Только обработка HTML:

HTML
↓
BeautifulSoup
↓
dict
↓
list[dict]

Не выполняет:

HTTP;

Playwright;

скачивание страниц.

3.1 Интерфейс функций
Функция	Назначение	Входные параметры	Возвращаемое значение
parse_html_data(html_pages)	Обрабатывает список HTML страниц товаров	List[str]	List[dict]
parse_product(html)	Извлекает все поля одного товара	HTML товара	dict
_extract_breadcrumb(soup)	Извлекает Breadcrumb	BeautifulSoup	str
_extract_title(soup)	Извлекает название	BeautifulSoup	str
_extract_short_description(soup)	Извлекает краткое описание	BeautifulSoup	str
_extract_description(soup)	Извлекает описание без HTML	BeautifulSoup	str
_extract_prices(soup)	Извлекает Price и Sale price	BeautifulSoup	dict
_extract_images(soup)	Получает imageurl и image_name	BeautifulSoup	dict
_extract_specs(soup)	Извлекает характеристики	BeautifulSoup	dict
3.2 Спецификация полей

Финальная структура строго соответствует DS-PRK-Scraper.json. Добавлять новые поля нельзя. 
GitHub

URL

Источник:

текущий URL страницы товара

Если отсутствует:

""
Breadcrumb

Источник:

div.breadcrumbs

Извлекаются элементы:

Home
Koelkasten&Kisten
Product name

Результат:

Home > Koelkasten&Kisten > Polar GE579
Title

Источник:

div.product-name h1

Пример:

Polar GE579
Short description

Источник:

div.short-description

Обработка:

удалить HTML;

заменить <br>;

оставить чистый текст.

imageurl

Источник:

.product-image img[src]

Если несколько:

url1,url2,url3
image_name

Источник:

из URL изображения.

Пример:

polar_ge579.jpg

Несколько:

name1,name2
Price

Источник:

.old-price .price

Если отсутствует:

""
Sale price

Источник:

.special-price .price

Если скидки нет:

""

Правило подтверждено требованиями клиента. 
GitHub

Description

Источник:

основной блок описания товара.

Обработка:

удалить HTML;

сохранить переносы строк;

убрать служебные элементы.

Specs

Источник:

блок характеристик товара.

Если отсутствует:

""
Spec_detail

Формат:

Название характеристики: значение

Правило:

текст до ":" = название характеристики

Если характеристик нет:

""
3.3 Финальная структура результата

Пример одного объекта:

JSON
{
  "URL": "https://www.professionele-koeling.nl/product.html",
  "Breadcrumb": "Home > Koelkasten&Kisten > Polar GE579",
  "Title ": "Polar GE579",
  "Short description": "De Polar GE579 is een zwarte minibar koelkast...",
  "imageurl": "image1.jpg,image2.jpg",
  "image_name": "image1.jpg,image2.jpg",
  "Price": 255.99,
  "Sale price": 229,
  "Description ": "Polar GE579: Zwarte minibar koelkast...",
  "Specs": "",
  "Spec_detail": ""
}
4. Обработка ошибок
Сценарий	Действие
Timeout страницы	Повторить до 3 раз. Если не получилось — записать в лог и пропустить
HTTP 403	Записать в лог, остановить выполнение для проверки Cloudflare
CAPTCHA	Остановить scrape, требуется ручная проверка
Не найден элемент	Записать пустое значение "", продолжить
Нет цены	Вернуть пустое поле
Нет описания	Вернуть пустое поле
Пустая категория	Записать лог и завершить обход
Ошибка HTML parsing	Записать ошибку и пропустить товар
5. Оценка рисков
Риск	Статус
Cloudflare	Есть
Авторизация	Нет
Rate limiting	Не определен
CAPTCHA	Не подтверждена
Infinite Scroll	Нет
Shadow DOM	Нет данных
iframe	Нет данных
WebSocket	Нет
GraphQL API	Нет
Сложный DOM	Средний риск

Основной риск — Cloudflare и изменение HTML-разметки, а не сложность извлечения данных. В cookies присутствует cf_clearance. 
GitHub

6. Порядок реализации
1. parser.py

Первым реализовать парсер.

Причины:

не зависит от сети;

можно тестировать на сохраненном HTML;

позволяет быстро проверить соответствие DS-PRK-Scraper.json.

2. scraper.py

После готового parser:

подключить PlaywrightEngine;

проверить получение HTML;

добавить переходы по товарам.

3. Интеграция

Проверить цепочку:

main.py
 ↓
scraper.scrape_data(engine)
 ↓
parser.parse_html_data()
 ↓
exporter.save_to_json()
4. Тестирование

Проверить:

ровно 2 товара;

порядок полей;

отсутствие HTML;

пустые значения;

изображения;

цены;

JSON структуру.

7. Краткое резюме

Выбранная технология:

Python
+
PlaywrightEngine
+
BeautifulSoup
+
JSON exporter

scraper.py:

Основные функции:

scrape_data(engine)

_fetch_listing_html()

_extract_product_urls()

_fetch_product_html()

_get_next_page_url()

parser.py:

Основные функции:

parse_html_data()

parse_product()

_extract_title()

_extract_prices()

_extract_images()

_extract_specs()

Итоговая структура данных:

List[dict]


[
 {
  URL,
  Breadcrumb,
  Title ,
  Short description,
  imageurl,
  image_name,
  Price,
  Sale price,
  Description ,
  Specs,
  Spec_detail
 }
]

Главные риски:

Cloudflare.

Изменение DOM Magento.

Неизвестная точная структура блока характеристик Specs/Spec_detail. 
GitHub