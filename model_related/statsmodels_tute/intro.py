import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# using pandas
########################

# Load data
dat = sm.datasets.get_rdataset("Guerry", "HistData").data

# Fit regression model (using the natural log of one of the regressors)
results = smf.ols("Lottery ~ Literacy + np.log(Pop1831)", data=dat).fit()

# Inspect the results
print(results.summary())

# residuals
resid = results.resid

# standard deviation of residuals
resid.std()

# diagnostic plots of residuals
import matplotlib.pyplot as plt
import scipy.stats as stats

fig = sm.graphics.qqplot(resid, dist=stats.norm, line="45", fit=True)
plt.show()

# fitted values (need a constant term for intercept)
fitted = results.fittedvalues

# using numpy arrays
########################

# Generate artificial data (2 regressors + constant)
nobs = 100

X = np.random.random((nobs, 2))

X = sm.add_constant(X)

beta = [1, 0.1, 0.5]

e = np.random.random(nobs)

y = np.dot(X, beta) + e

# Fit regression model
results = sm.OLS(y, X).fit()

# Inspect the results
print(results.summary())
