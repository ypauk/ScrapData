# РОЛЬ

Ты — DevOps-инженер. Создай Docker-конфигурацию для Python scraping-проекта **{{PROJECT_NAME}}**.

Скрапер уже работает локально. Нужен Docker для сдачи клиенту.

---

# ПРАВИЛА

{{AI_RULES}}

---

# АНАЛИЗ ПРОЕКТА

{{ANALYSIS}}

---

# REQUIREMENTS

```
{{REQUIREMENTS}}
```

---

# КОД ПРОЕКТА

{{PROJECT_CODE}}

---

# ЗАДАЧА

Сгенерируй три файла:

## 1. Dockerfile

- Python 3.11 slim
- Установка зависимостей из requirements.txt
- Если используется Playwright — установка браузера
- `IS_DOCKER=1` и `HEADLESS=1` в ENV
- Точка входа: `python -m app.main`
- Результаты в `/app/output` (volume)

## 2. docker-compose.yml

- Сервис `scraper`
- Volume для `output/`
- Переменные окружения из `.env`
- `restart: "no"` (одноразовый запуск)

## 3. .env.example

- `HEADLESS=1`
- `IS_DOCKER=1`
- `SCRAPER_TIMEOUT=30`
- `SCRAPER_RETRY=3`
- `PROXY_URL=` (пустой)

---

# ФОРМАТ ОТВЕТА

Для каждого файла — полное содержимое:

### Dockerfile
```dockerfile
...
```

### docker-compose.yml
```yaml
...
```

### .env.example
```
...
```

### Как запустить
```bash
docker compose up --build
```

**ЗАПРЕЩЕНО** менять код в `app/`. Только Docker-файлы.
