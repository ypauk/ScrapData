# test2

## Быстрый старт

```bash
# 1. Заполни AI_INPUT/ (description.txt, page.html, network.har...)
python ../ai_workflow.py analyze test2

# 2. Сохрани ответ ИИ в AI_OUTPUT/analysis.md
python ../ai_workflow.py project test2

# 3. Сохрани ответ в AI_OUTPUT/project_plan.md
python ../ai_workflow.py module scraper test2
python ../ai_workflow.py module parser test2

# 4. Запуск
cd test2
python -m app.main
```

## Структура

- `AI_INPUT/` — данные от клиента
- `AI_OUTPUT/` — промпты и ответы ИИ
- `app/` — код парсера
- `output/` — результаты CSV/JSON
