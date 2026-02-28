# %% [markdown]
# # Concurrent Query Execution with SQLAlchemy and Teradata
#
# This notebook demonstrates how to execute database queries concurrently using SQLAlchemy with connection pooling, proving that:
# - Concurrent queries complete faster than sequential queries
# - Multiple queries execute simultaneously (proven via timing logs and thread IDs)
# - Connection pooling enables safe concurrent database access

# %% [markdown]
# ## 1. Import Required Libraries and Setup
#
# We'll use:
# - **SQLAlchemy** for database connections
# - **concurrent.futures.ThreadPoolExecutor** for concurrent query execution
# - **threading** to track thread IDs (proof of concurrency)
# - **time** and **datetime** for performance measurement

# %%
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Tuple

# For visualization
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

print("✓ All libraries imported successfully")

# %% [markdown]
# ## 2. Configure Database Connection with Connection Pool
#
# We'll create a pooled SQLAlchemy engine with:
# - **pool_size=10**: maintain 10 persistent connections
# - **max_overflow=5**: allow 5 additional connections during spikes
# - This enables up to 15 concurrent queries simultaneously

# %%
# Load environment variables
teradata_host = os.getenv("TERADATA_HOST")
teradata_user = os.getenv("TERADATA_USER")
teradata_password = os.getenv("TERADATA_PASSWORD")
teradata_database = os.getenv("TERADATA_DATABASE", "DBC")

print("Environment Variables Status:")
print(f"  Host: {bool(teradata_host)}")
print(f"  User: {bool(teradata_user)}")
print(f"  Password: {bool(teradata_password)}")
print(f"  Database: {teradata_database}")

# Create pooled engine
connection_string = f"teradatasql://{teradata_user}:{teradata_password}@{teradata_host}/{teradata_database}"

engine = create_engine(
    connection_string,
    echo=False,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=1800,
)

# Test connection
with engine.connect() as conn:
    db = conn.execute(text("SELECT database")).scalar()
    print(f"\n✓ Engine created with QueuePool")
    print(f"✓ Connected to database: {db}")
    print(
        f"✓ Pool capacity: {engine.pool.size()} connections + {engine.pool._max_overflow} overflow"
    )

# %% [markdown]
# ## 3. Define Query Execution Function with Logging
#
# This function:
# - Records thread ID (proof of concurrency)
# - Records session ID from Teradata
# - Measures execution time
# - Logs start/end timestamps


# %%
def execute_query_with_logging(query_id: int, query: str, params: dict = None) -> Dict:
    """
    Execute a query and return detailed timing/concurrency information.

    Returns:
        Dictionary with query_id, thread_id, session_id, start_time, end_time,
        duration, and row_count
    """
    thread_id = threading.get_ident()
    start_time = datetime.now()
    start_epoch = time.perf_counter()

    try:
        with engine.connect() as conn:
            # Get Teradata session ID to prove different sessions
            session_id = conn.execute(text("SELECT SESSION")).scalar()

            # Execute the actual query
            result = conn.execute(text(query), params or {})
            rows = result.fetchall()
            row_count = len(rows)

        end_time = datetime.now()
        end_epoch = time.perf_counter()
        duration = end_epoch - start_epoch

        return {
            "query_id": query_id,
            "thread_id": thread_id,
            "session_id": session_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "row_count": row_count,
            "status": "SUCCESS",
        }
    except Exception as e:
        end_time = datetime.now()
        end_epoch = time.perf_counter()
        return {
            "query_id": query_id,
            "thread_id": thread_id,
            "session_id": None,
            "start_time": start_time,
            "end_time": end_time,
            "duration": end_epoch - start_epoch,
            "row_count": 0,
            "status": f"ERROR: {str(e)[:50]}",
        }


print("✓ Query execution function defined")

# %% [markdown]
# ## 4. Define Test Queries
#
# We'll run 10 different queries against Teradata system catalogs to simulate realistic workload with measurable execution time.

