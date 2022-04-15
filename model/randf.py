from sklearn.ensemble import RandomForestClassifier

config = dict(n_estimators=100, max_depth=5, random_state=0, min_samples_leaf=100)
x_train = 1
y_train = 1

rand_frst = RandomForestClassifier(**config)
rand_frst.fit(x_train, y_train)

rand_frst.predict_proba(x_train)
