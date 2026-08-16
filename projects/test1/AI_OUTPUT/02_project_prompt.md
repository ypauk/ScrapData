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


Клиент хочет получить **тестовый JSON-файл с данными о 2 товарах** с сайта Professionele-Koeling.nl, строго в соответствии со структурой `DS-PRK-Scraper.json`. После проверки теста предполагается возможность расширить сбор на весь сайт/категорию.


Нужно собирать:



- URL;

- Breadcrumb;

- название товара;

- краткое описание;

- URL всех изображений;

- имена изображений;

- обычную цену;

- цену со скидкой;

- полное описание **как чистый текст**, без HTML;

- характеристики, причём каждая характеристика должна попасть в отдельную колонку;

- отсутствующие значения оставлять пустыми;

- товары без скидки включать, но `Sale price` оставлять пустым;

- товары, которых нет в наличии, также включать;

- порядок и названия колонок не менять.


Авторитетной спецификацией является именно `DS-PRK-Scraper.json`; восстанавливать Google Sheet или трактовать его как повреждённый не требуется.


**Уровень уверенности: высокий.** Структура и правила явно заданы в исходном prompt. GitHub



## 2. Какой конечный результат нужен


Основной результат — **JSON**.


На текущем этапе клиент хочет только **2 товара** как тестовый результат. Изображения необходимо не только обнаружить, но и **скачать**.


При этом структура JSON должна строго соответствовать полям из `DS-PRK-Scraper.json`:



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


Значения вроде `if multipli seperated by comma` и `evertything before the : is the header` — это инструкции по заполнению, а не данные.



## 3. Как лучше решить задачу


### Рекомендация: Playwright + парсинг HTML


Наиболее подходящий вариант — **Playwright для получения страниц + обычный HTML parsing для извлечения данных**.


Причины:



- В предоставленных заметках прямо указано, что сайт работает с JavaScript.

- В framework проекта `scraper.py` уже получает готовый `PlaywrightEngine`, поэтому переход на `requests` как основной механизм здесь неуместен.

- Категорийная страница содержит ссылки на товары и цены, а страницы товаров содержат необходимые дополнительные поля.

- На сайте есть пагинация: текущая страница показывает 36 товаров и ссылки на следующие страницы. Professionele Koeling

- Текущая веб-страница действительно предупреждает, что JavaScript должен быть включён для полной функциональности. Professionele Koeling


При этом **не нужно автоматически усложнять scraper браузерной автоматизацией всех действий пользователя**. Playwright здесь прежде всего нужен как надёжный механизм загрузки страницы; после получения DOM данные можно извлекать обычным HTML-парсингом.


Для текущего теста достаточно:


**категория → ссылки на первые товары → страницы 2 выбранных товаров → извлечение данных → скачивание изображений → JSON.**



## 4. Почему остальные варианты хуже


### requests + BeautifulSoup


Как самостоятельный основной подход не рекомендую.


Главная причина — по предоставленной информации сайт использует JavaScript, а framework уже зафиксировал использование `PlaywrightEngine`.


Однако BeautifulSoup/аналогичный HTML parser **может быть полезен после загрузки страницы Playwright**, потому что сам по себе он не является альтернативой браузеру, а решает другую задачу — разбор уже полученного HTML.


### Scrapy


Избыточен для текущего задания.


429 товаров/страниц — это не тот объём, ради которого обязательно нужен полноценный Scrapy-проект. Для теста из двух товаров он тем более не оправдан.


### Selenium


Работать может, но преимуществ перед уже предусмотренным PlaywrightEngine нет.


### API


По предоставленным данным API не обнаружен, а в `notes.txt` прямо указано: **«API нет»**. `network.har` также пустой.


Искать и строить решение вокруг API сейчас оснований нет.


### GraphQL


Признаков GraphQL нет.


### Database


Не нужна. Клиент требует JSON, а не постоянное хранилище.


### Прямой парсинг только category page


Недостаточен для полного результата: категория содержит название, ссылку, изображение и цены, но предоставленный `product-page.html` показывает, что дополнительные требуемые поля находятся на странице товара. Например, там присутствуют breadcrumb, short description и подробности товара. Professionele Koeling