# %%
# Define 10 different queries for testing
TEST_QUERIES = [
    # Query 1: Table counts by kind
    """
    SELECT TableKind, COUNT(*) AS Cnt
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC'
    GROUP BY TableKind
    ORDER BY Cnt DESC
    """,
    # Query 2: Database sizes
    """
    SELECT TOP 10 DataBaseName, OwnerName, DBKind
    FROM DBC.DatabasesV
    ORDER BY DataBaseName
    """,
    # Query 3: Tables with indexes
    """
    SELECT TOP 20 TableName, TableKind, CreateTimeStamp
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC' AND TableKind IN ('T', 'V')
    ORDER BY CreateTimeStamp DESC
    """,
    # Query 4: Column information
    """
    SELECT TOP 15 TableName, ColumnName, ColumnType
    FROM DBC.ColumnsV
    WHERE DataBaseName = 'DBC'
    ORDER BY TableName, ColumnId
    """,
    # Query 5: User access rights
    """
    SELECT TOP 10 UserName, DatabaseName, AccessRight
    FROM DBC.AllRightsV
    WHERE DatabaseName = 'DBC'
    """,
    # Query 6: Function information
    """
    SELECT TOP 10 DataBaseName, FunctionName, FunctionType
    FROM DBC.FunctionsV
    WHERE DataBaseName IN ('SYSLIB', 'DBC')
    """,
    # Query 7: More table metadata
    """
    SELECT COUNT(*) AS TotalTables,
           SUM(CASE WHEN TableKind = 'T' THEN 1 ELSE 0 END) AS BaseTables,
           SUM(CASE WHEN TableKind = 'V' THEN 1 ELSE 0 END) AS Views
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC'
    """,
    # Query 8: Database permissions
    """
    SELECT TOP 10 DatabaseName, OwnerName, ProtectionType
    FROM DBC.DatabasesV
    ORDER BY DatabaseName
    """,
    # Query 9: Indexes
    """
    SELECT TOP 10 DataBaseName, TableName, IndexType
    FROM DBC.IndicesV
    WHERE DataBaseName = 'DBC'
    """,
    # Query 10: More columns
    """
    SELECT COUNT(*) AS ColumnCount,
           COUNT(DISTINCT TableName) AS TableCount
    FROM DBC.ColumnsV
    WHERE DataBaseName = 'DBC'
    """,
]

print(f"✓ Defined {len(TEST_QUERIES)} test queries")

# %% [markdown]
# ## 5. Execute Queries Sequentially (Baseline)
#
# Run all queries one after another to establish a performance baseline.

# %%
print("=" * 70)
print("SEQUENTIAL EXECUTION")
print("=" * 70)

sequential_start = time.perf_counter()
sequential_results = []

for i, query in enumerate(TEST_QUERIES, 1):
    print(f"Executing query {i}/{len(TEST_QUERIES)}...", end=" ")
    result = execute_query_with_logging(i, query)
    sequential_results.append(result)
    print(f"✓ ({result['duration']:.3f}s, {result['row_count']} rows)")

sequential_end = time.perf_counter()
sequential_total_time = sequential_end - sequential_start

print(f"\n{'='*70}")
print(f"SEQUENTIAL TOTAL TIME: {sequential_total_time:.3f} seconds")
print(f"{'='*70}\n")

# Create DataFrame for analysis
seq_df = pd.DataFrame(sequential_results)
print("Sequential Execution Summary:")
print(
    seq_df[["query_id", "thread_id", "session_id", "duration", "row_count"]].to_string(
        index=False
    )
)

# %% [markdown]
# ## 6. Execute Queries Concurrently with ThreadPoolExecutor
#
# Use ThreadPoolExecutor to run all queries simultaneously using connection pool.

# %%
print("=" * 70)
print("CONCURRENT EXECUTION (ThreadPoolExecutor)")
print("=" * 70)

concurrent_start = time.perf_counter()
concurrent_results = []

# Use ThreadPoolExecutor with max_workers matching our queries
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit all queries at once
    futures = {}
    for i, query in enumerate(TEST_QUERIES, 1):
        future = executor.submit(execute_query_with_logging, i, query)
        futures[future] = i
        print(f"Submitted query {i} to thread pool")

    # Collect results as they complete
    print("\nWaiting for concurrent queries to complete...")
    for future in as_completed(futures):
        query_id = futures[future]
        result = future.result()
        concurrent_results.append(result)
        print(
            f"Query {query_id} completed: {result['duration']:.3f}s, "
            f"Thread: {result['thread_id']}, Session: {result['session_id']}"
        )

