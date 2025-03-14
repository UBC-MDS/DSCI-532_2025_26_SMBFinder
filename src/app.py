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
        fix_cfips,
        update_map_display
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

def generate_latest_map_data(df):
    return df.sort_values('first_day_of_month').groupby('cfips').last().reset_index()

latest_map_data = generate_latest_map_data(df)

@app.callback(
    Output("map-placeholder", "figure"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value"),
     Input("column-dropdown", "value")]  
)
def update_map(selected_state, selected_county, selected_column):
    return update_map_display(latest_map_data, selected_state, selected_county, selected_column, counties_geojson)

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