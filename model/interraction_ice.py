import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

# Load dataset
boston = load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)
y = boston.target
feature = 'LSTAT'

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Grid of values for PDP/ICE
grid = np.linspace(X_test[feature].min(), X_test[feature].max(), 50)

# ICE: Predict for each sample with feature set to grid value
ice_curves = []
for i in range(len(X_test)):
    X_sample = X_test.iloc[[i]].copy()
    preds = []
    for val in grid:
        X_sample[feature] = val
        preds.append(model.predict(X_sample)[0])
    ice_curves.append(preds)

# PDP: average of ICE curves
ice_curves = np.array(ice_curves)
pdp_curve = ice_curves.mean(axis=0)

# Plotting
plt.figure(figsize=(10, 6))

# Plot ICE lines
for curve in ice_curves:
    plt.plot(grid, curve, color='lightgray', linewidth=0.8, alpha=0.5)

# Plot PDP line
plt.plot(grid, pdp_curve, color='blue', linewidth=2, label='PDP (Average Effect)')

plt.xlabel(feature)
plt.ylabel('Predicted Price')
plt.title(f'ICE and PDP for Feature: {feature}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()