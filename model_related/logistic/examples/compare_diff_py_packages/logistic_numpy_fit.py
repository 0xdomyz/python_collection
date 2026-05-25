"""Logistic regression from first principles using NumPy.

- Preprocesses Titanic data (see titanic_prep.py).
- Fits logistic regression with gradient descent and optional L2 regularization.
- Evaluates on a holdout split and saves artifacts for scoring.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from titanic_prep import (
    PreprocessStats,
    load_titanic,
    prepare_features,
    train_test_split,
)

ARTIFACT_DIR = Path(__file__).parent
MODEL_PATH = ARTIFACT_DIR / "logistic_numpy_model.npz"
STATS_PATH = ARTIFACT_DIR / "logistic_numpy_stats.json"


@dataclass
class NumpyModel:
    weights: np.ndarray
    bias: float
    feature_names: List[str]
    stats: PreprocessStats


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-z))


def predict_proba(weights: np.ndarray, bias: float, X: np.ndarray) -> np.ndarray:
    return sigmoid(X @ weights + bias)


def loss_and_grad(
    weights: np.ndarray,
    bias: float,
    X: np.ndarray,
    y: np.ndarray,
    l2: float,
) -> Tuple[float, np.ndarray, float]:
    m = len(y)
    preds = predict_proba(weights, bias, X)
    eps = 1e-9
    loss = -np.mean(y * np.log(preds + eps) + (1 - y) * np.log(1 - preds + eps))
    loss += 0.5 * l2 * np.sum(weights**2)

    error = preds - y
    grad_w = (X.T @ error) / m + l2 * weights
    grad_b = np.mean(error)
    return loss, grad_w, grad_b


def fit_model(
    X: np.ndarray,
    y: np.ndarray,
    lr: float = 0.1,
    l2: float = 0.01,
    max_iter: int = 5000,
    tol: float = 1e-6,
) -> Tuple[np.ndarray, float, List[float]]:
    rng = np.random.default_rng(42)
    weights = rng.normal(scale=0.01, size=X.shape[1])
    bias = 0.0
    losses: List[float] = []

    for i in range(max_iter):
        curr_loss, grad_w, grad_b = loss_and_grad(weights, bias, X, y, l2)
        weights -= lr * grad_w
        bias -= lr * grad_b
        losses.append(curr_loss)
        if i > 5 and abs(losses[-2] - losses[-1]) < tol:
            break
    return weights, bias, losses


def evaluate(
    weights: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray
) -> Dict[str, float]:
    probs = predict_proba(weights, bias, X)
    preds = (probs >= 0.5).astype(int)
    eps = 1e-9
    logloss = -np.mean(y * np.log(probs + eps) + (1 - y) * np.log(1 - probs + eps))
    acc = float((preds == y).mean())

    # Simple AUC approximation via ranking (no sklearn dependency)
    order = np.argsort(probs)
    y_sorted = y[order]
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        auc = float("nan")
    else:
        rank_sum = np.cumsum(y_sorted)[y_sorted == 1].sum()
        auc = float((rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))

    return {"logloss": float(logloss), "accuracy": acc, "auc": auc}


def save_artifacts(model: NumpyModel) -> None:
    np.savez(
        MODEL_PATH,
        weights=model.weights,
        bias=model.bias,
        feature_names=np.array(model.feature_names, dtype=object),
    )
    STATS_PATH.write_text(json.dumps(model.stats.to_dict(), indent=2), encoding="utf-8")
    print(f"Saved weights to {MODEL_PATH} and stats to {STATS_PATH}")


def run_training() -> Dict[str, Dict[str, float]]:
    raw = load_titanic()
    X_df, y_ser, stats, feature_names = prepare_features(raw)
    X_train, X_test, y_train, y_test = train_test_split(X_df, y_ser)

    weights, bias, losses = fit_model(X_train, y_train, lr=0.3, l2=0.02, max_iter=8000)

    train_metrics = evaluate(weights, bias, X_train, y_train)
    test_metrics = evaluate(weights, bias, X_test, y_test)

    model = NumpyModel(
        weights=weights, bias=bias, feature_names=feature_names, stats=stats
    )
    save_artifacts(model)

    print(
        "Train metrics:",
        train_metrics,
        "\nTest metrics:",
        test_metrics,
        f"\nConverged in {len(losses)} iters",
    )
    return {"train": train_metrics, "test": test_metrics}


if __name__ == "__main__":
    run_training()
