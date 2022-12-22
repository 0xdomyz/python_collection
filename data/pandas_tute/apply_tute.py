# apply func to index
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(4, 3), columns=["col1", "col2", "col3"])
print(df)

# apply func to each column
print(df.apply(np.mean))

# apply func to each row
print(df.apply(np.mean, axis=1))

# apply func to each element
print(df.applymap(lambda x: len(str(x))))

# apply func to each element of Series
print(df["col1"].map(lambda x: len(str(x))))

# apply func to index
print(df.index.map(lambda x: x + 1))
