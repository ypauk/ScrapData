# AI_CONTEXT — Быстрый вход в проект ScrapData

> Прочитай ТОЛЬКО этот файл перед работой. Не сканируй всю структуру.

## Что это

Конвейер для Upwork scraping-заказов. Генерирует промпты для ИИ поэтапно, получает код, тестирует, сдаёт клиенту.

## Архитектура (1 схема)

```
ai_workflow.py (CLI)
    │
    ├── new        → копирует starter-project/ в projects/<name>/
    ├── analyze    → промпт 01 (анализ сайта, выбор технологии)
    ├── project    → промпт 02 (архитектура scraper.py + parser.py)
    ├── scraper    → промпт 03 (код scraper.py)
    ├── parser     → промпт 04 (код parser.py)
    ├── debug      → промпт 05 (исправление ошибок)
    ├── docker     → промпт 06 (Dockerfile + compose)
    ├── clean      → очищает AI_OUTPUT + app/scraper.py + app/parser.py (для тестов)
    ├── pipeline   → полный конвейер analyze→project→scraper→parser (с --auto или вручную)
    └── archive    → перемещает в archive/
```

## Поток данных внутри проекта клиента

```
projects/<name>/AI_INPUT/     ← человек кладёт сюда данные (html, har, описание)
        │
        ▼
ai_workflow.py <команда>      ← генерирует промпт из шаблона + AI_INPUT
        │
        ▼
projects/<name>/AI_OUTPUT/    ← промпт сохраняется сюда (NN_*_prompt.md)
        │
        ▼
[ИИ-чат]                     ← человек копирует промпт, получает ответ
        │
        ▼
projects/<name>/AI_OUTPUT/    ← ответ сохраняется сюда (NN_*_answer.*)
        │
        ▼
projects/<name>/app/          ← код из ответа копируется в рабочие файлы
```

## Зависимости между этапами (порядок обязателен)

```
analyze (нужен: AI_INPUT/*)
    ↓
project (нужен: 01_analysis_answer.md)
    ↓
scraper (нужен: 01_analysis_answer.md + 02_project_answer.md)
    ↓
parser  (нужен: 03_scraper_answer.py)
    ↓
debug   (нужен: app/*.py + traceback)
    ↓
docker  (нужен: app/*.py + requirements.txt)
```

## Ключевые файлы и их роль

### Корень (ScrapData/)

| Файл | Роль | Когда читать |
|------|------|-------------|
| `ai_workflow.py` | CLI-оркестратор, генерирует промпты | При доработке workflow |
| `clear_chat.py` | Удаление активного чата в ChatGPT | При тестировании |
| `export_for_ai.py` | Дамп всего проекта в текст | НЕ НУЖЕН для обычной работы |
| `AI_CONTEXT.md` | **Этот файл** | Всегда первым |
| `WORKFLOW_INSTRUCTION.md` | Детальная инструкция для человека | Если нужны подробности |

### Шаблоны (scraping-templates/)

| Файл | Роль |
|------|------|
| `prompts/01_analysis_prompt.md` | Шаблон промпта анализа |
| `prompts/02_project_prompt.md` | Шаблон промпта проектирования |
| `prompts/03_scraper_prompt.md` | Шаблон промпта для кода scraper |
| `prompts/04_parser_prompt.md` | Шаблон промпта для кода parser |
| `prompts/05_debug_prompt.md` | Шаблон промпта отладки |
| `prompts/06_docker_prompt.md` | Шаблон промпта Docker |
| `AI_rules.md` | 10 правил для ИИ (вставляется в промпты) |

### Шаблон проекта (starter-project/app/)

| Файл | Изменяемый? | Контракт |
|------|------------|----------|
| `main.py` | НЕТ | Оркестратор: browser → scraper → parser → exporter |
| `browser.py` | НЕТ | `get_browser_context(playwright, cookies_path) → BrowserContext` |
| `config.py` | НЕТ | Пути, таймауты, env-переменные |
| `exporter.py` | НЕТ | `save_to_csv(data, filename)`, `save_to_json(data, filename)` |
| `utils.py` | НЕТ | `random_delay()`, `clean_price()`, `log_message()` |
| `scraper.py` | **ДА** | `fetch_page_data(context: BrowserContext) → List[str]` |
| `parser.py` | **ДА** | `parse_html_data(raw_contents: List[str]) → List[Dict[str, Any]]` |

## Контракты (самое важное для генерации кода)

```python
# === scraper.py ===
# Вход: BrowserContext (Playwright) или None (для requests-проектов)
# Выход: List[str] — список сырого HTML или JSON-строк
# Ограничения: только сеть/навигация, НЕ парсит DOM

def fetch_page_data(context: BrowserContext) -> List[str]: ...

# === parser.py ===
# Вход: List[str] — сырой контент от scraper
# Выход: List[Dict[str, Any]] — структурированные данные
# Ограничения: только парсинг, НЕ делает HTTP-запросы

def parse_html_data(raw_contents: List[str]) -> List[Dict[str, Any]]: ...
def parse_single_item(element) -> Dict[str, Any]: ...
```

## Переменные в шаблонах промптов

ai_workflow.py подставляет эти плейсхолдеры:

