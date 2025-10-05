# example of using pymc3
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm

# generate data
x = np.linspace(0, 1, 100)
y = 2 * x + np.random.normal(size=100)

# plot data
plt.plot(x, y, "o")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# build model
with pm.Model() as model:
    # define priors
    alpha = pm.Normal("alpha", mu=0, sd=10)
    beta = pm.Normal("beta", mu=0, sd=10)
    sigma = pm.HalfNormal("sigma", sd=1)

    # define likelihood
    mu = alpha + beta * x
    likelihood = pm.Normal("y", mu=mu, sd=sigma, observed=y)

    # inference
    trace = pm.sample(1000, tune=1000)

# plot results
pm.traceplot(trace)
plt.show()

# plot regression line
plt.plot(x, y, "o", label="data")
plt.plot(x, trace["alpha"].mean() + trace["beta"].mean() * x, label="regression line")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc=0)
plt.show()

# plot regression line with uncertainty
plt.plot(x, y, "o", label="data")
for i in range(100):
    plt.plot(x, trace["alpha"][i] + trace["beta"][i] * x, c="gray", alpha=0.1)
plt.plot(x, trace["alpha"].mean() + trace["beta"].mean() * x, label="regression line")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc=0)
plt.show()
