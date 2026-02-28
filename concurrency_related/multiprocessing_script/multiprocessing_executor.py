"""Multiprocessing-based concurrent query execution utilities."""

import multiprocessing
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger


class MultiprocessingExecutionError(Exception):
    """Custom exception for multiprocessing execution errors."""

    pass


@dataclass
class ExecutionResult:
    """Result of a query execution."""

    query_id: str
    process_id: int
    process_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    result: Any
    error: Optional[str] = None
    is_success: bool = True


def _worker_function(
    function: Callable, query_id: str, kwargs: Dict[str, Any]
) -> ExecutionResult:
    """
    Worker function to run in separate process.

    Args:
        function: Callable to execute
        query_id: Identifier for this execution
        kwargs: Keyword arguments for function

    Returns:
        ExecutionResult with metrics
    """
    process = multiprocessing.current_process()
    process_id = process.pid
    process_name = process.name
    start_time = datetime.now()
    start_perf = time.perf_counter()

    try:
        result = function(**kwargs)
        end_perf = time.perf_counter()
        end_time = datetime.now()
        duration = end_perf - start_perf

        return ExecutionResult(
            query_id=query_id,
            process_id=process_id,
            process_name=process_name,
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
            process_id=process_id,
            process_name=process_name,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            result=None,
            error=str(e),
            is_success=False,
        )


class MultiprocessingQueryExecutor:
    """Executor for running queries concurrently using multiprocessing.Pool."""

    def __init__(self, max_workers: int = None, timeout: Optional[float] = None):
        """
        Initialize multiprocessing executor.

        Args:
            max_workers: Maximum number of worker processes (default: CPU count)
            timeout: Timeout per query execution in seconds
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.timeout = timeout
        self.results: List[ExecutionResult] = []

    def execute_function_concurrent(
        self,
        function: Callable,
        arguments_list: List[Dict[str, Any]],
        query_ids: Optional[List[str]] = None,
    ) -> List[ExecutionResult]:
        """
        Execute a function concurrently across multiple argument sets using processes.

        Args:
            function: Callable that accepts keyword arguments
            arguments_list: List of dicts containing function arguments
            query_ids: Optional list of identifiers for each execution

        Returns:
            List of ExecutionResult objects

        Raises:
            MultiprocessingExecutionError: If execution fails
        """
        if not arguments_list:
            raise MultiprocessingExecutionError("arguments_list cannot be empty")

        results = []

        try:
            with multiprocessing.Pool(processes=self.max_workers) as pool:
                # Create async results for all tasks
                async_results = []
                for i, args in enumerate(arguments_list):
                    query_id = query_ids[i] if query_ids else f"query_{i}"
                    async_result = pool.apply_async(
                        _worker_function, (function, query_id, args)
                    )
                    async_results.append((i, query_id, async_result))

                # Collect results
                for i, query_id, async_result in async_results:
                    try:
                        result = async_result.get(timeout=self.timeout)
                        results.append(result)
                    except multiprocessing.TimeoutError:
                        results.append(
                            ExecutionResult(
                                query_id=query_id,
                                process_id=0,
                                process_name="timeout",
                                start_time=datetime.now(),
                                end_time=datetime.now(),
                                duration_seconds=0,
                                result=None,
                                error=f"Timeout after {self.timeout}s",
                                is_success=False,
                            )
                        )
                    except Exception as e:
                        results.append(
                            ExecutionResult(
                                query_id=query_id,
                                process_id=0,
                                process_name="error",
                                start_time=datetime.now(),
                                end_time=datetime.now(),
                                duration_seconds=0,
                                result=None,
                                error=str(e),
                                is_success=False,
                            )
                        )

        except Exception as e:
            raise MultiprocessingExecutionError(
                f"Multiprocessing execution failed: {e}"
            )

        self.results = results
        return results

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

        logger.info("\n" + "=" * 70)
        logger.info("MULTIPROCESSING EXECUTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total Executions:    {summary.get('total_executions', 0)}")
        logger.info(f"Successful:          {summary.get('successful', 0)}")
        logger.info(f"Failed:              {summary.get('failed', 0)}")
        logger.info(
            f"Total Exec Time:     {summary.get('total_execution_time', 0):.3f}s"
        )
        logger.info(f"Wall Clock Time:     {summary.get('wall_clock_time', 0):.3f}s")
        logger.info(f"Speedup Factor:      {summary.get('speedup', 1.0):.2f}x")
        logger.info(f"Min Duration:        {summary.get('min_duration', 0):.3f}s")
        logger.info(f"Max Duration:        {summary.get('max_duration', 0):.3f}s")
        logger.info(f"Avg Duration:        {summary.get('avg_duration', 0):.3f}s")
        logger.info("=" * 70)

        if verbose:
            logger.info("\nDETAILED RESULTS:")
            logger.info("-" * 70)
            for result in sorted(self.results, key=lambda r: r.start_time):
                status = "✓" if result.is_success else "✗"
                logger.info(
                    f"{status} {result.query_id:20s} | "
                    f"PID: {result.process_id:8d} | "
                    f"Duration: {result.duration_seconds:8.3f}s"
                )
                if result.error:
                    logger.error(f"  Error: {result.error}")
            logger.info("-" * 70)
