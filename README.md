# NC3 — Lansing Economic Ecosystem and Community Wealth Analysis

Workspace for analysis of Lansing's economic ecosystem and community wealth with the Lansing Growth Fund. This repository holds project documents, deliverables, working files, and data used to estimate how Lansing's largest institutional actors affect local jobs, the tax base, and community wealth retention.
## INSTALL INSTRUCTIONS
Head to the INSTALL.md file to see the install instructions before reading forward

## Figure Reproducibility

Every project figure has a step-by-step instruction notebook in [`figures/`](figures/README.md). The figure index there lists each figure, the notebook that rebuilds it, its input data, and where it is used. To reproduce Figure 1 after installing the environment, run from the repository root:

```bash
jupyter nbconvert --to notebook --execute --inplace figures/fig01_big4_employment_range.ipynb
```

## Project Overview

The project produces a practical, annually refreshable scorecard for Lansing's four largest institutional actors (the "Big 4"):

- Michigan State University (MSU)
- General Motors (GM)
- State Government
- Local and Regional Governments

The goal is to estimate how each institution affects local employment, the tax base, and local wealth retention using public indicators and clearly labeled stand-in measures when direct data are unavailable. The primary outcome is a partner-ready scorecard and dashboard that can guide strategy discussions and future data collection.

A lightweight GIS layer that shows where economic pressure and institutional presence may overlap is a stretch goal if time allows.

## Recent Partner Materials (November 2026)

The following notebooks in `notebooks/` are ready for the Lansing Growth Fund meeting:

- `NC3_Partner_Meeting_Snapshot.ipynb` — project overview, data inventory, key indicators, gaps, and discussion questions
- `NC3_GM_Data_Correlation.ipynb` — GM employment, taxable value, and parcel trends
- `NC3_Lansing_Findings_Correlation.ipynb` — combined GM + tri-county correlations and takeaways
- `NC3_Tract_Mismatch_Snapshot.ipynb` — tract-level poverty and income rankings

Supporting files:
- `Data_Files/scorecard_metrics_draft.csv` — candidate scorecard metrics
- `Data_Files/next_sources.md` — notes on QWI, PSEO, USASpending, HUD CHAS, Opportunity Atlas
- `Team_Management_Files/20261104_NC3_PartnerMeetingNotes.md` — meeting notes skeleton

## Community Partner

**Lansing Growth Fund** is a community-focused organization seeking to strengthen economic development, local investment, and community wealth creation in the Lansing region. The partner is interested in how capital, purchasing power, employment, taxation, and institutional investments flow through the local economy and how those flows affect community development and long-term economic resilience.

**Primary contact:** Chris Miller, [chris@nc3now.org](mailto:chris@nc3now.org)

**Advisory team:** TBD

## Research Questions

1. How can we estimate and compare the local economic footprint of each Big 4 institution using publicly available data and clear stand-in measures when direct measures are unavailable?
2. Which scorecard metrics best represent local wealth retention, employment contribution, and tax-base impact for annual tracking?
3. Where do neighborhood-level indicators suggest mismatch between institutional economic activity and resident-level economic benefit?
4. Which data gaps most limit decision quality, and what should the partner prioritize collecting next?

## Repository Structure

This repository is the main organizational space for the NC3 analysis. Keep the folder structure clear so collaborators can find files quickly.

| Folder | Purpose |
| --- | --- |
| `Team_Management_Files/` | Team Charter, meeting notes, weekly 3x3 reports, and signed agreements |
| `Project_Deliverables/` | Official submissions such as proposals, presentations, videos, and the final report |
| `Individual_TeamMember_files/` | Individual working files and drafts |
| `Data_Files/` | Datasets and other project data files |
| `figures/` | Figure reproducibility notebooks and exported figures (see `figures/README.md`) |
| `notebooks/` | Shared analysis and partner-meeting notebooks |

## File Naming Standards

