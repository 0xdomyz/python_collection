"""Categorical variable analysis using DuckDB."""

import duckdb
import pandas as pd


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """Object dtype columns."""
    return df.select_dtypes(include=["object"]).columns.tolist()


def execute_sql_query(df: pd.DataFrame, sql_query: str) -> pd.DataFrame | None:
    """Execute SQL on df using DuckDB, returns None on error."""
    con = duckdb.connect()
    try:
        con.register("df", df)
        return con.execute(sql_query).df()
    except Exception:
        return None
    finally:
        con.close()


def categorical_summary(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """DuckDB group by with value counts and percentages (null-safe)."""
    con = duckdb.connect()
    safe_col = col.replace('"', '""')
    query = f"""
    SELECT
        "{safe_col}" as value,
        COUNT(*) as count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
    FROM df
    GROUP BY "{safe_col}"
    ORDER BY "{safe_col}"
    """
    try:
        con.register("df", df)
        return con.execute(query).df()
    finally:
        con.close()
