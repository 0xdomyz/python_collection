"""Weight of Evidence (WoE) and Information Value (IV) from first principles.

- Provides simple quantile-based binning for numeric variables.
- Computes WoE/IV per bin and applies the transformation.
- Designed for credit-risk style binary targets (1 = event/bad).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


@dataclass
class WoEBinResult:
    bins: List[pd.Interval]
    woe: List[float]
    iv: float


def quantile_bins(series: pd.Series, n_bins: int = 10) -> pd.Series:
    """Discretize numeric series into quantile bins with duplicates handled."""
    quantiles = np.linspace(0, 1, n_bins + 1)
    edges = series.dropna().quantile(quantiles).to_numpy()
    edges[0], edges[-1] = -np.inf, np.inf
    # Ensure strictly increasing edges
    edges = np.unique(edges)
    if len(edges) < 3:  # pragma: no cover - unlikely but guard degenerate data
        edges = np.array([-np.inf, series.median(), np.inf])
    binned = pd.cut(series, bins=edges, include_lowest=True, duplicates="drop")
    return binned


def compute_woe_iv(
    binned: pd.Series, target: pd.Series, event: int = 1
) -> WoEBinResult:
    df = pd.DataFrame({"bin": binned, "target": target})
    grouped = df.groupby("bin")
    agg = grouped["target"].agg(
        [
            ("event", lambda x: (x == event).sum()),
            ("non_event", lambda x: (x != event).sum()),
        ]
    )
    agg["event_rate"] = agg["event"] / agg["event"].sum()
    agg["non_event_rate"] = agg["non_event"] / agg["non_event"].sum()

    eps = 1e-9
    agg["woe"] = np.log((agg["event_rate"] + eps) / (agg["non_event_rate"] + eps))
    agg["iv_component"] = (agg["event_rate"] - agg["non_event_rate"]) * agg["woe"]
    iv = float(agg["iv_component"].sum())
    return WoEBinResult(bins=agg.index.tolist(), woe=agg["woe"].tolist(), iv=iv)


def apply_woe(series: pd.Series, woe_bins: WoEBinResult) -> pd.Series:
    mapping = dict(zip(woe_bins.bins, woe_bins.woe))
    return series.map(mapping)


def demo():
    rng = np.random.default_rng(0)
    n = 1000
    age = rng.normal(40, 10, size=n)
    income = rng.lognormal(mean=10.5, sigma=0.5, size=n)
    prob_bad = 1 / (1 + np.exp(-(-8 + 0.05 * (50 - age) + 0.00005 * income)))
    y = rng.binomial(1, prob_bad)
    df = pd.DataFrame({"age": age, "income": income, "bad": y})

    age_bins = quantile_bins(df["age"], n_bins=5)
    age_res = compute_woe_iv(age_bins, df["bad"])
    print("Age IV:", age_res.iv)

    income_bins = quantile_bins(df["income"], n_bins=5)
    income_res = compute_woe_iv(income_bins, df["bad"])
    print("Income IV:", income_res.iv)

    df["age_woe"] = apply_woe(age_bins, age_res)
    df["income_woe"] = apply_woe(income_bins, income_res)
    print(df[["age_woe", "income_woe"]].head())


if __name__ == "__main__":
    demo()
