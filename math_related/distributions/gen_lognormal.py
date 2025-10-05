import math
import random

import matplotlib.pyplot as plt
import pandas as pd


def lognormal(result_mean, result_sd):
    # formula from https://en.wikipedia.org/wiki/Log-normal_distribution
    mean = math.log(result_mean**2 / math.sqrt(result_sd**2 + result_mean**2))
    sd = math.sqrt(math.log(1 + result_sd**2 / result_mean**2))
    return random.lognormvariate(mean, sd)


# 3 columns of it
mean = 10e6
sd = 1e6
res = pd.DataFrame(
    {
        "a": [lognormal(mean, sd) for _ in range(1000)],
        "b": [lognormal(mean, sd) for _ in range(1000)],
        "c": [lognormal(mean, sd) for _ in range(1000)],
    }
)
# save to csv
res.to_csv("res.csv")

# constraint col c has to be less than col b
res = res[res["c"] < res["b"]]
len(res)

#########
# checks
#########

# restirct to 5 and 95th percentile
res_plt = res["a"]
res_plt = res_plt[
    (res_plt > res_plt.quantile(0.05)) & (res_plt < res_plt.quantile(0.95))
]
# log scale
res_plt = res_plt.apply(math.log10)
res_plt.hist(bins=100)
plt.show()
# summary of res
print(res.describe())
