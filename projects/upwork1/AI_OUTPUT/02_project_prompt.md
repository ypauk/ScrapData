# РОЛЬ

Ты — Senior Python Developer / Web Scraping Engineer. Твоя цель — спроектировать техническое решение для конкретного сайта клиента **БЕЗ написания самого кода**. 

Ты должен распределить логику по существующей функциональной структуре проекта.

---

# ВХОДНЫЕ ДАННЫЕ
- **Описание задачи клиента:** 
Задание от клиента, для теста собирем 2 шт товаров и скину емку файл csv
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

Данные с файла spreadsheet:
URL	Breadcrumb	Title 	Short description	imageurl	image_name	Price	Sale price	Description 	Specs	Spec_detail
https://www.professionele-koeling.nl/koelkasten-kisten.html	Home	Polar GE579	"De Polar GE579 is een zwarte minibar koelkast met
29 liter inhoud voor gebruik in hotelkamers, B&B's of ver-
gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken."	if multipli seperated by comma	if multiple seperated by comma	259	229	"Polar GE579: Zwarte 30 liter minibar koelkast voor de hotelkamer
De Polar GE579 is een zwarte minibar koelkast met een capaciteit van 29 liter. Deze koelkast maakt gebruik van het absorptie
koelsysteem i.p.v. een compressor. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor
toepassingen in hotelkamers, B&B 's en vergaderzalen.

Uitvoering:

Exterieur: zwaart
Interieur: roestvrijstaal
Werking: Werkt met warmtepomp in plaats van ventilatoren
Verwisselbare en afsluitbare deur
Verlichting: LED
Roosters (2x)
Vrijwel geruisloos
Vrijstaand of inbouw
Absorptie koelsysteem
Automatische ontdooiing
Specificaties:

Artikelnummer: GE579
Inhoud: 29 liter
Temperatuurbereik:  3-5°C bij een omgevingstemperatuur van 16°C
Temperatuurbereik: 5-8°C bij een omgevingstemperatuur van 25°C
Temperatuurbereik: 8-12°C bij een omgevingstemperatuur van 32°C
Afmetingen BxDxH: 400 x 430 x 530 mm
Energieklasse: F
Aansluitwaarde: 220-240 Volt, 60 watt
Klimaatklasse: N (omgevingstemperatuur tussen +16°C en +32°)
Koelmiddel: R600a
Gewicht: 13 kg
Bij het absorptiesysteem, dat geheel zonder bewegende delen kan worden uitgevoerd, wordt gebruik gemaakt van het verschijnsel dat sommige vloeistoffen (bijvoorbeeld water) sommige koelmiddelen (bijvoorbeeld ammoniak) bij lage temperatuur absorberen en bij hogere weer afgeven. De in het vrieslichaam ontstane damp van het koelmiddel wordt door de absorberende vloeistof opgenomen in een absorptievat, waar de aanvankelijk verdunde oplossing tot een geconcentreerde wordt verdicht. Deze laatste oplossing komt in een ruimte waar het koelmiddel door een gasvlam of een andere dan gasvormige warmtebron uit de vloeistof wordt verdreven. Het koelmiddel wordt vervolgens in een condensor gekoeld en gecondenseerd en treedt daarna in het vrieslichaam, waarmee de kringloop gesloten is. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor toepassingen in hotelkamers en vergaderzalen.

Gebruikertips:
De kast kan de temperatuur bij normaal gebruik ca. 15 graden terug koelen.
Men moet zich bij inbouw aan de inbouwvoorschriften houden.
Als dit niet gebeurd en de kast draait in zijn eigen warmte, dan kan deze niet naar behoren functioneren."	https://www.awesomescreenshot.com/image/62286448?key=8b032d4304d185282fd860cfb3c858bb each own colom	evertything before the : is the header 
- **Утвержденная стратегия (Шаг 1):** 1. Краткое описание задачи

Клиент хочет собрать данные о товарах с сайта professionele-koeling.nl.

Требования:

