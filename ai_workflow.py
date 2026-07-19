#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый инструмент для Upwork scraping-проектов.

Использование:
    python ai_workflow.py new <project_name>
    python ai_workflow.py analyze [project_name]
    python ai_workflow.py project [project_name]
    python ai_workflow.py module scraper [project_name]
    python ai_workflow.py module parser [project_name]
    python ai_workflow.py debug [project_name]
    python ai_workflow.py docker [project_name]
    python ai_workflow.py review [project_name]
    python ai_workflow.py improve [project_name]

Если project_name не указан — берётся текущая папка (если это проект).

"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

import json
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore


# ---------------------------------------------------------------------------
# Пути
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = WORKSPACE_ROOT / "scraping-templates"
PROMPTS_DIR = TEMPLATES_DIR / "prompts"
AI_RULES_FILE = TEMPLATES_DIR / "AI_rules.md"
PROJECT_TEMPLATE = WORKSPACE_ROOT / "starter-project"
PROJECTS_DIR = WORKSPACE_ROOT / "projects"
ARCHIVE_DIR = WORKSPACE_ROOT / "archive"
WORKFLOW_VERSION = "0.2"

OUTPUT_PROMPT = "final_prompt.md"

STAGES = {
    "analyze": {"prompt": "01_analysis_prompt.md", "answer": "01_analysis_answer.md"},
    "project": {"prompt": "02_project_prompt.md", "answer": "02_project_answer.md"},
    "scraper": {"prompt": "03_scraper_prompt.md", "answer": "03_scraper_answer.py"},
    "parser": {"prompt": "04_parser_prompt.md", "answer": "04_parser_answer.py"},
    "debug": {"prompt": "05_debug_prompt.md", "answer": "05_debug_answer.md"},
    "docker": {"prompt": "06_docker_prompt.md", "answer": "06_Dockerfile"},
    "review": {"prompt": "07_platform_review_prompt.md", "answer": "07_platform_review_answer.md"},
    "improve": {"prompt": "08_platform_improve_prompt.md", "answer": "08_platform_improve_answer.md"},
}

# Задача (task) для платформенных команд review/improve.
# review — расследование архитектурной ошибки (берём существующий 06_review.md).
# improve — общие улучшения платформы без привязки к конкретной ошибке.
PLATFORM_TASK_FILES = {
    "review": "06_review.md",
    "improve": "09_improve_task.md",
}


CORE_FILES = [
    "app/main.py",
    "app/browser.py",
    "app/config.py",
    "app/exporter.py",
    "app/utils.py",
]

MODULE_FILES = {
    "scraper": "app/scraper.py",
    "parser": "app/parser.py",
}

COPY_SKIP_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".venv", "venv", "env",
    "node_modules", "dist", "build", "logs",
}

COPY_SKIP_FILES = {
    "output_results.csv",
    "output_results.json",
    OUTPUT_PROMPT,
    "final_prompt_for_ai.md",
    "analysis.md",
    "project_plan.md",
}


# ---------------------------------------------------------------------------
# Утилиты
# ---------------------------------------------------------------------------

def die(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}")
    sys.exit(code)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def info(message: str) -> None:
    print(f"[INFO] {message}")


def is_project_dir(path: Path) -> bool:
    return (path / "app" / "main.py").exists() and (path / "AI_INPUT").is_dir()


def find_project(name: Optional[str]) -> Path:
    if name:
        project = PROJECTS_DIR / name
        if not is_project_dir(project):
            die(f"Проект не найден: {project}")
        return project

    cwd = Path.cwd().resolve()
    if is_project_dir(cwd):
        return cwd

    die(
        "Не удалось определить проект.\n"
        "   Запусти из папки проекта или укажи имя:\n"
        "   python ai_workflow.py analyze amazon_scraper"
    )


def validate_project_name(name: str) -> str:
    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_-]*", name):
        die("Имя проекта: только латиница, цифры, _ и -. Начинаться с буквы.")
    if name == "starter-project":
        die("Нельзя использовать имя starter-project — это шаблон.")
    return name


