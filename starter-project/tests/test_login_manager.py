#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для Login Support (app/login_manager.py).

Все тесты используют мокированные RequestsEngine/PlaywrightEngine и
requests.Session — без реальных сетевых запросов/браузера, так как
Login Manager полностью engine-независим (принимает готовый движок).
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.login_manager import (
    ApiKeyStrategy,
    AuthCredentials,
    AuthResult,
    BearerTokenStrategy,
    CookieSessionStrategy,
    LoginDetector,
    LoginError,
    LoginManager,
    PlaywrightFormLoginStrategy,
    RequestsFormLoginStrategy,
)


class TestLoginDetector(unittest.TestCase):
    """Тесты переиспользуемой логики обнаружения ситуаций логина."""

    def test_is_unauthorized(self):
        self.assertTrue(LoginDetector.is_unauthorized(401))
        self.assertTrue(LoginDetector.is_unauthorized(403))
        self.assertFalse(LoginDetector.is_unauthorized(200))

    def test_was_redirected_to_login(self):
        self.assertTrue(LoginDetector.was_redirected_to_login(
            "https://example.com/login/", "https://example.com/login"
        ))
        self.assertFalse(LoginDetector.was_redirected_to_login(
            "https://example.com/dashboard", "https://example.com/login"
        ))
        self.assertFalse(LoginDetector.was_redirected_to_login("", "https://example.com/login"))

    def test_contains_login_form(self):
        self.assertTrue(LoginDetector.contains_login_form('<input type="password" name="pw">'))
        self.assertTrue(LoginDetector.contains_login_form("<input type='password'>"))
        self.assertFalse(LoginDetector.contains_login_form("<div>Welcome back!</div>"))
        self.assertFalse(LoginDetector.contains_login_form(""))

    def test_contains_captcha(self):
        self.assertTrue(LoginDetector.contains_captcha("<div>Please complete the CAPTCHA</div>"))
        self.assertTrue(LoginDetector.contains_captcha("g-recaptcha-response"))
        self.assertFalse(LoginDetector.contains_captcha("<div>Welcome back!</div>"))
        self.assertFalse(LoginDetector.contains_captcha(""))


class TestRequestsFormLoginStrategy(unittest.TestCase):
    """Тесты аутентификации через HTML-форму на базе RequestsEngine."""

    def _make_engine(self, status_code=200, text="<html>dashboard</html>"):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.text = text

        mock_engine = MagicMock()
        mock_engine.post.return_value = mock_response
        mock_engine.session.cookies = []
        return mock_engine, mock_response

    def test_successful_login_returns_success(self):
        engine, _ = self._make_engine(status_code=200, text="<html>Welcome, user!</html>")
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        result = strategy.authenticate(AuthCredentials(username="user", password="pass"))

        self.assertTrue(result.success)
        engine.post.assert_called_once()
        _, kwargs = engine.post.call_args
        self.assertEqual(kwargs["data"]["username"], "user")
        self.assertEqual(kwargs["data"]["password"], "pass")

    def test_unauthorized_status_returns_invalid_credentials(self):
        engine, _ = self._make_engine(status_code=401)
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        result = strategy.authenticate(AuthCredentials(username="user", password="wrong"))

        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_login_form_still_present_means_failure(self):
        engine, _ = self._make_engine(status_code=200, text='<input type="password">')
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        result = strategy.authenticate(AuthCredentials(username="user", password="wrong"))

        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_captcha_detected(self):
        engine, _ = self._make_engine(status_code=200, text="<div>Please solve the CAPTCHA</div>")
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        result = strategy.authenticate(AuthCredentials(username="user", password="pass"))

        self.assertFalse(result.success)
        self.assertEqual(result.reason, "captcha_detected")

    def test_custom_success_check_used(self):
        engine, _ = self._make_engine(status_code=200, text="<html>ok</html>")
        strategy = RequestsFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            success_check=lambda response: False,
        )

        result = strategy.authenticate(AuthCredentials(username="user", password="pass"))
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_custom_failure_check_used(self):
        engine, _ = self._make_engine(status_code=200, text="<html>Invalid password</html>")
        strategy = RequestsFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            failure_check=lambda response: "Invalid password" in response.text,
        )

        result = strategy.authenticate(AuthCredentials(username="user", password="wrong"))
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_engine_error_raises_login_error(self):
        from app.requests_engine import RequestsEngineError

        engine = MagicMock()
        engine.post.side_effect = RequestsEngineError("network down")
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        with self.assertRaises(LoginError) as ctx:
            strategy.authenticate(AuthCredentials(username="user", password="pass"))
        self.assertEqual(ctx.exception.reason, "timeout")

    @patch("app.login_manager.CookieManager.update")
    def test_cookies_persisted_on_success(self, mock_update):
        engine, _ = self._make_engine(status_code=200, text="<html>Welcome!</html>")
        strategy = RequestsFormLoginStrategy(engine=engine, login_url="https://example.com/login")

        strategy.authenticate(AuthCredentials(username="user", password="pass"))

        mock_update.assert_called_once()


