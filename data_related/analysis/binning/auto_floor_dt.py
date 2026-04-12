import pandas as pd


def auto_floor_for_target_nunique(
    dt_series: pd.Series,
    target_nunique: int = 50,
    start_scale: float = 4.0,
) -> tuple[pd.Series, str, int]:
    """Pick the finest dt.floor frequency that keeps unique bins <= target_nunique.

    The search starts from a larger interval derived from the observed min/max span,
    then moves to smaller intervals.
    """
    if target_nunique < 1:
        raise ValueError("target_nunique must be >= 1")

    valid = dt_series.dropna()
    if valid.empty:
        raise ValueError("dt_series has no non-null datetime values")

    tmin = valid.min()
    tmax = valid.max()
    span_seconds = max(int((tmax - tmin).total_seconds()), 1)

    freq_seconds_desc = [
        ("365D", 365 * 24 * 3600),
        ("180D", 180 * 24 * 3600),
        ("90D", 90 * 24 * 3600),
        ("60D", 60 * 24 * 3600),
        ("30D", 30 * 24 * 3600),
        ("14D", 14 * 24 * 3600),
        ("7D", 7 * 24 * 3600),
        ("3D", 3 * 24 * 3600),
        ("2D", 2 * 24 * 3600),
        ("1D", 24 * 3600),
        ("12h", 12 * 3600),
        ("8h", 8 * 3600),
        ("6h", 6 * 3600),
        ("4h", 4 * 3600),
        ("3h", 3 * 3600),
        ("2h", 2 * 3600),
        ("1h", 3600),
        ("30min", 30 * 60),
        ("15min", 15 * 60),
        ("10min", 10 * 60),
        ("5min", 5 * 60),
        ("2min", 2 * 60),
        ("1min", 60),
    ]

    # Span-based starting point, then search from larger to smaller intervals.
    ideal_seconds = max(span_seconds / target_nunique, 1)
    start_seconds = ideal_seconds * start_scale

    start_idx = 0
    for i, (_, secs) in enumerate(freq_seconds_desc):
        if secs <= start_seconds:
            start_idx = max(i - 1, 0)
            break
    else:
        start_idx = len(freq_seconds_desc) - 1

    selected_freq, selected_nunique = freq_seconds_desc[start_idx][0], valid.nunique()
    had_valid_choice = False

    for freq, _ in freq_seconds_desc[start_idx:]:
        n_bins = int(valid.dt.floor(freq).nunique())
        if n_bins <= target_nunique:
            selected_freq, selected_nunique = freq, n_bins
            had_valid_choice = True
        else:
            break

    if not had_valid_choice:
        # Fallback to coarser intervals if start point was still too fine.
        for freq, _ in reversed(freq_seconds_desc[: start_idx + 1]):
            n_bins = int(valid.dt.floor(freq).nunique())
            selected_freq, selected_nunique = freq, n_bins
            if n_bins <= target_nunique:
                break

    return dt_series.dt.floor(selected_freq), selected_freq, selected_nunique
