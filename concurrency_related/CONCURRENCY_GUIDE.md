# Python Concurrency Methods - Comprehensive Guide

## Overview

This guide covers four approaches to concurrent execution in Python, with practical examples and performance benchmarks.

---

## 1. ThreadPoolExecutor (High-level Thread Pool)

### Key Mechanism
```python
with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    # Submit all tasks → returns Future objects
    future_to_index = {}
    for i, args in enumerate(arguments_list):
        future = executor.submit(self._run_task, function, query_id, args)
        future_to_index[future] = i
    
    # Collect results as they complete (non-blocking wait)
    for future in as_completed(future_to_index, timeout=self.timeout):
        result = future.result(timeout=self.timeout)
        results.append(result)
```

**How it works**: Pool manages threads internally, `submit()` schedules work, `as_completed()` yields futures as they finish.

### Best For ✅
- **I/O-bound operations**: Network requests, file operations, database queries
- **Moderate concurrency**: 5-50 concurrent operations
- **Simple use cases**: Minimal setup, easy to understand
- **Mixed task durations**: `as_completed()` handles varying execution times efficiently
- **When you need**: Straightforward API with minimal boilerplate

### Not Ideal For ❌
- **CPU-bound tasks**: Limited by GIL (Global Interpreter Lock)
- **Very high concurrency**: Thread overhead becomes significant (>100 threads)
- **Real-time requirements**: Thread scheduling is non-deterministic
- **Memory-intensive tasks**: Each thread has its own stack (~8MB on Linux)

### Example Use Cases
- Making multiple HTTP API calls
- Reading/writing multiple files concurrently
- Database connection pooling and query execution
- Downloading multiple images or files
- Parallel web scraping (with rate limiting)

---

## 2. Asyncio (Event Loop Coroutines)

### Key Mechanism
```python
# Create coroutines and gather them on the event loop
tasks = []
for i, args in enumerate(arguments_list):
    task = self._run_task(async_function, query_id, args)  # Creates coroutine
    tasks.append(task)

# Gather all results - single event loop schedules all tasks
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**How it works**: Single-threaded event loop, `gather()` schedules all coroutines concurrently, switches between them at `await` points.

### Best For ✅
- **High-concurrency I/O**: Thousands of concurrent connections
- **Network-heavy applications**: Web servers, API clients, WebSocket handlers
- **Long-lived connections**: Chat servers, streaming data
- **Async libraries available**: aiohttp, aiofiles, asyncpg, etc.
- **Cooperative multitasking**: Fine-grained control over task switching
- **Memory efficiency**: Coroutines are much lighter than threads

### Not Ideal For ❌
- **CPU-bound tasks**: Still bound by GIL, single-threaded execution
- **Blocking I/O calls**: Must use async libraries only (no standard `requests`, `sqlite3`, etc.)
- **Legacy code integration**: Requires async/await throughout the call stack
- **Simple scripts**: More complex syntax and mental model
- **Synchronous libraries**: Need to wrap in `run_in_executor()`

### Example Use Cases
- High-performance web servers (FastAPI, aiohttp)
- Concurrent API aggregation (calling 1000s of endpoints)
- Real-time data streaming and processing
- WebSocket servers handling many connections
- Async database operations with asyncpg, motor
- Concurrent file operations with aiofiles

---

## 3. Multiprocessing (Process Pool)

### Key Mechanism
```python
# Spawn processes and use async apply for non-blocking dispatch
with multiprocessing.Pool(processes=self.max_workers) as pool:
    # Apply async → returns AsyncResult objects (non-blocking)
    async_results = []
    for i, args in enumerate(arguments_list):
        async_result = pool.apply_async(
            _worker_function, (function, query_id, args)
        )
        async_results.append((i, query_id, async_result))
    
    # Collect results (blocking wait with timeout)
    for i, query_id, async_result in async_results:
        result = async_result.get(timeout=self.timeout)
        results.append(result)
