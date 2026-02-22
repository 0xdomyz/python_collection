"""Categorical variable analysis utilities using DuckDB."""

import duckdb
import pandas as pd


def get_categorical_columns(df):
    """Get list of categorical (object dtype) columns."""
    return df.select_dtypes(include=["object"]).columns.tolist()


def execute_sql_query(df, sql_query):
    """
    Execute SQL query on DataFrame using DuckDB.

    Args:
        df: DataFrame
        sql_query: SQL query string (use 'df' as table name)

    Returns:
        Result as DataFrame, or None if query fails
    """
    try:
        con = duckdb.connect()
        result = con.execute(sql_query).df()
        con.close()
        return result
    except Exception as e:
        return None  # Error will be handled by caller


def categorical_summary(df, col):
    """
    Get categorical summary with counts and percentages.
    Does not drop NULLs.

    Args:
        df: DataFrame
        col: Column name

    Returns:
        DataFrame with value counts and distribution %
    """
    result = df[col].value_counts(dropna=False).sort_index()
    summary = pd.DataFrame(result)
    summary.columns = ["count"]
    summary["percentage"] = (summary["count"] / summary["count"].sum() * 100).round(2)
    return summary.reset_index()


def generate_sql_template(selected_cols=None):
    """
    Generate SQL template for data subset.

    Args:
        selected_cols: List of columns to include (None = all)

    Returns:
        SQL query string
    """
    if selected_cols:
        col_str = ", ".join(selected_cols)
        return f"select {col_str} from df"
    return "select * from df"
