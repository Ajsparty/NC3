# Data Files

Public extracts for the Lansing Big 4 community-wealth scorecard
(MSU, GM, state government, local/regional government).

**The data files are not stored in GitHub.** They are distributed as the data package
`Data_Files.zip` and copied into this folder during installation (see
[INSTALL.md](../INSTALL.md), section 4). Git ignores `*.csv` and `*.csv.gz` here, except
`source_catalog.csv` and `scorecard_metrics_draft.csv`, which are documentation.
This folder in the repository holds the documentation and the download scripts.

Do not commit credentials or restricted data. Do not commit full LODES
state files or full ACFR PDFs. The files in this folder are filtered extracts.

## Files in this folder

| File | Source | Geography | Year | Notes |
|---|---|---|---|---|
| `qcew_2019_2025_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton, Lansing-East Lansing MSA | 2019–2025 annual | **Primary QCEW file.** 433 rows, one per area × ownership × industry × year. Adds GM detail codes `3361`, `33611`, `336111`, `3363`. MSA rows stop at 2024 (2025 MSA query returns totals only); use the sum of the 3 counties for 2025. See *QCEW suppression* below. |
| `qcew_2024_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton, Lansing-East Lansing MSA | 2024 annual | Superseded by `qcew_2019_2025_a_focus.csv`; kept for history. Prior extract. Employment and wages by ownership and selected industries. |
| `qcew_2025_a_focus.csv` | BLS QCEW | Ingham, Eaton, Clinton | 2025 annual | Superseded by `qcew_2019_2025_a_focus.csv` (values identical); kept for history. Latest annual averages, posted 2026-08-28. MSA code `C2962` returned no industry rows. |
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
| `lansing_acfr_fy2025_principal_taxpayers.csv` | City of Lansing ACFR FY2025, Table 7 (p. 189), from Lansing City Assessor | City of Lansing | tax years 2025 and 2016 | Top 10 taxpayers by taxable value, long format. GM appears twice in 2025 (`General Motors LLC` + `General Motors Co.`, flagged `big4_flag = GM`). `Ultium Cell LLC` is the former GM joint venture, now LG Energy Solution — not GM. Row sums match published totals. |
| `lansing_acfr_fy2025_principal_employers.csv` | City of Lansing ACFR FY2025, Table 15 (p. 197), from LEAP top-employers list | Greater Lansing Region | 2025 and 2016 | Top 10 employers with headcount and share of metro employment (211,208 in 2025; 229,466 in 2016). Covers State of Michigan, MSU, and GM. 2016 LCC rank is printed as 4 in the source but is 5 by count; kept as published with a note. |
| `acs_commuting_flows_2016_2020_tri.csv` | Census ACS 2016–2020 county-to-county commuting flows (table1.xlsx) | Flows with residence or workplace in Ingham, Eaton, Clinton | 2016–2020 5-year | Survey-based workers by residence county × workplace county, with MOE. Second source for local-resident job capture (W1). |
| `lodes_od_tri_workplace_2021_agg.csv.gz` | Census LODES8 OD 2021, main + aux, with block crosswalk | Workplace blocks in the 3 counties | 2021 | Jobs by workplace block × residence county / place / county subdivision, with workplace block lat/lon. Used for institution-level footprints and city-income-tax residency. Aggregated from the raw files; regenerate with `load_retention_sources.py`. |
| `load_retention_sources.py` | — | — | — | Downloads the ACS commuting flows and LODES OD files and writes the two extracts above. |
| `acs_tract_2020_2024.csv` | ACS 2020–2024 5-year (Census Reporter or Census API) | All 136 census tracts in Clinton, Eaton, Ingham | 2020–2024 | Population, median household income, poverty, tenure, median home value, asset-income households, college enrollment, unemployment — each with MOE. 2020 tract boundaries. |
| `acs_places_2015_2019_2020_2024.csv` | ACS 5-year (Census API) | 3 counties, Lansing, East Lansing, Lansing–East Lansing MSA, Michigan | 2015–2019 and 2020–2024 | Same variables plus median household income by race/ethnicity. **The 2015–2019 MSA row includes Shiawassee County** (older OMB definition); do not use it for change over time. |
| `load_benefit_sources.py` | — | — | — | Downloads the two ACS files above. Uses the official Census API when `CENSUS_API_KEY` is set, otherwise Census Reporter (no key; 2020–2024 only). |
| `lansing_gm_parcel_inventory.csv` | City of Lansing BS&A Name search 'GENERAL MOTORS' | City of Lansing (Ingham + Eaton PA 425 area) | 2026 listing | All 34 GM records: parcel type (real / personal / IFT), active or inactive, plant site, and whether detail was collected. |
| `lansing_gm_area_parcels_values.csv` | City of Lansing BS&A parcel records (manual export) | 8 parcels | tax years 2023–2026 | Assessed, SEV, taxable value. GM: Delta Township plant real property, 3 IFT-abated buildings (certificates expire 2027–2028), 3 personal-property accounts (plant equipment is 100% exempt). Plus LG Energy Solution battery plant (former GM JV, **not GM**; Renaissance Zone to 2040). These GM LLC parcels explain 89% of ACFR Table 7 'General Motors LLC' for 2025. |
| `lansing_gm_area_parcels_tax_bills.csv` | City of Lansing BS&A tax history (screenshots) | Same 8 parcels | 2019–2026 summer/winter bills | Total tax billed per bill. Implied rates: ≈77–87 mills full rate; ≈41–44 mills on IFT parcels (half rate); ≈5–8 mills on the Renaissance Zone plant. Screenshot-to-parcel matching was checked with these implied rates. |
| `source_catalog.csv` | — | — | — | Bibliography, refresh cadence, and sources that are PDF or manual export only. |
| `load_lansing_sources.py` | — | — | — | Reloads QCEW, LODES, and ACS. |

