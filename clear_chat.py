#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Удаляет активный чат в ChatGPT через браузер (Playwright).

Использование:
    python clear_chat.py          # удалить текущий активный чат
    python clear_chat.py --new    # удалить и открыть новый чат
"""

import sys
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent
BROWSER_PROFILE_DIR = WORKSPACE_ROOT / ".browser_profile"
CHATGPT_URL = "https://chatgpt.com/"


def launch_browser():
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


def delete_active_chat(page) -> bool:
    """
    Удаляет текущий активный чат через меню ChatGPT.
    Возвращает True если удалось.
    """
    # Вариант 1: через кебаб-меню в заголовке чата
    # Ищем кнопку "..." (options) для текущего чата в сайдбаре
    try:
        # Находим активный чат в сайдбаре (он имеет aria-current или подсветку)
        active_chat = page.locator('nav li.relative a.bg-token-sidebar-surface-secondary').first
        if not active_chat.is_visible(timeout=3000):
            # Fallback: попробуем найти по другому селектору
            active_chat = page.locator('nav ol li a[class*="bg-"]').first

        # Наводим мышь чтобы появилась кнопка меню
        active_chat.hover()
        time.sleep(0.5)

        # Кликаем кнопку "..." (три точки)
        menu_btn = page.locator('button[data-testid="history-item-three-dots"]').first
        if not menu_btn.is_visible(timeout=2000):
            menu_btn = active_chat.locator('button').last
        menu_btn.click()
        time.sleep(0.5)

        # Ищем "Delete" в выпадающем меню
        delete_btn = page.locator('[data-testid="delete-chat-menu-item"]').first
        if not delete_btn.is_visible(timeout=2000):
            delete_btn = page.get_by_role("menuitem", name="Delete")
        delete_btn.click()
        time.sleep(0.5)

        # Подтверждаем удаление
        confirm_btn = page.locator('[data-testid="delete-chat-confirm-button"]').first
        if not confirm_btn.is_visible(timeout=2000):
            confirm_btn = page.get_by_role("button", name="Delete")
        confirm_btn.click()
        time.sleep(1)

        return True

    except Exception as e:
        print(f"  [!] Метод через сайдбар не сработал: {e}")

    # Вариант 2: через горячие клавиши / keyboard shortcut
    # ChatGPT не имеет shortcut для удаления, пробуем через Settings
    return False


def main():
    open_new = "--new" in sys.argv

    print(f"\n{'=' * 50}")
    print(f"  ChatGPT — Удаление активного чата")
    print(f"{'=' * 50}\n")

    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        print("[ERROR] Playwright не установлен.")
        print("  pip install playwright && playwright install chromium")
        sys.exit(1)

    print("  Запуск браузера...")
    pw, context, page = launch_browser()

    try:
        # Проверяем что мы на ChatGPT
        current_url = page.url
        if "chat" not in current_url and "chatgpt" not in current_url:
            print("  Открываю ChatGPT...")
            page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2)

        # Проверяем что есть активный чат (URL содержит /c/)
        current_url = page.url
        if "/c/" not in current_url:
            print("  [!] Нет активного чата (уже на главной странице).")
            if open_new:
                print("  Готово — уже на странице нового чата.")
            return

        print(f"  Текущий чат: {current_url}")
        print("  Удаляю...")

        success = delete_active_chat(page)

        if success:
            print("  ✓ Чат удалён.")
            if open_new:
                time.sleep(1)
                page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=30000)
                print("  ✓ Новый чат открыт.")
        else:
            print("  ✗ Не удалось удалить автоматически.")
            print("    Удали вручную в открытом окне браузера.")
            input("    Нажми Enter когда закончишь...")

        print(f"\n{'=' * 50}")
        print(f"  DONE")
        print(f"{'=' * 50}")

    except KeyboardInterrupt:
        print("\n\n  Прервано (Ctrl+C).")
    finally:
        try:
            context.close()
            pw.stop()
        except Exception:
            pass


if __name__ == "__main__":
    main()
