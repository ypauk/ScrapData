# Workflow: новый проект Upwork

## Этап 0. Создание проекта

```bash
python ai_workflow.py new amazon_scraper
```

Создаётся папка `amazon_scraper/` с копией шаблона `starter-project/`.

---

## Этап 1. Сбор данных

Заполни `amazon_scraper/AI_INPUT/`:

| Файл | Что положить |
|------|-------------|
| `description.txt` | ТЗ клиента, URL, поля |
| `page.html` | Сохранённая страница (Ctrl+S) |
| `network.har` | Экспорт из DevTools → Network |
| `cookies.json` | Если нужна авторизация |
| `screenshots/` | Скриншоты (опционально) |

---

## Этап 2. Анализ

```bash
python ai_workflow.py analyze amazon_scraper
```

→ `AI_OUTPUT/final_prompt.md` → отправь в ChatGPT  
→ сохрани ответ в `AI_OUTPUT/analysis.md`

---

## Этап 3. План проекта

```bash
python ai_workflow.py project amazon_scraper
```

→ `AI_OUTPUT/final_prompt.md` → отправь в ChatGPT  
→ сохрани ответ в `AI_OUTPUT/project_plan.md`

**project_plan.md** — это мини-ТЗ: какие функции в scraper.py и parser.py, формат данных, порядок работы. Не код.

---

## Этап 4. Генерация кода

```bash
python ai_workflow.py module scraper amazon_scraper
python ai_workflow.py module parser amazon_scraper
```

→ каждый раз `AI_OUTPUT/final_prompt.md` → ChatGPT → код в `app/`

---

## Этап 5. Запуск

```bash
cd amazon_scraper
pip install -r requirements.txt
playwright install chromium
python -m app.main
```

Результат: `output/output_results.csv` и `.json`

---

## Этап 6. Отладка

При ошибке сохрани traceback:

```
amazon_scraper/AI_OUTPUT/traceback.txt
```

```bash
python ai_workflow.py debug amazon_scraper
```

---

## Этап 7. Docker

```bash
python ai_workflow.py docker amazon_scraper
```

Сохрани сгенерированные `Dockerfile` и `docker-compose.yml` в корень проекта.

---

## Этап 8. Сдача клиенту

- `app/` — код
- `output/` — пример результата
- `README.md` — инструкция запуска
- `Dockerfile` — если просили
