#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для Resume Support (`app/resume_manager.py`).

Проверяют:
* отсутствие чекпоинта -> новая сессия (`reason="no_checkpoint"`);
* выключенный Resume Support (`enabled=False`) -> новая сессия,
  независимо от наличия валидного чекпоинта (`reason="disabled"`);
* успешное восстановление из валидного чекпоинта со статусом "running"
  или "failed" -> `resumed=True`, корректные `start_page`/`processed_count`/
  `exported_count`, состояние "засеяно" в переданный `CheckpointManager`;
* чекпоинт со статусом "completed" НЕ восстанавливается
  (`reason="already_completed"`) — завершённую работу не нужно продолжать;
* повреждённый чекпоинт (не JSON) -> graceful fallback на новую сессию
  (через `CheckpointManager.load()`, который уже сам возвращает None);
* неполный чекпоинт (отсутствуют обязательные поля) ->
  `reason="invalid_checkpoint"`, без исключений;
* устаревший чекпоинт (старше `RESUME_MAX_AGE_SECONDS`) ->
  `reason="expired_checkpoint"`;
* `RESUME_MAX_AGE_SECONDS=0` -> возраст чекпоинта не ограничивается;
* восстановленное состояние точно соответствует последнему
  зафиксированному чекпоинту (Duplicate Protection).

Запуск (из директории starter-project):
    python -m unittest tests.test_resume_manager
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app.checkpoint_manager import CheckpointManager
from app.resume_manager import ResumeManager


