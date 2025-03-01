from dash import Dash, dcc, callback, Output, Input, html, dash_table
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import numpy as np
import json
try:
    from components.map_view import (
        display_landing_page_map_dots,
        display_landing_page_map_choropleth_counties,
        display_state_level_map,
        display_county_level_map
    )
except ModuleNotFoundError:
    from src.components.map_view import (
        display_landing_page_map_dots,
        display_landing_page_map_choropleth_counties,
        display_state_level_map,
        display_county_level_map
    )

# data wrangling for filter & sidebar
df = pd.read_csv("data/processed/smb_enriched.csv",dtype={'cfips_fixed': str, 'cfips': str})  
df['cfips_fixed'] = df['cfips_fixed'].astype(str)
df['cfips'] = df['cfips'].astype(str)
# Load geojson files
with open("data/raw/us-states.json") as f:
    states_geojson = json.load(f)

with open("data/raw/geojson-counties-fips.json") as f:
    counties_geojson = json.load(f)

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

# Get numeric columns for the dropdown
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
# Filter out any columns you don't want to include
numeric_columns = ['microbusiness_density']

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

# Add new dropdown for selecting numeric column
filter_column = [
    dbc.Label("Select Data to Display"),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{"label": col.replace('_', ' ').title(), "value": col} for col in numeric_columns],
        value='microbusiness_density',  # Default value
        style={'width': '200px'}
    ),
]

global_metrics = html.Div([
    html.H4("USA-wide Metrics", style={'textAlign': 'center', 'fontSize': '21px', 'marginBottom': '25px'}),
    html.Div([
        html.H6("Total Microbusinesses", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '10px auto'}),
        html.P(f"{total_microbusinesses:,.0f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    html.Div([
        html.H6("Avg. Microbusiness Density", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '10px auto'}),
        html.P(f"{weighted_microbusiness_density:.2f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    html.Div([
        html.H6("Median Household Income", style={'marginBottom': '5px', 'fontSize': '16px'}),
        html.Hr(style={'border': '1px solid #AAC8E4', 'width': '80%', 'margin': '10px auto'}),
        html.P(f"${median_income:,.0f}", style={'fontSize': '18px', 'fontWeight': 'bold', 'marginTop': '5px'})
    ], style={'textAlign': 'center', 'backgroundColor': '#D7EBF6', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px'}),
], style={'border': '2px solid black', 'padding': '15px', 'borderRadius': '10px', 'width': '100%'})

map = dcc.Graph(id='map-placeholder', style={'height': '550px'})

chart_SMB_density = [
    dvc.Vega(id='density-placeholder', spec={'height': '230px'})  
]      

chart_med_income = [
    dvc.Vega(id='income-placeholder', style={'height': '230px'})
]

card_sellability = dbc.Card(id = "sellability")

card_growth = dbc.Card(id = "growth")

card_hireability = dbc.Card(id = "hireability")

end_credits = html.Div([
    html.Br(),
    html.H6("App allowing user to explore MicroBusiness density across the US, and derive key metrics used in deciding where to launch their next venture", style={'marginBottom': '5px', 'fontSize': '16px'}),
    html.H6("Created by: Anna Nandar, Dongchun Chen, Jiayi Li, Marek Boulerice", style={'marginBottom': '5px', 'fontSize': '10px'}),
    html.H6("Repo: https://github.com/UBC-MDS/DSCI-532_2025_26_SMBFinder", style={'marginBottom': '5px', 'fontSize': '10px'}),
    html.H6("Latest Deployment: 2025/03/01", style={'marginBottom': '5px', 'fontSize': '10px'}),
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
                            dbc.Col(filter_column),  # Add the new dropdown here
                    ]),
                    dbc.Row(map)
                ], md=9),
        ]),

        # Add this new row for the data table
        dbc.Row([
            dbc.Col([
                html.H4("Filtered Data"),
                html.Div(id='filtered-data-table')
            ])
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
                dbc.Col(card_growth),
                dbc.Col(card_hireability),
            ]
        ),
        dbc.Row(end_credits)
])

@app.callback(
    Output("county-dropdown", "options"),
    Input("state-dropdown", "value")
)
def update_county_dropdown(selected_state):
    if not selected_state:
        return []
    return [{"label": county, "value": county} for county in state_county_mapping[selected_state]]  

