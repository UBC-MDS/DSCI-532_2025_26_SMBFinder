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
            style={'width': '260px', 'fontSize': '15px'}
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
            style={'width': '260px', 'fontSize': '15px'}
        ),
    ])

    return filter_state, filter_county, filter_column

def limit_selections(selected_states, unique_states, state_county_mapping, selected_counties):
    """Limit state selection to 3 and allow multiple counties only if one state is chosen (max 3 counties)."""

    # Ensure state selection is limited to 3
    updated_state_options = [
        {
            "label": state,
            "value": state,
            "disabled": (selected_states is not None and len(selected_states) >= 3) and (state not in selected_states)
        }
        for state in unique_states
    ]

    available_counties = []
    county_disabled = True  # Default: disabled

    # Check if exactly one state is selected
    if selected_states and len(selected_states) == 1:
        selected_state = selected_states[0]
        available_counties = state_county_mapping.get(selected_state, [])  # Get counties
        county_disabled = False if available_counties else True  # Enable dropdown if there are counties

    # Ensure county selection is limited to 3
    updated_county_options = [
        {
            "label": county,
            "value": county,
            "disabled": (selected_counties is not None and len(selected_counties) >= 3) and (county not in selected_counties)
        }
        for county in available_counties
    ]

    return updated_state_options, updated_county_options, county_disabled