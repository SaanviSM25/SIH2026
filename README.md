# THERMALGUARD

## AI-Assisted Industrial Thermal Intelligence

THERMALGUARD is a prototype system for identifying and classifying thermal hotspots using satellite-based thermal observations, hotspot persistence, and proximity to mapped industrial locations.

The system is designed to help identify thermal events that may require further investigation.

> THERMALGUARD provides a prototype classification based on observed persistence and proximity to mapped industrial locations. It does not prove that an event is definitely an industrial fire.

## 1. Problem

Thermal hotspots detected from satellite data can have different causes. Some may be short-lived events, while others may repeatedly occur near industrial facilities.

Manually examining these hotspots can make it difficult to identify persistent patterns and prioritize locations for investigation.

## 2. What THERMALGUARD Does

The prototype:

* Processes thermal hotspot data.
* Identifies hotspot persistence.
* Calculates proximity to mapped industrial locations.
* Classifies thermal hotspots based on persistence and industrial proximity.
* Produces a final integrated CSV dataset.
* Displays the results through an interactive Streamlit dashboard and map.

## 3. Data Sources

The prototype uses:

* FIRMS thermal hotspot data.
* OpenStreetMap-derived industrial location data.
* Processed hotspot and industrial-location datasets.

The project includes raw and processed data under the `data/` directory.

## 4. Basic Architecture

```text
FIRMS CSV
    ↓
Data Cleaning
    ↓
Persistence Analysis
    ↓
OSM Industrial Context
    ↓
Thermal Classification
    ↓
Integration
    ↓
Final Hotspots CSV
    ↓
Streamlit Dashboard
    ↓
Interactive Map
```

## 5. Project Structure

```text
ThermalGuard/
├── app/
│   └── dashboard.py
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── classify.py
│   ├── integrate.py
│   └── persistence.py
├── src/
│   └── convert_osm.py
├── docs/
│   └── testing.md
└── README.md
```

## 6. Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

For the dashboard, the required packages include Streamlit, Pandas, Folium, and Streamlit-Folium.

## 7. Running the Prototype

Run the dashboard from the project root:

```bash
python -m streamlit run app/dashboard.py
```

The dashboard displays:

* Total thermal hotspots
* Persistent hotspots
* Possible industrial fires
* Unexplained persistent sources
* Hotspot locations on an interactive map
* Hotspot classification
* Active days
* Detection count
* Distance to the nearest mapped industrial location
* Reason for classification

## 8. Processing Pipeline

The intended processing sequence is:

```bash
python scripts/clean_firms.py
python scripts/persistence.py
python scripts/classify.py
python scripts/integrate.py
python -m streamlit run app/dashboard.py
```

The exact processing workflow depends on the availability of the FIRMS cleaning step and its generated input files. See `docs/testing.md` for the current testing status.

## 9. Example Classification

THERMALGUARD uses persistence and industrial proximity to support prototype classifications such as:

* **Persistent Industrial Source**
* **Possible Industrial Fire**
* **Unexplained Persistent Source**
* **Short-lived Thermal Event**

These classifications are intended to support investigation and prioritization rather than provide definitive conclusions about the cause of a hotspot.

## 10. Limitations

* The system is a prototype.
* Thermal hotspots may have causes that cannot be determined from satellite observations alone.
* Industrial-location data may be incomplete or inaccurate.
* Classification depends on the quality and coverage of the input data.
* The current processed dataset may not contain examples of every required persistence scenario.
* The prototype should not be treated as proof that a hotspot represents an industrial fire.

## 11. Demo Flow

For the prototype demonstration:

1. Open the dashboard.
2. Show the thermal hotspot map.
3. Select a hotspot.
4. Show its active days.
5. Show its industrial distance.
6. Show its classification.
7. Show the reason for the classification.
8. Select an unexplained persistent hotspot when available.
9. Explain why the hotspot is flagged for further investigation.

## 12. Testing

Testing results and known issues are documented in:

```text
docs/testing.md
```

The dashboard has been tested successfully for loading the final hotspot data, displaying the map and markers, selecting hotspots, and displaying hotspot details.
