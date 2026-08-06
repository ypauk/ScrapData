# Как находить и использовать API для скрапинга

## Что такое API в контексте скрапинга

Когда ты открываешь сайт, браузер загружает HTML (каркас страницы). Но данные (товары, цены, отзывы) часто приходят ОТДЕЛЬНЫМ запросом в формате JSON. Этот запрос — и есть API.

**Почему API лучше HTML-парсинга:**
- Данные уже структурированы (не нужен BeautifulSoup)
- Не нужен Playwright (работает через обычный requests)
- Не ломается при изменении дизайна
- Быстрее в 10-50 раз
- Код в 5 раз короче

---

## Шаг 1. Открой DevTools → Network

### Как открыть:
```
Chrome/Edge: F12 → вкладка "Network"
Или: Ctrl+Shift+I → Network
Или: правый клик → "Inspect" → Network
```

### Что ты увидишь:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Elements  Console  Sources  [Network]  Performance  Memory          │
├─────────────────────────────────────────────────────────────────────┤
│ Filter: [___________]  [All] [Fetch/XHR] [JS] [CSS] [Img] [Doc]   │
├──────┬──────────┬────────┬──────┬───────┬───────────────────────────┤
│Status│ Name     │ Type   │ Size │ Time  │                           │
├──────┼──────────┼────────┼──────┼───────┤                           │
│ 200  │ page.html│ doc    │ 45KB │ 120ms │  ← HTML страницы          │
│ 200  │ style.css│ css    │ 12KB │ 50ms  │  ← стили (не нужно)       │
│ 200  │ app.js   │ script │ 89KB │ 80ms  │  ← скрипт (не нужно)     │
│ 200  │ products?│ fetch  │ 8KB  │ 200ms │  ← ЭТО API! ★★★          │
│ 200  │ banner.jp│ img    │ 35KB │ 100ms │  ← картинка (не нужно)    │
└──────┴──────────┴────────┴──────┴───────┴───────────────────────────┘
```

---

## Шаг 2. Фильтруй — нажми "Fetch/XHR"

Эта кнопка убирает весь мусор (картинки, CSS, JS) и показывает ТОЛЬКО запросы за данными.

```
┌─────────────────────────────────────────────────────────────────────┐
│ Filter: [___________]  [All] [★Fetch/XHR★] [JS] [CSS] [Img] [Doc] │
├──────┬──────────────────────────┬────────┬──────┬───────────────────┤
│Status│ Name                     │ Type   │ Size │ Time              │
├──────┼──────────────────────────┼────────┼──────┼───────────────────┤
│ 200  │ /api/v2/products?page=1  │ fetch  │ 8KB  │ 200ms  ★ ДАННЫЕ  │
│ 200  │ /api/user/session        │ xhr    │ 1KB  │ 50ms   (сессия)  │
│ 200  │ /api/cart/count          │ xhr    │ 0.2KB│ 30ms   (корзина) │
│ 200  │ /api/recommendations     │ fetch  │ 4KB  │ 150ms  (похожие) │
└──────┴──────────────────────────┴────────┴──────┴───────────────────┘
```

**Как понять какой запрос нужный:**
- Самый большой по Size (8KB > 1KB) — там обычно данные
- В имени есть: `products`, `items`, `listings`, `search`, `catalog`
- Type = `fetch` или `xhr`

---

## Шаг 3. Кликни на запрос → смотри ответ

Когда кликнешь на строку — справа откроется панель с деталями:

```
┌──────────────────────────────────────────────────────────────────────┐
│  [Headers]  [Preview]  [Response]  [Cookies]  [Timing]               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ★ Вкладка "Headers" — информация о запросе:                         │
│                                                                      │
│  Request URL: https://api.shop.com/v2/products?category=laptops&p=1  │
│  Request Method: GET                                                 │
│  Status Code: 200 OK                                                 │
│                                                                      │
│  ★ Вкладка "Preview" — данные в удобном виде (дерево):               │
│                                                                      │
│  ▼ {                                                                 │
│    ▼ items: Array(20)                                                │
│      ▼ 0: {                                                          │
│          id: 12345                                                   │
│          title: "Gaming Laptop RTX 4060"                             │
│          price: 999.00                                               │
│          currency: "USD"                                              │
│          rating: 4.5                                                 │
│          reviews_count: 234                                          │
│          image: "https://cdn.shop.com/img/12345.jpg"                 │
│          url: "/product/gaming-laptop-rtx-4060"                      │
│        }                                                             │
│      ▶ 1: {id: 12346, title: "Ultrabook Pro 14"...}                 │
│      ▶ 2: {id: 12347, title: "MacBook Air M3"...}                   │
│    total: 450                                                        │
│    page: 1                                                           │
│    total_pages: 23                                                   │
│  }                                                                   │
│                                                                      │
│  ★ Вкладка "Response" — сырой JSON (для копирования):                │
│                                                                      │
│  {"items":[{"id":12345,"title":"Gaming Laptop RTX 4060",...}],...}    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Что тебе нужно отсюда:**
1. **URL запроса** (из Headers)
2. **Метод** (GET или POST)
3. **JSON ответ** (из Response — скопировать 1-2 элемента)
4. **Headers** запроса (если есть Authorization)