@app.callback(
    Output("map-placeholder", "figure"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value"),
     Input("column-dropdown", "value")]  
)
def update_map(selected_state, selected_county, selected_column):
    # Start with all data
    
    filtered_df = df.copy()
    filtered_df = filtered_df.sort_values('first_day_of_month').groupby('cfips').last().reset_index()
    
    # Filter based on selections
    if selected_state:
        if isinstance(selected_state, list):
            filtered_df = filtered_df[filtered_df["state"].isin(selected_state)]
        else:
            filtered_df = filtered_df[filtered_df["state"] == selected_state]
        
    if selected_county:
        if isinstance(selected_county, list):
            filtered_df = filtered_df[filtered_df["county"].isin(selected_county)]
        else:
            filtered_df = filtered_df[filtered_df["county"] == selected_county]
    

    print(filtered_df['cfips'].unique())

    # Default on microbusiness density for now 
    column_to_display = selected_column if selected_column else 'microbusiness_density'
    
    # If county is selected, show county level map
    if selected_county:
        fig = display_county_level_map(filtered_df, counties_geojson, 'cfips_fixed', column_to_display)
    # If state is selected but no county
    elif selected_state:
        fig = display_state_level_map(filtered_df, counties_geojson, 'cfips_fixed', column_to_display)
    # Default view for entire US
    else:
        fig = display_landing_page_map_choropleth_counties(filtered_df, counties_geojson, 0.7, 'cfips_fixed', column_to_display)
    
    # Remove the legend
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    
    return fig

@app.callback(
    Output("density-placeholder", "spec"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value")]
)

def update_chart(selected_state=None, selected_county=None):
    
    df_smb = df.copy()
    df_smb["year"] = pd.to_datetime(df_smb["first_day_of_month"]).dt.year  

    chart_title = "Average Business Density Growth Over Time Across USA"

    if not selected_state and not selected_county:
        filtered_df = df_smb.groupby("year", as_index=False)["microbusiness_density"].mean().round(2)

    else:

        filtered_df = df_smb.copy()

        if selected_state:
            filtered_df = filtered_df[filtered_df["state"] == selected_state]
            chart_title = f"Average Business Density Growth Over Time in {selected_state}" 

        
        if selected_county:
            filtered_df = filtered_df[filtered_df["county"] == selected_county]
            chart_title = f"Average Business Density Growth Over Time in {selected_county}, {selected_state}" 


        filtered_df = filtered_df.groupby("year", as_index=False)["microbusiness_density"].mean().round(2)


    if filtered_df.empty:
        return {}

    line_chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('year:O', title="Year", axis = alt.Axis(labelAngle = 0)),
        y=alt.Y('microbusiness_density:Q', title="Microbusiness Density"),
        tooltip=['year:O', 'microbusiness_density:Q']
    )

    scatter_points = alt.Chart(filtered_df).mark_point(
        size=120,  
        filled=True,
        color="green"  
    ).encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y('microbusiness_density:Q', title="Microbusiness Density"),
        tooltip=['year:O', 'microbusiness_density:Q']
    )

    final_chart = (line_chart + scatter_points).properties(
        width=500, height=300,
        title= chart_title
    ).configure_title(fontSize=15).interactive()

    return final_chart.to_dict()

@app.callback(
    Output("income-placeholder", "spec"),
    [Input("state-dropdown", "value"),
     Input("county-dropdown", "value")]
)
def update_income_chart(selected_state=None, selected_county=None):
    
    df_income = df.copy()

    income_columns = [col for col in df_income.columns if col.startswith("median_hh_inc_")]
    df_income = df_income.melt(id_vars=["state", "county"], 
                                value_vars=income_columns, 
                                var_name="year", 
                                value_name="median_income")

    df_income["year"] = df_income["year"].str.extract("(\d{4})").astype(int)

    chart_title = "Median Household Income Growth Over Time Across USA"

    if not selected_state and not selected_county:
        filtered_df = df_income.groupby("year", as_index=False)["median_income"].mean().round(2)

    else:
        filtered_df = df_income.copy()

        if selected_state:
            filtered_df = filtered_df[filtered_df["state"] == selected_state]
            chart_title = f"Median Household Income Growth Over Time in {selected_state}"

        if selected_county:
            filtered_df = filtered_df[filtered_df["county"] == selected_county]
            chart_title = f"Median Household Income Growth Over Time in {selected_county}, {selected_state}"

        filtered_df = filtered_df.groupby("year", as_index=False)["median_income"].mean().round(2)

    if filtered_df.empty:
        return {}

    line_chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('year:O', title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('median_income:Q', title="Median Household Income"),
        tooltip=['year:O', 'median_income:Q']
    )

    scatter_points = alt.Chart(filtered_df).mark_point(
        size=120,  
        filled=True,
        color="blue" 
    ).encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y('median_income:Q', title="Median Household Income"),
        tooltip=['year:O', 'median_income:Q']
    )

    final_chart = (line_chart + scatter_points).properties(
        width=500, height=300,
        title=chart_title  
    ).configure_title(
        fontSize=15 
    ).interactive()

    return final_chart.to_dict()

