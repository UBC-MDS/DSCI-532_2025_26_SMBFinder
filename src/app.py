from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

# data wrangling for filter & sidebar
df = pd.read_csv("data/processed/smb_enriched.csv")  

unique_states = sorted(df["state"].unique())
state_county_mapping = df.groupby("state")["county"].unique().apply(list).to_dict()

total_microbusinesses = df["active"].sum()  
df["adult_population"] = (df["active"] / df["microbusiness_density"]) * 100
weighted_microbusiness_density = (df["microbusiness_density"] * df["adult_population"]).sum() / df["adult_population"].sum()

latest_year = "2021"  
df = df.sort_values(by=f"median_hh_inc_{latest_year}")  
df["cumulative_population"] = df["adult_population"].cumsum()  
total_population = df["adult_population"].sum()
median_income = df[df["cumulative_population"] >= total_population / 2][f"median_hh_inc_{latest_year}"].iloc[0]

#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#initialize app variables
title = [html.H1('SMBFinder - Explore Microbusinesses around the United States'), html.Br()]

filter_state = [
    dbc.Label("Select a State"),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{"label": state, "value": state} for state in unique_states], 
        placeholder='Select a State',
        style={'width': '200px'}
    ),
]

filter_county = [
    dbc.Label("Select a County"),
    dcc.Dropdown(id='county-dropdown', placeholder='Select a County', style={'width': '200px'}),
]

global_metrics = html.Div([
    html.H4("USA-wide Metrics", style={'textAlign': 'center', 'fontSize': '21px', 'marginBottom': '25px'}),

    html.Div([
        html.H6("Total Microbusinesses", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #ccc', 'width': '80%', 'margin': '10px auto'}),  
        html.P(f"{total_microbusinesses:,.0f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#f8f9fa', 'padding': '12px', 'borderRadius': '10px', 'marginBottom': '25px'}),

    html.Div([
        html.H6("Avg. Microbusiness Density", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #ccc', 'width': '80%', 'margin': '10px auto'}),  
        html.P(f"{weighted_microbusiness_density:.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#f8f9fa', 'padding': '12px', 'borderRadius': '10px', 'marginBottom': '25px'}),

    html.Div([
        html.H6("Median Household Income", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #ccc', 'width': '80%', 'margin': '10px auto'}),  
        html.P(f"${median_income:,.0f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#f8f9fa', 'padding': '12px', 'borderRadius': '10px', 'marginBottom': '25px'}),

], style={'border': '2px solid black', 'padding': '15px', 'borderRadius': '10px', 'width': '100%'})

map = dcc.Graph(id='map-placeholder', style={'height': '550px'})

chart_SMB_density = [
    dbc.Label("Small Business density vs time in this overall/State/County", style={'textAlign': 'center', 'fontSize': '20px'}),
    dcc.Graph(id='density-placeholder', style={'height': '230px'})
]       

chart_med_income = [
    dbc.Label("Median income vs time in this overall/State/County", style={'textAlign': 'center', 'fontSize': '20px'}),
    dcc.Graph(id='income-placeholder', style={'height': '230px'})
]

card_sellability = dbc.Card([
    dbc.CardHeader('Sellability index'), 
    dbc.CardBody('placeholder sellability value'),
])  

card_competition = dbc.Card([
    dbc.CardHeader('competition index'), 
    dbc.CardBody('placeholder competition value'),
])

card_hireability = dbc.Card([
    dbc.CardHeader('hireability index'), 
    dbc.CardBody('placeholder hireability value'),
])


#app layout
app.layout = dbc.Container([
        dbc.Row(dbc.Col(title)),
        dbc.Row([
                dbc.Col(global_metrics, md = 3, style={'marginTop': '30px'}),
                dbc.Col([
                    dbc.Row([
                            dbc.Col(filter_state),
                            dbc.Col(filter_county),
                    ]),
                    dbc.Row(map)
                ], md=9),
        ]),

        dbc.Row(
            [
                dbc.Col(chart_SMB_density),
                dbc.Col(chart_med_income),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card_sellability),
                dbc.Col(card_competition),
                dbc.Col(card_hireability),
            ]
        ),
])

@app.callback(
    Output("county-dropdown", "options"),
    Input("state-dropdown", "value")
)
def update_county_dropdown(selected_state):
    if not selected_state:
        return []
    return [{"label": county, "value": county} for county in state_county_mapping[selected_state]]  


if __name__ == '__main__':
    app.run(debug=False)