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
| `scraper.py` | **Да** — под каждый заказ |
| `parser.py` | **Да** — под каждый заказ |

Подробный workflow: `workflows/new_project.md`
