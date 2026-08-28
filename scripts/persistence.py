import pandas as pd

# Input and output file paths
input_file = "data/processed/firms_clean.csv"
output_file = "data/processed/hotspot_history.csv"

# Load FIRMS data
df = pd.read_csv(input_file)

# Check column names
print("Columns found:")
print(df.columns.tolist())

# Convert date column to datetime
df["acq_date"] = pd.to_datetime(df["acq_date"])

# Create approximate grid coordinates
df["grid_lat"] = df["latitude"].round(3)
df["grid_lon"] = df["longitude"].round(3)

# Group detections by approximate location
grouped = df.groupby(["grid_lat", "grid_lon"])

# Calculate hotspot information
hotspots = grouped.agg(
    detection_count=("latitude", "count"),
    active_days=("acq_date", "nunique"),
    first_date=("acq_date", "min"),
    last_date=("acq_date", "max"),
    avg_frp=("frp", "mean")
).reset_index()

# Create hotspot IDs
hotspots.insert(
    0,
    "hotspot_id",
    [f"H{i:03d}" for i in range(1, len(hotspots) + 1)]
)

# Rename grid columns
hotspots = hotspots.rename(
    columns={
        "grid_lat": "latitude",
        "grid_lon": "longitude"
    }
)

# Round average FRP
hotspots["avg_frp"] = hotspots["avg_frp"].round(2)

# Save output
hotspots.to_csv(output_file, index=False)

# Print results
print("\nNumber of hotspot groups:", len(hotspots))

print("\nTop persistent hotspots:")

top_hotspots = hotspots.sort_values(
    by="active_days",
    ascending=False
)

for _, row in top_hotspots.iterrows():
    print(
        f"{row['hotspot_id']} — "
        f"{row['active_days']} active days"
    )

print("\nOutput saved to:")
print(output_file)