class ResumeManagerTestCase(unittest.TestCase):
    """Базовый класс: временный файл чекпоинта, удаляемый после каждого теста."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.checkpoint_file = Path(self.tmp_dir.name) / "checkpoint.json"

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def _make_checkpoint(self, **overrides) -> CheckpointManager:
        defaults = dict(
            run_id="new-run",
            enabled=True,
            file_path=self.checkpoint_file,
            interval_pages=1,
        )
        defaults.update(overrides)
        return CheckpointManager(**defaults)

    def _write_raw_checkpoint(self, **fields) -> None:
        """Пишет "сырой" JSON чекпоинта напрямую на диск (без CheckpointManager)."""
        defaults = dict(
            run_id="previous-run",
            status="running",
            current_page=3,
            current_url="https://example.com/page/3",
            processed_count=30,
            exported_count=30,
            timestamp=datetime.now(timezone.utc).isoformat(),
            extra_metadata={},
        )
        defaults.update(fields)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(defaults, f)


class TestNoCheckpoint(ResumeManagerTestCase):
    """Отсутствие чекпоинта должно приводить к новой сессии."""

    def test_no_checkpoint_starts_new_session(self):
        checkpoint = self._make_checkpoint()
        decision = ResumeManager().resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "no_checkpoint")
        self.assertEqual(decision.start_page, 0)


class TestDisabled(ResumeManagerTestCase):
    """Выключенный Resume Support должен игнорировать даже валидный чекпоинт."""

    def test_disabled_ignores_valid_checkpoint(self):
        self._write_raw_checkpoint(status="running", current_page=5)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager(enabled=False).resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "disabled")
        # Состояние CheckpointManager не должно быть изменено.
        self.assertEqual(checkpoint.state.current_page, 0)


class TestSuccessfulResume(ResumeManagerTestCase):
    """Успешное восстановление из валидного прерванного чекпоинта."""

    def test_resumes_from_running_checkpoint(self):
        self._write_raw_checkpoint(
            run_id="interrupted-run",
            status="running",
            current_page=7,
            processed_count=70,
            exported_count=65,
        )
        checkpoint = self._make_checkpoint()

        decision = ResumeManager().resume(checkpoint)

        self.assertTrue(decision.resumed)
        self.assertEqual(decision.reason, "resumed")
        self.assertEqual(decision.start_page, 7)
        self.assertEqual(decision.processed_count, 70)
        self.assertEqual(decision.exported_count, 65)

    def test_resumes_from_failed_checkpoint(self):
        self._write_raw_checkpoint(status="failed", current_page=2, processed_count=20, exported_count=20)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager().resume(checkpoint)

        self.assertTrue(decision.resumed)
        self.assertEqual(decision.start_page, 2)

    def test_seeds_checkpoint_manager_state(self):
        """Восстановленное состояние должно быть "засеяно" в CheckpointManager.state."""
        self._write_raw_checkpoint(
            run_id="interrupted-run",
            status="running",
            current_page=7,
            current_url="https://example.com/page/7",
            processed_count=70,
            exported_count=65,
            extra_metadata={"site": "example.com"},
        )
        checkpoint = self._make_checkpoint()

        ResumeManager().resume(checkpoint)

        self.assertEqual(checkpoint.state.run_id, "interrupted-run")
        self.assertEqual(checkpoint.state.status, "running")
        self.assertEqual(checkpoint.state.current_page, 7)
        self.assertEqual(checkpoint.state.current_url, "https://example.com/page/7")
        self.assertEqual(checkpoint.state.processed_count, 70)
        self.assertEqual(checkpoint.state.exported_count, 65)
        self.assertEqual(checkpoint.state.extra_metadata.get("site"), "example.com")

    def test_checkpoint_manager_continues_after_resume(self):
        """После восстановления CheckpointManager должен продолжать работать штатно."""
        self._write_raw_checkpoint(status="running", current_page=3, processed_count=30, exported_count=30)
        checkpoint = self._make_checkpoint(interval_pages=1)

        ResumeManager().resume(checkpoint)
        checkpoint.record_page(page_number=4, processed_count=40, exported_count=40)

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["current_page"], 4)
        self.assertEqual(data["processed_count"], 40)


class TestAlreadyCompleted(ResumeManagerTestCase):
    """Завершённая сессия (status=completed) не должна восстанавливаться."""

    def test_completed_checkpoint_starts_new_session(self):
        self._write_raw_checkpoint(status="completed", current_page=10)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager().resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "already_completed")
        self.assertEqual(checkpoint.state.current_page, 0)  # состояние не тронуто


class TestCorruptedCheckpoint(ResumeManagerTestCase):
    """Повреждённый (не-JSON) чекпоинт должен приводить к безопасному fallback."""

    def test_corrupted_json_starts_new_session(self):
        self.checkpoint_file.write_text("{not valid json", encoding="utf-8")
        checkpoint = self._make_checkpoint()

        decision = ResumeManager().resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "no_checkpoint")  # CheckpointManager.load() вернул None


class TestInvalidCheckpoint(ResumeManagerTestCase):
    """Чекпоинт с отсутствующими обязательными полями должен быть отклонён."""

    def test_missing_required_fields_starts_new_session(self):
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump({"status": "running"}, f)  # нет run_id, current_page, timestamp

        checkpoint = self._make_checkpoint()
        decision = ResumeManager().resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "invalid_checkpoint")

    def test_empty_run_id_starts_new_session(self):
        self._write_raw_checkpoint(run_id="")
        checkpoint = self._make_checkpoint()

        decision = ResumeManager().resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "invalid_checkpoint")

    def test_does_not_raise_on_malformed_types(self):
        self._write_raw_checkpoint(current_page="not-a-number")
        checkpoint = self._make_checkpoint()

        try:
            decision = ResumeManager().resume(checkpoint)
        except Exception as exc:  # pragma: no cover - тест должен провалиться при исключении
            self.fail(f"resume() выбросил исключение вместо graceful-обработки: {exc}")

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "invalid_checkpoint")


class TestExpiredCheckpoint(ResumeManagerTestCase):
    """Проверка ограничения "возраста" чекпоинта через RESUME_MAX_AGE_SECONDS."""

    def test_old_checkpoint_expires(self):
        old_timestamp = (datetime.now(timezone.utc) - timedelta(seconds=3600)).isoformat()
        self._write_raw_checkpoint(status="running", timestamp=old_timestamp)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager(max_age_seconds=60).resume(checkpoint)

        self.assertFalse(decision.resumed)
        self.assertEqual(decision.reason, "expired_checkpoint")

    def test_fresh_checkpoint_within_max_age_resumes(self):
        recent_timestamp = (datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat()
        self._write_raw_checkpoint(status="running", timestamp=recent_timestamp)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager(max_age_seconds=60).resume(checkpoint)

        self.assertTrue(decision.resumed)

    def test_zero_max_age_never_expires(self):
        very_old_timestamp = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat()
        self._write_raw_checkpoint(status="running", timestamp=very_old_timestamp)
        checkpoint = self._make_checkpoint()

        decision = ResumeManager(max_age_seconds=0).resume(checkpoint)

        self.assertTrue(decision.resumed)


class TestDuplicateProtection(ResumeManagerTestCase):
    """Восстановленное состояние должно точно соответствовать последнему чекпоинту."""

    def test_resumed_start_page_matches_last_checkpoint_exactly(self):
        checkpoint_a = self._make_checkpoint(interval_pages=1)
        checkpoint_a.start(status="running", site="example.com")
        for page in range(1, 6):
            checkpoint_a.record_page(page_number=page, processed_count=page * 10, exported_count=page * 10)

        # Симулируем новый процесс (перезапуск после сбоя).
        checkpoint_b = self._make_checkpoint(run_id="new-run-after-crash")
        decision = ResumeManager().resume(checkpoint_b)

        self.assertTrue(decision.resumed)
        self.assertEqual(decision.start_page, 5)
        self.assertEqual(decision.exported_count, 50)


if __name__ == "__main__":
    unittest.main()
