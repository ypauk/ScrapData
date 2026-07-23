# Starter Project — шаблон для Upwork scraping

Это **шаблон**, не рабочий проект. Для нового заказа:

```bash
python ai_workflow.py new my_project_name
```

## Команды workflow

| Команда | Что делает |
|---------|-----------|
| `new <name>` | Создать новый проект из шаблона |
| `analyze [name]` | Промпт для анализа сайта |
| `project [name]` | Промпт для плана (нужен analysis.md) |
| `module scraper [name]` | Промпт для генерации scraper.py |
| `module parser [name]` | Промпт для генерации parser.py |
| `debug [name]` | Промпт для отладки ошибки |
| `docker [name]` | Промпт для Dockerfile |

Все команды запускаются из корня `UPWORK-ALL/`:

```bash
python ai_workflow.py analyze my_project_name
```

Или из папки проекта (имя не нужно):

```bash
cd my_project_name
python ../ai_workflow.py analyze
```

## Структура app/

| Файл | Менять? |
|------|---------|
| `main.py` | Нет — оркестратор |
| `browser.py` | Нет — Playwright |
| `config.py` | Нет — пути и настройки |
| `exporter.py` | Нет — CSV/JSON |
| `utils.py` | Нет — логи, задержки, цены |
| `html_parser.py` | Нет — универсальный слой BeautifulSoup |
| `scraper.py` | **Да** — под каждый заказ (сейчас: демо-пример OLX) |
| `parser.py` | **Да** — под каждый заказ (сейчас: демо-пример OLX) |

⚠️ **Важно про `scraper.py`/`parser.py`:** прямо сейчас в них лежит не
пустая заготовка, а **рабочий демо-пример парсинга OLX** (объявления авто) —
он демонстрирует полный цикл workflow на реальном сайте. Для нового заказа
эти два файла нужно заменить:

```bash
python ../ai_workflow.py module scraper <project_name>
python ../ai_workflow.py module parser <project_name>
```

Это сгенерирует промпты под конкретный сайт клиента; ответы ИИ сохраняются
в `AI_OUTPUT/03_scraper_answer.py` / `AI_OUTPUT/04_parser_answer.py` и
переносятся в `app/scraper.py` / `app/parser.py` соответственно.

Подробный workflow: `workflows/new_project.md`


