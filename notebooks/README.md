# Notebooks

Back to the [README](../README.md). Set up the environment and data first with [INSTALL.md](../INSTALL.md).

## Main analysis — run in this order

| Order | Notebook | Question | Results written to `outputs/` |
| --- | --- | --- | --- |
| 1 | [01_footprint.ipynb](01_footprint.ipynb) | How big is each Big 4 institution in the regional economy? | `footprint_*.csv` |
| 2 | [02_retention.ipynb](02_retention.ipynb) | How much of its wages, purchasing, and taxes stays local? | `retention_*.csv` |
| 3 | [03_benefit.ipynb](03_benefit.ipynb) | What do residents nearby actually have, and where is the mismatch? | `benefit_*.csv` |

All three import [nc3_helpers.py](nc3_helpers.py), which holds the shared loading, suppression handling, and geography definitions. [outputs/](outputs/) stores their results so the figures can be rebuilt without re-running the analysis. Notebook 03 needs one extra public file; see [INSTALL.md](../INSTALL.md) section 4.

## Supporting notebooks

These are not part of the main sequence. Their charts are exported, together with all other project figures, by [figure_instructions/reproduce_figures.ipynb](../figure_instructions/reproduce_figures.ipynb).

| Notebook | Purpose |
| --- | --- |
| [baseline_visualizations.ipynb](baseline_visualizations.ipynb) | First baseline charts: unemployment, employment by ownership, industry stand-ins, median income. The last section is an optional Census API example that needs a key. |
| [NC3_Partner_Meeting_Snapshot.ipynb](NC3_Partner_Meeting_Snapshot.ipynb) | Overview prepared for the November 2026 partner meeting |
| [NC3_GM_Data_Correlation.ipynb](NC3_GM_Data_Correlation.ipynb) | GM employment, taxable value, and parcel trends for the partner meeting |
| [NC3_Lansing_Findings_Correlation.ipynb](NC3_Lansing_Findings_Correlation.ipynb) | GM and tri-county comparison for the partner meeting (three counties only, so correlations are descriptive) |
| [NC3_Tract_Mismatch_Snapshot.ipynb](NC3_Tract_Mismatch_Snapshot.ipynb) | Tract rankings by poverty and income, an early version of the mismatch analysis in notebook 03 |

The partner-meeting notebooks include some summary values typed into the notebook for the meeting. The analysis notebooks and the figure notebook read every value from the data package.
