# THERMALGUARD — Testing Report

## 1. Testing Overview

The prototype was tested after integrating the persistence, industrial context, classification, integration, and dashboard components.

The purpose of testing was to verify that the processed hotspot data could be displayed correctly through the Streamlit dashboard and that hotspot information could be selected and viewed.

## 2. Dashboard Testing

The following components were tested:

| Component                            | Result |
| ------------------------------------ | ------ |
| Dashboard starts                     | PASS   |
| THERMALGUARD title displayed         | PASS   |
| Summary numbers displayed            | PASS   |
| Hotspot map displayed                | PASS   |
| Hotspot markers displayed            | PASS   |
| Hotspot table displayed              | PASS   |
| Hotspot selection dropdown           | PASS   |
| Selected hotspot information updates | PASS   |
| Classification displayed             | PASS   |
| Active days displayed                | PASS   |
| Detection count displayed            | PASS   |
| Industrial distance displayed        | PASS   |
| Reason displayed                     | PASS   |

## 3. Issue Found and Fixed

### Issue: Industrial distance displayed as N/A

The final hotspot CSV uses the column:

`distance_to_industry_km`

The dashboard was initially checking for a different column name, causing the distance to appear as `N/A`.

### Fix

The dashboard was updated to read the `distance_to_industry_km` column.

### Result

Industrial distance is now displayed correctly for the selected hotspot.

## 4. Data Observation

The current processed hotspot dataset contains 22 hotspots.

The current dataset contains hotspots with `active_days = 1`. Therefore, the current processed data does not provide sufficient repeated-hotspot examples to independently demonstrate all four persistence/classification scenarios required for the final demo.

The existing classification and persistence outputs should therefore be verified against the team's intended test scenarios before the final demonstration.

## 5. Pipeline Testing

The persistence script was tested using:

```bash
python scripts/persistence.py
```

The script currently expects:

```text
data/processed/firms_clean.csv
```

This file was not present in the repository, resulting in a `FileNotFoundError`.

The repository should therefore include the FIRMS cleaning step/output or document the correct data-generation workflow before claiming that the complete pipeline can be reproduced from a fresh clone.

## 6. Dashboard Run Command

The dashboard was successfully launched from the project root using:

```bash
python -m streamlit run app/dashboard.py
```

The dashboard opened successfully in the browser.

## 7. Conclusion

The Streamlit dashboard and integrated final hotspot data were successfully tested.

The dashboard displays hotspot locations, classifications, persistence-related information, industrial distance, and hotspot reasons.

Before the final prototype is declared fully reproducible, the missing FIRMS cleaning step and the four required classification scenarios should be verified.
