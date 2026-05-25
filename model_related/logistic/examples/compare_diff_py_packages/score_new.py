"""Score new Titanic-like records using the NumPy logistic regression artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from titanic_prep import PreprocessStats, prepare_features

ARTIFACT_DIR = Path(__file__).parent
MODEL_PATH = ARTIFACT_DIR / "logistic_numpy_model.npz"
STATS_PATH = ARTIFACT_DIR / "logistic_numpy_stats.json"
DEFAULT_INPUT = ARTIFACT_DIR / "sample_new_data.csv"


def load_artifacts():
    npz = np.load(MODEL_PATH, allow_pickle=True)
    weights = npz["weights"]
    bias = float(npz["bias"])
    feature_names = npz["feature_names"].tolist()
    stats = PreprocessStats.from_dict(
        json.loads(STATS_PATH.read_text(encoding="utf-8"))
    )
    return weights, bias, feature_names, stats


def align_features(X: pd.DataFrame, feature_names: List[str]) -> np.ndarray:
    return X.reindex(columns=feature_names, fill_value=0).to_numpy()


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-z))


def score(input_path: Path = DEFAULT_INPUT) -> pd.DataFrame:
    weights, bias, feature_names, stats = load_artifacts()
    raw = pd.read_csv(input_path)
    X_df, _, _, _ = prepare_features(raw, stats)
    X = align_features(X_df, feature_names)
    probs = sigmoid(X @ weights + bias)
    out = raw.copy()
    out["prob_survived"] = probs
    out["pred_survived"] = (probs >= 0.5).astype(int)
    return out


def main():
    scored = score()
    print(scored[["prob_survived", "pred_survived"]])


if __name__ == "__main__":
    main()
