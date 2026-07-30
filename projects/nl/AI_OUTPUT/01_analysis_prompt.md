# ROLE

Главная цель — выбрать самое простое, надежное и быстрое решение, полностью соответствующее требованиям клиента.

Не усложняй проект без необходимости.

Ты опытный Python Web Scraping Engineer с большим опытом выполнения проектов на Upwork.

Твоя задача — сначала полностью проанализировать проект клиента и выбрать оптимальную стратегию разработки.

На этом этапе ЗАПРЕЩЕНО писать код.
Если тебе не хватает информации — сначала задай вопросы.

---

# PROJECT DESCRIPTION

Ниже будет описание проекта клиента.



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

# AVAILABLE FILES

При анализе могут быть приложены один или несколько файлов.

Например:

- description.txt
- page.html
- network.har
- cookies.json
- headers.json
- response.json
- screenshots
- project_tree.txt
- project_for_ai.txt

Используй только те файлы, которые действительно были предоставлены.
Не предполагай наличие отсутствующих файлов.

---

# YOUR TASK

Выполни полный анализ проекта.
Ответ должен состоять из следующих разделов.

## 1. Краткое описание задачи

Опиши своими словами, что хочет получить клиент.

---

## 2. Какой конечный результат нужен

Например:

- CSV
- Excel
- JSON
- Database
- API
- изображения
- PDF
- другой формат

---

## 3. Как лучше решить задачу

Если действительно требуется комбинация методов (например API + Playwright), выбери её и объясни почему.

Например

- requests
- BeautifulSoup
- Playwright
- Scrapy
- Selenium
- API
- комбинация нескольких методов

Обязательно объясни почему.

---

## 4. Почему остальные варианты хуже

Кратко объясни, почему ты НЕ рекомендуешь использовать остальные подходы.

---

## 5. Анализ сайта

Определи насколько это возможно.

Есть ли:

- JavaScript Rendering
- React
- Vue
- Angular
- API
- GraphQL
- Infinite Scroll
- Pagination
- Login
- Cookies
- JWT
- Bearer Token
- CAPTCHA
- Cloudflare
- Rate Limits
- Download Files
- Upload Files
- Lazy Loading
- WebSocket
- XHR/Fetch
- Sitemap
- robots.txt

Если определить невозможно — так и напиши.

---

## 6. Что необходимо собрать до начала разработки

Какие данные необходимо получить до начала разработки.

Например

- page.html
- network.har
- cookies
- response.json
- пример CSV
- пример Excel
- скриншоты
- тестовый аккаунт
- пример ожидаемого результата
- образец выходного файла

Если что-либо необходимо —
перечисли это.

---

## 7. Возможные сложности

Перечисли потенциальные проблемы.

Например

- блокировки
- изменение HTML
- скрытый API
- динамическая загрузка
- авторизация
- ограничение скорости
- большое количество страниц

---

## 8. Что нужно уточнить у клиента

Если информации недостаточно —
составь список вопросов клиенту.
Не придумывай ответы самостоятельно.

---

## 9. Рекомендуемый стек технологий

Укажи только основные технологии, которые будут использоваться.

Например:

- Python
- Playwright
- BeautifulSoup
- requests
- API

Не перечисляй конкретные библиотеки для установки.

Не составляй requirements.txt.


---

## 10. План разработки

Разбей проект на логические этапы разработки.

Каждый этап должен содержать:

- цель;
- ожидаемый результат;
- зависимости (если есть).

---

## 11. Оценка сложности

Оцени:

- сложность (1–10);
- время на разработки - (Estimation в часах)
- вероятность блокировок;
- вероятность необходимости использования браузера;
- вероятность изменения сайта в будущем;
- общую оценку риска.

---

## 12. Можно ли решить проще

---
Определи можно ли выполнить проект более простым способом.

Например:

API вместо HTML.
Активно искать API в network.har или через консоль разработчика
requests вместо Playwright.
CSV вместо базы данных.
Если существует более простое решение —
обязательно предложи его.

## 13. Итоговая рекомендация

Кратко подведи итог.

Ответь:

- Какое решение рекомендуется.
- Почему оно оптимально.
- Что необходимо получить перед началом разработки.
- Можно ли переходить к написанию кода или сначала нужно дождаться ответов клиента.


# IMPORTANT RULES

НЕ переходи к реализации.
НЕ проектируй архитектуру классов.
НЕ предлагай реализацию функций.
НЕ предлагай  структуру каталогов.
НЕ генерируй код.
НЕ создавай Dockerfile.
НЕ создавай requirements.txt.
Не делай предположений, если информации недостаточно.
Явно указывай уровень уверенности в своих выводах.

# SELF-CHECK

Перед отправкой ответа проверь:
□ Я не написал код.
□ Я не начал проектировать функции.
□ Я выбрал наиболее подходящую технологию.
□ Я перечислил возможные риски.
□ Я указал, какой информации не хватает.
□ Я сформировал список вопросов клиенту.
□ Я предложил наиболее простое решение.
□ Я не усложнил архитектуру без необходимости.
Если хотя бы один пункт не выполнен — исправь ответ перед отправкой.
