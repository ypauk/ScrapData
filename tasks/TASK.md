ЗАДАЧА: полностью автоматизировать передачу AI prompt через GitHub Raw URL вместо дробления на части

Работаем с существующим Python-проектом и существующим workflow.

Текущая команда запуска:

    python ai_workflow.py pipeline test1 --auto

Цель:
полностью убрать из auto-workflow функционал дробления большого prompt на части и заменить его на автоматическую публикацию итогового prompt-файла в GitHub с последующей передачей в AI-чаты только одной стабильной Raw-ссылки.

ВАЖНО:
Не переписывай проект с нуля.
Сначала изучи существующую архитектуру, найди текущий функционал:
- генерации AI prompt;
- дробления prompt на части;
- формирования chunks;
- отправки chunks в чат;
- генерации ссылок/результатов;
- pipeline test1 --auto.

После анализа внеси минимальные, но архитектурно правильные изменения.

==================================================
1. ТЕКУЩАЯ ПРОБЛЕМА
==================================================

Сейчас большой prompt разбивается на части примерно по 400 строк и затем передаётся в AI-чат несколькими сообщениями.

Это ненадёжно и занимает много времени.

Например, текущий prompt:

    projects/test1/AI_OUTPUT/03_scraper_prompt.md

может содержать тысячи строк.

Сейчас вместо передачи всего файла одним сообщением используется дробление на множество частей.

ЭТОТ МЕХАНИЗМ БОЛЬШЕ НЕ НУЖЕН.

Нужно полностью перейти на следующую схему:

    генерация prompt
            ↓
    сохранение prompt в .md
            ↓
    git add
            ↓
    git commit
            ↓
    git push
            ↓
    формирование стабильной GitHub Raw URL
            ↓
    передача ТОЛЬКО этой URL в AI chat

==================================================
2. ПРИМЕР GITHUB
==================================================

GitHub account:

    ypauk

Repository:

    ScrapData

Branch:

    main

Текущий пример файла:

    projects/test1/AI_OUTPUT/03_scraper_prompt.md

Текущая рабочая Raw URL:

    https://raw.githubusercontent.com/ypauk/ScrapData/refs/heads/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

Предпочтительный канонический формат Raw URL:

    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

Нужно использовать именно такой стабильный URL-шаблон:

    https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}

Где:

    owner = ypauk
    repo = ScrapData
    branch = main
    path = projects/test1/AI_OUTPUT/03_scraper_prompt.md

==================================================
3. НОВОЕ ПОВЕДЕНИЕ WORKFLOW
==================================================

После запуска:

    python ai_workflow.py pipeline test1 --auto

workflow должен автоматически:

1. Выполнить существующий pipeline.
2. Сгенерировать итоговый AI prompt.
3. Сохранить его в:

       projects/test1/AI_OUTPUT/03_scraper_prompt.md

4. НЕ разбивать его на части.
5. НЕ создавать chunks.
6. НЕ создавать файлы вида:
       part_01
       part_02
       chunk_01
       chunk_02
       и т.д.

7. Выполнить Git commit изменённого prompt-файла.
8. Выполнить Git push в GitHub.
9. Сформировать Raw URL.
10. Передать дальше в AI-chat только эту Raw URL.
11. В финальном результате workflow вывести Raw URL.

Пример итогового вывода:

    AI PROMPT PUBLISHED

    File:
    projects/test1/AI_OUTPUT/03_scraper_prompt.md

    GitHub:
    https://github.com/ypauk/ScrapData

    Raw URL:
    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

    Commit:
    <commit SHA>

    Status:
    SUCCESS

==================================================
4. КРИТИЧЕСКИ ВАЖНО: УДАЛИТЬ CHUNKING
==================================================

Найди существующий код, который отвечает за:

- split;
- chunk;
- chunks;
- split_prompt;
- split_into_parts;
- max_lines;
- 400 lines;
- prompt parts;
- prompt_part;
- отправку нескольких частей;
- ожидание между частями;
- сборку частей;
- retry отдельных частей.

Этот функционал больше НЕ должен использоваться в режиме:

    pipeline test1 --auto

Не просто отключи одну функцию.

Проследи весь execution path и убери chunking именно из auto pipeline.

После изменения должен существовать путь:

    prompt file
        ↓
    Git
        ↓
    Raw URL
        ↓
    AI chat

а НЕ:

    prompt
        ↓
    chunk 1
        ↓
    chunk 2
        ↓
    chunk 3
        ↓
    ...
        ↓
    AI chat

