import plotly.express as px
import pandas as pd

# Define consistent hover data and labels to be used across all map functions
def get_hover_data():
    return {
        'state': True,
        'county': True,
        'microbusiness_density': ':.2f',
        'active': True,
        'median_hh_inc_2021': True,
        'pct_bb_2021': ':.1f',
        'pct_college_2021': ':.1f',
        'pct_foreign_born_2021': ':.1f',
        'pct_it_workers_2021': ':.1f',
        'centroid_lat': False,
        'centroid_lng': False
    }

def get_labels():
    return {
        'microbusiness_density': 'Microbusiness Density',
        'cfips_fixed': 'County FIPS Code',
        'county': 'County',
        'state': 'State',
        'active': 'Active Microbusinesses',
        'median_hh_inc_2021': 'Median Household Income (2021)',
        'pct_bb_2021': 'Broadband Access %',
        'pct_college_2021': 'College Education %',
        'pct_foreign_born_2021': 'Foreign Born Population %',
        'pct_it_workers_2021': 'IT Industry Workers %'
    }

def get_tooltip_descriptions():
    return {
        'microbusiness_density': 'Microbusinesses per 100 people over the age of 18',
        'active': 'Raw count of microbusinesses in the county',
        'median_hh_inc_2021': 'Median household income (inflation-adjusted to 2021 dollars)',
        'pct_bb_2021': 'Percentage of households with access to broadband of any type',
        'pct_college_2021': 'Percentage of population over age 25 with a 4-year college degree',
        'pct_foreign_born_2021': 'Percentage of population born outside of the United States',
        'pct_it_workers_2021': 'Percentage of workforce employed in information related industries'
    }

def display_landing_page_map_dots(enriched_df):


    """
    (1)
    Initially, start with the map of the US. 
    - Maybe general Choropleth
    - Year slider on the top, Choropleth by the average microbusiness density

    OR
    - General map of the US. Center points of the counties are shown. So, each county is condensed into the middle point.
    - Plot all the points on the map where the county has a microbusiness density above average.
    - Year slider on the bottom.

    (2)
    All the geojson is in county level. 
    - Can it be Choropleth by county? 
    - So, filter by State, so that state is highlighted, else is grey. Then, a Choropleth by county for that state only.


    Stretch goals:
    - Have map to be selectable, so when a map is clicked, the selection propagates to the charts below.


    Implementation:
    Input: microbusiness dataset, geojson file by county

    1. 

    Output: Map of the US. 



    """

    fig = px.scatter_geo(
        enriched_df,
        lat='centroid_lat',
        lon='centroid_lng',
        scope='usa',
        color='microbusiness_density',
        size='active',
        hover_name='county',
        hover_data=get_hover_data(),
        color_continuous_scale='Viridis',
        labels=get_labels(),
        title='US Counties Microbusiness Density'
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":50,"l":0,"b":0},
        uirevision='constant',
        hovermode='closest',
        coloraxis_colorbar=dict(
            title=get_tooltip_descriptions()['microbusiness_density']
        )
    )


    return fig

def display_landing_page_map_choropleth_counties(enriched_df, geojson_file, percentile, location_col, color_col):

    percentile_filtered = enriched_df['microbusiness_density'].quantile(percentile)

    high_density_counties = enriched_df[enriched_df['microbusiness_density'] > percentile_filtered]


    # Display the filtered data
    # high_density_counties

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    
    fig = px.choropleth_map(high_density_counties, geojson=geojson_file, locations=location_col, color=color_col,
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels=get_labels(),
                           hover_data=get_hover_data()
                          )

    # fig.update_geos(showsubunits=True, subunitcolor="Black")
    
    # Add tooltip description to the colorbar title
    if color_col in get_tooltip_descriptions():
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=get_tooltip_descriptions()[color_col]
            )
        )

    return fig 

def display_landing_page_map_choropleth_states(enriched_df, geojson_file, percentile, location_col, color_col):

    percentile_filtered = enriched_df[color_col].quantile(percentile)

    high_density_counties = enriched_df[enriched_df[color_col] > percentile_filtered]

    # Display the filtered data
    # high_density_counties

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    fig = px.choropleth_map(high_density_counties, geojson=geojson_file, locations=location_col, 
    color=color_col,
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels=get_labels(),
                           hover_data=get_hover_data()
                          )

    # fig.update_geos(showsubunits=True, subunitcolor="Black")
    
    # Add tooltip description to the colorbar title
    if color_col in get_tooltip_descriptions():
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=get_tooltip_descriptions()[color_col]
            )
        )

    return fig 

def display_state_level_map(enriched_df, geojson_file, location_col, color_col):

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    # Filter the data for the specific state
    fig = px.choropleth_map(enriched_df, geojson=geojson_file, locations=location_col, color=color_col,
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels=get_labels(),
                           hover_data=get_hover_data()
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # Add tooltip description to the colorbar title
    if color_col in get_tooltip_descriptions():
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=get_tooltip_descriptions()[color_col]
            )
        )
    
    return fig


def display_county_level_map(enriched_df, geojson_file, location_col, color_col):
    
    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    fig = px.choropleth_map(enriched_df, geojson=geojson_file, locations=location_col, color=color_col,
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=8, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.8,
                           labels=get_labels(),
                           hover_data=get_hover_data()
                          )
    
    # Add tooltip description to the colorbar title
    if color_col in get_tooltip_descriptions():
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title=get_tooltip_descriptions()[color_col]
            )
        )
    else:
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title="Microbusiness Density"
            )
        )
    
    return fig



def fix_cfips(cfips):
    return str(cfips).zfill(5)