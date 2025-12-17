import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf

def _plot_hist(df, col, title, x_label):
    fig, ax = plt.subplots()
    ax.hist(df[col].dropna(), bins=40)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Frequency")
    return fig

def national_aggregate(df : pd.DataFrame) -> pd.DataFrame:
    """
    Creates national-level trends:
    - Averages rate variables
    - Sums actual count variables
    """ 
    Rate_vars = [col for col in df.columns if "_rate" in col or col in ['marriage_rate_per_1000','divorce_rate_per_1000']]
    Actual_vars = [col for col in df.columns if "_actual" in col or col in ['married_last_year','divorced_last_year','population','participated_population','population_over_15']]
    
    # Aggregate 
    agg_dict = {var: "mean" for var in Rate_vars}
    agg_dict.update({var: "sum" for var in Actual_vars})

    # Aggregate dataframe
    national_df = (
        df
        .groupby("year", as_index=False)
        .agg(agg_dict)
    )
    
    # Return Dataframe
    return national_df



def linear_regression_by_crime_rate(df : pd.DataFrame, crime):
    # Copy dataframe
    df = df.sort_values(["state","year"]).copy()

    model = smf.ols(f"{crime} ~ marriage_rate_per_1000 + divorce_rate_per_1000 + C(state) + C(year)",
                    data = df).fit(
                        cob_type="cluster",
                        cov_kwds={"groups": df["state"]}
                    )
    return model

def linear_regression_by_marriage_divorce(df : pd.DataFrame, marriage_true : bool, clearence_rate : bool):
    df = df.sort_values(["state","year"]).copy()
    if (marriage_true):
        model_base = "marriage_rate_per_1000"
    else:
        model_base = "divorce_rate_per_1000"
    
    if (clearence_rate):
        Rate_vars = [col for col in df.columns if "_rate" in col and col for col in df.columns if "_clearance_rate" in col]    
    else: 
        Rate_vars = [col for col in df.columns if "_rate" in col and col for col in df.columns if "_clearance_rate" not in col]    

    model_assumptions = "~ C(state) + C(year)"
    for Rate in Rate_vars:
        model_assumptions += f" + {Rate}"

    model = smf.ols(f"{model_base} {model_assumptions}",
                    data = df).fit(
                        cob_type="cluster",
                        cov_kwds={"groups": df["state"]}
                    )
    
    return model

# Create Histogram
def histogram_maker(
    df: pd.DataFrame,
    column: str,
    title: str,
    x_label: str,
):
    """
    Create a histogram for a given dataframe column
    """
    return _plot_hist(
        df=df,
        col=column,
        title=title,
        x_label=x_label
    )
