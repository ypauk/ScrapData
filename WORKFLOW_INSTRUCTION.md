# ScrapData — Полная инструкция по работе

## Обзор системы

ScrapData — конвейер для выполнения заказов на парсинг с Upwork. Ты собираешь данные о сайте, генерируешь промпты для ИИ, получаешь код, тестируешь, упаковываешь в Docker и сдаёшь клиенту.

**Главный файл:** `ai_workflow.py` — единая точка входа для всех этапов.

---

## Структура проекта

```
ScrapData/
├── ai_workflow.py          ← Главный скрипт (запуск всех команд)
├── prompt_splitter.py      ← Разбивка/автоотправка промптов в ChatGPT
├── clear_chat.py           ← Удаление активного чата ChatGPT (для тестов)
├── export_for_ai.py        ← Дамп проекта в текст (для отладки)
├── check-list.txt          ← Вопросы перед стартом
├── САМОЕ ГЛАВНОЕ.txt       ← Краткий workflow
├── scraping-templates/     ← Шаблоны промптов и знания
│   ├── prompts/            ← Шаблоны для каждого этапа
│   ├── knowledge/          ← Справка по технологиям
│   ├── templates/          ← Шаблоны Docker, проекта
│   ├── examples/           ← Примеры готовых проектов
│   └── AI_rules.md         ← Правила для ИИ
├── starter-project/        ← Шаблон нового проекта (не трогать!)
├── projects/               ← Здесь живут активные проекты
└── memory/                 ← База знаний по сайтам (TODO)
```

---

## Быстрый старт (5 минут)

```bash
# 1. Создать проект
python ai_workflow.py new имя_проекта

# 2. Заполнить данные (см. ниже)
# 3. Генерировать промпты один за другим
python ai_workflow.py analyze имя_проекта
python ai_workflow.py project имя_проекта
python ai_workflow.py scraper имя_проекта
python ai_workflow.py parser имя_проекта

# ИЛИ: всё сразу одной командой (полная автоматизация)
python ai_workflow.py pipeline имя_проекта --auto

# 4. При ошибке
python ai_workflow.py debug имя_проекта

# 5. Перед сдачей
python ai_workflow.py docker имя_проекта

# 6. Очистка для повторного теста
python ai_workflow.py clean имя_проекта
```

---

## Подробный workflow по шагам

---

### ШАГ 0. Получил заказ — ответь на вопросы

Открой `check-list.txt` и ответь на каждый вопрос:

| Вопрос | Что это значит |
|--------|---------------|
| HTML или API? | Можно ли получить данные через API (быстрее и надёжнее) или нужно парсить HTML? |
| Playwright нужен? | Есть ли JavaScript-рендеринг, который не отдаёт данные без браузера? |
| Есть логин? | Нужна ли авторизация (cookies, токен)? |
| Cloudflare? | Защита от ботов — усложняет работу. |
| CAPTCHA? | Если да — скорее всего отказ или доп. оплата. |
| Бесконечный скролл? | Нужен Playwright для скролла. |
| Пагинация? | Сколько страниц? URL-паттерн (`?page=N`) или кнопка "Next"? |
| Скачивание файлов? | PDF, изображения — дополнительная логика. |

**Результат:** Понимание сложности. Можешь оценить сроки и бюджет для клиента.

---

### ШАГ 1. Создание проекта

```bash
python ai_workflow.py new amazon_scraper
```

**Что происходит:**
- Копируется `starter-project/` в `projects/amazon_scraper/`
- Создаются пустые файлы в `AI_INPUT/`
- Создаётся `project_state.json`
- Очищаются `output/`, `AI_OUTPUT/`, `logs/`

**Результат:** Готовая структура проекта.

---

### ШАГ 2. Сбор данных (заполнение AI_INPUT)

Это САМЫЙ ВАЖНЫЙ шаг. Чем больше данных — тем лучше код от ИИ.

Перейди в `projects/amazon_scraper/AI_INPUT/` и заполни:

#### Обязательные файлы:

| Файл | Как получить | Зачем |
|------|-------------|-------|
| `description.txt` | Написать вручную | ТЗ: URL сайта, какие поля собрать, формат вывода |
| `page.html` | Chrome → Ctrl+S → "Только HTML" | ИИ увидит структуру DOM и напишет правильные селекторы |

#### Рекомендуемые файлы:

