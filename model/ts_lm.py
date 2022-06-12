import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score


df = pd.read_csv("ts_input.csv")
X = df.loc[:,lambda x:~x["date","y"]]
y = df["y"]

lr = LinearRegression()
ss = StandardScaler()
Xt = ss.fit(X).transform(X)

lr.fit(Xt, y)

accuracy_score(lr.predict(Xt), y)
lr.coef_