class TestPlaywrightFormLoginStrategy(unittest.TestCase):
    """Тесты аутентификации через форму логина на базе PlaywrightEngine."""

    def _make_engine(self, content="<html>dashboard</html>"):
        mock_page = MagicMock()
        mock_engine = MagicMock()
        mock_engine.page = mock_page
        mock_engine.content.return_value = content
        return mock_engine, mock_page

    def test_successful_login(self):
        engine, page = self._make_engine(content="<html>Welcome back</html>")
        page.wait_for_selector.side_effect = Exception("no failure selector present")

        strategy = PlaywrightFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            username_selector="#user",
            password_selector="#pass",
            submit_selector="#submit",
            failure_selector=".error",
        )

        result = strategy.authenticate(AuthCredentials(username="user", password="pass"))

        self.assertTrue(result.success)
        engine.goto.assert_called_once_with("https://example.com/login")
        page.fill.assert_any_call("#user", "user")
        page.fill.assert_any_call("#pass", "pass")
        page.click.assert_called_once_with("#submit")

    def test_failure_selector_present_means_failure(self):
        engine, page = self._make_engine(content="<html>error</html>")
        page.wait_for_selector.return_value = MagicMock()  # найден -> ошибка логина

        strategy = PlaywrightFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            username_selector="#user",
            password_selector="#pass",
            submit_selector="#submit",
            failure_selector=".error",
        )

        result = strategy.authenticate(AuthCredentials(username="user", password="wrong"))
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_navigation_failure_raises_login_error(self):
        from app.playwright_engine import PlaywrightEngineError

        engine, _ = self._make_engine()
        engine.goto.side_effect = PlaywrightEngineError("timed out")

        strategy = PlaywrightFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            username_selector="#user",
            password_selector="#pass",
            submit_selector="#submit",
        )

        with self.assertRaises(LoginError) as ctx:
            strategy.authenticate(AuthCredentials(username="user", password="pass"))
        self.assertEqual(ctx.exception.reason, "timeout")

    def test_cookies_updated_on_success(self):
        engine, page = self._make_engine(content="<html>Welcome back</html>")
        page.wait_for_selector.side_effect = Exception("no failure selector")

        strategy = PlaywrightFormLoginStrategy(
            engine=engine,
            login_url="https://example.com/login",
            username_selector="#user",
            password_selector="#pass",
            submit_selector="#submit",
        )

        strategy.authenticate(AuthCredentials(username="user", password="pass"))
        engine.update_cookies.assert_called_once()


class TestCookieSessionStrategy(unittest.TestCase):
    """Тесты восстановления сессии из сохраненных куки."""

    @patch("app.login_manager.CookieManager.load")
    def test_no_cookies_means_expired(self, mock_load):
        mock_load.return_value = []
        strategy = CookieSessionStrategy()

        result = strategy.authenticate(AuthCredentials())
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "expired_session")

    @patch("app.login_manager.CookieManager.load")
    def test_cookies_present_means_success(self, mock_load):
        mock_load.return_value = [{"name": "session_id", "value": "abc"}]
        strategy = CookieSessionStrategy()

        result = strategy.authenticate(AuthCredentials())
        self.assertTrue(result.success)

    @patch("app.login_manager.CookieManager.load")
    def test_custom_validate_callback_used(self, mock_load):
        mock_load.return_value = [{"name": "session_id", "value": "abc"}]
        strategy = CookieSessionStrategy(validate=lambda: False)

        result = strategy.authenticate(AuthCredentials())
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "expired_session")


class TestBearerTokenStrategy(unittest.TestCase):
    """Тесты аутентификации через Bearer Token."""

    def test_token_applied_to_session_headers(self):
        session = MagicMock()
        session.headers = {}
        strategy = BearerTokenStrategy(session=session)

        result = strategy.authenticate(AuthCredentials(token="abc123"))

        self.assertTrue(result.success)
        self.assertEqual(session.headers["Authorization"], "Bearer abc123")

    def test_missing_token_fails(self):
        session = MagicMock()
        session.headers = {}
        strategy = BearerTokenStrategy(session=session)

        result = strategy.authenticate(AuthCredentials())
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")

    def test_custom_header_name(self):
        session = MagicMock()
        session.headers = {}
        strategy = BearerTokenStrategy(session=session, header_name="X-Custom-Auth")

        strategy.authenticate(AuthCredentials(token="xyz"))
        self.assertEqual(session.headers["X-Custom-Auth"], "Bearer xyz")


