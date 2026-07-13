#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Створює повний дамп структури проекту.

✔ Записує ВСІ папки та підпапки.
✔ Записує ВСІ файли (крім виключених директорій).
✔ Записує повний вміст кожного файлу.
✔ Малює красиве дерево проекту.
✔ Працює з будь-якою глибиною вкладеності.
"""

from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------
# Налаштування
# ---------------------------------------------------------------------

ROOT_DIR = Path(__file__).parent.resolve()

OUTPUT_FILE = ROOT_DIR / "my_project_structure.txt"

EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "logs",
}

EXCLUDE_FILES = {
    OUTPUT_FILE.name,
}

# ---------------------------------------------------------------------


def should_skip(path: Path) -> bool:
    """
    Перевіряє чи потрібно пропустити файл або папку.
    """
    for part in path.relative_to(ROOT_DIR).parts:
        if part in EXCLUDE_DIRS:
            return True

    if path.is_file() and path.name in EXCLUDE_FILES:
        return True

    return False


# ---------------------------------------------------------------------


def get_all_files():
    """
    Повертає список всіх файлів проекту.
    """
    files = []

    for path in ROOT_DIR.rglob("*"):

        if should_skip(path):
            continue

        if path.is_file():
            files.append(path)

    return sorted(files)


# ---------------------------------------------------------------------


def write_tree(directory: Path, out, prefix=""):
    """
    Малює дерево директорій.
    """

    items = []

    for item in directory.iterdir():

        if should_skip(item):
            continue

        items.append(item)

    items.sort(key=lambda p: (p.is_file(), p.name.lower()))

    count = len(items)

    for index, item in enumerate(items):

        last = index == count - 1

        connector = "└── " if last else "├── "

        if item.is_dir():

            out.write(f"{prefix}{connector}📁 {item.name}/\n")

            extension = "    " if last else "│   "

            write_tree(item, out, prefix + extension)

        else:

            out.write(f"{prefix}{connector}📄 {item.name}\n")


# ---------------------------------------------------------------------


def dump_project():

    print("=" * 70)
    print("Створення дампу проекту...")
    print(ROOT_DIR)
    print("=" * 70)

    files = get_all_files()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        # --------------------------------------------------------------

        out.write("=" * 100 + "\n")
        out.write("ПОВНИЙ ДАМП ПРОЕКТУ\n")
        out.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        out.write("=" * 100 + "\n\n")

        # --------------------------------------------------------------

        out.write("СТРУКТУРА ПРОЕКТУ\n")
        out.write("-" * 100 + "\n\n")

        out.write(f"📁 {ROOT_DIR.name}/\n")
        write_tree(ROOT_DIR, out)

        # --------------------------------------------------------------

        out.write("\n")
        out.write("=" * 100 + "\n")
        out.write("ВМІСТ ФАЙЛІВ\n")
        out.write("=" * 100 + "\n")

        for file in files:

            rel = file.relative_to(ROOT_DIR)

            out.write("\n")
            out.write("=" * 100 + "\n")
            out.write(f"ФАЙЛ: {rel}\n")
            out.write("=" * 100 + "\n\n")

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="replace"
                )

                out.write(content)

                if not content.endswith("\n"):
                    out.write("\n")

            except Exception as e:

                out.write(f"[ПОМИЛКА ЧИТАННЯ: {e}]\n")

        # --------------------------------------------------------------

        out.write("\n")
        out.write("=" * 100 + "\n")
        out.write("СТАТИСТИКА\n")
        out.write("=" * 100 + "\n")

        out.write(f"Всього файлів : {len(files)}\n")

        extensions = {}

        for file in files:
            ext = file.suffix if file.suffix else "<без розширення>"
            extensions[ext] = extensions.get(ext, 0) + 1

        out.write("\nЗа типами:\n")

        for ext in sorted(extensions):
            out.write(f"  {ext:<20} {extensions[ext]}\n")

    print()
    print("✅ Готово!")
    print(f"Файл: {OUTPUT_FILE}")
    print(f"Файлів: {len(files)}")
    print(f"Розмір: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")


# ---------------------------------------------------------------------

if __name__ == "__main__":
    dump_project()