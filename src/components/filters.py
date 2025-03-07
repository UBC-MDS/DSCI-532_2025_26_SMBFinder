from dash import dcc, html
import dash_bootstrap_components as dbc

def create_filters(unique_states, numeric_columns):
    """Creates filter dropdowns and takes in required variables from app.py"""

    filter_state = dbc.Col([
        dbc.Label("Select a State"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{"label": state, "value": state} for state in unique_states], 
            placeholder='Select up to 3 States',
            multi=True,
            style={'width': '200px', 'fontSize': '15px'}
        ),
    ])

    filter_county = dbc.Col([
        dbc.Label("Select a County"),
        dcc.Dropdown(
            id='county-dropdown',
            placeholder='Select up to 3 Counties',
            multi=True,
            style={'width': '260px', 'fontSize': '15px'},
            disabled=True  # Disabled initially
        ),
    ])

    filter_column = dbc.Col([
        dbc.Label("Color by"),
        dcc.Dropdown(
            id='column-dropdown',
            options=[{"label": col.replace('_', ' ').title(), "value": col} for col in numeric_columns],
            value='growth_index',
            style={'width': '215px', 'fontSize': '15px'}
        ),
    ])

    return filter_state, filter_county, filter_column