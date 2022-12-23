import matplotlib.pyplot as plt
import numpy as np


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
