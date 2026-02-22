"""Categorical variable analysis page with DuckDB-powered subsetting."""

from itertools import zip_longest

import duckdb
import pandas as pd
import streamlit as st
from utils.categorical import categorical_summary, get_categorical_columns

st.set_page_config(
    page_title="Categorical Summary",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Require data to be loaded from main page
if "df" not in st.session_state:
    st.warning("⚠️ Load data from the main page first")
    st.stop()

df = st.session_state.df
st.title("📋 Categorical Variable Summary")

# Get categorical columns
cat_cols = get_categorical_columns(df)

if not cat_cols:
    st.info("No categorical (object) columns found in dataset")
    st.stop()

st.subheader("Data Subset Control")

with st.expander("SQL Query", expanded=True):
    sql_query = st.text_area(
        "Edit SQL to subset data (use 'df' as table name)",
        value="select * from df",
        height=80,
        help="Customize columns, add WHERE clause, etc.",
    )

    # Execute query and get subset
    try:
        con = duckdb.connect()
        df_subset = con.execute(sql_query).df()
        con.close()
        st.success(
            f"✓ Query result: {df_subset.shape[0]} rows × {df_subset.shape[1]} columns"
        )
    except Exception as e:
        st.error(f"❌ Query error: {str(e)}")
        st.stop()

# Summary controls
col1, col2 = st.columns(2)
with col1:
    n_cols_display = st.number_input(
        "Max columns to display",
        min_value=1,
        max_value=15,
        value=5,
        help="Maximum number of categorical columns in grid",
    )

# Get categorical columns from subset
cat_cols_subset = get_categorical_columns(df_subset)
cat_cols_subset = cat_cols_subset[:n_cols_display]

if not cat_cols_subset:
    st.info("No categorical columns in subset")
    st.stop()

# Create summary tables in grid layout
st.subheader("Summary Tables")

# Determine grid dimensions (max 3 columns)
n_cols = min(3, len(cat_cols_subset))
n_rows = (len(cat_cols_subset) + n_cols - 1) // n_cols

# Create grid
cols_layout = [st.columns(n_cols) for _ in range(n_rows)]
flat_cols = [col for row in cols_layout for col in row]

for i, cat_col in enumerate(cat_cols_subset):
    with flat_cols[i]:
        summary = categorical_summary(df_subset, cat_col)
        st.markdown(f"**{cat_col}**")
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.dataframe(summary, use_container_width=True, hide_index=True)
