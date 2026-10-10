from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page layout
st.set_page_config(page_title="California Housing Data (1990)", layout="centered")
st.title("California Housing Data (1990) by YOUR NAME")

# Read housing.csv from the same folder as this Python file
csv_path = Path(__file__).resolve().parent / "housing.csv"
df = pd.read_csv(csv_path)

# Main-page price slider (default: $200,000)
min_price = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000,
    key="housing_min_price_v2",
)
st.subheader("See more filters in the sidebar:")

# Sidebar: geographic location filters, all selected by default
location_types = sorted(df["ocean_proximity"].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types,
)

# Sidebar: income-level filter, starting with Low
income_level = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"],
    index=0,
)

# Apply ALL three filters to the same dataframe
price_mask = df["median_house_value"] >= min_price
location_mask = df["ocean_proximity"].isin(selected_locations)

if income_level == "Low":
    income_mask = df["median_income"] <= 2.5
elif income_level == "Medium":
    income_mask = (df["median_income"] > 2.5) & (df["median_income"] < 4.5)
else:
    income_mask = df["median_income"] >= 4.5

filtered_df = df.loc[price_mask & location_mask & income_mask].copy()

# Optional verification: uncomment this line while testing
# st.caption(f"Matching districts: {len(filtered_df):,}; price threshold: ${min_price:,}")

if filtered_df.empty:
    st.warning("No districts match these filters. Try different selections.")
else:
    # Map of filtered districts
    st.map(filtered_df[["latitude", "longitude"]].dropna())

    # Histogram of filtered median house values: exactly 30 bins
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(filtered_df["median_house_value"], bins=30)
    ax.set_xlabel("Median House Value (USD)")
    ax.set_ylabel("Number of Districts")
    ax.set_title("Distribution of Median House Value")
    st.pyplot(fig)
    plt.close(fig)
