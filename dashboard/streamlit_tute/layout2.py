import numpy as np
import pandas as pd
import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
pressed = left_column.button("Press me!")

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        "Sorting hat", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")

with left_column:
    if pressed:
        df = pd.DataFrame(np.random.randn(3, 15))
        df