---

## Шаг 4. Проверь пагинацию

Прокрути страницу вниз или нажми "Next Page" на сайте. Смотри какой новый запрос появился:

```
Было:   /api/v2/products?category=laptops&page=1&per_page=20
Стало:  /api/v2/products?category=laptops&page=2&per_page=20
                                           ^^^^^^
                                           Меняется только page!
```

**Паттерны пагинации в API:**

| Паттерн | Пример | Как использовать |
|---------|--------|-----------------|
| page= | `?page=1`, `?page=2` | `for page in range(1, total+1)` |
| offset= | `?offset=0`, `?offset=20` | `for offset in range(0, total, 20)` |
| cursor= | `?cursor=abc123` | Берёшь cursor из предыдущего ответа |
| skip/limit | `?skip=0&limit=50` | `for skip in range(0, total, 50)` |

---

## Шаг 5. Проверь нужны ли Headers

### Кликни на запрос → Headers → Request Headers:

```
┌──────────────────────────────────────────────────────────────────────┐
│  ▼ Request Headers                                                   │
│                                                                      │
│    Accept: application/json                                          │
│    Authorization: Bearer eyJhbGciOiJIUzI1NiIs...    ← ★ ВАЖНО!     │
│    Cookie: session_id=abc123; user=john              ← ★ ВАЖНО!     │
│    User-Agent: Mozilla/5.0 (Windows NT 10.0...                       │
│    X-API-Key: pk_live_abc123def456                   ← ★ ВАЖНО!     │
│    Referer: https://shop.com/catalog                                 │
│    Accept-Language: en-US,en;q=0.9                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Что важно:**
- `Authorization` — токен доступа (без него API не ответит)
- `Cookie` — сессия (если сайт требует логин)
- `X-API-Key` — ключ API (без него 403)
- Остальное обычно не обязательно

**Как проверить что нужно:** Открой новую вкладку инкогнито, вставь URL API — если отдаёт данные без авторизации, headers не нужны.

---

## Шаг 6. Скопируй как cURL (самый быстрый способ)

Правый клик на запрос → **Copy** → **Copy as cURL (bash)**:

```
┌────────────────────────────────────────────┐
│  Copy link address                          │
│  Copy as PowerShell                         │
│  ★ Copy as cURL (bash)  ← ЭТО!            │
│  Copy as fetch                              │
│  Copy response                              │
│  Copy all as HAR                            │
└────────────────────────────────────────────┘
```

Получишь что-то вроде:
```bash
curl 'https://api.shop.com/v2/products?page=1&per_page=20' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer eyJhbG...' \
  -H 'User-Agent: Mozilla/5.0...'
```

**Это можно вставить в терминал** для проверки — если вернёт JSON, значит API работает.

---

## Шаг 7. Что сохранить в AI_INPUT

После того как нашёл API, сохрани:

### Файл: `AI_INPUT/description.txt`
```
# Задача
URL сайта: https://shop.com/catalog/laptops
Собрать: title, price, rating, reviews_count, image, product_url
Формат: CSV
Всего товаров: ~450

# API (найден)
Endpoint: https://api.shop.com/v2/products
Method: GET
Параметры:
  - category=laptops (фильтр)
  - page=1,2,3... (пагинация)
  - per_page=20 (элементов на странице)
Всего страниц: 23

# Авторизация
Не требуется (работает без токена)
```

### Файл: `AI_INPUT/response_example.json`
```json
{
  "items": [
    {
      "id": 12345,
      "title": "Gaming Laptop RTX 4060",
      "price": 999.00,
      "currency": "USD",
      "rating": 4.5,
      "reviews_count": 234,
      "image": "https://cdn.shop.com/img/12345.jpg",
      "url": "/product/gaming-laptop-rtx-4060"
    },
    {
      "id": 12346,
      "title": "Ultrabook Pro 14",
      "price": 1299.00,
      "currency": "USD",
      "rating": 4.8,
      "reviews_count": 567,
      "image": "https://cdn.shop.com/img/12346.jpg",
      "url": "/product/ultrabook-pro-14"
    }
  ],
  "total": 450,
  "page": 1,
  "total_pages": 23
}
```

### Файл: `AI_INPUT/headers.json` (если нужна авторизация)
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs...",
  "Accept": "application/json",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
```

---

## Что ИИ напишет по этим данным

Из трёх файлов выше ИИ сгенерирует примерно такой scraper.py:

```python
import requests
import time
from typing import List

BASE_URL = "https://api.shop.com/v2/products"

def fetch_page_data(context=None) -> List[str]:
    """Собирает все страницы через API."""
    all_responses = []
    page = 1

    while True:
        params = {"category": "laptops", "page": page, "per_page": 20}

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break

        data = response.json()
        all_responses.append(response.text)

        if page >= data["total_pages"]:
            break

        page += 1
        time.sleep(1)

    return all_responses
```

