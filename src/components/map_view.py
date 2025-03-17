import plotly.express as px
import pandas as pd
import time  # Add this at the top with other imports


COLOR_SCALE = "thermal"

def get_hover_data():
    return {
        'state': True,
        'county': True,
        'microbusiness_density': ':.2f',
        'active': True,
        'median_hh_inc_2021': True,
        'centroid_lat': False,
        'centroid_lng': False,
        'sellability_index': ':.2f',
        'hireability_index': ':.2f',
        'growth_index': ':.2f'
    }

def get_labels():
    return {
        'microbusiness_density': 'Microbusiness Density',
        'cfips_fixed': 'County FIPS Code',
        'county': 'County',
        'state': 'State',
        'active': 'Active Microbusinesses',
        'median_hh_inc_2021': 'Median Household Income (2021)',
        'sellability_index': 'Sellability Index',
        'hireability_index': 'Hireability Index',
        'growth_index': 'Growth Index'
    }

def get_tooltip_descriptions():
    return {
        'microbusiness_density': 'Microbusinesses per 100 people over the age of 18',
        'active': 'Raw count of microbusinesses in the county',
        'median_hh_inc_2021': 'Median household income (inflation-adjusted to 2021 dollars)',
        'sellability_index': 'Index measuring potential for business sales',
        'hireability_index': 'Index measuring potential for hiring employees',
        'growth_index': 'Index measuring potential for business growth'
    }

def get_legend_margin():
    return {"r":0,"t":0,"l":0,"b":0}

def _configure_colorbar(fig, color_col):
    """Helper function to configure the colorbar based on the color column."""
    # Get the display name from the labels dictionary, or use a formatted version of the column name
    display_name = get_labels().get(color_col, color_col.replace('_', ' ').title())
    
    # Don't show description.
    title_text = display_name
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text=title_text,
                font=dict(size=14)
            ),
            thicknessmode="pixels", 
            thickness=25,
            lenmode="fraction", 
            len=0.8,
            ticks="outside",
            ticklen=5,
            outlinewidth=1,
            outlinecolor="black",
            x=1.02,
            y=0.5
        ),
        margin=get_legend_margin()
    )
    return fig

def _create_base_choropleth(data_df, geojson_file, location_col, color_col, zoom, opacity):
    """Create a base choropleth map with common settings."""
    start_time = time.time()
    
    center_lat = data_df['centroid_lat'].mean()
    center_lon = data_df['centroid_lng'].mean()

    if color_col == 'microbusiness_density':
        fig = px.choropleth_map(
            data_df, 
            geojson=geojson_file, 
            locations=location_col, 
            color=color_col,
            color_continuous_scale=COLOR_SCALE,
            map_style="carto-positron",
            zoom=zoom, 
            center={"lat": center_lat, "lon": center_lon},
            opacity=opacity,
            # range_color=(0, 100),
            labels=get_labels(),
            hover_data=get_hover_data()
        )
    
    else:
        fig = px.choropleth_map(
            data_df, 
            geojson=geojson_file, 
            locations=location_col, 
            color=color_col,
            color_continuous_scale=COLOR_SCALE,
            map_style="carto-positron",
            zoom=zoom, 
            center={"lat": center_lat, "lon": center_lon},
            opacity=opacity,
            range_color=(0, 100),
            labels=get_labels(),
            hover_data=get_hover_data()
        )
    
    fig = _configure_colorbar(fig, color_col)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Add timing information to the figure's layout title
    fig.update_layout(
        title=dict(
            text=f"Map Generation Time: {execution_time:.2f}s",
            x=0.01,  # Position at the left
            y=0.99,  # Position at the top
            xanchor='left',
            yanchor='top',
            font=dict(size=12)
        )
    )
    
    return fig

def display_landing_page_map_choropleth_counties(enriched_df, geojson_file, percentile, location_col, color_col):
    percentile_filtered = enriched_df[color_col].quantile(percentile)
    high_density_counties = enriched_df[enriched_df[color_col] > percentile_filtered]
    
    fig = _create_base_choropleth(
        high_density_counties, 
        geojson_file, 
        location_col, 
        color_col, 
        zoom=3, 
        opacity=0.5
    )

    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )

    return fig 

def display_state_level_map(enriched_df, geojson_file, location_col, color_col):
    if enriched_df['state'].nunique() > 1:
        return _create_base_choropleth(
            enriched_df, 
            geojson_file, 
            location_col, 
            color_col, 
            zoom=3, 
            opacity=0.5
        )
    else:
        return _create_base_choropleth(
            enriched_df, 
            geojson_file, 
            location_col, 
            color_col, 
            zoom=5, 
            opacity=0.5
        )

def display_county_level_map(enriched_df, geojson_file, location_col, color_col):

    if enriched_df['county'].nunique() > 1:
        return _create_base_choropleth(
                enriched_df, 
                geojson_file, 
                location_col, 
                color_col, 
                zoom=6, 
                opacity=0.5
            )
    else:
        return _create_base_choropleth(
            enriched_df, 
            geojson_file, 
            location_col, 
            color_col, 
            zoom=8, 
            opacity=0.5
        )

def fix_cfips(cfips):
    return str(cfips).zfill(5)

def update_map_display(latest_map_data, selected_state, selected_county, selected_column, counties_geojson):
    """
    Updates the map based on selected filters.
    
    Args:
        latest_map_data: DataFrame with the latest data for mapping
        selected_state: String or list of selected states
        selected_county: String or list of selected counties
        selected_column: Column to display in the choropleth
        counties_geojson: GeoJSON data for counties
    
    Returns:
        Plotly figure object
    """
    column_to_display = selected_column if selected_column else 'growth_index'
    
    if selected_state:
        if isinstance(selected_state, list):
            filtered_df = latest_map_data[latest_map_data["state"].isin(selected_state)]
        else:
            filtered_df = latest_map_data[latest_map_data["state"] == selected_state]
    else:
        filtered_df = latest_map_data
        
    if selected_county:
        if isinstance(selected_county, list):
            filtered_df = filtered_df[filtered_df["county"].isin(selected_county)]
        else:
            filtered_df = filtered_df[filtered_df["county"] == selected_county]
    
    if selected_county:
        fig = display_county_level_map(filtered_df, counties_geojson, 'cfips_fixed', column_to_display)
    elif selected_state:
        fig = display_state_level_map(filtered_df, counties_geojson, 'cfips_fixed', column_to_display)
    else:
        fig = display_landing_page_map_choropleth_counties(filtered_df, counties_geojson, 0.7, 'cfips_fixed', column_to_display)
    
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=True,
        margin={"r":150, "t":20, "l":20, "b":20},
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig