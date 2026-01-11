# Feature Inventory

## Purpose
This document provides a feature-level audit of all variables retained for modeling.
Each feature is reviewed in terms of type, missingness, preprocessing strategy,
and potential risks (e.g. leakage, proxy effects).

This inventory serves as the authoritative reference for preprocessing and
feature engineering decisions.

---

## 1. Identifiers & Target

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|-------|----------|--------------|---------|----------|-------|
| Order | int64 | identifier | none | drop | Row order identifier |
| PID | int64 | identifier | none | drop | Parcel identifier |
| SalePrice | int64 | target | none | target | Target variable |

---

## 2. Temporal & Transaction Variables (Excluded)

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|-------|----------|--------------|---------|----------|-------|
| Mo Sold | int64 | temporal | none | drop | Temporal leakage risk |
| Yr Sold | int64 | temporal | none | drop | Temporal leakage risk |
| Sale Type | object | categorical | none | drop | Transaction-specific |
| Sale Condition | object | categorical | none | drop | Transaction-specific |

---

## 3. Ordinal Categorical Variables

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|--------|----------|--------------|---------|----------|-------|
| Overall Qual | int64 | ordinal | none | keep | Overall material and finish quality (1–10) |
| Overall Cond | int64 | ordinal | none | keep | Overall condition rating (1–10) |
| Exter Qual | object | ordinal | none | encode_ordinal | Exterior material quality |
| Exter Cond | object | ordinal | none | encode_ordinal | Exterior condition |
| Bsmt Qual | object | ordinal | low | encode_ordinal | Basement quality; missing = no basement |
| Bsmt Cond | object | ordinal | low | encode_ordinal | Basement condition; missing = no basement |
| Bsmt Exposure | object | ordinal | low | encode_ordinal | Basement exposure; missing = no basement |
| BsmtFin Type 1 | object | ordinal | low | encode_ordinal | Basement finished area type |
| BsmtFin Type 2 | object | ordinal | low | encode_ordinal | Secondary basement finish |
| Heating QC | object | ordinal | none | encode_ordinal | Heating quality |
| Kitchen Qual | object | ordinal | none | encode_ordinal | Kitchen quality |
| Functional | object | ordinal | none | encode_ordinal | Home functionality rating |
| Fireplace Qu | object | ordinal | moderate | encode_ordinal | Fireplace quality; missing = no fireplace |
| Garage Finish | object | ordinal | low | encode_ordinal | Garage finish level; missing = no garage |
| Garage Qual | object | ordinal | low | encode_ordinal | Garage quality; missing = no garage |
| Garage Cond | object | ordinal | low | encode_ordinal | Garage condition; missing = no garage |
| Land Slope | object | ordinal | none | encode_ordinal | Slope of property |
| Lot Shape | object | ordinal | none | encode_ordinal | Regularity of lot shape |
| Paved Drive | object | ordinal | none | encode_ordinal | Driveway paving quality |

---

## 4. Numeric Continuous Variables

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|-------|----------|--------------|---------|----------|-------|
| Lot Frontage | float64 | numeric | moderate | impute | Linear feet of street frontage |
| Lot Area | int64 | numeric | none | keep | Lot size in square feet |
| Mas Vnr Area | float64 | numeric | low | impute | Masonry veneer area; missing = none |
| BsmtFin SF 1 | float64 | numeric | low | impute | Finished basement area (type 1) |
| BsmtFin SF 2 | float64 | numeric | low | impute | Finished basement area (type 2) |
| Bsmt Unf SF | float64 | numeric | low | impute | Unfinished basement area |
| Total Bsmt SF | float64 | numeric | low | keep | Total basement area |
| 1st Flr SF | int64 | numeric | none | keep | First floor living area |
| 2nd Flr SF | int64 | numeric | none | keep | Second floor living area |
| Low Qual Fin SF | int64 | numeric | none | keep | Low quality finished area |
| Gr Liv Area | int64 | numeric | none | keep | Above ground living area |
| Bsmt Full Bath | float64 | numeric | low | impute | Basement full bathrooms |
| Bsmt Half Bath | float64 | numeric | low | impute | Basement half bathrooms |
| Full Bath | int64 | numeric | none | keep | Full bathrooms above grade |
| Half Bath | int64 | numeric | none | keep | Half bathrooms above grade |
| Bedroom AbvGr | int64 | numeric | none | keep | Bedrooms above grade |
| Kitchen AbvGr | int64 | numeric | none | keep | Kitchens above grade |
| TotRms AbvGrd | int64 | numeric | none | keep | Total rooms above grade |
| Fireplaces | int64 | numeric | none | keep | Number of fireplaces |
| Garage Cars | float64 | numeric | low | impute | Garage capacity |
| Garage Area | float64 | numeric | low | impute | Garage size in square feet |
| Wood Deck SF | int64 | numeric | none | keep | Wood deck area |
| Open Porch SF | int64 | numeric | none | keep | Open porch area |
| Enclosed Porch | int64 | numeric | none | keep | Enclosed porch area |
| 3Ssn Porch | int64 | numeric | none | keep | Three-season porch area |
| Screen Porch | int64 | numeric | none | keep | Screen porch area |
| Pool Area | int64 | numeric | none | keep | Pool area (mostly zero) |
| Misc Val | int64 | numeric | none | keep | Value of miscellaneous features |

---

## 5. Nominal Categorical Variables

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|-------|----------|--------------|---------|----------|-------|
| MS Zoning | object | categorical | none | one_hot | General zoning classification |
| Street | object | categorical | none | one_hot | Type of road access |
| Land Contour | object | categorical | none | one_hot | Flatness of property |
| Utilities | object | categorical | none | one_hot | Type of utilities available |
| Lot Config | object | categorical | none | one_hot | Lot configuration |
| Neighborhood | object | categorical | none | one_hot | Physical location within city |
| Condition 1 | object | categorical | none | one_hot | Proximity to main road or railroad |
| Condition 2 | object | categorical | none | one_hot | Secondary proximity condition |
| Bldg Type | object | categorical | none | one_hot | Type of dwelling |
| House Style | object | categorical | none | one_hot | Style of dwelling |
| Roof Style | object | categorical | none | one_hot | Roof style |
| Roof Matl | object | categorical | none | one_hot | Roof material |
| Exterior 1st | object | categorical | none | one_hot | Exterior covering |
| Exterior 2nd | object | categorical | none | one_hot | Secondary exterior covering |
| Mas Vnr Type | object | categorical | moderate | one_hot | Masonry veneer type; missing = none |
| Foundation | object | categorical | none | one_hot | Foundation type |
| Heating | object | categorical | none | one_hot | Heating type |
| Central Air | object | categorical | none | one_hot | Central air conditioning |
| Electrical | object | categorical | low | one_hot | Electrical system |
| Garage Type | object | categorical | low | one_hot | Garage type; missing = no garage |

## 6. Dropped Features (by Design)

The following features are excluded entirely from the modeling pipeline
based on data quality decisions documented in Issue #4.
They are listed here for completeness and traceability.

| Column | Raw Type | Feature Type | Missing | Strategy | Notes |
|-------|----------|--------------|---------|----------|-------|
| Pool QC | object | ordinal | structural | drop | Extremely rare feature (≈99% missing) |
| Alley | object | categorical | structural | drop | Rare access feature |
| Fence | object | categorical | structural | drop | Rare perimeter feature |
| Misc Feature | object | categorical | structural | drop | Rare miscellaneous feature |




