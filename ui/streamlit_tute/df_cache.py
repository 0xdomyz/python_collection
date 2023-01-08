import time

import numpy as np
import pandas as pd
import streamlit as st


def get_df():
    df = pd.DataFrame(np.random.randn(10, 4), columns=("col %d" % i for i in range(4)))
    return df


@st.cache
def large():
    time.sleep(6)


left_column, right_column = st.columns(2)


with left_column:
    large()
    df = get_df()
    df
    df = get_df()
    df

with right_column:
    large()
    df = get_df()
    df
    df = get_df()
    df


time.sleep(5)
st.experimental_rerun()
