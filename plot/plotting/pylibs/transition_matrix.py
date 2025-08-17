from matplotlib import ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

VERSION = "2025.08.17.21"


def plot_transition_matrix(
    tm_df: pd.DataFrame,
    color_tm_df: pd.DataFrame = None,
    bottom_tm_df: pd.DataFrame = None,
    tm_formatter: callable = lambda x: f"{x:.0f}" if x != 0 else "",
    bottom_tm_formatter: callable = lambda x: f"{x:.2%}" if x != 0 else "",
    title="",
    ax=None,
    figsize=(6, 5),
    fontsize=5,
    fontsize_bottom=None,
    colorbar_label=None,
    colorbar_formatter: callable = lambda x, _: f"{x*100:.0f}%",
):

    # inputs
    if color_tm_df is None:
        color_tm_df = tm_df.div(tm_df.sum(axis=1), axis=0).fillna(0)
    assert (
        tm_df.shape == color_tm_df.shape
    ), f"TM and color TM must have the same shape, they are: {tm_df.shape} vs {color_tm_df.shape}"

    if bottom_tm_df is not None:
        assert (
            tm_df.shape == bottom_tm_df.shape
        ), f"TM and bottom TM must have the same shape, they are: {tm_df.shape} vs {bottom_tm_df.shape}"

    fontsize_bottom = fontsize if fontsize_bottom is None else fontsize_bottom

    # ax
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    # ticks
    yticks, yticklabels, ylabel = range(len(tm_df.index)), tm_df.index, tm_df.index.name
    xticks, xticklabels, xlabel = (
        range(len(tm_df.columns)),
        tm_df.columns,
        tm_df.columns.name,
    )

    # color
    cax = ax.imshow(color_tm_df.values, cmap="Blues")
    color_threshold = color_tm_df.values.max() / 2

    # texts
    for i in yticks:
        for j in xticks:
            color_value = color_tm_df.values[i, j]  # row i, col j from top left
            text_color = "white" if color_value > color_threshold else "black"

            # plot in x pos j, y pos i from top left
            ax.text(
                j,
                i,
                tm_formatter(tm_df.iloc[i, j]),
                ha="center",
                va="center" if bottom_tm_df is None else "bottom",
                color=text_color,
                fontsize=fontsize,
            )

            # bottom
            if bottom_tm_df is not None:
                ax.text(
                    j,
                    i,
                    bottom_tm_formatter(bottom_tm_df.iloc[i, j]),
                    ha="center",
                    va="top",
                    color=text_color,
                    fontsize=fontsize_bottom,
                )

    # misc plot elements
    ax.plot(
        [0, max(xticks)], [max(yticks), 0], color="black", linewidth=0.5, linestyle="--"
    )  # bot left is origin in labels
    # ax.plot([0, max(xticks)], [0, max(yticks)], color="black", linewidth=0.5, linestyle="--")# top left is origin in labels

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_ylabel(ylabel)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_xlabel(xlabel)

    ax.set_title(title)

    ax.set_xticks(np.arange(-0.5, len(xticks), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(yticks), 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="--", linewidth=0.5)

    if colorbar_label:
        fig.colorbar(
            cax,
            label=colorbar_label,
            format=mticker.FuncFormatter(colorbar_formatter),
            orientation="vertical",
            pad=0.02,
        )

    return fig, ax