| Файл | Как получить | Зачем |
|------|-------------|-------|
| `network.har` | DevTools → Network → правый клик → Save all as HAR | ИИ найдёт скрытый API |
| `cookies.json` | Расширение EditThisCookie → Export | Для авторизованных сайтов |
| `headers.json` | DevTools → Network → скопировать заголовки запроса | Для имитации браузера |
| `screenshots/` | Скриншоты страниц | Наглядность (ИИ не видит, но тебе помогает) |

#### Как заполнить description.txt:

```
# Описание задачи

URL: https://www.amazon.com/s?k=laptop

Что нужно собрать:
- Название товара
- Цена
- Рейтинг (звёзды)
- Количество отзывов
- URL товара
- URL изображения

Формат вывода: CSV

Количество страниц: первые 10

Дополнительно:
- Нужна пагинация (кнопка Next)
- Сайт доступен без логина
```

---

### ШАГ 3. Анализ (этап analyze)

```bash
python ai_workflow.py analyze amazon_scraper
```

**Что происходит:**
- Скрипт берёт шаблон `scraping-templates/prompts/01_analysis_prompt.md`
- Подставляет содержимое `AI_INPUT/` (description + сжатый HTML + другие файлы)
- Сохраняет готовый промпт в `AI_OUTPUT/01_analysis_prompt.md`

**Что делать дальше:**
1. Открой `projects/amazon_scraper/AI_OUTPUT/01_analysis_prompt.md`
2. Скопируй ВЕСЬ текст
3. Вставь в ChatGPT / Gemini / DeepSeek
4. Скопируй ответ ИИ
5. Сохрани в `projects/amazon_scraper/AI_OUTPUT/01_analysis_answer.md`

**Что ИИ должен вернуть:**
- Какой подход выбрать (API / requests / Playwright)
- Какие риски
- Что нужно уточнить у клиента
- Оценку сложности
- План разработки

**Проверь ответ:** Если ИИ предлагает Playwright, а ты видишь что есть API в HAR-файле — поправь вручную. Ты принимаешь решение, не ИИ.

---

### ШАГ 4. Проектирование (этап project)

```bash
python ai_workflow.py project amazon_scraper
```

**Зависимости:** Нужен файл `AI_OUTPUT/01_analysis_answer.md` (с предыдущего шага).

**Что происходит:**
- Берёт шаблон `02_project_prompt.md`
- Подставляет: описание клиента + утверждённый анализ + данные AI_INPUT
- Сохраняет в `AI_OUTPUT/02_project_prompt.md`

**Что делать:**
1. Скопируй `AI_OUTPUT/02_project_prompt.md` в ИИ
2. Ответ сохрани в `AI_OUTPUT/02_project_answer.md`

**Что ИИ должен вернуть:**
- Поток данных (URL → технология → сырые данные → парсер → экспорт)
- Проектирование `scraper.py` (какие функции, алгоритм обхода, пагинация)
- Проектирование `parser.py` (какие функции, какие поля, селекторы)
- Обработка ошибок
- Порядок реализации

**ВАЖНО:** На этом этапе НЕ должно быть кода. Только архитектура. Если ИИ написал код — переделай промпт или вырежи код из ответа.

---

### ШАГ 5. Генерация scraper.py

```bash
python ai_workflow.py scraper amazon_scraper
```

**Зависимости:** Нужны `01_analysis_answer.md` и `02_project_answer.md`.

**Что происходит:**
- Берёт шаблон `03_scraper_prompt.md`
- Подставляет: анализ + план + AI_rules + данные AI_INPUT + код ядра (main.py, config.py и др.) + шаблон scraper.py
- Сохраняет в `AI_OUTPUT/03_scraper_prompt.md`

**Что делать:**
1. Скопируй промпт в ИИ
2. ИИ вернёт готовый код `scraper.py`
3. Сохрани код в `AI_OUTPUT/03_scraper_answer.py`
4. **ТАКЖЕ** скопируй код в `app/scraper.py` (заменив шаблонный)

**Что проверить в коде:**
- Есть ли `fetch_page_data(context)` — эту функцию вызывает `main.py`
- Возвращает ли `List[str]`
- Нет ли классов (только функции)
- Используется ли `random_delay()` между запросами
- Нет ли лишних функций

---

### ШАГ 6. Генерация parser.py

```bash
python ai_workflow.py parser amazon_scraper
```

**Зависимости:** Нужен `03_scraper_answer.py`.

**Что происходит:**
- Берёт шаблон `04_parser_prompt.md`
- Подставляет: код скрапера + AI_rules
- Сохраняет в `AI_OUTPUT/04_parser_prompt.md`

**Что делать:**
1. Скопируй промпт в ИИ
2. Сохрани код в `AI_OUTPUT/04_parser_answer.py`
3. Скопируй код в `app/parser.py`

