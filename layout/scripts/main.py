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
    cd /d python_collection\layout
    python analysis\main.py 0 100
"""

import sys
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import random

_logger = logging.getLogger(__name__)
_module_path = Path(__file__).parent
_output_path = _module_path / 'output/out.csv'
_log_path = _module_path / 'log.log'

def main(seed,n):
    random.seed(seed)
    df = pd.DataFrame(
        dict(
            cat = [random.choice(['a','b','c']) for i in range(n)],
            score = [random.random() for i in range(n)]
        )
    )
    df.groupby('cat').agg(score=('score',np.mean)).reset_index().to_csv(_output_path)
    _logger.info("analysis done.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) - 1 != 2:
        print(__doc__)
        sys.exit(1)
    else:
        logging.basicConfig(
            level = logging.INFO,
            format = "%(asctime)s [%(levelname)s] %(message)s",
            handlers = [logging.StreamHandler(), logging.FileHandler(_log_path,'w+')]
        )
        _, seed, n = args
        main(int(seed), int(n))