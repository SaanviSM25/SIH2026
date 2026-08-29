import pandas as pd

history = pd.read_csv("data/processed/hotspot_history.csv")
classification = pd.read_csv("data/processed/classified_hotspots.csv")

classification = classification[
    [
        "hotspot_id",
        "distance_to_industry_km",
        "classification",
        "reason"
    ]
]

final = history.merge(
    classification,
    on="hotspot_id",
    how="left"
)

final.to_csv(
    "data/processed/final_hotspots.csv",
    index=False
)

print("Final hotspots:", len(final))
print("Columns:", list(final.columns))