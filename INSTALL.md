# NC3 Installation and Setup Guide

This guide takes a new user from a fresh computer to reproduced results: install the software, create the environment, add the data package, test the installation, run the analysis, and reproduce the figures.

Back to the [README](README.md).

## 1. System requirements

- [Git](https://git-scm.com/downloads)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) or Anaconda
- Access to the NC3 GitHub repository
- The NC3 data package, `Data_Files.zip` (section 4)

The environment uses **Python 3.11**. Packages are listed in [environment.yml](environment.yml) with minimum versions only. [requirements.txt](requirements.txt) lists the same packages for `pip` users; Conda users can ignore it.

## 2. Clone the repository

In PowerShell, Anaconda Prompt, Git Bash, or another terminal:

```bash
git clone https://github.com/Ajsparty/NC3.git
cd NC3
```

All later commands are run from this repository root (the folder that contains `README.md` and `INSTALL.md`).

## 3. Create the environment

```bash
conda env create --file environment.yml
conda activate nc3
```

Optional variations:

- To keep the environment inside the project folder instead of your global Conda folder, use `conda env create --prefix ./envs --file environment.yml` and then `conda activate ./envs`.
- To make the environment appear as a named kernel in an existing Jupyter installation: `python -m ipykernel install --user --name nc3 --display-name "Python (NC3)"`. Not needed if you start Jupyter from the activated environment.
- Without Conda: create a Python 3.11 virtual environment and run `pip install -r requirements.txt`.

If `conda activate` fails in Windows PowerShell, see [Troubleshooting](#9-troubleshooting).

## 4. Add the data package

The data files are **not stored in GitHub**. They are distributed separately as `Data_Files.zip`:

- **Lansing Growth Fund:** the zip is attached to, or linked in, the project delivery email.
- **Course instructors and reviewers:** download it from the NC3 Teams channel → **Shared** → `Data_Files`.

Copy the data files into the repository's `Data_Files/` folder. The folder already contains documentation and scripts; only the data files (`.csv` and `.csv.gz`) are added.

PowerShell (from the repository root; change the zip path if it is not in Downloads):

```powershell
Expand-Archive "$HOME\Downloads\Data_Files.zip" -DestinationPath "$env:TEMP\nc3_data" -Force
Copy-Item "$env:TEMP\nc3_data\Data_Files\*.csv*" -Destination Data_Files\
```

macOS / Linux / Git Bash:

```bash
unzip -o ~/Downloads/Data_Files.zip -d /tmp/nc3_data
cp /tmp/nc3_data/Data_Files/*.csv* Data_Files/
```

Check that the data is in place:

```bash
python -c "from pathlib import Path; n = len(list(Path('Data_Files').glob('*.csv*'))); print(n, 'data files found'); assert Path('Data_Files/qcew_2019_2025_a_focus.csv').exists(), 'Data package not found in Data_Files/'"
```

You should see "25 data files found" and no error. Git ignores these files, so they will not be committed by accident. [Data_Files/README.md](Data_Files/README.md) describes every file.

### One extra public file for notebook 03

[notebooks/03_benefit.ipynb](notebooks/03_benefit.ipynb) also needs the Census LODES block crosswalk (`mi_xwalk.csv.gz`, about 4.5 MB), downloaded directly from the Census Bureau:

PowerShell:

```powershell
New-Item -ItemType Directory -Force Data_Files/lansing_data/raw | Out-Null
Invoke-WebRequest https://lehd.ces.census.gov/data/lodes/LODES8/mi/mi_xwalk.csv.gz -OutFile Data_Files/lansing_data/raw/mi_xwalk.csv.gz
```

macOS / Linux / Git Bash:

```bash
mkdir -p Data_Files/lansing_data/raw
curl -L -o Data_Files/lansing_data/raw/mi_xwalk.csv.gz https://lehd.ces.census.gov/data/lodes/LODES8/mi/mi_xwalk.csv.gz
```

Only notebook 03 needs this file. The installation test and the figure notebook do not.

## 5. Test the installation

With `nc3` active, check the packages:

```bash
python -c "import pandas, numpy, matplotlib, seaborn, openpyxl; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| matplotlib', matplotlib.__version__)"
```

It should print three version numbers and no error. Then run the demo, which rebuilds every project figure from the data package:

```bash
jupyter nbconvert --to notebook --execute --inplace figure_instructions/reproduce_figures.ipynb
```

A successful run takes about a minute and ends with **"Figure export check passed."** The 21 PNG files are written to [figure_instructions/figures/](figure_instructions/figures/). If this works, the installation is complete.

## 6. Run the analysis

Start JupyterLab from the repository root with `nc3` active:

```bash
jupyter lab
```

Open each notebook and choose **Kernel → Restart Kernel and Run All Cells**. The analysis is three notebooks, run in this order:

| Order | Notebook | Question | Writes |
| --- | --- | --- | --- |
| 1 | [notebooks/01_footprint.ipynb](notebooks/01_footprint.ipynb) | How big is each Big 4 institution? Jobs, share of regional jobs, relative pay, trends | `notebooks/outputs/footprint_*.csv` |
| 2 | [notebooks/02_retention.ipynb](notebooks/02_retention.ipynb) | How much stays local? Where workers live, payroll leaving the region, GM property tax, city income tax | `notebooks/outputs/retention_*.csv` |
| 3 | [notebooks/03_benefit.ipynb](notebooks/03_benefit.ipynb) | What do residents have? Income, poverty, and neighborhoods where job centers and poverty overlap | `notebooks/outputs/benefit_*.csv` |

Each notebook ends with its findings, a robustness table (which conclusions hold across the range of estimates), and a list of data gaps. Each notebook runs in under a minute.

The results of these three notebooks are already stored in `notebooks/outputs/`, so the figure notebook (section 7) works without running them first. Re-run them to rebuild those results from the data package.

**Supporting notebooks** in [notebooks/](notebooks/README.md) are not part of the main sequence: `baseline_visualizations.ipynb` (first baseline charts) and four notebooks prepared for the November 2026 partner meeting.

## 7. Reproduce the figures

[figure_instructions/reproduce_figures.ipynb](figure_instructions/reproduce_figures.ipynb) rebuilds and exports every project figure. It is the same notebook as the installation test in section 5. Its first cell lists each figure and where it is used; [figure_instructions/README.md](figure_instructions/README.md) has the run steps.

## 8. Refresh the data from the original sources (optional)

The data package is enough to run everything above. These scripts re-download the public data for an annual update and need an internet connection.

| Script | Downloads | Command |
| --- | --- | --- |
| [Data_Files/load_lansing_sources.py](Data_Files/load_lansing_sources.py) | QCEW (BLS), LODES, ACS key indicators | `python Data_Files/load_lansing_sources.py --year 2025 --qtr a --skip-lodes` |
| [Data_Files/load_retention_sources.py](Data_Files/load_retention_sources.py) | ACS county commuting flows, LODES origin–destination files and block crosswalk | `python Data_Files/load_retention_sources.py` |
| [Data_Files/load_benefit_sources.py](Data_Files/load_benefit_sources.py) | ACS tract and place indicators | `python Data_Files/load_benefit_sources.py --skip-map` |

- `load_lansing_sources.py` downloads one QCEW year per run; repeat with `--year 2024` and so on. Drop `--skip-lodes` to also download LODES (large files).
- `load_retention_sources.py --skip-lodes` downloads only the ACS commuting flows.
- The **Census API requires a free key** (<https://api.census.gov/data/key_signup.html>). `load_benefit_sources.py` and the optional Census sections of the baseline and figure notebooks read it from the `CENSUS_API_KEY` environment variable. Set it for the current terminal only — never in code, notebooks, or committed files — and start Jupyter from that terminal:

  ```powershell
  $env:CENSUS_API_KEY="your_key"
  ```

  ```bash
  export CENSUS_API_KEY="your_key"
  ```

  Without a key, `load_benefit_sources.py` falls back to Census Reporter (2020–2024 only).

Downloads go to `Data_Files/lansing_data/`, which Git ignores. The scripts never overwrite the curated data files. Sources without a script (LAUS, IRS, BEA, CBP, IPEDS, City of Lansing ACFR tables, BS&A parcel records) are retrieved by hand as described in [Data_Files/README.md](Data_Files/README.md). After an update, rebuild `Data_Files.zip` from the new data files.

Never commit API keys, data files, full LODES state files, or ACFR PDFs.

## 9. Troubleshooting

**`conda env create` cannot find `environment.yml`.** Run it from the repository root (`pwd`, or `Get-Location` in PowerShell, should end in `NC3`).

**"Could not find conda environment: nc3".** The environment has not been created yet; run section 3.

**`conda activate` does nothing or is not recognized in PowerShell.** Run `conda init powershell` once, then close and reopen PowerShell. Or use Anaconda Prompt.

**Jupyter errors that mention another Python installation** (for example a path like `D:\python\...`, or a `mistune` / `nbconvert` import error). The terminal is using a different Jupyter. Activate `nc3` and check with `where.exe jupyter` (PowerShell) or `which jupyter`; the first result should be inside the `nc3` environment.

**A notebook says a data file is missing.** The data package is not in `Data_Files/` yet; repeat section 4. For notebook 03, also check `Data_Files/lansing_data/raw/mi_xwalk.csv.gz`.

**Package import errors.** Update the environment: `conda env update --file environment.yml --prune`. Avoid installing packages into the base environment.

**The optional Census request fails.** Set `CENSUS_API_KEY` (section 8) in the terminal before starting Jupyter. Everything else runs without it.

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

   Commit only the intended code and documentation, with a short, descriptive message.

3. Push the branch and open a pull request on GitHub:

   ```bash
   git push -u origin feature/short-description
   ```

4. After review, merge the pull request into `main`, then update your local copy with `git switch main` and `git pull --ff-only origin main`.

## 11. Current limitations

- QCEW, LODES, and ACS are downloaded by script; the other sources are retrieved by hand (section 8).
- The download scripts write next to, not over, the curated data files. An annual update combines automated and manual retrieval, a check of columns, geography, years, and definitions, and a deliberate replacement of the curated files. Record the retrieval date and source release for each update.
- Notebook 03 needs one public file that is not in the data package (section 4).
