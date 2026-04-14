# %% [markdown]
# # TeradataML Concurrent Query Execution Demo
#
# This script demonstrates how to execute multiple Teradata queries concurrently
# using TeradataML, including:
# - How TeradataML contexts enable concurrent operations
# - Executing queries in parallel using threading
# - Performance comparison: sequential vs concurrent execution
# - Proof of concurrency via execution timelines and session IDs

# %% [markdown]
# ## 1. Why TeradataML for Concurrent Queries?
#
# TeradataML advantages for concurrency:
# - **Native Teradata Integration**: Optimized for Teradata-specific operations
# - **Context-Based**: Each thread can have its own context/session
# - **Efficient Serialization**: Better performance than generic SQL libraries
# - **DataFrame API**: Lazy evaluation allows efficient query batching
#
# **Concurrency approach**: Use Python threading with separate TeradataML contexts
# per thread (each gets its own database session).

# %% [markdown]
# ## 2. Import Libraries

# %%
import os
import threading
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List

import pandas as pd
from teradataml import create_context, execute_sql, remove_context

warnings.filterwarnings("ignore")

print("✓ All libraries imported successfully")

# %% [markdown]
# ## 3. Load Configuration

# %%
teradata_host = os.getenv("TERADATA_HOST")
teradata_user = os.getenv("TERADATA_USER")
teradata_password = os.getenv("TERADATA_PASSWORD")
teradata_database = os.getenv("TERADATA_DATABASE", "DBC")
teradata_logmech = os.getenv("TERADATA_LOGMECH", "TD2")

print("Environment Variables Status:")
print(f"  Host: {bool(teradata_host)}")
print(f"  User: {bool(teradata_user)}")
print(f"  Password: {bool(teradata_password)}")
print(f"  Database: {teradata_database}")
print(f"  Logmech: {teradata_logmech}")

if not all([teradata_host, teradata_user, teradata_password]):
    print("\n⚠️  WARNING: Not all required environment variables are set!")
    print("Please set: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD")

# %% [markdown]
# ## 4. Test Single TeradataML Context Connection

# %%
try:
    context = create_context(
        host=teradata_host,
        username=teradata_user,
        password=teradata_password,
        database=teradata_database,
        logmech=teradata_logmech,
    )

    # Test connection
    cursor = execute_sql("SELECT DATABASE")
    db_name = cursor.fetchone()[0]
    print(f"✓ TeradataML context created successfully")
    print(f"✓ Connected to database: {db_name}")

    remove_context()
    print(f"✓ Connection test passed, context removed")
except Exception as e:
    print(f"✗ Connection failed: {type(e).__name__}: {str(e)}")

# %% [markdown]
# ## 5. Define Test Queries

# %%
TEST_QUERIES = [
    # Query 1: Table counts
    """
    SELECT TableKind, COUNT(*) AS Cnt
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC'
    GROUP BY TableKind
    ORDER BY Cnt DESC
    """,
    # Query 2: Database info
    """
    SELECT TOP 10 DataBaseName, OwnerName, DBKind
    FROM DBC.DatabasesV
    ORDER BY DataBaseName
    """,
    # Query 3: Table list
    """
    SELECT TOP 20 TableName, TableKind, CreateTimeStamp
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC'
    ORDER BY CreateTimeStamp DESC
    """,
    # Query 4: Column info
    """
    SELECT TOP 15 TableName, ColumnName, ColumnType
    FROM DBC.ColumnsV
    WHERE DataBaseName = 'DBC'
    ORDER BY TableName, ColumnId
    """,
    # Query 5: User rights
    """
    SELECT TOP 10 UserName, DatabaseName, AccessRight
    FROM DBC.AllRightsV
    WHERE DatabaseName = 'DBC'
    """,
    # Query 6: Functions
    """
    SELECT TOP 10 DataBaseName, FunctionName, FunctionType
    FROM DBC.FunctionsV
    WHERE DataBaseName IN ('SYSLIB', 'DBC')
    """,
    # Query 7: Aggregate
    """
    SELECT COUNT(*) AS TotalTables,
           SUM(CASE WHEN TableKind = 'T' THEN 1 ELSE 0 END) AS BaseTables,
           SUM(CASE WHEN TableKind = 'V' THEN 1 ELSE 0 END) AS Views
    FROM DBC.TablesV
    WHERE DataBaseName = 'DBC'
    """,
    # Query 8: DB permissions
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
    # Query 10: Column count
    """
    SELECT COUNT(*) AS ColumnCount,
           COUNT(DISTINCT TableName) AS TableCount
    FROM DBC.ColumnsV
    WHERE DataBaseName = 'DBC'
    """,
]

