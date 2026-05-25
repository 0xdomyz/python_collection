"""Plot ROC and Precision-Recall diagnostics for a sklearn logistic model."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from titanic_prep import load_titanic, prepare_features

PLOT_PATH = Path(__file__).parent / "logistic_diagnostics.png"


def plot_diagnostics():
    raw = load_titanic()
    X_df, y_ser, stats, feature_names = prepare_features(raw)
    X_train, X_test, y_train, y_test = train_test_split(
        X_df, y_ser, test_size=0.2, random_state=42, stratify=y_ser
    )

    clf = LogisticRegression(max_iter=1000, solver="lbfgs")
    clf.fit(X_train, y_train)
    prob = clf.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, prob)
    prec, rec, _ = precision_recall_curve(y_test, prob)
    auc = roc_auc_score(y_test, prob)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(fpr, tpr, label=f"AUC = {auc:.3f}")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray")
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].set_title("ROC Curve")
    axes[0].legend()

    axes[1].plot(rec, prec)
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_title("Precision-Recall Curve")

    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=150)
    print("Saved diagnostics plot to", PLOT_PATH)


if __name__ == "__main__":
    plot_diagnostics()
