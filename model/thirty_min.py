import pandas as pd
import numpy as np
import category_encoders as ce

#data & first look
import seaborn as sns
df = sns.load_dataset("titanic")
df.head()

target = "survived"

num_vars = [
    "fare",
    "age",
    "sibsp",
    "parch",
]

cat_vars =[
    "who",
    "sex",
    "adult_male",
    "class",
    "embark_town",
    "deck",
    "alone",
]

junk = [
     "alive",
     "pclass",
     "embarked",
]


X:pd.DataFrame = df.drop(junk+[target], axis=1).loc[:,num_vars + cat_vars]
y:pd.Series = df[target]

X.head()
X.dtypes
y

#encode categorical variables

#   dummy
pd.get_dummies(X["who"])

#   target
cols = ["who"]
encoder_class = ce.TargetEncoder
encoder = encoder_class(cols=cols,smoothing=1)
encoder.fit(X[cols], y)
encoder.transform(X[cols])

df.groupby(cols).agg(avg_survive = ("survived",np.mean))

def encode(encoder_class, X, cols):
    encoder = encoder_class(cols=cols)
    encoder.fit(X[cols], y)
    return encoder.transform(X[cols])

cols = ["who"]
encode(ce.TargetEncoder, X, cols)
encode(ce.LeaveOneOutEncoder, X, cols)
encode(ce.WOEEncoder, X, cols)

X_cat = X.select_dtypes([object,"category",bool])
X_cat_encoded = encode(ce.WOEEncoder, X_cat, list(X_cat.columns))
X[X_cat.columns] = X_cat_encoded


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

