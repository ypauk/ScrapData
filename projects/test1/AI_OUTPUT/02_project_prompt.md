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

- **Утвержденная стратегия (Шаг 1):** 1. Краткое описание задачи

Клиент хочет получить scraper для сайта Professionele-Koeling.nl, который собирает данные о товарах и сохраняет их в JSON.

На текущем этапе нужен тестовый результат только для 2 товаров, после проверки которого можно будет переходить к полному scraping.

Главное требование — строго соблюдать структуру DS-PRK-Scraper.json: не переименовывать, не объединять и не добавлять поля. Каждое поле должно находиться отдельно, без смешивания данных между колонками/полями.

Из каждого товара требуется получить:

URL;

Breadcrumb;

Title;

Short description;

URL изображений;

имена изображений;

обычную цену;

Sale price;

полное описание;

характеристики (Specs);

отдельные значения характеристик (Spec_detail).

Изображения также необходимо скачивать, а не только сохранять их URL.

Согласно предоставленным материалам, Google Sheet уже преобразован в DS-PRK-Scraper.json, поэтому обращаться к Google Sheet не требуется и восстанавливать его структуру не нужно.

Уровень уверенности: высокий.

2. Какой конечный результат нужен

Основной результат:

JSON, содержащий данные о товарах строго в заданной структуре.

На текущем этапе:

2 товара;

изображения должны быть скачаны;

отсутствующая скидочная цена → пустое поле;

отсутствующая характеристика → пустое поле;

HTML-разметку описания сохранять не нужно — нужен чистый текст;

товары без наличия также должны попадать в результат;

порядок полей должен соответствовать спецификации.

Важно: предоставленный пример DS-PRK-Scraper.json — это спецификация структуры, а не готовая запись, которую нужно буквально повторять для всех товаров.

Уровень уверенности: высокий.

3. Как лучше решить задачу
Рекомендация: PlaywrightEngine + обычный HTML parsing

В данном проекте оптимален Playwright, который уже является зафиксированной частью framework проекта согласно предоставленной инструкции.

Схема на уровне подхода:

Playwright открывает категорию.

Получается DOM/HTML страницы.

Из карточек товаров извлекаются URL и базовые данные.

Для необходимых товаров открываются product pages.

Из product pages извлекаются описание, изображения и характеристики.

Изображения скачиваются.

Данные преобразуются в строго заданную JSON-структуру.

Это лучше всего соответствует имеющимся данным.

Важный момент: предоставленный HTML показывает, что каталог и product page уже содержат значительную часть нужных данных непосредственно в HTML. Например, категория содержит ссылки на товары, названия и цены, а product page содержит breadcrumb, title, short description и цены.

При этом в предоставленном notes.txt прямо указано, что API не обнаружен и сайт использует JavaScript. Поэтому Playwright является безопасным базовым выбором.

При live-проверке категория действительно отдаёт товары и пагинацию: сейчас страница показывает 429 товаров, по 36 на страницу, с переходами на ?p=2, ?p=3 и т. д. 
Professionele Koeling

Уровень уверенности: высокий для выбора Playwright; средний для утверждения, что абсолютно все данные требуют browser rendering.

4. Почему остальные варианты хуже
requests + BeautifulSoup

Теоретически HTML достаточно хорошо структурирован, поэтому этот вариант мог бы работать для части полей.

Однако он не является рекомендуемым вариантом здесь:

framework проекта уже предоставляет PlaywrightEngine;

в исходных материалах сайт обозначен как JS-based;

часть функциональности может зависеть от browser execution;

нет необходимости усложнять framework попыткой заменить его другим способом доступа.

То есть requests может быть полезным оптимизационным направлением после тестирования, но не как основная рекомендация для текущего scraper.py.

Selenium

Работоспособный вариант, но хуже Playwright:

Playwright уже предусмотрен проектом;

Selenium не даёт здесь очевидного преимущества;

