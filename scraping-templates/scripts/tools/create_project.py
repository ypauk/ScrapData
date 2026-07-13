#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание нового проекта. Используй ai_workflow.py:

    python ai_workflow.py new <project_name>
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
AI_WORKFLOW = WORKSPACE / "ai_workflow.py"


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python create_project.py <project_name>")
        print("Или:          python ai_workflow.py new <project_name>")
        sys.exit(1)

    cmd = [sys.executable, str(AI_WORKFLOW), "new", sys.argv[1]]
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
