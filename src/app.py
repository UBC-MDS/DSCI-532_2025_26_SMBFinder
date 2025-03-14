from dash import Dash, Output, Input, html
import dash_bootstrap_components as dbc
import json

from .components.data_processing import generate_df
from .components.layout import create_layout
from .components.filters import limit_selections
from .components.charts import update_density_chart_details, update_income_chart_details
from .components.map_view import (
        display_landing_page_map_choropleth_counties,
        display_state_level_map,
        display_county_level_map,
        fix_cfips
    )
from .components.BI_cards import update_cards

# Generate and unpack processed data
data = generate_df()
df = data["df"]
unique_states = data["unique_states"]
state_county_mapping = data["state_county_mapping"]
total_microbusinesses = data["total_microbusinesses"]
weighted_microbusiness_density = data["weighted_microbusiness_density"]
median_income = data["median_income"]
numeric_columns = data["numeric_columns"]

# Load geojson files
with open("data/raw/us-states.json") as f:
    states_geojson = json.load(f)

with open("data/raw/geojson-counties-fips.json") as f:
    counties_geojson = json.load(f)

#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"])
app.title="SMBFinder"
server = app.server

# Set up layout (imported from `layout.py`)
app.layout = create_layout(unique_states, numeric_columns, total_microbusinesses, weighted_microbusiness_density, median_income)

@app.callback(
    Output("state-dropdown", "options"),
    Output("county-dropdown", "options"),
    Output("county-dropdown", "disabled"),
    Input("state-dropdown", "value"),
    Input("county-dropdown", "value")
)
def update_filter_options(selected_states, selected_counties):
    return limit_selections(selected_states, unique_states, state_county_mapping, selected_counties)

@app.callback(
    Output("map-placeholder", "figure"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value"),
     Input("column-dropdown", "value")]  
)
def update_map(selected_state, selected_county, selected_column):
    global df
    
    temp_df = df.copy()
    temp_df = temp_df.sort_values('first_day_of_month').groupby('cfips').last().reset_index()
    
    if selected_state:
        if isinstance(selected_state, list):
            filtered_df = temp_df[temp_df["state"].isin(selected_state)]
        else:
            filtered_df = temp_df[temp_df["state"] == selected_state]
    else:
        filtered_df = temp_df
        
    if selected_county:
        if isinstance(selected_county, list):
            filtered_df = filtered_df[filtered_df["county"].isin(selected_county)]
        else:
            filtered_df = filtered_df[filtered_df["county"] == selected_county]
    
    filtered_df['cfips_fixed'] = filtered_df['cfips_fixed'].apply(fix_cfips)

    column_to_display = selected_column if selected_column else 'growth_index'
    
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

@app.callback(
    Output("density-placeholder", "spec"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value")]
)
def update_density_chart(selected_state=None, selected_county=None):

    return update_density_chart_details(df, selected_state, selected_county)
    
@app.callback(
    Output("income-placeholder", "spec"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value")]
)
def update_income_chart(selected_state=None, selected_county=None):
    
    return update_income_chart_details(df, selected_state, selected_county)

@app.callback(
    [Output("sellability", "children"),
    Output("growth", "children"),
    Output("hireability", "children")],
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value")]
)
def update_BI_cards(state, county):

    return update_cards(df, state, county)

if __name__ == '__main__':
    app.run_server(debug=False, port=8001, host='127.0.0.1')