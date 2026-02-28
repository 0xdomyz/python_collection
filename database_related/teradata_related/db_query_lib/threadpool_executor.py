"""Threadpool-based concurrent query execution utilities."""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from .exceptions import ThreadPoolExecutionError

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of a query execution."""

    query_id: str
    thread_id: int
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    result: Any
    error: Optional[str] = None
    is_success: bool = True


class ThreadPoolQueryExecutor:
    """Executor for running queries concurrently using ThreadPoolExecutor."""

    def __init__(self, max_workers: int = 5, timeout: Optional[float] = None):
        """
        Initialize thread pool executor.

        Args:
            max_workers: Maximum number of worker threads
            timeout: Timeout per query execution in seconds
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self.results: List[ExecutionResult] = []

    def execute_function_concurrent(
        self,
        function: Callable,
        arguments_list: List[Dict[str, Any]],
        query_ids: Optional[List[str]] = None,
    ) -> List[ExecutionResult]:
        """
        Execute a function concurrently across multiple argument sets.

        Args:
            function: Callable that accepts keyword arguments
            arguments_list: List of dicts containing function arguments
            query_ids: Optional list of identifiers for each execution

        Returns:
            List of ExecutionResult objects

        Raises:
            ThreadPoolExecutionError: If execution fails
        """
        if not arguments_list:
            raise ThreadPoolExecutionError("arguments_list cannot be empty")

        results = []

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_index = {}
                for i, args in enumerate(arguments_list):
                    query_id = query_ids[i] if query_ids else f"query_{i}"
                    future = executor.submit(self._run_task, function, query_id, args)
                    future_to_index[future] = i

                # Collect results as they complete
                for future in as_completed(future_to_index, timeout=self.timeout):
                    try:
                        result = future.result(timeout=self.timeout)
                        results.append(result)
                    except Exception as e:
                        idx = future_to_index[future]
                        query_id = query_ids[idx] if query_ids else f"query_{idx}"
                        results.append(
                            ExecutionResult(
                                query_id=query_id,
                                thread_id=threading.get_ident(),
                                start_time=datetime.now(),
                                end_time=datetime.now(),
                                duration_seconds=0,
                                result=None,
                                error=str(e),
                                is_success=False,
                            )
                        )

        except Exception as e:
            raise ThreadPoolExecutionError(f"Threadpool execution failed: {e}")

        self.results = results
        return results

    @staticmethod
    def _run_task(
        function: Callable, query_id: str, kwargs: Dict[str, Any]
    ) -> ExecutionResult:
        """
        Run a single task and measure execution metrics.

        Args:
            function: Callable to execute
            query_id: Identifier for this execution
            kwargs: Keyword arguments for function

        Returns:
            ExecutionResult with metrics
        """
        thread_id = threading.get_ident()
        start_time = datetime.now()
        start_perf = time.perf_counter()

        try:
            result = function(**kwargs)
            end_perf = time.perf_counter()
            end_time = datetime.now()
            duration = end_perf - start_perf

            return ExecutionResult(
                query_id=query_id,
                thread_id=thread_id,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                result=result,
                error=None,
                is_success=True,
            )
        except Exception as e:
            end_perf = time.perf_counter()
            end_time = datetime.now()
            duration = end_perf - start_perf

            return ExecutionResult(
                query_id=query_id,
                thread_id=thread_id,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                result=None,
                error=str(e),
                is_success=False,
            )

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of all executions.

        Returns:
            Dictionary with timing and success statistics
        """
        if not self.results:
            return {}

        successful = [r for r in self.results if r.is_success]
        failed = [r for r in self.results if not r.is_success]

        durations = [r.duration_seconds for r in successful]
        total_duration = sum(durations)
        min_start = min(r.start_time for r in self.results)
        max_end = max(r.end_time for r in self.results)
        wall_clock_duration = (max_end - min_start).total_seconds()

        return {
            "total_executions": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "total_execution_time": total_duration,
            "wall_clock_time": wall_clock_duration,
            "speedup": (
                total_duration / wall_clock_duration if wall_clock_duration > 0 else 1.0
            ),
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
        }

    def print_results(self, verbose: bool = False) -> None:
        """
        Print execution results in a formatted way.

        Args:
            verbose: If True, print detailed information for each execution
        """
        summary = self.get_summary()

        print("\n" + "=" * 70)
        print("THREADPOOL EXECUTION SUMMARY")
        print("=" * 70)
        print(f"Total Executions:    {summary.get('total_executions', 0)}")
        print(f"Successful:          {summary.get('successful', 0)}")
        print(f"Failed:              {summary.get('failed', 0)}")
        print(f"Total Exec Time:     {summary.get('total_execution_time', 0):.3f}s")
        print(f"Wall Clock Time:     {summary.get('wall_clock_time', 0):.3f}s")
        print(f"Speedup Factor:      {summary.get('speedup', 1.0):.2f}x")
        print(f"Min Duration:        {summary.get('min_duration', 0):.3f}s")
        print(f"Max Duration:        {summary.get('max_duration', 0):.3f}s")
        print(f"Avg Duration:        {summary.get('avg_duration', 0):.3f}s")
        print("=" * 70)

        if verbose:
            print("\nDETAILED RESULTS:")
            print("-" * 70)
            for result in sorted(self.results, key=lambda r: r.start_time):
                status = "✓" if result.is_success else "✗"
                print(
                    f"{status} {result.query_id:20s} | "
                    f"Thread: {result.thread_id:8d} | "
                    f"Duration: {result.duration_seconds:8.3f}s"
                )
                if result.error:
                    print(f"  Error: {result.error}")
            print("-" * 70)
