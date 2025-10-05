"""statsmodels RollingOLS example"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import adfuller

np.random.seed(12345)
nobs = 1000
X = np.random.randn(nobs)
X = pd.Series(X, index=pd.date_range("1/1/2000", periods=nobs))
X = X.cumsum()
X.plot(figsize=(12, 8))
plt.show()
# 2. Create a time series with a unit root
# ----------------------------------------
# A unit root is a feature of time series data where a value from the
# previous time step is used to predict the current value. A unit root
# makes the time series non-stationary.  Non-stationary time series are
# difficult to model, and in some cases, impossible to model.  For
# example, the following time series has a unit root.
beta = 0.9
err = np.random.randn(nobs)
Y = beta * X + err
Y.plot(figsize=(12, 8))
plt.show()
# 3. Augmented Dickey-Fuller test
# ------------------------------
# A common test for checking if a time series is stationary is the
# Augmented Dickey-Fuller test.  The null hypothesis of the test is
# that there is a unit root, so a p-value below a threshold (such as
# 5%) indicates that we can reject the null hypothesis and that the
# time series does not have a unit root, and in turn that it is
# stationary.
adf_result = adfuller(Y)
print("Augmented Dickey-Fuller test statistic: {0:.1f}".format(adf_result[0]))
print("p-value: {0:.1f}".format(adf_result[1]))
print("Critical values:")
for key, value in adf_result[4].items():
    print("\t{0}: {1:.1f}".format(key, value))
# 4. Estimate a rolling regression
# -------------------------------
# We can use statsmodels to estimate a rolling regression.  The
# ``RollingOLS`` class can be used to estimate a regression for each
# rolling window of the independent variable.  In the following
# example, we use a window size of 250 days.  Note that the window
# size must be specified in the number of observations, and not in
# units of time.
window = 250

endog = Y
exog = sm.add_constant(X)
rolling_results = RollingOLS(endog, exog, window=window).fit()


# 5. Plot the estimated coefficients
# ---------------------------------
# We can plot the estimated coefficients from the rolling regression.
# We see that the estimated intercept and slope both increase over
# time.
rolling_results.params["const"].plot(figsize=(12, 8), title="Intercept")
plt.show()
rolling_results.params[0].plot(figsize=(12, 8), title="Slope")
plt.show()
# 6. Plot the estimated standard errors
# ------------------------------------
# We can also plot the estimated standard errors.
rolling_results.bse["const"].plot(figsize=(12, 8), title="Intercept SE")
plt.show()
rolling_results.bse[0].plot(figsize=(12, 8), title="Slope SE")
plt.show()
