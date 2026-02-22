"""Data Analysis Dashboard - CSV input and data overview."""

import pandas as pd
import streamlit as st
from utils.data_checks import get_data_overview

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

if csv_input:
    st.session_state.csv_path = csv_input

if "csv_path" in st.session_state and st.session_state.csv_path:
    try:
        df = pd.read_csv(st.session_state.csv_path)
        st.session_state.df = df
        st.success(f"✓ CSV loaded: {df.shape[0]} rows × {df.shape[1]} columns")

        st.subheader("Data Overview & Quality")
        overview = get_data_overview(df)
        st.dataframe(overview, use_container_width=True)

    except FileNotFoundError:
        st.error(f"❌ File not found: {st.session_state.csv_path}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.info("👈 Enter a CSV file path in the sidebar to get started")