сначала предоставить тестовый CSV с 2 товарами;
после подтверждения — выполнить полный парсинг;
каждый атрибут должен находиться в отдельной колонке;
структура CSV должна строго соответствовать Google Spreadsheet.

Уровень уверенности: высокий.

2. Какой конечный результат нужен

Конечный результат:

CSV-файл.

Структура колонок (по Google Spreadsheet):

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

Особенности:

несколько изображений — через запятую;
несколько имен изображений — через запятую;
Specs и Spec_detail должны быть разбиты по отдельным колонкам согласно примеру.

Уровень уверенности: высокий.

3. Как лучше решить задачу
Рекомендуемое решение

Python + requests + BeautifulSoup

Почему именно так:

предоставленный HTML показывает полностью сформированную разметку товаров;
цены присутствуют сразу в HTML;
ссылки и изображения доступны напрямую;
нет признаков обязательного JavaScript-рендеринга;
клиенту нужен обычный экспорт в CSV;
это самое простое, быстрое и надежное решение.

Использование браузерной автоматизации имеет смысл только если в процессе выяснится, что часть данных (например описание или характеристики) появляется исключительно после выполнения JavaScript.

Уровень уверенности: средне-высокий (нет HTML карточки товара).

4. Почему остальные варианты хуже
Playwright

Не рекомендую как основной вариант.

Минусы:

медленнее;
выше потребление ресурсов;
сложнее поддержка;
не видно необходимости по имеющимся данным.
Selenium

Также избыточен.

Минусы:

тяжелее;
менее стабилен;
преимуществ перед requests здесь не видно.
Scrapy

Подойдет для большого объема данных, но для данной задачи является усложнением.

Минусы:

более высокая стоимость разработки;
клиент не просил распределенный краулер.
API

На данный момент существование API не подтверждено.

HAR пустой.

5. Анализ сайта

На основании предоставленных файлов.

Возможность	Статус
JavaScript Rendering	не подтвержден
React	неизвестно
Vue	неизвестно
Angular	неизвестно
API	неизвестно
GraphQL	неизвестно
Infinite Scroll	неизвестно
Pagination	неизвестно
Login	не обнаружен
Cookies	не требуются (cookies.json пуст)
JWT	не обнаружен
Bearer Token	не обнаружен
CAPTCHA	не обнаружена
Cloudflare	не подтвержден
Rate Limits	неизвестно
Download Files	неизвестно
Upload Files	нет
Lazy Loading	не видно
WebSocket	неизвестно
XHR/Fetch	неизвестно (HAR пустой)
Sitemap	неизвестно
robots.txt	неизвестно

Важно:

network.har пустой;
cookies отсутствуют;
headers отсутствуют.

Поэтому нельзя сделать окончательные выводы.

Уровень уверенности: средний.

6. Что необходимо собрать до начала разработки

Желательно получить:

HTML страницы товара (не только страницы категории).
Непустой network.har, если есть сомнения по загрузке данных.
Подтверждение структуры CSV.
Подтверждение правил формирования колонок Specs и Spec_detail.
Подтверждение, нужно ли собирать абсолютно все товары категории или нескольких категорий.

Google Spreadsheet содержит пример, но без доступа к нему в предоставленных материалах нельзя проверить возможные дополнительные требования.

7. Возможные сложности

Возможные проблемы:

изменение HTML сайта;
большое количество товаров;
возможные ограничения по скорости запросов;
скрытая пагинация;
часть характеристик может находиться только внутри карточки товара;
характеристики могут иметь разное количество полей у разных товаров;
несколько изображений на товар.

Вероятность серьезных технических сложностей пока выглядит невысокой.

8. Что нужно уточнить у клиента

Перед началом разработки стоит уточнить:

