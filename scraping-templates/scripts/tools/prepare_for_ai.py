#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Устаревший скрипт. Используй ai_workflow.py:

    python ai_workflow.py analyze [project_name]
    python ai_workflow.py project [project_name]
    python ai_workflow.py module scraper [project_name]
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
AI_WORKFLOW = WORKSPACE / "ai_workflow.py"


def main() -> None:
    print("[WARN] prepare_for_ai.py устарел. Используй: python ai_workflow.py analyze")
    cmd = [sys.executable, str(AI_WORKFLOW), "analyze"] + sys.argv[1:]
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
