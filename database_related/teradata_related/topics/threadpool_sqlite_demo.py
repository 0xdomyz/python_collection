# %% [markdown]
# # ThreadPoolExecutor for Concurrent Database Queries
#
# This demo shows how to use `ThreadPoolExecutor` to run multiple SQLite queries concurrently.
# We'll compare sequential vs concurrent execution to demonstrate performance gains.

# %% [markdown]
# ## Setup: Create Sample Database

# %%
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Create sample database with test data
conn = sqlite3.connect("demo.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        city TEXT
    )
"""
)

# Insert sample data
data = [(i, f"User{i}", 20 + (i % 50), f"City{i % 10}") for i in range(1, 10001)]
cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data)
conn.commit()
conn.close()

print("✓ Database created with 10,000 users")

# %% [markdown]
# ## Sequential Execution (Baseline)


# %%
def run_query(query_id):
    """Execute a single query and simulate some processing"""
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    # Different queries for variety
    cursor.execute(f'SELECT * FROM users WHERE city = "City{query_id % 10}" LIMIT 100')
    results = cursor.fetchall()

    time.sleep(0.1)  # Simulate processing time
    conn.close()

    return query_id, len(results)


# Sequential execution
start = time.time()
results = []
for i in range(20):
    results.append(run_query(i))
sequential_time = time.time() - start

print(f"Sequential: {sequential_time:.2f}s for 20 queries")
print(f"Results sample: {results[:3]}")

# %% [markdown]
# ## Concurrent Execution with ThreadPoolExecutor
#
# Key benefits:
# - **I/O-bound tasks**: Perfect for database queries (waiting for disk/network)
# - **Easy syntax**: Context manager handles thread lifecycle
# - **Configurable workers**: Adjust thread count based on workload

# %%
# Concurrent execution
start = time.time()
results = []

with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit all tasks
    futures = {executor.submit(run_query, i): i for i in range(20)}

    # Collect results as they complete
    for future in as_completed(futures):
        results.append(future.result())

concurrent_time = time.time() - start

print(f"Concurrent: {concurrent_time:.2f}s for 20 queries")
print(f"Results sample: {results[:3]}")
print(f"\n⚡ Speedup: {sequential_time / concurrent_time:.2f}x faster")

# %% [markdown]
# ## Key Patterns

# %% [markdown]
# ### Pattern 1: map() for Simple Tasks
# Use when you don't need to track which task is which

# %%
with ThreadPoolExecutor(max_workers=4) as executor:
    query_ids = range(10)
    results = list(executor.map(lambda q: run_query(q), query_ids))

print(f"Map pattern: {len(results)} queries completed")

# %% [markdown]
# ### Pattern 2: as_completed() for Progress Tracking
# Use when you want results as soon as each task finishes

# %%
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_query, i) for i in range(10)]

    for i, future in enumerate(as_completed(futures), 1):
        query_id, count = future.result()
        print(f"[{i}/10] Query {query_id} returned {count} rows")

# %% [markdown]
# ## Best Practices
#
# 1. **Thread Count**: Start with `max_workers = 4-8` for I/O tasks
# 2. **Connection Management**: Each thread should have its own DB connection
# 3. **Error Handling**: Wrap work in try/except to avoid silent failures
# 4. **CPU vs I/O**: Use `ThreadPoolExecutor` for I/O, `ProcessPoolExecutor` for CPU-heavy tasks

# %% [markdown]
# ## Cleanup

# %%
import os

if os.path.exists("demo.db"):
    os.remove("demo.db")
    print("✓ Demo database cleaned up")
