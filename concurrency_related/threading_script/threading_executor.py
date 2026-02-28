"""Threading-based concurrent query execution utilities using manual thread management."""

import queue
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger


class ThreadingExecutionError(Exception):
    """Custom exception for threading execution errors."""

    pass


@dataclass
class ExecutionResult:
    """Result of a query execution."""

    query_id: str
    thread_id: int
    thread_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    result: Any
    error: Optional[str] = None
    is_success: bool = True


class ThreadingQueryExecutor:
    """Executor for running queries concurrently using manual thread management."""

    def __init__(self, max_workers: int = 5, timeout: Optional[float] = None):
        """
        Initialize threading executor.

        Args:
            max_workers: Maximum number of worker threads
            timeout: Timeout per query execution in seconds
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self.results: List[ExecutionResult] = []
        self.results_lock = threading.Lock()

    def execute_function_concurrent(
        self,
        function: Callable,
        arguments_list: List[Dict[str, Any]],
        query_ids: Optional[List[str]] = None,
    ) -> List[ExecutionResult]:
        """
        Execute a function concurrently across multiple argument sets using threads.

        Args:
            function: Callable that accepts keyword arguments
            arguments_list: List of dicts containing function arguments
            query_ids: Optional list of identifiers for each execution

        Returns:
            List of ExecutionResult objects

        Raises:
            ThreadingExecutionError: If execution fails
        """
        if not arguments_list:
            raise ThreadingExecutionError("arguments_list cannot be empty")

        # Reset results
        self.results = []

        # Create a queue for work items
        work_queue = queue.Queue()

        # Populate the queue
        for i, args in enumerate(arguments_list):
            query_id = query_ids[i] if query_ids else f"query_{i}"
            work_queue.put((query_id, args))

        # Create and start worker threads
        threads = []
        num_threads = min(self.max_workers, len(arguments_list))

        for i in range(num_threads):
            thread = threading.Thread(
                target=self._worker,
                args=(function, work_queue),
                name=f"Worker-{i}",
                daemon=False,
            )
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            if self.timeout:
                thread.join(timeout=self.timeout * len(arguments_list))
            else:
                thread.join()

        # Check if any threads are still alive (timeout)
        alive_threads = [t for t in threads if t.is_alive()]
        if alive_threads:
            logger.warning(f"{len(alive_threads)} threads still running after timeout")

        return self.results

    def _worker(self, function: Callable, work_queue: queue.Queue) -> None:
        """
        Worker thread that processes items from the queue.

        Args:
            function: Callable to execute
            work_queue: Queue containing work items
        """
        while True:
            try:
                # Get work item with timeout
                query_id, kwargs = work_queue.get(block=True, timeout=0.1)
            except queue.Empty:
                break

            try:
                result = self._run_task(function, query_id, kwargs)
                with self.results_lock:
                    self.results.append(result)
            except Exception as e:
                logger.error(f"Worker error for {query_id}: {e}")
            finally:
                work_queue.task_done()

    def _run_task(
        self, function: Callable, query_id: str, kwargs: Dict[str, Any]
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
        thread = threading.current_thread()
        thread_id = threading.get_ident()
        thread_name = thread.name
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
                thread_name=thread_name,
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
                thread_name=thread_name,
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
        logger.info("THREADING EXECUTION SUMMARY")
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
                    f"Thread: {result.thread_name:12s} | "
                    f"Duration: {result.duration_seconds:8.3f}s"
                )
                if result.error:
                    logger.error(f"  Error: {result.error}")
            logger.info("-" * 70)
