from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar(total_microbusinesses, weighted_microbusiness_density, median_income):
    """Creates sidebar metrics for the dashboard."""
    return html.Div([
        html.H4("USA-wide Metrics", style={'textAlign': 'center', 'fontSize': '20px', 'marginTop': '20px', 'marginBottom': '25px'}),
        html.Div([
            html.H6("Total Microbusinesses", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"{total_microbusinesses:,.0f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'margin': '0 auto 20px', 'width': '90%'}),
        html.Div([
            html.H6("Avg. Microbusiness Density", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.P("(Microbusinesses per 100 people)", style={'fontSize': '12px', 'color': 'black', 'marginBottom': '5px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"{weighted_microbusiness_density:.2f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'margin': '0 auto 20px', 'width': '90%'}),
        html.Div([
            html.H6("Median Household Income", style={'marginBottom': '7px', 'fontSize': '17px'}),
            html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '20px auto'}),
            html.P(f"${median_income:,.0f}", style={'fontSize': '17px', 'fontWeight': 'bold', 'marginTop': '5px'})
        ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'margin': '0 auto 20px', 'width': '90%'}),
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'})

def create_county_sidebar(card_sellability, card_growth, card_hireability):
    return html.Div([
        html.H4("County Business Indices", style={'textAlign': 'center', 'fontSize': '20px', 'marginTop': '20px'}),

        # Moved description below the title
        html.P(
            "Business indices measure how the selected county performs in key metrics, compared to all counties in the US.",
            style={'textAlign': 'left', 'marginBottom': '20px', 'fontSize': '13px', 'color': "#4A4A4A", 'padding-left': '12px', 'padding-right': '12px'}
        ),

        # Adding spacing between cards
        html.Div(card_sellability, style={'padding-left': '12px', 'padding-right': '12px'}),
        html.Div(card_growth, style={'padding-left': '12px', 'padding-right': '12px', 'marginTop': '15px'}),
        html.Div(card_hireability, style={'padding-left': '12px', 'padding-right': '12px', 'marginTop': '15px'}),
    ])
