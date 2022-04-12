import pandas as pd
from pathlib import Path

path = Path(__file__).parent / 'data.csv'

def csv_reader(path):
    return pd.read_csv(path)

if __name__ == '__main__':
    _ = pd.DataFrame(dict(a=range(5),b=[i for i in "aeiou"]))
    _.to_csv(path, index=False)
    d = csv_reader(path)
    print(d)