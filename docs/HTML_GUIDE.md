# Как собирать данные с HTML-сайтов для скрапинга

## Когда нужен HTML-парсинг

Ты уже проверил Network → Fetch/XHR и не нашёл API с данными. Значит данные "вшиты" прямо в HTML-код страницы. Нужен BeautifulSoup (или Playwright если есть JavaScript-рендеринг).

---

## Главное правило: сохраняй МИНИМУМ, но ПРАВИЛЬНЫЙ минимум

**НЕ НАДО:** сохранять всю страницу (3000-10000 строк)
**НАДО:** вырезать конкретные куски, которые нужны ИИ для написания селекторов

---

## Что сохранять для каждого типа страницы

---

## 1. Карточка товара (listing page)

Это страница каталога, где много товаров сразу (сетка или список).

### Что нужно ИИ:

| Что сохранить | Зачем | Куда |
|---------------|-------|------|
| Одна полная карточка | Написать `parse_single_item()` | `card_example.html` |
| Контейнер всех карточек (первые 2-3) | Написать `soup.select()` для списка | `listing_container.html` |
| URL страницы | Знать откуда парсить | `description.txt` |

### Как вырезать карточку:

```
1. DevTools → Elements (Ctrl+Shift+C)
2. Наведи курсор на карточку товара — она подсветится
3. В панели Elements найди элемент, который содержит ВСЮ карточку
4. Правый клик на элементе → Copy → Copy outerHTML
5. Вставь в AI_INPUT/card_example.html
```

### Как это выглядит в DevTools (Elements):

```
┌─ Elements ──────────────────────────────────────────────────────────┐
│                                                                      │
│  ▼ <div class="products-grid">          ← контейнер ВСЕХ карточек   │
│    ▼ <div class="product-card">         ← ★ ОДНА карточка (копируй) │
│        <a href="/product/12345">                                     │
│          <img src="https://cdn.site.com/img/laptop.jpg"             │
│               class="product-image">                                 │
│        </a>                                                          │
│        <div class="product-info">                                    │
│          <h3 class="product-title">Gaming Laptop RTX 4060</h3>      │
│          <div class="price-wrapper">                                 │
│            <span class="price-new">$999</span>                       │
│            <span class="price-old">$1,299</span>                     │
│          </div>                                                      │
│          <div class="rating">                                        │
│            <span class="stars" data-rating="4.5">★★★★☆</span>       │
│            <span class="review-count">(234)</span>                   │
│          </div>                                                      │
│        </div>                                                        │
│      </div>                             ← конец карточки             │
│    ▶ <div class="product-card">         ← следующая карточка         │
│    ▶ <div class="product-card">                                      │
│    ...                                                               │
│  </div>                                                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Что сохранить в `AI_INPUT/card_example.html`:

```html
<!-- Страница: https://shop.com/catalog/laptops -->
<!-- Контейнер всех карточек: div.products-grid -->
<!-- Одна карточка: div.product-card -->

<div class="product-card">
  <a href="/product/12345">
    <img src="https://cdn.site.com/img/laptop.jpg" class="product-image">
  </a>
  <div class="product-info">
    <h3 class="product-title">Gaming Laptop RTX 4060</h3>
    <div class="price-wrapper">
      <span class="price-new">$999</span>
      <span class="price-old">$1,299</span>
    </div>
    <div class="rating">
      <span class="stars" data-rating="4.5">★★★★☆</span>
      <span class="review-count">(234)</span>
    </div>
  </div>
</div>
```

**Обрати внимание:** Я добавил комментарии вверху — селектор контейнера и селектор карточки. Это критически важно для ИИ.

### Что написать в `AI_INPUT/description.txt`:

```
# Задача
URL: https://shop.com/catalog/laptops
Способ: HTML + BeautifulSoup (API не найден)

