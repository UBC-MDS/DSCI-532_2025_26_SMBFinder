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

def get_legend_margin():
    return {"r":0,"t":0,"l":0,"b":0}


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
                title=dict(
                    text=get_tooltip_descriptions()[color_col],
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased margin for colorbar
        )
    else:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text="Microbusiness Density",
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased margin for colorbar
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
    ))

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
    
    # Add tooltip description to the colorbar title
    if color_col in get_tooltip_descriptions():
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text=get_tooltip_descriptions()[color_col],
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased from 100 to 150
        )
    else:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text="Microbusiness Density",
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased margin for colorbar
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
            coloraxis_colorbar=dict(
                title=dict(
                    text=get_tooltip_descriptions()[color_col],
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased from 100 to 150
        )
    else:
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=dict(
                    text="Microbusiness Density",
                    font=dict(size=14)
                ),
                # Enhanced colorbar settings
                thicknessmode="pixels", 
                thickness=25,
                lenmode="fraction", 
                len=0.8,
                ticks="outside",
                ticklen=5,
                outlinewidth=1,
                outlinecolor="black",
                x=1.02,  # Position slightly outside the plot area
                y=0.5    # Center vertically
            ),
            # Significantly increase right margin to make room for colorbar
            margin=get_legend_margin()  # Increased margin for colorbar
        )
    
    return fig

def fix_cfips(cfips):
    return str(cfips).zfill(5)