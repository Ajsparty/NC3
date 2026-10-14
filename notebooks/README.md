# Notebooks

This folder contains Jupyter notebooks for exploratory analysis and visualization testing for the NC3 Lansing Economic Ecosystem and Community Wealth Analysis project.

## Baseline Visualizations

`baseline_visualizations.ipynb` provides a clean starting point for testing charts and scorecard-style outputs using the public data extracts in `Data_Files/`.

### Setup

From the repository root:

```bash
pip install pandas matplotlib seaborn jupyter
jupyter notebook notebooks/baseline_visualizations.ipynb
```

Paths in the notebook assume it is run with the repository root as the working directory (or adjust the `DATA_DIR` variable).
