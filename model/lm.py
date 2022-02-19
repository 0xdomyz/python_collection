from sklearn.linear_model import LogisticRegression

config = dict(
    penalty = None,
    solver = ''
)
x_train = 1
y_train = 1

log_reg = LogisticRegression(**config['parameters'])
log_reg.fit(x_train,y_train)

p = log_reg.predict_proba(x_train)

log_reg.coef_
log_reg.intercept_







