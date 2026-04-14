# %% [markdown]
# # Server-Side GroupBy from Scratch (No Runner)
#
# Direct implementation of server-side query execution:
# - Create driver + output tables
# - Load queries
# - Execute and fetch results
# - Real Teradata access, debug-friendly

# %%
import os
import sys
import time
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

sys.path.insert(0, str(Path.cwd()))

Host = os.getenv("TERADATA_HOST")
User = os.getenv("TERADATA_USER")
Pwd = os.getenv("TERADATA_PASSWORD")
DB = os.getenv("TERADATA_DATABASE", "DBC")

if not all([Host, User, Pwd]):
    raise RuntimeError("Missing TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD")

engine = create_engine(
    f"teradatasql://{User}:{Pwd}@{Host}/{DB}",
    poolclass=QueuePool,
    pool_size=4,
    max_overflow=2,
    pool_pre_ping=True,
)

print(f"Connected: {Host}, {User}, {DB}")

# %%
# Drop old tables if they exist (for clean reruns)
with engine.begin() as conn:
    try:
        conn.execute(text("DROP TABLE agg_jobs"))
        print("Dropped agg_jobs")
    except:
        pass

    try:
        conn.execute(text("DROP TABLE agg_out"))
        print("Dropped agg_out")
    except:
        pass

# Create driver table (holds the queries to execute)
with engine.begin() as conn:
    conn.execute(
        text(
            """
        CREATE TABLE agg_jobs (
            job_id INTEGER,
            sql_text VARCHAR(4000)
        )
    """
        )
    )
    print("Created agg_jobs")

# Create structured results table with dimension columns
with engine.begin() as conn:
    conn.execute(
        text(
            """
        CREATE TABLE agg_out (
            job_id INTEGER,
            query_type VARCHAR(100),
            table_kind VARCHAR(100),
            table_name VARCHAR(256),
            record_count BIGINT,
            distinct_table_count BIGINT,
            result_timestamp TIMESTAMP,
            sequence_num INTEGER,
            status VARCHAR(50),
            notes VARCHAR(500)
        )
    """
        )
    )
    print("Created agg_out")

# %%
# Create subset table (materialized filter of base table)
db_name = DB.replace("'", "''")

with engine.begin() as conn:
    conn.execute(
        text(
            f"""
        CREATE VOLATILE TABLE vt_subset_work AS (
            SELECT * FROM DBC.TablesV
            WHERE DataBaseName = '{db_name}'
        ) WITH DATA
        PRIMARY INDEX (1)
        ON COMMIT PRESERVE ROWS
    """
        )
    )
    print(f"Created vt_subset_work from DBC.TablesV")

# Define 5 queries targeting the subset - each is a complete INSERT...SELECT statement
queries = [
    """
    INSERT INTO agg_out (job_id, query_type, table_kind, record_count, result_timestamp, sequence_num, status)
    SELECT 1, 'TableKind Distribution', TableKind, COUNT(*), CURRENT_TIMESTAMP, ROW_NUMBER() OVER (ORDER BY TableKind), 'completed'
    FROM vt_subset_work 
    GROUP BY TableKind
    """,
    """
    INSERT INTO agg_out (job_id, query_type, distinct_table_count, result_timestamp, status)
    SELECT 2, 'Unique Table Count', COUNT(DISTINCT TableName), CURRENT_TIMESTAMP, 'completed'
    FROM vt_subset_work
    """,
    """
    INSERT INTO agg_out (job_id, query_type, record_count, result_timestamp, status)
    SELECT 3, 'Total Row Count', COUNT(*), CURRENT_TIMESTAMP, 'completed'
    FROM vt_subset_work
    """,
    """
    INSERT INTO agg_out (job_id, query_type, table_kind, distinct_table_count, result_timestamp, sequence_num, status)
    SELECT 4, 'Distinct Count by TableKind', TableKind, COUNT(DISTINCT TableName), CURRENT_TIMESTAMP, ROW_NUMBER() OVER (ORDER BY TableKind), 'completed'
    FROM vt_subset_work 
    GROUP BY TableKind
    """,
    """
    INSERT INTO agg_out (job_id, query_type, table_name, table_kind, result_timestamp, sequence_num, status)
    SELECT 5, 'Top Tables', TableName, TableKind, CURRENT_TIMESTAMP, ROW_NUMBER() OVER (ORDER BY TableName), 'completed'
    FROM vt_subset_work 
    ORDER BY TableName 
    QUALIFY ROW_NUMBER() OVER (ORDER BY TableName) <= 5
    """,
]

# Load queries into driver table
with engine.begin() as conn:
    for job_id, sql in enumerate(queries, start=1):
        conn.execute(
            text("INSERT INTO agg_jobs (job_id, sql_text) VALUES (:id, :sql)"),
            {"id": job_id, "sql": sql},
        )
    print(f"Loaded {len(queries)} queries into agg_jobs")

# %%
# Create stored procedure to execute all queries server-side
print("Creating stored procedure for server-side execution...")
with engine.begin() as conn:
    try:
        conn.execute(text("DROP PROCEDURE run_agg_dynamic_sql"))
    except:
        pass

    proc_sql = """
    REPLACE PROCEDURE run_agg_dynamic_sql()
    BEGIN
        DECLARE stmt VARCHAR(32000);
        FOR cur AS c1 CURSOR FOR
            SELECT sql_text FROM agg_jobs ORDER BY job_id
        DO
            SET stmt = cur.sql_text;
            CALL DBC.SysExecSQL(:stmt);
        END FOR;
    END;
    """
    conn.execute(text(proc_sql))
    print("Stored procedure created successfully")

# %%
# Execute all queries server-side via stored procedure
print("Calling stored procedure to execute queries server-side...")
with engine.begin() as conn:
    conn.execute(text("CALL run_agg_dynamic_sql()"))

print("Execution complete")

# %%
# Fetch and display results
result_df = pd.read_sql(
    text("SELECT * FROM agg_out ORDER BY job_id, sequence_num"), engine
)
print(f"Result shape: {result_df.shape}")
print("\nAll results:")
print(result_df.to_string(index=False))

print("\n" + "=" * 100)
print("Results Summary by Query:")
print("=" * 100)
for job_id in sorted(result_df["job_id"].unique()):
    subset = result_df[result_df["job_id"] == job_id]
    query_type = subset["query_type"].iloc[0]
    print(f"\nJob {job_id}: {query_type} ({len(subset)} rows)")

    # Show non-null dimension and metric columns
    cols_to_show = [
        "table_kind",
        "table_name",
        "record_count",
        "distinct_table_count",
        "notes",
    ]
    subset_display = subset[
        [col for col in cols_to_show if col in subset.columns]
    ].dropna(axis=1, how="all")
    print(subset_display.to_string(index=False))