@app.callback(
    [Output("sellability", "children"),
    Output("growth", "children"),
    Output("hireability", "children")],
    [Input("county-dropdown", "value")]
)
def update_BI_cards(county):
    print(county)

    if not county:
        sellability_empty = [
            dbc.CardHeader("Sellability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("County percentile median income", style={'fontSize': '12px'})
        ]
        growth_empty = [
            dbc.CardHeader("Growth index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("county percentile for average yealy Microbusiness growth",style={'fontSize': '12px'})
        ]
        hireability_empty = [
            dbc.CardHeader("Hireability index"),
            dbc.CardBody("[Select a county]"),
            dbc.CardFooter("County percentile for percent of population with bachelors degree", style={'fontSize': '12px'})
        ]
        return sellability_empty, growth_empty, hireability_empty
    
    latest_date = "2022-10-01"

    #calculating sellability index
    county_income = df[df["county"] == county][f"median_hh_inc_{latest_year}"].iloc[0]
    sell_df = df[df["first_day_of_month"] == latest_date]
    sell_df = sell_df[[f"median_hh_inc_{latest_year}"]]
    clean_sell = sell_df.dropna()
    sort_sell = np.sort(clean_sell[f"median_hh_inc_{latest_year}"])
    sell_percentile = round(np.searchsorted(sort_sell,county_income,side = "right")/ len(sort_sell)*100 , 2)

    #calculating Hireability index
    #note: brown county returns different value on app than in testing. look into
    county_education = df[df["county"] == county][f"pct_college_{latest_year}"].iloc[0]
    hire_df = df[df["first_day_of_month"] == latest_date]
    hire_df = hire_df[[f"pct_college_{latest_year}"]]
    clean_hire = hire_df.dropna()
    sort_hire = np.sort(clean_hire[f"pct_college_{latest_year}"])
    hire_percentile = round(np.searchsorted(sort_hire,county_education,side = "right")/ len(sort_hire)*100 , 2)


    # calculating growth index
    growth_df = df.copy()
    #create data frame of counties with number of businesses in each year
    growth_df = growth_df[["county","state", "first_day_of_month","active"]]
    growth_df["first_day_of_month"] = pd.to_datetime(growth_df["first_day_of_month"])
    growth_df["year"] = growth_df["first_day_of_month"].dt.year
    growth_df["month"] = growth_df["first_day_of_month"].dt.month
    growth_df = growth_df[growth_df["month"] == 10]
    growth_df = growth_df[["county", "state", "active", "year"]]
    growth_df = growth_df.pivot(index=["county", "state"], columns = "year", values="active")
    growth_df = growth_df.reset_index()
    growth_df.columns = growth_df.columns.astype(str)

    # Calculate percent change between years
    growth_df['pct_change_2019_2020'] = (growth_df['2020'] - growth_df['2019']) / growth_df['2019'] * 100
    growth_df['pct_change_2020_2021'] = (growth_df['2021'] - growth_df['2020']) / growth_df['2020'] * 100
    growth_df['pct_change_2021_2022'] = (growth_df['2022'] - growth_df['2021']) / growth_df['2021'] * 100

    # Calculate the average percent change across these years
    growth_df['mean_pct_change'] = growth_df[['pct_change_2019_2020', 'pct_change_2020_2021', 'pct_change_2021_2022']].mean(axis=1)
    growth_df = growth_df[["county", "state", "mean_pct_change"]]

    county_growth = growth_df[growth_df["county"] == county]["mean_pct_change"].iloc[0]
    clean_growth = growth_df.dropna()
    sort_growth = np.sort(clean_growth["mean_pct_change"])
    growth_percentile = round(np.searchsorted(sort_growth, county_growth, side = "right")/ len(sort_growth)*100, 2)



    sellability_list = [
        dbc.CardHeader("Sellability index"),
        dbc.CardBody(f"{sell_percentile}%"),
        dbc.CardFooter("County percentile median income", style={'fontSize': '12px'})
    ]
    growth_list = [
        dbc.CardHeader("Growth index"),
        dbc.CardBody(f"{growth_percentile}%"),
        dbc.CardFooter("county percentile for average yealy Microbusiness growth", style={'fontSize': '12px'})
    ]
    hireability_list = [
        dbc.CardHeader("Hireability index"),
        dbc.CardBody(f"{hire_percentile}%"),
        dbc.CardFooter("County percentile for percent of population with bachelors degree", style={'fontSize': '12px'})
    ]
    return sellability_list, growth_list, hireability_list


if __name__ == '__main__':
    app.run(debug=True)