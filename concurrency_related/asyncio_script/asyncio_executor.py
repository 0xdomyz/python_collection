"""Asyncio-based concurrent query execution utilities."""

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, List, Optional

from loguru import logger


class AsyncioExecutionError(Exception):
    """Custom exception for asyncio execution errors."""

    pass


@dataclass
class ExecutionResult:
    """Result of a query execution."""

    query_id: str
    task_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    result: Any
    error: Optional[str] = None
    is_success: bool = True


class AsyncioQueryExecutor:
    """Executor for running async queries concurrently using asyncio."""

    def __init__(self, timeout: Optional[float] = None):
        """
        Initialize asyncio executor.

        Args:
            timeout: Timeout per query execution in seconds
        """
        self.timeout = timeout
        self.results: List[ExecutionResult] = []

    async def execute_function_concurrent(
        self,
        async_function: Callable[..., Coroutine],
        arguments_list: List[Dict[str, Any]],
        query_ids: Optional[List[str]] = None,
    ) -> List[ExecutionResult]:
        """
        Execute an async function concurrently across multiple argument sets.

        Args:
            async_function: Async callable that accepts keyword arguments
            arguments_list: List of dicts containing function arguments
            query_ids: Optional list of identifiers for each execution

        Returns:
            List of ExecutionResult objects

        Raises:
            AsyncioExecutionError: If execution fails
        """
        if not arguments_list:
            raise AsyncioExecutionError("arguments_list cannot be empty")

        try:
            # Create tasks for all executions
            tasks = []
            for i, args in enumerate(arguments_list):
                query_id = query_ids[i] if query_ids else f"query_{i}"
                task = self._run_task(async_function, query_id, args)
                tasks.append(task)

            # Gather all results
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results and handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    query_id = query_ids[i] if query_ids else f"query_{i}"
                    processed_results.append(
                        ExecutionResult(
                            query_id=query_id,
                            task_name=f"task_{i}",
                            start_time=datetime.now(),
                            end_time=datetime.now(),
                            duration_seconds=0,
                            result=None,
                            error=str(result),
                            is_success=False,
                        )
                    )
                else:
                    processed_results.append(result)

            self.results = processed_results
            return processed_results

        except Exception as e:
            raise AsyncioExecutionError(f"Asyncio execution failed: {e}")

    async def _run_task(
        self,
        async_function: Callable[..., Coroutine],
        query_id: str,
        kwargs: Dict[str, Any],
    ) -> ExecutionResult:
        """
        Run a single async task and measure execution metrics.

        Args:
            async_function: Async callable to execute
            query_id: Identifier for this execution
            kwargs: Keyword arguments for function

        Returns:
            ExecutionResult with metrics
        """
        task_name = (
            asyncio.current_task().get_name() if asyncio.current_task() else "unknown"
        )
        start_time = datetime.now()
        start_perf = time.perf_counter()

        try:
            if self.timeout:
                result = await asyncio.wait_for(
                    async_function(**kwargs), timeout=self.timeout
                )
            else:
                result = await async_function(**kwargs)

            end_perf = time.perf_counter()
            end_time = datetime.now()
            duration = end_perf - start_perf

            return ExecutionResult(
                query_id=query_id,
                task_name=task_name,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                result=result,
                error=None,
                is_success=True,
            )
        except asyncio.TimeoutError:
            end_perf = time.perf_counter()
            end_time = datetime.now()
            duration = end_perf - start_perf

            return ExecutionResult(
                query_id=query_id,
                task_name=task_name,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration,
                result=None,
                error=f"Timeout after {self.timeout}s",
                is_success=False,
            )
        except Exception as e:
            end_perf = time.perf_counter()
            end_time = datetime.now()
            duration = end_perf - start_perf

            return ExecutionResult(
                query_id=query_id,
                task_name=task_name,
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

        logger.info("\n" + "=" * 70)
        logger.info("ASYNCIO EXECUTION SUMMARY")
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
                    f"Task: {result.task_name:15s} | "
                    f"Duration: {result.duration_seconds:8.3f}s"
                )
                if result.error:
                    logger.error(f"  Error: {result.error}")
            logger.info("-" * 70)
