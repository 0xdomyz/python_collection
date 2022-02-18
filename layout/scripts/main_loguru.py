"""Analyse random data and make summary"""

import pandas as pd
import numpy as np
import random
from loguru import logger
from pathlib import Path

def main(seed,n):
    logger.info(__doc__)
    logger.info(f"{seed = }")
    logger.info(f"{n = }")
    random.seed(seed)
    df = pd.DataFrame(
        dict(
            cat = [random.choice(['a','b','c']) for i in range(n)],
            score = [random.random() for i in range(n)]
        )
    )
    res = df.groupby('cat').agg(score=('score',np.mean)).reset_index()
    logger.info(f"\n{res.to_string()}")
    path = "res.csv"
    logger.info(f"save to {path}")
    res.to_csv(path)

if __name__ == "__main__":
    logger.add('log.log')
    main(0, 100)

"""Analyse random data and make summary"""

import pandas as pd
import numpy as np
import random
from loguru import logger
from pathlib import Path

_module_path = Path(__file__).parent
_file_name = Path(__file__).stem
_result_path = _module_path / f"{_file_name}_result.csv"
_log_path = _module_path / f"{_file_name}_log.log"
logger.add(_log_path)

logger.info(__doc__)

seed = 0
n = 100
logger.info(f"{seed = }")
logger.info(f"{n = }")

random.seed(seed)
df = pd.DataFrame(
    dict(
        cat = [random.choice(['a','b','c']) for i in range(n)],
        score = [random.random() for i in range(n)]
    )
)
res = df.groupby('cat').agg(score=('score',np.mean)).reset_index()

res.to_csv(_result_path)
logger.info(f"save to {_result_path}")
