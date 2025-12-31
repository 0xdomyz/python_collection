"""Weight of Evidence using `category_encoders.WOEEncoder` if available.

Install: `pip install category_encoders`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

try:
    from category_encoders.woe import WOEEncoder
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "category_encoders not installed. Install with `pip install category_encoders`"
    ) from exc

from titanic_prep import load_titanic, prepare_features

ARTIFACT_DIR = Path(__file__).parent
ENCODER_PATH = ARTIFACT_DIR / "woe_encoder.joblib"

try:
    import joblib
except ImportError as exc:  # pragma: no cover
    raise SystemExit("joblib is required: pip install joblib") from exc


def train_encoder() -> Tuple[WOEEncoder, pd.DataFrame, pd.Series]:
    raw = load_titanic()
    X_df, y_ser, stats, feature_names = prepare_features(raw)

    cat_cols = [c for c in X_df.columns if X_df[c].dtype == "uint8"]
    num_cols = [c for c in X_df.columns if c not in cat_cols]

    enc = WOEEncoder(cols=cat_cols, randomized=False, regularization=0.0)
    X_enc = enc.fit_transform(X_df, y_ser)

    joblib.dump(
        {"encoder": enc, "stats": stats.to_dict(), "feature_names": feature_names},
        ENCODER_PATH,
    )
    print("Saved WOE encoder to", ENCODER_PATH)
    return enc, X_enc, y_ser


def main():
    enc, X_enc, y = train_encoder()
    print(X_enc.head())


if __name__ == "__main__":
    main()
