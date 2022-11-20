from sklearn.base import BaseEstimator, TransformerMixin, is_outlier_detector
from sklearn.metrics import auc, mean_absolute_percentage_error, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, scale

x_train = 1
y_train = 1

train_test_split(x_train, y_train, test_size=0.2, random_state=0)

scaler = StandardScaler()
scaler.transform(x_train)
scaler.fit_transform(x_train)
scaler.scale_
scaler.mean_
