# %%
import numpy as np
import pandas as pd


def _make_sortable_labels(cats: pd.Index) -> dict:
    pad = max(2, len(str(len(cats) - 1)))
    label_map = {iv: f"{i:0{pad}d} {iv}" for i, iv in enumerate(cats)}
    return label_map


def make_binned_column_even(
    srs: pd.Series,
    bins: str | int | np.ndarray = "auto",
    sortable_str: bool = False,
) -> pd.Series:
    srs2 = srs.dropna()
    edges = np.histogram_bin_edges(srs2, bins=bins)
    binned_series = pd.cut(srs, bins=edges)

    if sortable_str:
        label_map = _make_sortable_labels(binned_series.cat.categories)
        binned_series = binned_series.cat.rename_categories(label_map)
    return binned_series


def make_binned_column_quantile(
    srs: pd.Series,
    q: int = 10,
    sortable_str: bool = False,
) -> pd.Series:
    edges = pd.qcut(srs, q=q, duplicates="drop").cat.categories
    binned_series = pd.cut(srs, bins=edges)

    if sortable_str:
        label_map = _make_sortable_labels(binned_series.cat.categories)
        binned_series = binned_series.cat.rename_categories(label_map)
    return binned_series
