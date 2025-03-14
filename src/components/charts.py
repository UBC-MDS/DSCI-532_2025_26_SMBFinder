import altair as alt
import pandas as pd


def update_density_chart_details(df, selected_states=None, selected_counties=None):

    df_smb = df.copy()
    df_smb["year"] = pd.to_datetime(df_smb["first_day_of_month"]).dt.year  

    chart_title = "Business Density Growth Over Time"

    filtered_df = df_smb.copy()

    # for multiple states or counties filter
    if selected_states:
        filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]

    if selected_counties:
        filtered_df = filtered_df[filtered_df["county"].isin(selected_counties)]

    # If nothing is chosen, overall chart should show
    if not selected_states and not selected_counties:
        grouped_df = df_smb.groupby("year", as_index=False)["microbusiness_density"].mean().round(2)
        grouped_df["Location"] = "overall" 
        group_col = "Location"
        chart_title = chart_title
    else:
        if selected_counties:
            group_col = "county"
            chart_title = f"Business Density Growth in Selected Counties"
        elif selected_states:
            group_col = "state"
            chart_title = f"Business Density Growth in Selected States"

        grouped_df = filtered_df.groupby(["year", group_col], as_index=False)["microbusiness_density"].mean().round(2)

    line_chart = alt.Chart(grouped_df).mark_line().encode(
        x=alt.X('year:O', title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('microbusiness_density:Q', title="Microbusiness Density"),
        color=alt.Color(f"{group_col}:N", title="Location"),
        tooltip=['year:O', 'microbusiness_density:Q', f"{group_col}:N"]
    )

    scatter_points = alt.Chart(grouped_df).mark_point(size=80, filled=True).encode(
        x='year:O',
        y='microbusiness_density:Q',
        color=alt.Color(f"{group_col}:N", title="Location"),
        tooltip=['year:O', 'microbusiness_density:Q', f"{group_col}:N"]
    )

    final_chart = (line_chart + scatter_points).properties(
        width=450, height=300, 
        title=chart_title
    ).configure_title(fontSize=15).interactive()

    return final_chart.to_dict()


def update_income_chart_details(df, selected_states=None, selected_counties=None):

    df_income = df.copy()

    income_columns = [col for col in df_income.columns if col.startswith("median_hh_inc_")]
    df_income = df_income.melt(id_vars=["state", "county"], 
                                value_vars=income_columns, 
                                var_name="year", 
                                value_name="median_income")

    df_income["year"] = df_income["year"].str.extract("(\d{4})").astype(int)

    chart_title = "Median Household Income Growth Over Time"

    filtered_df = df_income.copy()

    # for multiple states or counties filter
    if selected_states:
        filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]

    if selected_counties:
        filtered_df = filtered_df[filtered_df["county"].isin(selected_counties)]
    
    # If nothing is chosen, overall chart should show
    if not selected_states and not selected_counties:
        grouped_df = df_income.groupby("year", as_index=False)["median_income"].mean().round(2)
        grouped_df["Location"] = "overall" 
        group_col = "Location"
        chart_title = chart_title
    else:
        if selected_counties:
            group_col = "county"
            chart_title = f"Median Income Growth in Selected Counties"
        elif selected_states:
            group_col = "state"
            chart_title = f"Median Income Growth in Selected States"

        grouped_df = filtered_df.groupby(["year", group_col], as_index=False)["median_income"].mean().round(2)

    line_chart = alt.Chart(grouped_df).mark_line().encode(
        x=alt.X('year:O', title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('median_income:Q', title="Median Household Income"),
        color=alt.Color(f"{group_col}:N", title="Location", legend=alt.Legend(
            orient='none',
            legendX=130, legendY=-40,
            direction='vertical',
            titleAnchor='middle')),
        tooltip=['year:O', 'median_income:Q', f"{group_col}:N"],
    )


    scatter_points = alt.Chart(grouped_df).mark_point(
        size=80,  
        filled=True,
    ).encode(
        x='year:O',
        y='median_income:Q',
        color=alt.Color(f"{group_col}:N", title="Location"),
        tooltip=['year:O', 'median_income:Q', f"{group_col}:N"]
    )

    final_chart = (line_chart + scatter_points).properties(
        height=300, width=380,
        title=chart_title  
    ).configure_title(
        fontSize=15
    ).interactive()

    return final_chart.to_dict()
