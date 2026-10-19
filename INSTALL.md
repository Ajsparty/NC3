# NC3 Installation and Setup Guide

This guide explains how an authorized project collaborator can create the NC3 Python environment, prepare the public data files, and run the baseline visualization notebook.

## 1. System requirements

Install the following software before beginning:

- [Git](https://git-scm.com/downloads)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) or Anaconda
- Access to the private NC3 GitHub repository

The project environment uses **Python 3.9.20**. The required Python packages are listed in `environment.yml`.

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

## 4. Prepare the data files

The current repository uses manually downloaded public datasets. Follow `Data_Files/README.md` for source descriptions, update schedules, geographic coverage, and file-naming requirements.

The baseline notebook currently requires these files:

```text
Data_Files/laus_lansing_msa_2019_latest.csv
Data_Files/qcew_2024_a_focus.csv
Data_Files/acs_2024_key_indicators.csv
```

Keep the filenames and folder locations unchanged unless the notebook is updated at the same time. The notebook checks for these files before beginning the analysis and reports any missing filenames.

Additional datasets in `Data_Files/` support later scorecard development but are not required for the current baseline notebook.

### Optional public-source refresh script

The repository includes:

```text
Data_Files/load_lansing_sources.py
```

From the repository root, it can retrieve selected public QCEW, LODES, and ACS/Census Reporter data:

```bash
python Data_Files/load_lansing_sources.py --year 2025 --qtr a
```

The LODES downloads are relatively large. To refresh QCEW and ACS without downloading LODES, run:

```bash
python Data_Files/load_lansing_sources.py --year 2025 --qtr a --skip-lodes
```

Generated files are written under:

```text
Data_Files/lansing_data/raw/
Data_Files/lansing_data/tables/
```

These generated directories are excluded from version control. The script does **not** automatically overwrite the curated CSV files used by the baseline notebook. Before promoting a generated table into `Data_Files/`, compare its columns, geography, year, and definitions with the existing curated file, then update the notebook or canonical filename deliberately.

The script currently automates only QCEW, LODES, and ACS/Census Reporter sources. LAUS, IRS, BEA, CBP, IPEDS, portal exports, and PDF-based sources still follow the source-specific procedures in `Data_Files/README.md`.

Do not commit:

- API keys, passwords, tokens, or other credentials;
- restricted or partner-confidential data;
- full LODES state files;
- full ACFR PDF files; or
- regenerable large extracts stored under `Data_Files/lansing_data/tables/`.

The project `.gitignore` excludes designated credentials, local environments, and regenerable large data extracts. Always review `git status` before committing.

## 5. Start JupyterLab

From the repository root, with the `nc3` environment active, run:

```bash
jupyter lab
```

Open:

```text
notebooks/baseline_visualizations.ipynb
```

In Jupyter, select **Python (NC3)** as the kernel if it is not selected automatically. Then use:

```text
Kernel -> Restart Kernel and Run All Cells
```

Save the notebook after all cells finish successfully.

## 6. Expected notebook results

A successful run should:

1. identify the repository and `Data_Files` directories;
2. confirm that the three required CSV files exist;
3. display a Lansing-East Lansing MSA unemployment-rate trend;
4. compare Lansing MSA employment by ownership category;
5. visualize selected industry stand-ins;
6. compare median household income across the available geographies; and
7. optionally retrieve Lansing population and household-income values from the Census API.

The final API section is optional and requires an internet connection. The current request does not require an API key. If the request fails, the local-data sections should still remain usable.

## 7. Updating an existing environment

After `environment.yml` changes, update the environment with:

```bash
conda activate nc3
conda env update --file environment.yml --prune
```

## 8. Troubleshooting

### Conda cannot find `environment.yml`

Confirm that the terminal is in the repository root:

```bash
pwd
```

In Windows PowerShell, you can also run:

```powershell
Get-Location
```

The directory should contain `README.md`, `environment.yml`, `INSTALL.md`, `Data_Files/`, and `notebooks/`.

### The notebook reports missing data files

Check the data directory and exact filenames:

```powershell
Get-ChildItem Data_Files
```

The filenames are case-sensitive on some operating systems. Confirm that the required CSV files are located directly inside `Data_Files/`.

### Jupyter uses the wrong Python environment

Activate the NC3 environment and register the kernel again:

```bash
conda activate nc3
python -m ipykernel install --user --name nc3 --display-name "Python (NC3)"
```

Restart JupyterLab and select **Python (NC3)**.

### Package imports fail

Update the environment from the repository definition:

```bash
conda env update --file environment.yml --prune
```

Avoid installing packages into the base environment because doing so makes the project harder to reproduce.

### The optional Census request fails

Confirm that the computer has internet access and try again later. The baseline analysis is designed so that the local CSV sections can still run when the live request is unavailable.

## 9. Development workflow

Before making a change, update `main` and create a focused branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/short-description
```

Before committing, inspect the proposed changes:

```bash
git status
git diff
```

Commit only the intended code, documentation, and approved data extracts. Push the branch and open a pull request for team review.

## 10. Current reproducibility limitations

The repository provides partial automation through `Data_Files/load_lansing_sources.py`, but it does not yet refresh every source or automatically convert generated tables into all curated notebook inputs. An annual update therefore combines:

1. automated retrieval for supported QCEW, LODES, and ACS sources;
2. manual retrieval for the remaining public sources;
3. validation of schemas, geography, years, and definitions; and
4. deliberate replacement of curated analysis files.

Record the retrieval date and source release for every annual update. Future work should automate additional stable sources while retaining a documented manual process for portal exports and PDF-based sources.