```

**How it works**: Separate OS processes (bypasses GIL), `apply_async()` dispatches to workers, `get()` blocks until result ready.

### Best For ✅
- **CPU-bound tasks**: Computation, data processing, mathematical operations
- **True parallelism**: Bypass GIL, use multiple CPU cores
- **Independent tasks**: No shared state needed
- **Large data processing**: Divide-and-conquer strategies
- **Isolated execution**: Each process has separate memory space
- **CPU-intensive algorithms**: Machine learning, image processing, scientific computing

### Not Ideal For ❌
- **Shared state**: Requires IPC (Inter-Process Communication) - complex and slow
- **Small tasks**: Process creation overhead is significant (~100ms per process)
- **Memory-intensive**: Each process duplicates Python interpreter and data
- **Quick iterations**: Startup cost makes it slower for small workloads
- **I/O-bound tasks**: Overhead outweighs benefits (use threads/asyncio instead)

### Example Use Cases
- Parallel data processing (pandas DataFrames, numpy arrays)
- Image/video processing pipelines
- Machine learning model training/inference
- Scientific simulations and Monte Carlo methods
- Cryptographic operations (hashing, encryption)
- Batch processing of large datasets

---

## 4. Manual Threading (Queue-based Workers)

### Key Mechanism
```python
# Producer-consumer pattern with thread-safe queue
work_queue = queue.Queue()

# Populate queue (producer)
for i, args in enumerate(arguments_list):
    work_queue.put((query_id, args))

# Create and start worker threads (consumers)
threads = []
for i in range(num_threads):
    thread = threading.Thread(
        target=self._worker,  # Worker pulls from queue in loop
        args=(function, work_queue),
        daemon=False
    )
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
```

**How it works**: Thread-safe `Queue` for work distribution, workers pull tasks in loop, `join()` waits for completion.

### Best For ✅
- **Custom worker patterns**: Fine-grained control over thread behavior
- **Long-running workers**: Keep threads alive between tasks
- **Priority queues**: Use `PriorityQueue` for task ordering
- **Complex coordination**: Custom synchronization with locks, events, conditions
- **Educational purposes**: Understanding threading fundamentals
- **Specific thread lifecycles**: Control thread creation/destruction manually

### Not Ideal For ❌
- **Simple use cases**: ThreadPoolExecutor is easier and safer
- **Beginners**: More complex, error-prone (race conditions, deadlocks)
- **Maintenance**: More code to write and debug
- **CPU-bound tasks**: Still limited by GIL like ThreadPoolExecutor

### Example Use Cases
- Custom worker pools with specialized behavior
- Thread-safe producer-consumer pipelines
- Task prioritization systems
- Background job processors
- Rate-limited API consumers
- Custom thread pool implementations

---

## Performance Comparison (Benchmark Results)

| Method | Speedup | Overhead | Best Concurrency | Memory Usage |
|--------|---------|----------|------------------|--------------|
| **Asyncio** | 4.13x | Low | 1,000-10,000+ | Very Low |
| **Multiprocessing** | 3.82x | High | # of CPUs | High |
| **Manual Threading** | 3.01x | Medium | 10-100 | Medium |
| **ThreadPoolExecutor** | 3.00x | Low | 10-100 | Medium |

*Benchmark: 8 SQLite queries with artificial delays (0.05s-0.3s)*

---

## Benchmark Task Ideas

### I/O-Bound Tasks (Good for Threads/Asyncio)

1. **HTTP Requests**
   - Fetch 100 URLs from different domains
   - Measure: Requests/second, total time
   - Libraries: `requests`, `aiohttp`

2. **Database Queries**
   - Execute 50 SELECT queries on SQLite/PostgreSQL
   - Measure: Queries/second, average latency
   - Libraries: `sqlite3`, `asyncpg`, `psycopg2`

3. **File Operations**
   - Read/write 100 files (1MB each)
   - Measure: MB/second, total time
   - Libraries: `open()`, `aiofiles`

4. **API Aggregation**
   - Call 10 different REST APIs and combine results
   - Measure: Total latency, success rate
   - Libraries: `requests`, `aiohttp`

5. **Network Sockets**
   - Open 1000 TCP connections and send data
   - Measure: Connections/second, throughput
   - Libraries: `socket`, `asyncio.open_connection()`

### CPU-Bound Tasks (Good for Multiprocessing)

6. **Prime Number Generation**
   - Find all primes up to 1,000,000
   - Measure: Primes/second, CPU utilization
   - Libraries: Pure Python, `numba`

7. **Image Processing**
   - Resize/filter 100 images (1920x1080)
   - Measure: Images/second, memory usage
   - Libraries: `PIL`, `opencv-python`

8. **Cryptographic Hashing**
   - Hash 1000 strings with SHA-256/bcrypt
   - Measure: Hashes/second, CPU time
   - Libraries: `hashlib`, `bcrypt`

9. **Data Processing**
   - Sort/filter/aggregate 10 million rows
   - Measure: Rows/second, memory efficiency
   - Libraries: `pandas`, `numpy`

10. **Mathematical Computation**
    - Calculate Fibonacci(35) for 100 iterations
    - Measure: Iterations/second, CPU utilization
    - Libraries: Pure Python, `numpy`

### Mixed Workload Tasks

11. **Web Scraping**
    - Fetch 100 pages + parse HTML + extract data
    - Measure: Pages/second, accuracy
    - Libraries: `requests`, `beautifulsoup4`, `aiohttp`

12. **ETL Pipeline**
    - Extract from API → Transform data → Load to DB
    - Measure: Records/second, end-to-end latency
    - Libraries: `requests`, `pandas`, `sqlalchemy`

13. **Video Processing**
    - Download video → Extract frames → Apply filter
    - Measure: Frames/second, total time
    - Libraries: `requests`, `opencv-python`, `ffmpeg`

14. **Log Analysis**
    - Read 1GB log file → Parse → Aggregate → Write results
    - Measure: MB/second, memory usage
    - Libraries: `open()`, `re`, `collections`

15. **Machine Learning Inference**
    - Load model → Process 1000 samples → Return predictions
    - Measure: Predictions/second, latency
    - Libraries: `scikit-learn`, `tensorflow`, `torch`

---

## Quick Decision Tree

```
Is your task CPU-bound?
├─ YES → Use Multiprocessing
│   └─ Tasks are small/frequent? → Consider batching
│
└─ NO (I/O-bound) → Continue...
    │
    ├─ Need very high concurrency (1000+)?
    │   └─ YES → Use Asyncio
    │       └─ Async libraries available? → YES → Asyncio
    │                                    └─ NO → ThreadPoolExecutor + executor
    │
    ├─ Need simple implementation?
    │   └─ YES → Use ThreadPoolExecutor
    │
    └─ Need custom worker behavior?
        └─ YES → Use Manual Threading
        └─ NO → Use ThreadPoolExecutor
