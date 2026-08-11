# Как отправлять большие промпты в ChatGPT

## Проблема

Промпты на этапах scraper/parser/debug = 500-11000 строк (15-30k+ токенов).
Бесплатные ИИ:
- ChatGPT free: режет длинный ввод или теряет начало
- Gemini free: принимает большой ввод, но хуже следует инструкциям в начале
- DeepSeek: принимает, но качество падает на длинных промптах

## Решение: автоматическая отправка

Два способа использования:

1. **Через ai_workflow.py** (рекомендуемый) — генерация промпта + авто-отправка + сохранение ответа одной командой
2. **Через prompt_splitter.py** — отдельная разбивка/отправка любого файла

---

## Способ 1: ai_workflow.py --auto (рекомендуемый)

Генерирует промпт, автоматически разбивает если нужно, отправляет в ChatGPT, сохраняет ответ в правильный файл.

```bash
python ai_workflow.py debug my_project --auto
python ai_workflow.py scraper my_project --auto
python ai_workflow.py parser my_project --auto
python ai_workflow.py analyze my_project --auto
python ai_workflow.py project my_project --auto
python ai_workflow.py docker my_project --auto
```

### Маппинг промпт → ответ (автоматический)

| Команда | Prompt | Answer |
|---------|--------|--------|
| `analyze` | `01_analysis_prompt.md` | `01_analysis_answer.md` |
| `project` | `02_project_prompt.md` | `02_project_answer.md` |
| `scraper` | `03_scraper_prompt.md` | `03_scraper_answer.py` |
| `parser` | `04_parser_prompt.md` | `04_parser_answer.py` |
| `debug` | `05_debug_prompt.md` | `05_debug_answer.md` |
| `docker` | `06_docker_prompt.md` | `06_Dockerfile` |

### Указание количества строк на часть

```bash
# По умолчанию: 800 строк/часть
python ai_workflow.py debug my_project --auto

# Кастомный лимит:
python ai_workflow.py debug my_project --auto --max-lines 600
python ai_workflow.py scraper my_project --auto --max-lines 400
```

Если промпт меньше `--max-lines` — отправляется целиком без разбивки.

### Все опции

```bash
python ai_workflow.py debug my_project --auto                    # отправка
python ai_workflow.py debug my_project --auto --dry-run          # только план
python ai_workflow.py debug my_project --auto --max-lines 600    # размер частей
python ai_workflow.py debug my_project --auto --force            # без проверки ack
python ai_workflow.py debug my_project --auto --restart          # заново
python ai_workflow.py debug my_project --auto --delay 3          # пауза между частями
python ai_workflow.py debug my_project --auto --timeout 600      # таймаут ответа
python ai_workflow.py debug my_project --auto --retries 5        # повторы при ошибке
```

---

## Способ 2: prompt_splitter.py

Для отправки произвольного файла (не обязательно из ai_workflow).

```bash
# Автоотправка последнего промпта:
python prompt_splitter.py --auto

# Автоотправка конкретного файла:
python prompt_splitter.py --auto projects/amazon/AI_OUTPUT/03_scraper_prompt.md

# Свой лимит строк:
python prompt_splitter.py --auto --max-lines 600

# Только план:
python prompt_splitter.py --auto --dry-run

# Ручной режим (как раньше — копирование в clipboard):
python prompt_splitter.py
python prompt_splitter.py --max-lines 150

# Сохранить в файлы:
python prompt_splitter.py --save
```

---

## Первый запуск (настройка браузера)

### Установка Playwright

```bash
pip install playwright
playwright install chromium
```

### Первый запуск --auto

1. Запускаешь `--auto`
2. Откроется Chromium с пустым профилем
3. Вручную логинишься в ChatGPT (один раз)
4. Открываешь нужный чат или создаёшь новый
5. Нажимаешь Enter в терминале
6. Скрипт автоматически отправит все части и сохранит ответ

**Следующие запуски** — сессия сохранена, логин не нужен.

---

## Как это работает

### Полный цикл (--auto):

```
python ai_workflow.py debug my_project --auto
         │
         ▼
    генерация промпта (05_debug_prompt.md)
         │
         ▼
    промпт > max-lines строк?
         │
    ДА → разбивка на части с wrapper'ами
         │
         ▼
    запуск Chromium (persistent profile)
         │
         ▼
    открытие ChatGPT
         │
         ▼
    ожидание Enter от пользователя
         │
         ▼
    [1/N] отправка → ожидание ответа → проверка "Часть X принята"
    [2/N] отправка → ожидание ответа → проверка
    ...
    [N/N] отправка финальной части → ожидание полного ответа
         │
         ▼
    сохранение ответа → 05_debug_answer.md
         │
         ▼
    DONE
```

### Вывод в терминале:

```
============================================================
  ChatGPT Auto Sender
============================================================

  File: 05_debug_prompt.md
  Lines: 11239
  Parts: 16
  Answer: 05_debug_answer.md

  Browser: Chromium
  Profile: .browser_profile

  [1/16] Sending...
  [1/16] Waiting for response...
  [1/16] Acknowledgement ✓

  [2/16] Sending...
  [2/16] Waiting for response...
  [2/16] Acknowledgement ✓

  ...

  [16/16] Sending final task...
  [16/16] Response completed ✓

  ✓ Ответ сохранён: 05_debug_answer.md

============================================================
  DONE
============================================================
```

