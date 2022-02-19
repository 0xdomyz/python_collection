from configparser import MAX_INTERPOLATION_DEPTH
import lightgbm

config = dict(
    num_leaves = 5,
    max_depth = 10,
    min_child_weight = 0.2
)
x_train = 1
y_train = 1
x_eval = 1
y_eval = 1

lightgbm.Dataset(data=x_train, label=y_train)
lgb = lightgbm.LGBMClassifier(**config)
lgb.fit(
    x_train,
    y_train,
    eval_set=[x_eval, y_eval],
    early_stopping_rounds = 20
)

lgb.best_iteration_
lgb.predict(x_train, raw_score= True)
lgb.predict_proba(x_train)



