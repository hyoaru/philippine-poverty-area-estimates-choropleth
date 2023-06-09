import json
import pandas as pd
import plotly.express as px
import streamlit as st

# App imports
from app.utilities import load_fig_binary, save_fig_binary


# Initial computations

df = pd.read_csv(r'data/csv/poverty_statistics_clnd.csv')

region_codes_ordered = [region_code for region_code in df['Region code'].unique()]
region_codes_ordered.sort()

df['Region code'] = pd.Categorical(
    df['Region code'], categories = region_codes_ordered,
    ordered = True, )

columns_to_include = [
    x for x in df.columns 
    if not (x.startswith('Poverty') or x.startswith('Annual'))]

magnitude_pf_est_by_year_column_names = [
    x for x in columns_to_include 
    if x.startswith('Magnitude')]

total_magnitude_pf_est_by_year_column_names = [
    x for x in columns_to_include 
    if x.startswith('Total')]

year_by_column_name = dict(zip(
    ['2006', '2009', '2012', '2015'], 
    magnitude_pf_est_by_year_column_names))

year_by_column_name_total = dict(zip(
    ['2006', '2009', '2012', '2015'], 
    total_magnitude_pf_est_by_year_column_names))

region_name_by_region_code = dict(
    df[['Region', 'Region code']]
    .value_counts()
    .reset_index()
    .iloc[:, [0,1]]
    .sort_values('Region code')
    .values)

# Functions

@st.cache_data
def get_dataframe() -> pd.DataFrame:
    return df

@st.cache_data
def get_year_by_column_name() -> dict:
    return year_by_column_name

@st.cache_data
def get_year_by_column_name_total() -> dict:
    return year_by_column_name_total

@st.cache_data
def get_region_name_by_region_code():
    return region_name_by_region_code

def figure_update_layout(fig):
    fig.update_layout(
    coloraxis=dict(colorbar=dict(orientation='h', y=0.9)),
    coloraxis_colorbar = dict(title = 'Magnitude'), 
    margin={"r":0,"t":0,"l":0,"b":0}, 
    paper_bgcolor = 'rgba(0,0,0,0)', 
    plot_bgcolor = 'rgba(0,0,0,0)',
    geo = dict(bgcolor = 'rgba(0,0,0,0)', ), 
    modebar_bgcolor = 'rgba(0,0,0,0)',
    modebar_color = '#6d0006',
    modebar_activecolor = '#323140',
    modebar_orientation = 'v')

@st.cache_data
def get_plot_by_region(dataframe, year: str):
    file_name = f'by_region_{year}'
    folder_name = 'regions'

    fig = load_fig_binary(file_name = file_name, folder_name = folder_name)
    if fig is not None:
        return fig
    else:
        geojson_path = 'data/geojson'
        geojson_folder_name = 'regions'
        geojson_file_name = 'regions.0.01'
        geojson_file = json.load(open(rf'{geojson_path}/{geojson_folder_name}/{geojson_file_name}.json'))

        fig = px.choropleth(
            data_frame = dataframe,
            geojson = geojson_file,
            featureidkey = 'properties.ADM1_PCODE',
            locations = 'Region code',
            color = year_by_column_name_total[year],
            scope = 'asia',
            color_continuous_scale = px.colors.sequential.Reds, 
            custom_data = ['Region', 'Region code', year_by_column_name_total[year]])

        fig.update_traces(
            hovertemplate = '<br>'.join([
                'Region: %{customdata[0]}', 
                'Region code: %{customdata[1]}',
                '<b>Magnitude of poor families estimation: %{customdata[2]:,}</b>' ]), )

        fig.update_geos(fitbounds = 'locations', visible = False,)
        
        figure_update_layout(fig)
        
        save_fig_binary(figure = fig, file_name = file_name, folder_name = folder_name)
        return fig
    
@st.cache_data
def get_plot_by_province(dataframe, year: str, region_name: str):
    region_code = region_name_by_region_code[region_name]
    file_name = f'by_region_{region_code}_{year}'
    folder_name = 'provinces'

    fig = load_fig_binary(file_name = file_name, folder_name = folder_name)
    if fig is not None:
        return fig
    else:
        dataframe = dataframe.loc[dataframe['Region'].isin([region_name])]

        geojson_path = 'data/geojson'
        geojson_folder_name = 'provinces'
        geojson_file_name = f'provinces-region-{region_code.lower()}.0.01'
        geojson_file = json.load(open(rf'{geojson_path}/{geojson_folder_name}/{geojson_file_name}.json'))

        fig = px.choropleth(
            data_frame = dataframe,
            geojson = geojson_file,
            featureidkey = 'properties.ADM2_PCODE',
            locations = 'Province code',
            color = year_by_column_name[year],
            scope = 'asia',
            color_continuous_scale = px.colors.sequential.Reds, 
            custom_data = ['Province', 'Province code', year_by_column_name[year]],
            basemap_visible=False, )

        fig.update_traces(
            hovertemplate = '<br>'.join([
                'Province: %{customdata[0]}', 
                'Province code: %{customdata[1]}',
                '<b>Magnitude of poor families estimation: %{customdata[2]:,}</b>' ]), )

        fig.update_geos(fitbounds = 'locations', visible = False,)
        
        figure_update_layout(fig)

        save_fig_binary(figure = fig, file_name = file_name, folder_name = folder_name)
        return fig
    



    