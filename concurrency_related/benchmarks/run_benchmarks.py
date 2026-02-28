"""Benchmark runner for testing all concurrency methods."""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "concurrent_script"))
sys.path.insert(0, str(Path(__file__).parent.parent / "asyncio_script"))
sys.path.insert(0, str(Path(__file__).parent.parent / "multiprocessing_script"))
sys.path.insert(0, str(Path(__file__).parent.parent / "threading_script"))

from asyncio_executor import AsyncioQueryExecutor
from benchmark_tasks import BENCHMARK_TASKS
from multiprocessing_executor import MultiprocessingQueryExecutor
from threading_executor import ThreadingQueryExecutor
from threadpool_executor import ThreadPoolQueryExecutor

# Configure logger
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
)


class BenchmarkRunner:
    """Runs benchmarks across all concurrency methods."""

    def __init__(self, num_tasks: int = 10):
        """
        Initialize benchmark runner.

        Args:
            num_tasks: Number of concurrent tasks to run for each benchmark
        """
        self.num_tasks = num_tasks
        self.results = {}

    def run_threadpool(self, task_name: str, task_config: Dict) -> Dict[str, Any]:
        """Run benchmark with ThreadPoolExecutor."""
        logger.info(f"Running {task_name} with ThreadPoolExecutor...")

        executor = ThreadPoolQueryExecutor(max_workers=4, timeout=300.0)

        arguments_list = [task_config["default_args"](i) for i in range(self.num_tasks)]
        query_ids = [f"{task_name}_{i}" for i in range(self.num_tasks)]

        start = time.perf_counter()
        results = executor.execute_function_concurrent(
            function=task_config["function"],
            arguments_list=arguments_list,
            query_ids=query_ids,
        )
        total_time = time.perf_counter() - start

        summary = executor.get_summary()
        summary["total_wall_clock"] = total_time
        summary["method"] = "ThreadPoolExecutor"

        return summary

    async def run_asyncio(self, task_name: str, task_config: Dict) -> Dict[str, Any]:
        """Run benchmark with Asyncio."""
        logger.info(f"Running {task_name} with Asyncio...")

        # Create async wrapper for sync function
        async def async_wrapper(**kwargs):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, lambda: task_config["function"](**kwargs)
            )

        executor = AsyncioQueryExecutor(timeout=300.0)

        arguments_list = [task_config["default_args"](i) for i in range(self.num_tasks)]
        query_ids = [f"{task_name}_{i}" for i in range(self.num_tasks)]

        start = time.perf_counter()
        results = await executor.execute_function_concurrent(
            async_function=async_wrapper,
            arguments_list=arguments_list,
            query_ids=query_ids,
        )
        total_time = time.perf_counter() - start

        summary = executor.get_summary()
        summary["total_wall_clock"] = total_time
        summary["method"] = "Asyncio"

        return summary

    def run_multiprocessing(self, task_name: str, task_config: Dict) -> Dict[str, Any]:
        """Run benchmark with Multiprocessing."""
        logger.info(f"Running {task_name} with Multiprocessing...")

        executor = MultiprocessingQueryExecutor(max_workers=4, timeout=300.0)

        arguments_list = [task_config["default_args"](i) for i in range(self.num_tasks)]
        query_ids = [f"{task_name}_{i}" for i in range(self.num_tasks)]

        start = time.perf_counter()
        results = executor.execute_function_concurrent(
            function=task_config["function"],
            arguments_list=arguments_list,
            query_ids=query_ids,
        )
        total_time = time.perf_counter() - start

        summary = executor.get_summary()
        summary["total_wall_clock"] = total_time
        summary["method"] = "Multiprocessing"

        return summary

    def run_threading(self, task_name: str, task_config: Dict) -> Dict[str, Any]:
        """Run benchmark with Manual Threading."""
        logger.info(f"Running {task_name} with Threading...")

        executor = ThreadingQueryExecutor(max_workers=4, timeout=300.0)

        arguments_list = [task_config["default_args"](i) for i in range(self.num_tasks)]
        query_ids = [f"{task_name}_{i}" for i in range(self.num_tasks)]

        start = time.perf_counter()
        results = executor.execute_function_concurrent(
            function=task_config["function"],
            arguments_list=arguments_list,
            query_ids=query_ids,
        )
        total_time = time.perf_counter() - start

        summary = executor.get_summary()
        summary["total_wall_clock"] = total_time
        summary["method"] = "Threading"

        return summary

    def run_single_benchmark(self, task_name: str) -> Dict[str, Any]:
        """Run a single task across all concurrency methods."""
        if task_name not in BENCHMARK_TASKS:
            logger.error(f"Unknown task: {task_name}")
            return {}

        task_config = BENCHMARK_TASKS[task_name]
        logger.info(f"\n{'='*70}")
        logger.info(f"BENCHMARK: {task_config['name']} ({task_config['type'].upper()})")
        logger.info(f"{'='*70}")

        results = {
            "task_name": task_name,
            "task_display_name": task_config["name"],
            "task_type": task_config["type"],
            "num_tasks": self.num_tasks,
            "methods": {},
        }

        try:
            # ThreadPoolExecutor
            results["methods"]["threadpool"] = self.run_threadpool(
                task_name, task_config
            )
            time.sleep(0.5)  # Brief pause between methods

            # Asyncio
            results["methods"]["asyncio"] = asyncio.run(
                self.run_asyncio(task_name, task_config)
            )
            time.sleep(0.5)

            # Multiprocessing
            results["methods"]["multiprocessing"] = self.run_multiprocessing(
                task_name, task_config
            )
            time.sleep(0.5)

            # Threading
            results["methods"]["threading"] = self.run_threading(task_name, task_config)

        except Exception as e:
            logger.error(f"Error running benchmark {task_name}: {e}")
            import traceback

            traceback.print_exc()

        return results

    def run_all_benchmarks(self, task_names: List[str] = None) -> Dict[str, Any]:
        """Run all benchmarks."""
        if task_names is None:
            task_names = list(BENCHMARK_TASKS.keys())

        logger.info(f"\n{'#'*70}")
        logger.info(f"STARTING COMPREHENSIVE BENCHMARK SUITE")
        logger.info(
            f"Tasks: {len(task_names)} | Concurrent operations per task: {self.num_tasks}"
        )
        logger.info(f"{'#'*70}\n")

        start_time = datetime.now()
        all_results = {
            "metadata": {
                "start_time": start_time.isoformat(),
                "num_tasks": self.num_tasks,
                "tasks_benchmarked": len(task_names),
            },
            "benchmarks": {},
        }

        for task_name in task_names:
            result = self.run_single_benchmark(task_name)
            if result:
                all_results["benchmarks"][task_name] = result
            time.sleep(1)  # Pause between task types

        end_time = datetime.now()
        all_results["metadata"]["end_time"] = end_time.isoformat()
        all_results["metadata"]["total_duration_seconds"] = (
            end_time - start_time
        ).total_seconds()

        # Save results
        output_file = (
            Path(__file__).parent
            / f"benchmark_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=2)

        logger.success(f"\nBenchmark complete! Results saved to {output_file}")

        return all_results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a summary report from benchmark results."""
        report = []
        report.append("\n" + "=" * 80)
        report.append("CONCURRENCY BENCHMARK RESULTS")
        report.append("=" * 80)
        report.append(f"Date: {results['metadata']['start_time']}")
        report.append(
            f"Concurrent operations per task: {results['metadata']['num_tasks']}"
        )
        report.append(f"Total benchmarks: {results['metadata']['tasks_benchmarked']}")
        report.append(
            f"Total duration: {results['metadata']['total_duration_seconds']:.1f}s"
        )
        report.append("=" * 80 + "\n")

        # Group by task type
        by_type = {"io": [], "cpu": [], "mixed": []}
        for task_name, task_data in results["benchmarks"].items():
            by_type[task_data["task_type"]].append((task_name, task_data))

        for task_type, tasks in by_type.items():
            if not tasks:
                continue

            report.append(f"\n{task_type.upper()}-BOUND TASKS")
            report.append("-" * 80)

            for task_name, task_data in tasks:
                report.append(f"\n{task_data['task_display_name']}:")

                # Sort methods by speedup
                methods_sorted = sorted(
                    task_data["methods"].items(),
                    key=lambda x: x[1].get("speedup", 0),
                    reverse=True,
                )

                for method_name, method_data in methods_sorted:
                    speedup = method_data.get("speedup", 0)
                    wall_clock = method_data.get("wall_clock_time", 0)
                    successful = method_data.get("successful", 0)
                    failed = method_data.get("failed", 0)

                    report.append(
                        f"  {method_data['method']:20s} | "
                        f"Speedup: {speedup:5.2f}x | "
                        f"Time: {wall_clock:6.3f}s | "
                        f"Success: {successful}/{successful+failed}"
                    )

        # Summary table
        report.append("\n" + "=" * 80)
        report.append("OVERALL PERFORMANCE SUMMARY")
        report.append("=" * 80)
        report.append(f"{'Method':<20} | {'Avg Speedup':>12} | {'Best For'}")
        report.append("-" * 80)

        # Calculate average speedups
        method_speedups = {
            "threadpool": [],
            "asyncio": [],
            "multiprocessing": [],
            "threading": [],
        }
        for task_data in results["benchmarks"].values():
            for method_name, method_data in task_data["methods"].items():
                if "speedup" in method_data:
                    method_speedups[method_name].append(method_data["speedup"])

        for method, speedups in method_speedups.items():
            if speedups:
                avg_speedup = sum(speedups) / len(speedups)
                method_display = {
                    "threadpool": "ThreadPoolExecutor",
                    "asyncio": "Asyncio",
                    "multiprocessing": "Multiprocessing",
                    "threading": "Manual Threading",
                }[method]

                best_for = {
                    "threadpool": "Simple I/O tasks",
                    "asyncio": "High-concurrency I/O",
                    "multiprocessing": "CPU-intensive tasks",
                    "threading": "Custom worker patterns",
                }[method]

                report.append(
                    f"{method_display:<20} | {avg_speedup:>12.2f}x | {best_for}"
                )

        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Main entry point."""
    runner = BenchmarkRunner(num_tasks=10)

    # Run selected benchmarks (subset for faster testing)
    # Remove this filter to run ALL benchmarks
    task_selection = [
        "network_io",  # I/O
        "file_ops",  # I/O
        "prime_numbers",  # CPU
        "crypto_hash",  # CPU
        "fibonacci",  # CPU
        "data_processing",  # CPU
        "web_scraping",  # Mixed
        "etl_pipeline",  # Mixed
        "log_analysis",  # Mixed
        "ml_inference",  # Mixed
    ]

    results = runner.run_all_benchmarks(task_names=task_selection)

    # Generate and print report
    report = runner.generate_report(results)
    print(report)

    # Save report
    report_file = (
        Path(__file__).parent
        / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(report_file, "w") as f:
        f.write(report)

    logger.success(f"\nReport saved to {report_file}")


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    main()
