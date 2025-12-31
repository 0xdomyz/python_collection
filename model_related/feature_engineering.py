"""
Feature engineering utilities and transformations.

Common patterns for feature creation, encoding, and scaling.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "drop", fill_value: Optional[float] = None
) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.

    Args:
        df: Input DataFrame
        strategy: 'drop', 'mean', 'median', 'forward_fill', 'backward_fill', or 'constant'
        fill_value: Value for 'constant' strategy

    Returns:
        DataFrame with missing values handled

    Example:
        >>> df_clean = handle_missing_values(df, strategy='median')
    """
    if strategy == "drop":
        return df.dropna()
    elif strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == "median":
        return df.fillna(df.median(numeric_only=True))
    elif strategy == "forward_fill":
        return df.fillna(method="ffill")
    elif strategy == "backward_fill":
        return df.fillna(method="bfill")
    elif strategy == "constant":
        return df.fillna(fill_value)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def detect_outliers(
    series: pd.Series, method: str = "iqr", threshold: float = 1.5
) -> pd.Series:
    """
    Detect outliers in a series.

    Args:
        series: Data series
        method: 'iqr' (interquartile range) or 'zscore'
        threshold: IQR multiplier or Z-score threshold

    Returns:
        Boolean Series indicating outliers

    Example:
        >>> outliers = detect_outliers(df['price'], method='iqr')
        >>> df_clean = df[~outliers]
    """
    if method == "iqr":
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (series < lower_bound) | (series > upper_bound)

    elif method == "zscore":
        from scipy import stats

        z_scores = np.abs(stats.zscore(series.dropna()))
        return np.abs(stats.zscore(series)) > threshold

    else:
        raise ValueError(f"Unknown method: {method}")


def create_interaction_features(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    Create interaction features between specified columns.

    Args:
        df: Input DataFrame
        cols: Columns to interact

    Returns:
        DataFrame with interaction features added

    Example:
        >>> df_inter = create_interaction_features(df, ['age', 'income'])
    """
    df_copy = df.copy()

    for i, col1 in enumerate(cols):
        for col2 in cols[i + 1 :]:
            df_copy[f"{col1}_x_{col2}"] = df[col1] * df[col2]

    return df_copy


def create_polynomial_features(
    df: pd.DataFrame, cols: List[str], degree: int = 2
) -> pd.DataFrame:
    """
    Create polynomial features.

    Args:
        df: Input DataFrame
        cols: Columns to polynomialize
        degree: Polynomial degree

    Returns:
        DataFrame with polynomial features

    Example:
        >>> df_poly = create_polynomial_features(df, ['price'], degree=2)
    """
    df_copy = df.copy()

    for col in cols:
        for d in range(2, degree + 1):
            df_copy[f"{col}_pow{d}"] = df[col] ** d

    return df_copy


def categorical_encoding(
    df: pd.DataFrame, cols: List[str], method: str = "onehot"
) -> pd.DataFrame:
    """
    Encode categorical variables.

    Args:
        df: Input DataFrame
        cols: Categorical columns to encode
        method: 'onehot' or 'label'

    Returns:
        DataFrame with encoded columns

    Example:
        >>> df_encoded = categorical_encoding(df, ['color', 'size'], method='onehot')
    """
    if method == "onehot":
        return pd.get_dummies(df, columns=cols, drop_first=True)

    elif method == "label":
        df_copy = df.copy()
        for col in cols:
            df_copy[col] = pd.factorize(df[col])[0]
        return df_copy

    else:
        raise ValueError(f"Unknown method: {method}")


def scale_features(
    df: pd.DataFrame, cols: List[str], method: str = "standard"
) -> Tuple[pd.DataFrame, Dict]:
    """
    Scale numeric features.

    Args:
        df: Input DataFrame
        cols: Columns to scale
        method: 'standard' (z-score) or 'minmax'

    Returns:
        Scaled DataFrame and scaling parameters for inverse transform

    Example:
        >>> df_scaled, params = scale_features(df, ['price', 'age'])
    """
    df_copy = df.copy()
    params = {}

    if method == "standard":
        for col in cols:
            mean = df[col].mean()
            std = df[col].std()
            df_copy[col] = (df[col] - mean) / std
            params[col] = {"mean": mean, "std": std}

    elif method == "minmax":
        for col in cols:
            min_val = df[col].min()
            max_val = df[col].max()
            df_copy[col] = (df[col] - min_val) / (max_val - min_val)
            params[col] = {"min": min_val, "max": max_val}

    else:
        raise ValueError(f"Unknown method: {method}")

    return df_copy, params


def select_numeric_features(df: pd.DataFrame) -> List[str]:
    """
    Get numeric column names.

    Args:
        df: Input DataFrame

    Returns:
        List of numeric column names

    Example:
        >>> nums = select_numeric_features(df)
    """
    return df.select_dtypes(include=["number"]).columns.tolist()


def select_categorical_features(df: pd.DataFrame) -> List[str]:
    """
    Get categorical column names.

    Args:
        df: Input DataFrame

    Returns:
        List of categorical column names

    Example:
        >>> cats = select_categorical_features(df)
    """
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def feature_selection_by_variance(
    X: pd.DataFrame, threshold: float = 0.01
) -> List[str]:
    """
    Select features with variance above threshold.

    Args:
        X: Feature DataFrame
        threshold: Variance threshold

    Returns:
        List of selected feature names

    Example:
        >>> selected = feature_selection_by_variance(X, threshold=0.01)
    """
    variances = X.var()
    return variances[variances > threshold].index.tolist()


def correlation_filter(
    df: pd.DataFrame, threshold: float = 0.9, drop_first: bool = True
) -> pd.DataFrame:
    """
    Remove highly correlated features.

    Args:
        df: Feature DataFrame
        threshold: Correlation threshold
        drop_first: Drop first feature in correlated pair

    Returns:
        DataFrame with uncorrelated features

    Example:
        >>> df_uncorr = correlation_filter(df, threshold=0.9)
    """
    corr_matrix = df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    return df.drop(columns=to_drop)
