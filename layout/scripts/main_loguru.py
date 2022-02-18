"""
Analysis random data and make summary.

Generate random data, make basic summary,
output into csv.

Arguments
---------
seed : int
    Seed for random generation.
n : int
    Number of rows in data.

Effect
------
Write result csv into the output folder.

Examples
--------
:
    cd /d python_collection\layout\scripts
    python main.py 0 100
"""
import pandas as pd
import numpy as np
import random
from loguru import logger
from pathlib import Path
import sys

_module_path, _file_name = Path(__file__).parent, Path(__file__).stem

def main(seed,n):
    random.seed(seed)
    df = pd.DataFrame(
        dict(
            cat = [random.choice(['a','b','c']) for i in range(n)],
            score = [random.random() for i in range(n)]
        )
    )
    res = df.groupby('cat').agg(score=('score',np.mean)).reset_index()

    _result_path = _module_path / 'output' / f"{_file_name}_result.csv"
    res.to_csv(_result_path)
    logger.info(f"Results saved to {_result_path}")

if __name__ == "__main__":
    args = sys.argv
    if len(args) - 1 != 2:
        print(__doc__)
        sys.exit(1)
    else:
        logger.add(_module_path / "output" / f"{_file_name}_log.log")
        logger.info(__doc__)
        _, seed, n = args
        main(int(seed), int(n))