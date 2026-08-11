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

- **Утвержденная стратегия (Шаг 1):** Ниже — анализ только на основании предоставленного контекста и файлов. Я не буду восполнять отсутствующие данные предположениями. Там, где вывод нельзя подтвердить имеющимися материалами, это явно отмечено.

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
 },
 {
  "Breadcrumb": "Koelkasten&Kisten"
 }


--- ФАЙЛ: answers.txt ---


--- СЖАТЫЙ HTML: category-page.html ---
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
    raw_pages_content = fetch_page_data(engine)
```

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

**Пример:**

Клиент запускает main.py

main.py инициализирует браузер через browser.py

main.py вызывает scraper.fetch_listing()

scraper.py загружает страницу со списком товаров через Playwright

scraper.py передает сырой HTML в parser.parse_listing()

parser.py использует BeautifulSoup для извлечения карточек товаров

parser.py вызывает parse_single_item() для каждой карточки

parser.py возвращает список словарей (list[dict]) в scraper.py

scraper.py возвращает список в main.py

main.py передает список в exporter.save_to_csv()

### 2. Проектирование `app/scraper.py` (Сетевой сбор)

* **2.1. Интерфейс функций

Опиши контракт каждой функции, которую будет содержать `scraper.py`.
Предложи необходимый набор функций.

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