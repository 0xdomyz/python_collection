import streamlit as st
from utils import np

nbr = np.random.random(10)
nbr


pressed = st.button("Press")

if pressed:
    "pressed"