появится лишняя технологическая зависимость.

Scrapy

Для 429 товаров Scrapy технически подходит, особенно при полном scrape, но здесь он избыточен:

сайт не требует сложной spider-инфраструктуры;

Playwright уже интегрирован в framework;

основная задача — получить данные из относительно простой структуры каталога и product pages.

API

API в предоставленных материалах не обнаружен (notes.txt: «API нет»), а network.har пустой.

Поэтому строить решение вокруг API сейчас оснований нет.

Вывод: Playwright — самый простой и надёжный вариант в рамках данного framework.

5. Анализ сайта
JavaScript Rendering

Есть JavaScript.

Сайт сам выводит сообщение о необходимости JavaScript для полной функциональности. При этом серверный HTML уже содержит существенную часть каталога, поэтому нельзя утверждать, что весь scraper обязательно зависит от JS. 
Professionele Koeling

Уверенность: высокая.

React

Не обнаружен.

Структура HTML и URL-ы выглядят как классический server-rendered e-commerce сайт, а не React SPA.

Уверенность: средняя.

Vue

Не обнаружен.

Уверенность: средняя.

Angular

Не обнаружен.

Уверенность: средняя.

API

По предоставленному notes.txt — API не найден.

network.har также пустой.

Уверенность: высокая в рамках предоставленных материалов.

GraphQL

Не обнаружен.

Нет признаков GraphQL endpoint или GraphQL traffic.

Уверенность: средняя.

Infinite Scroll

Не обнаружен.

Напротив, используется обычная pagination. Категория сообщает 1 tot 36 van 429 и содержит ссылки на следующие страницы. 
Professionele Koeling

Уверенность: высокая.

Pagination

Есть.

Используется параметр:

?p=2, ?p=3 и т. д.

На странице отображается 36 товаров из 429. 
Professionele Koeling

Уверенность: высокая.

Login

Есть, но для обычного просмотра каталога и product pages login не требуется.

На сайте присутствует обычный account/login функционал. 
Professionele Koeling

Уверенность: высокая.

Cookies

Есть.

Предоставлен cookies.json, в котором присутствуют cookies домена сайта, включая session-related cookies.

При этом значения cookie в исходных материалах не следует хардкодить в scraper или раскрывать.

Уверенность: высокая.

JWT

Не обнаружен.

Bearer Token

Не обнаружен.

CAPTCHA

Не подтверждена.

Cloudflare

Есть признаки Cloudflare.

В предоставленном cookies.json присутствует cf_clearance, поэтому сайт в определённых условиях использует Cloudflare challenge/clearance mechanism.

Это один из главных факторов риска для автоматизации.

Уверенность: высокая.

Rate Limits

Точного лимита из предоставленных материалов определить нельзя.

Уверенность: низкая.

При 429 товарах необходимо использовать умеренную скорость запросов и не создавать лишнюю нагрузку.

Download Files

Для проекта нужно скачивать изображения товаров.

Сами страницы используют изображения из /media/catalog/product/..., что подтверждается предоставленным HTML.

Upload Files

Для scraping не требуется.

Lazy Loading

Не подтверждено.

В предоставленной карточке изображения присутствуют непосредственно через img src, поэтому для базового каталога lazy-loading не является доказанной проблемой.

Уверенность: средняя.

WebSocket

Не обнаружен.

XHR / Fetch

Из-за отсутствия содержимого network.har достоверно определить нельзя.

Уверенность: низкая/средняя.

Sitemap

На сайте присутствует ссылка на Sitemap в обычной навигации, что подтверждается индексируемыми страницами. 
Professionele Koeling

Однако прямой запрос к /sitemap.xml в рамках проверки не дал доступного содержимого.

Поэтому формат и фактическое расположение sitemap подтверждать нельзя.

Уверенность: средняя.

6. Что необходимо собрать до начала разработки