| Переменная | Откуда берётся |
|-----------|---------------|
| `{{CLIENT_DESCRIPTION}}` | AI_INPUT/* (все файлы склеены) |
| `{{APPROVED_STRATEGY}}` | AI_OUTPUT/01_analysis_answer.md |
| `{{AI_INPUT_ANALYSIS}}` | AI_INPUT/* (с упрощённым HTML) |
| `{{ANALYSIS}}` | AI_OUTPUT/01_analysis_answer.md |
| `{{PROJECT_PLAN}}` | AI_OUTPUT/02_project_answer.md |
| `{{AI_RULES}}` | scraping-templates/AI_rules.md |
| `{{AI_INPUT}}` | AI_INPUT/* (без HTML) |
| `{{CORE_FILES}}` | main.py + browser.py + config.py + exporter.py + utils.py |
| `{{MODULE_FILE}}` | "app/scraper.py" или "app/parser.py" |
| `{{MODULE_NAME}}` | "scraper" или "parser" |
| `{{MODULE_TEMPLATE}}` | Текущий код модуля |
| `{{SCRAPER_CODE}}` | AI_OUTPUT/03_scraper_answer.py |
| `{{CURRENT_CODE}}` | Все .py из app/ |
| `{{ERROR_LOG}}` | AI_OUTPUT/traceback.txt |
| `{{REQUIREMENTS}}` | requirements.txt |
| `{{PROJECT_NAME}}` | Имя папки проекта |
| `{{PROJECT_CODE}}` | Все .py из app/ |

## Что НЕ читать (экономия токенов)

- `export_for_ai.py` — дублирует ai_workflow.py, legacy
- `my_project_structure.txt` — генерируемый дамп, не источник правды
- `scraping-templates/prompts/01_analyze_project.md` — старая версия (дубль)
- `scraping-templates/prompts/02_generate_project.md` — старая версия
- `scraping-templates/prompts/03_generate_module.md` — старая версия
- `scraping-templates/prompts/04_debug.md` — старая версия
- `scraping-templates/prompts/05_refactor.md` — не используется
- `scraping-templates/prompts/06_review.md` — не используется
- `scraping-templates/prompts/07_optimize.md` — не используется
- `scraping-templates/prompts/08_create_tests.md` — не используется
- `scraping-templates/prompts/09_create_docker.md` — старая версия
- `scraping-templates/knowledge/*` — пустые заготовки
- `scraping-templates/snippets/*` — пустая папка
- `starter-project/AI_OUTPUT/*` — тестовые артефакты

## Дебаг: как вставить ошибку и получить исправление

**Для Claude Code (CLI/Desktop):** просто вставь traceback — `CLAUDE.md` в корне проекта автоматически подскажет ИИ что читать и где искать.

**Для внешнего ИИ-чата (ChatGPT, Claude.ai и т.д.):** используй `ai_workflow.py debug <project>` — он соберёт промпт с кодом + ошибкой. Перед этим положи traceback в `AI_OUTPUT/traceback.txt`.

**Порядок диагностики (для любого ИИ):**
1. Последняя строка traceback → файл с ошибкой
2. ImportError → проверить что экспортирует модуль-источник
3. AttributeError/TypeError → несовпадение контрактов между модулями
4. Значения из .env → проверить config.py + .env

## Быстрое тестирование

```bash
# Очистить все результаты (AI_OUTPUT + scraper.py + parser.py + output/) для чистого теста
python ai_workflow.py clean test1

# Удалить активный чат в ChatGPT (тот же профиль что и --auto)
python clear_chat.py          # удалить текущий чат
python clear_chat.py --new    # удалить и открыть новый

# Прогнать весь конвейер автоматически (analyze → project → scraper → parser)
python ai_workflow.py pipeline test1 --auto

# Прогнать вручную (ждёт Enter между этапами)
python ai_workflow.py pipeline test1

# Полный цикл тестирования с нуля:
python ai_workflow.py clean test1 && python clear_chat.py --new && python ai_workflow.py pipeline test1 --auto
```

## Известные ограничения

1. `main.py` жёстко импортирует Playwright — для requests-проектов scraper.py должен игнорировать `context` или main.py нужно менять
2. Промпты этапов 3-4 содержат 15-30k токенов — не помещаются в бесплатные ИИ
3. Нет автоматической интеграции с API ИИ — всё копируется вручную
4. `memory/` пустая — база знаний по сайтам не ведётся

## Частые задачи → что читать

| Задача | Читать |
|--------|--------|
| Очистить проект для теста | `python ai_workflow.py clean <name>` |
| Прогнать весь pipeline | `python ai_workflow.py pipeline <name> --auto` |
| Добавить новый этап workflow | `ai_workflow.py` (STAGES dict, cmd_* функции) |
| Изменить промпт | `scraping-templates/prompts/0N_*.md` |
| Изменить структуру нового проекта | `starter-project/` + `ai_workflow.py:cmd_new()` |
| Понять как генерируется промпт | `ai_workflow.py:cmd_<stage>()` + `fill_template()` |
| Добавить поддержку requests | `starter-project/app/main.py` + `scraper.py` |
| Добавить новый exporter (Excel) | `starter-project/app/exporter.py` |
