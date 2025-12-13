# python -m streamlit run streamlit_ver.py
import streamlit as st  # Streamlit
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Titanic Survival Analysis")  # streamlit UI

df = sns.load_dataset("titanic")
st.write(f"Dataset shape: {df.shape}")  # Streamlit 
st.dataframe(df.head())  # Interactive

possible_values = list(set(df.select_dtypes(include=['object','int','bool','category']).columns) - set(['survived']))
var = st.selectbox("Select grouping variable:", possible_values, index=0)

pdf = df.groupby([var], dropna=False, observed=False).agg(
    **{
        "n": ("survived", "size"),
        "survived_rate": ("survived", "mean"),
    }
)

st.subheader("Survival Statistics by Group")  # streamlit UI
st.dataframe(pdf)  # streamlit UI

fig, ax = plt.subplots()
pdf.plot(kind="bar", y="n", color='teal', ax=ax)
ax2 = ax.twinx()
pdf.plot(kind="line", y="survived_rate", ax=ax2, color="blue", marker="o")
ax.set_ylabel("Count")
ax2.set_ylabel("Survival Rate")

st.pyplot(fig)  # streamlit UI