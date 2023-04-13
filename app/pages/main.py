import streamlit as st

# App imports
from app.data import get_dataframe, plot_by_region

df = get_dataframe()

st.title('Philippine Poverty Area Estimates Dashboard')
st.markdown( "\n".join([
    '## Philippines: Povery Statistics Dataset',
    'Based on Republic Act 8425, otherwise known as Social Reform and Poverty Alleviation Act, dated 11 December 1997, the poor refers to individuals and families whose income fall below the poverty threshold as defined by the government and/or those that cannot afford in a sustained manner to provide their basic needs of food, health, education, housing and other amenities of life.',
    '* Data source: [United Nations Office for the Coordination of Humanitarian Affairs (UN OHCA)](https://www.unocha.org/philippines) and [Philippine Statistics Authority (PSA)](https://psa.gov.ph)',
    '* Data from: https://data.humdata.org/dataset/philippines-poverty-statistics',
    '* Geojson file from: [faeldon/philippines-json-maps](https://github.com/faeldon/philippines-json-maps)']) )

st.dataframe(df)