def read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def clean_directory(path: Path) -> None:
    """Удаляет все содержимое папки, кроме .gitkeep."""
    if not path.exists():
        return

    for item in path.iterdir():
        if item.name == ".gitkeep":
            continue

        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def create_project_state(project: Path) -> None:
    state = {
        "project_name": project.name,
        "status": "created",
        "workflow_version": WORKFLOW_VERSION,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "current_step": "new",
        "completed_steps": []
    }

    write_text(
        project / "project_state.json",
        json.dumps(state, indent=4, ensure_ascii=False)
    )

def clear_files(directory: Path) -> None:
    """Очищает содержимое всех файлов в папке, не удаляя сами файлы."""
    if not directory.exists():
        return

    for item in directory.iterdir():
        if item.is_file():
            item.write_text("", encoding="utf-8")

def load_template(stage: str) -> str:
    # Достаем словарь для этапа
    stage_info = STAGES.get(stage)
    if not stage_info:
        die(f"Неизвестный этап: {stage}")
    
    # Достаем имя файла промпта из словаря
    filename = stage_info.get("prompt")
    
    path = PROMPTS_DIR / filename
    if not path.exists():
        die(f"Шаблон промпта не найден: {path}")
    return read_text(path)


def fill_template(template: str, mapping: dict[str, str]) -> str:
    result = template
    for key, value in mapping.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def simplify_html(file_path: Path) -> str:
    if BeautifulSoup is None:
        return f"\n\n--- HTML: {file_path.name} ---\n{read_text(file_path)}"

    try:
        soup = BeautifulSoup(read_text(file_path), "html.parser")
        for tag in soup(["script", "style", "noscript", "svg", "meta", "link", "footer", "nav", "iframe"]):
            tag.decompose()

        allowed_attrs = {"class", "id", "data-test-id", "href", "src", "name"}
        for tag in soup.find_all(True):
            for attr in list(tag.attrs):
                if attr not in allowed_attrs:
                    del tag[attr]

        return f"\n\n--- СЖАТЫЙ HTML: {file_path.name} ---\n{soup.prettify()}"
    except Exception as exc:
        return f"\n\n--- ОШИБКА HTML {file_path.name}: {exc} ---\n"


def collect_ai_input(project: Path, include_html: bool = True) -> str:
    input_dir = project / "AI_INPUT"
    if not input_dir.exists():
        return "(AI_INPUT пуст или не существует)"

    extensions = {".txt", ".html", ".md", ".json", ".har"}
    files = sorted(
        [f for f in input_dir.iterdir() if f.is_file() and f.suffix in extensions],
        key=lambda x: (x.name != "description.txt", x.name),
    )

    parts: list[str] = []
    for file_path in files:
        if file_path.suffix == ".html" and include_html:
            parts.append(simplify_html(file_path))
        else:
            parts.append(f"\n\n--- ФАЙЛ: {file_path.name} ---\n{read_text(file_path)}")

    return "".join(parts) if parts else "(файлы в AI_INPUT не найдены)"


def collect_core_files(project: Path) -> str:
    parts: list[str] = []
    for rel in CORE_FILES:
        path = project / rel
        parts.append(f"\n\n--- {rel} (НЕ МЕНЯТЬ) ---\n{read_text(path, '(файл не найден)')}")
    return "".join(parts)


def collect_app_code(project: Path) -> str:
    app_dir = project / "app"
    if not app_dir.exists():
        return "(папка app не найдена)"

    parts: list[str] = []
    for path in sorted(app_dir.glob("*.py")):
        rel = path.relative_to(project).as_posix()
        parts.append(f"\n\n--- {rel} ---\n{read_text(path)}")
    return "".join(parts)


def collect_debug_context(project: Path) -> str:
    candidates = [
        project / "AI_OUTPUT" / "traceback.txt",
        project / "logs" / "last_error.txt",
        project / "traceback.txt",
    ]
    for path in candidates:
        if path.exists() and path.stat().st_size > 0:
            return f"\n\n--- {path.name} ---\n{read_text(path)}"
    return "(traceback не найден — сохрани ошибку в AI_OUTPUT/traceback.txt)"


