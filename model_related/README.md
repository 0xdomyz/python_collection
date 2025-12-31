# Model Related Module

Machine learning tutorials and examples across multiple frameworks and algorithms.

## Structure

### Algorithms by Category

**Classical ML**
- `sklearn_tute/` - Scikit-learn tutorials (models, pipelines, preprocessing)
- `decision_trees/` - Decision tree examples
- `logistic/` - Logistic regression
- `glm/` - Generalized Linear Models (statsmodels)
- `gbm/` - Gradient Boosting Machines
- `cluster/` - Clustering algorithms (K-means, hierarchical)

**Statistical Models**
- `statsmodels_tute/` - Statsmodels time series and statistical testing
- `ts_tute/` - Time series modeling
- `bayesian/` - Bayesian inference with PyMC3

**Deep Learning**
- `torch_tute/` - PyTorch neural networks
- `keras_tute/` - Keras/TensorFlow models
- `tensor_flow_script/` - TensorFlow examples

**Specialized**
- `signal_tute/` - Signal processing and Kalman filters
- `survival/` - Survival analysis
- `credit/` - Credit scoring and WOE
- `risk_theory/` - Risk modeling
- `option_pricing/` - Financial derivatives pricing
- `shap_related/` - SHAP interpretability
- `ds_framework/` - Data science framework patterns

### Core Modules

- `dataset.py` - Loading and exploring datasets (iris example)
- `feature.py` - Feature manipulation patterns
- `plot.py` - Plotting utilities reference
- `randf.py` - Random forest examples
- `scipy_scripts.py` - SciPy statistical functions
- `interraction_ice.py` - Interaction and ICE plots

## Reusable Utilities

### Model Evaluation (`evaluation_utils.py`)

Comprehensive model scoring and comparison:

```python
from python_collection.model_related import evaluation_utils

# Classification metrics
metrics = evaluation_utils.classification_metrics(y_test, y_pred, y_pred_proba)

# Regression metrics
metrics = evaluation_utils.regression_metrics(y_test, y_pred)

# Cross-validation scoring
cv_results = evaluation_utils.cv_score(estimator, X, y, cv=5)

# Compare multiple models
models = {
    'Random Forest': RandomForestClassifier(),
    'Gradient Boosting': GradientBoostingClassifier(),
}
comparison = evaluation_utils.compare_models(models, X_train, y_train, X_test, y_test)

# Feature importance
importance = evaluation_utils.feature_importance_summary(model, X.columns)
```

### Feature Engineering (`feature_engineering.py`)

Data transformation and feature creation:

```python
from python_collection.model_related import feature_engineering

# Handle missing values
df_clean = feature_engineering.handle_missing_values(df, strategy='median')

# Detect outliers
outliers = feature_engineering.detect_outliers(df['price'], method='iqr')

# Create interactions
df_inter = feature_engineering.create_interaction_features(df, ['age', 'income'])

# Polynomial features
df_poly = feature_engineering.create_polynomial_features(df, ['price'], degree=2)

# Encode categories
df_encoded = feature_engineering.categorical_encoding(df, ['color'], method='onehot')

# Scale features
df_scaled, params = feature_engineering.scale_features(df, ['price', 'age'])

# Feature selection
numeric = feature_engineering.select_numeric_features(df)
categorical = feature_engineering.select_categorical_features(df)
selected = feature_engineering.feature_selection_by_variance(X, threshold=0.01)
uncorr = feature_engineering.correlation_filter(df, threshold=0.9)
```

## Running Examples

### Jupyter Notebooks

```console
# Credit scoring examples
jupyter notebook model_related/credit/

# Sklearn tutorials
jupyter notebook model_related/sklearn_tute/

# Deep learning tutorials
jupyter notebook model_related/torch_tute/
jupyter notebook model_related/keras_tute/
```

### Python Scripts

```console
# Classification example
python model_related/sklearn_tute/skl_tute.py

# Time series
python model_related/ts_tute/ts_lm.py

# Clustering
python model_related/cluster/cluster.py
```

## Common ML Workflows

### 1. Train-Test Evaluation Pipeline

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from python_collection.model_related import evaluation_utils

# Load data
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
metrics = evaluation_utils.classification_metrics(y_test, y_pred)
print(f"Accuracy: {metrics['accuracy']:.3f}")
```

### 2. Feature Engineering Pipeline

```python
from python_collection.model_related import feature_engineering

# Clean and prepare
df_clean = feature_engineering.handle_missing_values(df, strategy='median')
df_clean = df_clean[~feature_engineering.detect_outliers(df_clean['price'])]

# Engineer features
df_eng = feature_engineering.create_interaction_features(df_clean, ['age', 'income'])
df_eng = feature_engineering.create_polynomial_features(df_eng, ['price'], degree=2)

# Encode & scale
df_encoded = feature_engineering.categorical_encoding(df_eng, ['color'])
X_scaled, params = feature_engineering.scale_features(df_encoded, ['price', 'age'])

# Select features
uncorr = feature_engineering.correlation_filter(X_scaled, threshold=0.9)
```

### 3. Model Comparison

```python
from python_collection.model_related import evaluation_utils
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

models = {
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100),
    'SVM': SVC(kernel='rbf', probability=True),
}

comparison = evaluation_utils.compare_models(models, X_train, y_train, X_test, y_test)
print(comparison.sort_values('f1', ascending=False))
```

## Best Practices

- **Start with simpler models** - baseline with logistic regression before complex algorithms
- **Validate early** - use cross-validation to assess model stability
- **Feature engineering matters** - often more important than algorithm choice
- **Monitor for overfitting** - compare train vs test metrics
- **Document data sources** - datasets module shows sklearn toy dataset usage
- **Use pipelines** - sklearn Pipeline combines preprocessing and modeling

## Installation

Install with ML dependencies:

```console
pip install -e ".[ml]"  # Standard ML
pip install -e ".[dl]"  # Deep learning (torch, tensorflow)
pip install -e ".[bayesian]"  # Bayesian (PyMC3)
```

## All Examples Are Standalone

Each script/notebook is self-contained. If you need to reuse utilities, install in editable mode:

```console
pip install -e .
```

Then import utilities:
```python
from python_collection.model_related import evaluation_utils
from python_collection.model_related import feature_engineering
```
