# Data Files

Public extracts for the Lansing Big 4 community-wealth scorecard
(MSU, GM, state government, local/regional government).

Do not commit credentials or restricted data. Do not commit full LODES
state files or full ACFR PDFs. The files in this folder are filtered extracts.

## Files in this folder

| File | Source | Geography | Year | Notes |
|---|---|---|---|---|
| `qcew_2024_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton, Lansing-East Lansing MSA | 2024 annual | Prior extract. Employment and wages by ownership and selected industries. |
| `qcew_2025_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton | 2025 annual | Latest annual averages, posted 2026-08-28. MSA code `C2962` returned no industry rows. |
| `lodes_wac_county_totals_2021.csv` | Census LODES WAC | Same 3 counties | 2021 | Workplace job counts. `C000` is total jobs. |
| `lodes_od_county_2021.csv` | Census LODES OD | Tri-county workplace or residence | 2021 | Origin-destination job counts. Latest Michigan year. 2022 and 2023 releases exclude Michigan. |
| `acs_key_indicators_lansing.csv` | ACS via Census Reporter | MSA, 3 counties, Lansing, East Lansing | prior extract | Kept for comparison with the 2024 file. |
| `acs_2024_key_indicators.csv` | ACS 2024 5-year via Census Reporter | Same geographies | 2020-2024 | Population, income, poverty, commute, employment, tenure, rent burden. |
| `irs_soi_migration_ingham_eaton_clinton_2022_2023.csv` | IRS SOI | Ingham, Eaton, Clinton | 2022-2023 | Inflow and outflow of returns, exemptions, and AGI. AGI is in thousands. New matching method; do not splice to older years without a note. |
| `bea_cagdp2_counties_2019_2024.csv` | BEA CAGDP2 | 3 counties | 2019-2024 | Real GDP by county and industry. Next county release 2026-12-02. |
| `bea_cainc1_counties_2019_2024.csv` | BEA CAINC1 | 3 counties | 2019-2024 | Personal income, population, per capita personal income. |
| `cbp_2023_focus.csv` | Census CBP | 3 counties | 2023 | Establishments, employment, payroll for all industries, manufacturing, 336, 611, and 92. 2024 CBP is delayed. |
| `laus_lansing_msa_2019_latest.csv` | BLS LAUS | Lansing-East Lansing MSA | 2019-2026 M08 | Not seasonally adjusted labor force, employment, unemployment, and rate. August 2026 is the latest month in this extract. |
| `ipeds_msu_171100_slim.csv` | IPEDS via Urban Institute | MSU unit 171100 | directory 2023, finance 2022 | Institution-level finance and FTE. Do not add on top of QCEW `own_code == 2`. |
| `ipeds_msu_salaries_2023.csv` | IPEDS instructional staff salaries | MSU | 2023 | Staff counts and salary outlays by rank, contract, and sex. |
| `source_catalog.csv` | — | — | — | Bibliography, refresh cadence, and sources that are PDF or manual export only. |
| `load_lansing_sources.py` | — | — | — | Reloads QCEW, LODES, and ACS. |

## How to refresh

```bash
pip install pandas requests lxml
python Data_Files/load_lansing_sources.py --year 2025 --qtr a
```

The script writes additional large extracts under `Data_Files/lansing_data/tables/`. Those files are regenerable and are not committed.

Annual replacements that are not in the loader:

- QCEW: same API pattern, year `2025`, quarter `a`.
- ACS: Census Reporter `latest`, or Census API `2024/acs/acs5` when a key is available.
- IRS: `countyinflow2223.csv` and `countyoutflow2223.csv` from irs.gov/pub/irs-soi.
- BEA: `CAGDP2.zip` and `CAINC1.zip` from apps.bea.gov/regional/zip.
- LAUS: `la.data.60.Metro`, series `LAUMT262962000000003` through `000006`.
- CBP: `cbp23co.zip` from www2.census.gov.
- IPEDS: Urban Institute Education Data Portal, unit ID `171100`.

## Not committed, still in the catalog

These are annual and official, but they are portal exports or PDFs:

- Michigan Treasury STC Taxable Valuation, 2025, county reports for Ingham, Eaton, and Clinton.
- City of Lansing ACFR, year ended June 30, 2025. Transcribe the statistical tax tables only.
- Michigan Civil Service Commission 46th Annual Workforce Report, FY 2024-25.
- MSU state transparency reports for FY2026, used as a cross-check on IPEDS.

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
