from dash import Dash, dcc, callback, Output, Input, html, dash_table
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import numpy as np
import json

from .components.data_processing import generate_df
from .components.charts import update_density_chart_details, update_income_chart_details

# Generate and unpack processed data
data = generate_df()
df = data["df"]
unique_states = data["unique_states"]
state_county_mapping = data["state_county_mapping"]
total_microbusinesses = data["total_microbusinesses"]
weighted_microbusiness_density = data["weighted_microbusiness_density"]
median_income = data["median_income"]
numeric_columns = data["numeric_columns"]

from .components.filters import create_filters
from .components.sidebar import create_sidebar

from .components.map_view import (
        display_landing_page_map_choropleth_counties,
        display_state_level_map,
        display_county_level_map,
        fix_cfips
    )

# Load geojson files
with open("data/raw/us-states.json") as f:
    states_geojson = json.load(f)

with open("data/raw/geojson-counties-fips.json") as f:
    counties_geojson = json.load(f)

#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#initialize app variables
title = [html.H1('SMBFinder - Explore Microbusinesses around the United States'), html.Br()]

filter_state, filter_county, filter_column = create_filters(unique_states, numeric_columns)
global_metrics = create_sidebar(total_microbusinesses, weighted_microbusiness_density, median_income)

map = dcc.Graph(id='map-placeholder', style={'height': '550px', 'width': '100%'})

chart_SMB_density = [
    dvc.Vega(id='density-placeholder', spec={'height': '230px'})  
]          

chart_med_income = [
    dvc.Vega(id='income-placeholder', style={'height': '230px'})
]

card_sellability = dbc.Card(id = "sellability")

card_growth = dbc.Card(id = "growth")

card_hireability = dbc.Card(id = "hireability")

end_credits = html.Div([
    html.Br(),
    html.H6("App allowing user to explore MicroBusiness density across the US, and derive key metrics used in deciding where to launch their next venture", style={'marginBottom': '5px', 'fontSize': '16px'}),
    html.H6("Created by: Anna Nandar, Dongchun Chen, Jiayi Li, Marek Boulerice", style={'marginBottom': '5px', 'fontSize': '10px'}),
    html.H6("Repo: https://github.com/UBC-MDS/DSCI-532_2025_26_SMBFinder", style={'marginBottom': '5px', 'fontSize': '10px'}),
    html.H6("Latest Deployment: 2025/03/01", style={'marginBottom': '5px', 'fontSize': '10px'}),
])

#app layout
app.layout = dbc.Container([
        dbc.Row(dbc.Col(title)),
        dbc.Row([
                dbc.Col(
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                [
                                    global_metrics
                                ],
                                label = "USA"
                            ),
                            dbc.Tab(
                                [
                                    dbc.Row(card_sellability),
                                    dbc.Row(card_growth),
                                    dbc.Row(card_hireability),
                                ],
                                label = "County"
                            )
                        ]
                    ), md = 3, style={'marginTop': '30px'}),
                dbc.Col([
                    dbc.Row([
                            dbc.Col(filter_state),
                            dbc.Col(filter_county),
                            dbc.Col(filter_column),  # Add the new dropdown here
                    ]),
                    # Put map in its own Row for proper alignment
                    dbc.Row(dbc.Col(map, className="p-0")),  # Added p-0 class to remove padding
                ], md=9),
        ]),

        # Add this new row for the data table
        dbc.Row([
            dbc.Col([
                html.H4("Filtered Data"),
                html.Div(id='filtered-data-table')
            ])
        ]),

        dbc.Row(
            [
                dbc.Col(chart_SMB_density),
                dbc.Col(chart_med_income),
            ]
        ), 
        dbc.Row(end_credits)
])

@app.callback(
    Output("state-dropdown", "options"),
    Output("county-dropdown", "options"),
    Output("county-dropdown", "disabled"),
    Input("state-dropdown", "value")
)
def limit_selections(selected_states):
    """Limit state selection to 3 and allow multiple counties only if one state is chosen."""

    # Ensure state selection is limited to 3
    updated_state_options = [
        {"label": state, "value": state, "disabled": selected_states and len(selected_states) >= 3}
        for state in unique_states
    ]

    available_counties = []
    county_disabled = True  # Default: disabled

    if selected_states and len(selected_states) == 1:
        # Ensure the selected state exists in the mapping
        available_counties = state_county_mapping.get(selected_states[0], [])
        county_disabled = False  # Enable dropdown if exactly 1 state is selected

    updated_county_options = [
        {"label": county, "value": county, "disabled": False}
        for county in available_counties
    ]

    return updated_state_options, updated_county_options, county_disabled

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

    if not county:
        sellability_empty = [
            dbc.CardHeader("Sellability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("County percentile median income", style={'fontSize': '12px'})
        ]
        growth_empty = [
            dbc.CardHeader("Growth index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("county percentile for average yealy Microbusiness growth",style={'fontSize': '12px'})
        ]
        hireability_empty = [
            dbc.CardHeader("Hireability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("County percentile for percent of population with bachelors degree", style={'fontSize': '12px'})
        ]
        return sellability_empty, growth_empty, hireability_empty
    
    #creating df of filtered counties at latest date
    latest_date = "2022-10-01"
    condition = "state in @state & county in @county & first_day_of_month == @latest_date"
    filtered_df = df.query(condition)

    #create index paragraph lists and populate with filtered df
    sell_list = []
    growth_list = []
    hire_list = []
    for i in range(len(filtered_df)):
        county = filtered_df.iloc[i]
        sell_list.append(html.P(f"{county['county']} : {county['sellability_index']}"))
        growth_list.append(html.P(f"{county['county']} : {county['growth_index']}"))
        hire_list.append(html.P(f"{county['county']} : {county['hireability_index']}"))


    sellability_card = [
        dbc.CardHeader("Sellability index"),
        dbc.CardBody(sell_list),
        dbc.CardFooter("County percentile median income", style={'fontSize': '12px'})
    ]
    growth_card = [
        dbc.CardHeader("Growth index"),
        dbc.CardBody(growth_list),
        dbc.CardFooter("county percentile for average yealy Microbusiness growth", style={'fontSize': '12px'})
    ]
    hireability_card = [
        dbc.CardHeader("Hireability index"),
        dbc.CardBody(hire_list),
        dbc.CardFooter("County percentile for percent of population with bachelors degree", style={'fontSize': '12px'})
    ]
    return sellability_card, growth_card, hireability_card

if __name__ == '__main__':
    app.run_server(debug=False, port=8001, host='127.0.0.1')