Нужно ли собирать только категорию koelkasten-kisten или весь сайт?
Как обрабатывать товары без скидки — оставлять Sale price пустым или дублировать обычную цену?
Нужно ли сохранять цены без символа евро и разделителей тысяч?
Нужно ли сохранять HTML в описании или только чистый текст?
Как именно должны быть представлены Specs и Spec_detail, если характеристик много?
Нужно ли скачивать изображения или достаточно ссылок?
Есть ли страницы с пагинацией, которые также необходимо обходить?
Какой ожидаемый объем товаров?
9. Рекомендуемый стек технологий

Основной стек:

Python
requests
BeautifulSoup

Только если потребуется после проверки сайта:

Playwright
10. План разработки
Этап 1. Анализ сайта

Цель

Проверить структуру карточек товаров и наличие пагинации.

Результат

Понятна структура всех необходимых данных.

Зависимости

Ответы клиента (при необходимости).

Этап 2. Сбор данных

Цель

Извлечь все необходимые поля.

Результат

Получены данные по товарам.

Зависимости

Этап 1.

Этап 3. Формирование CSV

Цель

Разместить каждое поле в отдельной колонке.

Результат

CSV соответствует шаблону клиента.

Зависимости

Этап 2.

Этап 4. Тестовый экспорт

Цель

Подготовить CSV с двумя товарами.

Результат

Клиент проверяет структуру.

Зависимости

Этап 3.

Этап 5. Полный экспорт

Цель

Собрать все товары.

Результат

Итоговый CSV.

Зависимости

Подтверждение тестового файла клиентом.

11. Оценка сложности
Параметр	Оценка
Сложность	3/10
Estimation	3–6 часов
Вероятность блокировок	Низкая
Вероятность необходимости браузера	Низкая–средняя
Вероятность изменения сайта	Средняя
Общий риск	Низкий–средний

Уровень уверенности: средний (из-за отсутствия HTML страницы товара и сетевого лога).

12. Можно ли решить проще

Да.

Самое простое решение:

использовать requests;
получать HTML страниц;
извлекать данные через HTML;
сохранять сразу в CSV.

На текущий момент нет оснований использовать Playwright.

Также стоит проверить, не доступны ли характеристики непосредственно в HTML карточки товара, чтобы минимизировать число запросов. Однако пустой network.har не позволяет подтвердить наличие или отсутствие скрытого API.

13. Итоговая рекомендация

Рекомендуемое решение

Использовать Python + requests + BeautifulSoup с экспортом в CSV.

Почему это оптимально

самое простое решение;
минимальная сложность;
высокая скорость работы;
нет подтверждений, что требуется браузерная автоматизация.

Что необходимо получить перед началом разработки

подтверждение структуры Specs и Spec_detail;
подтверждение области парсинга (одна категория или весь сайт);
при возможности — HTML страницы товара или непустой network.har для проверки источника данных.

Можно ли переходить к написанию кода?

Пока не рекомендуется. Лучше сначала дождаться ответов клиента на вопросы выше и убедиться, что все необходимые поля доступны без JavaScript. После этого можно приступать к реализации.
- **Анализ разметки/API (из файлов в AI_INPUT):** 

--- ФАЙЛ: description.txt ---

Задание от клиента, для теста собирем 2 шт товаров и скину емку файл csv
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

Данные с файла spreadsheet:
URL	Breadcrumb	Title 	Short description	imageurl	image_name	Price	Sale price	Description 	Specs	Spec_detail
https://www.professionele-koeling.nl/koelkasten-kisten.html	Home	Polar GE579	"De Polar GE579 is een zwarte minibar koelkast met
29 liter inhoud voor gebruik in hotelkamers, B&B's of ver-
gaderruimtes. Vrijwel geluidsloos met 2 roosters en 2 deurrekken."	if multipli seperated by comma	if multiple seperated by comma	259	229	"Polar GE579: Zwarte 30 liter minibar koelkast voor de hotelkamer
De Polar GE579 is een zwarte minibar koelkast met een capaciteit van 29 liter. Deze koelkast maakt gebruik van het absorptie
koelsysteem i.p.v. een compressor. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor
toepassingen in hotelkamers, B&B 's en vergaderzalen.

Uitvoering:

