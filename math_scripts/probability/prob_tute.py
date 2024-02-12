import matplotlib.pyplot as plt
import numpy as np

# probability of having at least 1 success in 5 trials, if success rate is x chart
###########################################################


# probability of having at least 1 success in 5 trials, if success rate is x
def prob(x, n=5):
    return 1 - (1 - x) ** n


prob(0.05, 5)

# plot it for different values of x
x = np.linspace(0, 1, 100)
y = [prob(i) for i in x]
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("probability")
plt.title("Probability of having at least 1 success in 5 trials")
plt.show()

# probability of having at least 1 success in n trials, if probability of success is x
prob_of_success = 0.09
x = np.linspace(0, 100, 100)
y = [prob(prob_of_success, i) for i in x]
plt.plot(x, y)
# add finer axis ticks,
plt.xticks(np.arange(0, 100, 5))
plt.yticks(np.arange(0, 1.1, 0.1))
# yticks as percentages
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:.0%}".format(x))
)
plt.xlabel("n")
plt.ylabel("probability")
plt.title(f"Probability of success for each trail is {prob_of_success}")
plt.suptitle("Probability of having at least 1 success in n trials")
# add finer grid lines
plt.grid(b=True, which="major", color="k", linestyle="-", alpha=0.2)
plt.grid(b=True, which="minor", color="k", linestyle="-", alpha=0.1)
plt.show()

# how much code did i write in this script? versus how much copilot write?
# i wrote 2 lines of code, copilot wrote 20 lines of code

# probability of getting a value less than 0.5 on matrix
###########################################################

# example matrix
mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * 0.1
mat

# normal distribution probability
from scipy.stats import norm

# probability of getting a value less than 0.5
norm.cdf(0.5)

# probability of getting a value less than 0.5, with mean 0.2 and standard deviation 0.1
norm.cdf(0.5, loc=0.2, scale=0.1)

# prob cdf applied to matrix
res = norm.cdf(mat)
res

# get last column
res.T[-1]
last_col_as_array = res[:, -1]
last_col_as_array

# get all cols except last
res.T[:-1]
non_last_cols = res[:, :-1]
non_last_cols


# stitch back
stitched = np.hstack((non_last_cols, last_col_as_array.reshape(-1, 1)))
stitched

np.allclose(stitched, res)
