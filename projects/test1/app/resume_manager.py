#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resume Support.

Централизованный компонент, отвечающий ТОЛЬКО за обнаружение,
валидацию и восстановление прогресса прерванной сессии скрапинга на
основе чекпоинтов, сохранённых Checkpoint Manager'ом (см.
`framework/ROADMAP.md`, Milestone 6, и `tasks/TASK.md`).

Resume Support:

* обнаруживает существующий чекпоинт через уже существующий
  `CheckpointManager.load()` (не реализует собственный механизм чтения
  состояния — переиспользует Checkpoint Manager, как того требует
  `tasks/TASK.md`, раздел "Do not duplicate checkpoint logic");
* валидирует чекпоинт (обязательные поля, статус, "свежесть" по
  `RESUME_MAX_AGE_SECONDS`, совместимость версии схемы);
* "засеивает" уже существующий `CheckpointManager` восстановленным
  состоянием через его публичное свойство `state` — не добавляет новую
  персистентность, только переиспользует объект, который сам же
  продолжит сохранять чекпоинты дальше в течение новой сессии;
* сообщает вызывающему коду (`app/main.py`), сколько страниц уже было
  обработано ранее, чтобы цикл скрапинга мог их пропустить.

Resume Support НЕ создаёт чекпоинты (это делает Checkpoint Manager), НЕ
пишет файлы экспорта (это делают `IncrementalCSVWriter`/`JSONWriter` в
режиме `append=True`, см. `app/exporter.py`) и НЕ выполняет парсинг —
он полностью независим от scraper-специфичного кода, как и Checkpoint
Manager, и может использоваться с любым скрапером фреймворка без
изменений.

Пример использования (см. интеграцию в `app/main.py::_run_incremental()`):

    from app.checkpoint_manager import CheckpointManager
    from app.resume_manager import ResumeManager

    checkpoint = CheckpointManager(run_id="olx_cars_2024")
    decision = ResumeManager().resume(checkpoint)

    if decision.resumed:
        print(f"Продолжаем с страницы {decision.start_page + 1}")
    else:
        checkpoint.start(status="running")

    for page_number, html in enumerate(raw_pages_content, 1):
        if page_number <= decision.start_page:
            continue  # уже обработано в прошлой сессии — не дублируем
        ...
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.checkpoint_manager import CheckpointManager
from app.config import RESUME_ENABLED, RESUME_MAX_AGE_SECONDS
from app.utils import log_message

# Статусы чекпоинта, которые считаются "прерванными" и подлежат
# восстановлению. "completed" сознательно НЕ входит в этот список —
# завершённую сессию не нужно "продолжать" (см. TASK.md, требование не
# путать полностью выполненную работу с прерванной).
_RESUMABLE_STATUSES = ("running", "failed")

# Обязательные поля, без которых чекпоинт считается повреждённым/неполным
# (см. TASK.md, "Error Handling" -> "incomplete checkpoint data").
_REQUIRED_FIELDS = ("run_id", "status", "current_page", "timestamp")


@dataclass
class ResumeDecision:
    """
    Результат попытки восстановления, возвращаемый `ResumeManager.resume()`.

    Атрибуты:
        resumed (bool): True, если сессия была успешно восстановлена из
            валидного чекпоинта; False — начата новая сессия "с нуля"
            (нет чекпоинта, он невалиден/устарел, либо Resume Support
            отключен через `RESUME_ENABLED`).
        start_page (int): Номер последней уже обработанной страницы.
            Вызывающий код должен пропустить страницы с номером
            `<= start_page` (см. TASK.md, "avoid reprocessing already
            completed work"). При `resumed=False` всегда 0.
        processed_count (int): Количество записей, обработанных в
            прошлой сессии (для информации/логирования). 0, если не
            восстановлено.
        exported_count (int): Количество записей, реально
            экспортированных в прошлой сессии — именно это значение
            должно совпадать с фактическим содержимым файлов вывода,
            открытых в режиме `append=True`. 0, если не восстановлено.
        reason (str): Причина решения — "no_checkpoint", "disabled",
            "invalid_checkpoint", "expired_checkpoint",
            "already_completed" или "resumed".
        checkpoint_data (dict, optional): Сырые данные восстановленного
            чекпоинта (для расширенного использования вызывающим кодом,
            например восстановления `current_url`/`extra_metadata`).
    """

    resumed: bool
    start_page: int = 0
    processed_count: int = 0
    exported_count: int = 0
    reason: str = "no_checkpoint"
    checkpoint_data: Optional[Dict[str, Any]] = None


