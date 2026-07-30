#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Добавляет starter-project в пути Python

from app.checkpoint_manager import CheckpointManager
from app.config import EXPORT_INCREMENTAL_ENABLED

from app.playwright_engine import PlaywrightEngine, PlaywrightEngineError
from app.resume_manager import ResumeManager
from app.scraper import fetch_page_data
from app.parser import parse_listing, parse_html_data
from app.exporter import save_to_csv, save_to_json, IncrementalCSVWriter, IncrementalJSONWriter, BatchWriter
from app.utils import log_message


def _run_incremental(raw_pages_content) -> int:
    """
    Incremental Saving + Batch Writer: парсит каждую страницу по
    отдельности и передает полученные записи в `BatchWriter`, который
    буферизует их в памяти и сбрасывает на диск (через
    `IncrementalCSVWriter`/`IncrementalJSONWriter`) пачками, а не при
    каждом вызове — это уменьшает количество операций записи на диск по
    сравнению с прямым вызовом `write_records()` на каждой странице,
    сохраняя устойчивость к сбоям уже сброшенных данных (Incremental
    Saving).

    Дополнительно интегрирован Checkpoint Manager (см. `tasks/TASK.md`,
    `framework/ROADMAP.md` Milestone 6): после обработки каждой страницы
    прогресс (номер страницы, количество обработанных/сброшенных на диск
    записей) передается в `CheckpointManager.record_page()`, который сам
    решает, нужно ли реально записать чекпоинт на диск в этот момент
    (на основе `CHECKPOINT_INTERVAL_PAGES/RECORDS/SECONDS`). Checkpoint
    Manager только записывает прогресс — он не влияет на сам цикл
    парсинга/экспорта и не может его прервать (см. Error Handling в
    `app/checkpoint_manager.py`).

    Resume Support (см. `app/resume_manager.py`, `tasks/TASK.md`
    Milestone 6): перед началом обработки `ResumeManager` проверяет,
    есть ли валидный чекпоинт от прерванной сессии. Если да —
    восстанавливает `run_id`/счётчики в тот же `CheckpointManager`, а
    CSV/JSON writer'ы открываются в режиме дозаписи (`append=True`),
    чтобы уже экспортированные записи не были перезаписаны/потеряны.
    Страницы, номер которых `<= decision.start_page`, пропускаются —
    это предотвращает повторную обработку уже завершённой работы.

    Память используется только под записи текущего буфера (максимум
    `BATCH_WRITER_BATCH_SIZE` записей) — предыдущие сброшенные батчи уже
    высвобождены сборщиком мусора. Это позволяет обрабатывать очень
    большие датасеты (сотни тысяч записей) без пропорционального роста
    потребления RAM.

    Args:
        raw_pages_content: Список строк HTML страниц (от `fetch_page_data`).

    Returns:
        int: Общее количество записей, успешно сброшенных на диск через BatchWriter.
    """
    # Resume Support: ищем чекпоинт от прерванной сессии ДО создания
    # нового run_id — если восстановление удастся, ResumeManager сам
    # перезапишет run_id в checkpoint.state значением из чекпоинта.
    fallback_run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    checkpoint = CheckpointManager(run_id=fallback_run_id)

    decision = ResumeManager().resume(checkpoint)

    if decision.resumed:
        log_message(
            "info",
            f"[{__file__}] Resume Support: восстановлена сессия '{checkpoint.state.run_id}' "
            f"(страница={decision.start_page}, экспортировано={decision.exported_count})",
        )
    else:
        checkpoint.start(status="running", total_pages=len(raw_pages_content))

    processed_total = decision.processed_count
    checkpoint_failed = False

    # Resume Support Integration с Incremental Saving (см. tasks/TASK.md,
    # "Integration with Incremental Saving"): при восстановленной сессии
    # writer'ы открываются в режиме дозаписи (append=True), чтобы уже
    # экспортированные ранее записи оставались нетронутыми — никогда не
    # перезаписываются. При отсутствии восстановления (append=False)
    # поведение полностью идентично поведению до появления Resume Support.
    with IncrementalCSVWriter("output_results.csv", append=decision.resumed) as csv_writer, \
            IncrementalJSONWriter("output_results.json", append=decision.resumed) as json_writer:

        with BatchWriter([csv_writer, json_writer]) as batch_writer:
            for idx, html in enumerate(raw_pages_content, 1):
                # Duplicate Protection (см. tasks/TASK.md, "Duplicate
                # Protection"): страницы, уже обработанные и сброшенные
                # на диск в прошлой (прерванной) сессии, пропускаются —
                # восстановленное состояние продолжает строго ПОСЛЕ
                # последнего успешно зафиксированного чекпоинта.
                if idx <= decision.start_page:
                    continue

                try:
                    page_records = parse_listing(html)
                except Exception as e:
                    log_message("error", f"[{__file__}] Не удалось обработать страницу #{idx}: {e}")
                    continue

                if not page_records:
                    continue

                batch_writer.add_records(page_records)
                processed_total += len(page_records)

                # Checkpoint Manager сам решает (на основе настроенных
                # интервалов), нужно ли реально записать чекпоинт сейчас.
                # Сбой сохранения чекпоинта НИКОГДА не должен прерывать
                # скрапинг (см. TASK.md, раздел "Error Handling") —
                # CheckpointManager сам это гарантирует, здесь только
                # защита на случай непредвиденного исключения самого вызова.
                try:
                    checkpoint.record_page(
                        page_number=idx,
                        processed_count=processed_total,
                        exported_count=batch_writer.total_flushed + decision.exported_count,
                    )
                except Exception as cp_exc:
                    if not checkpoint_failed:
                        log_message("error", f"[{__file__}] Checkpoint Manager: непредвиденная ошибка: {cp_exc}")
                        checkpoint_failed = True

        # Integration with Batch Writer (см. tasks/TASK.md, "Integration
        # with Batch Writer"): к этому моменту `with BatchWriter(...)` уже
        # завершился, и BatchWriter.close() выполнил shutdown-сброс
        # оставшихся в буфере записей (если BATCH_WRITER_FLUSH_ON_SHUTDOWN
        # включен) — весь ещё не сброшенный "хвост" гарантированно попал
        # на диск ДО финальной записи чекпоинта ниже, поэтому чекпоинт
        # никогда не укажет на страницу, чьи записи реально не сохранены.
        total_records = batch_writer.total_flushed + decision.exported_count

    checkpoint.finish(status="completed", processed_count=processed_total, exported_count=total_records)

    return total_records




