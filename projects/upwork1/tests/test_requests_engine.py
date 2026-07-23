#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тесты для Requests Engine (`app/requests_engine.py`).

Проверяют:
* базовое выполнение GET/POST через `requests_mock` (без реальной сети);
* автоматическое применение заголовков профиля идентичности, куки и прокси;
* делегирование задержек Delay Manager (`SessionManager.wait_before_request`);
* обертку сетевых сбоев в `RequestsEngineError`;
* `get_json()`/`get_text()`/`download_file()`;
* интеграцию с Proxy Manager (report_proxy_success/report_proxy_failure).

Запуск (из директории starter-project):
    python -m unittest tests.test_requests_engine
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app.proxy_manager import EnvProxyProvider, ProxyManager
from app.requests_engine import RequestsEngine, RequestsEngineError


class RequestsEngineTestCase(unittest.TestCase):
    """Базовый класс: чистое состояние Proxy Manager между тестами."""

    def setUp(self) -> None:
        self._orig_provider = ProxyManager.get_provider()
        ProxyManager.set_provider(EnvProxyProvider())  # без прокси по умолчанию в тестах

    def tearDown(self) -> None:
        ProxyManager.set_provider(self._orig_provider)


class TestBasicRequests(RequestsEngineTestCase):
    """Проверка базового выполнения GET/POST без реальной сети."""

    @patch("app.session_manager.DelayManager.wait")  # без реальных пауз в тестах
    def test_get_returns_response(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = engine.get("https://example.com")

            self.assertEqual(response.status_code, 200)
            mock_request.assert_called_once()
            self.assertEqual(mock_request.call_args.kwargs["method"], "GET")
            self.assertEqual(mock_request.call_args.kwargs["url"], "https://example.com")
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_post_passes_json_body(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            engine.post("https://example.com/api", json={"key": "value"})

            self.assertEqual(mock_request.call_args.kwargs["method"], "POST")
            self.assertEqual(mock_request.call_args.kwargs["json"], {"key": "value"})
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_wait_before_request_is_called(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            engine.get("https://example.com")

            mock_wait.assert_called_once()
        engine.close()


class TestResponseHandling(RequestsEngineTestCase):
    """Проверка get_json()/get_text()."""

    @patch("app.session_manager.DelayManager.wait")
    def test_get_json_decodes_valid_json(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_response._content = b'{"a": 1}'
            mock_request.return_value = mock_response

            result = engine.get_json("https://example.com/api")
            self.assertEqual(result, {"a": 1})
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_get_json_returns_none_on_invalid_json(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_response._content = b"not-json"
            mock_request.return_value = mock_response

            result = engine.get_json("https://example.com/api")
            self.assertIsNone(result)
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_get_text_returns_decoded_body(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_response._content = b"hello world"
            mock_request.return_value = mock_response

            result = engine.get_text("https://example.com")
            self.assertEqual(result, "hello world")
        engine.close()


class TestErrorHandling(RequestsEngineTestCase):
    """Проверка обертки сетевых сбоев в RequestsEngineError."""

    @patch("app.session_manager.DelayManager.wait")
    def test_connection_error_raises_engine_error(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError("boom")

            with self.assertRaises(RequestsEngineError):
                engine.get("https://example.com")
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_timeout_raises_engine_error(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("timed out")

            with self.assertRaises(RequestsEngineError):
                engine.get("https://example.com")
        engine.close()


class TestProxyIntegration(RequestsEngineTestCase):
    """Проверка, что Requests Engine сообщает Proxy Manager об исходе запроса."""

    @patch("app.session_manager.DelayManager.wait")
    def test_success_reports_proxy_success(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request, \
             patch.object(ProxyManager, "report_proxy_success") as mock_success, \
             patch.object(ProxyManager, "report_proxy_failure") as mock_failure:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            engine.get("https://example.com")

            mock_success.assert_called_once()
            mock_failure.assert_not_called()
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_server_error_reports_proxy_failure(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request, \
             patch.object(ProxyManager, "report_proxy_success") as mock_success, \
             patch.object(ProxyManager, "report_proxy_failure") as mock_failure:
            mock_response = requests.Response()
            mock_response.status_code = 503
            mock_request.return_value = mock_response

            engine.get("https://example.com")

            mock_failure.assert_called_once()
            mock_success.assert_not_called()
        engine.close()

    @patch("app.session_manager.DelayManager.wait")
    def test_network_error_reports_proxy_failure(self, mock_wait):
        engine = RequestsEngine()
        with patch.object(engine.session, "request") as mock_request, \
             patch.object(ProxyManager, "report_proxy_failure") as mock_failure:
            mock_request.side_effect = requests.exceptions.ConnectionError("boom")

            with self.assertRaises(RequestsEngineError):
                engine.get("https://example.com")

            mock_failure.assert_called_once()
        engine.close()


class TestDownloadFile(RequestsEngineTestCase):
    """Проверка download_file() — потокового скачивания в файл."""

    @patch("app.session_manager.DelayManager.wait")
    def test_download_file_writes_content(self, mock_wait):
        engine = RequestsEngine()
        destination = Path(__file__).parent / "_tmp_download_test.bin"
        try:
            with patch.object(engine.session, "request") as mock_request:
                mock_response = requests.Response()
                mock_response.status_code = 200
                mock_response._content = b"binary-data"
                mock_response._content_consumed = True  # iter_content() отдаст _content без обращения к response.raw
                mock_request.return_value = mock_response

                result_path = engine.download_file("https://example.com/file.bin", destination)

                self.assertEqual(result_path, destination)
                self.assertTrue(destination.exists())
                self.assertEqual(destination.read_bytes(), b"binary-data")
        finally:
            if destination.exists():
                destination.unlink()
            engine.close()


class TestContextManager(RequestsEngineTestCase):
    """Проверка использования RequestsEngine как контекстного менеджера."""

    def test_context_manager_closes_session(self):
        with RequestsEngine() as engine:
            self.assertIsNotNone(engine.session)
        # После выхода из блока сессия должна быть закрыта без исключений.


if __name__ == "__main__":
    unittest.main()