---

## Что происходит в чате ChatGPT

### Часть 1 (скрипт отправляет автоматически):
```
ВАЖНО: Я буду отправлять тебе контекст проекта по частям.
Это часть 1 из 16.
Запомни всю информацию ниже. НЕ отвечай и НЕ генерируй код пока не получишь последнюю часть с задачей.
Ответь ТОЛЬКО: "Часть 1 принята. Жду следующую."

---

# РОЛЬ
Ты — Senior Python Web Scraping Engineer...
```

### ChatGPT отвечает:
```
Часть 1 принята. Жду следующую.
```

### Части 2-15 аналогично...

### Последняя часть (16/16):
```
Это последняя часть (16 из 16).
Весь контекст получен. ТЕПЕРЬ выполни задачу.

---

# ЗАДАЧА
Исправь ошибку в коде...
```

### ChatGPT генерирует полный ответ → скрипт сохраняет в файл.

---

## Resume (восстановление после сбоя)

Если процесс прервался (закрылся терминал, потерялся интернет):

```
Обнаружен предыдущий прогресс:
5/16 частей завершено.

Продолжить с части 6? [Y/n]
```

Состояние хранится в `.prompt_splitter_state.json`.

Если файл промпта изменился — начинает заново:
```
WARNING: Исходный prompt изменился после предыдущего запуска.
Начинаем заново.
```

Принудительно начать заново:
```bash
python ai_workflow.py debug my_project --auto --restart
```

---

## --force (игнорировать проверку acknowledgement)

Если ChatGPT отвечает нестандартно на промежуточные части:

```bash
python ai_workflow.py debug my_project --auto --force
```

Без `--force` скрипт спрашивает подтверждение при неожиданном ответе.

---

## Рекомендуемые лимиты строк

| Ситуация | --max-lines | Почему |
|----------|-------------|--------|
| По умолчанию | 800 | Баланс: мало частей, но ChatGPT не теряет контекст |
| Большой debug промпт | 600 | Debug промпты 10k+ строк, лучше больше мелких частей |
| Быстрый analyze | 1000 | Analyze обычно короткий, можно крупнее |
| ChatGPT free | 400 | У free меньше контекст |

---

## Ручной режим (без --auto)

Работает как раньше — скрипт копирует части в clipboard, ты вставляешь вручную:

```bash
python prompt_splitter.py
python prompt_splitter.py --max-lines 150
python prompt_splitter.py --save
```

```
┌──────────────────────────────────────────────────────────┐
│  [Часть 1/5] Контекст (198 строк, 4521 символов)        │
│  → Нажми Enter чтобы скопировать...                      │
│  ✓ Скопировано в буфер. Вставляй в чат (Ctrl+V).        │
│                                                          │
│  [Часть 2/5] Контекст (195 строк, 5102 символов)        │
│  → Нажми Enter чтобы скопировать...                      │
└──────────────────────────────────────────────────────────┘
```

---

## Интеграция с workflow

### Полный процесс (автоматический):

```bash
# Всё одной командой:
python ai_workflow.py scraper amazon_scraper --auto
# → генерирует промпт
# → разбивает
# → отправляет в ChatGPT
# → сохраняет ответ в 03_scraper_answer.py
```

### Полный процесс (ручной):

```bash
# 1. Генерируешь промпт
python ai_workflow.py scraper amazon_scraper

# 2. Разбиваешь и отправляешь вручную
python prompt_splitter.py

# 3. Следуешь инструкциям (Enter → Ctrl+V → Enter → ...)

# 4. Копируешь ответ из ChatGPT

# 5. Сохраняешь вручную
# → projects/amazon_scraper/AI_OUTPUT/03_scraper_answer.py
```

---

## Ошибки и решения

### "Playwright не установлен"
```bash
pip install playwright
playwright install chromium
```

### "Composer не найден"
ChatGPT обновил DOM. Скрипт использует несколько fallback-селекторов, но если все сломались — нужно обновить селекторы в `prompt_splitter.py` (функция `find_chat_input`).

### "Таймаут ответа"
ChatGPT долго генерирует. Увеличь таймаут:
```bash
python ai_workflow.py debug my_project --auto --timeout 600
```

### "Неожиданный ответ после части N"
ChatGPT ответил не "Часть N принята". Варианты:
- Нажать `y` для продолжения
- Использовать `--force` чтобы игнорировать проверки
- Проверить что чат пустой (не содержит предыдущую беседу)

---

## Файлы и папки

| Путь | Роль |
|------|------|
| `prompt_splitter.py` | Скрипт разбивки и авто-отправки |
| `.browser_profile/` | Chromium профиль (сессия ChatGPT) |
| `.prompt_splitter_state.json` | Состояние resume |
| `.gitignore` | Исключает profile и state из git |
