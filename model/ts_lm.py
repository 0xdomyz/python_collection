import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


df = pd.read_csv("us_change.csv")
target = "Consumption"

X = (
    df
    .assign(
        inc_wa4 = lambda x:x["Income"].rolling(4).sum(),
        inc_d = lambda x:x["Income"].diff(),
        inc_lag_2 = lambda x:x["Income"].shift(2),
        inc_lead_2 = lambda x:x["Income"].shift(-2),
    )
    .dropna()
)
X, y = X.drop(columns=["Quarter",target]), X[target]

lr = LinearRegression()
ss = StandardScaler()

Xt = ss.fit(X).transform(X)
lr.fit(Xt, y)

print(f"{lr.intercept_ = }")
print(f"{lr.coef_ = }")
_ = np.abs(lr.coef_)
wts = np.round(_/_.sum()*100,2)
weights = pd.DataFrame({"var":X.columns, "weights":wts}).sort_values("weights",ascending=False)
print(weights.to_string())

p = lr.predict(Xt)
adj_r2 = 1 - float(len(p)-1)/(len(y)-len(lr.coef_)-1)*(1 - r2_score(p, y))
print(f"{adj_r2 = }")


