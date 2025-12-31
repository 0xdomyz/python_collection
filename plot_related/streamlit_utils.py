"""
Streamlit utility functions for interactive dashboards.

Common patterns for building Streamlit apps with caching and data loading.
"""

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


@st.cache_data
def load_csv_file(filepath: str) -> pd.DataFrame:
    """
    Load CSV with caching.

    Args:
        filepath: Path to CSV file

    Returns:
        Loaded DataFrame

    Example:
        >>> df = load_csv_file('data.csv')
    """
    return pd.read_csv(filepath)


@st.cache_data
def load_dataset(name: str) -> pd.DataFrame:
    """
    Load seaborn dataset with caching.

    Args:
        name: Dataset name (e.g., 'titanic', 'tips', 'iris')

    Returns:
        Loaded DataFrame

    Example:
        >>> df = load_dataset('titanic')
    """
    import seaborn as sns

    return sns.load_dataset(name)


def display_data_summary(df: pd.DataFrame) -> None:
    """
    Display dataset summary in Streamlit.

    Shows shape, data types, missing values.

    Args:
        df: DataFrame to summarize

    Example:
        >>> display_data_summary(df)
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        missing_pct = df.isna().sum().sum() / (df.shape[0] * df.shape[1]) * 100
        st.metric("Missing %", f"{missing_pct:.1f}%")

    st.subheader("Data Types")
    st.write(df.dtypes)

    st.subheader("Missing Values")
    st.write(df.isna().sum())


def create_column_selector(
    df: pd.DataFrame, label: str = "Select column", include_types: Optional[list] = None
) -> str:
    """
    Create selectbox for column selection.

    Args:
        df: DataFrame
        label: Selectbox label
        include_types: Data types to include (e.g., ['float64', 'int64'])

    Returns:
        Selected column name

    Example:
        >>> col = create_column_selector(df, include_types=['float64'])
    """
    if include_types:
        cols = [c for c in df.columns if df[c].dtype in include_types]
    else:
        cols = df.columns.tolist()

    return st.selectbox(label, cols)


def plot_column_distribution(df: pd.DataFrame, col: str) -> None:
    """
    Plot distribution of a column interactively.

    Args:
        df: DataFrame
        col: Column name

    Example:
        >>> plot_column_distribution(df, 'age')
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(8, 5))

    if df[col].dtype in ["float64", "int64"]:
        sns.histplot(data=df, x=col, kde=True, ax=ax)
    else:
        sns.countplot(data=df, x=col, ax=ax)

    ax.set_title(f"Distribution of {col}")
    st.pyplot(fig)


def create_filter_widget(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Create filter widget for a column and return filtered DataFrame.

    Args:
        df: DataFrame
        col: Column to filter on

    Returns:
        Filtered DataFrame

    Example:
        >>> df_filtered = create_filter_widget(df, 'category')
    """
    if df[col].dtype in ["float64", "int64"]:
        min_val, max_val = float(df[col].min()), float(df[col].max())
        selected = st.slider(
            f"Select {col} range", min_val, max_val, (min_val, max_val)
        )
        return df[(df[col] >= selected[0]) & (df[col] <= selected[1])]
    else:
        options = df[col].unique().tolist()
        selected = st.multiselect(f"Select {col}", options, default=options)
        return df[df[col].isin(selected)]


def display_metrics_row(metrics_dict: dict, cols: int = 3) -> None:
    """
    Display metrics in a grid layout.

    Args:
        metrics_dict: Dictionary of {label: value}
        cols: Number of columns

    Example:
        >>> display_metrics_row({'Mean': 42.5, 'Median': 41.0, 'Std': 12.3})
    """
    columns = st.columns(cols)

    for idx, (label, value) in enumerate(metrics_dict.items()):
        with columns[idx % cols]:
            st.metric(label, f"{value:.2f}" if isinstance(value, float) else value)
