from matplotlib import ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

VERSION = "2025.09.28.00"


### data
def calc_transition_matrixes_from_signal_with_level_alignment(
    signal_df: pd.DataFrame,
    from_col: str,
    to_col: str,
    n_col: str = "n",
    signal_col: str = "signal",
    from_levels: list = None,
    to_levels: list = None,
):
    """
    Signal df is result of group by as_index False that calcs volume and signals
    """
    assert (
        from_col in signal_df.columns and to_col in signal_df.columns
    ), f"columns {from_col} and {to_col} must be in signal_df"

    # fill gaps
    if from_levels is None and to_levels is not None:
        from_levels = signal_df[from_col].unique()
    elif to_levels is None and from_levels is not None:
        to_levels = signal_df[to_col].unique()

    if from_levels is not None and to_levels is not None:
        spine = pd.MultiIndex.from_product(
            [from_levels, to_levels], names=[from_col, to_col]
        ).to_frame(index=False)
        signal_df = spine.merge(signal_df, on=[from_col, to_col], how="left")

    # pdfs
    pdf = signal_df.pivot(index=from_col, columns=to_col).sort_index(
        axis=0, ascending=False, na_position="first"
    )
    pdf_n = (
        pdf.xs(n_col, axis=1, level=0).sort_index(axis=1, na_position="last").fillna(0)
    )
    pdf_s = (
        pdf.xs(signal_col, axis=1, level=0)
        .sort_index(axis=1, na_position="last")
        .fillna(0)
    )
    return pdf_n, pdf_s


def make_spine_from_cols(from_srs: pd.Series, to_srs: pd.Series) -> pd.DataFrame:
    from_vals = from_srs.unique()
    to_vals = to_srs.unique()
    spine = pd.MultiIndex.from_product(
        [from_vals, to_vals], names=[from_srs.name, to_srs.name]
    ).to_frame(index=False)
    return spine


### plot
def plot_transition_matrix(
    pdf_n: pd.DataFrame,
    pdf_s: pd.DataFrame = None,
    pdf_c: pd.DataFrame = None,
    n_formatter: callable = lambda x: f"{x:.0f}" if x != 0 else "",
    s_formatter: callable = lambda x: f"{x:.2%}" if x != 0 else "",
    colorbar_formatter: callable = lambda x, _: f"{x*100:.0f}%",
    n_fontsize=9,
    s_fontsize=9,
    ax=None,
    figsize=(8, 8),
    title="Transition Matrix",
    colorbar_label="Signal %",
):

    # data
    if pdf_s is None and pdf_c is None:
        pdf_s = pdf_n.div(pdf_n.sum(axis=1), axis=0).fillna(0)
        pdf_c = pdf_s
    elif pdf_s is not None and pdf_c is None:
        pdf_c = pdf_s

    s_values = pdf_s.values if pdf_s is not None else None
    c_values = pdf_c.values if pdf_c is not None else None

    # ax and ticks
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    yticklabels = pdf_n.index
    xticklabels = pdf_n.columns
    yticks = range(len(yticklabels))
    xticks = range(len(xticklabels))
    ylabel = pdf_n.index.name if yticklabels.name is not None else "From"
    xlabel = pdf_n.columns.name if xticklabels.name is not None else "To"

    # content
    ax, cax = plot_nsc_tm_content(
        ax=ax,
        yticklabels=yticklabels,
        xticklabels=xticklabels,
        n_values=pdf_n.values,
        s_values=s_values,
        c_values=c_values,
        n_formatter=n_formatter,
        s_formatter=s_formatter,
        n_fontsize=n_fontsize,
        s_fontsize=s_fontsize,
    )

    # decorations
    ax.set_yticks(yticks)
    ax.set_yticks(np.arange(-0.5, len(yticks), 1), minor=True)
    ax.set_yticklabels(yticklabels)
    ax.set_ylabel(ylabel)

    ax.set_xticks(xticks)
    ax.set_xticks(np.arange(-0.5, len(xticks), 1), minor=True)
    ax.set_xticklabels(xticklabels)
    ax.set_xlabel(xlabel)

    ax.set_title(title)
    ax.grid(which="minor", color="gray", linestyle="--", linewidth=0.5)

    if pdf_c is not None and colorbar_label is not None:
        fig.colorbar(
            cax,
            label=colorbar_label,
            format=mticker.FuncFormatter(colorbar_formatter),
            orientation="vertical",
            pad=0.02,
        )

    return fig, ax, cax


def plot_nsc_tm_content(
    ax: plt.Axes,
    yticklabels: list,
    xticklabels: list,
    n_values: np.ndarray,
    s_values: np.ndarray = None,
    c_values: np.ndarray = None,
    n_formatter: callable = lambda x: f"{x:.0f}" if x != 0 else "",
    s_formatter: callable = lambda x: f"{x:.2%}" if x != 0 else "",
    n_fontsize=8,
    s_fontsize=8,
    cmap="Blues",
):
    # check
    n_values = np.asarray(n_values)
    if c_values is not None:
        assert (
            n_values.shape == c_values.shape
        ), f"n_values and c_values must have the same shape, they are: {n_values.shape} vs {c_values.shape}"
    if s_values is not None:
        assert (
            n_values.shape == s_values.shape
        ), f"n_values and s_values must have the same shape, they are: {n_values.shape} vs {s_values.shape}"

    # ticks
    yticks = range(len(yticklabels))
    xticks = range(len(xticklabels))

    # element - color
    cax = ax.imshow(c_values, cmap=cmap)
    color_threshold = c_values.max() / 2

    # element - texts
    for i in yticks:
        for j in xticks:
            # ticks: i, j is coordinates: j, i
            color_value = c_values[i, j]
            text_color = "white" if color_value > color_threshold else "black"

            # n text
            ax.text(
                j,
                i,
                n_formatter(n_values[i, j]),
                ha="center",
                va="center" if s_values is None else "bottom",
                color=text_color,
                fontsize=n_fontsize,
            )

            # signal text
            if s_values is not None:
                ax.text(
                    j,
                    i,
                    s_formatter(s_values[i, j]),
                    ha="center",
                    va="top",
                    color=text_color,
                    fontsize=s_fontsize,
                )

    # element - diagonal line
    ax.plot(
        [0, max(xticks)], [max(yticks), 0], color="black", linewidth=0.5, linestyle="--"
    )

    return ax, cax