# Что собрать
- title (название товара)
- price (текущая цена)
- old_price (старая цена, может отсутствовать)
- rating (число 1-5)
- reviews_count (число)
- product_url (ссылка на товар)
- image_url (ссылка на изображение)

# Структура HTML
- Контейнер всех карточек: div.products-grid
- Одна карточка: div.product-card
- Пример карточки: см. card_example.html

# Формат вывода
CSV
```

---

## 2. Пагинация

### Тип A: Номера страниц в URL (?page=N)

```
Страница 1: https://shop.com/catalog/laptops
Страница 2: https://shop.com/catalog/laptops?page=2
Страница 3: https://shop.com/catalog/laptops?page=3
```

**Что сохранить:** Только паттерн URL (в description.txt)

```
# Пагинация
Тип: URL-параметр
Паттерн: https://shop.com/catalog/laptops?page={N}
Первая страница: page=1 (или без параметра)
Последняя страница: неизвестно (нужно определять по отсутствию товаров)
```

### Тип B: Кнопка "Next" / "Далее" (нужен Playwright)

Вырежи HTML кнопки пагинации:

```
1. DevTools → Elements
2. Найди блок пагинации внизу страницы
3. Правый клик → Copy → Copy outerHTML
```

**Что сохранить в `AI_INPUT/pagination.html`:**

```html
<!-- Блок пагинации (внизу страницы каталога) -->

<nav class="pagination">
  <a href="/catalog?page=1" class="page-link">1</a>
  <a href="/catalog?page=2" class="page-link active">2</a>
  <a href="/catalog?page=3" class="page-link">3</a>
  <span class="page-dots">...</span>
  <a href="/catalog?page=15" class="page-link">15</a>
  <a href="/catalog?page=3" class="page-link next">Next →</a>
</nav>
```

**В description.txt добавь:**

```
# Пагинация
Тип: HTML-ссылки
Блок пагинации: nav.pagination
Кнопка "Далее": a.page-link.next
Последняя страница: видна в пагинации (15)
Пример: см. pagination.html
```

### Тип C: Бесконечный скролл (infinite scroll)

Нет кнопок, данные подгружаются при прокрутке.

**Как определить:**
- Нет блока пагинации
- При скролле вниз появляются новые товары
- В Network видны новые запросы при скролле

**Что сохранить:**

```
# Пагинация
Тип: бесконечный скролл (infinite scroll)
Нужен Playwright для прокрутки
При скролле подгружаются новые div.product-card в тот же div.products-grid
Всего товаров: ~500 (видно в заголовке "Showing 500 results")
```

### Тип D: Кнопка "Показать ещё" / "Load More"

```html
<!-- Кнопка подгрузки -->
<button class="load-more-btn" data-page="2">Показать ещё</button>
```

**В description.txt:**
```
# Пагинация
Тип: кнопка "Load More"
Селектор: button.load-more-btn
Нужен Playwright (клик по кнопке)
После клика новые карточки добавляются в div.products-grid
```

---

## 3. Страница входа (Login)

### Когда нужна авторизация:
- Сайт показывает "Please login to view prices"
- При переходе редиректит на /login
- Часть данных скрыта за логином (email продавца, телефон)

### Что сохранить:

#### Файл: `AI_INPUT/login_page.html`

Вырежи ТОЛЬКО форму логина:

```html
<!-- URL страницы логина: https://site.com/login -->
<!-- Форма авторизации -->

<form action="/api/auth/login" method="POST" class="login-form">
  <input type="email" name="email" placeholder="Email" required>
  <input type="password" name="password" placeholder="Password" required>
  <input type="hidden" name="_token" value="abc123xyz">
  <button type="submit" class="btn-login">Sign In</button>