**15 строк** вместо 70 строк с Playwright + BeautifulSoup.

---

## Реальные примеры: где искать API

### Пример 1: Интернет-магазин

```
Действие:  Открыл каталог → включил Network (Fetch/XHR) → прокрутил

Что вижу:
  GET /api/catalog/products?category_id=15&page=1&sort=popular

В Preview:
  { "products": [...], "pagination": {"current": 1, "total": 12} }
```

### Пример 2: Сайт объявлений

```
Действие:  Открыл поиск → ввёл запрос → нажал "Искать"

Что вижу:
  POST /search/results
  Body: {"query": "laptop", "city": "kyiv", "page": 1}

В Preview:
  { "ads": [...], "total_found": 1234 }
```

### Пример 3: Сайт с отзывами

```
Действие:  Открыл товар → прокрутил вниз к отзывам

Что вижу:
  GET /reviews?product_id=555&page=1&sort=newest

В Preview:
  { "reviews": [...], "stats": {"avg": 4.3, "total": 89} }
```

### Пример 4: Сайт без API (нет запросов Fetch/XHR с данными)

```
Действие:  Включил Network → перезагрузил → фильтр Fetch/XHR

Что вижу:
  GET /analytics (аналитика — не данные)
  GET /session (сессия — не данные)
  ... больше ничего

Вывод: API нет. Данные в HTML. Нужен BeautifulSoup или Playwright.
```

---

## POST vs GET

### GET — данные в URL (параметры после ?)
```
GET https://api.site.com/products?page=2&category=phones

В коде:
  requests.get(url, params={"page": 2, "category": "phones"})
```

### POST — данные в теле запроса (Body)

Как увидеть Body в DevTools:
```
┌──────────────────────────────────────────────────────────────────────┐
│  [Headers]  [★Payload★]  [Preview]  [Response]                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ▼ Request Payload (или Form Data):                                  │
│                                                                      │
│    {                                                                  │
│      "query": "laptop",                                              │
│      "filters": {"price_min": 500, "price_max": 2000},              │
│      "page": 1,                                                      │
│      "limit": 50                                                     │
│    }                                                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

```python
# В коде:
requests.post(url, json={"query": "laptop", "page": 1, "limit": 50})
```

---

## GraphQL (особый случай)

Некоторые сайты (Shopify, GitHub) используют GraphQL. Один endpoint, разные запросы:

```
Всегда POST на один URL:  /graphql  или  /api/graphql

В Payload видишь:
{
  "query": "{ products(first: 20) { edges { node { title price } } } }",
  "variables": {"page": 1}
}
```

**Как распознать:** Все запросы на один URL, в Body есть поле `"query"` с фигурными скобками.

**Что делать:** Скопируй `query` и `variables` в AI_INPUT — ИИ разберётся.

---

## HAR-файл (автоматический способ)

Если не хочешь вручную искать — сохрани всё одним файлом:

1. DevTools → Network
2. Перезагрузи страницу
3. Прокрути, покликай (чтобы записались все запросы)
4. Правый клик на любом запросе → **Save all as HAR with content**
5. Сохрани в `AI_INPUT/network.har`

ИИ сам найдёт нужный API в HAR-файле. Но HAR большой (500KB-5MB) — для бесплатных ИИ лучше вручную найти нужный запрос.

---

## Чек-лист: нашёл ли я API?

- [ ] Открыл DevTools → Network → Fetch/XHR
- [ ] Перезагрузил страницу / перешёл на следующую
- [ ] Нашёл запрос, в Preview которого есть мои данные (товары/цены/отзывы)
- [ ] Записал URL запроса
- [ ] Записал метод (GET/POST)
- [ ] Если POST — записал Body (Payload)
- [ ] Проверил нужны ли Headers (открыл URL в инкогнито)
- [ ] Нажал Next Page — увидел как меняется параметр пагинации
- [ ] Скопировал 1-2 элемента из Response в `response_example.json`

**Если ни один запрос не содержит нужных данных → API нет → используй HTML-парсинг.**

---

## Частые ситуации

### "Вижу запрос, но ответ пустой или 403"
→ Нужны headers (Cookie или Authorization). Скопируй их из DevTools.

### "Данные приходят, но зашифрованы или непонятный формат"
→ Это может быть protobuf или зашифрованный ответ. Лучше использовать HTML-парсинг.

### "API есть, но отдаёт только 10 элементов"
→ Ищи параметр `limit`, `per_page`, `page_size` — поставь максимум (обычно 50-100).

### "На сайте нет кнопки Next, а данные подгружаются при скролле"
→ Скролль и смотри новые запросы в Network. Обычно это тот же API с offset/page+1.

### "URL API содержит длинный токен, который меняется"
→ Токен обычно живёт 1-24 часа. Для разовой задачи — копируй и используй. Для автоматизации — нужно сначала получать токен (отдельный запрос).