def main() -> None:
    """
    Главная точка входа. Управляет жизненным циклом парсера.

    Поддерживает два режима экспорта (см. `app/config.py`,
    `EXPORT_INCREMENTAL_ENABLED`):
      - Incremental Saving + Batch Writer (по умолчанию) — каждая
        страница парсится, записи буферизуются в памяти и сбрасываются
        в CSV/JSON пачками (см. `_run_incremental()`).
      - Batch-режим (обратная совместимость) — все страницы парсятся,
        результаты копятся в памяти и экспортируются одним вызовом
        `save_to_csv`/`save_to_json` после завершения скрапинга —
        поведение, идентичное поведению проекта до появления
        Incremental Saving.
    """
    print("=" * 70)
    print(f"[{__file__}] ЗАПУСК ПАРСЕРА")
    print("=" * 70)

    try:
        # 1. Запуск браузерной автоматизации через централизованный Playwright Engine
        # (идентичность, куки и прокси применяются автоматически)
        with PlaywrightEngine() as engine:

            # 2. Сбор данных (Scraping)
            # Передаем движок в scraper.py для обхода страниц
            try:
                raw_pages_content = fetch_page_data(engine)
            except PlaywrightEngineError as e:
                print(f"[{__file__}] Критическая ошибка браузера: {e}")
                sys.exit(1)

            if not raw_pages_content:
                print(f"[{__file__}] Критическая ошибка: Нечего парсить (список страниц пуст).")
                sys.exit(1)

            # 3. Обработка данных (Parsing) + 4. Экспорт результатов (Export)
            if EXPORT_INCREMENTAL_ENABLED:
                print(f"[{__file__}] Incremental Saving + Batch Writer включены: обработка {len(raw_pages_content)} страниц(ы)...")
                total_records = _run_incremental(raw_pages_content)

                if total_records:
                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО (Всего записей: {total_records})")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат.")
            else:
                # Batch-режим — прежнее поведение (обратная совместимость)
                print(f"[{__file__}] Начало парсинга контента (batch-режим)...")
                scraped_results = parse_html_data(raw_pages_content)

                if scraped_results:
                    print(f"[{__file__}] Экспорт данных (Всего элементов: {len(scraped_results)})...")
                    save_to_csv(scraped_results, "output_results.csv")
                    save_to_json(scraped_results, "output_results.json")

                    print("=" * 70)
                    print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО")
                    print("=" * 70)
                else:
                    print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат. Файлы не созданы.")

    except KeyError as ke:
        print(f"[{__file__}] Ошибка конфигурации или структуры: {ke}")
        sys.exit(1)
    except Exception as e:
        print(f"[{__file__}] Критический сбой в главном потоке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