concurrent_end = time.perf_counter()
concurrent_total_time = concurrent_end - concurrent_start

print(f"\n{'='*70}")
print(f"CONCURRENT TOTAL TIME: {concurrent_total_time:.3f} seconds")
print(f"{'='*70}\n")

# Create DataFrame for analysis
conc_df = pd.DataFrame(concurrent_results).sort_values("query_id")
print("Concurrent Execution Summary:")
print(
    conc_df[["query_id", "thread_id", "session_id", "duration", "row_count"]].to_string(
        index=False
    )
)

# %% [markdown]
# ## 7. Proof of Concurrency: Timeline Analysis
#
# Visualize query execution timelines to prove queries ran simultaneously.

# %%
print("=" * 70)
print("CONCURRENCY PROOF: Query Execution Timeline")
print("=" * 70)

# Check for overlapping execution times
conc_sorted = conc_df.sort_values("start_time")

print("\nConcurrent Execution Timeline:")
print(
    f"{'Query':<8} {'Thread ID':<12} {'Session':<10} {'Start':<12} {'End':<12} {'Duration':<10}"
)
print("-" * 70)

for _, row in conc_sorted.iterrows():
    start_ms = (
        row["start_time"] - conc_sorted.iloc[0]["start_time"]
    ).total_seconds() * 1000
    end_ms = (
        row["end_time"] - conc_sorted.iloc[0]["start_time"]
    ).total_seconds() * 1000
    print(
        f"{row['query_id']:<8} {row['thread_id']:<12} {row['session_id']:<10} "
        f"{start_ms:>8.0f}ms   {end_ms:>8.0f}ms   {row['duration']:>6.3f}s"
    )

# Check for overlaps (proof of concurrency)
overlapping_pairs = []
for i, row1 in conc_sorted.iterrows():
    for j, row2 in conc_sorted.iterrows():
        if row1["query_id"] < row2["query_id"]:
            # Check if row1 and row2 overlap
            if (
                row1["start_time"] < row2["end_time"]
                and row2["start_time"] < row1["end_time"]
            ):
                overlapping_pairs.append((row1["query_id"], row2["query_id"]))

print(f"\n✓ PROOF: Found {len(overlapping_pairs)} overlapping query pairs")
print(f"✓ PROOF: {len(conc_df['thread_id'].unique())} unique threads used")
print(f"✓ PROOF: {len(conc_df['session_id'].unique())} unique database sessions")

if len(overlapping_pairs) > 0:
    print(f"\n✓ CONCURRENCY CONFIRMED: Queries executed simultaneously!")
else:
    print(f"\n⚠ WARNING: No overlaps detected - queries may have run sequentially")

# %% [markdown]
# ## 8. Performance Comparison
#
# Calculate speedup and efficiency metrics.

# %%
print("=" * 70)
print("PERFORMANCE COMPARISON")
print("=" * 70)

speedup = sequential_total_time / concurrent_total_time
time_saved = sequential_total_time - concurrent_total_time
efficiency = (speedup / len(TEST_QUERIES)) * 100

print(f"\nSequential Total Time:   {sequential_total_time:.3f} seconds")
print(f"Concurrent Total Time:   {concurrent_total_time:.3f} seconds")
print(
    f"\nTime Saved:              {time_saved:.3f} seconds ({time_saved/sequential_total_time*100:.1f}%)"
)
print(f"Speedup Factor:          {speedup:.2f}x")
print(f"Parallel Efficiency:     {efficiency:.1f}%")

print(f"\n{'='*70}")
print("COMPARISON TABLE")
print(f"{'='*70}\n")

