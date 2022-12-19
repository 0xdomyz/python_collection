from pathlib import Path

import pandas as pd
import streamlit as st

col1_value = st.text_input("Enter the col1 value", "aaa")

col2_value = st.number_input("Enter the col2 value", 0, 100, 2)

pressed = st.button("update")

file = Path(__file__).parent / "update_csv.csv"

# df = pd.DataFrame({"col1": ["aaa", "bbb"], "col2": [1.0, 2.0]})

table_div = st.empty()

df = pd.read_csv(file)
table_div.dataframe(df)

# Initialization
if "text" not in st.session_state:
    st.session_state["text"] = [""]

if pressed:
    df.loc[lambda x: x.col1 == col1_value, "col2"] += col2_value
    df.to_csv(file, index=False)

    st.session_state.text.append(f"Updated {col1_value} with {col2_value}")
    st.write(st.session_state.text)

    df = pd.read_csv(file)
    table_div.dataframe(df)
