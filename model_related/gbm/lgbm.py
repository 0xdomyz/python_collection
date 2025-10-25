import xgboost as xgb
import shap
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

# Load data
X, y = fetch_california_housing(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train GBM model
model = xgb.XGBRegressor(
    n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42
)
model.fit(X_train, y_train)

# SHAP explainer and values
explainer = shap.Explainer(model, X_test)
shap_values = explainer(X_test)

# SHAP summary plot (shows top features & interactions)
shap.plots.beeswarm(shap_values)

# SHAP interaction values (pairwise SHAP decomposition)
interaction_vals = shap.TreeExplainer(model).shap_interaction_values(X_test)

# Interaction plot for a specific feature (e.g., 'AveOccup')
shap.dependence_plot(
    ind="AveOccup",
    shap_values=interaction_vals,
    features=X_test,
    interaction_index="HouseAge",  # Or let SHAP auto-pick strongest pair
    show=True,
)
