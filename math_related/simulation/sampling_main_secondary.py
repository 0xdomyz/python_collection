import pandas as pd
import numpy as np

from loguru import logger
from enum import IntFlag


def decode_flags(bitfield: int, flags: IntFlag) -> list[str]:
    return [name for name, value in flags.__members__.items() if bitfield & value]


def sample_df_via_main_and_secondary_flags(
    df: pd.DataFrame,
    flags_col: str,
    flags_main: list[IntFlag],
    req_n_main: list[int],
    flags_secondary: list[IntFlag],
    req_n_secondary: list[int],
) -> pd.Series:

    sample_res = pd.Series(False, index=df.index)

    for f, n in zip(flags_main, req_n_main):
        mask = df[flags_col] & int(f) > 0
        candidates = df.loc[mask & ~sample_res]
        chosen = np.random.choice(candidates.index, size=n, replace=False)
        logger.debug(f"Chosen {n} samples for flag {f.name}")
        sample_res.loc[chosen] = True

    for f, n in zip(flags_secondary, req_n_secondary):
        mask = df[flags_col] & int(f) > 0
        already_chosen = df.loc[sample_res & mask]
        if already_chosen.shape[0] >= n:
            logger.debug(
                f"Already have {already_chosen.shape[0]} samples for flag {f.name}, need {n}, skip"
            )
            continue
        else:
            n_needed = n - already_chosen.shape[0]
            candidates = df.loc[mask & ~sample_res]
            chosen = np.random.choice(candidates.index, size=n_needed, replace=False)
            logger.debug(f"Chosen {n_needed} samples for flag {f.name}")
            sample_res.loc[chosen] = True

    return sample_res


def make_sampling_summary_df(
    df: pd.DataFrame,
    flags_col: str,
    sample_col: str,
    flags_main: list[IntFlag],
    flags_secondary: list[IntFlag],
):
    summary = []

    for f in flags_main + flags_secondary:
        mask = df[flags_col] & int(f) > 0
        total = df.loc[mask].shape[0]
        chosen = df.loc[mask & df[sample_col]].shape[0]
        summary.append(
            {
                "Flag": f.name,
                "Chosen": chosen,
                "Total": total,
                "Percentage": f"{chosen/total:.1%}",
                "Type": "Main" if f in flags_main else "Secondary",
                "Ratio": f"{chosen}/{total}",
            }
        )

    return pd.DataFrame(summary).set_index("Flag")
