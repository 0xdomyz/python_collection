import numpy as np
import pandas as pd
import streamlit as st


def get_df(number):
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": number * np.random.randn(4)})
    return df


"""
# My first app
Here's our first attempt at using data to create a table:

"""

url = "https://en.wikipedia.org/wiki/Main_Page"
f"[{url}]({url})"


number = st.slider("Pick a number", 0, 100, 50)
df = get_df(number)

df
st.write(df)
st.table(df)

st.line_chart(df)
