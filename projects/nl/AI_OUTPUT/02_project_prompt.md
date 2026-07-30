# РОЛЬ

Ты — Senior Python Developer / Web Scraping Engineer. Твоя цель — спроектировать техническое решение для конкретного сайта клиента **БЕЗ написания самого кода**. 

Ты должен распределить логику по существующей функциональной структуре проекта.

---

# ВХОДНЫЕ ДАННЫЕ
- **Описание задачи клиента:** Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

example.json -содержит ожидаемую структуру ,нужно получить результат 2 продуктов в csv

Нужно собрать только категорию koelkasten-kisten или весь сайт? - сначала только 2 продуктов в csv
Нужно ли обходить все страницы пагинации?- - сначала только 2 продуктов в csv из одной категории
В каком формате нужен результат (JSON, CSV, Excel)? - CSV
Нужно ли скачивать изображения или достаточно ссылок? - ссылка
Если изображений несколько — сохранить все? - 1 
Нужно ли разворачивать характеристики (Specs) в отдельные колонки? - да 
Да будут отдельно колонки Merk, Kleur, Breedte ... и надо их брать значения Polar, Zwart.. Нмже подробнее
Merk	Polar
Kleur	Zwart
Breedte	400-500mm
Diepte	400-500mm
Hoogte	450-550mm
Inhoud	20-30 liter
Temperatuurbereik	+4 ºC / +8 ºC
Vermogen	Nee


Нужно ли собирать товары, которых нет в наличии? - нужно
Нужно ли сохранять HTML-разметку описания или только чистый текст? - чистый текст
Требуется ли регулярный запуск или это разовая выгрузка? - разовая
- **Утвержденная стратегия (Шаг 1):** 1. Краткое описание задачи

Клиенту необходимо выполнить тестовый парсинг первых 2 товаров из категории:

https://www.professionele-koeling.nl/koelkasten-kisten.html

Результат требуется предоставить в CSV, где:

каждый товар — отдельная строка;
каждое поле — отдельная колонка;
структура соответствует example.json;
характеристики (Specs / Extra informatie) должны быть развернуты в отдельные столбцы (Merk, Kleur, Breedte, Diepte и т.д.);
изображения сохранять только в виде ссылки (одно изображение);
описание — обычный текст без HTML;
после проверки тестового CSV, вероятно, потребуется полный парсинг категории (или сайта — пока это не подтверждено).

Уверенность: высокая.

2. Какой конечный результат нужен

На текущем этапе:

✅ CSV
2 товара
одна категория (koelkasten-kisten)
одна строка = один товар
отдельная колонка для каждого поля
отдельная колонка для каждой характеристики (Specs)

Не требуется:

скачивание изображений
JSON
Excel
база данных
API

Уверенность: высокая.

3. Как лучше решить задачу
Рекомендуемое решение

Python + requests + BeautifulSoup

Причины:

HTML страницы уже содержит всю необходимую информацию.
В предоставленном HTML присутствуют:
название;
цены;
описание;
характеристики;
breadcrumb;
изображение.
Нет признаков обязательного JavaScript-рендеринга.
Нет необходимости использовать браузер для первых двух товаров.

Алгоритм будет максимально простой:

открыть страницу категории;
получить ссылки на первые два товара;
открыть страницы товаров;
извлечь поля;
развернуть таблицу характеристик;
сохранить CSV.

Это самое простое, быстрое и надежное решение.

Уверенность: высокая.

4. Почему остальные варианты хуже
Playwright

Не рекомендуется.

Причины:

лишняя сложность;
значительно медленнее;
HTML уже содержит нужные данные.

Использовать только если обнаружится защита или динамическая подгрузка.

Selenium

Еще тяжелее Playwright.

Преимуществ нет.

Scrapy

Подойдет для полного сайта.

Но сейчас задача — всего 2 товара.

Использование Scrapy будет избыточным.

API

Пока нет подтверждения существования API.

Комбинация requests + Playwright

Излишне.

Начинать стоит именно с requests.

5. Анализ сайта

На основании предоставленного HTML.