==================================================
5. GIT AUTOMATION
==================================================

Git операции должны выполняться автоматически.

После генерации:

    git add <prompt-file>

затем:

    git commit -m "<message>"

затем:

    git push origin main

Но НЕ надо бездумно выполнять git add .

Добавлять нужно только файлы, которые workflow действительно предназначен публиковать.

Минимально ожидаемый файл:

    projects/test1/AI_OUTPUT/03_scraper_prompt.md

Если существующая архитектура предусматривает дополнительные AI_OUTPUT-файлы, сначала проанализируй её и не ломай существующее поведение.

==================================================
6. COMMIT MESSAGE
==================================================

Сделай commit message автоматически.

Например:

    ai: update prompt for test1

или:

    ai_workflow: update test1 prompt

Можно использовать существующий стиль commit message проекта, если он уже есть.

Не требуй от пользователя вводить commit message вручную при запуске --auto.

==================================================
7. ЕСЛИ ИЗМЕНЕНИЙ НЕТ
==================================================

Очень важно.

Если prompt-файл после генерации не изменился относительно последнего commit:

НЕ нужно создавать пустой commit.

В этом случае:

1. определить текущий commit;
2. не выполнять git commit;
3. не выполнять ненужный push;
4. всё равно сформировать стабильную Raw URL;
5. вернуть её как результат.

Например:

    Prompt unchanged.
    No commit required.

    Raw URL:
    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

==================================================
8. GIT ERROR HANDLING
==================================================

Git операции должны иметь нормальную обработку ошибок.

Если:

    git add

не удался → workflow завершается с понятной ошибкой.

Если:

    git commit

не удался → понятная ошибка.

Если:

    git push

не удался → понятная ошибка.

НЕ считать workflow успешным, если push фактически не произошёл.

Особенно важно не вывести:

    SUCCESS

если файл был только локально изменён, но в GitHub не попал.

==================================================
9. ПРОВЕРКА PUSH
==================================================

После push желательно проверить, что commit действительно появился в remote.

Можно использовать:

    git rev-parse HEAD
    git ls-remote origin main

или другой надёжный способ.

Сравнивать SHA локального HEAD и remote main, если это соответствует существующей архитектуре.

Только после подтверждения push считать публикацию успешной.

==================================================
10. RAW URL
==================================================

Создай отдельную функцию, например:

    build_raw_url(...)

Она должна принимать:

    github_owner
    github_repo
    github_branch
    file_path

и возвращать:

    https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}

Например:

    build_raw_url(
        owner="ypauk",
        repo="ScrapData",
        branch="main",
        path="projects/test1/AI_OUTPUT/03_scraper_prompt.md",
    )

должна вернуть:

    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

Не хардкодить весь URL в нескольких местах.

==================================================
11. КОНФИГУРАЦИЯ GITHUB
==================================================

НЕ хардкодить:

    GitHub token
    password
    PAT
    SSH private key

в исходный код.

Также НЕ записывать token в:

    prompt
    log
    commit message
    output
    JSON
    GitHub repository

GitHub credentials должны браться из безопасного источника.

Предпочтительный вариант для локального CLI workflow:

    уже настроенный git credential manager / SSH / gh auth

Если проект использует GitHub API напрямую, использовать environment variable.

Например:

    GITHUB_TOKEN

Но не добавлять реальное значение в .env, если .env отслеживается Git.

Если используется .env:
- убедиться, что он находится в .gitignore;
- не коммитить секрет;
- не печатать значение токена.

==================================================
12. ЧТО НУЖНО НАСТРОИТЬ ПОЛЬЗОВАТЕЛЮ
==================================================

После реализации явно задокументируй, какие данные пользователь должен предоставить.

Минимально:

    GITHUB_OWNER=ypauk
    GITHUB_REPO=ScrapData
    GITHUB_BRANCH=main

Путь должен формироваться автоматически из текущего test id.

Для:

    python ai_workflow.py pipeline test1 --auto

ожидаемый prompt path:

    projects/test1/AI_OUTPUT/03_scraper_prompt.md

Для другого pipeline, например:

    test2

ожидаемый путь:

    projects/test2/AI_OUTPUT/03_scraper_prompt.md

То есть НЕ хардкодить test1.

==================================================
13. AUTHENTICATION
==================================================

Нужно определить, какой способ Git authentication уже используется проектом.

