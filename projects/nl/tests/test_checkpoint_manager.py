#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit-тесты для Checkpoint Manager (`app/checkpoint_manager.py`).

Проверяют:
* создание первичного чекпоинта при `start()` независимо от интервалов;
* срабатывание/несрабатывание сохранения по интервалу страниц/записей/времени;
* принудительное сохранение (`save_now()`, `finish()`);
* атомарность записи (никогда не остается частично записанного/повреждённого
  файла — временный файл не подменяет целевой при сбое);
* политику "timestamped" (дополнительная копия с суффиксом-таймстампом);
* graceful-обработку сбоев записи (никогда не бросает исключение наружу);
* `CheckpointManager.load()` для чтения сохранённого чекпоинта;
* отключение через `enabled=False` (no-op, обратная совместимость).

Запуск (из директории starter-project):
    python -m unittest tests.test_checkpoint_manager
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent.resolve()))  # добавляет starter-project в sys.path

from app.checkpoint_manager import CheckpointManager


class CheckpointManagerTestCase(unittest.TestCase):
    """Базовый класс: временный файл чекпоинта, удаляемый после каждого теста."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.checkpoint_file = Path(self.tmp_dir.name) / "checkpoint.json"

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def _make_manager(self, **overrides) -> CheckpointManager:
        defaults = dict(
            run_id="test-run",
            enabled=True,
            file_path=self.checkpoint_file,
            interval_pages=1,
            interval_records=0,
            interval_seconds=0,
            overwrite_policy="overwrite",
        )
        defaults.update(overrides)
        return CheckpointManager(**defaults)


class TestStartAndFinish(CheckpointManagerTestCase):
    """Проверка гарантированного сохранения на старте/финише независимо от интервалов."""

    def test_start_creates_checkpoint_immediately(self):
        manager = self._make_manager(interval_pages=100)  # заведомо не сработает сам по себе
        manager.start(status="running")

        self.assertTrue(self.checkpoint_file.exists())
        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["status"], "running")
        self.assertEqual(data["run_id"], "test-run")

    def test_finish_forces_save_regardless_of_interval(self):
        manager = self._make_manager(interval_pages=100)
        manager.start(status="running")
        manager.finish(status="completed")

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["status"], "completed")

    def test_extra_metadata_is_preserved(self):
        manager = self._make_manager()
        manager.start(status="running", site="example.com")

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["extra_metadata"]["site"], "example.com")


class TestIntervalPages(CheckpointManagerTestCase):
    """Проверка условия сохранения по количеству обработанных страниц."""

    def test_saves_when_page_interval_reached(self):
        manager = self._make_manager(interval_pages=2)
        manager.start(status="running")  # чекпоинт #1 (force)

        saved_1 = manager.record_page(page_number=1, processed_count=10)
        self.assertFalse(saved_1)  # 1 страница с последнего сохранения < interval_pages=2

        saved_2 = manager.record_page(page_number=2, processed_count=20)
        self.assertTrue(saved_2)  # 2 страницы с последнего сохранения >= interval_pages=2

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["current_page"], 2)
        self.assertEqual(data["processed_count"], 20)

    def test_disabled_page_interval_never_triggers_on_its_own(self):
        manager = self._make_manager(interval_pages=0, interval_records=0, interval_seconds=0)
        manager.start(status="running")

        saved = manager.record_page(page_number=1, processed_count=10)
        self.assertFalse(saved)


class TestIntervalRecords(CheckpointManagerTestCase):
    """Проверка условия сохранения по количеству обработанных записей."""

    def test_saves_when_record_interval_reached(self):
        manager = self._make_manager(interval_pages=0, interval_records=50)
        manager.start(status="running")

        self.assertFalse(manager.record_records(processed_count=30))
        self.assertTrue(manager.record_records(processed_count=60))

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["processed_count"], 60)


class TestIntervalSeconds(CheckpointManagerTestCase):
    """Проверка ограничения по минимальному времени между чекпоинтами."""

    def test_time_interval_blocks_frequent_saves(self):
        manager = self._make_manager(interval_pages=1, interval_seconds=9999)
        manager.start(status="running")  # force save устанавливает _last_saved_monotonic

        # interval_pages=1 сработал бы сам по себе, но interval_seconds
        # блокирует, так как прошло намного меньше 9999 секунд.
        saved = manager.record_page(page_number=1, processed_count=1)
        self.assertFalse(saved)

    def test_manual_save_ignores_time_interval(self):
        manager = self._make_manager(interval_seconds=9999)
        manager.start(status="running")

        saved = manager.save_now(note="manual checkpoint")
        self.assertTrue(saved)

        data = CheckpointManager.load(self.checkpoint_file)
        self.assertEqual(data["extra_metadata"]["note"], "manual checkpoint")


class TestDisabled(CheckpointManagerTestCase):
    """Проверка no-op поведения при выключенном Checkpoint Manager."""

    def test_disabled_never_writes_file(self):
        manager = self._make_manager(enabled=False, interval_pages=1)
        manager.start(status="running")
        manager.record_page(page_number=1, processed_count=10)
        manager.finish(status="completed")

        self.assertFalse(self.checkpoint_file.exists())

    def test_disabled_save_now_returns_false(self):
        manager = self._make_manager(enabled=False)
        self.assertFalse(manager.save_now())


class TestOverwritePolicy(CheckpointManagerTestCase):
    """Проверка политик хранения файлов чекпоинта: overwrite vs timestamped."""

    def test_overwrite_policy_keeps_single_file(self):
        manager = self._make_manager(overwrite_policy="overwrite", interval_pages=1)
        manager.start(status="running")
        manager.record_page(page_number=1, processed_count=1)
        manager.record_page(page_number=2, processed_count=2)

        files = list(self.checkpoint_file.parent.glob("checkpoint*.json"))
        self.assertEqual(len(files), 1)

    def test_timestamped_policy_creates_additional_files(self):
        manager = self._make_manager(overwrite_policy="timestamped", interval_pages=1)
        manager.start(status="running")
        manager.record_page(page_number=1, processed_count=1)

        # Основной файл + минимум одна timestamped-копия
        self.assertTrue(self.checkpoint_file.exists())
        timestamped_files = [
            f for f in self.checkpoint_file.parent.glob(f"{self.checkpoint_file.stem}_*.json")
        ]
        self.assertGreaterEqual(len(timestamped_files), 1)


class TestLoad(CheckpointManagerTestCase):
    """Проверка `CheckpointManager.load()` для несуществующих/повреждённых файлов."""

    def test_load_returns_none_when_file_missing(self):
        missing_path = Path(self.tmp_dir.name) / "does_not_exist.json"
        self.assertIsNone(CheckpointManager.load(missing_path))

    def test_load_returns_none_on_corrupted_json(self):
        self.checkpoint_file.write_text("{not valid json", encoding="utf-8")
        self.assertIsNone(CheckpointManager.load(self.checkpoint_file))

    def test_load_returns_none_on_empty_file(self):
        self.checkpoint_file.write_text("", encoding="utf-8")
        self.assertIsNone(CheckpointManager.load(self.checkpoint_file))


class TestErrorHandling(CheckpointManagerTestCase):
    """Проверка, что сбой записи чекпоинта логируется, но не бросает исключение."""

    def test_write_failure_does_not_raise(self):
        manager = self._make_manager()

        with patch.object(CheckpointManager, "_atomic_write", side_effect=OSError("disk full")):
            try:
                result = manager.save_now()
            except Exception as exc:  # pragma: no cover - тест должен провалиться, если исключение поднято
                self.fail(f"save_now() выбросил исключение вместо graceful-обработки: {exc}")

        self.assertFalse(result)

    def test_previous_checkpoint_survives_failed_write(self):
        manager = self._make_manager()
        manager.start(status="running")  # первый валидный чекпоинт на диске

        with patch.object(CheckpointManager, "_atomic_write", side_effect=OSError("disk full")):
            manager.record_page(page_number=1, processed_count=1)

        # Старый валидный чекпоинт должен остаться нетронутым.
        data = CheckpointManager.load(self.checkpoint_file)
        self.assertIsNotNone(data)
        self.assertEqual(data["status"], "running")


class TestTotalSaves(CheckpointManagerTestCase):
    """Проверка счётчика фактически выполненных записей на диск."""

    def test_total_saves_counts_only_actual_writes(self):
        manager = self._make_manager(interval_pages=2)
        manager.start(status="running")  # save #1 (force)

        manager.record_page(page_number=1, processed_count=1)  # не сохраняет (1 < 2)
        manager.record_page(page_number=2, processed_count=2)  # save #2

        manager.finish(status="completed")  # save #3 (force)

        self.assertEqual(manager.total_saves, 3)


if __name__ == "__main__":
    unittest.main()
