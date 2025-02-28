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
        df_latest,
        lat='centroid_lat',
        lon='centroid_lng',
        scope='usa',
        color='microbusiness_density',
        size='active',
        # hover_name='county',
        # hover_data={
        #     'state': True,
        #     'microbusiness_density': ':.2f',
        #     'active': True,
        #     'median_hh_inc_2021': True,
        #     'centroid_lat': False,
        #     'centroid_lng': False
        # },
        color_continuous_scale='Viridis',
        title='US Counties Microbusiness Density'
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":50,"l":0,"b":0},
        uirevision='constant',
        hovermode=False,
    )


    return fig

def display_landing_page_map_choropleth_counties(enriched_df, geojson_file, percentile):

    percentile_filtered = enriched_df['microbusiness_density'].quantile(percentile)

    high_density_counties = enriched_df[enriched_df['microbusiness_density'] > percentile_filtered]


    # Display the filtered data
    high_density_counties

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    

    fig = px.choropleth_map(high_density_counties, geojson=geojson_file, locations='cfips', color='microbusiness_density',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )

    # fig.update_geos(showsubunits=True, subunitcolor="Black")

    return fig 

def display_landing_page_map_choropleth_states(enriched_df, geojson_file, percentile):

    percentile_filtered = enriched_df['microbusiness_density'].quantile(percentile)

    high_density_counties = enriched_df[enriched_df['microbusiness_density'] > percentile_filtered]

    # Display the filtered data
    high_density_counties

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    fig = px.choropleth_map(high_density_counties, geojson=geojson_file, locations='state_id', 
    color='microbusiness_density',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )

    # fig.update_geos(showsubunits=True, subunitcolor="Black")

    return fig 

def display_state_level_map(enriched_df, geojson_file):

    center_lat = enriched_df['centroid_lat'].mean()
    center_lon = enriched_df['centroid_lng'].mean()

    # Filter the data for the specific state
    fig = px.choropleth_map(enriched_df, geojson=geojson_file, locations='cfips', color='microbusiness_density',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": center_lat, "lon": center_lon},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    
    return fig


def display_county_level_map(enriched_df, geojson_file):
    return
