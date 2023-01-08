import numpy as np
import pandas as pd
import streamlit as st

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

center = [-33.86, 151.2]

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [20, 20] + center, columns=["lat", "lon"]
)

st.map(map_data)
