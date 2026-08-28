import pandas as pd
from geopy.distance import geodesic


# -----------------------------
# 1. Read the input CSV files
# -----------------------------

hotspots = pd.read_csv("data/raw/hotspot_history.csv")
industries = pd.read_csv("data/raw/industrial_locations.csv")


# -----------------------------
# 2. Find nearest industry
# -----------------------------

def find_nearest_industry(lat, lon):
    nearest_distance = float("inf")

    for _, industry in industries.iterrows():

        hotspot_location = (lat, lon)
        industry_location = (
            industry["latitude"],
            industry["longitude"]
        )

        distance_km = geodesic(
            hotspot_location,
            industry_location
        ).kilometers

        if distance_km < nearest_distance:
            nearest_distance = distance_km

    return nearest_distance


# -----------------------------
# 3. Classification rules
# -----------------------------

def classify_hotspot(active_days, distance_km):

    if active_days >= 3 and distance_km <= 1:
        return "Persistent Industrial Source"

    elif active_days < 3 and distance_km <= 1:
        return "Possible Industrial Fire"

    elif active_days >= 3 and distance_km > 1:
        return "Unexplained Persistent Source"

    else:
        return "Short-lived Thermal Event"


# -----------------------------
# 4. Process every hotspot
# -----------------------------

results = []

for _, hotspot in hotspots.iterrows():

    distance = find_nearest_industry(
        hotspot["latitude"],
        hotspot["longitude"]
    )

    classification = classify_hotspot(
        hotspot["active_days"],
        distance
    )

    reason = (
        f"Detected on {hotspot['active_days']} days "
        f"and located {distance:.2f} km "
        f"from the nearest industrial location."
    )

    results.append({
        "hotspot_id": hotspot["hotspot_id"],
        "latitude": hotspot["latitude"],
        "longitude": hotspot["longitude"],
        "active_days": hotspot["active_days"],
        "distance_to_industry_km": round(distance, 2),
        "classification": classification,
        "reason": reason
    })


# -----------------------------
# 5. Save the result
# -----------------------------

result_df = pd.DataFrame(results)

result_df.to_csv(
    "data/processed/classified_hotspots.csv",
    index=False
)


# -----------------------------
# 6. Display results
# -----------------------------

for _, row in result_df.iterrows():

    print()
    print(row["hotspot_id"])
    print("Classification:", row["classification"])
    print("Reason:", row["reason"])

print()
print("Classification complete.")
print("Output saved to data/processed/classified_hotspots.csv")