import time

import numpy as np
import pandas as pd
import streamlit as st

st.title("Caching demo (st.cache_data)")


@st.cache_data(ttl=30)
def get_df(rows: int = 10, cols: int = 4) -> pd.DataFrame:
    """Return a random DataFrame; cached for 30s."""
    time.sleep(2)  # simulate slow fetch
    return pd.DataFrame(
        np.random.randn(rows, cols), columns=[f"col {i}" for i in range(cols)]
    )


rows = st.slider("Rows", 5, 50, 10)
cols = st.slider("Cols", 2, 8, 4)
refresh = st.button("Force refresh (bust cache)")

if refresh:
    get_df.clear()

left, right = st.columns(2)

with left:
    st.caption("Cached call")
    st.dataframe(get_df(rows, cols))

with right:
    st.caption("Second cached call (should be instant)")
    st.dataframe(get_df(rows, cols))

st.info("Cached for 30s; use the button to clear the cache.")
