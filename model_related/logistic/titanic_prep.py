"""Utilities to load and preprocess Titanic data for logistic regression examples.

- Uses the public seaborn titanic CSV URL to avoid extra dependencies.
- Fills missing numeric columns with medians and categorical with modes.
- One-hot encodes categorical features with `drop_first=True` for identifiability.
- Records preprocessing statistics so scoring can reuse them.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"


@dataclass
class PreprocessStats:
    numeric_median: Dict[str, float]
    categorical_mode: Dict[str, str]

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        return {
            "numeric_median": self.numeric_median,
            "categorical_mode": self.categorical_mode,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, str]]) -> "PreprocessStats":
        return cls(
            numeric_median=data.get("numeric_median", {}),
            categorical_mode=data.get("categorical_mode", {}),
        )


FEATURE_COLS = [
    "pclass",
    "sex",
    "age",
    "fare",
    "embarked",
    "sibsp",
    "parch",
]
TARGET_COL = "survived"


def load_titanic(path: str | Path | None = None) -> pd.DataFrame:
    """Load Titanic dataset from path or remote URL."""
    if path:
        return pd.read_csv(path)
    return pd.read_csv(DATA_URL)


def _compute_stats(df: pd.DataFrame) -> PreprocessStats:
    numeric_cols = ["age", "fare", "sibsp", "parch"]
    categorical_cols = ["sex", "embarked", "pclass"]
    numeric_median = {col: float(df[col].median()) for col in numeric_cols}
    categorical_mode = {
        col: (
            str(df[col].mode(dropna=True)[0])
            if not df[col].mode(dropna=True).empty
            else ""
        )
        for col in categorical_cols
    }
    return PreprocessStats(
        numeric_median=numeric_median, categorical_mode=categorical_mode
    )


def prepare_features(
    df: pd.DataFrame, stats: PreprocessStats | None = None
) -> Tuple[pd.DataFrame, pd.Series, PreprocessStats, List[str]]:
    """Clean, engineer, and one-hot encode features.

    Returns
    -------
    X : pd.DataFrame
        Feature matrix after encoding.
    y : pd.Series
        Target vector (survived).
    stats : PreprocessStats
        Medians/modes used to fill missing values.
    feature_names : list[str]
        Column names after encoding.
    """

    df = df.copy()
    stats = stats or _compute_stats(df)

    # Fill missing values
    for col, med in stats.numeric_median.items():
        df[col] = df[col].fillna(med)
    for col, mode in stats.categorical_mode.items():
        if mode:
            df[col] = df[col].fillna(mode)

    df["family_size"] = df["sibsp"] + df["parch"] + 1

    y = df[TARGET_COL].astype(int)
    feature_df = df[FEATURE_COLS + ["family_size"]]
    X = pd.get_dummies(
        feature_df, columns=["sex", "embarked", "pclass"], drop_first=True
    )
    feature_names = X.columns.tolist()
    return X, y, stats, feature_names


def train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Simple deterministic split without sklearn dependency."""
    n = len(X)
    rng = np.random.default_rng(seed)
    idx = np.arange(n)
    rng.shuffle(idx)
    split = int(n * (1 - test_size))
    train_idx, test_idx = idx[:split], idx[split:]
    X_train, X_test = X.iloc[train_idx].to_numpy(), X.iloc[test_idx].to_numpy()
    y_train, y_test = y.iloc[train_idx].to_numpy(), y.iloc[test_idx].to_numpy()
    return X_train, X_test, y_train, y_test