Сначала проверь:

    git remote -v
    git config --get remote.origin.url
    gh auth status

Если GitHub CLI уже авторизован и это подходит существующей архитектуре — использовать его.

Если нужен token для API, использовать GITHUB_TOKEN через environment variable.

НЕ просить пользователя вставлять токен каждый запуск.

НЕ хранить token в Python-файлах.

НЕ хранить token в prompt.

Для GitHub repository write operations необходимы соответствующие права записи в repository contents. Fine-grained PAT должен иметь доступ к нужному repository и permission на запись содержимого. См. официальную документацию GitHub.

==================================================
14. CLI CONFIGURATION
==================================================

Добавь конфигурацию таким образом, чтобы пользователь мог настроить:

    github.owner
    github.repository
    github.branch

Предпочтительный порядок:

1. CLI arguments, если они уже предусмотрены проектом.
2. Environment variables.
3. config file.
4. разумные defaults.

Например:

    GITHUB_OWNER=ypauk
    GITHUB_REPO=ScrapData
    GITHUB_BRANCH=main

Не ломать существующие настройки проекта.

==================================================
15. AUTO MODE
==================================================

Ключевое требование:

    python ai_workflow.py pipeline test1 --auto

должен работать БЕЗ ручного вмешательства.

То есть после запуска пользователь НЕ должен:

- копировать prompt;
- дробить prompt;
- выбирать части;
- вручную выполнять git add;
- вручную выполнять git commit;
- вручную выполнять git push;
- вручную искать Raw URL;
- вручную собирать Raw URL.

Всё должно происходить автоматически.

Пользователь в итоге получает:

    Raw URL

которую можно вставить в ChatGPT / Claude / другой AI.

==================================================
16. ВАЖНО: AI CHAT INPUT
==================================================

Текущий workflow может иметь существующий browser/chat automation.

Нужно найти место, где сейчас формируются/передаются chunks.

В auto mode заменить передачу chunks на передачу одной строки:

    <RAW_URL>

Например:

    Прочитай полный prompt по этой ссылке и выполни задачу:
    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

Если текущий workflow уже имеет шаблон сообщения для AI, сохранить его, изменив только источник prompt.

НЕ вставлять содержимое prompt в браузер.

НЕ вставлять 400 строк.

НЕ вставлять 4000 строк.

В браузер должен передаваться только короткий запрос с Raw URL.

==================================================
17. ПУБЛИКАЦИЯ ДОЛЖНА БЫТЬ ДО AI CHAT
==================================================

Правильный порядок:

    generate prompt
        ↓
    write prompt file
        ↓
    git status
        ↓
    git add
        ↓
    git commit
        ↓
    git push
        ↓
    verify remote
        ↓
    build Raw URL
        ↓
    AI chat automation

НЕЛЬЗЯ запускать AI chat до успешной публикации prompt.

Иначе AI может получить старую версию файла.

==================================================
18. CACHE / СТАРАЯ ВЕРСИЯ
==================================================

Основная Raw URL должна оставаться стабильной:

    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

Не добавлять timestamp к URL по умолчанию.

Но предусмотрите возможность cache-busting, если существующий AI chat иногда получает старую версию.

Например опционально:

    ?v=<commit_sha>

Но по умолчанию использовать стабильный URL без query parameter.

Если добавляется cache-busting, не ломать основную canonical URL.

==================================================
19. LOGGING
==================================================

Добавить понятный лог:

    [AI] Generating prompt...
    [AI] Prompt written: ...
    [Git] Checking changes...
    [Git] Changes detected.
    [Git] Committing...
    [Git] Commit: ...
    [Git] Pushing to origin/main...
    [Git] Push successful.
    [Git] Remote verified.
    [AI] Raw URL:
    https://raw.githubusercontent.com/...

Не выводить секреты.

==================================================
20. IDEMPOTENCY
==================================================

Workflow должен быть безопасным при повторном запуске.

Если пользователь дважды запускает:

    python ai_workflow.py pipeline test1 --auto

не должно появляться два одинаковых commit подряд, если файл не изменился.

Если файл изменился — создать один новый commit.

==================================================
21. НЕ ЛОМАТЬ СУЩЕСТВУЮЩИЙ WORKFLOW
==================================================

До изменений:

- изучи ai_workflow.py;
- найди pipeline;
- найди --auto;
- найди chunking;
- найди AI chat integration;
- найди текущую систему output;
- найди существующую Git integration, если она уже есть;
- найди config/environment handling;
- найди tests.

