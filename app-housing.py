
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Set up the webpage
st.set_page_config(
    page_title="California Housing Data",
    layout="wide"
)

# 2. Title - replace YOUR NAME with your own name
st.title("California Housing Data (1990) by YOUR NAME")

# 3. Load the California housing dataset
data_path = Path(__file__).with_name("housing.csv")
df = pd.read_csv(data_path)

# 4. Slider for minimum median house value
min_price = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)

st.subheader("See more filters in the sidebar:")

# 5. Sidebar: location type multiselect
location_types = sorted(df["ocean_proximity"].dropna().unique())

selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types
)

# 6. Sidebar: income level radio buttons
income_level = st.sidebar.radio(
    "Choose income level",
    ["Low", "Medium", "High"]
)

# 7. Filter by house value
filtered_df = df[
    df["median_house_value"] >= min_price
]

# 8. Filter by location type
filtered_df = filtered_df[
    filtered_df["ocean_proximity"].isin(selected_locations)
]

# 9. Filter by income level
if income_level == "Low":
    filtered_df = filtered_df[
        filtered_df["median_income"] <= 2.5
    ]

elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) &
        (filtered_df["median_income"] < 4.5)
    ]

else:
    filtered_df = filtered_df[
        filtered_df["median_income"] >= 4.5
    ]

# 10. Show the filtered map and histogram
if filtered_df.empty:
    st.warning("No districts match your selected filters.")

else:
    # Display the map
    st.map(
        filtered_df[["latitude", "longitude"]].dropna()
    )

    # Display the histogram with 30 bins
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        filtered_df["median_house_value"],
        bins=30
    )

    ax.set_xlabel("Median House Value (USD)")
    ax.set_ylabel("Number of Districts")
    ax.set_title("Distribution of Median House Value")

    st.pyplot(fig)
    plt.close(fig)