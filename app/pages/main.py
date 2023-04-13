import streamlit as st

# App imports
from app.data import get_dataframe

df = get_dataframe()

st.title('Philippine Poverty Area Estimates Dashboard')
st.dataframe(df)