</form>
```

#### Что важно заметить:

```
┌────────────────────────────────────────────────────────────────┐
│ На что обращать внимание в форме логина:                        │
│                                                                │
│ 1. action="/api/auth/login"  ← КУДА отправляется форма        │
│ 2. method="POST"             ← Метод (всегда POST для логина) │
│ 3. name="email"              ← Имена полей (для requests)     │
│ 4. name="password"           ← Имя поля пароля                │
│ 5. name="_token"             ← CSRF-токен! (нужно получить)   │
│ 6. Есть ли CAPTCHA?          ← Если есть — сложнее            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### В description.txt добавь:

```
# Авторизация
Нужна: ДА
URL логина: https://site.com/login
Метод: POST на /api/auth/login
Поля: email, password
CSRF-токен: есть (hidden поле "_token")
CAPTCHA: нет
Тестовый аккаунт: login@example.com / password123

После логина:
- Сайт ставит cookie "session_id"
- Все дальнейшие запросы должны содержать эту cookie
```

#### Файл: `AI_INPUT/cookies.json` (после ручного логина)

Если проще — залогинься вручную и сохрани cookies:

```
1. Залогинься в Chrome
2. DevTools → Application → Cookies → выбери домен
3. Или используй расширение "EditThisCookie" → Export
```

```json
[
  {
    "name": "session_id",
    "value": "eyJhbGciOiJIUzI1NiIs...",
    "domain": ".site.com",
    "path": "/"
  },
  {
    "name": "user_token",
    "value": "abc123def456",
    "domain": ".site.com",
    "path": "/"
  }
]
```

---

## 4. Страница товара (detail page)

Когда нужно собирать данные не только из каталога, но и заходить на каждый товар.

### Что сохранить в `AI_INPUT/product_page.html`:

Вырежи ТОЛЬКО блок с данными (не всю страницу!):

```html
<!-- URL: https://shop.com/product/gaming-laptop-rtx-4060 -->
<!-- Блок товара: div.product-detail -->

<div class="product-detail">
  <h1 class="product-title">Gaming Laptop RTX 4060 16GB RAM</h1>

  <div class="product-gallery">
    <img src="https://cdn.site.com/img/main.jpg" class="main-image">
    <img src="https://cdn.site.com/img/side.jpg" class="thumb">
    <img src="https://cdn.site.com/img/back.jpg" class="thumb">
  </div>

  <div class="product-price">
    <span class="current-price">$999.00</span>
    <span class="old-price">$1,299.00</span>
    <span class="discount">-23%</span>
  </div>

  <div class="product-specs">
    <table class="specs-table">
      <tr><td>Brand</td><td>ASUS</td></tr>
      <tr><td>CPU</td><td>Intel i7-13700H</td></tr>
      <tr><td>RAM</td><td>16GB DDR5</td></tr>
      <tr><td>GPU</td><td>RTX 4060 8GB</td></tr>
      <tr><td>Storage</td><td>512GB SSD</td></tr>
      <tr><td>Screen</td><td>15.6" FHD 144Hz</td></tr>
    </table>
  </div>

  <div class="product-description">
    <p>High-performance gaming laptop with latest GPU...</p>
  </div>

  <div class="seller-info">
    <span class="seller-name">TechStore Official</span>
    <span class="seller-rating">98% positive</span>
    <a href="/seller/techstore">View seller</a>
  </div>

  <div class="availability">
    <span class="in-stock">In Stock</span>
    <span class="delivery">Free shipping, 2-3 days</span>
  </div>
</div>
```

### В description.txt:

```
# Страница товара (detail)
URL паттерн: https://shop.com/product/{slug}
Блок данных: div.product-detail

Поля для сбора:
- title: h1.product-title
- price: span.current-price
- old_price: span.old-price (может отсутствовать)
- discount: span.discount (может отсутствовать)
- images: все img в div.product-gallery
- specs: таблица table.specs-table (ключ-значение)
- description: div.product-description
- seller: span.seller-name
- in_stock: есть ли span.in-stock
- delivery: span.delivery

Пример HTML: см. product_page.html
```

---

## 5. Таблица данных

