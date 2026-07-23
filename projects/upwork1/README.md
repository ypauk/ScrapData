# upwork1

## Быстрый старт

```bash
# 1. Заполни AI_INPUT/ (description.txt, page.html, network.har...)
python ../ai_workflow.py analyze upwork1

# 2. Сохрани ответ ИИ в AI_OUTPUT/analysis.md
python ../ai_workflow.py project upwork1

# 3. Сохрани ответ в AI_OUTPUT/project_plan.md
python ../ai_workflow.py module scraper upwork1
python ../ai_workflow.py module parser upwork1

# 4. Запуск
cd upwork1
python -m app.main
```

## Структура

- `AI_INPUT/` — данные от клиента
- `AI_OUTPUT/` — промпты и ответы ИИ
- `app/` — код парсера
- `output/` — результаты CSV/JSON