**Уровень уверенности: высокий для Playwright; средний для утверждения, что абсолютно все поля требуют product page, поскольку предоставленный HTML является сжатым и не содержит полной страницы.**



## 5. Анализ сайта


### JavaScript Rendering


**Да, присутствует.**


Предоставленный `notes.txt` прямо говорит, что сайт на JS. Кроме того, текущая страница сайта сообщает о необходимости JavaScript для полной функциональности. Professionele Koeling


**Уверенность: высокая.**


### React


**Не установлено.**


В предоставленных материалах нет признаков React.


**Уверенность: низкая/недостаточно данных.**


### Vue


**Не установлено.**


**Уверенность: низкая/недостаточно данных.**


### Angular


**Не установлено.**


**Уверенность: низкая/недостаточно данных.**


### API


Согласно `notes.txt`, API нет.


`network.har` пустой, поэтому дополнительного подтверждения через HAR нет.


**Уверенность: средняя.** Корректнее говорить: *доступного/обнаруженного API в предоставленных материалах нет*, а не доказывать абсолютное отсутствие любого внутреннего endpoint.


### GraphQL


Признаков нет.


**Уверенность: средняя.**


### Infinite Scroll


**Нет признаков.**


Вместо этого используется обычная пагинация.


### Pagination


**Да.**


Category page показывает 36 товаров на странице и ссылки `p=2`, `p=3`, `p=4` и т.д. Professionele Koeling


В исходных данных указано 429 товаров и 1 обработанная страница в checkpoint; текущая версия сайта показывает то же наличие пагинации, хотя число товаров может меняться. Professionele Koeling


**Уверенность: высокая.**


### Login


Для просмотра товаров login не требуется.


На сайте существует пользовательский аккаунт, но предоставленные страницы доступны без авторизации. Professionele Koeling


**Уверенность: высокая для scraping public product pages.**


### Cookies


**Да.**


В `cookies.json` присутствуют cookies сайта, включая:



- `_ga`;

- `_gcl_au`;

- `frontend`;

- `frontend_cid`;

- `cf_clearance`.


Особенно важен `cf_clearance`.


### JWT


**Не обнаружен.**


### Bearer Token


**Не обнаружен.**


### CAPTCHA


Явной CAPTCHA в предоставленных материалах нет.


### Cloudflare


**Да, есть признаки Cloudflare.**


Наличие cookie `cf_clearance` является сильным признаком прохождения Cloudflare challenge.


Однако из имеющихся материалов нельзя утверждать, что Cloudflare будет требовать challenge при каждом запуске scraper.


**Уверенность: высокая в наличии Cloudflare-механизма; средняя в вероятности challenge при каждом запуске.**


### Rate Limits


Явный лимит не указан.


Но поскольку есть Cloudflare, большое количество последовательных запросов потенциально может привести к challenge/block.


**Уверенность: средняя.**


### Download Files


**Да — требуются изображения.**


Клиент явно указал, что изображения необходимо скачивать.


### Upload Files


Для scraping задачи признаков необходимости upload нет.


### Lazy Loading


**Не установлено.**


В предоставленном HTML обычное изображение присутствует через `<img src="...">`.


### WebSocket


**Не обнаружен.**


### XHR/Fetch


Достоверно определить по пустому `network.har` невозможно.


### Sitemap


Попытка проверить `robots.txt` и `sitemap.xml` через текущий веб-доступ не дала содержимого, поэтому наличие/отсутствие sitemap **нельзя достоверно установить**.



## 6. Что необходимо собрать до начала разработки


**Для самого тестового запуска дополнительная информация от клиента не требуется.** Уже предоставлены:



- authoritative output specification;

- URL категории;

- пример category HTML;

- пример product HTML;

- pagination;

- cookies;

- checkpoint;

- правила обработки отсутствующих значений;

- требуемый JSON;

- требование скачать изображения.


Но перед **полным production scrape** желательно получить/подтвердить:



- **Какие именно 2 товара использовать для теста.**
Если клиент не выбирает, логично взять первые два товара из текущего листинга — `Polar DM071` и `Cavanova 605002`. На текущей странице они действительно идут первыми. Professionele Koeling

