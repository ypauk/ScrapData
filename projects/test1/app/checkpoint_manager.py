#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Checkpoint Manager.

Централизованный компонент, отвечающий ТОЛЬКО за периодическое
сохранение прогресса скрапинга на диск (см. `framework/ROADMAP.md`,
Milestone 6, и `tasks/TASK.md`).

Checkpoint Manager:

* записывает текущий прогресс (номер страницы, URL, количество
  обработанных/экспортированных записей, статус, метаданные) в JSON-файл;
* решает, КОГДА нужно создать новый чекпоинт, на основе настраиваемых
  условий (число страниц / число записей / прошедшее время / ручной запрос);
* безопасно перезаписывает файл чекпоинта (запись во временный файл +
  атомарная замена), чтобы никогда не оставить частично записанный файл;
* предоставляет статический `load()` для будущего Resume Support —
  сам Checkpoint Manager чекпоинты НЕ читает и НЕ использует для
  восстановления, это ответственность отдельного будущего компонента.

Checkpoint Manager НЕ выполняет HTTP-запросы, НЕ парсит HTML/JSON, НЕ
экспортирует записи и НЕ знает о селекторах/логике конкретного сайта —
он полностью независим от scraper-специфичного кода (см. `app/scraper.py`,
`app/pagination.py`, `app/exporter.py`), что позволяет использовать его
в любом скрапере фреймворка без изменений.

Пример использования (см. интеграцию в `app/main.py::_run_incremental()`):

    from app.checkpoint_manager import CheckpointManager

    checkpoint = CheckpointManager(run_id="olx_cars_2024")
    checkpoint.start(status="running")

    for page_number, html in enumerate(raw_pages_content, 1):
        records = parse_listing(html)
        batch_writer.add_records(records)

        # save() решает сам, нужно ли реально писать на диск в этот
        # момент, основываясь на CHECKPOINT_INTERVAL_PAGES/RECORDS/SECONDS
        checkpoint.record_page(
            page_number=page_number,
            url=None,
            processed_count=len(records),
            exported_count=batch_writer.total_flushed,
        )

    checkpoint.finish(status="completed")
"""

import json
import os
import tempfile
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.config import (
    CHECKPOINT_ENABLED,
    CHECKPOINT_FILE,
    CHECKPOINT_INTERVAL_PAGES,
    CHECKPOINT_INTERVAL_RECORDS,
    CHECKPOINT_INTERVAL_SECONDS,
    CHECKPOINT_OVERWRITE_POLICY,
)
from app.utils import log_message


@dataclass
class CheckpointState:
    """
    Снимок прогресса скрапинга на момент создания чекпоинта.

    架构 намеренно оставляет дверь открытой для новых полей: любой
    дополнительный параметр, переданный через `extra_metadata`,
    сохраняется как есть в результирующем JSON без изменения структуры
    класса — старые чекпоинты остаются читаемыми (совместимость вперед).

    Атрибуты:
        run_id (str): Идентификатор конкретного запуска скрапинга
            (позволяет различать чекпоинты разных запусков/заказов).
        status (str): Текущий статус ("running", "completed", "failed").
        current_page (int): Номер последней обработанной страницы.
        current_url (str, optional): URL последней обработанной страницы.
        processed_count (int): Общее количество обработанных (спарсенных) записей.
        exported_count (int): Общее количество записей, реально сброшенных
            на диск (например, через BatchWriter.total_flushed).
        timestamp (str): ISO 8601 UTC-таймстамп момента создания чекпоинта.
        extra_metadata (dict): Произвольные дополнительные поля
            (например, имя сайта, параметры запуска) — расширяемость
            без изменения схемы.
    """

    run_id: str
    status: str = "running"
    current_page: int = 0
    current_url: Optional[str] = None
    processed_count: int = 0
    exported_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует состояние в словарь, готовый для json.dump()."""
        return asdict(self)