TRACEBACK_NOT_FOUND = "(traceback не найден — сохрани ошибку в AI_INPUT/traceback.txt)"
EXECUTION_LOG_NOT_FOUND = "(лог выполнения не найден — сохрани вывод консоли в AI_INPUT/log.txt)"


def collect_traceback(project: Path) -> str:
    """Ищет traceback в стандартных местах проекта."""
    candidates = [
        project / "AI_INPUT" / "traceback.txt",
        project / "AI_OUTPUT" / "traceback.txt",
        project / "logs" / "last_error.txt",
        project / "traceback.txt",
    ]
    for path in candidates:
        if path.exists() and path.stat().st_size > 0:
            return read_text(path)
    return TRACEBACK_NOT_FOUND


def collect_execution_log(project: Path) -> str:
    """Ищет лог выполнения (консольный вывод) в стандартных местах проекта."""
    candidates = [
        project / "AI_INPUT" / "log.txt",
        project / "AI_INPUT" / "console_output.txt",
        project / "logs" / "console_output.txt",
        project / "logs" / "log.txt",
    ]
    for path in candidates:
        if path.exists() and path.stat().st_size > 0:
            return read_text(path)

    logs_dir = project / "logs"
    if logs_dir.exists():
        for f in sorted(logs_dir.glob("*.txt")):
            if f.stat().st_size > 0:
                return read_text(f)

    return EXECUTION_LOG_NOT_FOUND



def code_block(path: Path, lang: str = "python") -> str:
    """Оборачивает содержимое файла в markdown code block."""
    content = read_text(path, "(файл не найден)")
    return f"```{lang}\n{content}\n```"


