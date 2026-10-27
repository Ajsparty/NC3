"""Shared helpers for the NC3 Big 4 scorecard notebooks.

Every notebook imports from here so that loading, suppression handling, and
geography definitions are written exactly once.

Usage (from a notebook in this folder):
    from nc3_helpers import *
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from `start` (default: current directory) until a folder that
    contains `Data_Files/` is found. Works no matter which subfolder a
    notebook lives in."""
    here = Path(start or Path.cwd()).resolve()
    for folder in [here, *here.parents]:
        if (folder / "Data_Files").is_dir():
            return folder
    raise FileNotFoundError("Could not find the repo root (no Data_Files/ folder above here).")


REPO_ROOT = find_repo_root()
DATA_DIR = REPO_ROOT / "Data_Files"

# ---------------------------------------------------------------------------
# Geography and code definitions
# ---------------------------------------------------------------------------

# "Local region" for the scorecard = the three counties of the
# Lansing-East Lansing MSA. (Checked: QCEW MSA totals equal the sum of these
# three counties for every year 2019-2024.)
TRI_COUNTY = {"26065": "Ingham", "26045": "Eaton", "26037": "Clinton"}
COUNTY_NAMES = list(TRI_COUNTY.values())

# QCEW ownership codes
OWN_TOTAL, OWN_FEDERAL, OWN_STATE, OWN_LOCAL, OWN_PRIVATE = "0", "1", "2", "3", "5"

# QCEW numeric columns we use
QCEW_NUM = ["annual_avg_estabs", "annual_avg_emplvl", "total_annual_wages", "avg_annual_pay"]

# Big 4 display order and colors (reference categorical palette, fixed order:
# color follows the institution in every chart, never its rank).
BIG4 = ["MSU", "GM", "State Government", "Local Government"]
BIG4_COLORS = {
    "MSU": "#2a78d6",
    "GM": "#eb6834",
    "State Government": "#1baf7a",
    "Local Government": "#eda100",
}
REGION_COLOR = "#8a8984"  # neutral gray for "all jobs in region" reference lines

# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_qcew(path: Path | str | None = None, mask_suppressed: bool = True) -> pd.DataFrame:
    """Load the combined QCEW extract (2019-2025 annual averages).

    BLS writes suppressed cells (disclosure_code == "N") as 0. Those are not
    real zeros, so by default they are converted to NaN and flagged in a
    `suppressed` column.
    """
    path = Path(path) if path else DATA_DIR / "qcew_2019_2025_a_focus.csv"
    df = pd.read_csv(
        path,
        dtype={"area_fips": str, "own_code": str, "industry_code": str, "disclosure_code": str},
    )
    df["year"] = df["year"].astype(int)
    for col in QCEW_NUM:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["suppressed"] = df["disclosure_code"].eq("N")
    if mask_suppressed:
        df.loc[df["suppressed"], QCEW_NUM] = np.nan
    # Keep county rows only; MSA rows are dropped because the 2025 MSA pull
    # returned totals only, and the MSA equals the 3-county sum anyway.
    df = df[df["area_fips"].isin(TRI_COUNTY)].copy()
    df["county"] = df["area_fips"].map(TRI_COUNTY)
    return df


def load_acfr_employers() -> pd.DataFrame:
    """City of Lansing ACFR FY2025 Table 15 (principal employers, from LEAP)."""
    return pd.read_csv(DATA_DIR / "lansing_acfr_fy2025_principal_employers.csv")


def load_acfr_taxpayers() -> pd.DataFrame:
    """City of Lansing ACFR FY2025 Table 7 (principal property taxpayers)."""
    return pd.read_csv(DATA_DIR / "lansing_acfr_fy2025_principal_taxpayers.csv")

# ---------------------------------------------------------------------------
# QCEW accessors
# ---------------------------------------------------------------------------

def qcew_cell(df: pd.DataFrame, own: str, industry: str, measure: str = "annual_avg_emplvl") -> pd.DataFrame:
    """Return a year x county table for one ownership/industry cell.
    NaN means suppressed (or not in the extract)."""
    sub = df[(df["own_code"] == own) & (df["industry_code"] == industry)]
    out = sub.pivot_table(index="year", columns="county", values=measure, aggfunc="first")
    return out.reindex(columns=COUNTY_NAMES)


def tri_county_sum(table: pd.DataFrame, require_all: bool = True) -> pd.Series:
    """Sum a year x county table across the three counties.

    require_all=True returns NaN for any year where a county is missing, so a
    suppressed cell can never silently shrink a total.
    """
    total = table.sum(axis=1, min_count=1)
    if require_all:
        total[table.isna().any(axis=1)] = np.nan
    return total


def suppression_report(df: pd.DataFrame, cells: list[tuple[str, str]]) -> pd.DataFrame:
    """For each (own_code, industry_code), list the county-years that BLS suppressed."""
    rows = []
    for own, ind in cells:
        sub = df[(df["own_code"] == own) & (df["industry_code"] == ind) & df["suppressed"]]
        for county, g in sub.groupby("county"):
            rows.append({"own_code": own, "industry_code": ind, "county": county,
                         "suppressed_years": ", ".join(map(str, sorted(g["year"])))})
    return pd.DataFrame(rows, columns=["own_code", "industry_code", "county", "suppressed_years"])

# ---------------------------------------------------------------------------
# Small numeric helpers
# ---------------------------------------------------------------------------

def pct_change(series: pd.Series, start: int, end: int) -> float:
    """Percent change between two years of a year-indexed series."""
    a, b = series.get(start, np.nan), series.get(end, np.nan)
    return (b - a) / a * 100 if pd.notna(a) and a else np.nan


def index_to(series: pd.Series, base_year: int) -> pd.Series:
    """Rebase a year-indexed series so base_year = 100."""
    base = series.get(base_year, np.nan)
    return series / base * 100 if pd.notna(base) and base else series * np.nan


def hhi(shares_pct: pd.Series) -> float:
    """Herfindahl-Hirschman index from shares given in percent (0-100)."""
    return float((shares_pct ** 2).sum())
