# Figure instructions

This folder holds the instructions for every figure in the NC3 project.
The instruction file is `reproduce_figures.ipynb`.

Install the project first. Follow `../INSTALL.md` through the environment and data sections.
The data files this notebook reads are already in `Data_Files/`.

## Run

From the repository root, with the `nc3` environment active:

```bash
jupyter lab
```

Open `figure_instructions/reproduce_figures.ipynb`.
Select the **Python (NC3)** kernel.
Use **Kernel → Restart Kernel and Run All Cells**.

The notebook finds the repository root by walking upward until it sees `Data_Files/` and `INSTALL.md`.
You can start Jupyter from the repository root or from this folder.

A normal run finishes in about a minute. It does not download data.

## What the run writes

| Path | What it is |
| --- | --- |
| `figures/` | One PNG per figure. Files are named `01_` through `21_`. |
| `intermediate/` | The table plotted in each figure, plus `figure_index.csv`. |

The last cell prints the file list and checks that 21 figures were written.

Figure 22 is the optional live Census API chart from `notebooks/baseline_visualizations.ipynb`.
It stays off unless you set `RUN_LIVE_CENSUS = True` in the setup cell. That call needs internet and no API key.

## Where the figures are used

The notebook's first section is the index. In short:

- Figures 01–04 are the four charts in the `INSTALL.md` demo and in `notebooks/baseline_visualizations.ipynb`.
- Figures 05–16 are the partner-meeting charts in `notebooks/`. Those notebooks display Plotly charts and do not save image files. This notebook exports the same series as PNG.
- Figures 17–21 are the scorecard charts in `Individual_TeamMember_files/wangz153/`. They read the CSVs already stored in `wangz153/outputs/`.

## If a scorecard CSV is missing

Skip this unless `reproduce_figures.ipynb` stops and names a file under `wangz153/outputs/`.

Those CSVs are the intermediate results of the scorecard notebooks. To rebuild them, run all cells in this order:

1. `Individual_TeamMember_files/wangz153/01_footprint.ipynb`
2. `Individual_TeamMember_files/wangz153/02_retention.ipynb`
3. `Individual_TeamMember_files/wangz153/03_benefit.ipynb`

Then re-run `reproduce_figures.ipynb`.
Notebook 02 reads `Data_Files/lodes_od_tri_workplace_2021_agg.csv.gz`, which is already in the repository.
That rebuild takes several minutes. A normal review uses the stored CSVs and skips it.
