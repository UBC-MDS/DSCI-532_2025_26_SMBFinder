import pandas as pd
from .map_view import fix_cfips

def generate_df(filepath: str = "data/processed/data_details_smb.csv", latest_year: str = "2021") -> dict:
    """
    Load and process the microbusiness dataset, returning a dictionary of computed results.

    Args:
        filepath (str): The path to the CSV file.
        latest_year (str): The year to use for income-related calculations.

    Returns:
        dict: A dictionary containing:
            - df: The processed DataFrame.
            - unique_states: Sorted list of unique states.
            - state_county_mapping: Mapping from each state to its list of counties.
            - total_microbusinesses: Sum of the active microbusinesses.
            - weighted_microbusiness_density: Weighted average microbusiness density.
            - median_income: Calculated median household income.
            - numeric_columns: List of relevant numeric columns.
    """
    # Load data with correct data types
    df = pd.read_csv(filepath, dtype={'cfips_fixed': str, 'cfips': str})
    
    # Standardize CFIPS columns
    df['cfips_fixed'] = df['cfips_fixed'].astype(str).apply(fix_cfips)
    df['cfips'] = df['cfips'].astype(str)
    
    # Compute unique states and state to county mapping
    unique_states = sorted(df["state"].unique())
    state_county_mapping = df.groupby("state")["county"].unique().apply(list).to_dict()

    # Total number of microbusinesses
    total_microbusinesses = df["active"].sum()

    # Calculate adult population and weighted microbusiness density
    df["adult_population"] = (df["active"] / df["microbusiness_density"]) * 100
    weighted_microbusiness_density = (
        (df["microbusiness_density"] * df["adult_population"]).sum() / 
        df["adult_population"].sum()
    )

    # Compute median income using cumulative adult population
    income_col = f"median_hh_inc_{latest_year}"
    df = df.sort_values(by=income_col)
    df["cumulative_population"] = df["adult_population"].cumsum()
    total_population = df["adult_population"].sum()
    median_income = df[df["cumulative_population"] >= total_population / 2][income_col].iloc[0]

    # Define numeric columns for analysis
    numeric_columns = ["growth_index", "sellability_index", "hireability_index", "microbusiness_density"]

    return {
        "df": df,
        "unique_states": unique_states,
        "state_county_mapping": state_county_mapping,
        "total_microbusinesses": total_microbusinesses,
        "weighted_microbusiness_density": weighted_microbusiness_density,
        "median_income": median_income,
        "numeric_columns": numeric_columns,
    }
