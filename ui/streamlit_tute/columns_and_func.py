import numpy as np
import pandas as pd
import streamlit as st


def get_df(number):
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": number * np.array([5, 6, 7, 8])})
    return df


def get_and_display_df(key):
    url = "https://en.wikipedia.org/wiki/Main_Page"
    f"[{url}]({url})"

    number = st.slider("Pick a number", 0, 100, 50, key=key)
    df = get_df(number)

    st.table(df)

    st.line_chart(df)


col1, col2 = st.columns(2)

with col1:
    get_and_display_df(1)


with col2:
    get_and_display_df(2)