class CheckpointManager:
    """
    Отвечает за принятие решения "нужно ли сохранять чекпоинт сейчас" и
    за безопасную запись результата на диск.

    Не хранит зависимостей от scraper-специфичного кода — принимает
    только простые значения (номер страницы, URL, счётчики) через
    `record_page()`/`record_records()`, вызываемые из цикла скрапинга.
    """

    def __init__(
        self,
        run_id: str,
        *,
        enabled: Optional[bool] = None,
        file_path: Optional[Path] = None,
        interval_pages: Optional[int] = None,
        interval_records: Optional[int] = None,
        interval_seconds: Optional[float] = None,
        overwrite_policy: Optional[str] = None,
    ) -> None:
        """
        Args:
            run_id: Идентификатор запуска (используется в самом
                чекпоинте и в имени timestamped-файлов).
            enabled: Включает/выключает создание чекпоинтов.
                По умолчанию — config.CHECKPOINT_ENABLED.
            file_path: Путь к файлу чекпоинта.
                По умолчанию — config.CHECKPOINT_FILE.
            interval_pages: Раз в сколько страниц сохранять чекпоинт.
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_PAGES.
            interval_records: Раз в сколько записей сохранять чекпоинт.
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_RECORDS.
            interval_seconds: Минимальный интервал между чекпоинтами (сек).
                0 — не учитывать. По умолчанию — config.CHECKPOINT_INTERVAL_SECONDS.
            overwrite_policy: "overwrite" или "timestamped".
                По умолчанию — config.CHECKPOINT_OVERWRITE_POLICY.
        """
        self.run_id = run_id
        self.enabled = enabled if enabled is not None else CHECKPOINT_ENABLED
        self.file_path = Path(file_path) if file_path is not None else CHECKPOINT_FILE
        self.interval_pages = interval_pages if interval_pages is not None else CHECKPOINT_INTERVAL_PAGES
        self.interval_records = interval_records if interval_records is not None else CHECKPOINT_INTERVAL_RECORDS
        self.interval_seconds = interval_seconds if interval_seconds is not None else CHECKPOINT_INTERVAL_SECONDS
        self.overwrite_policy = (overwrite_policy or CHECKPOINT_OVERWRITE_POLICY).strip().lower()

        self._state = CheckpointState(run_id=run_id)
        self._last_saved_page = 0
        self._last_saved_records = 0
        self._last_saved_monotonic: Optional[float] = None
        self._total_saves = 0

        if self.enabled:
            log_message(
                "info",
                f"CheckpointManager: инициализирован (run_id={run_id}, "
                f"file={self.file_path.name}, policy={self.overwrite_policy})",
            )

    # =====================================================================
    # ПУБЛИЧНОЕ API
    # =====================================================================

    def start(self, status: str = "running", **extra_metadata: Any) -> None:
        """
        Отмечает начало скрапинга и сразу сохраняет первичный чекпоинт
        (независимо от интервалов) — гарантирует, что файл чекпоинта
        существует с самого начала запуска, а не только после первого
        сработавшего интервала.

        Args:
            status: Начальный статус (по умолчанию "running").
            **extra_metadata: Произвольные дополнительные поля
                (например, source_url="...", site="olx").
        """
        self._state.status = status
        self._state.extra_metadata.update(extra_metadata)
        self._save(force=True)

    def record_page(
        self,
        page_number: int,
        *,
        url: Optional[str] = None,
        processed_count: Optional[int] = None,
        exported_count: Optional[int] = None,
        **extra_metadata: Any,
    ) -> bool:
        """
        Обновляет прогресс после обработки очередной страницы и
        сохраняет чекпоинт, если сработало хотя бы одно из условий
        интервала (страницы/записи/время).

        Args:
            page_number: Номер обработанной страницы (текущий прогресс).
            url: URL обработанной страницы (опционально).
            processed_count: Текущее суммарное количество обработанных записей.
            exported_count: Текущее суммарное количество экспортированных записей.
            **extra_metadata: Дополнительные поля, объединяются с уже
                накопленными (перезапись по ключу).

        Returns:
            bool: True, если чекпоинт был реально записан на диск.
        """
        self._state.current_page = page_number
        if url is not None:
            self._state.current_url = url
        if processed_count is not None:
            self._state.processed_count = processed_count
        if exported_count is not None:
            self._state.exported_count = exported_count
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)

        pages_since_save = page_number - self._last_saved_page
        should_save = self.interval_pages > 0 and pages_since_save >= self.interval_pages

        return self._maybe_save(should_save)

    def record_records(self, processed_count: int, *, exported_count: Optional[int] = None) -> bool:
        """
        Обновляет счётчики записей независимо от страниц и сохраняет
        чекпоинт, если сработало условие интервала по записям (или по
        времени — оно проверяется всегда в `_maybe_save`).

        Args:
            processed_count: Текущее суммарное количество обработанных записей.
            exported_count: Текущее суммарное количество экспортированных записей.

        Returns:
            bool: True, если чекпоинт был реально записан на диск.
        """
        self._state.processed_count = processed_count
        if exported_count is not None:
            self._state.exported_count = exported_count

        records_since_save = processed_count - self._last_saved_records
        should_save = self.interval_records > 0 and records_since_save >= self.interval_records

        return self._maybe_save(should_save)

    def save_now(self, **extra_metadata: Any) -> bool:
        """
        Принудительно сохраняет чекпоинт немедленно, игнорируя все
        интервалы (ручной запрос — см. TASK.md "manual checkpoint requests").

        Returns:
            bool: True, если чекпоинт был записан (False только при
                CHECKPOINT_ENABLED=False или сбое записи).
        """
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)
        return self._save(force=True)

    def finish(self, status: str = "completed", **extra_metadata: Any) -> bool:
        """
        Отмечает завершение скрапинга (успешное или с ошибкой) и
        принудительно сохраняет финальный чекпоинт независимо от
        интервалов — гарантирует, что последнее состояние всегда
        зафиксировано на диске.

        Args:
            status: Финальный статус ("completed" или "failed").
            **extra_metadata: Дополнительные поля для финального чекпоинта.

        Returns:
            bool: True, если чекпоинт был записан.
        """
        self._state.status = status
        if extra_metadata:
            self._state.extra_metadata.update(extra_metadata)
        return self._save(force=True)

    @property
    def state(self) -> CheckpointState:
        """Текущее состояние прогресса (для инспекции/тестов)."""
        return self._state

    @property
    def total_saves(self) -> int:
        """Общее количество реально выполненных записей чекпоинта на диск."""
        return self._total_saves

    # =====================================================================
    # ЗАГРУЗКА ЧЕКПОИНТА (для будущего Resume Support)
    # =====================================================================

    @staticmethod
    def load(file_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """
        Читает последний сохранённый чекпоинт с диска.

        Checkpoint Manager сам эти данные никогда не использует — метод
        предоставлен исключительно для будущего Resume Support, чтобы
        тот не реализовывал собственный механизм отслеживания прогресса
        (см. `tasks/TASK.md`, раздел "Integration").

        Args:
            file_path: Путь к файлу чекпоинта. По умолчанию — config.CHECKPOINT_FILE.

        Returns:
            dict, optional: Содержимое чекпоинта, либо None, если файл
                отсутствует, пуст или повреждён.
        """
        path = Path(file_path) if file_path is not None else CHECKPOINT_FILE
        if not path.exists() or path.stat().st_size == 0:
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_message("error", f"CheckpointManager: не удалось загрузить чекпоинт {path.name}: {e}")
            return None

    # =====================================================================
    # ВНУТРЕННЯЯ ЛОГИКА
    # =====================================================================

    def _maybe_save(self, should_save: bool) -> bool:
        """
        Проверяет условие по времени (оно всегда учитывается как
        дополнительное ограничение сверху условий pages/records — не
        даёт сохранять чекпоинты слишком часто) и выполняет сохранение,
        если хотя бы одно из условий (переданное `should_save` ИЛИ
        отсутствие ограничения по времени) выполнено.
        """
        if not should_save:
            return False

        if self.interval_seconds > 0 and self._last_saved_monotonic is not None:
            elapsed = time.monotonic() - self._last_saved_monotonic
            if elapsed < self.interval_seconds:
                return False

        return self._save(force=False)

    def _save(self, *, force: bool) -> bool:
        """
        Выполняет фактическую запись чекпоинта на диск, если
        `self.enabled`. При `overwrite_policy == "timestamped"`
        дополнительно сохраняет копию с суффиксом-таймстампом.

        Запись выполняется через временный файл в той же директории +
        `os.replace()` (атомарная операция на POSIX и Windows) — исключает
        ситуацию, когда процесс прерывается посреди записи и оставляет
        частично записанный/повреждённый JSON-файл чекпоинта.

        Args:
            force: Если True — запись выполняется независимо от
                состояния интервалов (используется start()/finish()/save_now()).

        Returns:
            bool: True при успешной записи, False если чекпоинт
                отключен либо запись завершилась ошибкой.
        """
        if not self.enabled:
            return False

        self._state.timestamp = datetime.now(timezone.utc).isoformat()
        payload = self._state.to_dict()

        try:
            self._atomic_write(self.file_path, payload)

            if self.overwrite_policy == "timestamped":
                ts_suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
                timestamped_path = self.file_path.with_name(
                    f"{self.file_path.stem}_{ts_suffix}{self.file_path.suffix}"
                )
                self._atomic_write(timestamped_path, payload)

            self._last_saved_page = self._state.current_page
            self._last_saved_records = self._state.processed_count
            self._last_saved_monotonic = time.monotonic()
            self._total_saves += 1

            log_message(
                "debug" if not force else "info",
                f"CheckpointManager: чекпоинт сохранён (страница={self._state.current_page}, "
                f"записей={self._state.processed_count}, статус={self._state.status})",
            )
            return True

        except Exception as e:
            # Требование TASK.md: сбой чекпоинта никогда не должен
            # прерывать скрапинг — только логируется как ошибка.
            log_message("error", f"CheckpointManager: не удалось сохранить чекпоинт: {e}")
            return False

    @staticmethod
    def _atomic_write(path: Path, payload: Dict[str, Any]) -> None:
        """
        Записывает JSON атомарно: пишет во временный файл в той же
        директории, принудительно сбрасывает буферы ОС на диск
        (`flush()` + `os.fsync()`), затем атомарно переименовывает
        (`os.replace()`) во целевой путь. Если процесс будет прерван
        в любой момент до `os.replace()`, целевой файл чекпоинта
        останется нетронутым (старая валидная версия).

        Args:
            path: Итоговый путь файла чекпоинта.
            payload: Сериализуемые данные для записи.
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), prefix=f".{path.stem}_", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        except Exception:
            # Гарантируем, что временный файл не остаётся мусором при сбое.
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import shutil
    import time as _time

    test_file = Path(tempfile.gettempdir()) / "checkpoint_manager_selftest.json"
    if test_file.exists():
        test_file.unlink()

    print(f"[{__file__}] Тест CheckpointManager (файл: {test_file})")

    checkpoint = CheckpointManager(
        run_id="selftest",
        enabled=True,
        file_path=test_file,
        interval_pages=2,
        interval_records=0,
        interval_seconds=0,
        overwrite_policy="overwrite",
    )

    checkpoint.start(status="running", site="example.com")

    for page in range(1, 6):
        saved = checkpoint.record_page(
            page_number=page,
            url=f"https://example.com/page/{page}",
            processed_count=page * 10,
            exported_count=page * 10,
        )
        print(f"  Страница {page}: сохранено={saved}")

    checkpoint.finish(status="completed")

    print(f"Всего сохранений: {checkpoint.total_saves}")
    print(f"Итоговое содержимое файла: {json.dumps(CheckpointManager.load(test_file), ensure_ascii=False, indent=2)}")

    test_file.unlink(missing_ok=True)
