# Data Files

Public extracts for the Lansing Big 4 community-wealth scorecard
(MSU, GM, state government, local/regional government).

Do not commit credentials or restricted data.

## Files in this folder

| File | Source | Geography | Year | Notes |
|---|---|---|---|---|
| `qcew_2024_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton, Lansing–East Lansing MSA | 2024 annual | Employment and wages by ownership and selected industries (all, manufacturing, 336, education, public administration) |
| `lodes_wac_county_totals_2021.csv` | Census LODES WAC | Same 3 counties | 2021 | Workplace job counts by county. `C000` is total jobs. |
| `acs_census_reporter_lansing.csv` | ACS via Census Reporter | MSA, 3 counties, Lansing, East Lansing | ACS 2024 | Population, income, poverty, commute, industry of workers |
| `load_lansing_sources.py` | — | — | — | Reloads QCEW, LODES, ACS, and catalogs budget/tax PDFs |

## How to refresh

```bash
pip install pandas requests lxml
python Data_Files/load_lansing_sources.py --year 2024 --qtr a --skip-docs
```

Optional keys for extra series:

```bash
export CENSUS_API_KEY=...
export BLS_API_KEY=...
export BEA_API_KEY=...
```

The script writes additional large extracts (full QCEW, block-level LODES) next to itself under `lansing_data/tables/`. Those files are not committed because they are regenerable and large.

## QCEW ownership codes

- `0` total
- `1` federal
- `2` state government
- `3` local government
- `5` private

State government employment in QCEW includes public universities. Do not add an MSU headcount on top of `own_code == 2`.

## QCEW industry stand-ins

- `10` all industries
- `31-33` manufacturing
- `336` transportation equipment (GM plant stand-in)
- `611` educational services
- `92` public administration
- `921` executive, legislative, and other general government

## LODES columns used for wealth retention

- `C000` total jobs
- `CE01` / `CE02` / `CE03` jobs by earnings band
- `CNS*` jobs by NAICS sector