## How to refresh

```bash
pip install pandas requests lxml
python Data_Files/load_lansing_sources.py --year 2025 --qtr a
```

For the retention sources (ACS commuting flows and LODES OD):

```bash
pip install pandas requests openpyxl
python Data_Files/load_retention_sources.py
```

Raw downloads go to `Data_Files/lansing_data/raw/` and are not committed.

For the resident-outcome sources (ACS tracts and places):

```bash
# PowerShell: $env:CENSUS_API_KEY="your_key"   (do not commit keys)
python Data_Files/load_benefit_sources.py --skip-map
```

The official Census API now requires a free key (https://api.census.gov/data/key_signup.html). Without a key the script falls back to Census Reporter, which serves 2020–2024 but no longer serves 2015–2019.

The main loader writes additional large extracts under `Data_Files/lansing_data/tables/`. Those files are regenerable and are not committed.

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
- City of Lansing ACFR, year ended June 30, 2025. Tables 7 and 15 are now transcribed (see the two `lansing_acfr_fy2025_*.csv` files). Do not commit the PDF.
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
- `336` transportation equipment (GM-anchored auto cluster: GM plants plus local suppliers)
- `3361` motor vehicle manufacturing (assembly; closest public code to GM itself)
- `33611`, `336111` automobile / light-truck detail (almost always suppressed here)
- `3363` motor vehicle parts (local suppliers)
- `611` educational services
- `92` public administration
- `921` executive, legislative, and other general government

## QCEW suppression (read before analysis)

When BLS withholds a cell to protect a single employer, `disclosure_code == "N"` and
employment and wages are written as **0**. These are **not real zeros**.
Convert them to missing before any sum, average, or chart:

```python
qcew = pd.read_csv("Data_Files/qcew_2019_2025_a_focus.csv", dtype={"area_fips": str, "industry_code": str, "own_code": str})
num = ["annual_avg_emplvl", "total_annual_wages", "avg_annual_pay"]
qcew.loc[qcew["disclosure_code"] == "N", num] = float("nan")
```

What this means for GM (2019–2025 extract):

- **Eaton `3361`** is published for 2021–2025 (4,432 jobs in 2025, 5 establishments). Best public stand-in for GM Lansing Delta Township.
- **Ingham `3361`** is suppressed every year (1 establishment — GM Lansing Grand River). Stand-in: Ingham `336` minus Ingham `3363` (2025: 3,715 − 1,764 = 1,951). This residual still includes small non-GM 336 activity; label it as an estimate.
- **`3363` suppliers**: published for Ingham all years; suppressed for Eaton 2020–2025 and Clinton 2019, 2023–2025.
- Cross-check: LEAP/ACFR Table 15 lists GM at 4,549 regional employees in 2025, below the QCEW-based estimate. Report GM employment as a range, not a single number.
- Data quality flag: Clinton `336` in 2023 shows employment rising to 643 while wages fall (avg pay $54,834 vs ~$100k other years). Treat 2023 Clinton `336` as suspect.

## Commuting sources disagree (read before using LODES OD)

For jobs located in Ingham County, the share held by residents of the 3 counties is
**54% in LODES 2021** but **86% in ACS 2016–2020**. LODES assigns residence from
administrative address records (for example, a student worker's permanent family
address), while ACS records where the worker actually lives. Treat LODES as a
lower bound on local capture and ACS as the central estimate; report both.

## Parcel data notes (City of Lansing, BS&A)

- Parcels starting `33-` are Ingham real property, `23-` Eaton real property under the
  Lansing–Delta Township PA 425 agreement, `90-` personal property, `95-` IFT-abated parcels.
- GM plant equipment (personal property) shows **$0 taxable** — eligible manufacturing
  personal property is exempt under Michigan law.
- Parcel values and tax bills were transcribed by hand from BS&A screenshots and PDF
  exports on 2026-10-27. Re-check against BS&A before publishing figures.