def generate_project_structure(project: Path) -> str:
    """Строит дерево структуры конкретного проекта (без содержимого workspace)."""
    lines: list[str] = [f"{project.name}/"]

    def walk(directory: Path, prefix: str = "") -> None:
        try:
            items = sorted(
                [
                    item for item in directory.iterdir()
                    if item.name not in COPY_SKIP_DIRS and not item.name.startswith(".")
                ],
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except PermissionError:
            return

        for index, item in enumerate(items):
            last = index == len(items) - 1
            connector = "└── " if last else "├── "
            if item.is_dir():
                lines.append(f"{prefix}{connector}{item.name}/")
                walk(item, prefix + ("    " if last else "│   "))
            else:
                lines.append(f"{prefix}{connector}{item.name}")

    walk(project)
    return "\n".join(lines)



def save_prompt(project: Path, content: str, stage: str) -> Path:
    # Берем имя файла промпта из вложенного словаря
    filename = STAGES[stage]["prompt"]
    out = project / "AI_OUTPUT" / filename
    write_text(out, content)
    return out


def create_default_ai_output_files(project: Path) -> None:
    """Создаёт пустые шаблоны для ответов ИИ в AI_OUTPUT проекта."""
    ai_output_dir = project / "AI_OUTPUT"
    ai_output_dir.mkdir(parents=True, exist_ok=True)

    for filename in [
        "01_analysis_answer.md",
        "02_project_answer.md",
        "03_scraper_answer.py",
        "04_parser_answer.py",
    ]:
        write_text(ai_output_dir / filename, "")


def next_step_hint(stage: str, project: Path) -> None:
    # Получаем имена файлов из нашего словаря STAGES
    prompt_file = project / "AI_OUTPUT" / STAGES[stage]["prompt"]
    answer_file = project / "AI_OUTPUT" / STAGES[stage]["answer"]
    
    print()
    info("Следующий шаг:")
    print(f"1. Открой: {prompt_file}")
    print(f"2. Отправь в ChatGPT")
    print(f"3. Сохрани ответ в: {answer_file}")


# ---------------------------------------------------------------------------
# Команды
# ---------------------------------------------------------------------------

def cmd_new(name: str) -> None:
    name = validate_project_name(name)
    PROJECTS_DIR.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)

    dest = PROJECTS_DIR / name

    if dest.exists():
        die(f"Проект уже существует: {dest}")

    if not PROJECT_TEMPLATE.exists():
        die(f"Шаблон не найден: {PROJECT_TEMPLATE}")

    info(f"Создаю проект: {dest}")

    def ignore(dir_path: str, names: list[str]) -> list[str]:
        ignored = []
        for n in names:
            if n in COPY_SKIP_DIRS:
                ignored.append(n)
            elif n in COPY_SKIP_FILES:
                ignored.append(n)
        return ignored

    shutil.copytree(PROJECT_TEMPLATE, dest, ignore=ignore)
    create_project_state(dest)  

    # Очистка артефактов шаблона
    clean_directory(dest / "output")
    clean_directory(dest / "AI_OUTPUT")
    clean_directory(dest / "logs")
    clean_directory(dest / "tests" / "output")
    clear_files(dest / "AI_INPUT")

    # Пустые шаблоны AI_INPUT и AI_OUTPUT
    write_text(dest / "AI_INPUT" / "description.txt", "# Описание задачи клиента\n\nURL:\n\nПоля для извлечения:\n\n")
    write_text(dest / "AI_INPUT" / "answers.txt", "")
    write_text(dest / "AI_INPUT" / "cookies.json", "[]\n")
    write_text(dest / "AI_INPUT" / "headers.json", "{}\n")
    create_default_ai_output_files(dest)

    # README проекта
    readme = f"""# {name}

## Быстрый старт

```bash
# 1. Заполни AI_INPUT/ (description.txt, page.html, network.har...)
python ../ai_workflow.py analyze {name}

# 2. Сохрани ответ ИИ в AI_OUTPUT/analysis.md
python ../ai_workflow.py project {name}

# 3. Сохрани ответ в AI_OUTPUT/project_plan.md
python ../ai_workflow.py module scraper {name}
python ../ai_workflow.py module parser {name}

# 4. Запуск
cd {name}
python -m app.main
```

## Структура

- `AI_INPUT/` — данные от клиента
- `AI_OUTPUT/` — промпты и ответы ИИ
- `app/` — код парсера
- `output/` — результаты CSV/JSON
"""
    write_text(dest / "README.md", readme)

    # Dockerfile-заготовка
    if not (dest / "Dockerfile").exists():
        write_text(dest / "Dockerfile", read_text(TEMPLATES_DIR / "templates" / "docker" / "Dockerfile", ""))

    ok(f"Проект создан: {dest}")
    print()
    info("Дальше:")
    print(f"   1. Заполни {dest / 'AI_INPUT' / 'description.txt'}")
    print(f"   2. Копируй и вставляй команды ниже:")
    print(f"      python ai_workflow.py analyze {name}")
    print(f"      python ai_workflow.py project {name}")
    print(f"      python ai_workflow.py scraper {name}")
    print(f"      python ai_workflow.py parser {name}")
    print(f"      python ai_workflow.py debug {name}")
    print(f"   3. В {dest / 'AI_OUTPUT'} созданы пустые шаблоны:")
    for filename in [
        "01_analysis_answer.md",
        "02_project_answer.md",
        "03_scraper_answer.py",
        "04_parser_answer.py",
    ]:
        print(f"      - {dest / 'AI_OUTPUT' / filename}")


def cmd_analyze(project: Path) -> None:
    template = load_template("analyze")
    prompt = fill_template(template, {
        "CLIENT_DESCRIPTION": collect_ai_input(project),
    })
    out = save_prompt(project, prompt, "analyze")
    ok(f"Промпт анализа: {out}")
    next_step_hint("analyze", project)


def cmd_project(project: Path) -> None:
    # Теперь мы ищем не "analysis.md", а файл из STAGES["analyze"]["answer"]
    analysis_answer = project / "AI_OUTPUT" / STAGES["analyze"]["answer"]
    
    if not analysis_answer.exists():
        die(f"Сначала сохрани ответ ИИ в {analysis_answer}")

    template = load_template("project")
    prompt = fill_template(template, {
        "CLIENT_DESCRIPTION": read_text(project / "AI_INPUT" / "description.txt"),
        "APPROVED_STRATEGY": read_text(analysis_answer),
        "AI_INPUT_ANALYSIS": collect_ai_input(project),
    })
    
    out = save_prompt(project, prompt, "project")
    ok(f"Промпт проектирования: {out}")
    next_step_hint("project", project)


