"""
Reusable plotting utility functions.

Common patterns for matplotlib, seaborn, and plotly visualizations.
"""

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_style(style: str = "whitegrid", palette: str = "husl") -> None:
    """
    Set consistent seaborn style and matplotlib parameters.

    Args:
        style: seaborn style ('darkgrid', 'whitegrid', 'dark', 'white', 'ticks')
        palette: seaborn palette ('husl', 'deep', 'pastel', 'Set1', etc.)

    Example:
        >>> set_style("whitegrid", "deep")
    """
    import seaborn as sns

    sns.set_style(style)
    sns.set_palette(palette)
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 11


def create_subplots(rows: int, cols: int, figsize: Tuple[int, int] = (12, 8)):
    """
    Create matplotlib subplots with consistent sizing.

    Args:
        rows: Number of rows
        cols: Number of columns
        figsize: Figure size tuple (width, height)

    Returns:
        fig, axes tuple

    Example:
        >>> fig, axes = create_subplots(2, 2)
    """
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1 and cols == 1:
        axes = np.array([axes])  # Handle single subplot case
    axes = axes.flatten() if axes.ndim > 1 else axes
    return fig, axes


def plot_distribution(
    data: pd.Series, title: str = "", ax=None, kde: bool = True
) -> None:
    """
    Plot distribution with histogram and optional KDE.

    Args:
        data: Series to plot
        title: Plot title
        ax: Matplotlib axes (creates new if None)
        kde: Include KDE line

    Example:
        >>> plot_distribution(df['age'], title='Age Distribution')
    """
    import seaborn as sns

    if ax is None:
        fig, ax = plt.subplots()

    sns.histplot(data, kde=kde, ax=ax)
    ax.set_title(title or f"Distribution of {data.name}")
    ax.set_xlabel(data.name)


def plot_correlation_heatmap(
    df: pd.DataFrame,
    figsize: Tuple[int, int] = (10, 8),
    annot: bool = True,
    cmap: str = "coolwarm",
) -> None:
    """
    Plot correlation heatmap for numeric columns.

    Args:
        df: DataFrame with numeric columns
        figsize: Figure size
        annot: Show correlation values
        cmap: Color map

    Example:
        >>> plot_correlation_heatmap(df.select_dtypes(include='number'))
    """
    import seaborn as sns

    corr = df.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap=cmap, center=0, ax=ax, square=True)
    ax.set_title("Correlation Heatmap")


def plot_categorical_vs_numeric(
    df: pd.DataFrame, cat_col: str, num_col: str, kind: str = "box", ax=None
) -> None:
    """
    Plot relationship between categorical and numeric columns.

    Args:
        df: DataFrame
        cat_col: Categorical column name
        num_col: Numeric column name
        kind: Plot type ('box', 'violin', 'strip')
        ax: Matplotlib axes

    Example:
        >>> plot_categorical_vs_numeric(df, 'category', 'value', kind='violin')
    """
    import seaborn as sns

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if kind == "box":
        sns.boxplot(data=df, x=cat_col, y=num_col, ax=ax)
    elif kind == "violin":
        sns.violinplot(data=df, x=cat_col, y=num_col, ax=ax)
    elif kind == "strip":
        sns.stripplot(data=df, x=cat_col, y=num_col, ax=ax)

    ax.set_title(f"{num_col} by {cat_col}")


def add_gridlines(ax, alpha: float = 0.3, linestyle: str = "--") -> None:
    """
    Add consistent gridlines to plot.

    Args:
        ax: Matplotlib axes
        alpha: Grid transparency
        linestyle: Line style
    """
    ax.grid(True, alpha=alpha, linestyle=linestyle)


def save_and_show(
    fig, filename: Optional[str] = None, dpi: int = 300, show: bool = True
) -> None:
    """
    Save figure to file and optionally display.

    Args:
        fig: Matplotlib figure
        filename: Optional filename to save (e.g., 'plot.png')
        dpi: Resolution for saved file
        show: Whether to display plot

    Example:
        >>> save_and_show(fig, 'output.png', show=True)
    """
    if filename:
        fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"Saved to {filename}")

    if show:
        plt.show()