Часто встречается на сайтах статистики, финансов, спорта.

### Что сохранить в `AI_INPUT/table_example.html`:

Вырежи заголовок + 2-3 строки:

```html
<!-- URL: https://stats.com/players -->
<!-- Таблица: table.data-table -->

<table class="data-table" id="players-stats">
  <thead>
    <tr>
      <th>Rank</th>
      <th>Player</th>
      <th>Team</th>
      <th>Goals</th>
      <th>Assists</th>
      <th>Rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><a href="/player/123">Lionel Messi</a></td>
      <td>Inter Miami</td>
      <td>15</td>
      <td>12</td>
      <td>9.2</td>
    </tr>
    <tr>
      <td>2</td>
      <td><a href="/player/456">Kylian Mbappé</a></td>
      <td>Real Madrid</td>
      <td>14</td>
      <td>8</td>
      <td>8.9</td>
    </tr>
  </tbody>
</table>
```

**Таблицы — самые простые для парсинга.** ИИ сразу напишет:
```python
rows = soup.select("table.data-table tbody tr")
```

---

## 6. Фильтры и формы поиска

Если нужно парсить с фильтрами (категория, город, цена).

### Что сохранить в `AI_INPUT/filters.html`:

```html
<!-- Форма фильтрации -->
<form action="/search" method="GET" class="filter-form">
  <select name="category">
    <option value="laptops">Laptops</option>
    <option value="phones">Phones</option>
    <option value="tablets">Tablets</option>
  </select>

  <select name="brand">
    <option value="">All Brands</option>
    <option value="apple">Apple</option>
    <option value="samsung">Samsung</option>
  </select>

  <input type="number" name="price_min" placeholder="Min price">
  <input type="number" name="price_max" placeholder="Max price">

  <select name="sort">
    <option value="popular">Most Popular</option>
    <option value="price_asc">Price: Low to High</option>
    <option value="price_desc">Price: High to Low</option>
  </select>

  <button type="submit">Apply</button>
</form>
```

**Зачем:** ИИ увидит URL-параметры и сможет генерировать URL для разных фильтров:
```
https://shop.com/search?category=laptops&brand=apple&price_min=500&sort=price_asc
```

---

## 7. Защита от ботов (Cloudflare, CAPTCHA)

### Как определить Cloudflare:

```
┌────────────────────────────────────────────────────────────────────┐
│  Признаки Cloudflare:                                              │
│                                                                    │
│  1. При первом заходе — экран "Checking your browser..."           │
│     с крутилкой на 3-5 секунд                                      │
│                                                                    │
│  2. В DevTools → Network → первый запрос:                          │
│     Status: 403 или 503                                            │
│     Server: cloudflare                                              │
│                                                                    │
│  3. В Cookies появляется:                                          │
│     cf_clearance=...                                                │
│     __cf_bm=...                                                     │
│                                                                    │
│  4. В HTML видно:                                                   │
│     <title>Just a moment...</title>                                 │
│     <div id="challenge-running">                                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Что сохранить если есть Cloudflare:

В `description.txt` добавь:
```
# Защита
Cloudflare: ДА
Тип challenge: JavaScript challenge (не CAPTCHA)
Нужен: Playwright с ожиданием (wait 5-10 sec)
Cookies после прохождения: cf_clearance (сохранить и переиспользовать)
```

### Как определить CAPTCHA:

```
Типы:
- reCAPTCHA (Google) — чекбокс "I'm not a robot" или картинки
- hCaptcha — похоже на reCAPTCHA, но другой логотип
- Cloudflare Turnstile — невидимая, автоматическая
- Кастомная — "введите символы с картинки"
```

В `description.txt`:
```
# Защита
CAPTCHA: reCAPTCHA v2 (чекбокс)
Появляется: после 50+ запросов / при логине
Решение: нужен сервис (2captcha/anticaptcha) ИЛИ ручное решение
```

---

## 8. JavaScript-рендеринг (SPA)

### Как определить что сайт на React/Vue/Angular:

```
┌────────────────────────────────────────────────────────────────────┐
│  Метод 1: View Source (Ctrl+U)                                     │
│                                                                    │
│  Если в исходном коде видишь:                                       │
│    <div id="root"></div>        ← React                            │
│    <div id="app"></div>         ← Vue                              │
│    <app-root></app-root>        ← Angular                          │
│  И НЕ видишь данных (товаров, текста) — это SPA.                   │
│  Данные загружаются JavaScript'ом.                                  │
│                                                                    │
│  Метод 2: Отключить JavaScript                                     │
│                                                                    │
│  DevTools → Settings (F1) → Debugger → Disable JavaScript          │
│  Перезагрузи страницу.                                              │
│  Если страница пустая или "Enable JavaScript" — это SPA.            │
│                                                                    │
│  Метод 3: Сравни View Source и Elements                            │
│                                                                    │
│  Ctrl+U (source): пустая страница, только <div id="root">         │
│  F12 → Elements: полный DOM с товарами                             │
│  Разница = JavaScript генерирует контент                           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Что это значит:**
- `requests.get()` вернёт ПУСТУЮ страницу (без данных)
- Нужен **Playwright** (который выполнит JavaScript)
- ИЛИ ищи API (SPA-сайты ВСЕГДА используют API для загрузки данных!)

