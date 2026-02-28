"""
Example: Concurrent Query Execution with ThreadPool

This example demonstrates concurrent query execution using ThreadPoolExecutor
with both SQLAlchemy and test functions.

Set environment variables before running:
    export TERADATA_HOST=your_host
    export TERADATA_USER=your_user
    export TERADATA_PASSWORD=your_password
"""

import sys
import time
from pathlib import Path
from typing import Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import DatabaseConfig, SQLAlchemyClient, ThreadPoolQueryExecutor


def example_concurrent_simple_functions():
    """Example 1: Concurrent execution with simple functions."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Concurrent Execution with Simple Functions")
    print("=" * 70)

    def slow_computation(task_id: int, iterations: int = 1000000) -> int:
        """Simulate some CPU work."""
        result = 0
        for i in range(iterations):
            result += i
        return result

    print("\nExecuting 5 computational tasks concurrently...")
    print("Each task computes sum of 0 to 1,000,000")

    # Prepare arguments for concurrent execution
    tasks = [{"task_id": i, "iterations": 1000000} for i in range(5)]
    query_ids = [f"task_{i}" for i in range(5)]

    # Execute concurrently
    executor = ThreadPoolQueryExecutor(max_workers=3, timeout=30)
    results = executor.execute_function_concurrent(slow_computation, tasks, query_ids)

    # Print results
    executor.print_results(verbose=True)

    print("\n✓ Concurrent execution completed successfully")


def example_concurrent_database_queries():
    """Example 2: Concurrent database queries."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Concurrent Database Queries with SQLAlchemy")
    print("=" * 70)

    def execute_single_query(client: SQLAlchemyClient, query: str) -> Any:
        """Helper function to execute a query."""
        return client.execute_query(query)

    try:
        # Create client with pool for concurrent access
        config = DatabaseConfig.from_env()
        client = SQLAlchemyClient(config, pool_size=10, max_overflow=5)

        # Define multiple queries to run concurrently
        queries = [
            "SELECT COUNT(*) AS cnt FROM DBC.TablesV WHERE DataBaseName = 'DBC'",
            "SELECT COUNT(*) AS cnt FROM DBC.ColumnsV WHERE DatabaseName = 'DBC'",
            "SELECT COUNT(*) AS cnt FROM DBC.DatabasesV",
            "SELECT TopNumber FROM DBC.DiskSpace LIMIT 5",
            "SELECT COUNT(*) AS cnt FROM DBC.AllRights",
        ]

        print(f"\nExecuting {len(queries)} database queries concurrently...")
        print("Queries run in parallel using threading\n")

        # Prepare function calls
        tasks = [{"client": client, "query": q} for q in queries]
        query_ids = [f"db_query_{i}" for i in range(len(queries))]

        # Execute concurrently
        executor = ThreadPoolQueryExecutor(max_workers=5, timeout=60)
        results = executor.execute_function_concurrent(
            execute_single_query,
            tasks,
            query_ids,
        )

        # Print summary
        executor.print_results(verbose=False)

        print("\nDetailed Results:")
        for result in results:
            if result.is_success:
                rows_count = len(result.result) if result.result is not None else 0
                print(
                    f"  ✓ {result.query_id}: {rows_count} rows "
                    f"({result.duration_seconds:.3f}s)"
                )
            else:
                print(f"  ✗ {result.query_id}: Error - {result.error}")

        client.close()

    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")


def example_sequential_vs_concurrent():
    """Example 3: Compare sequential vs concurrent execution."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Sequential vs Concurrent Performance")
    print("=" * 70)

    def slow_task(task_id: int, duration: float = 0.5) -> str:
        """Simulate I/O work (sleeping)."""
        time.sleep(duration)
        return f"Task {task_id} completed"

    num_tasks = 5
    task_duration = 0.5

    # Sequential execution
    print(
        f"\nSequential: {num_tasks} tasks × {task_duration}s = expected ~{num_tasks * task_duration}s"
    )
    start = time.time()
    for i in range(num_tasks):
        slow_task(i, task_duration)
    sequential_time = time.time() - start

    print(f"  Actual time: {sequential_time:.2f}s")

    # Concurrent execution
    print(f"\nConcurrent: {num_tasks} tasks, {3} workers")
    tasks = [{"task_id": i, "duration": task_duration} for i in range(num_tasks)]
    executor = ThreadPoolQueryExecutor(max_workers=3)

    start = time.time()
    results = executor.execute_function_concurrent(slow_task, tasks)
    concurrent_time = time.time() - start

    executor.print_results(verbose=False)

    # Calculate speedup
    speedup = sequential_time / concurrent_time
    print(f"\n✓ Speedup: {speedup:.2f}x faster with concurrent execution")
    print(f"  Sequential: {sequential_time:.2f}s")
    print(f"  Concurrent: {concurrent_time:.2f}s")


def example_error_resilience():
    """Example 4: Error handling in concurrent execution."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Error Resilience")
    print("=" * 70)

    def task_with_errors(task_id: int, fail_on: int = -1) -> int:
        """Task that may fail on specific IDs."""
        if task_id == fail_on:
            raise ValueError(f"Task {task_id} intentionally failed")
        return task_id * 100

    print("\nExecuting 5 tasks where task #2 fails...")
    tasks = [{"task_id": i, "fail_on": 2} for i in range(5)]

    executor = ThreadPoolQueryExecutor(max_workers=3)
    results = executor.execute_function_concurrent(task_with_errors, tasks)

    executor.print_results(verbose=True)

    print("\n✓ Other tasks continue despite failures")


if __name__ == "__main__":
    print("ThreadPool Concurrent Execution Examples")
    print("=" * 70)
    print("\nExamples include:")
    print("  1. Simple concurrent computations")
    print("  2. Concurrent database queries (requires connection)")
    print("  3. Sequential vs Concurrent performance comparison")
    print("  4. Error resilience in concurrent execution")

    # Uncomment to run examples:
    example_concurrent_simple_functions()
    # example_concurrent_database_queries()
    example_sequential_vs_concurrent()
    example_error_resilience()

    print("\n✓ All examples completed.")