Возможность	Статус
JavaScript Rendering	признаков нет
React	не обнаружено
Vue	не обнаружено
Angular	не обнаружено
API	неизвестно
GraphQL	не обнаружено
Infinite Scroll	нет
Pagination	вероятно есть
Login	не требуется
Cookies	возможны, но не обязательны
JWT	не обнаружено
Bearer Token	не обнаружено
CAPTCHA	есть на форме отзывов, не относится к чтению страниц
Cloudflare	неизвестно
Rate Limits	неизвестно
Download Files	не требуется
Upload Files	нет
Lazy Loading	признаков нет
WebSocket	неизвестно
XHR / Fetch	определить невозможно (HAR отсутствует)
Sitemap	не проверялся
robots.txt	не проверялся

Уверенность: средняя.

6. Что необходимо собрать до начала разработки

Для выполнения тестового задания уже имеется практически всё необходимое:

✅ пример структуры (example.json);
✅ пример HTML страницы;
✅ ссылка на категорию;
✅ требования по CSV.

Однако для полной выгрузки позже желательно иметь:

пример ожидаемого CSV (если есть);
доступ к Google Sheet (для проверки полного списка полей, если он отличается от example.json);
подтверждение, потребуется ли после теста весь каталог.

Уверенность: высокая.

7. Возможные сложности

Возможные риски:

изменение HTML;
разные наборы характеристик у разных товаров;
отсутствие скидочной цены у части товаров;
разные форматы описания;
большое количество страниц при полном парсинге;
возможные ограничения по скорости запросов;
возможная защита сайта (не подтверждена).

На текущем тестовом этапе риски минимальны.

8. Что нужно уточнить у клиента

Для тестового задания критичных вопросов почти нет, но перед полной выгрузкой желательно уточнить:

После проверки тестового CSV нужно будет собирать:
только категорию koelkasten-kisten;
или весь сайт?
Если у товара отсутствует старая цена (Sale/Old Price), что записывать:
пустое значение;
текущую цену;
0?
Если характеристика отсутствует у товара, оставлять пустую колонку?
Нужно ли сохранять все найденные колонки характеристик, даже если они встречаются только у одного товара?
Нужно ли включать наличие товара (Availability) в CSV?
9. Рекомендуемый стек технологий

Минимальный стек:

Python
requests
BeautifulSoup
CSV

Больше ничего для данного проекта не требуется.

10. План разработки
Этап 1. Анализ страницы

Цель

Проверить структуру категории и товара.

Результат

Понимание расположения всех необходимых полей.

Зависимости

Нет.

Этап 2. Извлечение ссылок

Цель

Получить первые два товара из категории.

Результат

Список URL товаров.

Зависимости

Этап 1.

Этап 3. Извлечение данных

Цель

Собрать все требуемые поля каждого товара.

Результат

Полный набор данных.

Зависимости

Этап 2.

Этап 4. Разворачивание характеристик

Цель

Преобразовать таблицу Specs в отдельные колонки.

Результат

CSV с единым набором заголовков.

Зависимости

Этап 3.

Этап 5. Формирование CSV

Цель

Подготовить итоговый файл.

Результат

CSV с двумя товарами.

Зависимости

Этапы 3–4.

11. Оценка сложности
Параметр	Оценка
Сложность	2/10
Estimation	1–2 часа
Вероятность блокировок	низкая (~10%)
Вероятность необходимости браузера	низкая (~15%)
Вероятность изменения сайта	средняя (~30%)
Общий риск	низкий
12. Можно ли решить проще

Да.

На основании предоставленного HTML наиболее простое решение — парсинг статического HTML через requests + BeautifulSoup.

Нет оснований использовать:

Playwright;
Selenium;
Scrapy;
браузерную автоматизацию.

Также стоит проверить network.har, если он будет предоставлен, на наличие скрытого API. Однако сейчас HAR-файл отсутствует (пустой), поэтому подтверждений существования API нет.

CSV является оптимальным форматом — дополнительная база данных или промежуточный JSON не нужны.

Уверенность: высокая.

13. Итоговая рекомендация
Рекомендуемое решение

Использовать Python + requests + BeautifulSoup для получения первых двух товаров из категории и формирования CSV.

