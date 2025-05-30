import numpy as np
import pandas as pd
import streamlit as st
import random
import matplotlib.pyplot as plt


def refresh_data(k):
    data = pd.read_csv("titanic.csv")
    index = random.sample(data.index.tolist(), k=min(k, data.shape[0]))  # random index
    data = data.loc[index, :]
    return data


(col1,) = st.columns(1)

with col1:
    slider = st.slider("Select number of rows", 1, 891, 500)  # slider
    column = st.selectbox(
        "Select column",
        [
            "class",
            "who",
            "sex",
            "age",
            "sibsp",
            "parch",
            "embarked",
        ],
    )
    checkbox = st.checkbox("plot?", value=True)  # checkbox
    pressed = st.button("refresh data")  # button

    if pressed:
        data = refresh_data(slider)
        data  # display dataframe

        if checkbox:
            chart_data = data.groupby(column).agg({"survived": "mean"})
            fig, ax = plt.subplots()
            chart_data.plot.bar(ax=ax)
            st.pyplot(fig)  # show pyplot

    st.button("Re-run")  # un-connected button to rerun.
