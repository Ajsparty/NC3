# Notebooks

This folder contains Jupyter notebooks for exploratory analysis and visualization for the NC3 Lansing Economic Ecosystem and Community Wealth Analysis project.

## Partner Meeting Materials (November 2026)

| Notebook | Purpose |
|----------|---------|
| `NC3_Partner_Meeting_Snapshot.ipynb` | Concise, presentation-ready overview of project scope, data inventory, labor market, employment footprint, resident outcomes, Big 4 context, data gaps, and discussion questions for the Lansing Growth Fund meeting. |
| `NC3_GM_Data_Correlation.ipynb` | Focused correlation of GM regional employment (ACFR), City of Lansing taxable value, and parcel-level taxable value trends (Delta Township Assembly). Ultium/LG Energy Solution tracked separately. |
| `NC3_Lansing_Findings_Correlation.ipynb` | Combines GM footprint with tri-county ACS/QCEW indicators; descriptive cross-county correlations, city–county contrasts, and takeaways for partner discussion. |
| `NC3_Tract_Mismatch_Snapshot.ipynb` | Tract-level ACS indicators ranked by poverty and median income; starting point for neighborhood mismatch analysis near institutional sites. |

## Baseline Visualizations

`baseline_visualizations.ipynb` provides a clean starting point for testing charts and scorecard-style outputs using the public data extracts in `Data_Files/`.

## Figure export

`baseline_visualizations.ipynb` and the partner notebooks show charts inside the notebook. They do not write image files.

To export every project figure, including the charts in this folder, run `figure_instructions/reproduce_figures.ipynb`. The steps are in `figure_instructions/README.md`.

## Setup

From the repository root:

```bash
pip install -r requirements.txt
# or
conda env create -f environment.yml
conda activate nc3
```

Then:

```bash
jupyter notebook notebooks/NC3_Partner_Meeting_Snapshot.ipynb
```

Paths in the notebooks assume the repository root as the working directory (or adjust any `DATA_DIR` variable). The partner notebooks use pandas and Plotly.
