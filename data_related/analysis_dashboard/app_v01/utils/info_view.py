"""Info view utilities - vertical information display."""

import pandas as pd


def create_vertical_info_view(df):
    """
    Create a vertical info view with example value, dtype, and null count.

    Args:
        df: DataFrame

    Returns:
        DataFrame with columns: example_value, dtypes, n_null
    """
    info_view = pd.concat([df.head(1).T, df.dtypes, df.isna().sum()], axis=1)
    info_view.columns = ["example_value", "dtypes", "n_null"]
    return info_view
