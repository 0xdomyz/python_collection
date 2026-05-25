"""Logistic regression using scikit-learn on the Titanic dataset."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from titanic_prep import load_titanic, prepare_features

ARTIFACT_DIR = Path(__file__).parent
MODEL_PATH = ARTIFACT_DIR / "logistic_sklearn_model.joblib"


def train_sklearn(random_state: int = 42):
    raw = load_titanic()
    X_df, y_ser, stats, feature_names = prepare_features(raw)
    X_train, X_test, y_train, y_test = train_test_split(
        X_df, y_ser, test_size=0.2, random_state=random_state, stratify=y_ser
    )

    clf = LogisticRegression(max_iter=1000, solver="lbfgs")
    clf.fit(X_train, y_train)

    prob_train = clf.predict_proba(X_train)[:, 1]
    prob_test = clf.predict_proba(X_test)[:, 1]

    metrics = {
        "train": {
            "accuracy": accuracy_score(y_train, clf.predict(X_train)),
            "logloss": log_loss(y_train, prob_train),
            "auc": roc_auc_score(y_train, prob_train),
        },
        "test": {
            "accuracy": accuracy_score(y_test, clf.predict(X_test)),
            "logloss": log_loss(y_test, prob_test),
            "auc": roc_auc_score(y_test, prob_test),
        },
    }

    coef_df = pd.DataFrame(
        {
            "feature": feature_names,
            "coef": clf.coef_.ravel(),
        }
    ).sort_values(by="coef", key=abs, ascending=False)

    joblib.dump(
        {"model": clf, "stats": stats.to_dict(), "features": feature_names}, MODEL_PATH
    )
    print("Saved sklearn model to", MODEL_PATH)
    print("Top coefficients:\n", coef_df.head(10).to_string(index=False))
    print("Metrics:", metrics)
    return clf, metrics, coef_df


if __name__ == "__main__":
    train_sklearn()
