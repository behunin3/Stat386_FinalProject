import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from wrangling import load_data, load_offense_mapping

def main():
    print(os.getcwd())
    st.title("Discovering the Relationship Between Divorce and Crime")

    df = load_data("src/data/Combined_DF.csv")

    # Reverse mapping: full name -> code
    offense_map = load_offense_mapping("src/json/crime_abbr.json")
    name_to_code = {v: k for k, v in offense_map.items()}

    # sidebar controls
    state = st.sidebar.selectbox(
        "Select a state",
        sorted(df['state'].unique())
    )

    crime_name = st.sidebar.selectbox(
        "Select a crime",
        list(name_to_code.keys()) 
    )
    crime_code = name_to_code[crime_name] 

    metric = st.sidebar.radio(
        "Select metric",
        ["Actual", "Rate"]
    )

    column_name = f"{crime_code}_{metric.lower()}"

    filtered = (
        df[df['state'] == state]
        .sort_values("year")
    )

    fig, ax1 = plt.subplots()

    ax1.plot(
        filtered["year"],
        filtered[column_name],
        label=f"{crime_name} ({metric})",
        color="blue"
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel(f"{metric} of {crime_name}")

    ax2 = ax1.twinx()
    ax2.plot(
        filtered["year"],
        filtered["divorced_last_year"],
        label="Divorces",
        color="red"
    )
    ax2.set_ylabel("Number of Divorces")

    ax1.set_title(f"{crime_name} vs Divorces in {state}")

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left")

    st.pyplot(fig)

if __name__ == "__main__":
    main()