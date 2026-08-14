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
    python ai_workflow.py clean [project_name]
    python ai_workflow.py pipeline [project_name] [--auto]

Если project_name не указан — берётся текущая папка (если это проект).

"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import json
from datetime import datetime

# ---------------------------------------------------------------------------
# Auto-send конфигурация (для --auto)
# ---------------------------------------------------------------------------

AUTO_SEND_DEFAULTS = {
    "max_lines": 400,
    "delay": 2,
    "timeout": 600,
    "retries": 3,
}

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

# ---------------------------------------------------------------------------
# GitHub Raw URL конфигурация
# Порядок: env vars → config file → defaults
# ---------------------------------------------------------------------------

GITHUB_CONFIG_FILE = WORKSPACE_ROOT / ".github_config.json"

def _load_github_config() -> dict:
    cfg: dict = {}
    if GITHUB_CONFIG_FILE.exists():
        try:
            cfg = json.loads(GITHUB_CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return cfg

def _get_github_setting(key: str, config_key: str, default: str) -> str:
    """Читает настройку: env var → config file → default."""
    val = os.environ.get(key, "").strip()
    if val:
        return val
    cfg = _load_github_config()
    return cfg.get(config_key, default)

GITHUB_OWNER = lambda: _get_github_setting("GITHUB_OWNER", "owner", "ypauk")
GITHUB_REPO  = lambda: _get_github_setting("GITHUB_REPO",  "repo",  "ScrapData")
GITHUB_BRANCH = lambda: _get_github_setting("GITHUB_BRANCH", "branch", "main")

PROMPT_FILE_TEMPLATE = "projects/{project}/AI_OUTPUT/03_scraper_prompt.md"

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
    "app/playwright_engine.py",
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


def extract_python_code(content: str) -> str:
    """
    Извлекает Python-код из ответа GPT.
    Если есть ```python ... ``` блок — берёт содержимое блока.
    Если блоков нет — ищет начало кода по первой строке с # или import/from/def/class.
    """
    # Ищем блоки ```python ... ``` или просто ``` ... ```
    pattern = r"```(?:python)?\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        # Берём самый длинный блок (это и есть основной код)
        return max(matches, key=len).strip()

    # Блока нет — GPT вернул код без markdown-обёртки (с объяснениями вокруг).
    # Ищем первую строку, которая выглядит как начало Python-файла.
    import ast
    lines = content.splitlines()
    code_start_re = re.compile(r"^(#!|# |#$|import |from |def |class )")
    for i, line in enumerate(lines):
        if code_start_re.match(line):
            candidate = "\n".join(lines[i:])
            # Отрезаем "хвост" после последней валидной Python-строки:
            # ищем последнюю позицию, с которой AST парсится без ошибок.
            # Простой вариант: обрезаем строки снизу, пока не останется валидный код.
            chunk_lines = candidate.splitlines()
            for j in range(len(chunk_lines), 0, -1):
                try:
                    ast.parse("\n".join(chunk_lines[:j]))
                    return "\n".join(chunk_lines[:j]).strip()
                except SyntaxError:
                    continue
            break

    return content


def validate_python_syntax(code: str) -> tuple[bool, str]:
    """Проверяет синтаксис Python. Возвращает (ok, error_message)."""
    import ast
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, str(e)


def apply_answer_to_app(stage: str, project: Path) -> bool:
    """Копирует ответ ИИ (scraper/parser) в app/ если файл не пустой и синтаксически валиден.
    Возвращает True при успехе, False при ошибке."""
    if stage not in MODULE_FILES:
        return True

    answer_file = project / "AI_OUTPUT" / STAGES[stage]["answer"]
    target_file = project / MODULE_FILES[stage]

    if not answer_file.exists():
        return True

    raw_content = answer_file.read_text(encoding="utf-8").strip()
    if not raw_content:
        return True

    # Извлекаем Python-код из ответа (на случай если GPT добавил текст вокруг кода)
    code = extract_python_code(raw_content)

    # Проверяем синтаксис перед записью
    syntax_ok, syntax_error = validate_python_syntax(code)
    if not syntax_ok:
        print(f"[WARNING] Синтаксическая ошибка в ответе ИИ для '{stage}': {syntax_error}")
        print(f"          Файл {target_file.name} НЕ обновлён.")
        print(f"          Проверь ответ вручную: {answer_file}")
        return False

    write_text(target_file, code)
    ok(f"Скопировано: {STAGES[stage]['answer']} → {MODULE_FILES[stage]}")
    return True


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
# GitHub Raw URL workflow
# ---------------------------------------------------------------------------

def build_raw_url(owner: str, repo: str, branch: str, file_path: str) -> str:
    path = file_path.replace("\\", "/").lstrip("/")
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result


def publish_prompt_to_github(prompt_path: Path, project_name: str) -> str:
    """
    Выполняет git add/commit/push для prompt_path, проверяет remote и возвращает Raw URL.
    Если файл не изменился — пропускает commit/push, возвращает URL текущего HEAD.
    """
    repo_root = WORKSPACE_ROOT
    rel_path = prompt_path.relative_to(repo_root).as_posix()
    owner = GITHUB_OWNER()
    repo = GITHUB_REPO()
    branch = GITHUB_BRANCH()

    # --- git status: проверяем, изменён ли файл ---
    print(f"[Git] Checking changes for {rel_path}...")
    status_result = _run_git(["status", "--porcelain", rel_path], repo_root)
    if status_result.returncode != 0:
        raise RuntimeError(f"[Git] git status failed: {status_result.stderr.strip()}")

    changed = bool(status_result.stdout.strip())

    if changed:
        # --- git add ---
        print(f"[Git] Changes detected. Staging {rel_path}...")
        add_result = _run_git(["add", rel_path], repo_root)
        if add_result.returncode != 0:
            raise RuntimeError(f"[Git] git add failed: {add_result.stderr.strip()}")

        # --- git commit ---
        commit_msg = f"ai: update prompt for {project_name}"
        print(f"[Git] Committing: {commit_msg}")
        commit_result = _run_git(["commit", "-m", commit_msg], repo_root)
        if commit_result.returncode != 0:
            err = commit_result.stderr.strip()
            if "Please tell me who you are" in err or "unable to auto-detect email" in err:
                raise RuntimeError(
                    "[Git] git commit failed: Git user не настроен.\n"
                    "  Выполни один раз:\n"
                    '    git config --global user.email "your@email.com"\n'
                    '    git config --global user.name "Your Name"'
                )
            raise RuntimeError(f"[Git] git commit failed: {err}")

        commit_sha = commit_result.stdout.strip().split("\n")[0]
        print(f"[Git] Commit: {commit_sha}")

        # --- git push ---
        print(f"[Git] Pushing to origin/{branch}...")
        push_result = _run_git(["push", "origin", branch], repo_root)
        if push_result.returncode != 0:
            raise RuntimeError(
                f"[Git] git push failed: {push_result.stderr.strip()}\n"
                f"  Убедись что Git credentials настроены (gh auth, credential manager или SSH)."
            )
        print(f"[Git] Push successful.")
    else:
        print(f"[Git] Prompt unchanged. No commit required.")

    # --- Получить текущий локальный SHA ---
    head_result = _run_git(["rev-parse", "HEAD"], repo_root)
    if head_result.returncode != 0:
        raise RuntimeError(f"[Git] rev-parse HEAD failed: {head_result.stderr.strip()}")
    local_sha = head_result.stdout.strip()

    # --- Проверить remote ---
    print(f"[Git] Verifying remote...")
    remote_result = _run_git(["ls-remote", "origin", branch], repo_root)
    if remote_result.returncode != 0:
        raise RuntimeError(f"[Git] ls-remote failed: {remote_result.stderr.strip()}")

    remote_sha = remote_result.stdout.strip().split("\t")[0] if remote_result.stdout.strip() else ""
    if remote_sha != local_sha:
        raise RuntimeError(
            f"[Git] Remote SHA mismatch after push!\n"
            f"  local:  {local_sha}\n"
            f"  remote: {remote_sha}\n"
            f"  Файл может быть не опубликован в GitHub."
        )
    print(f"[Git] Remote verified. SHA: {local_sha[:8]}")

    raw_url = build_raw_url(owner, repo, branch, rel_path)
    print(f"[AI] Raw URL: {raw_url}")

    # --- Итоговый вывод ---
    print()
    print("=" * 60)
    print("  AI PROMPT PUBLISHED")
    print()
    print(f"  File:")
    print(f"  {rel_path}")
    print()
    print(f"  GitHub:")
    print(f"  https://github.com/{owner}/{repo}")
    print()
    print(f"  Raw URL:")
    print(f"  {raw_url}")
    print()
    print(f"  Commit:")
    print(f"  {local_sha}")
    print()
    if changed:
        print("  Status: SUCCESS")
    else:
        print("  Status: SUCCESS (no changes, existing commit used)")
    print("=" * 60)

    return raw_url


def auto_send_via_url(raw_url: str, answer_path: Path,
                      timeout: int, retries: int, no_interact: bool = False) -> None:
    """
    Отправляет ОДНО короткое сообщение с Raw URL в ChatGPT через браузер.
    Ответ сохраняется в answer_path.
    """
    from prompt_splitter import (
        check_playwright_available, launch_browser, open_chatgpt,
        send_message, wait_for_response_complete, get_last_response,
        BROWSER_PROFILE_DIR, WORKSPACE_ROOT as PS_WORKSPACE,
    )

    message = (
        f"Прочитай полный prompt по этой ссылке и выполни задачу:\n{raw_url}"
    )

    print(f"\n{'=' * 60}")
    print(f"  ChatGPT Auto Sender (Raw URL mode)")
    print(f"{'=' * 60}")
    print(f"\n  URL: {raw_url}")
    print(f"  Answer: {answer_path.name}")
    print(f"\n  Browser: Chromium")
    print(f"  Profile: {BROWSER_PROFILE_DIR.relative_to(PS_WORKSPACE)}")
    print()

    if not check_playwright_available():
        die(
            "Playwright не установлен.\n"
            "  Установка:\n"
            "    pip install playwright\n"
            "    playwright install chromium"
        )

    print("  Запуск браузера...")
    pw, context, page = launch_browser()

    try:
        print("  Открываю ChatGPT...")
        open_chatgpt(page)

        print(f"\n{'=' * 60}")
        print("  ChatGPT готов.")
        if no_interact:
            import time as _time
            print("  Автоматический режим — старт через 3 сек...")
            _time.sleep(3)
        else:
            print("  Открой нужный чат или создай новый.")
            input("  Нажми Enter для начала отправки...")
        print(f"{'=' * 60}\n")

        print("  Sending Raw URL message...")
        prev_response = get_last_response(page)

        try:
            send_message(page, message, retries=retries)
        except RuntimeError as e:
            raise RuntimeError(f"Не удалось отправить сообщение: {e}")

        print("  Waiting for response...")
        wait_for_response_complete(page, timeout=timeout, prev_response=prev_response)
        print("  Response completed ✓")

        final_response = get_last_response(page)
        if final_response:
            if str(answer_path).endswith(".py"):
                code = extract_python_code(final_response)
                syntax_ok, _ = validate_python_syntax(code)
                if not syntax_ok:
                    print(f"  ⚠ WARNING: Ответ GPT не содержит валидный Python-код!")
                    if no_interact:
                        retry_messages = [
                            "Весь контекст получен. ТЕПЕРЬ выполни задачу — напиши полный Python код. Ответь ТОЛЬКО кодом в блоке ```python ... ```",
                            "Пожалуйста, напиши код сейчас. Ответь ТОЛЬКО Python кодом в блоке ```python ... ``` без пояснений.",
                        ]
                        for attempt, retry_msg in enumerate(retry_messages, 1):
                            print(f"  Автоматический режим — повторный запрос ({attempt}/{len(retry_messages)})...")
                            try:
                                _prev = get_last_response(page)
                                send_message(page, retry_msg, retries=retries)
                                wait_for_response_complete(page, timeout=timeout, prev_response=_prev)
                                final_response = get_last_response(page)
                                code = extract_python_code(final_response)
                                syntax_ok, _ = validate_python_syntax(code)
                                if syntax_ok:
                                    print(f"  ✓ Повторный запрос сработал, код получен.")
                                    break
                                else:
                                    print(f"  ⚠ Повторный запрос ({attempt}) — ответ всё ещё не код.")
                            except Exception as _err:
                                print(f"  [ERROR] Ошибка при повторном запросе: {_err}")
                        else:
                            print("  Все повторные запросы не дали кода.")
                            print(f"  Скопируй код вручную из ChatGPT в: {answer_path}")
                            return

            answer_path.parent.mkdir(parents=True, exist_ok=True)
            answer_path.write_text(final_response, encoding="utf-8")
            print(f"  ✓ Ответ сохранён: {answer_path}")
        else:
            print("  ✗ Не удалось получить текст ответа.")
            print("    Скопируй ответ вручную из окна ChatGPT.")

        print(f"\n{'=' * 60}")
        print(f"  DONE")
        print(f"{'=' * 60}")

    except KeyboardInterrupt:
        print("\n\n  Прервано (Ctrl+C). Браузер оставлен открытым.")
    finally:
        try:
            context.close()
            pw.stop()
        except Exception:
            pass


def auto_send_prompt(prompt_path: Path, answer_path: Path, max_lines: int,
                     delay: int, timeout: int, retries: int,
                     dry_run: bool = False, force: bool = False,
                     restart: bool = False, no_interact: bool = False) -> None:
    """
    Автоматически разбивает prompt и отправляет в ChatGPT через prompt_splitter.
    Ответ сохраняется в answer_path.
    """
    from prompt_splitter import (
        split_by_sections, group_sections, wrap_parts,
        calculate_file_hash, load_state, save_state, clear_state,
        check_playwright_available, launch_browser, open_chatgpt,
        send_message, wait_for_response_complete, get_last_response,
        verify_acknowledgement, find_chat_input,
        BROWSER_PROFILE_DIR, WORKSPACE_ROOT, STATE_FILE,
    )

    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    total_lines = text.count("\n") + 1

    # Разбиваем если нужно
    if total_lines <= max_lines:
        parts = [text]
    else:
        sections = split_by_sections(text)
        raw_parts = group_sections(sections, max_lines)
        parts = wrap_parts(raw_parts)

    total = len(parts)
    file_hash = calculate_file_hash(prompt_path)

    # --- Header ---
    print(f"\n{'=' * 60}")
    print(f"  ChatGPT Auto Sender")
    print(f"{'=' * 60}")
    print(f"\n  File: {prompt_path.name}")
    print(f"  Lines: {total_lines}")
    print(f"  Parts: {total}")
    print(f"  Answer: {answer_path.name}")
    print(f"\n  Browser: Chromium")
    print(f"  Profile: {BROWSER_PROFILE_DIR.relative_to(WORKSPACE_ROOT)}")
    print()

    if not check_playwright_available():
        die(
            "Playwright не установлен.\n"
            "  Установка:\n"
            "    pip install playwright\n"
            "    playwright install chromium"
        )

    # --- Resume ---
    start_part = 0
    if not restart:
        state = load_state()
        if state and state.get("file") == str(prompt_path):
            if state.get("file_hash") != file_hash:
                print("  WARNING: Исходный prompt изменился. Начинаем заново.\n")
                clear_state()
            elif state.get("last_completed_part", 0) > 0:
                completed = state["last_completed_part"]
                print(f"  Обнаружен предыдущий прогресс: {completed}/{total} частей.\n")
                if no_interact:
                    start_part = completed
                else:
                    answer = input(f"  Продолжить с части {completed + 1}? [Y/n] ").strip().lower()
                    if answer in ("", "y", "yes", "д", "да"):
                        start_part = completed
                    else:
                        clear_state()
    else:
        clear_state()

    # --- Dry run ---
    if dry_run:
        print("  --- DRY RUN ---")
        print(f"  Частей к отправке: {total - start_part}")
        for i in range(start_part, total):
            lines_count = parts[i].count("\n") + 1
            chars_count = len(parts[i])
            label = "ЗАДАЧА" if i == total - 1 else "Контекст"
            print(f"    [{i+1}/{total}] {label}: {lines_count} строк, {chars_count} символов")
        print(f"\n  Ответ будет сохранён в: {answer_path.name}")
        print("\n  Playwright: OK")
        print("  Сообщения НЕ будут отправлены.")
        print(f"\n{'=' * 60}")
        return

    # --- Launch browser ---
    print("  Запуск браузера...")
    pw, context, page = launch_browser()

    try:
        print("  Открываю ChatGPT...")
        open_chatgpt(page)

        print(f"\n{'=' * 60}")
        print("  ChatGPT готов.")
        if no_interact:
            import time as _time
            print("  Автоматический режим — старт через 3 сек...")
            _time.sleep(3)
        else:
            print("  Открой нужный чат или создай новый.")
            input("  Нажми Enter для начала автоматической отправки...")
        print(f"{'=' * 60}\n")

        import time

        for i in range(start_part, total):
            part_num = i + 1
            is_last = (i == total - 1)

            if is_last:
                print(f"  [{part_num}/{total}] Sending final task...")
            else:
                print(f"  [{part_num}/{total}] Sending...")

            prev_response = get_last_response(page)

            try:
                send_message(page, parts[i], retries=retries)
            except RuntimeError as e:
                print(f"\n  [ERROR] Не удалось отправить часть {part_num}/{total}.")
                print(f"  Причина: {e}")
                if no_interact:
                    save_state(str(prompt_path), file_hash, total, i)
                    print("  Автоматический режим — прерываем.")
                    return
                while True:
                    action = input("  [R] Retry / [A] Abort: ").strip().upper()
                    if action == "R":
                        try:
                            send_message(page, parts[i], retries=retries)
                            break
                        except RuntimeError as e2:
                            print(f"  [ERROR] Повторная ошибка: {e2}")
                    elif action == "A":
                        save_state(str(prompt_path), file_hash, total, i)
                        print("  Прервано. Браузер оставлен открытым.")
                        return

            print(f"  [{part_num}/{total}] Waiting for response...")
            try:
                wait_for_response_complete(page, timeout=timeout, prev_response=prev_response)
            except TimeoutError as e:
                print(f"  [ERROR] {e}")
                if no_interact:
                    print(f"  Автоматический режим — ждём ещё {timeout}с...")
                    try:
                        wait_for_response_complete(page, timeout=timeout)
                    except TimeoutError as e2:
                        print(f"  [ERROR] {e2}")
                        save_state(str(prompt_path), file_hash, total, i)
                        print("  Автоматический режим — прерываем по таймауту.")
                        return
                while True:
                    action = input("  [R] Retry wait / [A] Abort: ").strip().upper()
                    if action == "R":
                        try:
                            wait_for_response_complete(page, timeout=timeout)
                            break
                        except TimeoutError:
                            pass
                    elif action == "A":
                        save_state(str(prompt_path), file_hash, total, i)
                        return

            if not is_last:
                response_text = get_last_response(page)
                ack_ok = verify_acknowledgement(response_text, part_num)
                if ack_ok:
                    print(f"  [{part_num}/{total}] Acknowledgement ✓")
                elif force or no_interact:
                    print(f"  [{part_num}/{total}] Acknowledgement ? (auto/force)")
                else:
                    print(f"\n  WARNING: Неожиданный ответ после части {part_num}.")
                    if response_text:
                        print(f"  Ответ: {response_text[:200]}")
                    answer_input = input("  Продолжить? [y/N] ").strip().lower()
                    if answer_input not in ("y", "yes", "д", "да"):
                        save_state(str(prompt_path), file_hash, total, i)
                        return
            else:
                print(f"  [{part_num}/{total}] Response completed ✓")

            save_state(str(prompt_path), file_hash, total, part_num)

            if not is_last:
                time.sleep(delay)

            print()

        # --- Save answer ---
        print("  Сохраняю финальный ответ...")
        final_response = get_last_response(page)
        if final_response:
            # Для .py файлов — предупреждаем если ответ выглядит как acknowledgement, а не код
            if str(answer_path).endswith(".py"):
                code = extract_python_code(final_response)
                syntax_ok, _ = validate_python_syntax(code)
                if not syntax_ok:
                    print(f"  ⚠ WARNING: Ответ GPT не содержит валидный Python-код!")
                    print(f"  Возможно GPT ответил подтверждением вместо кода.")
                    print(f"  Ответ (первые 200 символов): {final_response[:200]}")
                    if no_interact:
                        # Retry: send explicit trigger to generate code
                        retry_messages = [
                            "Весь контекст получен. ТЕПЕРЬ выполни задачу — напиши полный Python код. Ответь ТОЛЬКО кодом в блоке ```python ... ```",
                            "Пожалуйста, напиши код сейчас. Ответь ТОЛЬКО Python кодом в блоке ```python ... ``` без пояснений.",
                        ]
                        for attempt, retry_msg in enumerate(retry_messages, 1):
                            print(f"  Автоматический режим — повторный запрос ({attempt}/{len(retry_messages)})...")
                            try:
                                _prev_before_retry = get_last_response(page)
                                send_message(page, retry_msg, retries=retries)
                                wait_for_response_complete(page, timeout=timeout, prev_response=_prev_before_retry)
                                final_response = get_last_response(page)
                                code = extract_python_code(final_response)
                                syntax_ok, _ = validate_python_syntax(code)
                                if syntax_ok:
                                    print(f"  ✓ Повторный запрос сработал, код получен.")
                                    break
                                else:
                                    print(f"  ⚠ Повторный запрос ({attempt}) — ответ всё ещё не код.")
                                    print(f"  Ответ (первые 200 символов): {final_response[:200]}")
                            except Exception as _retry_err:
                                print(f"  [ERROR] Ошибка при повторном запросе: {_retry_err}")
                        else:
                            print("  Автоматический режим — все повторные запросы не дали кода.")
                            print(f"  Скопируй код вручную из ChatGPT в: {answer_path}")
                            return
                    else:
                        action = input("  Сохранить всё равно? [y/N] ").strip().lower()
                        if action not in ("y", "yes", "д", "да"):
                            print("  Ответ НЕ сохранён. Скопируй код вручную из ChatGPT.")
                            return
            answer_path.parent.mkdir(parents=True, exist_ok=True)
            answer_path.write_text(final_response, encoding="utf-8")
            print(f"  ✓ Ответ сохранён: {answer_path}")
        else:
            print("  ✗ Не удалось получить текст ответа.")
            print("    Скопируй ответ вручную из окна ChatGPT.")

        clear_state()
        print(f"\n{'=' * 60}")
        print(f"  DONE")
        print(f"{'=' * 60}")

    except KeyboardInterrupt:
        print("\n\n  Прервано (Ctrl+C). Браузер оставлен открытым.")
    finally:
        try:
            context.close()
            pw.stop()
        except Exception:
            pass


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


def cmd_clean(project: Path) -> None:
    """Очищает AI_OUTPUT + scraper.py + parser.py + output/ для чистого теста."""
    ai_output = project / "AI_OUTPUT"
    if not ai_output.exists():
        die(f"Папка не найдена: {ai_output}")

    count = 0
    for item in ai_output.iterdir():
        if item.is_file():
            item.write_text("", encoding="utf-8")
            count += 1

    for module in ("scraper.py", "parser.py"):
        module_path = project / "app" / module
        if module_path.exists():
            module_path.write_text("", encoding="utf-8")
            count += 1

    output_dir = project / "output"
    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.name == ".gitkeep":
                continue
            if item.is_file():
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item)
                count += 1

    ok(f"Очищено: {count} (AI_OUTPUT + app/scraper.py, app/parser.py, output/)")


