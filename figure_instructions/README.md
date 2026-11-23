# Figure instructions

[reproduce_figures.ipynb](reproduce_figures.ipynb) is the instruction file for every figure in the NC3 project. It reads the data package and the stored analysis results, rebuilds each figure, and exports it as a PNG.

Back to the [README](../README.md).

## Before you run it

Complete [INSTALL.md](../INSTALL.md) sections 1–4: environment created and active, data package copied into `Data_Files/`.

## Run

From the repository root, with `nc3` active:

```bash
jupyter nbconvert --to notebook --execute --inplace figure_instructions/reproduce_figures.ipynb
```

or start `jupyter lab`, open this notebook, and choose **Kernel → Restart Kernel and Run All Cells**.

A run takes about a minute, needs no internet, and ends with **"Figure export check passed."**

## What the run writes

| Path | Contents |
| --- | --- |
| [figures/](figures/) | One PNG per figure, `01_` to `21_` |
| [intermediate/](intermediate/) | The table each figure plots, plus `figure_index.csv` (every figure, what it shows, where it is used) |

## Which figures come from where

| Figures | Source notebook | Role |
| --- | --- | --- |
| 17–21 | [01_footprint](../notebooks/01_footprint.ipynb), [02_retention](../notebooks/02_retention.ipynb), [03_benefit](../notebooks/03_benefit.ipynb) | Main analysis figures, used in the report and presentations |
| 01–04 | [baseline_visualizations](../notebooks/baseline_visualizations.ipynb) | Baseline regional context |
| 05–16 | Partner-meeting notebooks in [notebooks/](../notebooks/README.md) | Charts shown at the November 2026 partner meeting |

Figures 17–21 read the analysis results stored in [notebooks/outputs/](../notebooks/outputs/). To rebuild those results first, run notebooks 01, 02, and 03 in order ([INSTALL.md](../INSTALL.md) section 6), then re-run this notebook.

Figure 22 is an optional live Census API chart. It is off by default (`RUN_LIVE_CENSUS = False` in the setup cell) and needs internet and a Census API key in the `CENSUS_API_KEY` environment variable ([INSTALL.md](../INSTALL.md) section 8).
