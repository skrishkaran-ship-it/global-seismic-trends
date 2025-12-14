import streamlit as st
import pandas as pd

# -----------------------------
# Load Data from CSV
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("streamlit/earthquakes.csv")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Seismic Trends Dashboard")

# -----------------------------
# Load Data with Error Handling
# -----------------------------
try:
    df = load_data()
    st.success("✅ Data loaded successfully from CSV!")
except Exception as e:
    st.error("❌ Failed to load data")
    st.exception(e)
    st.stop()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

min_mag, max_mag = st.sidebar.slider(
    "Magnitude range",
    float(df["magnitude"].min()),
    float(df["magnitude"].max()),
    (1.0, 5.0)
)

filtered_df = df[
    (df["magnitude"] >= min_mag) &
    (df["magnitude"] <= max_mag)
]

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", len(filtered_df))
col2.metric("Max Magnitude", round(filtered_df["magnitude"].max(), 2))
col3.metric("Avg Depth (km)", round(filtered_df["depth_km"].mean(), 2))

# -----------------------------
# Charts
# -----------------------------
st.subheader("📊 Earthquake Magnitude Distribution")
st.bar_chart(
    filtered_df["magnitude"]
    .value_counts()
    .sort_index()
)

st.subheader("🗺️ Global Earthquake Locations")
st.map(filtered_df[["latitude", "longitude"]])

# -----------------------------
# Data Preview
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(50))

# -----------------------------
# Download Option
# -----------------------------
st.download_button(
    "⬇️ Download Filtered Data (CSV)",
    filtered_df.to_csv(index=False),
    "filtered_earthquakes.csv",
    mime="text/csv"
)