def cmd_pipeline(project: Path, opts) -> None:
    """
    Полный конвейер: analyze -> project -> scraper -> parser.

    В режиме --auto:
    - Этап 'scraper': генерирует промпт, публикует в GitHub, передаёт Raw URL в ChatGPT.
    - Остальные этапы: используют прежний chunked auto-send через ChatGPT.
    """
    stages_order = ["analyze", "project", "scraper", "parser"]

    stage_commands = {
        "analyze": cmd_analyze,
        "project": cmd_project,
        "scraper": cmd_scraper,
        "parser": cmd_parser,
    }

    total = len(stages_order)

    for idx, stage in enumerate(stages_order, 1):
        print(f"\n{'=' * 60}")
        print(f"  PIPELINE [{idx}/{total}]: {stage}")
        print(f"{'=' * 60}\n")

        stage_commands[stage](project)

        if opts.auto:
            stage_info = STAGES[stage]
            prompt_path = project / "AI_OUTPUT" / stage_info["prompt"]
            answer_path = project / "AI_OUTPUT" / stage_info["answer"]

            if not prompt_path.exists():
                die(f"Промпт не найден: {prompt_path}")

            # --- GitHub Raw URL flow для всех этапов ---
            print(f"\n[AI] Prompt written: {prompt_path}")
            try:
                raw_url = publish_prompt_to_github(prompt_path, project.name)
            except RuntimeError as e:
                die(str(e))
            if not opts.dry_run:
                auto_send_via_url(
                    raw_url=raw_url,
                    answer_path=answer_path,
                    timeout=opts.timeout,
                    retries=opts.retries,
                    no_interact=True,
                )

            if not opts.dry_run:
                if not answer_path.exists() or not answer_path.read_text(encoding="utf-8").strip():
                    die(f"Ответ не получен для этапа '{stage}'. Pipeline остановлен.")

            applied = apply_answer_to_app(stage, project)
            if not applied:
                die(f"Этап '{stage}': ответ GPT не содержит валидный Python-код. Pipeline остановлен.\n"
                    f"  Проверь файл вручную: {answer_path}\n"
                    f"  Скопируй код из ChatGPT и сохрани в этот файл, затем запусти pipeline заново.")
            ok(f"Этап '{stage}' завершён. Ответ сохранён в {answer_path.name}")
        else:
            answer_path = project / "AI_OUTPUT" / STAGES[stage]["answer"]
            print(f"\n  [!] --auto не указан. Ручной режим.")
            print(f"      1. Открой промпт: {project / 'AI_OUTPUT' / STAGES[stage]['prompt']}")
            print(f"      2. Отправь в ChatGPT")
            print(f"      3. Сохрани ответ в: {answer_path}")

            while True:
                input(f"\n  Нажми Enter когда ответ для '{stage}' будет сохранён (или Ctrl+C для выхода)...")

                if not answer_path.exists():
                    print(f"  [!] Файл не найден: {answer_path}")
                    print(f"      Создай файл и вставь туда ответ ИИ.")
                    continue

                if not answer_path.read_text(encoding="utf-8").strip():
                    print(f"  [!] Файл пуст: {answer_path}")
                    print(f"      Вставь ответ ИИ в этот файл и нажми Enter снова.")
                    continue

                apply_answer_to_app(stage, project)
                break

    print(f"\n{'=' * 60}")
    print(f"  PIPELINE ЗАВЕРШЁН УСПЕШНО")
    print(f"  Все этапы: {' -> '.join(stages_order)}")
    print(f"{'=' * 60}\n")


