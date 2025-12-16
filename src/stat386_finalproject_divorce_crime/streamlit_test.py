import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from stat386_finalproject_divorce_crime.wrangling import load_data, load_offense_mapping

st.title("Discovering the Relationship Between Divorce and Crime")

df = load_data("../data/Combined_DF.csv")

# Reverse mapping: full name -> code
offense_map = load_offense_mapping("../json/crime_abbr.json")
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

# plot
fig, ax = plt.subplots()
ax.plot(filtered["year"], filtered[column_name])
ax.set_xlabel("Year")
ax.set_ylabel(f"{metric} of {crime_name}")
ax.set_title(f"{crime_name} ({metric}) in {state} Over Time")
st.pyplot(fig)