После этого составь краткий план.

Затем реализуй изменения.

Не удаляй старый chunking код без проверки, используется ли он другими режимами.

Если chunking нужен для старого режима, сохрани его для старого режима.

Но:

    pipeline test1 --auto

должен использовать только новый Raw URL flow.

==================================================
22. ДОКУМЕНТАЦИЯ
==================================================

После реализации обнови README / docs проекта.

Добавь раздел:

    GitHub Raw Prompt Workflow

с объяснением:

    python ai_workflow.py pipeline test1 --auto

делает:

    prompt → Git commit → Git push → Raw URL → AI

Также объясни настройку:

    GITHUB_OWNER
    GITHUB_REPO
    GITHUB_BRANCH

и authentication.

Покажи пример:

    GITHUB_OWNER=ypauk
    GITHUB_REPO=ScrapData
    GITHUB_BRANCH=main

НЕ указывать реальный токен в документации.

==================================================
23. TESTS
==================================================

Добавь/обнови тесты.

Минимально проверить:

1. build_raw_url()

2. правильное преобразование:

    projects/test1/AI_OUTPUT/03_scraper_prompt.md

в:

    https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/test1/AI_OUTPUT/03_scraper_prompt.md

3. отсутствие chunking в auto path.

4. отсутствие commit, если файл не изменился.

5. commit + push при изменении файла.

6. ошибка push должна приводить к failed workflow.

7. test2 должен автоматически получить:

    projects/test2/AI_OUTPUT/03_scraper_prompt.md

а не test1.

8. token не должен попадать в logs.

==================================================
24. ACCEPTANCE CRITERIA
==================================================

Работа считается выполненной только если:

[ ] python ai_workflow.py pipeline test1 --auto запускается одной командой.

[ ] Prompt НЕ разбивается на 400 строк.

[ ] Prompt НЕ передаётся в AI chat содержимым.

[ ] Prompt сохраняется одним .md файлом.

[ ] Git автоматически определяет изменение.

[ ] При изменении выполняется commit.

[ ] Выполняется push в GitHub.

[ ] Push проверяется.

[ ] Формируется стабильная Raw URL.

[ ] AI chat получает только короткое сообщение с Raw URL.

[ ] При отсутствии изменений новый commit не создаётся.

[ ] Повторный запуск безопасен.

[ ] test1 не захардкожен.

[ ] GitHub credentials не находятся в коде.

[ ] GitHub token не появляется в логах.

[ ] Документация обновлена.

[ ] Тесты проходят.

==================================================
25. ВАЖНО: СНАЧАЛА ПРОАНАЛИЗИРУЙ, ПОТОМ МЕНЯЙ
==================================================

Не начинай сразу редактировать файлы.

Сначала:

1. Найди все места, связанные с chunking.
2. Найди pipeline --auto.
3. Найди AI chat sender.
4. Найди генерацию 03_scraper_prompt.md.
5. Найди Git integration.
6. Найди configuration.
7. Найди tests.

После анализа покажи:

- какие файлы будут изменены;
- какой текущий execution flow;
- какой будет новый execution flow;
- где именно будет удалено/обходиться chunking;
- где будет добавлен Git push;
- где будет формироваться Raw URL.

После этого реализуй изменения.

Не меняй unrelated functionality.

==================================================
КОНЕЧНАЯ АРХИТЕКТУРА
==================================================

Должно получиться:

    python ai_workflow.py pipeline test1 --auto
                    │
                    ▼
            Generate prompt
                    │
                    ▼
       03_scraper_prompt.md
                    │
                    ▼
              git status
                    │
             ┌──────┴──────┐
             │             │
        changed          unchanged
             │             │
             ▼             │
         git add            │
             │              │
             ▼              │
         git commit         │
             │              │
             ▼              │
         git push           │
             │              │
             └──────┬───────┘
                    ▼
             verify remote
                    │
                    ▼
              build Raw URL
                    │
                    ▼
              AI Chat
                    │
                    ▼
        ONLY ONE SHORT MESSAGE
        containing Raw URL


Главная цель:

Убрать ненадёжную передачу большого prompt через 10–20 сообщений и заменить её на надёжный:

    FILE → GITHUB → RAW URL → AI

Не ограничивай размер prompt искусственно 400 строками.

Один prompt = один файл.

Одна публикация = один Git commit (только если файл изменился).

Один AI input = одна Raw URL.