- **Ожидаемый пример итогового JSON**, если клиент хочет проверить не только структуру, но и точное форматирование значений. При этом это не блокирует разработку, поскольку структура уже задана `DS-PRK-Scraper.json`.

- Для полноценного запуска — подтверждение, что предоставленные cookies являются допустимым способом доступа и при необходимости могут быть обновлены.

- Если Cloudflare начнёт требовать интерактивный challenge — понадобится решение вопроса с устойчивым способом получения валидной browser session.


**Не нужно запрашивать оригинальную Google Sheet:** prompt прямо запрещает это и говорит, что JSON является полной спецификацией.



## 7. Возможные сложности


### 1. Cloudflare


Главный технический риск.


`cf_clearance` присутствует в предоставленных cookies, но такие cookies могут истекать или становиться недействительными.


### 2. JavaScript


Сайт требует browser-based loading для полной функциональности, поэтому простой HTTP scraper может оказаться ненадёжным.


### 3. Изменение HTML


CSS selectors и структура Magento-подобного HTML могут измениться.


Особенно важно не строить парсер исключительно на длинных CSS/XPath цепочках.


### 4. Несовпадение структуры товаров


У разных товаров некоторые характеристики могут отсутствовать.


По инструкции клиента в таком случае значение должно оставаться пустым.


### 5. Изображения


Необходимо различать:



- URL изображения;

- имя файла;

- фактическое скачивание изображения.


Также у товара может быть несколько изображений, причём они должны сохраняться через запятую в соответствующих полях.


### 6. Характеристики


`Spec_detail` требует преобразовать пары вида:


`Artikelnummer: GE579`


в отдельные поля, где часть **до : является header**.


Это потенциально самая чувствительная часть схемы: нужно сохранить строгий порядок колонок и не смешивать несколько характеристик в одну колонку.


### 7. Цена


На странице присутствуют `old-price` и `special-price`. Например, для `Polar GE579` текущая страница показывает `€255,99` и `€229,00 Excl. BTW`. Professionele Koeling


Следовательно:



- `Price` = обычная/старая цена;

- `Sale price` = специальная цена.


Если special price отсутствует, `Sale price` должен быть пустым.


### 8. Пагинация


Сейчас категория содержит сотни товаров и несколько страниц. При полном scraping необходимо корректно пройти все страницы, не задублировав товары. Professionele Koeling


### 9. Динамика сайта


Содержимое и количество товаров могут меняться. Текущий сайт уже отличается от некоторых значений checkpoint, поэтому checkpoint нельзя считать источником актуального каталога.



## 8. Что нужно уточнить у клиента


Для **текущего теста из 2 товаров** критических вопросов нет.


Перед переходом к полному scraping я бы задал клиенту только следующие вопросы:



- **Подтвердите, что для теста использовать первые 2 товара категории — Polar DM071 и Cavanova 605002?**

- **После успешного теста нужно собирать все товары категории Koelkasten&Kisten (сейчас сайт показывает 429 товаров) или полный сайт/другие категории?**
В исходном описании есть некоторая неоднозначность между «all required info» и текущим требованием «сначала только 2 товара». Текущий этап однозначно ограничен двумя товарами. Professionele Koeling

- **Достаточно ли текущих правил для именования скачанных изображений, или есть отдельное требование к имени локального файла?**


Других вопросов, блокирующих начало разработки теста, нет.



## 9. Рекомендуемый стек технологий



- **Python**

- **Playwright**

- **HTML parser / BeautifulSoup**

- **JSON**

- **Playwright download/browser context для изображений**


Без API, базы данных, Selenium или Scrapy.



## 10. План разработки


### Этап 1 — Проверка доступа


**Цель:** убедиться, что Playwright может стабильно открыть category и product pages.


**Результат:** доступная browser session и корректно загруженный DOM.


**Зависимости:** предоставленные cookies, если они всё ещё необходимы.



### Этап 2 — Получение товаров из категории


**Цель:** определить ссылки на товары и отобрать 2 товара для теста.


**Результат:** две корректные product URLs.


**Зависимости:** успешная загрузка category page.



### Этап 3 — Сбор данных product page


**Цель:** получить все поля, предусмотренные authoritative JSON specification.


**Результат:** полный набор данных для каждого тестового товара, включая пустые значения там, где характеристика отсутствует.


