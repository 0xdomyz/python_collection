import hashlib

import pandas as pd
from sklearn.datasets import load_iris

x = load_iris(as_frame=True)["data"]

h=hashlib.sha1(pd.util.hash_pandas_object(x).values).hexdigest()
print(h)

import pandas as pd
import hashlib

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z'],
    'C': [True, False, True],
    'D': [9.1, 8.2, 7.3]
})

# Choose columns to hash
cols_to_hash = ['A', 'B', 'C']

# Combine values into a single string per row
combined = df[cols_to_hash].astype(str).agg('-'.join, axis=1)

# Apply a hash function (e.g., SHA256)
df['row_hash'] = combined.apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
