"""Quick plotting helpers for WoE per bin."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from woe_first_principles import WoEBinResult

PLOT_PATH = Path(__file__).parent / "woe_plot.png"


def plot_woe(bin_result: WoEBinResult, title: str = "WoE by bin") -> Path:
    labels = [str(b) for b in bin_result.bins]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, bin_result.woe)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("WoE")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=150)
    print("Saved", PLOT_PATH)
    return PLOT_PATH


if __name__ == "__main__":
    import numpy as np
    from woe_first_principles import compute_woe_iv, quantile_bins

    rng = np.random.default_rng(0)
    x = rng.normal(size=500)
    y = rng.binomial(1, 0.3, size=500)
    bins = quantile_bins(pd.Series(x), n_bins=5)
    res = compute_woe_iv(bins, pd.Series(y))
    plot_woe(res)
