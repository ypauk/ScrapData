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


Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает данные о товарах из категории `Koelkasten&Kisten`.


На текущем этапе требуется **не полный scrape, а тестовый результат для 2 товаров**. При этом структура результата уже окончательно определена файлом `DS-PRK-Scraper.json`: нельзя менять названия, порядок или состав полей.


Из каждого товара необходимо собрать:



- URL;

- Breadcrumb;

- Title;

- Short description;

- URL всех изображений;

- имена изображений;

- обычную цену;

- Sale price;

- полное описание как чистый текст;

- характеристики `Specs`;

- отдельные значения `Spec_detail`.


Изображения нужно **скачивать**, а не только сохранять их URL. Если скидочной цены нет — поле Sale price оставляется пустым. Отсутствующие характеристики также оставляются пустыми. GitHub+1


**Уверенность: высокая** — требования явно зафиксированы в предоставленном prompt.



## 2. Какой конечный результат нужен


**JSON.**


Причём структура каждого объекта должна строго соответствовать `DS-PRK-Scraper.json`, включая исходный порядок колонок/полей.


Текущий тестовый результат — **2 товара**, а не все 429 товаров категории. На сайте сейчас действительно отображается 429 товаров, по 36 на странице, с обычной пагинацией. Professionele Koeling


Дополнительно должны быть сохранены сами изображения.



## 3. Как лучше решить задачу


### Рекомендация: PlaywrightEngine + парсинг HTML


Это наиболее подходящий вариант.


Причины:



- В prompt прямо указано, что `scraper.py` получает готовый **PlaywrightEngine**, поэтому переходить на `requests` вместо Playwright нельзя.

- Сам сайт сообщает, что для полной функциональности требуется JavaScript. Professionele Koeling

- При этом основные данные товара фактически присутствуют в HTML после загрузки страницы: название, описание, цены и характеристики доступны непосредственно в DOM. Например, для Polar DM071 все эти данные находятся на product page. Professionele Koeling

- Категория содержит прямые ссылки на product pages, поэтому после получения списка товаров можно перейти к нужным страницам.

- Playwright также позволит надёжнее получить реальные URL изображений и скачать их в случае, если изображения зависят от браузерной загрузки.

- Уже имеющийся `cf_clearance` cookie показывает, что при доступе к сайту может участвовать Cloudflare, поэтому браузерный подход безопаснее с точки зрения совместимости. GitHub


**Оптимальная стратегия:** использовать PlaywrightEngine для открытия category/product pages и получения итогового HTML, а данные извлекать из HTML/DOM. Не использовать браузерную автоматизацию там, где она не нужна — например, не имитировать клики по интерфейсу без необходимости.


**Уверенность: высокая.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Не рекомендую как основной механизм.


Несмотря на то что текущие страницы содержат много данных в HTML, проект уже зафиксирован на PlaywrightEngine, а сайт явно рассчитан на JavaScript. Использование requests потребовало бы отдельно решать вопросы cookies, Cloudflare и возможного различия между browser-rendered и обычным response.


### Selenium


Работать может, но преимуществ перед уже предусмотренным PlaywrightEngine нет. Это лишнее усложнение.


### Scrapy


Для большого crawl Scrapy был бы интересен, но здесь уже есть browser engine, а задача относительно небольшая. Добавление Scrapy не даст необходимого преимущества.


### API


Не рекомендую строить решение вокруг API: в предоставленных материалах указано `API нет`, а `network.har` пуст. Наличие API не подтверждено.


### GraphQL


Признаков GraphQL нет.


### Полноценная browser automation


Также не нужна. Не требуется кликать по каждому элементу интерфейса — достаточно загрузить страницы и извлечь данные из DOM.



## 5. Анализ сайта


ВозможностьОценкаОбоснованиеJavaScript Rendering**Есть / используется**Сайт сам выводит сообщение о необходимости JavaScript; при этом HTML уже содержит основной контент. Professionele KoelingReact**Не подтверждено**Признаков React в предоставленных данных нетVue**Не подтверждено**Признаков нетAngular**Не подтверждено**Признаков нетAPI**Не обнаружено**`notes.txt` прямо сообщает «API нет»GraphQL**Не обнаружено**Данных для подтверждения нетInfinite Scroll**Нет признаков**Используется обычная paginationPagination**Есть**429 товаров, 36 на страницу, присутствуют `?p=2`, `?p=3` и т. д. Professionele KoelingLogin**Не нужен**На сайте существует account/login, но product pages доступны без авторизации. Professionele KoelingCookies**Есть**Передан `cookies.json`, включая cookies домена сайтаJWT**Не обнаружен**Нет данных о JWTBearer Token**Не обнаружен**Нет данныхCAPTCHA**Есть reCAPTCHA на review form**На product page присутствует reCAPTCHA для отправки отзыва; это не означает CAPTCHA для обычного scraping. Professionele KoelingCloudflare**Вероятно есть**Передан `cf_clearance` cookieRate Limits**Неизвестно**В предоставленных материалах нет измеренийDownload Files**Нужно**Требуется скачать изображения товаровUpload Files**Не требуется**Нет такого требованияLazy Loading**Не подтверждено**Нужна проверка реального DOM/сетевых запросов при загрузке изображенийWebSocket**Не подтверждено**`network.har` пустXHR/Fetch**Не подтверждено**Нет HAR/сетевых данныхSitemap**Есть ссылка на Sitemap**Ссылка присутствует в footer product page. Professionele Koelingrobots.txt**Не удалось подтвердить**Прямой запрос в текущей проверке вернул internal error
### Важное наблюдение


