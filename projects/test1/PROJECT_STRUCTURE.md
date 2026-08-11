# Структура проекта: ScrapData

```text
ScrapData/
├── 📁 projects/            ← Активные проекты клиентов
├── 📁 archive/             ← Завершённые проекты
├── 📁 scraping-templates/
│   ├── 📁 prompts/         ← Шаблоны промптов (01-08)
│   ├── 📁 knowledge/       ← Справка по технологиям
│   ├── 📁 templates/       ← Шаблоны Docker, проекта
│   ├── 📁 examples/        ← Примеры готовых проектов
│   └── 📄 AI_rules.md      ← Правила для ИИ
├── 📁 starter-project/     ← Шаблон нового проекта
│   ├── 📁 AI_INPUT/        ← Данные от клиента
│   ├── 📁 AI_OUTPUT/       ← Промпты и ответы ИИ
│   ├── 📁 app/
│   │   ├── 📄 main.py      ← Оркестратор (НЕ менять)
│   │   ├── 📄 browser.py   ← Playwright (НЕ менять)
│   │   ├── 📄 config.py    ← Конфиг из .env (НЕ менять)
│   │   ├── 📄 exporter.py  ← CSV/JSON экспорт (НЕ менять)
│   │   ├── 📄 utils.py     ← Утилиты (НЕ менять)
│   │   ├── 📄 scraper.py   ← ИЗМЕНЯЕМЫЙ (ИИ генерирует)
│   │   └── 📄 parser.py    ← ИЗМЕНЯЕМЫЙ (ИИ генерирует)
│   ├── 📁 output/
│   ├── 📄 .env
│   ├── 📄 requirements.txt
│   └── 📄 Dockerfile
├── 📄 ai_workflow.py        ← CLI-оркестратор (все команды)
├── 📄 prompt_splitter.py    ← Авто-отправка в ChatGPT
├── 📄 clear_chat.py         ← Удаление активного чата ChatGPT (для тестов)
├── 📄 AI_CONTEXT.md         ← Быстрый вход для ИИ
├── 📄 WORKFLOW_INSTRUCTION.md ← Полная инструкция
└── 📄 CLAUDE.md             ← Инструкции для Claude Code
```

## Команды ai_workflow.py

```bash
# Создание / этапы
python ai_workflow.py new <name>         # Создать проект
python ai_workflow.py analyze <name>     # Промпт: анализ сайта
python ai_workflow.py project <name>     # Промпт: архитектура
python ai_workflow.py scraper <name>     # Промпт: код scraper.py
python ai_workflow.py parser <name>      # Промпт: код parser.py
python ai_workflow.py debug <name>       # Промпт: исправление ошибок
python ai_workflow.py docker <name>      # Промпт: Dockerfile

# Тестирование
python ai_workflow.py clean <name>       # Очистить AI_OUTPUT + scraper.py + parser.py + output/
python clear_chat.py --new               # Удалить активный чат в ChatGPT, открыть новый
python ai_workflow.py pipeline <name> --auto  # Все этапы подряд автоматически

# Автоотправка (для любого этапа)
python ai_workflow.py analyze <name> --auto   # Отправить промпт в ChatGPT

# Обслуживание
python ai_workflow.py archive <name>     # Переместить в archive/
python ai_workflow.py review <name>      # Ревью платформы
python ai_workflow.py improve <name>     # Улучшения платформы
```