def cmd_scraper(project: Path) -> None:
    # Проверяем, что анализ уже существует
    analysis_file = project / "AI_OUTPUT" / "01_analysis_answer.md"
    if not analysis_file.exists():
        die(f"Сначала сохрани анализ в {analysis_file}")

    # Проверяем, что план уже существует
    plan_file = project / "AI_OUTPUT" / "02_project_answer.md"
    if not plan_file.exists():
        die(f"Сначала сохрани план в {plan_file}")

    module_file = MODULE_FILES["scraper"]
    module_path = project / module_file

    template = load_template("scraper")

    prompt = fill_template(
        template,
        {
            "ANALYSIS": read_text(analysis_file),
            "PROJECT_PLAN": read_text(plan_file),
            "AI_RULES": read_text(AI_RULES_FILE),
            "AI_INPUT": collect_ai_input(project, include_html=False),

            "MODULE_FILE": module_file,
            "MODULE_NAME": "scraper",
            "MODULE_TEMPLATE": read_text(module_path, "(пустой файл)"),
            "CORE_FILES": collect_core_files(project),
        },
    )

    out = save_prompt(project, prompt, "scraper")

    ok(f"Промпт скрапера: {out}")
    print(f"\n1. Отправь в ChatGPT: {out}")
    print(f"2. Сохрани ответ (код) в: {project / 'AI_OUTPUT' / '03_scraper_answer.py'}")


def cmd_parser(project: Path) -> None:
    # Проверяем, что анализ уже существует
    analysis_file = project / "AI_OUTPUT" / "01_analysis_answer.md"
    if not analysis_file.exists():
        die(f"Сначала сохрани анализ в {analysis_file}")

    # Проверяем, что план уже существует
    plan_file = project / "AI_OUTPUT" / "02_project_answer.md"
    if not plan_file.exists():
        die(f"Сначала сохрани план в {plan_file}")

    # Парсер теперь знает про код скрапера (для согласования формата данных)
    scraper_code = project / "AI_OUTPUT" / "03_scraper_answer.py"
    if not scraper_code.exists():
        die(f"Сначала сохрани код скрапера в {scraper_code}")

    module_file = MODULE_FILES["parser"]
    module_path = project / module_file

    template = load_template("parser")  # Подтянет 04_parser_prompt.md

    prompt = fill_template(
        template,
        {
            "ANALYSIS": read_text(analysis_file),
            "PROJECT_PLAN": read_text(plan_file),
            "AI_RULES": read_text(AI_RULES_FILE),
            "AI_INPUT": collect_ai_input(project, include_html=False),

            "MODULE_FILE": module_file,
            "MODULE_NAME": "parser",
            "MODULE_TEMPLATE": read_text(module_path, "(пустой файл)"),
            "CORE_FILES": collect_core_files(project),

            # SCRAPER_CODE оставлен для совместимости, если понадобится в шаблоне промпта
            "SCRAPER_CODE": read_text(scraper_code),
        },
    )

    out = save_prompt(project, prompt, "parser")
    ok(f"Промпт парсера: {out}")
    print(f"\n1. Отправь в ChatGPT: {out}")
    print(f"2. Сохрани ответ (код) в: {project / 'AI_OUTPUT' / '04_parser_answer.py'}")


def cmd_archive(project: Path) -> None:
    """Перемещает проект в архив."""

    if not project.exists():
        die(f"Проект не найден: {project}")

    year = datetime.now().strftime("%Y")

    target = ARCHIVE_DIR / year / project.name
    target.parent.mkdir(parents=True, exist_ok=True)

    info(f"Архивирую проект: {project.name}")

    shutil.move(str(project), str(target))

    ok(f"Проект перенесён в: {target}")

