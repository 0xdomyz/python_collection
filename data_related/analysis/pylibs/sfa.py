import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


VERSION = "2025-09-06"


def calculate_signal(
    df,
    col,
    target_col,
    seg_col=None,
    exposure_col=None,
    exposure_on_target_too=True,
):

    df = df.copy()

    # placeholder col for segment column
    if seg_col is None:
        seg_col = "_seg"
        if seg_col in df.columns:
            raise ValueError(f"Column '{seg_col}' is reserved, change column name.")
        df[seg_col] = "all"

    # aggregate
    agg_dict = {}
    agg_dict["count"] = (target_col, np.size)
    agg_dict[target_col] = (target_col, "sum")
    if exposure_col is not None:
        agg_dict[exposure_col] = (exposure_col, "sum")

        if exposure_on_target_too:
            tar_exp = f"{target_col}_{exposure_col}"
            df[tar_exp] = df[target_col].mul(df[exposure_col])
            agg_dict[tar_exp] = (tar_exp, "sum")

    _ = df.groupby([seg_col, col], dropna=False, observed=False)
    _ = _.agg(**agg_dict)

    # count dist
    grps = _.groupby(seg_col, dropna=False, observed=False)
    for name, group in grps:
        group["count_dist"] = group["count"].div(group["count"].sum())
        _.loc[group.index, ["count_dist"]] = group[["count_dist"]]

    # rates
    grps = _.groupby(seg_col, dropna=False, observed=False)
    for name, group in grps:
        group[f"{target_col}_dist"] = group[target_col].div(group[target_col].sum())
        group[f"{target_col}_rate"] = group[target_col].div(group["count"])
        _.loc[group.index, [f"{target_col}_dist", f"{target_col}_rate"]] = group[
            [f"{target_col}_dist", f"{target_col}_rate"]
        ]

    # exp rates
    if exposure_col is not None:
        grps = _.groupby(seg_col, dropna=False, observed=False)
        for name, group in grps:
            group[f"{tar_exp}_dist"] = group[tar_exp].div(group[tar_exp].sum())
            group[f"{tar_exp}_rate"] = group[tar_exp].div(group[exposure_col])

            _.loc[group.index, [f"{tar_exp}_dist", f"{tar_exp}_rate"]] = group[
                [f"{tar_exp}_dist", f"{tar_exp}_rate"]
            ]

    if seg_col == "_seg":
        _.index = _.index.droplevel(0)

    return _


import matplotlib.ticker as mtick


def plot_one_bar_and_line(
    df,
    col,
    target_col,
    rotation=0,
    y_lim=(None, None),
    ax2_y_lim=(None, None),
    figsize=(7.5, 5),
    ax=None,
    pct_decimals=1,
    title_prefix="",
):
    df2 = df.copy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    index = df2.index
    title = f"{col} & {target_col} by {index.name}"
    x_ticks = index.astype(str)

    ax.bar(x_ticks, df2[col])
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, rotation=rotation)
    ax.set_xlabel(index.name)
    ax.set_ylabel(col, loc="center")
    ax.set_ylim(*y_lim)
    ax.set_title(f"{title_prefix}{title}")

    ax2 = ax.twinx()
    ax2.plot(x_ticks, df2[target_col], color="red", marker="o")
    ax2.set_ylabel(target_col, loc="bottom")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=pct_decimals))
    ax2.set_ylim(*ax2_y_lim)

    return fig, (ax, ax2)


def plot_multi_lines(
    df,
    col,
    rotation=0,
    y_lim=(None, None),
    figsize=(15, 5),
    ax=None,
    pct_decimals=None,
):
    df2 = df.copy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # first index is the segments, second is the x-axis
    index_names = df2.index.names
    df2.reset_index(inplace=True)
    pdf = df2.pivot(index=index_names[1], columns=index_names[0], values=col)
    pdf.plot(
        ax=ax,
        marker="o",
        rot=rotation,
        title=f"{col} by {index_names[1]}",
        legend=True,
        xlabel=index_names[1],
        ylabel=col,
        ylim=y_lim,
        grid=True,
    )
    if pct_decimals is not None:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=pct_decimals))

    return fig, ax, pdf


def plot_bar_and_line_by_segment(
    df,
    col,
    target_col,
    rotation=0,
    y_lim=(None, None),
    ax2_y_lim=(None, None),
    figsize=(15, 5),
    plots_in_each_row=2,
    pct_decimals=1,
):

    df2 = df.copy()

    # plot for each segment
    segs = df2.index.levels[0]

    rows = int(np.ceil(len(segs) / plots_in_each_row))

    for row in range(rows):
        start = row * plots_in_each_row
        end = start + plots_in_each_row

        df3 = df2.loc[segs[start:end], :]

        fig, ax = plt.subplots(1, plots_in_each_row, figsize=figsize)

        indexes_in_this_row = df3.index.levels[0][start:end]
        for i, seg in enumerate(indexes_in_this_row):
            if plots_in_each_row == 1:
                ax2 = ax
            else:
                ax2 = ax[i]

            # plot each segment
            plot_one_bar_and_line(
                df=df3.loc[seg],
                col=col,
                target_col=target_col,
                rotation=rotation,
                y_lim=y_lim,
                ax2_y_lim=ax2_y_lim,
                ax=ax2,
                pct_decimals=pct_decimals,
                title_prefix=f"{seg} - ",
            )


def plot_bar_and_line_dist_pairs_by_segment(
    df,
    col,
    target_col,
    rotation=0,
    y_lim=(None, None),
    y_lim2=(None, None),
    ax2_y_lim=(None, None),
    figsize=(15, 5),
    pct_decimals=1,
):

    df2 = df.copy()

    # add dummy index for single level
    if df2.index.nlevels == 1:
        df2.index = pd.MultiIndex.from_product(
            [["all"], df2.index], names=["all", df2.index.name]
        )
    elif len(df2.index.levels) > 2:
        raise ValueError(
            f"index levels in input can only be 1 or 2, {df2.index.levels = }"
        )

    # plot for each segment
    segs = df2.index.levels[0]

    for seg in segs:

        df3 = df2.loc[seg, :]

        fig, ax = plt.subplots(1, 2, figsize=figsize)

        if segs.size > 1:
            fig.suptitle(f"{seg}", fontsize=16)

        plot_one_bar_and_line(
            df=df3,
            col=col,
            target_col=target_col,
            rotation=rotation,
            y_lim=y_lim,
            ax2_y_lim=ax2_y_lim,
            ax=ax[0],
            pct_decimals=pct_decimals,
        )
        plot_one_bar_and_line(
            df=df3,
            col=f"{col}_dist",
            target_col=target_col,
            rotation=rotation,
            y_lim=y_lim2,
            ax2_y_lim=ax2_y_lim,
            ax=ax[1],
            pct_decimals=pct_decimals,
        )

    plt.show()
