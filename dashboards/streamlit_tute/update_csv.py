from pathlib import Path

import pandas as pd
import streamlit as st

# update this csv
################################################################
file = Path(__file__).parent / "update_csv.csv"
# df = pd.DataFrame({"col1": ["aaa", "bbb"], "col2": [1.0, 2.0]})

# input fields
col1_value = st.text_input("Enter the col1 value", "aaa")
col2_value = st.number_input("Enter the col2 value", 0, 100, 2)

# button to update
pressed = st.button("update")

# display table
table_div = st.empty()

# log the actions
log_div = st.empty()

# actions:

# read and display
df = pd.read_csv(file)
table_div.dataframe(df)

# initialise a list of actions storage
if "text" not in st.session_state:
    st.session_state["text"] = [""]

# update csv
if pressed:
    df.loc[lambda x: x.col1 == col1_value, "col2"] += col2_value
    df.to_csv(file, index=False)

    st.session_state.text.append(f"Updated {col1_value} with {col2_value}")
    log_div.write(st.session_state.text)

    df = pd.read_csv(file)
    table_div.dataframe(df)
