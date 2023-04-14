import streamlit as st

# App imports
from app.data import get_dataframe, get_region_name_by_region_code, get_year_by_column_name, get_plot_by_province, get_plot_by_region
from app.config import hide_streamlit_style

st.set_page_config(page_title="PH Poverty Area Estimates", page_icon = ":round_pushpin:")
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

df = get_dataframe()
region_name_by_region_code = get_region_name_by_region_code()
region_names = [name for name in region_name_by_region_code.keys()]
year_by_column_name = get_year_by_column_name()
years = [year for year in year_by_column_name.keys()]

with st.container():
    st.title('Philippine Poverty Area Estimates Choropleth Visualization')
    st.caption('Estimates from year 2006, 2009, 2012, 2015')

    with st.expander("See dataset information"):
        st.markdown( "\n".join([
            '## Philippines: Povery Statistics Dataset',
            'Based on Republic Act 8425, otherwise known as Social Reform and Poverty Alleviation Act, dated 11 December 1997, the poor refers to individuals and families whose income fall below the poverty threshold as defined by the government and/or those that cannot afford in a sustained manner to provide their basic needs of food, health, education, housing and other amenities of life.',
            '* Data source: [United Nations Office for the Coordination of Humanitarian Affairs (UN OHCA)](https://www.unocha.org/philippines) and [Philippine Statistics Authority (PSA)](https://psa.gov.ph)',
            '* Data from: https://data.humdata.org/dataset/philippines-poverty-statistics',
            '* Geojson file from: [faeldon/philippines-json-maps](https://github.com/faeldon/philippines-json-maps)']) )
        
        with st.container():
            st.subheader('\n')
            st.dataframe(df)

    col1, col2 = st.columns([1.2,1]) 
    with col1:
        visualize_by_option = st.selectbox(
            'Visualize by',
            ['Select option', 'Region', 'Province'], )

    with col2:
        year_by_option = st.radio(
            'Year at', years,
            horizontal = True, )

    if visualize_by_option == 'Province':
        options_province_visualize_by = ['Select province'] + region_names
        province_visualize_by = st.selectbox(
            'Visualize provinces by region',
            options_province_visualize_by, )

    with st.container():
        if visualize_by_option == 'Region':
            figure = get_plot_by_region(
                dataframe = df, 
                year = year_by_option, )
            st.plotly_chart(figure, use_container_width = True)

        elif visualize_by_option == 'Province':
            if province_visualize_by != 'Select province':
                figure = get_plot_by_province(
                    dataframe = df,
                    year = year_by_option, 
                    region_name = province_visualize_by, )
                st.plotly_chart(figure, use_container_width = True)