def cmd_debug(project: Path) -> None:
    # ВАЖНО: используем реальные имена файлов из STAGES, а не устаревшие
    # "analysis.md"/"project_plan.md" — их не существует в проекте.
    analysis_file = project / "AI_OUTPUT" / STAGES["analyze"]["answer"]
    plan_file = project / "AI_OUTPUT" / STAGES["project"]["answer"]

    # Собираем ERROR_LOG из двух источников: traceback (если реальный краш)
    # и execution log (если просто "0 карточек", "пустой результат" и т.п.)
    # ВАЖНО: сравниваем с точными константами-заглушками, а не ищем подстроку
    # "не найден" — реальные логи парсера часто содержат фразы вида
    # "Карточки объявлений на странице не найдены", что ранее приводило
    # к ложному отбрасыванию валидного лога.
    traceback_text = collect_traceback(project)
    log_text = collect_execution_log(project)

    error_log_parts = []
    if traceback_text != TRACEBACK_NOT_FOUND:
        error_log_parts.append(f"--- TRACEBACK ---\n{traceback_text}")
    if log_text != EXECUTION_LOG_NOT_FOUND:
        error_log_parts.append(f"--- EXECUTION LOG (консольный вывод) ---\n{log_text}")


    if not error_log_parts:
        error_log = (
            "(Ни traceback, ни лог выполнения не найдены.\n"
            " Сохрани вывод консоли в AI_INPUT/log.txt "
            "или реальный traceback в AI_INPUT/traceback.txt перед запуском debug.)"
        )
    else:
        error_log = "\n\n".join(error_log_parts)

    template = load_template("debug")
    prompt = fill_template(template, {
        "ANALYSIS": read_text(analysis_file, "(нет 01_analysis_answer.md — сначала выполни analyze)"),
        "PROJECT_PLAN": read_text(plan_file, "(нет 02_project_answer.md — сначала выполни project)"),
        "CURRENT_CODE": collect_app_code(project),
        "ERROR_LOG": error_log,
        "AI_RULES": read_text(AI_RULES_FILE),
    })
    out = save_prompt(project, prompt, "debug")
    ok(f"Промпт отладки: {out}")
    next_step_hint("debug", project)


def cmd_docker(project: Path) -> None:
    template = load_template("docker")
    prompt = fill_template(template, {
        "PROJECT_NAME": project.name,
        "ANALYSIS": read_text(project / "AI_OUTPUT" / STAGES["analyze"]["answer"], "(нет 01_analysis_answer.md)"),
        "PROJECT_CODE": collect_app_code(project),
        "REQUIREMENTS": read_text(project / "requirements.txt"),
        "AI_RULES": read_text(AI_RULES_FILE),
    })
    out = save_prompt(project, prompt, "docker")
    ok(f"Промпт Docker: {out}")
    next_step_hint("docker", project)



def build_platform_dump(project: Path, task_content: str) -> str:
    """
    Собирает ВСЁ по цепочке workflow в единый markdown-документ:

    description.txt -> 01_analysis_answer -> 02_project_answer ->
    scraper.py -> parser.py -> browser.py -> main.py ->
    traceback -> execution log -> PROJECT_STRUCTURE -> TASK

    Именно этот документ вставляется целиком в ChatGPT.
    """
    sections: list[tuple[str, str]] = []

    sections.append(("CLIENT DESCRIPTION", read_text(
        project / "AI_INPUT" / "description.txt", "(description.txt не найден)"
    )))

    sections.append(("ANALYSIS", read_text(
        project / "AI_OUTPUT" / STAGES["analyze"]["answer"], "(01_analysis_answer.md не найден)"
    )))

    sections.append(("PROJECT PLAN", read_text(
        project / "AI_OUTPUT" / STAGES["project"]["answer"], "(02_project_answer.md не найден)"
    )))

    sections.append(("SCRAPER.PY", code_block(project / "app" / "scraper.py")))
    sections.append(("PARSER.PY", code_block(project / "app" / "parser.py")))

    sections.append(("TRACEBACK", collect_traceback(project)))
    sections.append(("EXECUTION LOG", collect_execution_log(project)))

    sections.append(("BROWSER.PY", code_block(project / "app" / "browser.py")))
    sections.append(("MAIN.PY", code_block(project / "app" / "main.py")))

    sections.append(("PROJECT STRUCTURE", generate_project_structure(project)))

    sections.append(("YOUR TASK", task_content))

    separator = "\n\n" + ("-" * 60) + "\n\n"
    parts = [f"# {title}\n\n{content}" for title, content in sections]
    return separator.join(parts)