class ResumeManager:
    """
    Принимает решение "можно ли и нужно ли восстанавливать сессию" и
    передаёт восстановленное состояние в уже существующий
    `CheckpointManager`, не создавая собственного хранилища состояния.
    """

    def __init__(
        self,
        *,
        enabled: Optional[bool] = None,
        max_age_seconds: Optional[int] = None,
    ) -> None:
        """
        Args:
            enabled: Включает/выключает автоматическое восстановление.
                По умолчанию — `config.RESUME_ENABLED`.
            max_age_seconds: Максимальный возраст чекпоинта (секунды),
                при котором он ещё пригоден для восстановления. 0 — не
                ограничивать. По умолчанию — `config.RESUME_MAX_AGE_SECONDS`.
        """
        self.enabled = enabled if enabled is not None else RESUME_ENABLED
        self.max_age_seconds = max_age_seconds if max_age_seconds is not None else RESUME_MAX_AGE_SECONDS

    def resume(self, checkpoint: CheckpointManager) -> ResumeDecision:
        """
        Пытается обнаружить и восстановить прогресс из чекпоинта,
        связанного с переданным `CheckpointManager` (используется его
        `file_path`, чтобы Resume Support не хранил собственный путь —
        единый источник правды остаётся в Checkpoint Manager).

        При успешном восстановлении "засеивает" `checkpoint.state`
        восстановленными значениями через публичное свойство `state` —
        сам `checkpoint` после этого продолжает работать как обычно
        (`record_page()`, `finish()` и т.д.), просто не с нулевого, а с
        восстановленного состояния. Явно НЕ вызывает `checkpoint.start()`
        здесь — это оставлено на решение вызывающего кода (`app/main.py`),
        чтобы Resume Support не диктовал момент первой записи на диск.

        Args:
            checkpoint: Экземпляр `CheckpointManager`, чей `file_path`
                используется для поиска чекпоинта, и чьё состояние
                будет обновлено при успешном восстановлении.

        Returns:
            ResumeDecision: Итоговое решение (см. докстринг класса).
        """
        if not self.enabled:
            log_message("info", "ResumeManager: восстановление отключено (RESUME_ENABLED=0) — новая сессия")
            return ResumeDecision(resumed=False, reason="disabled")

        data = CheckpointManager.load(checkpoint.file_path)
        if data is None:
            log_message("info", "ResumeManager: чекпоинт не найден — начинается новая сессия")
            return ResumeDecision(resumed=False, reason="no_checkpoint")

        log_message("info", f"ResumeManager: обнаружен чекпоинт ({checkpoint.file_path.name})")

        validation_error = self._validate(data)
        if validation_error is not None:
            log_message(
                "error",
                f"ResumeManager: чекпоинт невалиден ({validation_error}) — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="invalid_checkpoint")

        if data["status"] not in _RESUMABLE_STATUSES:
            # status == "completed" — работа уже была полностью
            # завершена в прошлый раз, восстанавливать нечего.
            log_message(
                "info",
                f"ResumeManager: чекпоинт со статусом '{data['status']}' не подлежит "
                f"восстановлению — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="already_completed")

        if self._is_expired(data):
            log_message(
                "error",
                f"ResumeManager: чекпоинт устарел (старше {self.max_age_seconds}с) — начинается новая сессия",
            )
            return ResumeDecision(resumed=False, reason="expired_checkpoint")

        # Восстановление состояния: "засеиваем" уже существующий
        # CheckpointManager, а не создаём параллельное хранилище.
        checkpoint.state.run_id = data.get("run_id", checkpoint.state.run_id)
        checkpoint.state.status = "running"
        checkpoint.state.current_page = int(data.get("current_page", 0))
        checkpoint.state.current_url = data.get("current_url")
        checkpoint.state.processed_count = int(data.get("processed_count", 0))
        checkpoint.state.exported_count = int(data.get("exported_count", 0))
        checkpoint.state.extra_metadata = dict(data.get("extra_metadata") or {})

        log_message(
            "info",
            f"ResumeManager: сессия восстановлена (страница={checkpoint.state.current_page}, "
            f"обработано={checkpoint.state.processed_count}, экспортировано={checkpoint.state.exported_count})",
        )

        return ResumeDecision(
            resumed=True,
            start_page=checkpoint.state.current_page,
            processed_count=checkpoint.state.processed_count,
            exported_count=checkpoint.state.exported_count,
            reason="resumed",
            checkpoint_data=data,
        )

    # =====================================================================
    # ВНУТРЕННЯЯ ЛОГИКА
    # =====================================================================

    @staticmethod
    def _validate(data: Dict[str, Any]) -> Optional[str]:
        """
        Проверяет наличие обязательных полей и базовую консистентность
        типов чекпоинта (см. TASK.md, "Error Handling" -> "incomplete
        checkpoint data" / "corrupted checkpoint").

        Returns:
            str, optional: Текст ошибки, если чекпоинт невалиден,
                либо None, если валиден.
        """
        if not isinstance(data, dict):
            return "чекпоинт не является объектом"

        missing = [field for field in _REQUIRED_FIELDS if field not in data]
        if missing:
            return f"отсутствуют обязательные поля: {', '.join(missing)}"

        if not isinstance(data.get("run_id"), str) or not data["run_id"]:
            return "поле run_id пустое или некорректного типа"

        if not isinstance(data.get("status"), str):
            return "поле status некорректного типа"

        try:
            int(data.get("current_page", 0))
        except (TypeError, ValueError):
            return "поле current_page некорректного типа"

        if not isinstance(data.get("timestamp"), str):
            return "поле timestamp некорректного типа"

        return None

    def _is_expired(self, data: Dict[str, Any]) -> bool:
        """
        Проверяет "возраст" чекпоинта относительно `max_age_seconds`.
        При `max_age_seconds == 0` возраст не ограничивается.
        """
        if self.max_age_seconds <= 0:
            return False

        try:
            checkpoint_time = datetime.fromisoformat(data["timestamp"])
            if checkpoint_time.tzinfo is None:
                checkpoint_time = checkpoint_time.replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            # Не удалось разобрать timestamp — считаем чекпоинт
            # невалидным для целей возраста, но это уже отловлено
            # в _validate() раньше в общем потоке resume().
            return True

        age_seconds = (datetime.now(timezone.utc) - checkpoint_time).total_seconds()
        return age_seconds > self.max_age_seconds


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    test_file = Path(tempfile.gettempdir()) / "resume_manager_selftest.json"
    test_file.unlink(missing_ok=True)

    print(f"[{__file__}] Тест ResumeManager (файл: {test_file})")

    # --- Сценарий 1: нет чекпоинта -> новая сессия ---
    checkpoint = CheckpointManager(run_id="selftest", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(checkpoint)
    print(f"  Без чекпоинта: resumed={decision.resumed}, reason={decision.reason}")
    assert decision.resumed is False

    # --- Симулируем прерванную сессию: 3 страницы обработаны, status=running ---
    checkpoint.start(status="running", site="example.com")
    checkpoint.record_page(page_number=3, processed_count=30, exported_count=30)

    # --- Сценарий 2: новый CheckpointManager (новый запуск процесса) -> восстановление ---
    fresh_checkpoint = CheckpointManager(run_id="selftest-new", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(fresh_checkpoint)
    print(
        f"  С чекпоинтом (running, стр.3): resumed={decision.resumed}, "
        f"start_page={decision.start_page}, exported={decision.exported_count}"
    )
    assert decision.resumed is True
    assert decision.start_page == 3

    # --- Сценарий 3: сессия завершена (completed) -> не восстанавливать ---
    fresh_checkpoint.finish(status="completed")
    another_checkpoint = CheckpointManager(run_id="selftest-completed", file_path=test_file, interval_pages=1)
    decision = ResumeManager().resume(another_checkpoint)
    print(f"  С чекпоинтом (completed): resumed={decision.resumed}, reason={decision.reason}")
    assert decision.resumed is False
    assert decision.reason == "already_completed"

    test_file.unlink(missing_ok=True)
    print(f"[{__file__}] Все проверки пройдены успешно.")
