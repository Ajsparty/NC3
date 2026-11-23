# NC3 — Lansing Economic Ecosystem and Community Wealth Analysis

**Repository:** <https://github.com/Ajsparty/NC3>

An annually refreshable scorecard of how Lansing's four largest institutions — Michigan State University, General Motors, State Government, and Local and Regional Governments (the "Big 4") — affect local jobs, the tax base, and community wealth. Built with public data for the **Lansing Growth Fund** (contact: Chris Miller, <chris@nc3now.org>) as a CMSE 495 capstone project at Michigan State University.

## Start here

1. **Install** — follow [INSTALL.md](INSTALL.md): create the environment, get the data package, and run the installation test.
2. **Run the analysis, in order:**
   1. [notebooks/01_footprint.ipynb](notebooks/01_footprint.ipynb) — how big is each institution?
   2. [notebooks/02_retention.ipynb](notebooks/02_retention.ipynb) — how much of its activity stays local?
   3. [notebooks/03_benefit.ipynb](notebooks/03_benefit.ipynb) — what do residents nearby actually have?
   - **Regional and partner-meeting context:** [baseline_visualizations.ipynb](notebooks/baseline_visualizations.ipynb) (labor market, employment by ownership, income) and four notebooks prepared for the November 2026 partner meeting — GM footprint, county comparison, tract rankings, and a meeting snapshot. They are listed in [notebooks/README.md](notebooks/README.md) and can be run in any order.
3. **Reproduce every project figure** — run [figure_instructions/reproduce_figures.ipynb](figure_instructions/reproduce_figures.ipynb). Steps and the figure index are in [figure_instructions/README.md](figure_instructions/README.md).
4. **Read the results** — the report draft and presentations are in [Project_Deliverables/](Project_Deliverables/README.md).

## Testing and demo instructions

### Quick demo on GitHub

Open the [November findings report](Project_Deliverables/NC3_Findings_by_Metric.md), then use these charts to walk through the results. This demo requires no installation.

| Chart | Expected result |
| --- | --- |
| [Big 4 employment range](figure_instructions/figures/17_big4_employment_range.png) | GM's estimated 2025 employment was 4,549–6,383 jobs. |
| [Local resident capture](figure_instructions/figures/19_local_resident_capture.png) | MSU ranked highest under both methods, with 70%–89% of workers estimated to live in the three-county region. |
| [Poverty near institutional sites](figure_instructions/figures/20_poverty_near_sites.png) | Poverty was about 24% near the State Capitol and 17% near GM Grand River, compared with 12% across regional tracts outside student-dominated areas. |

### Test the full figure export locally

1. Follow [INSTALL.md](INSTALL.md) sections 1–4: create the `nc3` environment and copy the data files from the separately distributed data package into `Data_Files/`.
2. Open [figure_instructions/reproduce_figures.ipynb](figure_instructions/reproduce_figures.ipynb) in JupyterLab with the `nc3` environment. Leave `RUN_LIVE_CENSUS = False` and select **Restart Kernel and Run All Cells**.
3. Confirm that the final cell reports **21 exported figures** and prints "Figure export check passed." Check the PNGs in `figure_instructions/figures/` and compare the generated CSVs in `figure_instructions/intermediate/` with the expected results above.

## Research questions

1. **Footprint:** How large is each Big 4 institution's local economic footprint, measured with public data?
2. **Retention:** Which metrics best capture local wealth retention, employment contribution, and tax-base impact for annual tracking?
3. **Benefit:** Where do neighborhood indicators show a mismatch between institutional activity and resident economic benefit?
4. **Data gaps:** Which gaps most limit decisions, and what should the partner collect next?

## Repository structure

| Folder or file | What it contains |
| --- | --- |
| [INSTALL.md](INSTALL.md) | Installation, data, testing, and troubleshooting instructions |
| [notebooks/](notebooks/README.md) | The three analysis notebooks (run in order), their shared helper `nc3_helpers.py`, stored results in `outputs/`, and supporting notebooks |
| [figure_instructions/](figure_instructions/README.md) | One notebook that rebuilds and exports every project figure, plus the exported PNGs and the plotted tables |
| [Data_Files/](Data_Files/README.md) | Data documentation, source catalog, and download scripts. The data files themselves are distributed separately (see [INSTALL.md](INSTALL.md)) |
| [Project_Deliverables/](Project_Deliverables/README.md) | Report draft, presentations, and other official submissions |
| [environment.yml](environment.yml) | Conda environment (`requirements.txt` is the pip alternative) |
| [LICENSE](LICENSE) | MIT License |

## Data

All inputs are public: BLS QCEW and LAUS, Census ACS and LODES, IRS migration data, and City of Lansing financial and parcel records. Because data files do not change the way code does, they are not stored in GitHub; they are shared as a data package, `Data_Files.zip`. [Data_Files/README.md](Data_Files/README.md) documents every file, and [Data_Files/source_catalog.csv](Data_Files/source_catalog.csv) lists each source with its refresh schedule. No NDA or non-public data is used.

## Team

Kyle Syron, Scott Wang, K M Tausif Saadman, Aidan Swenson — CMSE 495, Fall 2026. Licensed under the [MIT License](LICENSE).
