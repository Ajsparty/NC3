# Data Files

Public extracts for the Lansing Big 4 community-wealth scorecard
(MSU, GM, state government, local/regional government).

Do not commit credentials or restricted data.

## Files in this folder

| File | Source | Geography | Year | Notes |
|---|---|---|---|---|
| `qcew_2024_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton, Lansing-East Lansing MSA | 2024 annual | Employment and wages by ownership and selected industries |
| `lodes_wac_county_totals_2021.csv` | Census LODES WAC | Same 3 counties | 2021 | Workplace job counts by county. `C000` is total jobs |
| `acs_key_indicators_lansing.csv` | ACS via Census Reporter | MSA, 3 counties, Lansing, East Lansing | ACS 2024 5-year | Population, income, poverty, commute, selected industries |
| `load_lansing_sources.py` | -- | -- | -- | Reloads QCEW, LODES, and ACS |

## How to refresh

```bash
pip install pandas requests lxml
python Data_Files/load_lansing_sources.py --year 2024 --qtr a
```

The script writes additional large extracts under `Data_Files/lansing_data/tables/`. Those files are regenerable and are not committed.

## QCEW ownership codes

- `0` total
- `1` federal
- `2` state government (includes public universities)
- `3` local government
- `5` private

Do not add an MSU headcount on top of `own_code == 2`.

## QCEW industry stand-ins

- `10` all industries
- `31-33` manufacturing
- `336` transportation equipment (GM plant stand-in)
- `611` educational services
- `92` public administration
- `921` executive, legislative, and other general government
