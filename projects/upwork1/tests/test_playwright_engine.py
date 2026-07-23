#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для Playwright Engine (`app/playwright_engine.py`).

Проверяют (без реального запуска браузера, через мокирование
`app.playwright_engine.sync_playwright` и `get_browser_context`):
* запуск/закрытие браузера (start/close, контекстный менеджер);
* делегирование создания контекста в `app.browser.get_browser_context()`
  с примененными идентичностью/куки/прокси;
* делегирование пауз Delay Manager (`SessionManager.wait_before_request`);
* обертку сбоев навигации в `PlaywrightEngineError`;
* интеграцию с Proxy Manager (report_proxy_success/report_proxy_failure);
* интеграцию с Cookie Manager (update_cookies/save_cookies).

Запуск (из директории starter-project):
    python -m unittest tests.test_playwright_engine
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from playwright.sync_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError

from app.proxy_manager import EnvProxyProvider, ProxyManager
from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError


def _make_mock_context():
    """Строит мок BrowserContext/Browser/Page, достаточный для тестов движка."""
    mock_page = MagicMock()
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_context.browser = mock_browser
    mock_context.new_page.return_value = mock_page
    mock_context.cookies.return_value = []
    return mock_context, mock_browser, mock_page


class PlaywrightEngineTestCase(unittest.TestCase):
    """Базовый класс: чистое состояние Proxy Manager и мок sync_playwright между тестами."""

    def setUp(self) -> None:
        self._orig_provider = ProxyManager.get_provider()
        ProxyManager.set_provider(EnvProxyProvider())  # без прокси по умолчанию в тестах

        self.mock_context, self.mock_browser, self.mock_page = _make_mock_context()

        self._sync_playwright_patcher = patch("app.playwright_engine.sync_playwright")
        mock_sync_playwright = self._sync_playwright_patcher.start()
        mock_sync_playwright.return_value.start.return_value = MagicMock()

        self._get_browser_context_patcher = patch("app.playwright_engine.get_browser_context")
        self.mock_get_browser_context = self._get_browser_context_patcher.start()
        self.mock_get_browser_context.return_value = self.mock_context

        self._save_cookies_patcher = patch("app.playwright_engine.CookieManager.save")
        self.mock_save_cookies = self._save_cookies_patcher.start()

        self._update_cookies_patcher = patch("app.playwright_engine.CookieManager.update")
        self.mock_update_cookies = self._update_cookies_patcher.start()

    def tearDown(self) -> None:
        ProxyManager.set_provider(self._orig_provider)
        self._sync_playwright_patcher.stop()
        self._get_browser_context_patcher.stop()
        self._save_cookies_patcher.stop()
        self._update_cookies_patcher.stop()


class TestLifecycle(PlaywrightEngineTestCase):
    """Проверка запуска/закрытия браузера."""

    def test_start_creates_context_via_get_browser_context(self):
        engine = PlaywrightEngine()
        engine.start()

        self.mock_get_browser_context.assert_called_once()
        self.assertIs(engine.context, self.mock_context)
        engine.close()

    def test_context_manager_starts_and_closes(self):
        with PlaywrightEngine() as engine:
            self.assertIs(engine.context, self.mock_context)

        self.mock_context.close.assert_called_once()
        self.mock_browser.close.assert_called_once()

    def test_close_saves_cookies(self):
        with PlaywrightEngine():
            pass
        self.mock_save_cookies.assert_called_once()

    def test_start_launch_failure_raises_engine_error(self):
        self.mock_get_browser_context.side_effect = RuntimeError("boom")
        engine = PlaywrightEngine()
        with self.assertRaises(PlaywrightEngineError):
            engine.start()


class TestNavigation(PlaywrightEngineTestCase):
    """Проверка goto() и делегирования Delay Manager/Proxy Manager."""

    @patch("app.playwright_engine.SessionManager.wait_before_request")
    def test_goto_calls_wait_before_request(self, mock_wait):
        with PlaywrightEngine() as engine:
            engine.goto("https://example.com")
            mock_wait.assert_called_once()

    @patch("app.playwright_engine.SessionManager.wait_before_request")
    def test_goto_reports_proxy_success(self, mock_wait):
        with patch.object(ProxyManager, "report_proxy_success") as mock_success, \
             patch.object(ProxyManager, "report_proxy_failure") as mock_failure:
            with PlaywrightEngine() as engine:
                engine.goto("https://example.com")

            mock_success.assert_called_once()
            mock_failure.assert_not_called()

    @patch("app.playwright_engine.SessionManager.wait_before_request")
    def test_goto_timeout_reports_proxy_failure_and_raises(self, mock_wait):
        self.mock_page.goto.side_effect = PlaywrightTimeoutError("timed out")
        with patch.object(ProxyManager, "report_proxy_failure") as mock_failure:
            with PlaywrightEngine() as engine:
                with self.assertRaises(PlaywrightEngineError):
                    engine.goto("https://example.com")
                mock_failure.assert_called_once()

    @patch("app.playwright_engine.SessionManager.wait_before_request")
    def test_goto_navigation_error_raises_engine_error(self, mock_wait):
        self.mock_page.goto.side_effect = PlaywrightError("navigation failed")
        with PlaywrightEngine() as engine:
            with self.assertRaises(PlaywrightEngineError):
                engine.goto("https://example.com")

    @patch("app.playwright_engine.SessionManager.wait_before_request")
    def test_goto_updates_cookies(self, mock_wait):
        with PlaywrightEngine() as engine:
            engine.goto("https://example.com")
            self.mock_update_cookies.assert_called_once()


class TestPageOperations(PlaywrightEngineTestCase):
    """Проверка content()/evaluate()/wait_for_selector()."""

    def test_content_returns_page_html(self):
        self.mock_page.content.return_value = "<html></html>"
        with PlaywrightEngine() as engine:
            self.assertEqual(engine.content(), "<html></html>")

    def test_evaluate_delegates_to_page(self):
        self.mock_page.evaluate.return_value = 42
        with PlaywrightEngine() as engine:
            result = engine.evaluate("() => 42")
            self.assertEqual(result, 42)
            self.mock_page.evaluate.assert_called_once_with("() => 42")

    def test_wait_for_selector_raises_engine_error_on_timeout(self):
        self.mock_page.wait_for_selector.side_effect = PlaywrightTimeoutError("not found")
        with PlaywrightEngine() as engine:
            with self.assertRaises(PlaywrightEngineError):
                engine.wait_for_selector(".missing")


class TestUsageWithoutStart(unittest.TestCase):
    """Проверка защиты от использования контекста без start()."""

    def test_context_without_start_raises(self):
        engine = PlaywrightEngine()
        with self.assertRaises(PlaywrightEngineError):
            _ = engine.context


if __name__ == "__main__":
    unittest.main()
