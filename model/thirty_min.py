import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import category_encoders as ce
import sklearn.preprocessing as prep
import statsmodels.api as sm
import sklearn.metrics as metrics
import sklearn.ensemble as ens
from sklearn.compose import ColumnTransformer

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


#pre-pre-processing: dup columns, nas, train, test sets
X:pd.DataFrame = df.drop(duplicated_columns+[target], axis=1).loc[:,num_vars+cat_vars]
y:pd.Series = df[target]

#    simple summary on data
X.describe(include="all")
X.isna().sum()

#    impute age as avg age
X.loc[lambda x:x["age"].isna(),'age'] = int(X["age"].median())

#    train test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

X_train.head()
X_train.dtypes
y_train
X_train.shape
X_test.shape


#encode categorical variables
cat_cols = X_train.select_dtypes([object,"category",bool]).columns

encoder = ce.WOEEncoder(cols=cat_cols)
encoder.fit(X_train[cat_cols], y_train)

X_train[cat_cols] = encoder.transform(X_train[cat_cols])
X_test[cat_cols] = encoder.transform(X_test[cat_cols])

X_train.head()
X_test.head()


#discretize numeric variables
sns.displot(data=X[["fare"]],x="fare")

est = prep.KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
est.fit(X_train[["fare"]])
X_train["fare"] = est.transform(X_train[["fare"]])
X_test["fare"] = est.transform(X_test[["fare"]])

sns.displot(data=X_train[["fare"]],x="fare")

#   dummy and other encoders
if False:
    pd.get_dummies()
    prep.OneHotEncoder
    ce.TargetEncoder
    ce.LeaveOneOutEncoder
    ce.GLMMEncoder#doco says this is log odds if target is binary

#standardise
cols = X_train.columns
scaler = prep.StandardScaler()
scaler.fit(X_train)
X_train[cols] = scaler.transform(X_train)
X_test[cols] = scaler.transform(X_test)


X_train.head()
scaler.mean_
np.sqrt(scaler.var_)


#statsmodels
fitted_glm_model = sm.GLM(
    endog = y_train,
    exog = sm.add_constant(X_train),
    family = sm.families.Binomial()
).fit()

fitted_glm_model.summary()
fitted_glm_model.params.abs()/sum(fitted_glm_model.params.abs())*100

fitted_glm_model.get_prediction().summary_frame(alpha=0.05)


#evaluation

#    accuracy
import scipy

preds_train = fitted_glm_model.get_prediction().summary_frame()["mean"]
preds_test = fitted_glm_model.get_prediction(sm.add_constant(X_test)).summary_frame()["mean"]

scipy.stats.somersd(y_train, preds_train).statistic
scipy.stats.somersd(y_test, preds_test).statistic


#    calibration
preds_test_calibrated = np.where(preds_test>0.5, 1, 0)

_ = pd.concat([
    df.loc[X_test.index].assign(
        survived=preds_test_calibrated,
        prediction_actual="prediction"
    ),
    df.loc[X_test.index].assign(
        survived=y_test,
        prediction_actual="actual"
    ),
])

import matplotlib.pyplot as plt
sns.catplot(data=_, x="survived", hue = "prediction_actual",kind="count")
sns.catplot(data=_, x="survived", hue = "prediction_actual",col="adult_male",kind="count")
sns.catplot(data=_, x="survived", hue = "prediction_actual",col="class",kind="count")
plt.show()

#stability
from psi import calculate_psi

for col in X_train.columns:
    psi = calculate_psi(
        X_train[col], 
        X_test[col]
    )
    print(f"{col = }, {psi = }")


#sklearn
clf = ens.RandomForestClassifier(random_state=0)
clf.fit(X_train,y_train)

scipy.stats.somersd(y_train, clf.predict(X_train)).statistic
scipy.stats.somersd(y_test, clf.predict(X_test)).statistic


#pipeline
from sklearn.pipeline import make_pipeline

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

cat_cols = X_train.select_dtypes([object,"category",bool]).columns

column_trans = ColumnTransformer(
    [
        (
            'disc',
            prep.KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile'),
            ['fare']
        ),
        ('woe', ce.WOEEncoder(cols=cat_cols), cat_cols),
    ],
    remainder = 'passthrough'
)

column_trans.fit(X_train, y_train)
a = column_trans.transform(X_train)
a[0]


pipe = make_pipeline(
    column_trans,
    prep.StandardScaler(),
    ens.RandomForestClassifier(random_state=0)
)
pipe.fit(X_train, y_train)
pipe.predict(X_test)

#cv as evaluation
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate

X, y = make_regression(n_samples=1000, random_state=0)
lr = LinearRegression()

result = cross_validate(lr, X, y)  # defaults to 5-fold CV
result['test_score']  # r_squared score is high because dataset is easy

#para search
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from scipy.stats import randint

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# define the parameter space that will be searched over
param_distributions = {'n_estimators': randint(1, 5),
                       'max_depth': randint(5, 10)}

# now create a searchCV object and fit it to the data
search = RandomizedSearchCV(estimator=RandomForestRegressor(random_state=0),
                            n_iter=5,
                            param_distributions=param_distributions,
                            random_state=0)
search.fit(X_train, y_train)


search.best_params_


# the search object now acts like a normal random forest estimator
# with max_depth=9 and n_estimators=4
search.score(X_test, y_test)