Переход на product page действительно даёт необходимые данные. Например, для Polar DM071 доступны цена, скидочная цена, описание и отдельные характеристики вроде `Merk`, `Kleur`, `Breedte`, `Diepte`, `Hoogte` и т. д. Professionele Koeling


Для Polar GE579 также доступны полное описание и блок характеристик, включая `Artikelnummer`, `Inhoud`, `Temperatuurbereik`, `Afmetingen`, `Energieklasse`, `Aansluitwaarde`, `Klimaatklasse`, `Koelmiddel` и `Gewicht`. Professionele Koeling


**Уверенность по HTML-структуре: высокая.
Уверенность по внутренней JS/network-механике: средняя**, поскольку HAR не предоставлен.



## 6. Что необходимо собрать до начала разработки


**Критически необходимой дополнительной информации сейчас практически нет.**


Уже предоставлены:



- `DS-PRK-Scraper.json` — authoritative specification;

- category HTML;

- product HTML;

- pagination HTML;

- cookies;

- notes;

- checkpoint;

- описание требуемого результата;

- правила обработки отсутствующих данных;

- требование скачать изображения.


Поэтому **не нужно просить оригинальную Google Sheet** — prompt прямо запрещает это, и JSON считается окончательной спецификацией.


Единственное, что желательно проверить непосредственно перед реализацией:



- фактический HTML/DOM изображения на product page;

- наличие нескольких изображений у товара;

- URL оригинального изображения против thumbnail/cache URL;

- фактический механизм загрузки изображений;

- можно ли использовать текущие cookies или scraper должен корректно работать без них.


Это уже техническая проверка, а не недостающая бизнес-информация.



## 7. Возможные сложности


### 1. Cloudflare


Наличие `cf_clearance` означает потенциальную защиту от автоматизированного доступа. Если cookie протухнет или Cloudflare начнёт выдавать challenge, scraper может перестать получать страницы.


**Риск: средний.**


### 2. JavaScript


Сайт может менять DOM после первоначальной загрузки. Поэтому желательно извлекать данные после корректного завершения загрузки страницы.


**Риск: средний.**


### 3. Изображения


Требуется не просто URL, а скачивание файлов. Нужно отличать thumbnail/cache URL от оригинального изображения.


**Риск: средний.**


### 4. Разнородность характеристик


У товаров разные наборы характеристик. Например, у DM071 присутствуют одни значения, у GE579 — другие. Professionele Koeling+1


Следовательно, нельзя предполагать, что каждый товар содержит одинаковые характеристики.


При отсутствии значения поле должно оставаться пустым согласно требованиям клиента.


**Риск: средний.**


### 5. Цены


На странице одновременно присутствуют обычная и специальная цена (`Van` / `Voor`). Их нельзя перепутать. Professionele Koeling


### 6. Пагинация


Сейчас категория содержит 429 товаров и 36 товаров на страницу. Для будущего полного scrape потребуется корректно пройти все страницы. Professionele Koeling


Для текущего теста это не является проблемой, поскольку нужны только 2 товара.


### 7. Изменение HTML


Magento-подобная структура сайта может измениться, что потенциально сломает CSS/XPath-селекторы.


**Риск: средний.**


### 8. Cookie expiration


Предоставленные cookies имеют срок действия. Их нельзя считать вечным способом обхода Cloudflare.



## 8. Что нужно уточнить у клиента


**На текущем этапе блокирующих вопросов нет.**


Все существенные бизнес-требования уже отвечены в `notes.txt`:



- формат — JSON;

- сейчас 2 товара;

- изображения скачивать;

- Sale price при отсутствии — пустое;

- отсутствующие характеристики — пустые;

- описание — plain text;

- out-of-stock товары включать;

- порядок полей сохранять;

- JSON содержит окончательный список полей.


Единственное потенциальное уточнение, которое **можно** задать, но оно не блокирует тестовую разработку:



При скачивании нескольких изображений следует сохранять оригинальные файлы в их исходном формате и использовать имя файла из URL/страницы, если оно доступно?



Причина вопроса — `image_name` явно требует имена изображений, но точное правило формирования имени в спецификации не задано.


