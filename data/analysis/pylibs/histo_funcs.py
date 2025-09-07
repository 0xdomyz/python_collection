import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

VERSION = "2025-09-07"


def calc_7_numbers(dat: pd.Series) -> list[float]:
    qtls = dat.quantile([0.25, 0.5, 0.75]).to_list()
    icr_1_point_5 = (qtls[2] - qtls[0]) * 1.5
    fivnum = [
        dat.min(),
        max(qtls[0] - icr_1_point_5, dat.min()),
        qtls[0],
        qtls[1],
        qtls[2],
        min(qtls[2] + icr_1_point_5, dat.max()),
        dat.max(),
    ]
    return fivnum


def even_width_bins(dat: pd.Series, nbins: int) -> list[float]:
    return np.arange(
        dat.min(),
        dat.max() + (dat.max() - dat.min()) / nbins,
        (dat.max() - dat.min()) / nbins,
    )


def bin_cat_to_pct_labels(cats: pd.Index) -> list[str]:
    """cat is [)"""
    labels = []
    for category in cats:
        if pd.isna(category):
            labels.append("NaN")
        else:
            left = category.left
            right = category.right
            mid = (left + right) / 2
            labels.append(f"[{left:.0%} - {right:.0%})")
    return labels


def bin_cat_to_mid_labels(cats: pd.Index) -> list[str]:
    labels = []
    for category in cats:
        if pd.isna(category):
            labels.append("NaN")
        else:
            left = category.left
            right = category.right
            mid = (left + right) / 2
            labels.append(f"~{mid:.0%}")
    return labels


def calc_freq_signal(sdf: pd.DataFrame, col) -> pd.DataFrame:
    sdf = (
        sdf.loc[lambda x: x[col].notna(), :]
        .groupby([col], dropna=False, observed=False)
        .agg(
            **{
                "n": (col, "size"),
            }
        )
    )
    sdf[f"{col}_freq"] = sdf["n"] / sdf["n"].sum()
    return sdf


def plot_pct_interval_histogram(x_ticks, x_labels, y, ax=None) -> tuple:

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    else:
        fig = ax.get_figure()

    ax.bar(
        x_ticks,
        y,
        width=0.8,
        alpha=0.7,
        color="lightblue",
        edgecolor="black",
    )
    for x, yv in zip(x_ticks, y):
        ax.text(x, yv, f"{yv:.1%}", ha="center", va="bottom")
    ax.set_xticks(x_ticks, x_labels, rotation=45, ha="right")

    ax.grid(True, linestyle="--", alpha=0.5)

    return fig, ax


def pct_histogram_from_edges(
    df: pd.DataFrame, ff: callable, col: str, edges: list, ax: None
) -> tuple:

    df[f"{col}_binned"] = None
    df.loc[ff, f"{col}_binned"] = pd.cut(df.loc[ff, col], bins=edges, right=False)
    freqs = calc_freq_signal(df.loc[ff], col=f"{col}_binned")
    fig, ax = plot_pct_interval_histogram(
        x_ticks=np.arange(freqs.shape[0], dtype=int),
        x_labels=bin_cat_to_pct_labels(freqs.index),
        y=freqs[f"{col}_binned_freq"],
        ax=ax,
    )
    return freqs, fig, ax
