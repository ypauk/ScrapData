# test-pagination

## Быстрый старт

```bash
# 1. Заполни AI_INPUT/ (description.txt, page.html, network.har...)
python ../ai_workflow.py analyze test-pagination

# 2. Сохрани ответ ИИ в AI_OUTPUT/analysis.md
python ../ai_workflow.py project test-pagination

# 3. Сохрани ответ в AI_OUTPUT/project_plan.md
python ../ai_workflow.py module scraper test-pagination
python ../ai_workflow.py module parser test-pagination

# 4. Запуск
cd test-pagination
python -m app.main
```

## Структура

- `AI_INPUT/` — данные от клиента
- `AI_OUTPUT/` — промпты и ответы ИИ
- `app/` — код парсера
- `output/` — результаты CSV/JSON