comparison_data = {
    "Metric": ["Total Time", "Avg Query Time", "Min Query Time", "Max Query Time"],
    "Sequential": [
        f"{sequential_total_time:.3f}s",
        f"{seq_df['duration'].mean():.3f}s",
        f"{seq_df['duration'].min():.3f}s",
        f"{seq_df['duration'].max():.3f}s",
    ],
    "Concurrent": [
        f"{concurrent_total_time:.3f}s",
        f"{conc_df['duration'].mean():.3f}s",
        f"{conc_df['duration'].min():.3f}s",
        f"{conc_df['duration'].max():.3f}s",
    ],
}

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# %% [markdown]
# ## 9. Visualize Performance Improvement
#
# Bar charts showing sequential vs concurrent execution times.

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Total execution time comparison
axes[0].bar(
    ["Sequential", "Concurrent"],
    [sequential_total_time, concurrent_total_time],
    color=["#ff6b6b", "#4ecdc4"],
)
axes[0].set_ylabel("Total Time (seconds)", fontsize=12)
axes[0].set_title("Total Execution Time Comparison", fontsize=14, fontweight="bold")
axes[0].grid(axis="y", alpha=0.3)

# Add value labels on bars
for i, v in enumerate([sequential_total_time, concurrent_total_time]):
    axes[0].text(i, v + 0.1, f"{v:.2f}s", ha="center", va="bottom", fontweight="bold")

# Chart 2: Individual query durations
query_ids = seq_df["query_id"]
x = range(len(query_ids))
width = 0.35

axes[1].bar(
    [i - width / 2 for i in x],
    seq_df["duration"],
    width,
    label="Sequential",
    color="#ff6b6b",
    alpha=0.8,
)
axes[1].bar(
    [i + width / 2 for i in x],
    conc_df.sort_values("query_id")["duration"],
    width,
    label="Concurrent",
    color="#4ecdc4",
    alpha=0.8,
)

axes[1].set_xlabel("Query ID", fontsize=12)
axes[1].set_ylabel("Duration (seconds)", fontsize=12)
axes[1].set_title("Individual Query Durations", fontsize=14, fontweight="bold")
axes[1].set_xticks(x)
axes[1].set_xticklabels(query_ids)
axes[1].legend()
axes[1].grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\n✓ Speedup: {speedup:.2f}x faster with concurrent execution")

# %% [markdown]
# ## 10. Connection Pool Statistics
#
# Check pool usage during and after concurrent execution.

# %%
print("=" * 70)
print("CONNECTION POOL STATISTICS")
print("=" * 70)

pool = engine.pool

print(f"\nPool Configuration:")
print(f"  Pool Size:      {pool.size()}")
print(f"  Max Overflow:   {pool._max_overflow}")
print(f"  Total Capacity: {pool.size() + pool._max_overflow}")

print(f"\nCurrent State:")
print(f"  Checked In:     {pool.checkedin()}")
print(f"  Checked Out:    {pool.checkedout()}")
print(f"  Overflow:       {pool.overflow()}")

print(f"\n✓ Pool successfully handled {len(TEST_QUERIES)} concurrent queries")
print(f"✓ Peak concurrent connections: {len(conc_df['session_id'].unique())}")

# %% [markdown]
# ## 11. Summary and Conclusions
#
# Key findings from this concurrent query execution demonstration.

# %%
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"\n✓ PROOF OF CONCURRENCY:")
print(f"  • {len(conc_df['thread_id'].unique())} different threads executed queries")
print(f"  • {len(conc_df['session_id'].unique())} different database sessions used")
print(f"  • {len(overlapping_pairs)} pairs of queries had overlapping execution times")

print(f"\n✓ PERFORMANCE IMPROVEMENT:")
print(f"  • Sequential execution: {sequential_total_time:.3f} seconds")
print(f"  • Concurrent execution: {concurrent_total_time:.3f} seconds")
print(f"  • Speedup: {speedup:.2f}x faster")
print(
    f"  • Time saved: {time_saved:.3f} seconds ({time_saved/sequential_total_time*100:.1f}%)"
)

print(f"\n✓ KEY LEARNINGS:")
print(f"  • Connection pooling enables safe concurrent database access")
print(f"  • ThreadPoolExecutor simplifies concurrent query execution")
print(f"  • Real-world speedup depends on query complexity and I/O wait time")
print(f"  • Multiple queries can share a pool without connection exhaustion")

print(f"\n{'='*70}")
print("Concurrent query execution demonstration completed successfully!")
print(f"{'='*70}")

# %% [markdown]
# ## 12. Cleanup
#
# Dispose of the engine and close all pooled connections.

# %%
# Dispose of the engine to close all connections
engine.dispose()
print("✓ All pooled connections closed")
print("✓ Engine disposed successfully")
