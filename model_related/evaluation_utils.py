"""
Model evaluation metrics and comparison utilities.

Common patterns for scoring, cross-validation, and model comparison.
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score


def classification_metrics(y_true, y_pred, y_pred_proba=None) -> Dict[str, float]:
    """
    Calculate comprehensive classification metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_pred_proba: Predicted probabilities (optional, for ROC-AUC)

    Returns:
        Dictionary with metrics

    Example:
        >>> metrics = classification_metrics(y_test, y_pred, y_pred_proba)
        >>> print(metrics)
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(
            y_true, y_pred, average="weighted", zero_division=0
        ),
        "recall": recall_score(y_true, y_pred, average="weighted", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }

    if y_pred_proba is not None:
        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_pred_proba, multi_class="ovr")
        except Exception:
            pass

    return metrics


def regression_metrics(y_true, y_pred) -> Dict[str, float]:
    """
    Calculate comprehensive regression metrics.

    Args:
        y_true: True values
        y_pred: Predicted values

    Returns:
        Dictionary with metrics

    Example:
        >>> metrics = regression_metrics(y_test, y_pred)
    """
    return {
        "mse": mean_squared_error(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "mape": np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
    }


def cv_score(
    estimator, X, y, cv: int = 5, scoring: str = "accuracy"
) -> Dict[str, float]:
    """
    Cross-validation scoring with statistics.

    Args:
        estimator: Sklearn estimator
        X: Features
        y: Target
        cv: Number of folds
        scoring: Scoring metric ('accuracy', 'f1', 'r2', etc.)

    Returns:
        Dictionary with mean, std, and individual fold scores

    Example:
        >>> scores = cv_score(clf, X, y, cv=5)
    """
    scores = cross_val_score(estimator, X, y, cv=cv, scoring=scoring)

    return {
        "mean": scores.mean(),
        "std": scores.std(),
        "folds": scores.tolist(),
    }


def compare_models(
    models: Dict[str, Any],
    X_train,
    y_train,
    X_test,
    y_test,
    task: str = "classification",
) -> pd.DataFrame:
    """
    Compare multiple models on same dataset.

    Args:
        models: Dictionary of {name: estimator}
        X_train, y_train: Training data
        X_test, y_test: Test data
        task: 'classification' or 'regression'

    Returns:
        DataFrame with model comparisons

    Example:
        >>> models = {'RF': RandomForestClassifier(), 'GB': GradientBoostingClassifier()}
        >>> comparison = compare_models(models, X_train, y_train, X_test, y_test)
    """
    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if task == "classification":
            metrics = classification_metrics(y_test, y_pred)
        else:
            metrics = regression_metrics(y_test, y_pred)

        metrics["model"] = name
        results.append(metrics)

    return pd.DataFrame(results).set_index("model")


def feature_importance_summary(
    model, feature_names: list, top_n: int = 10
) -> pd.DataFrame:
    """
    Extract and rank feature importances.

    Args:
        model: Fitted sklearn model with feature_importances_
        feature_names: List of feature names
        top_n: Return top N features

    Returns:
        DataFrame with feature importances sorted

    Example:
        >>> importance = feature_importance_summary(rf_model, X.columns)
    """
    if not hasattr(model, "feature_importances_"):
        raise ValueError("Model must have feature_importances_ attribute")

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    return importance_df.head(top_n)
