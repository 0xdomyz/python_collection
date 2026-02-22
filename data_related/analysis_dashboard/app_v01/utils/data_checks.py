"""Data quality and overview utilities."""

import pandas as pd


def get_data_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Vertical view with sample value, dtype, null count, and DQ checks."""
    n_nulls = df.isnull().sum()
    n_zero = df.apply(lambda x: x == 0).sum()
    n_negative = df.select_dtypes(include="number").apply(lambda x: x < 0).sum()
    n_blank_str = (
        df.select_dtypes(include=object).apply(lambda x: x.str.strip() == "").sum()
    )

    info = pd.concat([df.head(1).T, df.dtypes, n_nulls], axis=1)
    info.columns = ["example_value", "dtype", "n_missing"]
    info["n_zero"] = n_zero
    info["n_negative"] = n_negative
    info["n_blank_str"] = n_blank_str

    return info.fillna(0).astype(
        {"n_missing": int, "n_zero": int, "n_negative": int, "n_blank_str": int}
    )