Почему это оптимально
HTML уже содержит все необходимые данные.
Не требуется JavaScript-рендеринг.
Минимальная сложность.
Быстрая разработка.
Простое сопровождение.
Что необходимо получить перед началом разработки

Для выполнения тестового задания достаточно имеющихся данных. Перед полной выгрузкой желательно получить подтверждение объема работ (только категория или весь сайт) и, при необходимости, пример итогового CSV или доступ к Google Sheet для сверки структуры.

Можно ли переходить к написанию кода

Да, для тестового задания (2 товара → CSV) информации достаточно, можно переходить к реализации. Для последующего полного парсинга рекомендуется дождаться ответов клиента на вопросы о полном объеме выгрузки и обработке отсутствующих полей.
- **Анализ разметки/API (из файлов в AI_INPUT):** 

--- ФАЙЛ: description.txt ---
Summary
Scrape a website for all the required info — details are in the Google Sheet, ask if anything's unclear. Before the full scrape, send a test file with 2 products. Every field must be in its own column with a consistent header — no mixed data across columns.

Please let me know when you can deliver.

https://docs.google.com/spreadsheets/d/1Ru8hf8jBDAhUSCTGGsm_fNueRIyfd9V19QD6ecPrnKw/edit?usp=sharing

example.json -содержит ожидаемую структуру ,нужно получить результат 2 продуктов в csv

Нужно собрать только категорию koelkasten-kisten или весь сайт? - сначала только 2 продуктов в csv
Нужно ли обходить все страницы пагинации?- - сначала только 2 продуктов в csv из одной категории
В каком формате нужен результат (JSON, CSV, Excel)? - CSV
Нужно ли скачивать изображения или достаточно ссылок? - ссылка
Если изображений несколько — сохранить все? - 1 
Нужно ли разворачивать характеристики (Specs) в отдельные колонки? - да 
Да будут отдельно колонки Merk, Kleur, Breedte ... и надо их брать значения Polar, Zwart.. Нмже подробнее
Merk	Polar
Kleur	Zwart
Breedte	400-500mm
Diepte	400-500mm
Hoogte	450-550mm
Inhoud	20-30 liter
Temperatuurbereik	+4 ºC / +8 ºC
Vermogen	Nee


Нужно ли собирать товары, которых нет в наличии? - нужно
Нужно ли сохранять HTML-разметку описания или только чистый текст? - чистый текст
Требуется ли регулярный запуск или это разовая выгрузка? - разовая

--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: example.json ---

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


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---