def cmd_review(project: Path) -> None:
    cmd_platform(project, "review")


def cmd_improve(project: Path) -> None:
    cmd_platform(project, "improve")


def cmd_login() -> None:
    """Открывает ChatGPT в браузере для ручного входа. Профиль сохраняется."""
    from prompt_splitter import launch_browser, BROWSER_PROFILE_DIR, CHATGPT_URL

    print("=" * 60)
    print("  ChatGPT Login")
    print("=" * 60)
    print(f"\n  Профиль: {BROWSER_PROFILE_DIR}")
    print("  Браузер откроется. Войди в аккаунт ChatGPT вручную.")
    print("  После входа нажми Enter в этом окне.\n")

    pw, context, page = launch_browser()
    try:
        page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=60000)
        input("  Войди в ChatGPT и нажми Enter для сохранения сессии...")
        context.storage_state()
    finally:
        try:
            context.close()
            pw.stop()
        except Exception:
            pass

    ok("Сессия сохранена. Теперь можно запускать pipeline --auto")



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
  python ai_workflow.py scraper amazon_scraper
  python ai_workflow.py parser amazon_scraper
  python ai_workflow.py debug amazon_scraper
  python ai_workflow.py docker amazon_scraper
  python ai_workflow.py review amazon_scraper
  python ai_workflow.py improve amazon_scraper

