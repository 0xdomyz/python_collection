# %% [markdown]
# # Teradata SQLAlchemy Connection Pool Demo
#
# This script demonstrates how SQLAlchemy engine pools work with Teradata, including:
# - What a connection pool is
# - How to configure a pooled engine
# - How pooled connections are reused while running queries

# %% [markdown]
# ## 1. What is a connection pool?
#
# A **connection pool** is a cache of open database connections managed by SQLAlchemy's `Engine`.
#
# Instead of opening a brand-new network connection for every query:
# - SQLAlchemy checks out an existing connection from the pool
# - Runs the query
# - Returns the connection back to the pool for reuse
#
# **Why it matters:**
# - Lower latency (reusing open connections)
# - Better throughput (fewer expensive connect/disconnect cycles)
# - Controlled concurrency (limit number of active DB connections)

# %% [markdown]
# ## 2. Set Up Environment Variables
#
# Required environment variables:
# - `TERADATA_HOST`
# - `TERADATA_USER`
# - `TERADATA_PASSWORD`
# - `TERADATA_DATABASE` (optional, defaults to `DBC`)

# %%
import os
import time
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

teradata_host = os.getenv("TERADATA_HOST")
teradata_user = os.getenv("TERADATA_USER")
teradata_password = os.getenv("TERADATA_PASSWORD")
teradata_database = os.getenv("TERADATA_DATABASE", "DBC")

print("Environment Variables Status:")
print(f"  Host configured: {bool(teradata_host)}")
print(f"  User configured: {bool(teradata_user)}")
print(f"  Password configured: {bool(teradata_password)}")
print(f"  Database: {teradata_database}")

if not all([teradata_host, teradata_user, teradata_password]):
    print("\n⚠️  WARNING: Not all required environment variables are set!")
    print("Please set: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD")

# %% [markdown]
# ## 3. Create a Pooled SQLAlchemy Engine
#
# Pool parameters used here:
# - `pool_size=5`: keep up to 5 persistent connections
# - `max_overflow=2`: allow up to 2 temporary extra connections during spikes
# - `pool_timeout=30`: wait up to 30s when pool is exhausted
# - `pool_pre_ping=True`: verify connections are alive before use
# - `pool_recycle=1800`: recycle connections older than 30 minutes

# %%
connection_string = f"teradatasql://{teradata_user}:{teradata_password}@{teradata_host}/{teradata_database}"

try:
    engine = create_engine(
        connection_string,
        echo=False,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=1800,
    )

    with engine.connect() as connection:
        current_db = connection.execute(text("SELECT database")).scalar()

    print("✓ Pooled SQLAlchemy engine created successfully")
    print(f"✓ Connected to database: {current_db}")
    print(f"✓ Pool implementation: {type(engine.pool).__name__}")
except Exception as e:
    print(f"✗ Engine creation failed: {type(e).__name__}: {str(e)}")
    engine = None


# %%
def pool_stat_value(name: str, default: str = "n/a"):
    if engine is None:
        return default

    value = getattr(engine.pool, name, None)
    if value is None:
        return default
    if callable(value):
        try:
            return value()
        except TypeError:
            return value
    return value


def execute_query(query: str, params: Optional[dict] = None) -> Optional[pd.DataFrame]:
    if engine is None:
        print("Error: No active pooled engine")
        return None

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            rows = result.fetchall()
            columns = result.keys()
            return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        print(f"Query failed: {type(e).__name__}: {str(e)}")
        return None


# %% [markdown]
# ## 4. Run Queries Through the Pool
#
# Each query checks out a connection from the pool and returns it afterwards.

# %%
print("=" * 60)
print("Example 1: Single Query via Pool")
print("=" * 60)

query1 = """
SELECT TOP 10
    TableName,
    TableKind,
    CreateTimeStamp
FROM DBC.TablesV
WHERE DataBaseName = :db_name
ORDER BY TableName
"""

result_df = execute_query(query1, {"db_name": "DBC"})
if result_df is not None:
    print(f"Rows returned: {len(result_df)}")
    print(result_df)

print("\nPool Stats:")
print(f"  Pool size: {pool_stat_value('size')}")
print(f"  Checked-in: {pool_stat_value('checkedin')}")
print(f"  Checked-out: {pool_stat_value('checkedout')}")

# %%
print("\n" + "=" * 60)
print("Example 2: Repeated Queries (Connection Reuse)")
print("=" * 60)

query2 = """
SELECT COUNT(*) AS TableCount
FROM DBC.TablesV
WHERE DataBaseName = :db_name
"""

for i in range(1, 6):
    start = time.perf_counter()
    df = execute_query(query2, {"db_name": "DBC"})
    elapsed_ms = (time.perf_counter() - start) * 1000

    if df is not None and not df.empty:
        print(
            f"Run {i}: table count = {int(df.iloc[0]['TableCount'])}, elapsed = {elapsed_ms:.2f} ms"
        )
    else:
        print(f"Run {i}: query failed")

print("\nPool Stats After Reuse Loop:")
print(f"  Pool size: {pool_stat_value('size')}")
print(f"  Checked-in: {pool_stat_value('checkedin')}")
print(f"  Checked-out: {pool_stat_value('checkedout')}")

# %%
print("\n" + "=" * 60)
print("Example 3: Multiple Concurrent Checkouts (Sequential Demo)")
print("=" * 60)

if engine is not None:
    connections = []
    try:
        for idx in range(3):
            conn = engine.connect()
            connections.append(conn)
            session_id = conn.execute(text("SELECT SESSION")).scalar()
            print(f"Checked out connection {idx + 1}, session: {session_id}")

        print("\nPool Stats While Connections Are Checked Out:")
        print(f"  Checked-in: {pool_stat_value('checkedin')}")
        print(f"  Checked-out: {pool_stat_value('checkedout')}")
    except Exception as e:
        print(f"Checkout demo failed: {type(e).__name__}: {str(e)}")
    finally:
        for conn in connections:
            conn.close()

print("\nPool Stats After Returning Connections:")
print(f"  Checked-in: {pool_stat_value('checkedin')}")
print(f"  Checked-out: {pool_stat_value('checkedout')}")

# %% [markdown]
# ## 5. Connection Pool Best Practices
#
# - Keep queries short to release pooled connections quickly
# - Always use `with engine.connect()` or close connections explicitly
# - Use `pool_pre_ping=True` for long-running apps
# - Tune `pool_size` / `max_overflow` based on app concurrency and DB limits
# - Dispose the engine on shutdown

# %% [markdown]
# ## 6. Cleanup

# %%
if engine is not None:
    engine.dispose()
    print("✓ All pooled connections closed (engine disposed)")

# %%
