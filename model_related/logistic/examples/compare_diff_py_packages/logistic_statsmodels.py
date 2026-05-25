"""Logistic regression using statsmodels on the Titanic dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from titanic_prep import load_titanic, prepare_features

SUMMARY_PATH = Path(__file__).parent / "logistic_statsmodels_summary.txt"


def train_statsmodels():
    raw = load_titanic()
    X_df, y_ser, stats, feature_names = prepare_features(raw)
    X = sm.add_constant(X_df)

    model = sm.Logit(y_ser, X)
    res = model.fit(disp=False, maxiter=200)

    SUMMARY_PATH.write_text(res.summary().as_text(), encoding="utf-8")
    print("Saved statsmodels summary to", SUMMARY_PATH)

    odds = pd.Series(res.params, index=["const"] + feature_names).apply(np.exp)
    print("Top odds ratios:\n", odds.sort_values(ascending=False).head(10))

    return res


if __name__ == "__main__":
    train_statsmodels()
