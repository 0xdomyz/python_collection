import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import category_encoders as ce
import sklearn.preprocessing as prep
#from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import sklearn.linear_model as sklm
import sklearn.metrics as metrics


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


#pre-pre-processing
X:pd.DataFrame = df.drop(junk+[target], axis=1).loc[:,num_vars + cat_vars]
y:pd.Series = df[target]

X.head()
X.dtypes
y


#encode categorical variables
cols = X.select_dtypes([object,"category",bool]).columns
encoder = ce.WOEEncoder(cols=cols)
encoder.fit(X[cols], y)
X[cols] = encoder.transform(X[cols])

X

#   dummy
pd.get_dummies(X["who"])

drop_enc = prep.OneHotEncoder(drop='first').fit(X[cols])
drop_enc.transform(X[cols]).toarray()

#   other encoders
def encode(encoder_class, X, cols, y):
    encoder = encoder_class(cols=cols)
    encoder.fit(X[cols], y)
    return encoder.transform(X[cols])

cols = ["who"]
encode(ce.TargetEncoder, X, cols, y)
df.groupby(cols).agg(avg_survive = ("survived",np.mean))

encode(ce.LeaveOneOutEncoder, X, cols, y)
encode(ce.GLMMEncoder, X, cols, y)#doco says this is log odds if target is binary


#standardise
cols = X.columns
scaler = prep.StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
X_df = pd.DataFrame(X, columns=cols)

X
X.shape
scaler.mean_
np.sqrt(scaler.var_)


#remove na
X_df = sm.add_constant(X_df)
X_df = X_df.dropna()
X = X_df.values
y = y.loc[X_df.index]

#statsmodels
estimator = sm.GLM(endog = y, exog = X_df, family = sm.families.Binomial())
res = estimator.fit()

res.summary()
res.get_prediction().summary_frame(alpha=0.05)


#sklearn
sklm.LogisticRegression, sklm.LogisticRegressionCV
metrics.roc_curve, metrics.auc, metrics.r2_score

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