Очистка AI_OUTPUT (для тестов):
  python ai_workflow.py clean test1

Полный конвейер (все этапы подряд):
  python ai_workflow.py pipeline test1 --auto
  python ai_workflow.py pipeline test1            (ручной режим — ждёт Enter между этапами)

Автоотправка в ChatGPT:
  python ai_workflow.py debug amazon_scraper --auto
  python ai_workflow.py scraper amazon_scraper --auto --max-lines 600
  python ai_workflow.py analyze amazon_scraper --auto --dry-run
        """,
    )
    parser.add_argument(
        "command",
        choices=["new", "analyze", "archive", "project", "scraper", "parser", "debug", "docker", "review", "improve", "clean", "pipeline", "login"],
        help="Этап workflow",
    )

    parser.add_argument(
        "args",
        nargs="*",
        help="Для new: имя проекта. Для module: scraper|parser. Опционально: имя проекта.",
    )

    # Auto-send аргументы
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Автоматически отправить промпт в ChatGPT через браузер",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=AUTO_SEND_DEFAULTS["max_lines"],
        help=f"Макс. строк на часть при разбивке (по умолчанию: {AUTO_SEND_DEFAULTS['max_lines']})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать план разбивки без отправки",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Не проверять acknowledgement",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Начать заново, игнорируя предыдущий прогресс",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=AUTO_SEND_DEFAULTS["delay"],
        help=f"Задержка между частями, сек (по умолчанию: {AUTO_SEND_DEFAULTS['delay']})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=AUTO_SEND_DEFAULTS["timeout"],
        help=f"Таймаут ожидания ответа, сек (по умолчанию: {AUTO_SEND_DEFAULTS['timeout']})",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=AUTO_SEND_DEFAULTS["retries"],
        help=f"Повторные попытки при ошибке (по умолчанию: {AUTO_SEND_DEFAULTS['retries']})",
    )
    return parser


def parse_args(raw_args: list[str]) -> tuple[str, Optional[str], Optional[str], argparse.Namespace]:
    """
    Разбирает аргументы:
      new <name>
      module <scraper|parser> [project]
      <command> [project] [--auto ...]
    """
    parser = build_parser()

    # --help без команды
    if not raw_args or raw_args == ["-h"] or raw_args == ["--help"]:
        if not raw_args:
            die("Укажи команду. Пример: python ai_workflow.py analyze")
        parser.parse_args(raw_args)
        sys.exit(0)

    # Разделяем positional и optional аргументы вручную
    # потому что argparse не умеет nargs="*" + именованные args в таком виде
    positional = []
    optional = []
    i = 0
    while i < len(raw_args):
        if raw_args[i].startswith("--"):
            optional.append(raw_args[i])
            if raw_args[i] in ("--max-lines", "--delay", "--timeout", "--retries") and i + 1 < len(raw_args):
                i += 1
                optional.append(raw_args[i])
        elif raw_args[i] in ("-h",):
            optional.append(raw_args[i])
        else:
            positional.append(raw_args[i])
        i += 1

    if not positional:
        die("Укажи команду. Пример: python ai_workflow.py analyze")

    # Парсим optional
    opts = parser.parse_args(positional[:1] + optional)

    command = positional[0]
    rest = positional[1:]

    if command == "new":
        if not rest:
            die("Укажи имя проекта: python ai_workflow.py new amazon_scraper")
        return command, rest[0], None, opts

    if command == "module":
        if not rest:
            die("Укажи модуль: python ai_workflow.py module scraper")
        module_name = rest[0]
        project_name = rest[1] if len(rest) > 1 else None
        return command, project_name, module_name, opts

    project_name = rest[0] if rest else None
    return command, project_name, None, opts


def main() -> None:
    command, project_name, module_name, opts = parse_args(sys.argv[1:])

    if command == "new":
        cmd_new(project_name)  # type: ignore[arg-type]
        return

    if command == "login":
        cmd_login()
        return

    project = find_project(project_name)

    if command == "clean":
        cmd_clean(project)
        return

    if command == "pipeline":
        cmd_pipeline(project, opts)
        return

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

    # Генерируем промпт
    dispatch[command]()

    # Если --auto — автоматически отправляем в ChatGPT
    if opts.auto and command in STAGES:
        stage_info = STAGES[command]
        prompt_path = project / "AI_OUTPUT" / stage_info["prompt"]
        answer_path = project / "AI_OUTPUT" / stage_info["answer"]

        if not prompt_path.exists():
            die(f"Промпт не найден: {prompt_path}")

        auto_send_prompt(
            prompt_path=prompt_path,
            answer_path=answer_path,
            max_lines=opts.max_lines,
            delay=opts.delay,
            timeout=opts.timeout,
            retries=opts.retries,
            dry_run=opts.dry_run,
            force=opts.force,
            restart=opts.restart,
        )

        if not opts.dry_run:
            apply_answer_to_app(command, project)


if __name__ == "__main__":
    import io, os

    # Определяем папку лога: projects/<name>/ или рядом со скриптом
    _log_dir = WORKSPACE_ROOT
    for _arg in sys.argv[1:]:
        _candidate = PROJECTS_DIR / _arg
        if _candidate.is_dir():
            _log_dir = _candidate
            break

    _log_path = _log_dir / "log"
    _log_file = open(_log_path, "w", encoding="utf-8")
    print(f"[LOG] {_log_path}", file=sys.stderr, flush=True)

    class _Tee:
        def __init__(self, original, logfile):
            self._original = original
            self._logfile = logfile
        def write(self, s):
            self._original.write(s)
            self._original.flush()
            self._logfile.write(s)
            self._logfile.flush()
            return len(s)
        def flush(self):
            self._original.flush()
            self._logfile.flush()
        def fileno(self):
            return self._original.fileno()

    _orig_stdout = sys.stdout
    _orig_stderr = sys.stderr
    sys.stdout = _Tee(sys.stdout, _log_file)
    sys.stderr = _Tee(sys.stderr, _log_file)

    try:
        main()
    finally:
        sys.stdout = _orig_stdout
        sys.stderr = _orig_stderr
        _log_file.close()
