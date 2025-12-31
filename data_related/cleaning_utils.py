"""Common data cleaning patterns."""

import pandas as pd
import numpy as np


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names: strip whitespace, replace spaces with underscores, lowercase.
    
    Example:
        >>> df = pd.DataFrame({'col A': [1, 2], ' col B': [3, 4]})
        >>> standardize_column_names(df).columns.tolist()
        ['col_a', 'col_b']
    """
    return df.rename(columns=lambda x: x.strip().str.replace(' ', '_').str.lower())


def detect_data_quality_issues(df: pd.DataFrame) -> dict:
    """
    Detect common data quality issues: missing values, zeros, negatives, blanks.
    
    Returns:
        dict with column-level statistics
    """
    issues = {}
    for col in df.columns:
        issues[col] = {
            'n_missing': df[col].isna().sum(),
            'n_zeros': (df[col] == 0).sum() if df[col].dtype in ['int64', 'float64'] else 0,
            'n_negative': (df[col] < 0).sum() if df[col].dtype in ['int64', 'float64'] else 0,
            'n_blank_string': (df[col] == '').sum() if df[col].dtype == 'object' else 0,
        }
    return issues