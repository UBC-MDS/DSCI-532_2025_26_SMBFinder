import pandas as pd
from dash import Dash, Output, Input, html
import dash_bootstrap_components as dbc

def update_cards(df, state, county):
    if not county:
        sellability_empty = [
            dbc.CardHeader("Sellability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("Percentile - median income", style={'fontSize': '10px'})
        ]
        growth_empty = [
            dbc.CardHeader("Growth index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("Percentile - yearly Microbusiness growth", style={'fontSize': '10px'})
        ]
        hireability_empty = [
            dbc.CardHeader("Hireability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("Percentile - pop. % with bachelors degree", style={'fontSize': '10px'})
        ]
        return sellability_empty, growth_empty, hireability_empty
    
    #creating df of filtered counties at latest date
    latest_date = "2022-10-01"
    condition = "state in @state & county in @county & first_day_of_month == @latest_date"
    filtered_df = df.query(condition)

    #create index paragraph lists and populate with filtered df
    sell_list = []
    growth_list = []
    hire_list = []
    for i in range(len(filtered_df)):
        county = filtered_df.iloc[i]
        sell_list.append(html.P(f"{county['county']} : {county['sellability_index']}%"))
        growth_list.append(html.P(f"{county['county']} : {county['growth_index']}%"))
        hire_list.append(html.P(f"{county['county']} : {county['hireability_index']}%"))


    sellability_card = [
        dbc.CardHeader("Sellability index"),
        dbc.CardBody(sell_list),
        dbc.CardFooter("Percentile - median income", style={'fontSize': '10px'})
    ]
    growth_card = [
        dbc.CardHeader("Growth index"),
        dbc.CardBody(growth_list),
        dbc.CardFooter("Percentile - yearly Microbusiness growth", style={'fontSize': '10px'})
    ]
    hireability_card = [
        dbc.CardHeader("Hireability index"),
        dbc.CardBody(hire_list),
        dbc.CardFooter("Percentile - pop. % with bachelors degree", style={'fontSize': '10px'})
    ]
    return sellability_card, growth_card, hireability_card
