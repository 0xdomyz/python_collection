import streamlit as st
from utils import np

st.set_page_config(page_title="Multipage demo", page_icon="📄")

st.write("main page text")

nbr = np.random.random(10)
st.write(nbr)
