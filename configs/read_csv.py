from pathlib import Path

import pandas as pd

path = Path(__file__).parent / "data.csv"


def read_csv(path):
    return pd.read_csv(path)


if __name__ == "__main__":
    _ = pd.DataFrame(dict(a=range(5), b=[i for i in "aeiou"]))
    _.to_csv(path, index=False)
    d = read_csv(path)
    print(d)
