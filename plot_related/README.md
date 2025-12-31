# Plot Related Module

Visualization demonstrations and utilities across multiple Python plotting libraries.

## Structure

- **mpl_notes/** - Matplotlib documentation and examples
  - `docu_notes/` - Detailed matplotlib feature demos
  - `contents/` - Specific plot types (bars, lines, scatter, etc.)
  - `addons/` - Extensions and additional utilities

- **seaborn_notes/** - Seaborn statistical visualization examples
  - High-level interface over matplotlib
  - Distribution, relationship, and categorical plots

- **pandas_plot/** - Pandas plotting (built on matplotlib)
  - DataFrame `.plot()` method variations
  - Quick exploratory plots

- **ui_approaches/** - Interactive UI frameworks
  - `streamlit_app.py` - Streamlit dashboard example
  - `script_mpl.py` - Matplotlib script
  - `script_plotly.py` - Plotly interactive example
  - `vscode_interactive.py` - VS Code interactive plots

- **plot_examples/** - Specific plot type examples
  - `bars/` - Bar chart variations
  - `lines/` - Line plot variations

## Reusable Utilities

### Plotting Utils (`plotting_utils.py`)

Common matplotlib and seaborn helpers:

```python
from python_collection.plot_related import plotting_utils

# Set consistent style
plotting_utils.set_style("whitegrid", "deep")

# Create subplots easily
fig, axes = plotting_utils.create_subplots(2, 2)

# Plot distributions
plotting_utils.plot_distribution(df['column'], title='Distribution')

# Correlation heatmap
plotting_utils.plot_correlation_heatmap(df)

# Categorical vs numeric
plotting_utils.plot_categorical_vs_numeric(df, 'category', 'value', kind='violin')
```

### Streamlit Utils (`streamlit_utils.py`)

Streamlit dashboard helpers:

```python
from python_collection.plot_related import streamlit_utils

# Load data with caching
df = streamlit_utils.load_dataset('titanic')

# Display summary
streamlit_utils.display_data_summary(df)

# Create column selector
col = streamlit_utils.create_column_selector(df)

# Plot distribution
streamlit_utils.plot_column_distribution(df, col)

# Filter widget
df_filtered = streamlit_utils.create_filter_widget(df, col)

# Display metrics
streamlit_utils.display_metrics_row({'Mean': 42.5, 'Std': 12.3})
```

## Running Examples

### Streamlit Apps

```console
# Run Streamlit dashboard
python -m streamlit run plot_related/ui_approaches/streamlit_app.py
```

### Jupyter Notebooks

```console
# Open matplotlib examples
jupyter notebook plot_related/mpl_notes/docu_notes/

# Open seaborn examples
jupyter notebook plot_related/seaborn_notes/
```

### Python Scripts

```console
# Run matplotlib script
python plot_related/ui_approaches/script_mpl.py

# Run plotly script
python plot_related/ui_approaches/script_plotly.py
```

## Common Patterns

### 1. Using Plotting Utils

```python
from python_collection.plot_related import plotting_utils
import pandas as pd

df = pd.read_csv('data.csv')

# Create subplots with consistent sizing
fig, axes = plotting_utils.create_subplots(2, 2, figsize=(12, 10))

# Plot distributions on subplots
for idx, col in enumerate(df.select_dtypes(include=['float64']).columns):
    plotting_utils.plot_distribution(df[col], ax=axes[idx])

# Save figure
plotting_utils.save_and_show(fig, 'distributions.png', show=True)
```

### 2. Building Streamlit Dashboard

```python
import streamlit as st
from python_collection.plot_related import streamlit_utils

st.title("Data Dashboard")

# Load and display data summary
df = streamlit_utils.load_dataset('titanic')
streamlit_utils.display_data_summary(df)

# Create filter
df_filtered = streamlit_utils.create_filter_widget(df, 'pclass')

# Select column to plot
col = streamlit_utils.create_column_selector(df_filtered)
streamlit_utils.plot_column_distribution(df_filtered, col)
```

### 3. Correlation Analysis

```python
from python_collection.plot_related import plotting_utils
import pandas as pd

df = pd.read_csv('data.csv')

# Plot correlation heatmap
plotting_utils.plot_correlation_heatmap(df, annot=True, cmap='coolwarm')
```

## Installation

Install with plot dependencies:

```console
pip install -e ".[viz]"
```

This includes: matplotlib, seaborn, plotly, streamlit

## All Examples Are Standalone

Each script/notebook is self-contained and can be run independently. No cross-imports required.

If you need to reuse utilities, install this project in editable mode first:
```console
pip install -e .
```

Then import utilities in your own code:
```python
from python_collection.plot_related import plotting_utils
```
