from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from .filters import create_filters
from .sidebar import create_sidebar, create_county_sidebar

# Constants
PROJECT_GITHUB_LINK = "https://github.com/UBC-MDS/DSCI-532_2025_26_SMBFinder"
LATEST_DEPLOYMENT_DATE = "March 15, 2025"

# Navbar with About Button
navbar = dbc.NavbarSimple(
    children=[
        # GitHub Icon Button (Improved Contrast & Size)
        dbc.Button(
            html.I(className="fa-brands fa-github", style={"fontSize": "24px", "color": "black"}),  
            href=PROJECT_GITHUB_LINK,
            target="_blank",
            color="light",
            outline=True,
            style={
                "border": "0px",
                "background": "transparent",  # Remove button background
                "padding": "5px",
                "margin-right": "10px",
                "transition": "color 0.2s ease-in-out",
            },
        ),

        # About Button (Smaller & Less Bulky)
        dbc.Button(
            "About",
            id="open-about",
            color="primary",
            className="ml-2",
            style={
                "border": "0px",
                "fontSize": "15px",  # Smaller text
                "padding": "3px 7px",  # Adjust padding
                "margin-left": "5px",
                "margin-right": "20px",
                "transition": "background-color 0.2s ease-in-out",
            },
        ),
    ],
    brand="SMBFinder - Explore Microbusinesses in the US",
    brand_href="#",
    brand_style={"font-size": "30px", "margin-left": "50px", "fontWeight": "bold"},
    id="custom-navbar",
    color="#D7EBF6",
    dark=False,
    style={"border-radius": 0, "padding-right": 0, "backgroundColor": "#D7EBF6"},
    fluid=True,
)


# About Section (Initially Hidden)
about_text = html.Div(
    [
        html.P(
            "App allowing users to explore MicroBusiness density across the US and derive key metrics for launching ventures.",
            style={"marginBottom": "5px", "fontSize": "16px"},
        ),
        html.P(
            "Created by: Anna Nandar, Dongchun Chen, Jiayi Li, Marek Boulerice",
            style={"marginBottom": "5px", "fontSize": "14px"},
        ),
        html.P(f"Latest Deployment: {LATEST_DEPLOYMENT_DATE}", style={"marginBottom": "5px", "fontSize": "14px"}),
    ],
    id="about-text",
    style={
        "display": "none",  # Initially hidden
        "backgroundColor": "#D7EBF6",
        "color": "black",
        "padding-left": "50px",
        "padding-top": "10px",
        "padding-bottom": "10px",
        "border-radius": "0 0 5px 5px",
    },
)

# Function to create full layout
def create_layout(unique_states, numeric_columns, total_microbusinesses, weighted_microbusiness_density, median_income):
    # Filters
    filter_state, filter_county, filter_column = create_filters(unique_states, numeric_columns)

    # Sidebar Content (USA & County Metrics as Tabs)
    global_metrics = create_sidebar(total_microbusinesses, weighted_microbusiness_density, median_income)

    # Business Index Cards (For County)
    card_sellability = dbc.Card(id="sellability")
    card_growth = dbc.Card(id="growth")
    card_hireability = dbc.Card(id="hireability")
    county_metrics = create_county_sidebar(card_sellability, card_growth, card_hireability)

    # Sidebar with Tabs
    sidebar_content = dbc.Tabs(
        [
            dbc.Tab(global_metrics, label="USA Metrics"),
            dbc.Tab(county_metrics, label="County Metrics"),
        ],
        id="sidebar-tabs",
        style={"backgroundColor": "#F8F9FA", "padding": "10px"},
    )

    # Map Component
    map_component = dcc.Graph(id='map-placeholder', style={'height': '550px', 'width': '100%'})

    # Charts
    chart_SMB_density = [dvc.Vega(id='density-placeholder', spec={'height': '230px'})]  
    chart_med_income = dbc.Card(
        dbc.CardBody([
            dvc.Vega(id='income-placeholder', style={'width': '100%', 'height': '100%'})
        ],style={"backgroundColor": "#F8F9FA",
                 "padding": "10px",
                 "overflow": "hidden",
                 "md":"6",
                 })
    )
    
    

    # Final Layout
    return dbc.Container([
        # Navbar & About Section
        dbc.Row([navbar, about_text]),
        html.Br(),

        # Sidebar & Main Content
        dbc.Row(
            [
                # Sidebar (Full Column with Tabs)
                dbc.Col(
                    sidebar_content,
                    md=3,
                    style={"backgroundColor": "#F8F9FA", "padding": "20px", "borderRight": "1px solid #ddd"}
                ),

                # Main Content
                dbc.Col(
                    [
                        dbc.Row([dbc.Col(filter_state), dbc.Col(filter_county), dbc.Col(filter_column)]),
                        dbc.Row(dbc.Col(map_component, className="p-0")),  # Ensures proper spacing
                        html.Br(),
                        dbc.Row([
                            dbc.Col(chart_SMB_density, md=6), 
                            dbc.Col(chart_med_income, md=6),
                        ],justify="between")
                    ],
                    md=9,
                ),
            ]
        ),
    ])


# Callback to toggle About section
@callback(
    Output("about-text", "style"),
    Input("open-about", "n_clicks"),
    prevent_initial_call=True
)
def toggle_about(n_clicks):
    """Toggle visibility of About section"""
    if n_clicks and n_clicks % 2 == 1:
        return {"display": "block", "backgroundColor": "#D7EBF6", "color": "black", "padding-left": "60px", "padding-bottom": "10px",
                "border-radius": "0 0 5px 5px"}
    return {"display": "none"}