--- СЖАТЫЙ HTML: page.html ---
На странице https://www.professionele-koeling.nl/koelkasten-kisten.html есть список товаров
<li class="item">
 <div class="product-image-wrapper">
  <a class="product-image" href="https://www.professionele-koeling.nl/diamond-img15s-a1.html">
   <img id="product-collection-image-1210" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/small_image/295x295/9df78eab33525d08d6e5fb8d27136e95/d/i/diamond_img15_s_a1_wandkoelmeubel_1500mm_met_glazen_schuifdeuren.jpg"/>
  </a>
  <ul class="add-to-links clearer addto-links-icons addto-onimage display-onhover">
   <li>
    <a class="link-wishlist" href="https://www.professionele-koeling.nl/wishlist/index/add/product/1210/form_key/p8EcxN2r4x0ikJzf/">
     <span class="2 icon ib ic ic-heart">
     </span>
    </a>
   </li>
   <li>
    <a class="link-compare" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/1210/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuLmh0bWw_cD00Mw,,/form_key/p8EcxN2r4x0ikJzf/">
     <span class="2 icon ib ic ic-compare">
     </span>
    </a>
   </li>
  </ul>
 </div>
 <!-- end: product-image-wrapper -->
 <h2 class="product-name">
  <a href="https://www.professionele-koeling.nl/diamond-img15s-a1.html">
   Diamond IMG15/S-A1
  </a>
 </h2>
 <div class="price-box">
  <p class="old-price">
   <span class="price-label">
    Van:
   </span>
   <span class="price" id="old-price-1210">
    € 4.607,00
   </span>
  </p>
  <p class="special-price">
   <span class="price-label">
    Voor
   </span>
   <span class="price" id="product-price-1210">
    € 3.289,00
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
Также страница товара:
<div class="inner-container">
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
     Polar DM071
    </span>
   </li>
  </ul>
 </div>
 <div class="preface">
 </div>
 <div class="col-main">
  <div id="messages_product_view">
  </div>
  <div class="product-view nested-container">
   <form id="product_addtocart_form">
    <input name="form_key"/>
    <div class="no-display">
     <input name="product"/>
     <input id="related-products-field" name="related_product"/>
    </div>
    <div class="product-img-column grid12-4">
     <div class="img-box img-box-style1">
      <p class="product-image zoom-inside">
       <div id="wrap">
        <a class="cloud-zoom product-image-gallery" href="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" id="zoom1">
         <img class="gallery-image visible" id="image-main" src="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/363x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg"/>
        </a>
        <div class="mousetrap">
        </div>
       </div>
       <a class="lightbox-group zoom-btn-small cboxElement" href="https://www.professionele-koeling.nl/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/p/o/polar_dm071_glasdeurkoelkast_46_liter.jpg" id="zoom-btn">
        Zoom
       </a>
      </p>
     </div>
     <!-- end: img-box -->
    </div>
    <div class="product-primary-column product-shop grid12-5">
     <div class="product-name">
      <h1>
       Polar DM071
      </h1>
     </div>
     <div class="ratings no-rating">
      <div class="rating-box">
       <div class="rating">
       </div>
      </div>
      <p class="rating-links">
       <a href="#review-form" id="goto-reviews-form">
        Schrijf de eerste review over dit product
       </a>
      </p>
     </div>
     <div class="short-description">
      <div class="std">
       <p>
        De Polar DM071 is een klein tafelmodel glasdeurkoelkast in witte uitvoering.
        <br/>
        Deze voordelige compacte koeler heeft 46 liter capaciteit en weegt maar 18 kilo.
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
       <br/>
       <p>
       </p>
      </div>
     </div>
     <div>
      <div class="product-type-data">
       <p class="availability in-stock">
        Beschikbaarheid:
        <span>
         Op voorraad
        </span>
       </p>
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
      </div>
     </div>
     <div class="add-to-box s">
      <div class="add-to-cart left-side">
       <div class="qty-wrapper">
        <label>
         Aantal:
        </label>
        <input class="input-text qty" id="qty" name="qty"/>
       </div>
       <button class="button btn-cart" id="product-addtocart-button">
        <span>
         <span>
          In winkelwagen
         </span>
        </span>
       </button>
      </div>
      <div class="paypal-wrapper">
      </div>
     </div>
     <div class="product-benefits">
      <ul>
       <li>
        Levering in de Benelux
       </li>
       <li>
        Zakelijk op rekening kopen
       </li>
       <li>
        2 jaar garantie
       </li>
       <li>
        Deskundig advies
       </li>
       <li>
        Officieel dealer van topmerken
       </li>
      </ul>
     </div>
     <div class="action-box clearer">
      <ul class="add-to-links">
       <li>
        <a class="link-wishlist feature feature-icon-hover first" href="https://www.professionele-koeling.nl/wishlist/index/add/product/212/form_key/TIOaSPgIeleEQ6nQ/">
         <span class="ic ic-heart ib icon-color-productview">
         </span>
         <span class="label">
          Zet op verlanglijst
         </span>
        </a>
       </li>
       <li>
        <a class="link-compare feature feature-icon-hover first" href="https://www.professionele-koeling.nl/catalog/product_compare/add/product/212/uenc/aHR0cHM6Ly93d3cucHJvZmVzc2lvbmVsZS1rb2VsaW5nLm5sL2tvZWxrYXN0ZW4ta2lzdGVuL3BvbGFyLWRtMDcxLmh0bWw,/form_key/TIOaSPgIeleEQ6nQ/">
         <span class="ic ic-compare ib icon-color-productview">
         </span>
         <span class="label">
          Voeg toe aan productvergelijking
         </span>
        </a>
       </li>
       <li>
        <a class="link-share feature feature-icon-hover first" href="https://www.professionele-koeling.nl/sendfriend/product/send/id/212/cat_id/3/">
         <span class="ic ic-share ib icon-color-productview">
         </span>
         <span class="label">
          E-mail naar een vriend
         </span>
        </a>
       </li>
      </ul>
     </div>
    </div>
    <!-- end: product-shop -->
    <div class="product-secondary-column grid12-3 custom-sidebar-right">
     <div class="inner">
      <div class="feature-wrapper bottom-border">
       <div class="box-brand">
        <a class="fade-on-hover" href="https://www.professionele-koeling.nl/catalogsearch/result/?q=Polar">
         <img src="https://www.professionele-koeling.nl/media/wysiwyg/infortis/brands/polar.png"/>
        </a>
       </div>
      </div>
      <div class="container_product_secondary_2 std block_product_secondary_bottom">
       <p>
        <strong>
         Let op:
        </strong>
       </p>
       <ul>
        <li>
         Betreft het grote aantallen?
        </li>
        <li>
         Is het orderbedrag hoger dan € 1500,-?
        </li>
       </ul>
       <p>
        <strong>
         <a class="fancybox" href="https://www.professionele-koeling.nl/offerte">
          Vraag dan een offerte aan
         </a>
        </strong>
       </p>
      </div>
     </div>
    </div>
    <!-- end: product-secondary-column -->
   </form>
   <div class="box-additional grid12-9">
    <div class="box-collateral collateral-container box-tabs">
     <div class="gen-tabs gen-tabs--style1" id="product-tabs">
      <ul class="tabs clearer">
       <li id="tab-description">
        <a class="current" href="#">
         Productbeschrijving
        </a>
       </li>
       <li id="tab-additional">
        <a href="#">
         Extra informatie
        </a>
       </li>
       <li id="tab-tabreviews">
        <a href="#">
         Beoordelen
        </a>
       </li>
       <li id="tab-tags">
        <a href="#">
         Eigen tags
        </a>
       </li>
      </ul>
      <div class="tabs-panels">
       <h2 class="acctab" id="acctab-description">
        Productbeschrijving
       </h2>
       <div class="panel">
        <h2>
         Details
        </h2>
        <div class="std">
         <h2>
          Polar DM071: Witte glasdeurkoelkast tafelmodel
          <br/>
         </h2>
         <p>
          De
          <strong>
           Polar DM071
          </strong>
          is een kleine
          <strong>
           tafelmodel glasdeurkoelkast
          </strong>
          met een inhoud van 46 liter. Deze compacte
          <strong>
           witte
          </strong>
          koeler
          <br/>
          heeft een draaideur voorzien van dubbel glas en is door zijn lage gewicht van 18kg zeer gemakkelijk te verplaatsen.
          <br/>
          Kortom: een handige kleine glasdeurkoeler voor een net zo'n kleine prijs.
          <br/>
          <br/>
          <strong>
           Uitvoering:
          </strong>
         </p>
         <ul>
          <li>
           Tafelmodel glasdeurkoelkast
          </li>
          <li>
           Draaideur voorzien van dubbel glas
          </li>
          <li>
           Kleur: wit
          </li>
          <li>
           Voorzien van instelbare thermostaat
          </li>
         </ul>
         <p>
          <strong>
           Specificaties:
          </strong>
         </p>
         <ul>
          <li>
           Artikelnummer: DM071
          </li>
          <li>
           Afmetingen BxDxH: 430 x 480 x 510 mm
          </li>
          <li>
           Inhoud: 46 liter
          </li>
          <li>
           Temperatuur: +4 ºC tot +18 ºC
          </li>
          <li>
           Aansluitwaarde: 220 Volt, 85 Watt
          </li>
          <li>
           Energieklasse: B
          </li>
          <li>
           Gewicht: 18 kg
          </li>
         </ul>
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
         <p>
         </p>
         <p>
         </p>
        </div>
       </div>
       <h2 class="acctab" id="acctab-additional">
        Extra informatie
       </h2>
       <div class="panel">
        <h2>
         Extra informatie
        </h2>
        <table class="data-table" id="product-attribute-specs-table">
         <colgroup>
          <col/>
          <col/>
         </colgroup>
         <tbody>
          <tr class="first odd">
           <th class="label">
            Merk
           </th>
           <td class="data last">
            Polar
           </td>
          </tr>
          <tr class="even">
           <th class="label">
            Kleur
           </th>
           <td class="data last">
            Wit
           </td>
          </tr>
          <tr class="odd">
           <th class="label">
            Breedte
           </th>
           <td class="data last">
            400-500mm
           </td>
          </tr>
          <tr class="even">
           <th class="label">
            Diepte
           </th>
           <td class="data last">
            400-500mm
           </td>
          </tr>
          <tr class="odd">
           <th class="label">
            Hoogte
           </th>
           <td class="data last">
            450-550mm
           </td>
          </tr>
          <tr class="even">
           <th class="label">
            Inhoud
           </th>
           <td class="data last">
            Nee
           </td>
          </tr>
          <tr class="odd">
           <th class="label">
            Temperatuurbereik
           </th>
           <td class="data last">
            +4 ºC / +18 ºC
           </td>
          </tr>
          <tr class="last even">
           <th class="label">
            Vermogen
           </th>
           <td class="data last">
            Nee
           </td>
          </tr>
         </tbody>
        </table>
       </div>
       <h2 class="acctab" id="acctab-tabreviews">
        Beoordelen
       </h2>
       <div class="panel">
        <div class="box-collateral box-reviews" id="customer-reviews">
         <!--<body onLoad="showcaptcha()">-->
         <div class="form-add">
          <h2>
           Schrijf uw eigen review
          </h2>
          <form id="review-form">
           <input name="form_key"/>
           <input name="form_key"/>
           <fieldset>
            <h3>
             U plaatst een review over:
             <span>
              Polar DM071
             </span>
            </h3>
            <div class="fieldset">
             <ul class="form-list">
              <li>
               <label class="required">
                <em>
                 *
                </em>
                Uw naam
               </label>
               <div class="input-box">
                <input class="input-text required-entry" id="nickname_field" name="nickname"/>
               </div>
              </li>
              <li>
               <label class="required">
                <em>
                 *
                </em>
                Titel van uw review
               </label>
               <div class="input-box">
                <input class="input-text required-entry" id="summary_field" name="title"/>
               </div>
              </li>
              <li>
               <label class="required">
                <em>
                 *
                </em>
                Beoordelen
               </label>
               <div class="input-box">
                <textarea class="required-entry" id="review_field" name="detail"></textarea>
               </div>
              </li>
              <li id="rcode">
               <div class="captcha">
                <div class="g-recaptcha">
                 <div>
                  <div>
                  </div>
                  <textarea class="g-recaptcha-response" id="g-recaptcha-response" name="g-recaptcha-response"></textarea>
                 </div>
                </div>
               </div>
               <span id="captcha-required">
                Please Fill Recaptcha To Continue
               </span>
              </li>
             </ul>
            </div>
           </fieldset>
           <div class="buttons-set">
            <button class="button">
             <span>
              <span>
               Review versturen
              </span>
             </span>
            </button>
           </div>
          </form>
         </div>
         <!--</body>-->
        </div>
       </div>
       <h2 class="acctab" id="acctab-tags">
        Eigen tags
       </h2>
       <div class="panel">
        <div class="box-collateral box-tags">
         <h2>
          Eigen tags
         </h2>
         <form id="addTagForm">
          <div class="form-add">
           <label>
            Uw tags toevoegen
           </label>
           <div class="input-box">
            <input class="input-text required-entry" id="productTagName" name="productTagName"/>
           </div>
           <button class="button">
            <span>
             <span>
              Tags toevoegen
             </span>
            </span>
           </button>
          </div>
         </form>
         <p class="note">
          Gebruik spaties om tags te scheiden. Gebruik enkele aanhalingstekens (‘) voor woordgroepen.
         </p>
        </div>
       </div>
      </div>
     </div>
    </div>
   </div>
   <!-- end: box-tabs -->
   <div class="box-additional grid12-9">
   </div>
  </div>
  <!-- end: product-view -->
 </div>
 <div class="postscript">
 </div>
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