**В description.txt:**
```
# Рендеринг
Тип: SPA (React)
View Source пустой — данные загружаются через JS
Проверь Network → Fetch/XHR — скорее всего есть API!
Если API не найден → нужен Playwright
```

---

## 9. Скрытые данные в HTML (JSON в script)

Многие сайты встраивают данные прямо в HTML как JSON внутри `<script>`:

### Как найти:

```
1. Ctrl+U (View Source)
2. Ctrl+F → ищи: "__NEXT_DATA__" или "window.__data" или "application/ld+json"
```

### Как это выглядит:

```html
<!-- Next.js сайт (очень частое) -->
<script id="__NEXT_DATA__" type="application/json">
{
  "props": {
    "pageProps": {
      "products": [
        {"id": 1, "title": "Laptop", "price": 999},
        {"id": 2, "title": "Phone", "price": 599}
      ]
    }
  }
}
</script>

<!-- Или structured data (schema.org) -->
<script type="application/ld+json">
{
  "@type": "Product",
  "name": "Gaming Laptop",
  "offers": {"price": 999, "priceCurrency": "USD"}
}
</script>

<!-- Или кастомный формат -->
<script>
  window.__INITIAL_STATE__ = {"catalog": {"items": [...]}};
</script>
```

**Это ЗОЛОТО!** Не нужен ни Playwright, ни BeautifulSoup для карточек. Просто:
```python
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
script = soup.find("script", id="__NEXT_DATA__")
data = json.loads(script.string)
products = data["props"]["pageProps"]["products"]
```

### Что сохранить в `AI_INPUT/embedded_json.txt`:

```
# Скрытые данные в HTML

Найдено в View Source (Ctrl+U → Ctrl+F → "__NEXT_DATA__"):

Тег: <script id="__NEXT_DATA__" type="application/json">
Путь к данным: props.pageProps.products

Пример (первые 2 элемента):
{
  "id": 1,
  "title": "Gaming Laptop",
  "price": 999,
  "rating": 4.5,
  "image": "/img/laptop.jpg"
}
```

---

## Итого: что сохранять для каждой ситуации

### Минимальный набор файлов в AI_INPUT:

