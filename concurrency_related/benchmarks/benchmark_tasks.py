"""Benchmark tasks for testing concurrency methods."""

import hashlib
import math
import random
import time
from pathlib import Path
from typing import Any, Dict

# Task parameters
BENCHMARK_DATA_DIR = Path(__file__).parent / "test_data"


# ============================================================================
# I/O-BOUND TASKS
# ============================================================================


def task_file_operations(file_id: int, size_kb: int = 100) -> Dict[str, Any]:
    """
    Task 3: File Operations - Read/write files.

    Args:
        file_id: Unique file identifier
        size_kb: Size of file in KB

    Returns:
        Dict with results
    """
    BENCHMARK_DATA_DIR.mkdir(exist_ok=True)
    filepath = BENCHMARK_DATA_DIR / f"test_file_{file_id}.txt"

    # Write file
    data = "x" * (size_kb * 1024)
    start_write = time.perf_counter()
    with open(filepath, "w") as f:
        f.write(data)
    write_time = time.perf_counter() - start_write

    # Read file
    start_read = time.perf_counter()
    with open(filepath, "r") as f:
        content = f.read()
    read_time = time.perf_counter() - start_read

    # Cleanup
    filepath.unlink()

    return {
        "file_id": file_id,
        "size_kb": size_kb,
        "write_time": write_time,
        "read_time": read_time,
        "total_time": write_time + read_time,
        "bytes_processed": len(content),
    }


def task_simulated_network_io(request_id: int, delay_ms: int = 100) -> Dict[str, Any]:
    """
    Task 1/4/5: Simulated network I/O (HTTP requests, API calls, sockets).

    Args:
        request_id: Unique request identifier
        delay_ms: Simulated network latency in milliseconds

    Returns:
        Dict with results
    """
    start = time.perf_counter()

    # Simulate network latency
    time.sleep(delay_ms / 1000.0)

    # Simulate some data processing
    result = sum(i * i for i in range(1000))

    duration = time.perf_counter() - start

    return {
        "request_id": request_id,
        "delay_ms": delay_ms,
        "duration": duration,
        "result": result,
        "timestamp": time.time(),
    }


# ============================================================================
# CPU-BOUND TASKS
# ============================================================================


def task_prime_numbers(n: int, max_num: int = 50000) -> Dict[str, Any]:
    """
    Task 6: Prime Number Generation.

    Args:
        n: Task identifier
        max_num: Find primes up to this number

    Returns:
        Dict with prime count and timing
    """
    start = time.perf_counter()

    primes = []
    for num in range(2, max_num):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    duration = time.perf_counter() - start

    return {
        "task_id": n,
        "max_num": max_num,
        "prime_count": len(primes),
        "duration": duration,
        "primes_per_sec": len(primes) / duration if duration > 0 else 0,
    }


def task_cryptographic_hashing(task_id: int, num_hashes: int = 1000) -> Dict[str, Any]:
    """
    Task 8: Cryptographic Hashing with SHA-256.

    Args:
        task_id: Task identifier
        num_hashes: Number of strings to hash

    Returns:
        Dict with hash count and timing
    """
    start = time.perf_counter()

    hashes = []
    for i in range(num_hashes):
        data = f"task_{task_id}_string_{i}".encode()
        hash_obj = hashlib.sha256(data)
        hashes.append(hash_obj.hexdigest())

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_hashes": num_hashes,
        "duration": duration,
        "hashes_per_sec": num_hashes / duration if duration > 0 else 0,
        "sample_hash": hashes[0] if hashes else None,
    }


def task_fibonacci(task_id: int, n: int = 30) -> Dict[str, Any]:
    """
    Task 10: Mathematical Computation - Fibonacci calculation.

    Args:
        task_id: Task identifier
        n: Fibonacci number to calculate

    Returns:
        Dict with result and timing
    """
    start = time.perf_counter()

    def fib(x):
        if x <= 1:
            return x
        return fib(x - 1) + fib(x - 2)

    result = fib(n)
    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "n": n,
        "result": result,
        "duration": duration,
    }


def task_data_processing(task_id: int, num_rows: int = 100000) -> Dict[str, Any]:
    """
    Task 9: Data Processing - Sort, filter, aggregate operations.

    Args:
        task_id: Task identifier
        num_rows: Number of data rows to process

    Returns:
        Dict with processing stats
    """
    start = time.perf_counter()

    # Generate random data
    data = [
        {
            "id": i,
            "value": random.randint(1, 1000),
            "category": random.choice(["A", "B", "C"]),
        }
        for i in range(num_rows)
    ]

    # Sort by value
    sorted_data = sorted(data, key=lambda x: x["value"])

    # Filter high values
    filtered = [d for d in sorted_data if d["value"] > 500]

    # Aggregate by category
    aggregates = {}
    for item in filtered:
        cat = item["category"]
        if cat not in aggregates:
            aggregates[cat] = {"count": 0, "sum": 0}
        aggregates[cat]["count"] += 1
        aggregates[cat]["sum"] += item["value"]

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_rows": num_rows,
        "filtered_count": len(filtered),
        "categories": len(aggregates),
        "duration": duration,
        "rows_per_sec": num_rows / duration if duration > 0 else 0,
    }


# ============================================================================
# MIXED WORKLOAD TASKS
# ============================================================================


def task_simulated_web_scraping(task_id: int, num_items: int = 50) -> Dict[str, Any]:
    """
    Task 11: Web Scraping simulation - Fetch + Parse + Extract.

    Args:
        task_id: Task identifier
        num_items: Number of items to scrape

    Returns:
        Dict with scraping stats
    """
    start = time.perf_counter()

    results = []
    for i in range(num_items):
        # Simulate network fetch (I/O)
        time.sleep(0.01)

        # Simulate HTML parsing (CPU)
        html = f"<html><body><div>Item {i}</div></body></html>" * 100
        parsed = html.count("div")

        results.append({"item": i, "divs": parsed})

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_items": num_items,
        "items_scraped": len(results),
        "duration": duration,
        "items_per_sec": num_items / duration if duration > 0 else 0,
    }


