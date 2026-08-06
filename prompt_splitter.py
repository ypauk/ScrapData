#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разбивает большие промпты на части для бесплатных ИИ.

Использование:
    python prompt_splitter.py                         # разбить последний промпт
    python prompt_splitter.py projects/my/AI_OUTPUT/03_scraper_prompt.md
    python prompt_splitter.py --max-lines 150        # свой лимит строк на часть

Как работает:
    1. Берёт большой промпт (5000+ строк)
    2. Разбивает по смысловым секциям (по заголовкам #)
    3. Группирует секции в части по лимиту строк
    4. Добавляет обёртки ("запомни контекст" / "теперь задача")
    5. Копирует части по очереди в буфер обмена (Enter между частями)
"""

import sys
import re
import subprocess
from pathlib import Path
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Настройки
# ---------------------------------------------------------------------------

MAX_LINES_PER_PART = 200
WORKSPACE_ROOT = Path(__file__).resolve().parent
PROJECTS_DIR = WORKSPACE_ROOT / "projects"

# ---------------------------------------------------------------------------
# Обёртки для частей
# ---------------------------------------------------------------------------

WRAPPER_FIRST = """ВАЖНО: Я буду отправлять тебе контекст проекта по частям.
Это часть {current} из {total}.
Запомни всю информацию ниже. НЕ отвечай и НЕ генерируй код пока не получишь последнюю часть с задачей.
Ответь ТОЛЬКО: "Часть {current} принята. Жду следующую."

---

{content}"""

WRAPPER_MIDDLE = """Это часть {current} из {total}. Продолжение контекста.
Запомни. НЕ отвечай и НЕ генерируй код.
Ответь ТОЛЬКО: "Часть {current} принята. Жду следующую."

---

{content}"""

WRAPPER_LAST = """Это последняя часть ({current} из {total}).
Весь контекст получен. ТЕПЕРЬ выполни задачу.

---

{content}"""

WRAPPER_SINGLE = """{content}"""

# ---------------------------------------------------------------------------
# Логика разбивки
# ---------------------------------------------------------------------------


def find_latest_prompt() -> Path:
    """Находит последний сгенерированный промпт в projects/."""
    if not PROJECTS_DIR.exists():
        die("Папка projects/ не найдена")

    prompts = []
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        ai_output = project_dir / "AI_OUTPUT"
        if not ai_output.exists():
            continue
        for f in ai_output.glob("*_prompt.md"):
            prompts.append(f)

    if not prompts:
        die("Промпты не найдены в projects/*/AI_OUTPUT/")

    return max(prompts, key=lambda p: p.stat().st_mtime)


def split_by_sections(text: str) -> List[Tuple[str, str]]:
    """
    Разбивает текст по заголовкам Markdown (# или ---).
    Возвращает список (заголовок, содержимое).
    """
    lines = text.split("\n")
    sections = []
    current_title = ""
    current_lines = []

    for line in lines:
        if re.match(r"^#{1,3}\s+", line) or line.strip() == "---":
            if current_lines:
                sections.append((current_title, "\n".join(current_lines)))
            current_title = line.strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines)))

    return sections


def group_sections(sections: List[Tuple[str, str]], max_lines: int) -> List[str]:
    """
    Группирует секции в части, не превышая max_lines.
    Не разрывает секцию пополам.
    """
    parts = []
    current_part_lines = []
    current_count = 0

    for title, content in sections:
        section_lines = content.count("\n") + 1

        if section_lines > max_lines:
            if current_part_lines:
                parts.append("\n".join(current_part_lines))
                current_part_lines = []
                current_count = 0

            chunk_lines = content.split("\n")
            for i in range(0, len(chunk_lines), max_lines):
                chunk = "\n".join(chunk_lines[i:i + max_lines])
                parts.append(chunk)
        elif current_count + section_lines > max_lines and current_part_lines:
            parts.append("\n".join(current_part_lines))
            current_part_lines = [content]
            current_count = section_lines
        else:
            current_part_lines.append(content)
            current_count += section_lines

    if current_part_lines:
        parts.append("\n".join(current_part_lines))

    return parts


def wrap_parts(parts: List[str]) -> List[str]:
    """Добавляет обёртки к каждой части."""
    total = len(parts)

    if total == 1:
        return [WRAPPER_SINGLE.format(content=parts[0])]

    wrapped = []
    for i, part in enumerate(parts, start=1):
        if i == 1:
            template = WRAPPER_FIRST
        elif i == total:
            template = WRAPPER_LAST
        else:
            template = WRAPPER_MIDDLE

        wrapped.append(template.format(current=i, total=total, content=part))

    return wrapped


def copy_to_clipboard(text: str) -> bool:
    """Копирует текст в буфер обмена (Windows)."""
    try:
        process = subprocess.Popen(
            ["clip"],
            stdin=subprocess.PIPE,
            shell=True
        )
        process.communicate(text.encode("utf-16le"))
        return True
    except Exception:
        return False


def die(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Режимы работы
# ---------------------------------------------------------------------------


def mode_interactive(parts: List[str]) -> None:
    """Интерактивный режим: копирует части по одной."""
    total = len(parts)

    print(f"\n{'=' * 60}")
    print(f"  Промпт разбит на {total} частей")
    print(f"{'=' * 60}")
    print(f"\n  Инструкция:")
    print(f"  1. Нажми Enter → часть скопируется в буфер")
    print(f"  2. Вставь в чат ИИ (Ctrl+V)")
    print(f"  3. Дождись ответа 'Часть N принята'")
    print(f"  4. Нажми Enter → следующая часть")
    print(f"  5. Последняя часть содержит задачу — ИИ начнёт работать")
    print()

    for i, part in enumerate(parts, start=1):
        lines_count = part.count("\n") + 1
        chars_count = len(part)

        if i < total:
            label = f"  [Часть {i}/{total}] Контекст ({lines_count} строк, {chars_count} символов)"
        else:
            label = f"  [Часть {i}/{total}] ЗАДАЧА ({lines_count} строк, {chars_count} символов)"

        print(label)
        input("  → Нажми Enter чтобы скопировать...")

        if copy_to_clipboard(part):
            print(f"  ✓ Скопировано в буфер. Вставляй в чат (Ctrl+V).")
        else:
            print(f"  ✗ Не удалось скопировать. Файл сохранён (см. ниже).")

        print()

    print(f"{'=' * 60}")
    print(f"  Готово! Все {total} частей отправлены.")
    print(f"{'=' * 60}")


def mode_save_files(parts: List[str], output_dir: Path) -> None:
    """Сохраняет части в файлы (если clipboard не работает)."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, part in enumerate(parts, start=1):
        filename = f"part_{i:02d}_of_{len(parts):02d}.md"
        filepath = output_dir / filename
        filepath.write_text(part, encoding="utf-8")

    print(f"\n  Части сохранены в: {output_dir}")
    print(f"  Файлов: {len(parts)}")
    print(f"\n  Отправляй в чат по порядку:")
    for i in range(1, len(parts) + 1):
        filename = f"part_{i:02d}_of_{len(parts):02d}.md"
        print(f"    {i}. {filename}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Разбивает большие промпты для бесплатных ИИ"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Путь к промпту (если не указан — берёт последний из projects/)"
    )
    parser.add_argument(
        "--max-lines", "-m",
        type=int,
        default=MAX_LINES_PER_PART,
        help=f"Максимум строк на часть (по умолчанию: {MAX_LINES_PER_PART})"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Сохранить части в файлы вместо копирования в буфер"
    )

    args = parser.parse_args()

    # Определяем файл
    if args.file:
        prompt_path = Path(args.file)
        if not prompt_path.exists():
            prompt_path = WORKSPACE_ROOT / args.file
        if not prompt_path.exists():
            die(f"Файл не найден: {args.file}")
    else:
        prompt_path = find_latest_prompt()

    print(f"\n  Файл: {prompt_path.name}")
    print(f"  Путь: {prompt_path}")

    # Читаем
    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    total_lines = text.count("\n") + 1
    print(f"  Строк: {total_lines}")
    print(f"  Символов: {len(text)}")

    # Проверяем нужна ли разбивка
    if total_lines <= args.max_lines:
        print(f"\n  Промпт короткий ({total_lines} строк) — разбивка не нужна.")
        print(f"  Копирую целиком...")
        if copy_to_clipboard(text):
            print(f"  ✓ Скопировано в буфер.")
        else:
            print(f"  ✗ Не удалось скопировать.")
        return

    # Разбиваем
    sections = split_by_sections(text)
    parts = group_sections(sections, args.max_lines)
    wrapped = wrap_parts(parts)

    print(f"  Частей: {len(wrapped)}")
    print(f"  Лимит: {args.max_lines} строк/часть")

    # Выводим
    if args.save:
        output_dir = prompt_path.parent / f"{prompt_path.stem}_parts"
        mode_save_files(wrapped, output_dir)
    else:
        mode_interactive(wrapped)


if __name__ == "__main__":
    main()
