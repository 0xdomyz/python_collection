"""Integration benchmark tests for groupby runner against a real Teradata DB.

This module is intentionally opt-in. To run:

    set RUN_TERADATA_INTEGRATION=1
    set TERADATA_HOST=<host>
    set TERADATA_USER=<user>
    set TERADATA_PASSWORD=<password>
    set TERADATA_DATABASE=DBC   # optional
    pytest -s database_related/teradata_related/groupby_runner/tests/test_integration_groupby_benchmark.py
"""

import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

# Ensure package importability from this test location.
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from database_related.teradata_related.groupby_runner import ParallelGroupByRunner


def _env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y"}


def _integration_enabled() -> Tuple[bool, str]:
    if not _env_flag("RUN_TERADATA_INTEGRATION"):
        return False, "RUN_TERADATA_INTEGRATION is not enabled"

    required = ["TERADATA_HOST", "TERADATA_USER", "TERADATA_PASSWORD"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        return False, f"Missing required env vars: {', '.join(missing)}"

    return True, ""


def _build_engine():
    host = os.getenv("TERADATA_HOST")
    user = os.getenv("TERADATA_USER")
    password = os.getenv("TERADATA_PASSWORD")
    database = os.getenv("TERADATA_DATABASE", "DBC")

    connection_string = f"teradatasql://{user}:{password}@{host}/{database}"
    return create_engine(
        connection_string,
        echo=False,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=1800,
    )


def _sql_literal(value: str) -> str:
    return value.replace("'", "''")


def _build_benchmark_queries() -> List[str]:
    db = _sql_literal(os.getenv("TERADATA_DATABASE", "DBC"))
    return [
        f"""
        SELECT TableKind, COUNT(*) AS Cnt
        FROM DBC.TablesV
        WHERE DataBaseName = '{db}'
        GROUP BY TableKind
        """,
        f"""
        SELECT COUNT(*) AS TotalTables
        FROM DBC.TablesV
        WHERE DataBaseName = '{db}'
        """,
        f"""
        SELECT COUNT(DISTINCT TableName) AS DistinctTables
        FROM DBC.ColumnsV
        WHERE DataBaseName = '{db}'
        """,
        f"""
        SELECT ColumnType, COUNT(*) AS Cnt
        FROM DBC.ColumnsV
        WHERE DataBaseName = '{db}'
        GROUP BY ColumnType
        """,
        f"""
        SELECT TOP 200 TableName, TableKind
        FROM DBC.TablesV
        WHERE DataBaseName = '{db}'
        ORDER BY TableName
        """,
        f"""
        SELECT TOP 200 TableName, ColumnName, ColumnType
        FROM DBC.ColumnsV
        WHERE DataBaseName = '{db}'
        ORDER BY TableName, ColumnId
        """,
        f"""
        SELECT TOP 100 t.TableName, COUNT(c.ColumnName) AS ColCnt
        FROM DBC.TablesV t
        JOIN DBC.ColumnsV c
          ON t.DataBaseName = c.DataBaseName
         AND t.TableName = c.TableName
        WHERE t.DataBaseName = '{db}'
        GROUP BY t.TableName
        ORDER BY ColCnt DESC
        """,
        f"""
        SELECT COUNT(*) AS TotalDatabases
        FROM DBC.DatabasesV
        """,
    ]


def _sleep_seconds() -> float:
    raw = os.getenv("TERADATA_BENCHMARK_CLIENT_SLEEP", "0.15")
    try:
        value = float(raw)
    except ValueError:
        value = 0.15
    return max(0.0, value)


def _overlap_count(records: List[Dict]) -> int:
    overlap = 0
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            a = records[i]
            b = records[j]
            if a["start_epoch"] < b["end_epoch"] and b["start_epoch"] < a["end_epoch"]:
                overlap += 1
    return overlap


def _execute_query_with_logging(engine, query_id: int, query: str) -> Dict:
    thread_id = threading.get_ident()
    start_time = datetime.now()
    start_epoch = time.perf_counter()
    session_id = None
    status = "SUCCESS"
    row_count = 0

    try:
        sleep_s = _sleep_seconds()
        if sleep_s > 0:
            time.sleep(sleep_s)

        with engine.connect() as conn:
            session_id = conn.execute(text("SELECT SESSION")).scalar()
            rows = conn.execute(text(query)).fetchall()
            row_count = len(rows)
    except Exception as exc:  # pragma: no cover - integration guardrail
        status = f"ERROR: {str(exc)[:200]}"
    finally:
        end_time = datetime.now()
        end_epoch = time.perf_counter()

    return {
        "query_id": query_id,
        "thread_id": thread_id,
        "session_id": session_id,
        "start_time": start_time,
        "end_time": end_time,
        "start_epoch": start_epoch,
        "end_epoch": end_epoch,
        "duration": end_epoch - start_epoch,
        "row_count": row_count,
        "status": status,
    }


def _run_sequential_direct(engine, queries: List[str]) -> Tuple[float, List[Dict]]:
    start = time.perf_counter()
    records = [
        _execute_query_with_logging(engine, idx, sql)
        for idx, sql in enumerate(queries, start=1)
    ]
    total = time.perf_counter() - start
    return total, records


def _run_threadpool_direct(
    engine, queries: List[str], max_workers: int = 6
) -> Tuple[float, List[Dict]]:
    start = time.perf_counter()
    records: List[Dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [
            pool.submit(_execute_query_with_logging, engine, idx, sql)
            for idx, sql in enumerate(queries, start=1)
        ]
        for future in as_completed(futures):
            records.append(future.result())
    total = time.perf_counter() - start
    records.sort(key=lambda item: item["query_id"])
    return total, records


class _InstrumentedParallelRunner(ParallelGroupByRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records: List[Dict] = []
        self._records_lock = threading.Lock()

    def _run_single(self, sql: str) -> pd.DataFrame:
        thread_id = threading.get_ident()
        start_time = datetime.now()
        start_epoch = time.perf_counter()
        session_id = None

        sleep_s = _sleep_seconds()
        if sleep_s > 0:
            time.sleep(sleep_s)

        with self.engine.connect() as conn:
            session_id = conn.execute(text("SELECT SESSION")).scalar()
            df = pd.read_sql(text(sql), conn)

        end_time = datetime.now()
        end_epoch = time.perf_counter()
        record = {
            "thread_id": thread_id,
            "session_id": session_id,
            "start_time": start_time,
            "end_time": end_time,
            "start_epoch": start_epoch,
            "end_epoch": end_epoch,
            "duration": end_epoch - start_epoch,
            "row_count": len(df),
            "status": "SUCCESS",
        }
        with self._records_lock:
            self.records.append(record)
        return df


def _run_framework_parallel(engine, queries: List[str]) -> Tuple[float, List[Dict]]:
    runner = _InstrumentedParallelRunner(
        engine=engine,
        base_table="DBC.TablesV",
        subset_filter=None,
        subset_table="vt_subset",
        max_workers=6,
    )

    start = time.perf_counter()
    frames = runner.run(queries, materialise_subset=False)
    total = time.perf_counter() - start

    assert len(frames) == len(queries)
    return total, runner.records


@pytest.mark.integration
def test_real_teradata_concurrency_benchmark_three_methods():
    enabled, reason = _integration_enabled()
    if not enabled:
        pytest.skip(reason)

    queries = _build_benchmark_queries()
    if len(queries) < 3:
        pytest.skip("Need at least 3 queries for benchmark")

    engine = _build_engine()

    sequential_time, sequential_records = _run_sequential_direct(engine, queries)
    threadpool_time, threadpool_records = _run_threadpool_direct(engine, queries)
    framework_parallel_time, framework_records = _run_framework_parallel(
        engine, queries
    )

    sequential_ok = all(item["status"] == "SUCCESS" for item in sequential_records)
    threadpool_ok = all(item["status"] == "SUCCESS" for item in threadpool_records)
    framework_ok = all(item["status"] == "SUCCESS" for item in framework_records)

    assert sequential_ok, "Sequential method had query failures"
    assert threadpool_ok, "ThreadPool method had query failures"
    assert framework_ok, "ParallelGroupByRunner method had query failures"

    threadpool_thread_ids = {item["thread_id"] for item in threadpool_records}
    framework_thread_ids = {item["thread_id"] for item in framework_records}
    threadpool_sessions = {
        item["session_id"]
        for item in threadpool_records
        if item["session_id"] is not None
    }
    framework_sessions = {
        item["session_id"]
        for item in framework_records
        if item["session_id"] is not None
    }

    assert len(threadpool_thread_ids) > 1, "ThreadPool did not use multiple threads"
    assert (
        len(framework_thread_ids) > 1
    ), "ParallelGroupByRunner did not use multiple threads"
    assert len(threadpool_sessions) > 1, "ThreadPool did not open multiple DB sessions"
    assert (
        len(framework_sessions) > 1
    ), "ParallelGroupByRunner did not open multiple DB sessions"

    threadpool_overlaps = _overlap_count(threadpool_records)
    framework_overlaps = _overlap_count(framework_records)
    assert threadpool_overlaps > 0, "ThreadPool execution windows did not overlap"
    assert (
        framework_overlaps > 0
    ), "ParallelGroupByRunner execution windows did not overlap"

    best_parallel = min(threadpool_time, framework_parallel_time)
    assert best_parallel < sequential_time, (
        "Expected at least one concurrent method to beat sequential timing. "
        f"sequential={sequential_time:.3f}s, "
        f"threadpool={threadpool_time:.3f}s, "
        f"framework_parallel={framework_parallel_time:.3f}s"
    )

    speedup_threadpool = (
        sequential_time / threadpool_time if threadpool_time else float("inf")
    )
    speedup_framework = (
        sequential_time / framework_parallel_time
        if framework_parallel_time
        else float("inf")
    )

    print("\n=== Teradata Concurrency Benchmark (3 Methods) ===")
    print(f"queries={len(queries)}, client_sleep_s={_sleep_seconds():.3f}")
    print(f"sequential_direct     : {sequential_time:.3f}s")
    print(
        f"threadpool_direct     : {threadpool_time:.3f}s  speedup={speedup_threadpool:.2f}x"
    )
    print(
        f"parallel_runner       : {framework_parallel_time:.3f}s  "
        f"speedup={speedup_framework:.2f}x"
    )
    print(
        f"threadpool: threads={len(threadpool_thread_ids)}, sessions={len(threadpool_sessions)}, "
        f"overlaps={threadpool_overlaps}"
    )
    print(
        f"parallel_runner: threads={len(framework_thread_ids)}, sessions={len(framework_sessions)}, "
        f"overlaps={framework_overlaps}"
    )