**Уверенность: высокая, что разработку можно начать без ответа клиента.**



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **BeautifulSoup** — для удобного разбора полученного HTML

- стандартные средства Python для обработки JSON и файлов изображений


Другие технологии на данном этапе не нужны.



## 10. План разработки


### Этап 1 — проверка двух тестовых товаров


**Цель:** подтвердить, что необходимые поля извлекаются из product pages.


**Ожидаемый результат:** данные двух товаров полностью соответствуют `DS-PRK-Scraper.json`.


**Зависимости:** PlaywrightEngine, предоставляемый проектом.



### Этап 2 — извлечение ссылок товаров


**Цель:** получить URL товаров из категории.


**Ожидаемый результат:** корректные product URLs без ручного перечисления товаров.


**Зависимости:** HTML category page.



### Этап 3 — сбор product data


**Цель:** собрать Title, Breadcrumb, descriptions, prices и характеристики.


**Ожидаемый результат:** один корректный JSON-объект на товар.


**Зависимости:** product pages.



### Этап 4 — обработка характеристик


**Цель:** преобразовать блок `Specs` / `Spec_detail` согласно точной инструкции из JSON.


**Ожидаемый результат:** каждое требуемое поле находится отдельно, без смешивания нескольких характеристик в одной колонке.


**Зависимости:** структура `DS-PRK-Scraper.json`.



### Этап 5 — изображения


**Цель:** получить URL изображений и скачать сами файлы.


**Ожидаемый результат:** `imageurl` и `image_name` заполнены согласно спецификации, изображения физически сохранены.


**Зависимости:** проверка реального DOM image gallery.



### Этап 6 — тестовая валидация


**Цель:** проверить первые 2 товара.


**Ожидаемый результат:** тестовый JSON без лишних/пропущенных/объединённых полей.


**Зависимости:** завершение этапов 1–5.



### Этап 7 — подготовка к полному scrape


**Цель:** после подтверждения тестового файла перейти к остальным товарам.


**Ожидаемый результат:** возможность обработать всю категорию с пагинацией.


**Зависимости:** подтверждение клиентом тестовых 2 товаров.



## 11. Оценка сложности


ПараметрОценкаСложность**5/10**Разработка тестовой версии**3–5 часов**Полная версия**6–10 часов**Вероятность блокировок**средняя**Вероятность необходимости браузера**высокая — ~80%**Вероятность изменения сайта в будущем**средняя**Общий риск**средний**
Оценка полной версии предполагает, что не возникнет нового Cloudflare challenge и структура product pages останется примерно такой же.


Главная техническая неопределённость — не сами текстовые данные, а **работа с изображениями + Cloudflare/JS**.



## 12. Можно ли решить проще


**Да.**


Самое важное упрощение — не пытаться строить сложный scraper.


Для текущего теста достаточно:


**category page → 2 product URLs → product pages → HTML parsing → JSON + image download.**


Не требуется:



- API;

- база данных;

- Scrapy;

- Selenium;

- отдельная архитектура для API;

- сложная система авторизации;

- обход infinite scroll;

- параллельный distributed crawler.


Кроме того, для полного scrape нет необходимости вручную обходить все товары: category page уже предоставляет обычную пагинацию (`?p=2`, `?p=3` и т. д.). Professionele Koeling


Ещё одно потенциальное упрощение — **не использовать браузерные клики для каждой характеристики**. Если данные уже присутствуют в DOM, их следует извлекать напрямую.


При этом заменять PlaywrightEngine на `requests` нельзя: это прямо запрещено условиями проекта.



## 13. Итоговая рекомендация


**Рекомендуемое решение:** Python + предоставляемый проектом PlaywrightEngine + HTML parsing.


Это оптимально, потому что:



- API не обнаружен;

- сайт имеет JavaScript;

- product data фактически доступна в HTML/DOM;

- есть обычная pagination;

- авторизация для товаров не требуется;

- текущая задача ограничена 2 товарами;

- JSON-схема уже полностью определена;

- изображения необходимо скачивать;

- добавление Scrapy/Selenium/API сделает решение сложнее без очевидной пользы.


Текущая структура сайта подтверждает такой подход: category page содержит ссылки на товары и цены, а product page содержит описания и характеристики. Professionele Koeling+2Professionele Koeling+2


**Что необходимо получить перед началом:** обязательных дополнительных данных нет. Желательно только технически проверить DOM галереи изображений и формат оригинальных image URLs.


**Можно ли переходить к написанию кода:** **да, можно начинать тестовую реализацию без ожидания ответа клиента.** Бизнес-требования достаточно определены.


При этом **к полному scrape всех товаров переходить следует только после проверки/подтверждения тестового JSON с 2 товарами**, как и требует клиент.


**Итоговая уверенность: высокая (~85–90%).** Основные требования и структура данных определены однозначно; оставшаяся неопределённость касается преимущественно технического поведения изображений, Cloudflare и динамики сайта.
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