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


def _find_active_chat_in_sidebar(page):
    """Ищет ссылку активного чата в сайдбаре по нескольким стратегиям."""
    selectors = [
        'nav li a[aria-current="page"]',
        'nav li a[class*="bg-token-sidebar-surface-secondary"]',
        'nav li a[class*="active"]',
        'nav ol li a[class*="bg-"]',
    ]
    for sel in selectors:
        el = page.locator(sel).first
        try:
            if el.is_visible(timeout=1500):
                print(f"    Активный чат найден по: {sel}")
                return el
        except Exception:
            continue
    return None


def _click_delete_menu_item(page):
    """Кликает 'Delete' в открытом выпадающем меню."""
    strategies = [
        lambda: page.locator('[data-testid="delete-chat-menu-item"]').first,
        lambda: page.get_by_role("menuitem", name="Delete"),
        lambda: page.get_by_role("menuitem", name="Удалить"),
        lambda: page.locator('[role="menuitem"]').filter(has_text="Delete").first,
        lambda: page.locator('[role="menuitem"]').filter(has_text="Удалить").first,
    ]
    for strategy in strategies:
        try:
            btn = strategy()
            if btn.is_visible(timeout=1500):
                btn.click()
                return True
        except Exception:
            continue
    return False


def _confirm_delete(page):
    """Подтверждает диалог удаления."""
    strategies = [
        lambda: page.locator('[data-testid="delete-chat-confirm-button"]').first,
        lambda: page.get_by_role("button", name="Delete"),
        lambda: page.get_by_role("button", name="Удалить"),
        lambda: page.locator('button').filter(has_text="Delete").last,
    ]
    for strategy in strategies:
        try:
            btn = strategy()
            if btn.is_visible(timeout=2000):
                btn.click()
                return True
        except Exception:
            continue
    return False


def delete_active_chat(page) -> bool:
    """
    Удаляет текущий активный чат через меню ChatGPT.
    Возвращает True если удалось.
    """
    # Вариант 1: через кебаб-меню активного чата в сайдбаре
    try:
        active_chat = _find_active_chat_in_sidebar(page)
        if active_chat is None:
            print("  [!] Активный чат в сайдбаре не найден, пробую через заголовок...")
        else:
            active_chat.hover()
            time.sleep(0.5)

            # Кнопка "..." рядом с чатом
            menu_btn = None
            for sel in [
                'button[data-testid="history-item-three-dots"]',
                'button[aria-label="Options"]',
                'button[aria-label="Chat options"]',
            ]:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=1500):
                        menu_btn = btn
                        print(f"    Кнопка меню найдена по: {sel}")
                        break
                except Exception:
                    continue

            if menu_btn is None:
                # Последний button внутри ссылки активного чата
                menu_btn = active_chat.locator('button').last

            menu_btn.click()
            time.sleep(0.5)

            if _click_delete_menu_item(page):
                time.sleep(0.5)
                if _confirm_delete(page):
                    time.sleep(1)
                    return True
                print("  [!] Диалог подтверждения не найден")
            else:
                print("  [!] Пункт меню Delete не найден")

    except Exception as e:
        print(f"  [!] Метод через сайдбар не сработал: {e}")

    # Вариант 2: через кнопку Options в заголовке страницы чата
    try:
        print("  Пробую через заголовок чата...")
        header_btn = None
        for sel in [
            'button[data-testid="chat-options-button"]',
            'header button[aria-label*="option" i]',
            'header button[aria-label*="Option" i]',
            'header button[aria-haspopup="menu"]',
        ]:
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=1500):
                    header_btn = btn
                    print(f"    Кнопка заголовка найдена по: {sel}")
                    break
            except Exception:
                continue

        if header_btn:
            header_btn.click()
            time.sleep(0.5)
            if _click_delete_menu_item(page):
                time.sleep(0.5)
                if _confirm_delete(page):
                    time.sleep(1)
                    return True

    except Exception as e:
        print(f"  [!] Метод через заголовок не сработал: {e}")

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
