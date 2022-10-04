"""random forest"""
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(random_state=0)
X = [[1, 2, 3], [11, 12, 13]]  # 2 samples, 3 features
y = [0, 1]  # classes of each sample
clf.fit(X, [0, 0, 1])
clf.fit(X, y)

clf.predict(X)  # predict classes of the training data
clf.predict([[4, 5, 6], [14, 15, 16]])  # predict classes of new data
clf.predict([[1, 1, 1], [16, 16, 16]])
clf.predict([[-10, -1000, 10000], [99, 1100, 1]])

clf.n_features_in_
clf.feature_importances_
clf.base_estimator

clf.verbose = 100
clf.fit(X, y)
clf.predict([[0, 1, 0]])


"""transform preproc"""
from sklearn.preprocessing import StandardScaler
import numpy as np

X = [[0, 15], [0.2, 10], [0.5, 0], [0.7, 10], [2, -15]]
# scale data according to computed scaling values
StandardScaler().fit(X).transform(X)

x2 = [i[1] for i in X]
(x2 - np.mean(x2)) / np.std(x2)


"""pipeline"""
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# create a pipeline object
pipe = make_pipeline(StandardScaler(), LogisticRegression())

# load the iris dataset and split it into train and test sets
iris = load_iris(as_frame=True)
iris.keys()
iris["data"]
iris["target"]
iris["frame"]
iris["target_names"]
X, y = load_iris(return_X_y=True)
X
y
len(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
len(X_train)
len(X_test)

# fit the whole pipeline
pipe.fit(X_train, y_train)

# we can now use it like any other estimator
accuracy_score(pipe.predict(X_test), y_test)


"""evaluation"""
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate

make_regression(10, 3, random_state=0)
X, y = make_regression(n_samples=1000, random_state=0)
X, y = make_regression(n_samples=1000, random_state=0, bias=5)
len(X)
lr = LinearRegression()

result = cross_validate(lr, X, y)  # defaults to 5-fold CV
result["test_score"]  # r_squared score is high because dataset is easy


"""parameter search"""
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from scipy.stats import randint

randint(5, 7).cdf(5.1)

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
len(y_train)

# define the parameter space that will be searched over
param_distributions = {"n_estimators": randint(1, 5), "max_depth": randint(5, 10)}

# now create a searchCV object and fit it to the data
search = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=0),
    n_iter=5,
    param_distributions=param_distributions,
    random_state=0,
)
search.fit(X_train, y_train)

search.best_params_

# the search object now acts like a normal random forest estimator
# with max_depth=9 and n_estimators=4
search.score(X_test, y_test)