Для начала полноценной реализации критически новых данных не требуется: проект уже содержит достаточно информации для разработки тестового scrape.

Уже имеются:

description.txt;

authoritative DS-PRK-Scraper.json;

category HTML;

product-page HTML;

pagination HTML;

cookies;

notes;

checkpoint;

пустые network.har, headers.json, proxies.txt.

Однако перед переходом от теста к full scrape желательно получить

Подтверждение клиента после тестового JSON на 2 товара.

Проверку скачанных изображений.

Подтверждение, что трактовка Specs и Spec_detail соответствует ожиданию клиента.

Подтверждение того, что все поля должны заполняться именно в указанном порядке.

Особенно важен Spec_detail: спецификация говорит:

everything before the : is the header

То есть характеристики должны разделяться на отдельные пары header → value, а не складываться в одно смешанное поле.

Дополнительный пример CSV/Excel не нужен, поскольку DS-PRK-Scraper.json объявлен окончательной спецификацией.

7. Возможные сложности
1. Cloudflare / блокировки

cf_clearance показывает наличие Cloudflare-механизма. Это основной инфраструктурный риск.

Риск: средний.

2. JavaScript

Некоторые элементы могут зависеть от browser execution, несмотря на то что основной HTML уже содержит данные.

Риск: средний.

3. Большое количество товаров

Сейчас категория содержит 429 товаров. При 36 товарах на страницу это примерно 12 страниц. 
Professionele Koeling

Если для каждого товара открывать отдельную product page, количество переходов будет значительно больше количества страниц каталога.

Риск: низкий технически, но влияет на время scrape.

4. Изображения

Нужно не просто извлекать URL, но и скачивать изображения.

Возможны:

разные размеры/версии одного изображения;

несколько изображений;

изменение URL media path;

ошибки отдельных image downloads.

5. Разная полнота характеристик

У товаров могут отсутствовать отдельные характеристики.

Это уже решено требованиями клиента: оставлять поле пустым, а не пытаться выводить альтернативное значение.

6. Изменение HTML

Сайт имеет достаточно традиционную HTML-структуру, но CSS selectors/classes могут измениться.

Риск: средний.

7. Несовпадение количества товаров

Checkpoint показывает ранее обработанные 49 товаров, тогда как текущая live-страница показывает 429 товаров. Это может означать, что checkpoint относится к отдельному тестовому запуску/срезу, а не к текущему полному каталогу. 
Professionele Koeling

Поэтому старый processed_count нельзя использовать как источник истины о текущем количестве товаров.

8. Что нужно уточнить у клиента

Здесь информации достаточно для тестовой реализации на 2 товара, поэтому блокирующих вопросов нет.

Но перед full scrape я бы уточнил только следующие моменты:

После теста: подтверждает ли клиент, что структура JSON и разбор Spec_detail выглядят именно так, как он ожидает?

Нужно ли сохранять изображения с оригинальным расширением/именем файла или допустимо использовать имя, полученное из URL?

Нужно ли сохранять абсолютный URL изображения в imageurl одновременно с локальным именем в image_name? По спецификации это выглядит именно так, но лучше подтвердить на тестовом результате.

При отсутствии Sale price действительно оставлять значение пустым, а не null? В answers.txt это указано как «пустое», но конкретное JSON-представление не определено.

Важно: эти вопросы не препятствуют созданию тестового результата из 2 товаров.

9. Рекомендуемый стек технологий

Python

Playwright

HTML parsing / BeautifulSoup

JSON

Основная технология браузерной автоматизации — Playwright.

BeautifulSoup имеет смысл использовать как средство разбора уже полученного HTML, а не как замену Playwright.

10. План разработки
Этап 1 — тестовый сбор 2 товаров

Цель: проверить selectors и соответствие структуры данных спецификации.

Результат: JSON с двумя товарами + скачанные изображения.

Зависимости: предоставленные HTML и DS-PRK-Scraper.json.

Этап 2 — валидация полей

