import numpy as np
import pandas as pd
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider("Select a range of values", 0.0, 30.0, (5.0, 10.0))


_ = [int(i) for i in add_slider]
df = pd.DataFrame(np.random.randn(*_))

add_selectbox
df
