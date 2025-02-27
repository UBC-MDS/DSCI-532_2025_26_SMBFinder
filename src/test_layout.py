from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc

#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#initialize app variables
title = [html.H1('SMBFinder - Explore Microbusinesses around the United States'), html.Br()]

filter_state = [
    dbc.Label("Select a State"),
    dcc.Dropdown(id='state-dropdown', placeholder='Select a State', style={'width': '200px'}),
]

filter_county = [
    dbc.Label("Select a County"),
    dcc.Dropdown(id='county-dropdown', placeholder='Select a County', style={'width': '200px'}),
]

global_metrics = html.Div([
            html.H4("USA-wide metrics", style={'fontSize': '18px', 'marginBottom': '30px'}),
            html.Button("# Number of Business in total", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'}),
            html.Br(),
            html.Button("# Number of Average Population", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'}),
            html.Br(),
            html.Button("# Average household income", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'})
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'border': '1px solid black', 'padding': '20px', 'height': '500px'}
)

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
                dbc.Col(global_metrics, md = 4),
                dbc.Col([
                    dbc.Row([
                            dbc.Col(filter_state),
                            dbc.Col(filter_county),
                    ]),
                    dbc.Row(map)
                ], md=8),
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



# Get underlying Flask server
server = app.server

if __name__ == '__main__':
    app.run(debug=True)