**Зависимости:** product URLs.



### Этап 4 — Обработка характеристик


**Цель:** преобразовать характеристики в требуемые отдельные поля и сохранить порядок колонок.


**Результат:** структура точно соответствует `DS-PRK-Scraper.json`.


**Зависимости:** успешное извлечение product details.



### Этап 5 — Скачивание изображений


**Цель:** скачать все требуемые изображения и сформировать `imageurl` / `image_name`.


**Результат:** изображения физически сохранены и связаны с соответствующими товарами.


**Зависимости:** доступ к image URLs.



### Этап 6 — Формирование тестового JSON


**Цель:** создать результат ровно для 2 товаров.


**Результат:** тестовый JSON с двумя полностью обработанными товарами.


**Зависимости:** этапы 2–5.



### Этап 7 — Валидация


**Цель:** проверить структуру, обязательные поля, порядок колонок, пустые значения и соответствие источнику.


**Результат:** готовый тестовый файл, который можно отправить клиенту.


**Зависимости:** тестовый JSON.



### Этап 8 — Расширение до полного scraping


**Цель:** после одобрения теста пройти pagination и собрать весь требуемый объём.


**Результат:** полный JSON.


**Зависимости:** одобрение тестового результата и подтверждение клиентом конечного scope.



## 11. Оценка сложности


ПараметрОценкаСложность**4/10**Разработка теста на 2 товара**2–4 часа**Полный scraper**5–9 часов**Вероятность блокировок**Средняя**Вероятность необходимости браузера**Высокая — ~90%**Вероятность изменения сайта в будущем**Средняя**Общий риск**Средний**
### Почему не выше 4/10


Сайт представляет собой обычный e-commerce каталог с понятной пагинацией и product pages. На текущей странице товары, ссылки и цены извлекаются достаточно прозрачно. Professionele Koeling


Основной фактор риска — не сложность данных, а **Cloudflare + JavaScript + возможные изменения HTML**.


Для текущего теста риск значительно ниже, чем для полного запуска.



## 12. Можно ли решить проще


**Да.**


Самое простое решение — использовать уже предоставленный **PlaywrightEngine**, но не делать сложную браузерную автоматизацию.


Оптимальная схема:


**Playwright → загрузка HTML → извлечение ссылок/данных → скачивание изображений → JSON.**


Не требуется:



- API;

- GraphQL;

- база данных;

- Scrapy;

- Selenium;

- отдельный сервис;

- сложная архитектура;

- обход всего сайта на текущем этапе.


### Ещё более простый вариант


Для теста можно вообще ограничиться **двумя product pages**, если их URL уже известны. Но для проверки полного процесса лучше получить их через category page, поскольку это одновременно проверяет discovery товаров.


Есть важный потенциальный shortcut: если все необходимые поля окажутся непосредственно в category HTML, переход на product pages можно будет сократить. Однако предоставленные материалы уже показывают, что product page содержит дополнительные данные, которых нет в карточке категории, поэтому **на данный момент переход на product pages остаётся рекомендуемым**.



## 13. Итоговая рекомендация


**Рекомендуемое решение: Python + PlaywrightEngine + HTML parsing + скачивание изображений + JSON.**


Это оптимальный вариант потому что:



- framework уже использует PlaywrightEngine;

- сайт использует JavaScript;

- API не предоставлен/не обнаружен;

- pagination обычная;

- данные находятся в HTML;

- итоговый формат уже однозначно определён;

- для текущего теста нужно обработать всего 2 товара.


Сначала следует сделать **тест на 2 товарах**, проверить абсолютно все поля и формат JSON, включая характеристики и изображения. Только после одобрения теста переходить к полному scraping.


**Критически необходимой дополнительной информации для начала теста сейчас нет.** Единственное полезное подтверждение клиента — какие именно 2 товара использовать; если он не укажет их, разумный выбор — первые два товара листинга: `Polar DM071` и `Cavanova 605002`. Текущая страница подтверждает их порядок. Professionele Koeling


**К написанию кода можно переходить после выбора/подтверждения двух тестовых товаров.** До этого этап анализа завершён; архитектуру и функции на данном этапе проектировать не следует, как и требовал исходный prompt.


**Итоговая уверенность: высокая.**
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