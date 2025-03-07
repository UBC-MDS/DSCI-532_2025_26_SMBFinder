import plotly.express as px
import pandas as pd

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
    center_lat = data_df['centroid_lat'].mean()
    center_lon = data_df['centroid_lng'].mean()
    
    fig = px.choropleth_map(
        data_df, 
        geojson=geojson_file, 
        locations=location_col, 
        color=color_col,
        color_continuous_scale="Blackbody",
        map_style="carto-positron",
        zoom=zoom, 
        center={"lat": center_lat, "lon": center_lon},
        opacity=opacity,
        range_color=(0, 100),
        labels=get_labels(),
        hover_data=get_hover_data()
    )
    
    return _configure_colorbar(fig, color_col)

def display_landing_page_map_choropleth_counties(enriched_df, geojson_file, percentile, location_col, color_col):
    percentile_filtered = enriched_df['microbusiness_density'].quantile(percentile)
    high_density_counties = enriched_df[enriched_df['microbusiness_density'] > percentile_filtered]
    
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