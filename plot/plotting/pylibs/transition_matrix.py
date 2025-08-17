from matplotlib import ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_transition_matrix(
    transition_matrix_df: pd.DataFrame,
    color_transition_matrix_df: pd.DataFrame = None,
    title="",
    display_transition_rates=True,
    ax=None,
    figsize=(6, 5),
    fontsize=5,
    colorbar_label=None,
):

    def text_formatter(x):
        return f"{x:.0f}" if x != 0 else ""

    def pct_formatter(x):
        return f"{x:.2%}" if x != 0 else ""

    pdf = transition_matrix_df.copy()
    pdf_color = (
        color_transition_matrix_df.copy()
        if color_transition_matrix_df is not None
        else pdf.div(pdf.sum(axis=1), axis=0)
    )
    assert (
        pdf.shape == pdf_color.shape
    ), f"Transition matrix and color transition matrix must have the same shape, they are: {pdf.shape} vs {pdf_color.shape}"

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    yticks, yticklabels, ylabel = range(len(pdf.index)), pdf.index, pdf.index.name
    xticks, xticklabels, xlabel = range(len(pdf.columns)), pdf.columns, pdf.columns.name

    cax = ax.imshow(pdf_color.values, cmap="Blues")
    color_threshold = pdf_color.values.max() / 2

    for i in yticks:
        for j in xticks:
            color_value = pdf_color.values[i, j]  # row i, col j from top left
            text_color = "white" if color_value > color_threshold else "black"

            va = "bottom" if display_transition_rates else "center"
            # plot in x pos j, y pos i from top left
            ax.text(
                j,
                i,
                text_formatter(pdf.iloc[i, j]),
                ha="center",
                va=va,
                color=text_color,
                fontsize=fontsize,
            )

            if display_transition_rates:
                ax.text(
                    j,
                    i,
                    pct_formatter(color_value),
                    ha="center",
                    va="top",
                    color=text_color,
                    fontsize=fontsize,
                )

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

    # Add minor ticks at halfway points
    ax.set_xticks(np.arange(-0.5, len(xticks), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(yticks), 1), minor=True)

    # Show grid at minor ticks (halfway points between cells)
    ax.grid(which="minor", color="gray", linestyle="--", linewidth=0.5)

    if colorbar_label:
        fig.colorbar(
            cax,
            label=colorbar_label,
            format=mticker.FuncFormatter(lambda x, _: f"{x*100:.0f}%"),
            orientation="vertical",
            pad=0.02,
        )

    return fig, ax
