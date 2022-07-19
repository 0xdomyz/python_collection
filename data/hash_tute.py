import hashlib
import pandas as pd
from sklearn.datasets import load_iris

x = load_iris(as_frame=True)["data"]

if __name__ == "__main__":
    h = hashlib.sha1(pd.util.hash_pandas_object(x).values).hexdigest()
    print(h)