def cmd_platform(project: Path, mode: str) -> None:
    """
    Общая реализация для 'review' и 'improve'.

    Собирает весь контекст проекта (описание, анализ, план, код модулей,
    traceback, лог выполнения, структуру) + задачу (task) в один готовый
    промпт AI_OUTPUT/0X_platform_..._prompt.md, который остаётся только
    вставить в ChatGPT.
    """
    task_file = PROMPTS_DIR / PLATFORM_TASK_FILES[mode]
    task_content = read_text(
        task_file,
        f"(файл задачи не найден: {task_file})"
    )

    prompt = build_platform_dump(project, task_content)
    out = save_prompt(project, prompt, mode)

    ok(f"Промпт '{mode}' собран: {out}")
    print(f"\n1. Открой файл: {out}")
    print(f"2. Вставь ЦЕЛИКОМ в ChatGPT.")
    print(f"3. Сохрани ответ в: {project / 'AI_OUTPUT' / STAGES[mode]['answer']}")


def cmd_review(project: Path) -> None:
    cmd_platform(project, "review")


def cmd_improve(project: Path) -> None:
    cmd_platform(project, "improve")



# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Единый workflow для Upwork scraping-проектов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python ai_workflow.py new amazon_scraper
  python ai_workflow.py analyze amazon_scraper
  python ai_workflow.py project amazon_scraper
  python ai_workflow.py module scraper amazon_scraper
  python ai_workflow.py module parser amazon_scraper
  python ai_workflow.py debug amazon_scraper
  python ai_workflow.py docker amazon_scraper
  python ai_workflow.py review amazon_scraper
  python ai_workflow.py improve amazon_scraper
        """,
    )
    parser.add_argument(
        "command",
        choices=["new", "analyze", "archive", "project", "scraper", "parser", "debug", "docker", "review", "improve"],
        help="Этап workflow",
    )

    parser.add_argument(
        "args",
        nargs="*",
        help="Для new: имя проекта. Для module: scraper|parser. Опционально: имя проекта.",
    )
    return parser


def parse_args(raw_args: list[str]) -> tuple[str, Optional[str], Optional[str]]:
    """
    Разбирает аргументы:
      new <name>
      module <scraper|parser> [project]
      <command> [project]
    """
    if not raw_args:
        die("Укажи команду. Пример: python ai_workflow.py analyze")

    command = raw_args[0]
    rest = raw_args[1:]

    if command == "new":
        if not rest:
            die("Укажи имя проекта: python ai_workflow.py new amazon_scraper")
        return command, rest[0], None

    if command == "module":
        if not rest:
            die("Укажи модуль: python ai_workflow.py module scraper")
        module_name = rest[0]
        project_name = rest[1] if len(rest) > 1 else None
        return command, project_name, module_name

    project_name = rest[0] if rest else None
    return command, project_name, None


def main() -> None:
    command, project_name, module_name = parse_args(sys.argv[1:])

    if command == "new":
        cmd_new(project_name)  # type: ignore[arg-type]
        return

    project = find_project(project_name)

    dispatch = {
        "analyze": lambda: cmd_analyze(project),
        "project": lambda: cmd_project(project),
        "scraper": lambda: cmd_scraper(project),
        "parser": lambda: cmd_parser(project),
        "debug": lambda: cmd_debug(project),
        "docker": lambda: cmd_docker(project),
        "archive": lambda: cmd_archive(project),
        "review": lambda: cmd_review(project),
        "improve": lambda: cmd_improve(project),
    }


    dispatch[command]()


if __name__ == "__main__":
    main()
