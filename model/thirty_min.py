#data
import seaborn as sns
df = sns.load_dataset("titanic")
df.head()

#get rid of useless columns
spec = r"""
target:
    - survived

num_vars:
    - fare
    - age
    - sibsp
    - parch

cat_vars:
    - who
    - sex
    - adult_male
    - class
    - embark_town
    - deck
    - alone

junk:
    - alive
    - pclass
    - embarked
"""

from yaml import safe_load
loaded_spec = safe_load(spec)
target = loaded_spec["target"][0]
num_vars = loaded_spec["num_vars"]
cat_vars = loaded_spec["cat_vars"]

df_useful = df.loc[:,num_vars + cat_vars + [target]]

#categorical variables - dummy
import pandas as pd

pd.get_dummies(df_useful["who"])

#categorical variables - target
import category_encoders as ce

encoder = ce.TargetEncoder(cols=["sex"])
encoder.fit(df_useful["sex"], df_useful[target])
encoder.transform(df_useful["sex"])

import numpy as np
df_useful.groupby("sex").agg(avg_survive = ("survived",np.mean))

#categorical variables - leave one out
encoder = ce.LeaveOneOutEncoder(cols=["class"], random_state=0)
encoder.fit(df_useful["class"], df_useful[target])
encoder.transform(df_useful["class"])

#categorical variables - woe
encoder = ce.WOEEncoder(cols=["embark_town"], random_state=0)
encoder.fit(df_useful["embark_town"], df_useful[target])
encoder.transform(df_useful["embark_town"])

encoder = ce.WOEEncoder(cols=["deck"], random_state=0)
encoder.fit(df_useful["deck"], df_useful[target])
encoder.transform(df_useful["deck"])

#categorical variables
df_cat_clean = df_useful.copy()
for var in cat_vars:
    encoder = ce.WOEEncoder(cols=[var], random_state=0)
    encoder.fit(df_useful[var], df_useful[target])
    df_cat_clean[var] = encoder.transform(df_useful[var])
    

encoder = ce.WOEEncoder(cols=[], random_state=0)
encoder.fit(df_useful[var], df_useful[target])
df_cat_clean[var] = encoder.transform(df_useful[var])
df_cat_clean.head()

#standardise
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(X)
ss.mean
np.sqrt(ss.var_)
Xt = ss.transform(X)

#statsmodels
import statsmodels.api as sm

sm.add_constant()
est = sm.GLM().fit()
print(est.summary())

est.get_prediction().summary_frame(alpha=0.05)



#sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import roc_curve, auc, r2_score

lr = LogisticRegression()

lr.fit(X,y)

lr.coef_
lr.intercept_

wts = np.round(np.abs(lr.intercept_)/sum(lr.intercept_)*100,2)

p = lr.predict()

r2_score(y, p)

n=len(p)
k = len(lr.coef_)
adj_r2 = 1 - (1-r2) * float(n-1) / float(n-k-1)

