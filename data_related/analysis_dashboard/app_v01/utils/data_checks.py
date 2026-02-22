"""Data quality check utilities."""

import numpy as np
import pandas as pd


def compute_data_quality_checks(df):
    """
    Compute data quality metrics: missing, zero, negative, blank string counts.

    Returns:
        dict with 'counts' and 'percentages' DataFrames
    """
    n_nulls = df.isnull().sum()
    n_zero = df.apply(lambda x: x == 0).sum()
    n_negative = df.select_dtypes(include="number").apply(lambda x: x < 0).sum()
    n_blank_str = (
        df.select_dtypes(include=object).apply(lambda x: x.str.strip() == "").sum()
    )

    # Create counts dataframe
    counts_df = (
        pd.DataFrame(
            {
                "n_missing": n_nulls,
                "n_zero": n_zero,
                "n_negative": n_negative,
                "n_blank_string": n_blank_str,
            }
        )
        .fillna(0)
        .astype(int)
    )

    # Create percentages dataframe
    pct_df = (
        counts_df.div(df.shape[0])
        .mul(100)
        .round(2)
        .rename(columns=lambda x: x + "_pct")
    )

    return {"counts": counts_df, "percentages": pct_df}
