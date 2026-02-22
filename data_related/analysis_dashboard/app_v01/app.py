"""Data Analysis Dashboard - CSV input and basic data quality checks."""

import pandas as pd
import streamlit as st
from utils.data_checks import compute_data_quality_checks
from utils.info_view import create_vertical_info_view

st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Data Analysis Dashboard")

with st.sidebar:
    st.header("📁 Data Input")
    csv_input = st.text_input(
        "CSV file path",
        placeholder="path/to/file.csv",
        help="Provide the path to your CSV file.",
    )

# Store CSV path in session state
if csv_input:
    st.session_state.csv_path = csv_input

# Load and display CSV data with checks
if "csv_path" in st.session_state and st.session_state.csv_path:
    try:
        df = pd.read_csv(st.session_state.csv_path)
        st.session_state.df = df

        st.success(f"✓ CSV loaded: {df.shape[0]} rows × {df.shape[1]} columns")

        # Info view section
        st.subheader("Dataset Overview")
        col1, col2 = st.columns([2, 1])

        with col1:
            info_view = create_vertical_info_view(df)
            st.dataframe(info_view, use_container_width=True)

        # Data quality checks section
        st.subheader("Data Quality Checks")
        dq_checks = compute_data_quality_checks(df)

        tab1, tab2 = st.tabs(["Counts", "Percentages"])
        with tab1:
            st.dataframe(dq_checks["counts"], use_container_width=True)
        with tab2:
            st.dataframe(dq_checks["percentages"], use_container_width=True)

    except FileNotFoundError:
        st.error(f"❌ File not found: {st.session_state.csv_path}")
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
else:
    st.info("👈 Enter a CSV file path in the sidebar to get started")
