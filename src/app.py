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
        display_county_level_map,
        fix_cfips
    )
except ModuleNotFoundError:
    from src.components.map_view import (
        display_landing_page_map_dots,
        display_landing_page_map_choropleth_counties,
        display_state_level_map,
        display_county_level_map,
        fix_cfips
    )

# data wrangling for filter & sidebar
df = pd.read_csv("data/processed/smb_enriched.csv",dtype={'cfips_fixed': str, 'cfips': str})  
df['cfips_fixed'] = df['cfips_fixed'].astype(str)
df['cfips'] = df['cfips'].astype(str)
df['cfips_fixed'] = df['cfips_fixed'].apply(fix_cfips)


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
    
    filtered_df['cfips_fixed'] = filtered_df['cfips_fixed'].apply(fix_cfips)

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


if __name__ == '__main__':
    app.run(debug=True)