class TestApiKeyStrategy(unittest.TestCase):
    """Тесты аутентификации через статический API Key."""

    def test_api_key_applied_to_session_headers(self):
        session = MagicMock()
        session.headers = {}
        strategy = ApiKeyStrategy(session=session)

        result = strategy.authenticate(AuthCredentials(api_key="my-key"))

        self.assertTrue(result.success)
        self.assertEqual(session.headers["X-API-Key"], "my-key")

    def test_missing_api_key_fails(self):
        session = MagicMock()
        session.headers = {}
        strategy = ApiKeyStrategy(session=session)

        result = strategy.authenticate(AuthCredentials())
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "invalid_credentials")


class TestLoginManager(unittest.TestCase):
    """Тесты оркестрации LoginManager (повторы, переиспользование сессий)."""

    def setUp(self):
        LoginManager.reset()

    def tearDown(self):
        LoginManager.reset()

    def test_successful_login_marks_session_authenticated(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        result = LoginManager.login(strategy, AuthCredentials(username="u", password="p"), session_id="job-1")

        self.assertTrue(result.success)
        self.assertTrue(LoginManager.is_session_authenticated("job-1"))

    def test_invalid_credentials_not_retried(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=False, reason="invalid_credentials")

        result = LoginManager.login(strategy, AuthCredentials(username="u", password="wrong"), max_attempts=3)

        self.assertFalse(result.success)
        self.assertEqual(strategy.authenticate.call_count, 1)

    def test_transient_login_error_is_retried(self):
        strategy = MagicMock()
        strategy.authenticate.side_effect = [
            LoginError("timeout", reason="timeout"),
            AuthResult(success=True),
        ]

        result = LoginManager.login(strategy, AuthCredentials(username="u", password="p"), max_attempts=3)

        self.assertTrue(result.success)
        self.assertEqual(strategy.authenticate.call_count, 2)

    def test_captcha_error_not_retried(self):
        strategy = MagicMock()
        strategy.authenticate.side_effect = LoginError("captcha", reason="captcha_detected")

        result = LoginManager.login(strategy, AuthCredentials(username="u", password="p"), max_attempts=3)

        self.assertFalse(result.success)
        self.assertEqual(result.reason, "captcha_detected")
        self.assertEqual(strategy.authenticate.call_count, 1)

    def test_all_attempts_exhausted_returns_last_result(self):
        strategy = MagicMock()
        strategy.authenticate.side_effect = LoginError("timeout", reason="timeout")

        result = LoginManager.login(strategy, AuthCredentials(username="u", password="p"), max_attempts=2)

        self.assertFalse(result.success)
        self.assertEqual(result.reason, "timeout")
        self.assertEqual(strategy.authenticate.call_count, 2)

    def test_ensure_login_reuses_authenticated_session(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        LoginManager.login(strategy, session_id="job-2")
        strategy.authenticate.reset_mock()

        result = LoginManager.ensure_login(strategy, session_id="job-2")

        self.assertTrue(result.success)
        strategy.authenticate.assert_not_called()

    def test_ensure_login_performs_login_when_not_authenticated(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        result = LoginManager.ensure_login(strategy, session_id="job-3")

        self.assertTrue(result.success)
        strategy.authenticate.assert_called_once()

    def test_session_lifetime_expiration(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        with patch("app.login_manager.config.LOGIN_SESSION_LIFETIME_SECONDS", 0.01):
            LoginManager.login(strategy, session_id="job-4")
            self.assertTrue(LoginManager.is_session_authenticated("job-4"))

            import time
            time.sleep(0.02)

            self.assertFalse(LoginManager.is_session_authenticated("job-4"))

    def test_invalidate_session(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        LoginManager.login(strategy, session_id="job-5")
        self.assertTrue(LoginManager.is_session_authenticated("job-5"))

        LoginManager.invalidate_session("job-5")
        self.assertFalse(LoginManager.is_session_authenticated("job-5"))

    def test_no_session_id_does_not_track_authentication(self):
        strategy = MagicMock()
        strategy.authenticate.return_value = AuthResult(success=True)

        result = LoginManager.login(strategy)
        self.assertTrue(result.success)
        self.assertIsNone(result.session_id)


if __name__ == "__main__":
    unittest.main()
