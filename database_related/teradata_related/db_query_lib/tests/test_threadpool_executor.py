"""Tests for ThreadPoolQueryExecutor."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import ExecutionResult, ThreadPoolQueryExecutor
from db_query_lib.exceptions import ThreadPoolExecutionError


class TestThreadPoolQueryExecutor:
    """Test cases for ThreadPoolQueryExecutor."""

    def test_init(self):
        """Test executor initialization."""
        executor = ThreadPoolQueryExecutor(max_workers=5, timeout=30)
        assert executor.max_workers == 5
        assert executor.timeout == 30
        assert len(executor.results) == 0

    def test_execute_function_concurrent_success(self):
        """Test successful concurrent function execution."""

        def sample_function(x, y):
            return x + y

        arguments = [
            {"x": 1, "y": 2},
            {"x": 3, "y": 4},
            {"x": 5, "y": 6},
        ]
        query_ids = ["calc1", "calc2", "calc3"]

        executor = ThreadPoolQueryExecutor(max_workers=3)
        results = executor.execute_function_concurrent(
            sample_function, arguments, query_ids
        )

        assert len(results) == 3
        assert all(isinstance(r, ExecutionResult) for r in results)
        assert all(r.is_success for r in results)
        # Check that all expected results are present (in any order)
        result_values = sorted([r.result for r in results])
        assert result_values == [3, 7, 11]  # 1+2, 3+4, 5+6

    def test_execute_function_concurrent_with_errors(self):
        """Test concurrent execution with some failures."""

        def sample_function(x):
            if x < 0:
                raise ValueError("x must be positive")
            return x * 2

        arguments = [
            {"x": 1},
            {"x": -1},  # Will fail
            {"x": 2},
        ]

        executor = ThreadPoolQueryExecutor(max_workers=3)
        results = executor.execute_function_concurrent(sample_function, arguments)

        assert len(results) == 3
        successful = [r for r in results if r.is_success]
        failed = [r for r in results if not r.is_success]
        assert len(successful) == 2
        assert len(failed) == 1
        assert failed[0].error is not None

    def test_execute_function_concurrent_empty_list(self):
        """Test that empty arguments list raises error."""
        executor = ThreadPoolQueryExecutor(max_workers=5)

        with pytest.raises(ThreadPoolExecutionError):
            executor.execute_function_concurrent(lambda x: x, [])

    def test_get_summary(self):
        """Test getting execution summary."""

        def sample_function(x):
            return x * 2

        arguments = [{"x": i} for i in range(5)]

        executor = ThreadPoolQueryExecutor(max_workers=3)
        executor.execute_function_concurrent(sample_function, arguments)

        summary = executor.get_summary()

        assert summary["total_executions"] == 5
        assert summary["successful"] == 5
        assert summary["failed"] == 0
        assert summary["total_execution_time"] > 0
        assert summary["wall_clock_time"] > 0
        assert summary["speedup"] > 0
        assert "min_duration" in summary
        assert "max_duration" in summary
        assert "avg_duration" in summary

    def test_get_summary_with_failures(self):
        """Test summary with some failed executions."""

        def sample_function(x):
            if x == 3:
                raise ValueError("test error")
            return x

        arguments = [{"x": i} for i in range(5)]

        executor = ThreadPoolQueryExecutor(max_workers=3)
        executor.execute_function_concurrent(sample_function, arguments)

        summary = executor.get_summary()

        assert summary["total_executions"] == 5
        assert summary["successful"] == 4
        assert summary["failed"] == 1

    def test_get_summary_empty(self):
        """Test summary on empty executor."""
        executor = ThreadPoolQueryExecutor(max_workers=5)
        summary = executor.get_summary()

        assert summary == {}

    def test_execution_result_creation(self):
        """Test ExecutionResult dataclass."""
        from datetime import datetime

        result = ExecutionResult(
            query_id="test1",
            thread_id=12345,
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_seconds=1.5,
            result={"data": "value"},
            error=None,
            is_success=True,
        )

        assert result.query_id == "test1"
        assert result.thread_id == 12345
        assert result.duration_seconds == 1.5
        assert result.is_success is True

    def test_print_results(self, capsys):
        """Test printing results."""

        def sample_function(x):
            return x

        arguments = [{"x": i} for i in range(2)]

        executor = ThreadPoolQueryExecutor(max_workers=2)
        executor.execute_function_concurrent(sample_function, arguments)

        executor.print_results(verbose=False)
        captured = capsys.readouterr()

        assert "THREADPOOL EXECUTION SUMMARY" in captured.out
        assert "Total Executions:" in captured.out
        assert "Successful:" in captured.out

    def test_print_results_verbose(self, capsys):
        """Test printing results in verbose mode."""

        def sample_function(x):
            return x

        arguments = [{"x": i} for i in range(2)]

        executor = ThreadPoolQueryExecutor(max_workers=2)
        executor.execute_function_concurrent(
            sample_function, arguments, query_ids=["q1", "q2"]
        )

        executor.print_results(verbose=True)
        captured = capsys.readouterr()

        assert "DETAILED RESULTS:" in captured.out
        assert "q1" in captured.out or "q2" in captured.out

    def test_concurrency_parallelism(self):
        """Test that tasks actually run in parallel."""
        import time

        def slow_function(duration):
            time.sleep(duration)
            return duration

        # 3 tasks of 0.1s each
        arguments = [{"duration": 0.1} for _ in range(3)]

        executor = ThreadPoolQueryExecutor(max_workers=3)
        import time as time_module

        start = time_module.time()
        results = executor.execute_function_concurrent(slow_function, arguments)
        elapsed = time_module.time() - start

        # Sequential would take ~0.3s, parallel should take ~0.1s
        # With some overhead, should be less than 0.25s
        assert elapsed < 0.25  # Parallel execution is faster

    def test_different_query_ids(self):
        """Test with custom query IDs."""

        def sample_function(value):
            return value

        arguments = [{"value": 1}, {"value": 2}]
        query_ids = ["custom_query_1", "custom_query_2"]

        executor = ThreadPoolQueryExecutor(max_workers=2)
        results = executor.execute_function_concurrent(
            sample_function, arguments, query_ids
        )

        result_ids = {r.query_id for r in results}
        assert result_ids == {"custom_query_1", "custom_query_2"}
