import json
import csv
import os

input_file = "data/raw/osm/industrial_locations.geojson"
output_file = "data/processed/industrial_locations.csv"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for i, feature in enumerate(data["features"], start=1):

    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    name = properties.get("name", "Unknown Industrial Location")

    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates")

    latitude = None
    longitude = None

    # Point
    if geometry_type == "Point":
        longitude = coordinates[0]
        latitude = coordinates[1]

    # Polygon
    elif geometry_type == "Polygon":
        points = coordinates[0]

        longitude = sum(point[0] for point in points) / len(points)
        latitude = sum(point[1] for point in points) / len(points)

    # MultiPolygon
    elif geometry_type == "MultiPolygon":
        points = coordinates[0][0]

        longitude = sum(point[0] for point in points) / len(points)
        latitude = sum(point[1] for point in points) / len(points)

    if latitude is not None and longitude is not None:
        rows.append([
            f"I{i:03d}",
            name,
            latitude,
            longitude,
            "industrial"
        ])

os.makedirs("data/processed", exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "facility_id",
        "name",
        "latitude",
        "longitude",
        "type"
    ])

    writer.writerows(rows)

print(f"Created {output_file}")
print(f"Number of industrial locations: {len(rows)}")