**Что проверить:**
- Есть ли `parse_html_data(raw_contents: List[str])` — это вызывает `main.py`
- Возвращает ли `List[Dict[str, Any]]`
- Есть ли `parse_single_item()`
- Поля совпадают с тем, что просил клиент

---

### ШАГ 7. Запуск и тестирование

```bash
cd projects/amazon_scraper
pip install -r requirements.txt
playwright install chromium   # только если используется Playwright
python -m app.main
```

**Проверь:**
- Файлы `output/output_results.csv` и `output/output_results.json` созданы
- Данные корректны (открой CSV в Excel)
- Нет пустых полей там, где не должно быть
- Количество записей соответствует ожиданиям

---

### ШАГ 8. Отладка ошибок (при необходимости)

Если скрипт упал:

1. Скопируй traceback (ошибку из консоли)
2. Сохрани в `AI_OUTPUT/traceback.txt`
3. Запусти:

```bash
python ai_workflow.py debug amazon_scraper
```

4. Промпт будет в `AI_OUTPUT/05_debug_prompt.md`
5. Отправь в ИИ → получи исправленный код
6. Замени соответствующий файл в `app/`
7. Запусти снова

**Повторяй** пока не заработает.

---

### ШАГ 9. Docker (перед сдачей клиенту)

```bash
python ai_workflow.py docker amazon_scraper
```

1. Отправь промпт из `AI_OUTPUT/06_docker_prompt.md` в ИИ
2. Получишь: `Dockerfile`, `docker-compose.yml`, `.env.example`
3. Сохрани файлы в корень проекта
4. Проверь:

```bash
docker compose up --build
```

5. Убедись что `output/` содержит результаты

---

### ШАГ 10. Сдача клиенту

Что отправляешь:
- Папку `app/` (код)
- `output/` с примером результата
- `requirements.txt`
- `Dockerfile` + `docker-compose.yml` (если просили)
- `README.md` с инструкцией запуска

**НЕ отправляй:**
- `AI_INPUT/` (твои рабочие файлы)
- `AI_OUTPUT/` (промпты и ответы ИИ)
- `project_state.json`

---

### ШАГ 11. Очистка для повторного тестирования

Если нужно начать генерацию с нуля (при тестировании фреймворка):

```bash
python ai_workflow.py clean amazon_scraper
```

**Что происходит:**
- Все файлы в `AI_OUTPUT/` очищаются (содержимое = пусто, файлы остаются)
- `app/scraper.py` очищается
- `app/parser.py` очищается

После этого можно прогнать pipeline заново.

---

### ШАГ 12. Полный конвейер одной командой (pipeline)

Вместо запуска каждого этапа вручную:

```bash
# Полностью автоматический (отправляет всё в ChatGPT через браузер)
python ai_workflow.py pipeline amazon_scraper --auto

# Полуавтоматический (генерирует промпт, ждёт Enter после ручного ответа)
python ai_workflow.py pipeline amazon_scraper
```

**Что происходит:**
- Последовательно выполняет: analyze → project → scraper → parser
- С `--auto`: каждый промпт автоматически отправляется в ChatGPT, ответ сохраняется, и переход к следующему этапу
- Без `--auto`: генерирует промпт, показывает путь, ждёт Enter — ты вручную копируешь промпт, получаешь ответ, сохраняешь его и нажимаешь Enter для перехода

**Типичный цикл тестирования:**
```bash
python ai_workflow.py clean test1        # сбросить файлы проекта
python clear_chat.py --new               # удалить старый чат в ChatGPT, открыть новый
python ai_workflow.py pipeline test1 --auto  # прогнать заново
cd projects/test1 && python app/main.py   # проверить результат
```

**Или одной строкой:**
```bash
python ai_workflow.py clean test1 && python clear_chat.py --new && python ai_workflow.py pipeline test1 --auto
```

---

### ШАГ 13. Архивация

```bash
python ai_workflow.py archive amazon_scraper
```

Переместит проект в `archive/2026/amazon_scraper/`.

---

## Работа с ИИ — советы

### Какой ИИ использовать на каком этапе:

| Этап | Лучший выбор | Альтернатива |
|------|-------------|-------------|
| Analyze (анализ) | GPT-4o, Claude | Gemini Pro |
| Project (проектирование) | GPT-4o, Claude | Gemini Pro |
| Scraper (код) | Claude, GPT-4o | DeepSeek (проверяй!) |
| Parser (код) | Claude, GPT-4o | DeepSeek |
| Debug (отладка) | Claude, GPT-4o | — |
| Docker | Любой | GPT-4o mini |

