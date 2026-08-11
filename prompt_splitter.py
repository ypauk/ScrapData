#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разбивает большие промпты на части для бесплатных ИИ.
Режим --auto автоматически отправляет части в ChatGPT через Playwright.

Использование:
    python prompt_splitter.py                         # разбить последний промпт
    python prompt_splitter.py projects/my/AI_OUTPUT/03_scraper_prompt.md
    python prompt_splitter.py --max-lines 150        # свой лимит строк на часть
    python prompt_splitter.py --save                 # сохранить части в файлы
    python prompt_splitter.py --auto                 # автоотправка в ChatGPT
    python prompt_splitter.py --auto --dry-run       # показать план без отправки
    python prompt_splitter.py --auto --restart       # начать заново
    python prompt_splitter.py --auto --force         # не проверять acknowledgement
"""

import sys
import re
import subprocess
import json
import hashlib
import time
from pathlib import Path
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Конфигурация
# ---------------------------------------------------------------------------

MAX_LINES_PER_PART = 800
DEFAULT_RESPONSE_TIMEOUT = 300
DEFAULT_DELAY = 2
DEFAULT_RETRIES = 3
WORKSPACE_ROOT = Path(__file__).resolve().parent
PROJECTS_DIR = WORKSPACE_ROOT / "projects"
BROWSER_PROFILE_DIR = WORKSPACE_ROOT / ".browser_profile"
STATE_FILE = WORKSPACE_ROOT / ".prompt_splitter_state.json"
CHATGPT_URL = "https://chatgpt.com/"

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
# Утилиты
# ---------------------------------------------------------------------------


def die(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


def calculate_file_hash(filepath: Path) -> str:
    content = filepath.read_bytes()
    return hashlib.sha256(content).hexdigest()


def get_answer_path(prompt_path: Path) -> Optional[Path]:
    """
    Определяет путь answer-файла по имени prompt-файла.
    01_analysis_prompt.md  → 01_analysis_answer.md
    02_project_prompt.md   → 02_project_answer.md
    03_scraper_prompt.md   → 03_scraper_answer.py
    04_parser_prompt.md    → 04_parser_answer.py
    """
    name = prompt_path.stem  # e.g. "03_scraper_prompt"

    if "_prompt" not in name:
        return None

    base = name.replace("_prompt", "_answer")

    # Код-этапы получают .py, остальные .md
    code_stages = ("03_scraper", "04_parser")
    ext = ".py" if any(base.startswith(s) for s in code_stages) else ".md"

    return prompt_path.parent / (base + ext)


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


# ---------------------------------------------------------------------------
# State management (resume)
# ---------------------------------------------------------------------------


def load_state() -> Optional[dict]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def save_state(file: str, file_hash: str, total_parts: int, last_completed_part: int) -> None:
    state = {
        "file": file,
        "file_hash": file_hash,
        "total_parts": total_parts,
        "last_completed_part": last_completed_part,
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def clear_state() -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()


# ---------------------------------------------------------------------------
# Browser automation (Playwright)
# ---------------------------------------------------------------------------


def check_playwright_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        return False


def launch_browser():
    """Запускает Chromium с persistent profile. Возвращает (playwright, context, page)."""
    from playwright.sync_api import sync_playwright

    BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    pw = sync_playwright().start()
    context = pw.chromium.launch_persistent_context(
        user_data_dir=str(BROWSER_PROFILE_DIR),
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 900},
    )
    page = context.pages[0] if context.pages else context.new_page()
    return pw, context, page


def open_chatgpt(page) -> None:
    """Открывает ChatGPT."""
    page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2000)


def find_chat_input(page, timeout: int = 30000):
    """
    Находит composer ChatGPT через DOM с fallback-селекторами.
    Возвращает Playwright locator.
    """
    selectors = [
        '#prompt-textarea',
        'div[contenteditable="true"][id="prompt-textarea"]',
        'div[contenteditable="true"][data-placeholder]',
        'textarea[data-id="root"]',
        'div.ProseMirror[contenteditable="true"]',
        '[contenteditable="true"]',
    ]

    for selector in selectors:
        try:
            locator = page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout // len(selectors))
            return locator
        except Exception:
            continue

    die(f"Composer не найден. Убедитесь, что ChatGPT открыт и загружен.")


def send_message(page, text: str, retries: int = 1) -> None:
    """
    Отправляет сообщение в ChatGPT:
    1. Находит composer
    2. Вставляет текст через clipboard
    3. Нажимает Send
    """
    for attempt in range(retries):
        try:
            composer = find_chat_input(page)

            composer.click()
            page.wait_for_timeout(300)

            # Вставка через clipboard (быстро, без посимвольного ввода)
            page.evaluate("""(text) => {
                const el = document.querySelector('#prompt-textarea') ||
                           document.querySelector('[contenteditable="true"]');
                if (el) {
                    el.focus();
                    // Для contenteditable div
                    if (el.contentEditable === 'true') {
                        el.innerHTML = '';
                        const p = document.createElement('p');
                        p.textContent = text;
                        el.appendChild(p);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    } else {
                        // Для textarea
                        el.value = text;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            }""", text)

            page.wait_for_timeout(500)

            # Нажать Send
            send_clicked = _click_send_button(page)
            if not send_clicked:
                # Fallback: Enter
                composer.press("Enter")

            page.wait_for_timeout(1000)
            return

        except Exception as e:
            if attempt < retries - 1:
                print(f"    Retry отправки ({attempt + 1}/{retries}): {e}")
                page.wait_for_timeout(2000)
            else:
                raise RuntimeError(f"Не удалось отправить сообщение: {e}")


def _click_send_button(page) -> bool:
    """Пытается кликнуть кнопку Send."""
    selectors = [
        'button[data-testid="send-button"]',
        'button[aria-label="Send prompt"]',
        'button[aria-label="Отправить запрос"]',
        'button[class*="send"]',
        'form button[type="submit"]',
    ]
    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=1000):
                btn.click()
                return True
        except Exception:
            continue
    return False


def wait_for_response_complete(page, timeout: int = DEFAULT_RESPONSE_TIMEOUT) -> None:
    """
    Ждёт завершения генерации ответа ChatGPT.
    Определяет по исчезновению кнопки Stop / появлению кнопки Send.
    """
    deadline = time.time() + timeout

    # Ждём начала генерации (появление Stop или streaming)
    page.wait_for_timeout(2000)

    stop_selectors = [
        'button[aria-label="Stop generating"]',
        'button[aria-label="Остановить генерацию"]',
        'button[data-testid="stop-button"]',
        'button[class*="stop"]',
    ]

    # Ждём исчезновения Stop generating
    while time.time() < deadline:
        stop_visible = False
        for selector in stop_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible(timeout=500):
                    stop_visible = True
                    break
            except Exception:
                continue

        if not stop_visible:
            # Проверяем что composer снова доступен (ответ завершён)
            try:
                composer = find_chat_input(page, timeout=3000)
                if composer.is_visible():
                    page.wait_for_timeout(1000)
                    return
            except Exception:
                pass

        page.wait_for_timeout(1000)

    raise TimeoutError(f"Таймаут {timeout}с: ответ ChatGPT не завершился.")


def get_last_response(page) -> str:
    """Получает текст последнего ответа ChatGPT."""
    try:
        # ChatGPT messages are in article or div[data-message-author-role]
        selectors = [
            'div[data-message-author-role="assistant"]',
            'article div.markdown',
            'div.agent-turn div.markdown',
            '[data-testid="conversation-turn"] div.markdown',
        ]
        for selector in selectors:
            elements = page.locator(selector)
            count = elements.count()
            if count > 0:
                last = elements.nth(count - 1)
                text = last.inner_text(timeout=5000)
                if text.strip():
                    return text.strip()
        return ""
    except Exception:
        return ""


def verify_acknowledgement(response_text: str, part_number: int) -> bool:
    """
    Проверяет, что ChatGPT подтвердил получение части.
    Допускает вариации.
    """
    text_lower = response_text.lower()

    patterns = [
        f"часть {part_number} принята",
        f"часть {part_number}",
        "принята",
        "жду следующую",
        "жду",
        f"part {part_number}",
        "received",
        "waiting",
    ]

    matches = sum(1 for p in patterns if p in text_lower)
    return matches >= 2


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


def mode_auto(
    parts: List[str],
    prompt_path: Path,
    file_hash: str,
    dry_run: bool = False,
    force: bool = False,
    restart: bool = False,
    delay: int = DEFAULT_DELAY,
    timeout: int = DEFAULT_RESPONSE_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> None:
    """Автоматическая отправка частей в ChatGPT через Playwright."""
    total = len(parts)

    # --- Header ---
    print(f"\n{'=' * 60}")
    print(f"  ChatGPT Auto Sender")
    print(f"{'=' * 60}")
    print(f"\n  File: {prompt_path.name}")
    print(f"  Lines: {sum(p.count(chr(10)) + 1 for p in parts)}")
    print(f"  Parts: {total}")
    print(f"\n  Browser: Chromium")
    print(f"  Profile: {BROWSER_PROFILE_DIR.relative_to(WORKSPACE_ROOT)}")
    print()

    # --- Check Playwright ---
    if not check_playwright_available():
        die(
            "Playwright не установлен.\n"
            "  Установка:\n"
            "    pip install playwright\n"
            "    playwright install chromium"
        )

    # --- Resume state ---
    start_part = 0
    if not restart:
        state = load_state()
        if state and state.get("file") == str(prompt_path):
            if state.get("file_hash") != file_hash:
                print("  WARNING: Исходный prompt изменился после предыдущего запуска.")
                print("  Начинаем заново.\n")
                clear_state()
            elif state.get("last_completed_part", 0) > 0:
                completed = state["last_completed_part"]
                print(f"  Обнаружен предыдущий прогресс:")
                print(f"  {completed}/{total} частей завершено.\n")
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
        answer_path = get_answer_path(prompt_path)
        if answer_path:
            print(f"\n  Ответ будет сохранён в: {answer_path.name}")
        print("\n  Playwright: OK")
        print("  Сообщения НЕ будут отправлены.")
        print(f"\n{'=' * 60}")
        return

    # --- Launch browser ---
    print("  Запуск браузера...")
    pw, context, page = launch_browser()

    try:
        # --- Open ChatGPT ---
        print("  Открываю ChatGPT...")
        open_chatgpt(page)

        print(f"\n{'=' * 60}")
        print("  ChatGPT готов.")
        print("  Открой нужный чат или создай новый.")
        input("  Нажми Enter для начала автоматической отправки...")
        print(f"{'=' * 60}\n")

        # --- Send parts ---
        for i in range(start_part, total):
            part_num = i + 1
            is_last = (i == total - 1)

            if is_last:
                print(f"  [{part_num}/{total}] Sending final task...")
            else:
                print(f"  [{part_num}/{total}] Sending...")

            try:
                send_message(page, parts[i], retries=retries)
            except RuntimeError as e:
                print(f"\n  [ERROR] Не удалось отправить часть {part_num}/{total}.")
                print(f"  Причина: {e}")
                print()
                while True:
                    action = input("  [R] Retry / [A] Abort: ").strip().upper()
                    if action == "R":
                        try:
                            send_message(page, parts[i], retries=retries)
                            break
                        except RuntimeError as e2:
                            print(f"  [ERROR] Повторная ошибка: {e2}")
                    elif action == "A":
                        print("  Прервано. Браузер оставлен открытым.")
                        save_state(str(prompt_path), file_hash, total, i)
                        return
                    else:
                        print("  Введи R или A.")

            # Wait for response
            print(f"  [{part_num}/{total}] Waiting for response...")
            try:
                wait_for_response_complete(page, timeout=timeout)
            except TimeoutError as e:
                print(f"  [ERROR] {e}")
                while True:
                    action = input("  [R] Retry wait / [A] Abort: ").strip().upper()
                    if action == "R":
                        try:
                            wait_for_response_complete(page, timeout=timeout)
                            break
                        except TimeoutError as e2:
                            print(f"  [ERROR] {e2}")
                    elif action == "A":
                        save_state(str(prompt_path), file_hash, total, i)
                        return

            # Verify acknowledgement (only for non-last parts)
            if not is_last:
                response_text = get_last_response(page)
                ack_ok = verify_acknowledgement(response_text, part_num)

                if ack_ok:
                    print(f"  [{part_num}/{total}] Acknowledgement ✓")
                elif force:
                    print(f"  [{part_num}/{total}] Acknowledgement ? (--force, продолжаем)")
                else:
                    print(f"\n  WARNING: Неожиданный ответ ChatGPT после части {part_num}.")
                    if response_text:
                        preview = response_text[:200]
                        print(f"  Ответ: {preview}")
                    print()
                    answer = input("  Продолжить? [y/N] ").strip().lower()
                    if answer not in ("y", "yes", "д", "да"):
                        save_state(str(prompt_path), file_hash, total, i)
                        print("  Прервано. Браузер оставлен открытым.")
                        return
            else:
                print(f"  [{part_num}/{total}] Response completed ✓")

            # Save progress
            save_state(str(prompt_path), file_hash, total, part_num)

            # Delay between parts
            if not is_last and i < total - 1:
                time.sleep(delay)

            print()

        # --- Save final answer ---
        answer_path = get_answer_path(prompt_path)
        if answer_path:
            print("  Сохраняю финальный ответ...")
            final_response = get_last_response(page)
            if final_response:
                answer_path.write_text(final_response, encoding="utf-8")
                print(f"  ✓ Ответ сохранён: {answer_path.name}")
                print(f"    Путь: {answer_path}")
            else:
                print("  ✗ Не удалось получить текст ответа из браузера.")
                print("    Скопируй ответ вручную из открытого окна ChatGPT.")
        else:
            print("  Файл не соответствует паттерну NN_*_prompt.* — ответ не сохранён автоматически.")
            print("  Скопируй ответ вручную из открытого окна ChatGPT.")

        # --- Done ---
        clear_state()
        print(f"\n{'=' * 60}")
        print(f"  DONE")
        print(f"{'=' * 60}")

    except KeyboardInterrupt:
        print("\n\n  Прервано пользователем (Ctrl+C).")
        print("  Браузер оставлен открытым.")
    finally:
        # Не закрываем browser — пользователь может хотеть продолжить вручную
        pass


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
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Автоматическая отправка в ChatGPT через браузер"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать план без отправки (только с --auto)"
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Начать заново, игнорируя предыдущий прогресс"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Не проверять acknowledgement от ChatGPT"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=DEFAULT_DELAY,
        help=f"Задержка между частями в секундах (по умолчанию: {DEFAULT_DELAY})"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_RESPONSE_TIMEOUT,
        help=f"Таймаут ожидания ответа в секундах (по умолчанию: {DEFAULT_RESPONSE_TIMEOUT})"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help=f"Количество повторных попыток при ошибке (по умолчанию: {DEFAULT_RETRIES})"
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
    if total_lines <= args.max_lines and not args.auto:
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

    # Режим работы
    if args.auto:
        file_hash = calculate_file_hash(prompt_path)
        mode_auto(
            parts=wrapped,
            prompt_path=prompt_path,
            file_hash=file_hash,
            dry_run=args.dry_run,
            force=args.force,
            restart=args.restart,
            delay=args.delay,
            timeout=args.timeout,
            retries=args.retries,
        )
    elif args.save:
        output_dir = prompt_path.parent / f"{prompt_path.stem}_parts"
        mode_save_files(wrapped, output_dir)
    else:
        mode_interactive(wrapped)


if __name__ == "__main__":
    main()
