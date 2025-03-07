import pandas as pd
from .map_view import fix_cfips

# data wrangling for filter, sidebar & map
df = pd.read_csv("data/processed/data_details_smb.csv",dtype={'cfips_fixed': str, 'cfips': str})  

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

numeric_columns = ["growth_index", "sellability_index",  "hireability_index","microbusiness_density", ]

df['cfips_fixed'] = df['cfips_fixed'].astype(str)
df['cfips'] = df['cfips'].astype(str)
df['cfips_fixed'] = df['cfips_fixed'].apply(fix_cfips)