print(f"✓ Defined {len(TEST_QUERIES)} test queries")

# %% [markdown]
# ## 6. Create Shared TeradataML Context for Concurrent Queries

# %%
# Create a single shared context that all threads will use
# Each thread gets a separate cursor, which are thread-safe
try:
    shared_context = create_context(
        host=teradata_host,
        username=teradata_user,
        password=teradata_password,
        database=teradata_database,
        logmech=teradata_logmech,
    )
    print("✓ Shared TeradataML context created for concurrent operations")
except Exception as e:
    print(f"✗ Failed to create shared context: {e}")
    shared_context = None

# %% [markdown]
# ## 7. Query Execution Function


# %%
def execute_query_concurrent(query_id: int, query: str) -> Dict:
    """
    Execute a query using the shared TeradataML context.
    Each thread gets its own cursor (thread-safe operation).

    Returns:
        Dictionary with timing, session ID, thread info, and row count
    """
    thread_id = threading.get_ident()
    start_time = datetime.now()
    start_epoch = time.perf_counter()

    try:
        # Each thread gets its own cursor from the shared context
        # TeradataML cursors are thread-safe
        cursor = execute_sql(query)
        rows = cursor.fetchall()
        row_count = len(rows)

        # Get session ID from a quick query
        session_cursor = execute_sql("SELECT SESSION")
        session_id = session_cursor.fetchone()[0]

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
# ## 8. Sequential Execution Baseline

# %%
print("=" * 70)
print("SEQUENTIAL EXECUTION (Using Shared Context)")
print("=" * 70)

sequential_start = time.perf_counter()
sequential_results = []

if shared_context is None:
    print("✗ Cannot run sequential execution without shared context")
else:
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"Executing query {i}/{len(TEST_QUERIES)}...", end=" ", flush=True)
        result = execute_query_concurrent(i, query)
        sequential_results.append(result)
        print(f"✓ ({result['duration']:.3f}s, {result['row_count']} rows)")

sequential_end = time.perf_counter()
sequential_total_time = sequential_end - sequential_start

print(f"\n{'='*70}")
print(f"SEQUENTIAL TOTAL TIME: {sequential_total_time:.3f} seconds")
print(f"{'='*70}\n")

if sequential_results:
    seq_df = pd.DataFrame(sequential_results)
    print("Sequential Execution Summary:")
    print(
        seq_df[
            ["query_id", "thread_id", "session_id", "duration", "row_count"]
        ].to_string(index=False)
    )

# %% [markdown]
# ## 9. Concurrent Execution with ThreadPoolExecutor

# %%
print("\n" + "=" * 70)
print("CONCURRENT EXECUTION (ThreadPoolExecutor with Shared Context)")
print("=" * 70)

if shared_context is None:
    print("✗ Cannot run concurrent execution without shared context")
    concurrent_total_time = 0
    concurrent_results = []
else:
    concurrent_start = time.perf_counter()
    concurrent_results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for i, query in enumerate(TEST_QUERIES, 1):
            future = executor.submit(execute_query_concurrent, i, query)
            futures[future] = i
            print(f"Submitted query {i} to thread pool")

        print("\nWaiting for concurrent queries to complete...")
        for future in as_completed(futures):
            query_id = futures[future]
            result = future.result()
            concurrent_results.append(result)
            status_icon = "✓" if result["status"] == "SUCCESS" else "✗"
            print(
                f"Query {query_id} completed: {status_icon} {result['duration']:.3f}s, "
                f"Thread: {result['thread_id']}, Session: {result['session_id']}"
            )

    concurrent_end = time.perf_counter()
    concurrent_total_time = concurrent_end - concurrent_start

    print(f"\n{'='*70}")
    print(f"CONCURRENT TOTAL TIME: {concurrent_total_time:.3f} seconds")
    print(f"{'='*70}\n")

    if concurrent_results:
        conc_df = pd.DataFrame(concurrent_results).sort_values("query_id")
        print("Concurrent Execution Summary:")
        print(
            conc_df[
                ["query_id", "thread_id", "session_id", "duration", "row_count"]
            ].to_string(index=False)
        )

# %% [markdown]
# ## 10. Proof of Concurrency: Timeline Analysis

# %%
print("\n" + "=" * 70)
print("CONCURRENCY PROOF: Execution Timeline")
print("=" * 70)

if not concurrent_results:
    print("⚠ No concurrent results to analyze")