- Use clear and descriptive file names.
- Use the date format **YYYYMMDD** when a date is helpful.
- Use each team member's **MSU NetID** for individually authored files.
- Use **NC3** for files that represent the whole team.
- Avoid vague names such as `final.docx`, `newfile.docx`, or `document1.docx`.

Example:

```text
20260913_NC3_MeetingNotes.docx
```

## Data and Methods

The work follows a standard data-science pipeline: collection and generation, cleaning and munging, analysis, and visualization.

### Sources

The project relies primarily on public and partner-accessible datasets that can be refreshed on a yearly cycle. Expected sources include:

- U.S. Census and American Community Survey (ACS)
- Bureau of Labor Statistics (BLS) employment indicators
- Local tax and property datasets
- Public institutional budget and procurement disclosures
- Regional economic-development data resources

Prefer sources that are stable, well documented, and reproducible so the scorecard can be maintained ongoing. Proprietary data may be used only when access is reliable and definitions support recurring updates.

The team should maintain a **data bibliography** that records datasets, source links, update cadence, geographic coverage, and key field notes. At a minimum, the bibliography should start with Census-based sources that anchor the public-data baseline.

### Cleaning

Data preparation focuses on making multiple public sources analytically consistent:

- Harmonize time periods
- Standardize geographic units
- Align organization and entity naming
- Resolve missing or inconsistent values across employment, tax, and institutional indicators

For the GIS component, prepare a small set of geocoded layers tied to neighborhood or tract-level boundaries. Document cleaning decisions so partner staff can understand assumptions and repeat the workflow.

### Analysis approach

This project uses descriptive and comparative analytics rather than predictive modeling. The scorecard combines institution-level indicators, citywide context indicators, and a small set of neighborhood-level map indicators.

Appropriate methods include scaling indicators to comparable ranges, year-over-year trend analysis, simple concentration measures, and clearly documented summary scoring when useful.

Implementation should follow a three-tier architecture:

1. **Data tier (ETL):** extract, transform, and load source data; standardize fields and run quality checks.
2. **Application / logic tier:** compute scorecard indicators, trends, and summary metrics.
3. **Presentation tier:** generate dashboard tables and charts and export outputs for reports or partner systems.

### Visualizations

Core outputs should include a Big 4 comparison scorecard and a short set of trend charts. Keep the visualization package compact and presentation-ready. A dashboard and light GIS views are stretch goals.

## Deliverables

Required deliverables:

- Big 4 local economic footprint scorecard
- Concise analytic report describing methods and findings
- Reproducible workflow to support annual refresh
- Reproducible code, data dictionaries, and partner-facing documentation
- Initial data bibliography beginning with Census sources
- Stakeholder presentation summarizing key indicators, neighborhood context, data limitations, and recommended next steps

Stretch goals:

- Lightweight dashboard
- Companion GIS visuals

## Tools and Software

- **Primary language:** Python for data integration, indicator calculation, and reproducible analysis
- **Optional:** SQL for structured joins and aggregation
- **Notebooks:** Jupyter for exploratory work and stakeholder-facing narratives
- **GIS:** QGIS or equivalent Python geospatial libraries
- **Dashboard:** Tableau, Power BI, or a comparable platform selected with the partner based on usability and maintenance constraints

## Project Risks and Backup Plan

The largest risk is scope expansion beyond what the team can complete with available data. Additional risks include limited access to proprietary institutional information and inconsistent definitions across public data sources.

**Backup plan:** prioritize a public-data baseline scorecard with a documented methodology and a limited set of high-value indicators. If deeper institutional data cannot be obtained in time, still deliver a reproducible pipeline, a usable core scorecard, and explicit recommendations for future data partnerships. Treat dashboard expansion and GIS features as stretch goals.

## NDA and Intellectual Property

No NDA or IP agreement is currently expected. If non-public institutional data are introduced, clarify data access and sharing terms with the partner before use.

This repository is licensed under the [MIT License](LICENSE).

## README Maintenance

Update this README whenever the team adds, removes, or reorganizes major folders or important project files. Keep the folder structure clear so collaborators can quickly find what they need.
