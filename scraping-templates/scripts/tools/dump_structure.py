#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

# Скрипт лежит в ...\scraping-templates\scripts\tools\
# Нам нужно подняться на 3 уровня вверх, чтобы попасть в UPWORK-ALL\
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Целевой файл
OUTPUT_FILE = ROOT_DIR / "starter-project" / "PROJECT_STRUCTURE.md"

# Папки, которые нужно игнорировать
EXCLUDE_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", ".pytest_cache", 
    ".mypy_cache", ".ruff_cache", ".venv", "venv", "env", 
    "node_modules", "dist", "build", "logs"
}

def write_tree(directory, out, prefix=""):
    """Рекурсивно рисует структуру папок."""
    try:
        items = sorted(
            [item for item in directory.iterdir() if item.name not in EXCLUDE_DIRS], 
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        return

    for index, item in enumerate(items):
        last = index == len(items) - 1
        connector = "└── " if last else "├── "
        
        if item.is_dir():
            out.write(f"{prefix}{connector}📁 {item.name}/\n")
            write_tree(item, out, prefix + ("    " if last else "│   "))
        else:
            out.write(f"{prefix}{connector}📄 {item.name}\n")

def dump_structure():
    # Создаем папку, если её нет
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"# Структура проекта: {ROOT_DIR.name}\n\n")
        out.write("```text\n")
        out.write(f"{ROOT_DIR.name}/\n")
        write_tree(ROOT_DIR, out)
        out.write("```\n")
    
    print(f"✅ Структура успешно создана:")
    print(f"   {OUTPUT_FILE}")

if __name__ == "__main__":
    dump_structure()