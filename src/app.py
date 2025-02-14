from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.Label("Select a State"),
        dcc.Dropdown(id='state-dropdown', placeholder='Select a State', style={'width': '200px'}),
        html.Label("Select a County"),
        dcc.Dropdown(id='county-dropdown', placeholder='Select a County', style={'width': '200px'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H4("Explore the Microbusiness in USA", style={'fontSize': '18px', 'marginBottom': '30px'}),
            html.Button("# Number of Business in total", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'}),
            html.Br(),
            html.Button("# Number of Average Population", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'}),
            html.Br(),
            html.Button("# Average household income", style={'width': '100%', 'marginBottom': '30px', 'padding': '20px'})
        ], style={'width': '18%', 'display': 'inline-block', 'verticalAlign': 'top', 'border': '1px solid black', 'padding': '20px', 'height': '500px'}),
        
        html.Div([
            dcc.Graph(id='map-placeholder', style={'height': '550px'})
        ], style={'width': '70%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'alignItems': 'center'}),

    html.Div([
        html.Div([
            html.H5("Median Income Level in this overall/State/County", style={'textAlign': 'center', 'fontSize': '20px'}),
            dcc.Graph(id='income-placeholder', style={'height': '230px'})
        ], style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            html.H5("Hireability vs Business Growth in this overall/State/County", style={'textAlign': 'center', 'fontSize': '20px'}),
            dcc.Graph(id='hireability-placeholder', style={'height': '230px'})
        ], style={'width': '40%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)