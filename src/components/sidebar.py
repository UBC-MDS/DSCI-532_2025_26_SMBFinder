from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar(total_microbusinesses, weighted_microbusiness_density, median_income):
    """Creates sidebar metrics for the dashboard."""
    return html.Div([
        html.H4("USA-wide Metrics", style={'textAlign': 'center', 'fontSize': '20px', 'marginBottom': '25px'}),
        html.Div([
            html.H6("Total Microbusinesses", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"{total_microbusinesses:,.0f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
        html.Div([
            html.H6("Avg. Microbusiness Density", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"{weighted_microbusiness_density:.2f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
        html.Div([
            html.H6("Median Household Income", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"${median_income:,.0f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    ], style={'border': '2px solid black', 'padding': '15px', 'borderRadius': '10px', 'width': '90%'})