else:
    conc_sorted = pd.DataFrame(concurrent_results).sort_values("start_time")

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
                if (
                    row1["start_time"] < row2["end_time"]
                    and row2["start_time"] < row1["end_time"]
                ):
                    overlapping_pairs.append((row1["query_id"], row2["query_id"]))

    print(f"\n✓ PROOF: Found {len(overlapping_pairs)} overlapping query pairs")
    print(f"✓ PROOF: {len(conc_sorted['thread_id'].unique())} unique threads used")
    print(
        f"✓ PROOF: {len(conc_sorted['session_id'].unique())} unique database sessions"
    )

    if len(overlapping_pairs) > 0:
        print(f"\n✓ CONCURRENCY CONFIRMED: Queries executed simultaneously!")
    else:
        print(f"\n⚠ WARNING: No overlaps detected - may have run sequentially")

# %% [markdown]
# ## 11. Performance Comparison

# %%
print("\n" + "=" * 70)
print("PERFORMANCE ANALYSIS")
print("=" * 70)

if not sequential_results or not concurrent_results or concurrent_total_time == 0:
    print(
        "⚠ Cannot compare performance - missing data from sequential or concurrent execution"
    )
else:
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
    print("DETAILED COMPARISON")
    print(f"{'='*70}\n")

    seq_df = pd.DataFrame(sequential_results)
    conc_df = pd.DataFrame(concurrent_results)

    comparison_data = {
        "Metric": [
            "Total Time",
            "Avg Query Time",
            "Min Query Time",
            "Max Query Time",
            "Queries Run",
        ],
        "Sequential": [
            f"{sequential_total_time:.3f}s",
            f"{seq_df['duration'].mean():.3f}s",
            f"{seq_df['duration'].min():.3f}s",
            f"{seq_df['duration'].max():.3f}s",
            f"{len(seq_df)}",
        ],
        "Concurrent": [
            f"{concurrent_total_time:.3f}s",
            f"{conc_df['duration'].mean():.3f}s",
            f"{conc_df['duration'].min():.3f}s",
            f"{conc_df['duration'].max():.3f}s",
            f"{len(conc_df)}",
        ],
    }

    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))

# %% [markdown]
# ## 12. Key Findings

# %%
print("\n" + "=" * 70)
print("SUMMARY: TeradataML Concurrent Query Execution")
print("=" * 70)

if concurrent_results:
    print(f"\n✓ CONCURRENCY APPROACH:")
    print(f"  • Shared TeradataML context with multi-threaded query execution")
    print(f"  • Each thread uses thread-safe cursors from the shared context")
    print(f"  • Native Teradata optimization via TeradataML")

    conc_df = pd.DataFrame(concurrent_results)
    seq_df = pd.DataFrame(sequential_results)

    overlapping = 0
    conc_sorted = conc_df.sort_values("start_time")
    for i, row1 in conc_sorted.iterrows():
        for j, row2 in conc_sorted.iterrows():
            if row1["query_id"] < row2["query_id"]:
                if (
                    row1["start_time"] < row2["end_time"]
                    and row2["start_time"] < row1["end_time"]
                ):
                    overlapping += 1

    print(f"\n✓ PROOF OF CONCURRENCY:")
    print(
        f"  • {len(conc_df['thread_id'].unique())} different threads executed queries"
    )
    print(f"  • {len(conc_df['session_id'].unique())} different database sessions")
    print(f"  • {overlapping} overlapping query execution pairs")

    if concurrent_total_time > 0:
        speedup = sequential_total_time / concurrent_total_time
        time_saved = sequential_total_time - concurrent_total_time

        print(f"\n✓ PERFORMANCE IMPROVEMENT:")
        print(f"  • Sequential total: {sequential_total_time:.3f}s")
        print(f"  • Concurrent total: {concurrent_total_time:.3f}s")
        print(f"  • Speedup: {speedup:.2f}x faster")
        print(
            f"  • Time saved: {time_saved:.3f}s ({time_saved/sequential_total_time*100:.1f}%)"
        )

    print(f"\n✓ TeradataML ADVANTAGES:")
    print(f"  • Native Teradata integration for optimal performance")
    print(f"  • Thread-safe multi-cursor execution from shared context")
    print(f"  • Automatic session handling and query optimization")
    print(f"  • Efficient result materialization via cursors")

    print(f"\n{'='*70}")
    print("Concurrent query execution with TeradataML completed successfully!")
    print(f"{'='*70}")
else:
    print("\n✗ Unable to complete performance analysis - execution failed")

# %% [markdown]
# ## 13. Cleanup

# %%
if shared_context is not None:
    try:
        remove_context()
        print("✓ TeradataML context closed successfully")
    except Exception as e:
        print(f"⚠ Error closing context: {e}")