Цель: проверить каждое обязательное поле:

URL;

breadcrumb;

title;

short description;

images;

prices;

description;

specs.

Результат: отсутствие смешанных данных и соответствие порядка/названий полей спецификации.

Зависимости: успешный этап 1.

Этап 3 — проверка pagination

Цель: убедиться, что scraper корректно проходит все страницы категории.

Результат: все необходимые product URLs без пропусков и дублей.

Зависимости: этап 1.

Этап 4 — полный scrape

Цель: собрать весь требуемый каталог.

Результат: полный JSON и локальные изображения.

Зависимости: подтверждение тестовых двух товаров клиентом.

Этап 5 — контроль качества

Цель: проверить:

количество товаров;

дубли;

пустые поля;

корректность цен;

корректность изображений;

соответствие JSON schema/структуре.

Результат: финальный проверенный dataset.

Зависимости: полный scrape.

11. Оценка сложности
Параметр	Оценка
Сложность	4/10
Разработка тестовой версии	2–4 часа
Полная реализация scraper	5–8 часов
Полный scrape + проверка	1–3 часа, в зависимости от скорости сайта
Вероятность блокировок	средняя
Вероятность необходимости браузера	высокая
Вероятность изменения сайта в будущем	средняя
Общий риск	средний

Оценка времени предполагает, что существующий framework действительно предоставляет готовый PlaywrightEngine, как указано в инструкции проекта.

Сам scraping не выглядит сложным: структура категории и pagination достаточно прозрачны, а каталог имеет обычные product URLs. 
Professionele Koeling

Главный источник неопределённости — не parsing, а Cloudflare/browser behavior и необходимость скачивания нескольких изображений.

12. Можно ли решить проще

Да.

Самое простое решение — не строить отдельную сложную scraping-систему и не использовать API/database.

Для текущей задачи достаточно:

PlaywrightEngine → category page → product URLs → product pages → HTML parsing → JSON + image downloads.

Особенно важно не делать лишнюю архитектуру.

Кроме того, перед полным переходом на product pages стоит проверить 2 товара, чтобы выяснить, есть ли все требуемые поля непосредственно в product HTML. Если окажется, что нужные данные полностью доступны на category listing, переходы на product pages для каждого товара можно будет минимизировать.

Однако по предоставленному примеру уже видно, что category page содержит как минимум URL, title и цены, тогда как подробные description/specs находятся на product page. Поэтому для полной спецификации скорее всего всё равно понадобятся product pages.

API искать как основной способ решения сейчас не нужно: в проекте он уже проверялся и не обнаружен.

13. Итоговая рекомендация

Рекомендуемое решение: Python + существующий PlaywrightEngine + HTML parsing + JSON + скачивание изображений.

Это оптимально потому что:

framework уже ориентирован на Playwright;

сайт содержит JavaScript;

API не найден;

pagination обычная и понятная;

HTML имеет достаточно стабильную структуру;

login для scraping каталога не нужен;

все требуемые поля описаны в DS-PRK-Scraper.json;

не требуется база данных или сложная архитектура.

Текущая live-проверка подтверждает обычный каталог с pagination и 429 товарами, а также наличие названий и цен непосредственно в HTML. 
Professionele Koeling

Что необходимо перед началом разработки

Ничего критически недостающего для тестовой версии.

Можно использовать уже предоставленные:

DS-PRK-Scraper.json;

category HTML;

product HTML;

pagination;

существующий PlaywrightEngine framework.

Для перехода к full scrape желательно сначала получить подтверждение клиента на тестовом JSON из 2 товаров.

Можно ли переходить к коду?

Да — для тестовой версии из 2 товаров.

Но согласно условиям проекта сейчас на этапе анализа код писать не следует. После получения/подтверждения тестового результата можно переходить к реализации полного scraper.

Итоговая уверенность: высокая. 
raw.githubusercontent.com
+1
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