```

---

## Implementation Files

- **ThreadPoolExecutor**: `concurrent_script/threadpool_executor.py`
- **Asyncio**: `asyncio_script/asyncio_executor.py`
- **Multiprocessing**: `multiprocessing_script/multiprocessing_executor.py`
- **Manual Threading**: `threading_script/threading_executor.py`

Each includes a test file demonstrating SQLite query parallelization.

---

## Common Pitfalls

### ThreadPoolExecutor
- Don't use for CPU-bound tasks (GIL limits performance)
- Avoid creating too many threads (memory overhead)
- Remember to handle exceptions in futures

### Asyncio
- Can't mix sync and async code easily
- Must use async libraries throughout
- Blocking calls will freeze the entire event loop
- Debugging can be more complex

### Multiprocessing
- High startup cost (process creation ~100ms)
- Data must be picklable for IPC
- Shared state requires special handling (Manager, Queue)
- More memory usage (separate Python interpreter per process)

### Manual Threading
- Race conditions with shared state
- Potential deadlocks with multiple locks
- Queue must be properly drained
- Need explicit thread lifecycle management

---

## Best Practices

1. **Profile first**: Identify bottlenecks before optimizing
2. **Start simple**: Use ThreadPoolExecutor unless you have specific needs
3. **Match the tool**: CPU-bound → multiprocessing, I/O-bound → threads/asyncio
4. **Limit workers**: More workers ≠ better performance (diminishing returns)
5. **Handle errors**: Always implement timeout and exception handling
6. **Test thoroughly**: Concurrency bugs are hard to reproduce
7. **Use logging**: Track what's happening across workers (like loguru!)
8. **Benchmark**: Measure your specific use case, don't rely on theory alone

---

## Resources

- Python `concurrent.futures` documentation
- Python `asyncio` documentation
- Python `multiprocessing` documentation
- Python `threading` documentation
- "High Performance Python" by Micha Gorelick
- "Python Concurrency with asyncio" by Matthew Fowler

---

*Generated: February 28, 2026*
