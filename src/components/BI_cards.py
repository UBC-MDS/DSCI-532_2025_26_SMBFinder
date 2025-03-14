import pandas as pd
from dash import Dash, Output, Input, html
import dash_bootstrap_components as dbc

def update_cards(df, state, county):
    """Generate styled metric cards with clean background & no border."""
    
    card_style = {
        'backgroundColor': '#D7EBF6', 
         'borderRadius': '5px',  
        'border': 'none',  
        'boxShadow': 'none'
    }

    header_footer_style = {
        'backgroundColor': '#D7EBF6'
    }

    if not county:
        sellability_empty = dbc.Card(
            [
                dbc.CardHeader("Sellability index", style=header_footer_style),
                dbc.CardBody(html.P("[Please select a county]", style={'fontSize': '15px'})),
                dbc.CardFooter("Percentile - median income", style={**header_footer_style, 'fontSize': '11px'})
            ],
            style=card_style  
        )

        growth_empty = dbc.Card(
            [
                dbc.CardHeader("Growth index", style=header_footer_style),
                dbc.CardBody(html.P("[Please select a county]", style={'fontSize': '15px'})),
                dbc.CardFooter("Percentile - yearly Microbusiness growth", style={**header_footer_style, 'fontSize': '11px'})
            ],
            style=card_style  
        )

        hireability_empty = dbc.Card(
            [
                dbc.CardHeader("Hireability index", style=header_footer_style),
                dbc.CardBody(html.P("[Please select a county]", style={'fontSize': '15px'})),
                dbc.CardFooter("Percentile - pop. % with bachelors degree", style={**header_footer_style, 'fontSize': '11px'})
            ],
            style=card_style 
        )

        return sellability_empty, growth_empty, hireability_empty

    # Creating df of filtered counties at latest date
    latest_date = "2022-10-01"
    condition = "state in @state & county in @county & first_day_of_month == @latest_date"
    filtered_df = df.query(condition)

    # Create index paragraph lists and populate with filtered df
    sell_list = [html.P(f"{county['county']} : {county['sellability_index']}%") for _, county in filtered_df.iterrows()]
    growth_list = [html.P(f"{county['county']} : {county['growth_index']}%") for _, county in filtered_df.iterrows()]
    hire_list = [html.P(f"{county['county']} : {county['hireability_index']}%") for _, county in filtered_df.iterrows()]

    sellability_card = dbc.Card(
        [
            dbc.CardHeader("Sellability index", style=header_footer_style),
            dbc.CardBody(sell_list, style={'fontSize': '14px'}),
            dbc.CardFooter("Percentile - median income", style={**header_footer_style, 'fontSize': '11px'})
        ],
        style=card_style  
    )

    growth_card = dbc.Card(
        [
            dbc.CardHeader("Growth index", style=header_footer_style),
            dbc.CardBody(growth_list, style={'fontSize': '14px'}),
            dbc.CardFooter("Percentile - yearly Microbusiness growth", style={**header_footer_style, 'fontSize': '11px'})
        ],
        style=card_style 
    )

    hireability_card = dbc.Card(
        [
            dbc.CardHeader("Hireability index", style=header_footer_style),
            dbc.CardBody(hire_list, style={'fontSize': '14px'}),
            dbc.CardFooter("Percentile - pop. % with bachelors degree", style={**header_footer_style, 'fontSize': '11px'})
        ],
        style=card_style  
    )

    return sellability_card, growth_card, hireability_card
