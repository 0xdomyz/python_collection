import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import category_encoders as ce
import sklearn.preprocessing as prep
#from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import sklearn.metrics as metrics


#data
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

duplicated_columns = [
     "alive",
     "pclass",
     "embarked",
]


#create X and y modelling frames
X:pd.DataFrame = df.drop(duplicated_columns+[target], axis=1).loc[:,num_vars+cat_vars]
y:pd.Series = df[target]

X.head()
X.dtypes
y


#encode categorical variables
cols = X.select_dtypes([object,"category",bool]).columns
encoder = ce.WOEEncoder(cols=cols)
encoder.fit(X[cols], y)
X[cols] = encoder.transform(X[cols])

X.head()
X.dtypes


#discretize numeric variables
est = prep.KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
est.fit(X[["fare"]])
X["fare_bin"] = est.transform(X[["fare"]])

_ = (
    prep.KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')
    .fit(X[["fare"]])
    .transform(X[["fare"]])
)
pd.DataFrame(_).value_counts()

X["fare_bin"].value_counts()


#dummy and other encoders
if False:

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
X_df.head()

scaler.mean_
np.sqrt(scaler.var_)


#remove na
X_df = sm.add_constant(X_df)
X_df = X_df.dropna()
X = X_df.values
y = y.loc[X_df.index]

X_df.head()
X_df.shape


#statsmodels
estimator = sm.GLM(endog = y, exog = X_df, family = sm.families.Binomial())
fitted_glm_model = estimator.fit()

fitted_glm_model.summary()
fitted_glm_model.params.abs()/sum(fitted_glm_model.params.abs())*100

fitted_glm_model.get_prediction().summary_frame(alpha=0.05)
predictions = fitted_glm_model.get_prediction().summary_frame()["mean"]


#evaluation

#    accuracy
import scipy
scipy.stats.somersd(y, predictions).statistic


#    calibration
predictions_calibrated = np.where(predictions>0.5, 1, 0)

_ = pd.concat([
    df.loc[X_df.index].assign(
        survived=predictions_calibrated,
        prediction_actual="prediction"
    ),
    df.loc[X_df.index].assign(
        survived=y,
        prediction_actual="actual"
    ),
])

import matplotlib.pyplot as plt
sns.catplot(data=_, x="survived", hue = "prediction_actual",kind="count")
sns.catplot(data=_, x="survived", hue = "prediction_actual",col="adult_male",kind="count")
sns.catplot(data=_, x="survived", hue = "prediction_actual",col="class",kind="count")
plt.show()

#sklearn


