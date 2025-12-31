# Data Related Module

Data manipulation, cleaning, APIs, and database examples. Scripts and notebooks are standalone demos.

## Structure
- **pandas_related/** – DataFrame operations (aggregation, apply, pivot/melt, timeseries, janitor)
- **analysis/** – Data quality summaries, feature flags, category summaries (notebooks)
- **apis/** – External API examples (e.g., `yfi_tute.py` for yfinance)
- **db_related/** – Database connections (asyncpg, DuckDB, SQLAlchemy), sample Chinook DB
- **cleanning/** – Data wrangling notebooks
- **toydata/** – Sample datasets
- **cleaning_utils.py** – Reusable cleaning helpers

## Reusable Utilities
### Cleaning Utils (`cleaning_utils.py`)
- `standardize_column_names(df)` – strip, underscore, lowercase column names
- `detect_data_quality_issues(df)` – missing/zero/negative/blank counts per column

### DB Connectors
- `db_related/connectors_base.py` – base patterns for DB connectors
- `db_related/asyncpg_script.py` / `asyncio_tothread_qry.py` – async DB access examples

## Running Examples
```console
# Pandas scripts
python data_related/pandas_related/apply_script.py

# API example (yfinance)
python data_related/apis/yfi_tute.py

# Database async example
python data_related/db_related/asyncpg_script.py

# Notebooks
jupyter notebook data_related/pandas_related/
jupyter notebook data_related/analysis/
```

## Notes
- Examples are self-contained; install dependencies as needed (`pip install -e .[ml]` covers pandas, numpy, matplotlib, seaborn, scipy, statsmodels).
- Avoid `sys.path` tweaks; use editable install if importing utilities: `pip install -e .` then
  ```python
  from python_collection.data_related import cleaning_utils
  ```