```
AI_INPUT/
├── description.txt         ← ВСЕГДА (URL + поля + способ + пагинация)
├── card_example.html       ← если парсим каталог (одна карточка)
├── pagination.html         ← если пагинация через кнопки (не URL)
├── product_page.html       ← если нужно заходить на каждый товар
├── login_page.html         ← если нужна авторизация
├── cookies.json            ← если залогинился вручную
├── table_example.html      ← если парсим таблицу
├── filters.html            ← если нужно перебирать фильтры
├── embedded_json.txt       ← если нашёл JSON в <script>
└── response_example.json   ← если нашёл API (лучший случай!)
```

### Что ОБЯЗАТЕЛЬНО указать в description.txt:

```
# Задача
URL: [ссылка на страницу]
Что собрать: [список полей]
Формат вывода: CSV / JSON / Excel

# Способ получения данных
[API / HTML+BS4 / Playwright]
Причина: [почему этот способ]

# Структура (селекторы)
Контейнер списка: [селектор]
Одна карточка: [селектор]
Пример: см. [файл]

# Пагинация
Тип: [URL ?page=N / кнопка Next / скролл / Load More]
Всего страниц: [число или "неизвестно"]

# Защита
Cloudflare: [да/нет]
CAPTCHA: [да/нет]
Логин: [да/нет]

# Особенности
[что-то необычное: iframe, shadow DOM, lazy loading и т.д.]
```

---

## Как вырезать HTML правильно (пошагово)

### Метод 1: Через DevTools Elements (рекомендуемый)

```
1. F12 → Elements
2. Ctrl+Shift+C (режим выбора элемента)
3. Кликни на нужный элемент на странице
4. В панели Elements он подсветится
5. Поднимись на уровень выше если нужен контейнер
   (стрелки ▶ слева раскрывают/сворачивают)
6. Правый клик → Copy → Copy outerHTML
7. Вставь в файл
```

### Метод 2: Через Console (если нужен чистый текст)

```javascript
// Скопировать одну карточку:
copy(document.querySelector('.product-card').outerHTML)

// Скопировать все карточки (первые 2):
copy([...document.querySelectorAll('.product-card')].slice(0,2).map(e=>e.outerHTML).join('\n'))

// Скопировать пагинацию:
copy(document.querySelector('.pagination').outerHTML)
```

После команды `copy(...)` результат в буфере обмена — вставляй Ctrl+V.

### Метод 3: View Source + Ctrl+F (для скрытого JSON)

```
1. Ctrl+U (открывает исходный код)
2. Ctrl+F → ищи ключевые слова:
   - "__NEXT_DATA__"
   - "window.__"
   - "application/ld+json"
   - название товара который видишь на странице
3. Скопируй найденный блок
```

---

## Частые ошибки

| Ошибка | Почему плохо | Как правильно |
|--------|-------------|---------------|
| Сохранил всю page.html (Ctrl+S) | 5000+ строк, ИИ теряет контекст | Вырежи одну карточку (20-50 строк) |
| Не указал селекторы | ИИ придумает свои (угадает неправильно) | Напиши: "контейнер: div.products-grid" |
| Скопировал из Elements а не Source | Elements показывает DOM ПОСЛЕ JavaScript | Для SPA-проверки используй Ctrl+U |
| Не проверил API перед HTML | Потратил время на BS4, а API был | Всегда сначала Network → Fetch/XHR |
| Сохранил карточку без контейнера | ИИ не знает как найти ВСЕ карточки | Укажи родительский селектор |
| Не указал тип пагинации | ИИ не знает как переходить по страницам | Укажи: URL / кнопка / скролл |

---

## Приоритет: что проверять первым

```
1. Network → Fetch/XHR → есть API?           → ЛУЧШИЙ вариант
   ↓ нет
2. Ctrl+U → Ctrl+F → есть JSON в <script>?   → ОТЛИЧНЫЙ вариант
   ↓ нет
3. Ctrl+U → видны ли данные в HTML?           → requests + BS4
   ↓ нет (HTML пустой)
4. SPA → данные только через JavaScript       → Playwright
                                                 (но вернись к п.1 — API точно есть!)
```
