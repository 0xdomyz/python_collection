# %%
import numpy as np
import pandas as pd


def interval_to_padded_str(interval: pd.Interval, max_digits: int) -> str:
    if not hasattr(interval, "left"):
        return "nan"
    left = str(int(interval.left)).zfill(max_digits)
    right = str(int(interval.right)).zfill(max_digits)
    return f"({left}, {right}]"


def make_binned_column(
    srs: pd.Series,
    bins: str | int | np.ndarray = "auto",
    fill_value: float = 0,
    make_padded_str: bool = False,
) -> pd.Series:
    series = srs.fillna(fill_value)
    edges = np.histogram_bin_edges(series, bins=bins)
    max_digits = max(len(str(int(edges.max()))), len(str(int(edges.min()))))

    binned_series = pd.cut(series, bins=edges)
    if make_padded_str:
        binned_series = binned_series.map(
            lambda interval: interval_to_padded_str(interval, max_digits)
        )
    return binned_series
