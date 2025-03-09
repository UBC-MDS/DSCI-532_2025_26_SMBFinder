from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from .filters import create_filters
from .sidebar import create_sidebar

def create_layout(unique_states, numeric_columns, total_microbusinesses, weighted_microbusiness_density, median_income):
    # Title
    title = [html.H1('SMBFinder - Explore Microbusinesses around the United States'), 
             html.Br()]

    # Filters
    filter_state, filter_county, filter_column = create_filters(unique_states, numeric_columns)

    # Sidebar
    global_metrics = create_sidebar(total_microbusinesses, weighted_microbusiness_density, median_income)

    # Map
    map_component = dcc.Graph(id='map-placeholder', style={'height': '550px', 'width': '100%'})

    # Charts
    chart_SMB_density = [dvc.Vega(id='density-placeholder', spec={'height': '230px'})]  
    chart_med_income = [dvc.Vega(id='income-placeholder', style={'height': '230px'})]

    # Business Index Cards
    card_sellability = dbc.Card(id="sellability")
    card_growth = dbc.Card(id="growth")
    card_hireability = dbc.Card(id="hireability")

    # Footer / End Credits
    end_credits = html.Div([
        html.Br(),
        html.H6("App allowing user to explore MicroBusiness density across the US, and derive key metrics used in deciding where to launch their next venture", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.H6("Created by: Anna Nandar, Dongchun Chen, Jiayi Li, Marek Boulerice", style={'marginBottom': '5px', 'fontSize': '10px'}),
        html.H6("Repo: https://github.com/UBC-MDS/DSCI-532_2025_26_SMBFinder", style={'marginBottom': '5px', 'fontSize': '10px'}),
        html.H6("Latest Deployment: 2025/03/09", style={'marginBottom': '5px', 'fontSize': '10px'}),
    ])

    # Final Layout with Tabs
    return dbc.Container([
        dbc.Row(dbc.Col(title)),
        dbc.Row([
            dbc.Col(
                dbc.Tabs(
                    [
                        dbc.Tab([global_metrics], label="USA"),
                        dbc.Tab([
                            dbc.Row(card_sellability),
                            dbc.Row(card_growth),
                            dbc.Row(card_hireability),
                        ], label="County")
                    ]
                ), md=3, style={'marginTop': '30px'}
            ),
            dbc.Col([
                dbc.Row([dbc.Col(filter_state), dbc.Col(filter_county), dbc.Col(filter_column)]),
                dbc.Row(dbc.Col(map_component, className="p-0")),  # Added p-0 class to remove padding
            ], md=9),
        ]),
        dbc.Row([dbc.Col([html.H4("Filtered Data"), html.Div(id='filtered-data-table')])]),
        dbc.Row([dbc.Col(chart_SMB_density), dbc.Col(chart_med_income)]),
        dbc.Row(end_credits)
    ])