def task_etl_pipeline(task_id: int, num_records: int = 100) -> Dict[str, Any]:
    """
    Task 12: ETL Pipeline simulation - Extract, Transform, Load.

    Args:
        task_id: Task identifier
        num_records: Number of records to process

    Returns:
        Dict with ETL stats
    """
    start = time.perf_counter()

    # Extract (I/O simulation)
    time.sleep(0.05)
    extracted = [
        {"id": i, "raw_value": random.random() * 100} for i in range(num_records)
    ]

    # Transform (CPU)
    transformed = []
    for record in extracted:
        transformed.append(
            {
                "id": record["id"],
                "value": round(record["raw_value"], 2),
                "category": "high" if record["raw_value"] > 50 else "low",
                "hash": hashlib.md5(str(record["id"]).encode()).hexdigest()[:8],
            }
        )

    # Load (I/O simulation)
    time.sleep(0.05)

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_records": num_records,
        "records_processed": len(transformed),
        "duration": duration,
        "records_per_sec": num_records / duration if duration > 0 else 0,
    }


def task_log_analysis(task_id: int, num_lines: int = 10000) -> Dict[str, Any]:
    """
    Task 14: Log Analysis - Read, Parse, Aggregate.

    Args:
        task_id: Task identifier
        num_lines: Number of log lines to analyze

    Returns:
        Dict with analysis results
    """
    start = time.perf_counter()

    # Generate log data
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    logs = [f"{random.choice(log_levels)} - Message {i}" for i in range(num_lines)]

    # Parse and aggregate
    stats = {"INFO": 0, "WARNING": 0, "ERROR": 0, "DEBUG": 0}
    for log in logs:
        for level in log_levels:
            if level in log:
                stats[level] += 1
                break

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_lines": num_lines,
        "stats": stats,
        "duration": duration,
        "lines_per_sec": num_lines / duration if duration > 0 else 0,
    }


def task_ml_inference_simulation(
    task_id: int, num_samples: int = 100
) -> Dict[str, Any]:
    """
    Task 15: ML Inference simulation - Preprocessing + Prediction.

    Args:
        task_id: Task identifier
        num_samples: Number of samples to process

    Returns:
        Dict with inference stats
    """
    start = time.perf_counter()

    # Generate sample data
    samples = [[random.random() for _ in range(10)] for _ in range(num_samples)]

    # Simulate preprocessing
    preprocessed = []
    for sample in samples:
        normalized = [(x - 0.5) * 2 for x in sample]  # Normalize to [-1, 1]
        preprocessed.append(normalized)

    # Simulate inference (matrix multiplication)
    predictions = []
    weights = [random.random() for _ in range(10)]
    for sample in preprocessed:
        pred = sum(s * w for s, w in zip(sample, weights))
        predictions.append(1 if pred > 0 else 0)

    duration = time.perf_counter() - start

    return {
        "task_id": task_id,
        "num_samples": num_samples,
        "predictions": predictions[:5],  # Sample predictions
        "positive_rate": sum(predictions) / len(predictions) if predictions else 0,
        "duration": duration,
        "samples_per_sec": num_samples / duration if duration > 0 else 0,
    }


# ============================================================================
# TASK REGISTRY
# ============================================================================

BENCHMARK_TASKS = {
    # I/O-Bound
    "file_ops": {
        "name": "File Operations",
        "function": task_file_operations,
        "type": "io",
        "default_args": lambda i: {"file_id": i, "size_kb": 100},
    },
    "network_io": {
        "name": "Network I/O Simulation",
        "function": task_simulated_network_io,
        "type": "io",
        "default_args": lambda i: {"request_id": i, "delay_ms": 50},
    },
    # CPU-Bound
    "prime_numbers": {
        "name": "Prime Number Generation",
        "function": task_prime_numbers,
        "type": "cpu",
        "default_args": lambda i: {"n": i, "max_num": 10000},
    },
    "crypto_hash": {
        "name": "Cryptographic Hashing",
        "function": task_cryptographic_hashing,
        "type": "cpu",
        "default_args": lambda i: {"task_id": i, "num_hashes": 500},
    },
    "fibonacci": {
        "name": "Fibonacci Calculation",
        "function": task_fibonacci,
        "type": "cpu",
        "default_args": lambda i: {"task_id": i, "n": 28},
    },
    "data_processing": {
        "name": "Data Processing",
        "function": task_data_processing,
        "type": "cpu",
        "default_args": lambda i: {"task_id": i, "num_rows": 50000},
    },
    # Mixed
    "web_scraping": {
        "name": "Web Scraping Simulation",
        "function": task_simulated_web_scraping,
        "type": "mixed",
        "default_args": lambda i: {"task_id": i, "num_items": 30},
    },
    "etl_pipeline": {
        "name": "ETL Pipeline",
        "function": task_etl_pipeline,
        "type": "mixed",
        "default_args": lambda i: {"task_id": i, "num_records": 100},
    },
    "log_analysis": {
        "name": "Log Analysis",
        "function": task_log_analysis,
        "type": "mixed",
        "default_args": lambda i: {"task_id": i, "num_lines": 5000},
    },
    "ml_inference": {
        "name": "ML Inference Simulation",
        "function": task_ml_inference_simulation,
        "type": "mixed",
        "default_args": lambda i: {"task_id": i, "num_samples": 100},
    },
}
