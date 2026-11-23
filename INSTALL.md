# NC3 Installation and Setup Guide

This guide explains how an authorized project collaborator can create the NC3 Python environment, test the installation, prepare the data files, reproduce the project figures, and run the analysis notebooks.

## 1. System requirements

Install the following software before beginning:

- [Git](https://git-scm.com/downloads)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) or Anaconda
- Access to the private NC3 GitHub repository

The project environment uses **Python 3.9.20**. The required Python packages are listed in `environment.yml`, which is the authoritative environment definition. `requirements.txt` lists the same packages with minimum versions for collaborators who use `pip` instead of Conda; Conda users can ignore it.

## 2. Clone the repository

Open PowerShell, Git Bash, Anaconda Prompt, or another terminal and run:

```bash
git clone https://github.com/Ajsparty/NC3.git
cd NC3
```

Because the repository is private, GitHub may require an authorized account, a personal access token, or another configured authentication method.

If the repository has already been cloned, update the local `main` branch before continuing:

```bash
git switch main
git pull --ff-only origin main
```

Do not use force-pull or hard-reset commands when the working tree contains uncommitted work.

## 3. Create the Conda environment

From the repository root, run:

```bash
conda env create --file environment.yml
```

Activate the environment:

```bash
conda activate nc3
```

If `conda activate` fails in Windows PowerShell, see *Troubleshooting* (section 9) or use **Anaconda Prompt** instead.

Optionally register it as a named Jupyter kernel:

```bash
python -m ipykernel install --user --name nc3 --display-name "Python (NC3)"
```

To confirm the active Python version, run:

```bash
python --version
```

The expected output is:

```text
Python 3.9.20
```

## 4. Test the installation

With the `nc3` environment active, confirm that the core packages import correctly:

```bash
python -c "import pandas, numpy, matplotlib, openpyxl; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| matplotlib', matplotlib.__version__)"
```

The command should print three version numbers (pandas 2.2.x, numpy 1.26.4, matplotlib 3.9.x) and no errors.

Then run the Figure 1 demo from the repository root. It uses only data already committed in `Data_Files/` and needs no internet connection or API key:

```bash
jupyter nbconvert --to notebook --execute --inplace figures/fig01_big4_employment_range.ipynb
```

A successful run takes under 10 seconds, writes `figures/fig01_big4_employment_range.png`, and ends with the message **"All values match the published figure."** If this works, the installation is complete.

## 5. Data files

All Data files are included in the attatched email.

### Which files each part of the project uses

| Notebook | Input files in `Data_Files/` | Extra download needed? |
| --- | --- | --- |
| `figures/fig01_big4_employment_range.ipynb` | `qcew_2019_2025_a_focus.csv`, `lansing_acfr_fy2025_principal_employers.csv` | No |
| `Individual_TeamMember_files/wangz153/01_footprint.ipynb` | `qcew_2019_2025_a_focus.csv`, `lansing_acfr_fy2025_principal_employers.csv` | No |
| `Individual_TeamMember_files/wangz153/02_retention.ipynb` | `qcew_2019_2025_a_focus.csv`, `lodes_od_tri_workplace_2021_agg.csv.gz`, `acs_commuting_flows_2016_2020_tri.csv`, `lansing_acfr_fy2025_principal_taxpayers.csv`, `lansing_gm_area_parcels_values.csv`, `lansing_gm_area_parcels_tax_bills.csv`, `irs_soi_migration_ingham_eaton_clinton_2022_2023.csv` | No |
| `Individual_TeamMember_files/wangz153/03_benefit.ipynb` | `acs_tract_2020_2024.csv`, `acs_places_2015_2019_2020_2024.csv`, `lodes_od_tri_workplace_2021_agg.csv.gz` | **Yes** — the LODES block crosswalk (below) |
| `notebooks/baseline_visualizations.ipynb` | `laus_lansing_msa_2019_latest.csv`, `qcew_2024_a_focus.csv`, `acs_2024_key_indicators.csv` | No (optional Census request at the end) |

Keep filenames and folder locations unchanged unless the notebook that reads them is updated at the same time.

### Extra download for `03_benefit.ipynb`

Notebook 03 locates each census tract using the Census LODES block crosswalk (`mi_xwalk.csv.gz`, about 4.5 MB). It is a public file but is not committed. Download it once into `Data_Files/lansing_data/raw/`.

PowerShell (from the repository root):

```powershell
New-Item -ItemType Directory -Force Data_Files/lansing_data/raw | Out-Null
Invoke-WebRequest https://lehd.ces.census.gov/data/lodes/LODES8/mi/mi_xwalk.csv.gz -OutFile Data_Files/lansing_data/raw/mi_xwalk.csv.gz
```

macOS / Linux / Git Bash:

```bash
mkdir -p Data_Files/lansing_data/raw
curl -L -o Data_Files/lansing_data/raw/mi_xwalk.csv.gz https://lehd.ces.census.gov/data/lodes/LODES8/mi/mi_xwalk.csv.gz
```

Running `python Data_Files/load_retention_sources.py` (section 8) also downloads this file.

## 6. Reproduce the project figures

Every figure used in presentations, videos, and reports has an instruction notebook in `figures_instructions/`. The figure index in [`figures_instructions/README.md`](figures_instructions/README.md) lists each figure, its notebook, its inputs, and where it is used.

To reproduce a figure, either run it from the repository root:

```bash
jupyter nbconvert --to notebook --execute --inplace figures_instructions/fig01_big4_employment_range.ipynb
```

or open it in JupyterLab and choose **Kernel → Restart Kernel and Run All Cells**. Each figure notebook ends by comparing your numbers with the published figure.

## 7. Run the analysis notebooks

From the repository root, with the `nc3` environment active, run:

```bash
jupyter lab
```

Select **Python (NC3)** as the kernel if it is not selected automatically, then use **Kernel → Restart Kernel and Run All Cells**.

| Notebook | What it does | Expected result |
| --- | --- | --- |
| `Individual_TeamMember_files/wangz153/01_footprint.ipynb` | Footprint: jobs, share of regional jobs, relative pay, and trends for the Big 4 | Range chart and trend chart; CSV files written to `Individual_TeamMember_files/wangz153/outputs/footprint_*.csv` |
| `Individual_TeamMember_files/wangz153/02_retention.ipynb` | Retention: where workers live, payroll leaving the region, GM property tax, city income tax | Capture and wage charts; `outputs/retention_*.csv` |
| `Individual_TeamMember_files/wangz153/03_benefit.ipynb` | Benefit: resident income, poverty, and tracts where job centers and poverty overlap | Tract and site charts; `outputs/benefit_*.csv` (requires the crosswalk in section 5) |
| `notebooks/baseline_visualizations.ipynb` | Baseline regional indicators: unemployment, employment by ownership, industry stand-ins, median income | Four baseline charts; the final Census API section is optional and needs internet |

The three `wangz153` notebooks import `nc3_helpers.py` from the same folder, so open them from that folder (JupyterLab does this automatically). Each of them takes under a minute to run.

## 8. Refresh the data from the original sources (optional)

The committed CSV files are enough to run everything above. These scripts re-download the public data for an annual update. They need an internet connection. Run them from the repository root.

| Script | Downloads | Command |
| --- | --- | --- |
| `Data_Files/load_lansing_sources.py` | QCEW (BLS), LODES, ACS key indicators | `python Data_Files/load_lansing_sources.py --year 2025 --qtr a --skip-lodes` |
| `Data_Files/load_retention_sources.py` | ACS county commuting flows, LODES origin–destination files and block crosswalk | `python Data_Files/load_retention_sources.py` |
| `Data_Files/load_benefit_sources.py` | ACS tract and place indicators | `python Data_Files/load_benefit_sources.py --skip-map` |

Notes:

- `load_lansing_sources.py` downloads one QCEW year per run; repeat with `--year 2024`, `--year 2023`, and so on. Drop `--skip-lodes` to also download LODES (large files).
- `load_retention_sources.py --skip-lodes` downloads only the ACS commuting flows.
- `load_benefit_sources.py` uses the official Census API when the `CENSUS_API_KEY` environment variable is set, and falls back to Census Reporter otherwise (Census Reporter serves 2020–2024 only). A free key is available at https://api.census.gov/data/key_signup.html. Set it **only as an environment variable** for the current terminal session — never in code, notebooks, or committed files:

  ```powershell
  $env:CENSUS_API_KEY="your_key"
  ```

  ```bash
  export CENSUS_API_KEY="your_key"
  ```


Do not commit:

- API keys, passwords, tokens, or other credentials;
- restricted or partner-confidential data;
- full LODES state files;
- full ACFR PDF files; or

Always review `git status` before committing.

## 9. Troubleshooting

### Conda cannot find `environment.yml`

Confirm that the terminal is in the repository root (`pwd`, or `Get-Location` in PowerShell). The directory should contain `README.md`, `environment.yml`, `INSTALL.md`, `figure_instructions/`, and `notebooks/`.

### `conda activate nc3` fails

- **"Could not find conda environment: nc3"** — the environment has not been created yet. Run `conda env create --file environment.yml` first.
- **`conda activate` does nothing or is not recognized in PowerShell** — run `conda init powershell` once, close and reopen PowerShell, and try again. Alternatively, use **Anaconda Prompt**.

### `jupyter` errors that mention another Python installation

If an error message shows a path outside the `nc3` environment (for example `D:\python\...` or a `mistune` / `nbconvert` import error), the terminal is using a different Jupyter installation. Activate the environment and check which Jupyter is used:

```powershell
conda activate nc3
where.exe jupyter
```

```bash
which jupyter
```

### Jupyter uses the wrong Python environment

```bash
conda activate nc3
python -m ipykernel install --user --name nc3 --display-name "Python (NC3)"
```

Restart JupyterLab and select **Python (NC3)**.

### Package imports fail

Update the environment from the repository definition:

```bash
conda activate nc3
conda env update --file environment.yml --prune
```

Avoid installing packages into the base environment because doing so makes the project harder to reproduce.

### The optional Census request in the baseline notebook fails

Confirm that the computer has internet access and try again later. The local-data sections of the notebook still run without it.

## 10. Development workflow

Changes are made on a branch and merged into `main` through a pull request.

1. Update `main` and create a focused branch:

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c feature/short-description
   ```

2. Make the change, then inspect it before committing:

   ```bash
   git status
   git diff
   ```

   Commit only the intended code, documentation, and approved data extracts, with a short, descriptive commit message.

3. Push the branch and open a pull request on GitHub:

   ```bash
   git push -u origin feature/short-description
   ```

4. After review, merge the pull request into `main`, then update your local copy with `git switch main` and `git pull --ff-only origin main`.
