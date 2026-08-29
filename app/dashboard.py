import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(page_title="THERMALGUARD", layout="wide")

CSV_PATH = "data/processed/final_hotspots.csv"


# -----------------------------------------------------------------------------
# Step 1: Load Data (with Fallback Sample Data)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        st.warning(
            f"File `{CSV_PATH}` not found. Displaying fallback sample data."
        )
        sample_data = {
            "hotspot_id": ["H001", "H002", "H003", "H004", "H005"],
            "latitude": [28.6139, 28.6210, 28.6050, 28.6300, 28.5900],
            "longitude": [77.2090, 77.2150, 77.2200, 77.1950, 77.2300],
            "active_days": [2, 12, 8, 7, 15],
            "detection_count": [3, 24, 15, 12, 30],
            "distance_to_industry": [5.20, 0.15, 1.20, 0.42, 8.50],
            "classification": [
                "Transient Source",
                "Possible Industrial Fire",
                "Possible Industrial Fire",
                "Possible Industrial Fire",
                "Unexplained Persistent Source",
            ],
            "reason": [
                "Detected for short duration with no nearby industry.",
                "High thermal intensity sustained over 12 days within 0.15 km of industrial zone.",
                "Detected 15 times over 8 days near mapped manufacturing facility.",
                "Detected repeatedly over 7 days near a mapped industrial location.",
                "High persistence (15 days) but more than 8 km from any mapped industrial facility.",
            ],
        }
        df = pd.DataFrame(sample_data)

    # Ensure distance column exists / handles variations
    if "distance_to_industry" not in df.columns and "distance" in df.columns:
        df["distance_to_industry"] = df["distance"]

    # Ensure detection count exists
    if "detection_count" not in df.columns:
        df["detection_count"] = df["active_days"] * 2

    return df


df = load_data()


# -----------------------------------------------------------------------------
# Step 2: Streamlit Title
# -----------------------------------------------------------------------------
st.title("THERMALGUARD")
st.subheader("AI-Assisted Industrial Thermal Intelligence")
st.markdown("---")


# -----------------------------------------------------------------------------
# Step 3: Summary Numbers
# -----------------------------------------------------------------------------
total_hotspots = len(df)
persistent_hotspots = len(df[df["active_days"] >= 5])
industrial_fires = len(
    df[df["classification"].str.contains("Fire", case=False, na=False)]
)
unexplained_sources = len(
    df[df["classification"].str.contains("Unexplained", case=False, na=False)]
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Hotspots", total_hotspots)
col2.metric("Persistent Hotspots", persistent_hotspots)
col3.metric("Possible Industrial Fires", industrial_fires)
col4.metric("Unexplained Persistent Sources", unexplained_sources)

st.markdown("---")


# Helper function to map classifications to marker colors
def get_color(classification):
    cls = str(classification).lower()
    if "fire" in cls:
        return "red"
    elif "persistent industrial" in cls:
        return "orange"
    elif "unexplained" in cls:
        return "purple"
    else:
        return "blue"


# -----------------------------------------------------------------------------
# Step 4: Interactive Map
# -----------------------------------------------------------------------------
st.markdown("### Hotspot Map")

if not df.empty:
    avg_lat = df["latitude"].mean()
    avg_lon = df["longitude"].mean()

    # Create Folium Map
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Add markers
    for _, row in df.iterrows():
        color = get_color(row["classification"])
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"<b>ID:</b> {row['hotspot_id']}<br><b>Class:</b> {row['classification']}",
            tooltip=f"{row['hotspot_id']} ({row['classification']})",
        ).add_to(m)

    st_folium(m, width="100%", height=500)


st.markdown("---")


# -----------------------------------------------------------------------------
# Step 5: Hotspot Table & Selected Details
# -----------------------------------------------------------------------------
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### Hotspot Table")
    display_cols = [
        "hotspot_id",
        "active_days",
        "distance_to_industry",
        "classification",
    ]
    # Filter only available columns
    available_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[available_cols].rename(
            columns={
                "hotspot_id": "Hotspot ID",
                "active_days": "Active Days",
                "distance_to_industry": "Distance to Industry (km)",
                "classification": "Classification",
            }
        ),
        use_container_width=True,
        height=300,
    )

with right_col:
    st.markdown("### Selected Hotspot Details")

    selected_id = st.selectbox("Select Hotspot:", df["hotspot_id"].unique())

    selected_row = df[df["hotspot_id"] == selected_id].iloc[0]
    

    st.markdown(f"**Classification:** {selected_row['classification']}")
    st.markdown(f"**Active Days:** {selected_row['active_days']}")
    st.markdown(
        f"**Detection Count:** {selected_row.get('detection_count', 'N/A')}"
    )

    dist_val = selected_row.get(
    "distance_to_industry_km",
    selected_row.get("distance_to_industry", selected_row.get("distance", "N/A"))
)
    if isinstance(dist_val, (int, float)):
        st.markdown(f"**Distance to Industry:** {dist_val:.2f} km")
    else:
        st.markdown(f"**Distance to Industry:** {dist_val}")

    st.markdown(f"**Reason:**\n{selected_row['reason']}")