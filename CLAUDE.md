# CLAUDE.md — Инструкции для ИИ-ассистента

## Что это за проект

Универсальный конвейер для Upwork scraping-заказов. Подробности — в `AI_CONTEXT.md`.

## Лог консоли

При каждом запуске `ai_workflow.py` вывод автоматически сохраняется в файл `projects/<name>/log`.
Путь выводится первой строкой в консоли: `[LOG] C:\...\projects\<name>\log`

При дебаге — **сначала читай этот файл**, там полный stdout + stderr запуска.

## При получении ошибки (traceback)

Когда пользователь вставляет traceback или ошибку:

1. Определи из traceback путь к проекту (например `projects/test1/`)
2. Прочитай файлы в таком порядке:
   - Файл, указанный в последней строке traceback (где упала ошибка)
   - Файл, из которого идёт импорт (если ImportError)
   - `<project>/app/config.py` — если ошибка связана с конфигом/переменными
   - `<project>/.env` — если ошибка связана с отсутствующими значениями
   - `<project>/app/main.py` — если неясен порядок вызовов
3. Исправь проблему. Не спрашивай "что делать" — чини.

## Структура клиентского проекта (projects/<name>/)

```
app/
  main.py        — точка входа, оркестратор (НЕ менять без причины)
  config.py      — все настройки из .env (НЕ менять без причины)
  scraper.py     — ИЗМЕНЯЕМЫЙ: сбор данных (сеть/навигация)
  parser.py      — ИЗМЕНЯЕМЫЙ: парсинг HTML → структурированные данные
  browser.py     — запуск Playwright (НЕ менять)
  exporter.py    — экспорт CSV/JSON (НЕ менять)
  utils.py       — утилиты (НЕ менять)
.env             — настройки (BASE_URL, таймауты, прокси)
AI_INPUT/        — входные данные от клиента (описание, примеры, cookies)
AI_OUTPUT/       — промпты и ответы ИИ
output/          — результаты парсинга (CSV, JSON)
```

## Контракты модулей

```python
# scraper.py — принимает PlaywrightEngine, возвращает сырой HTML
def scrape_data(engine: PlaywrightEngine) -> List[str]: ...

# parser.py — принимает HTML, возвращает структурированные данные
def parse_html_data(raw_contents: List[str]) -> List[Dict[str, Any]]: ...
def parse_listing(html: str) -> List[Dict[str, Any]]: ...
```

## Команды ai_workflow.py

```
python ai_workflow.py login                      — войти в ChatGPT (нужно при первом запуске или после удаления .browser_profile)
python ai_workflow.py new <name>                 — создать новый проект
python ai_workflow.py pipeline <name> --auto     — полный конвейер с автоотправкой в ChatGPT
python ai_workflow.py clean <name>               — очистить AI_OUTPUT + scraper.py/parser.py/output/
python ai_workflow.py analyze|project|scraper|parser|debug|docker|review|improve <name>
```

Если `pipeline --auto` падает с "rate limit" или "modal-no-auth" — сначала запусти `login`.
После удаления `.browser_profile` сессия сбрасывается — нужен повторный `login`.

## Ключевые правила

- `BASE_URL` задаётся в `.env` проекта
- `scraper.py` использует PlaywrightEngine (браузер), НЕ requests
- `parser.py` НЕ делает HTTP-запросы, только разбирает HTML
- При дебаге: сначала читай файл с ошибкой, потом связанные
- Не ломай файлы помеченные "НЕ менять" без явной просьбы пользователя
