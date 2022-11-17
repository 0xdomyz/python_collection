import numpy as np
import pandas as pd
import streamlit as st

if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    chart_data


df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

option = st.selectbox("Which number do you like best?", df["first column"])

"You selected: ", option

_ = float(df.loc[lambda x: x["first column"] == option, "second column"])
f"which means {_}"
