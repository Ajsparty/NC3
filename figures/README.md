# Figures

Every figure used in NC3 presentations, videos, and reports has its own instruction notebook in this folder. Running a notebook from top to bottom rebuilds the figure from the data in `Data_Files/` and saves it here.

## Figure index

| # | Figure | Instructions | Output | Used in | Inputs |
|---|---|---|---|---|---|
| 1 | Big 4 direct employment in the Lansing region, 2025 (low–high range chart) | [`fig01_big4_employment_range.ipynb`](fig01_big4_employment_range.ipynb) | `fig01_big4_employment_range.png`, `fig01_big4_employment_range_data.csv` | Storyboard update slide 5; MVP video, Finding 1; final report, Footprint section | `Data_Files/qcew_2019_2025_a_focus.csv`, `Data_Files/lansing_acfr_fy2025_principal_employers.csv` |

## How to reproduce a figure

1. Install the project environment by following [`INSTALL.md`](../INSTALL.md) (`conda env create --file environment.yml`, then `conda activate nc3`).
2. From the repository root, run the figure's notebook:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace figures/fig01_big4_employment_range.ipynb
   ```

   Or open it in JupyterLab and choose **Kernel → Restart Kernel and Run All Cells**.
3. The PNG and a CSV of the plotted values are written to this folder. The last step of each notebook compares your numbers with the published figure.

No internet connection or API key is needed: the input files are committed in `Data_Files/`. Each notebook explains how to re-download its data from the original source.

## Adding a new figure

Copy an existing notebook, rename it `figNN_short_description.ipynb` (no spaces), and keep the same steps:

1. What the figure shows and where it is used
2. Install link
3. Input data: file, original source, and how to regenerate it
4. Paths and input checks
5. Loading and cleaning
6. Calculations
7. Drawing the figure
8. Labels and formatting
9. Export and result check

Then add a row to the figure index above.