### Если промпт слишком длинный для бесплатного ИИ:

**Проблема:** Промпты на этапах scraper/parser содержат 15-30k токенов (весь контекст проекта).

**Решение 1 — Разбить на части:**
1. Сначала отправь ТОЛЬКО `AI_rules` + `project_plan` + описание задачи
2. Потом отправь: "Вот код ядра проекта: [main.py, config.py]"
3. Потом: "Напиши scraper.py по плану выше"

**Решение 2 — Сократить промпт вручную:**
- Открой сгенерированный промпт в `AI_OUTPUT/`
- Удали секции, которые не нужны (например, если не используешь browser.py — убери его)
- Сократи HTML в AI_INPUT до ключевых фрагментов

**Решение 3 — Использовать API ($0.01-0.10 за запрос):**
- GPT-4o mini API: контекст 128k токенов, стоимость копейки
- Claude Sonnet API: контекст 200k, лучшее качество кода

### Если ИИ генерирует лишний код:

Добавь в начало промпта (перед вставкой):
```
ВАЖНО: Не добавляй функции, которые я не просил. Не создавай классы. 
Не добавляй меню, GUI, CLI. Следуй СТРОГО плану проекта.
Верни ТОЛЬКО код одного файла.
```

---

## Файлы ядра проекта (не менять!)

Эти файлы одинаковые для всех проектов. ИИ пишет только `scraper.py` и `parser.py`.

| Файл | Что делает |
|------|-----------|
| `app/main.py` | Запускает всё: браузер → scraper → parser → exporter |
| `app/browser.py` | Настраивает Playwright: headless, user-agent, cookies |
| `app/config.py` | Пути к папкам, таймауты, настройки из env |
| `app/exporter.py` | Сохраняет в CSV и JSON |
| `app/utils.py` | `random_delay()`, `clean_price()`, логгер |

### Контракты (что вызывает main.py):

```python
# scraper.py — ОБЯЗАТЕЛЬНАЯ функция:
def fetch_page_data(context: BrowserContext) -> List[str]:
    """Принимает контекст Playwright, возвращает список HTML-строк."""

# parser.py — ОБЯЗАТЕЛЬНАЯ функция:
def parse_html_data(raw_contents: List[str]) -> List[Dict[str, Any]]:
    """Принимает HTML-строки, возвращает список словарей с данными."""
```

Если ИИ переименовал эти функции — переименуй обратно или поправь main.py.

---

## Типичные проблемы и решения

| Проблема | Причина | Решение |
|----------|---------|---------|
| `ModuleNotFoundError: playwright` | Не установлен | `pip install playwright && playwright install chromium` |
| `TimeoutError` | Страница грузится долго | Увеличь `SCRAPER_TIMEOUT` в env или config.py |
| Пустой CSV | Парсер не нашёл элементы | Проверь селекторы в parser.py — открой page.html в браузере |
| `403 Forbidden` | Сайт блокирует | Добавь cookies, смени User-Agent, добавь задержки |
| ИИ написал класс | Не читает правила | Добавь "НЕ используй классы" в промпт |
| Промпт не помещается | Слишком длинный | Сократи HTML или разбей на части |

---

## Когда НЕ нужен Playwright

Если на вопросы check-list ответ "нет" на все пункты про JavaScript, логин, Cloudflare — используй `requests + BeautifulSoup`. Это быстрее, проще и надёжнее.

В этом случае:
- `browser.py` не используется
- В `scraper.py` вместо Playwright пиши обычные `requests.get()`
- В `main.py` замени `sync_playwright` блок на простой вызов `fetch_page_data()` без context

**ВАЖНО:** Текущий `main.py` привязан к Playwright. Для requests-проектов тебе придётся либо:
1. Попросить ИИ переписать main.py (нарушает правило "не менять ядро")
2. Или в scraper.py игнорировать аргумент `context` и делать свои requests

Рекомендация: для requests-проектов передавай `context=None` и обрабатывай это в scraper.py.

---

## Чек-лист перед сдачей

- [ ] Скрипт запускается без ошибок: `python -m app.main`
- [ ] CSV/JSON создаются в `output/`
- [ ] Данные корректны (проверь 5-10 записей вручную)
- [ ] Нет хардкода путей (всё через config.py)
- [ ] requirements.txt актуален
- [ ] README.md содержит инструкцию запуска
- [ ] Docker работает (если просили): `docker compose up --build`
- [ ] Удалены лишние файлы (AI_INPUT, AI_OUTPUT, project_state.json)