Exterieur: zwaart
Interieur: roestvrijstaal
Werking: Werkt met warmtepomp in plaats van ventilatoren
Verwisselbare en afsluitbare deur
Verlichting: LED
Roosters (2x)
Vrijwel geruisloos
Vrijstaand of inbouw
Absorptie koelsysteem
Automatische ontdooiing
Specificaties:

Artikelnummer: GE579
Inhoud: 29 liter
Temperatuurbereik:  3-5°C bij een omgevingstemperatuur van 16°C
Temperatuurbereik: 5-8°C bij een omgevingstemperatuur van 25°C
Temperatuurbereik: 8-12°C bij een omgevingstemperatuur van 32°C
Afmetingen BxDxH: 400 x 430 x 530 mm
Energieklasse: F
Aansluitwaarde: 220-240 Volt, 60 watt
Klimaatklasse: N (omgevingstemperatuur tussen +16°C en +32°)
Koelmiddel: R600a
Gewicht: 13 kg
Bij het absorptiesysteem, dat geheel zonder bewegende delen kan worden uitgevoerd, wordt gebruik gemaakt van het verschijnsel dat sommige vloeistoffen (bijvoorbeeld water) sommige koelmiddelen (bijvoorbeeld ammoniak) bij lage temperatuur absorberen en bij hogere weer afgeven. De in het vrieslichaam ontstane damp van het koelmiddel wordt door de absorberende vloeistof opgenomen in een absorptievat, waar de aanvankelijk verdunde oplossing tot een geconcentreerde wordt verdicht. Deze laatste oplossing komt in een ruimte waar het koelmiddel door een gasvlam of een andere dan gasvormige warmtebron uit de vloeistof wordt verdreven. Het koelmiddel wordt vervolgens in een condensor gekoeld en gecondenseerd en treedt daarna in het vrieslichaam, waarmee de kringloop gesloten is. Voordeel van dit systeem, door geen bewegende delen is het apparaat uitermate geschikt voor toepassingen in hotelkamers en vergaderzalen.

Gebruikertips:
De kast kan de temperatuur bij normaal gebruik ca. 15 graden terug koelen.
Men moet zich bij inbouw aan de inbouwvoorschriften houden.
Als dit niet gebeurd en de kast draait in zijn eigen warmte, dan kan deze niet naar behoren functioneren."	https://www.awesomescreenshot.com/image/62286448?key=8b032d4304d185282fd860cfb3c858bb each own colom	evertything before the : is the header 

--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---
{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "WebInspector",
      "version": "537.36"
    },
    "pages": [],
    "entries": []
  }
}

--- ФАЙЛ: notes.txt ---


--- СЖАТЫЙ HTML: page.html ---
<li class="item">
 <div class="product-image-wrapper">
  <a class="product-image" href="https://www.professionele-koeling.nl/koelkasten-kisten/polar-dm071.html">
   <img id="product-collection-image-212" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg"/>
  </a>
  <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover">
   <li>
    <a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/RTXXHZVsWjqQoFjc/">
     <span class="2 icon ib ic ic-heart">
     </span>
    </a>
   </li>
   <li>
    <a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw,/form_key/RTXXHZVsWjqQoFjc/">
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

# СТРАТЕГИЯ ОПРЕДЕЛЕНИЯ ТЕХНОЛОГИИ СБОРА

Перед проектированием проанализируй входные данные и выбери оптимальный способ получения данных. 
Приоритет выбора решения:

1. Минимальная сложность
2. Максимальная надежность
3. Минимальное количество зависимостей
4. Простота сопровождения
5. Производительность (если это не противоречит первым четырем пунктам)

1. **Есть API → использовать API.**
Если API покрывает все требования клиента —
используй API.
Если API не предоставляет необходимые данные —
объясни причину и переходи к следующему способу.   
2. **Есть готовый HTML без JavaScript → использовать requests + BeautifulSoup**   
3. **Контент появляется только после выполнения JavaScript, требуется авторизация через браузер, сложные взаимодействия или антибот → использовать Playwright.**
   
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