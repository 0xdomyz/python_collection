from math import floor, log10

import numpy as np
import pandas as pd

# data
######################
# create a dataframe of 10 rows and 3 columns with random numbers
df = pd.DataFrame(np.random.randn(10, 3), columns=list("ABC"))

# rounding
######################
round_to_n = lambda x, n: round(x, -int(floor(log10(x))) + (n - 1))
np.round(3.141592653589793, 2)

# np log functions
######################
np.log(2.718281828459045)
np.log10(1000)
np.log2(1024)
np.log1p(1.718281828459045)
np.log1p(df)
