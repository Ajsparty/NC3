#!/usr/bin/env python3
"""Download the extra public sources used by 02_retention (stage B).

Sources
  1. ACS 2016-2020 county-to-county commuting flows (Census, table1.xlsx)
     -> acs_commuting_flows_2016_2020_tri.csv            (committed, small)
  2. LODES8 Michigan origin-destination 2021, main + aux, plus block crosswalk
     -> lodes_od_tri_workplace_2021_agg.csv.gz           (committed, aggregated)
     -> lansing_data/raw/*.csv.gz                         (NOT committed)

Usage (from the repo root):
    python Data_Files/load_retention_sources.py
    python Data_Files/load_retention_sources.py --skip-lodes   # ACS only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "lansing_data" / "raw"
TRI = {"26037": "Clinton", "26045": "Eaton", "26065": "Ingham"}
UA = "LansingWealthScorecard/1.0 (research; python; contact nc3now.org)"

ACS_URL = ("https://www2.census.gov/programs-surveys/demo/tables/metro-micro/2020/"
           "commuting-flows-2020/table1.xlsx")
LODES_BASE = "https://lehd.ces.census.gov/data/lodes/LODES8/mi"
LODES_YEAR = "2021"
LODES_FILES = {
    "xwalk": f"{LODES_BASE}/mi_xwalk.csv.gz",
    "od_main": f"{LODES_BASE}/od/mi_od_main_JT00_{LODES_YEAR}.csv.gz",  # live and work in MI
    "od_aux": f"{LODES_BASE}/od/mi_od_aux_JT00_{LODES_YEAR}.csv.gz",    # work in MI, live elsewhere
}


def download(url: str, dest: Path) -> Path:
    """Stream a file to disk once; reuse it on later runs."""
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  have {dest.name} ({dest.stat().st_size/1e6:.1f} MB)")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {url}")
    with requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=300) as r:
        r.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
        tmp.replace(dest)
    print(f"  saved {dest.name} ({dest.stat().st_size/1e6:.1f} MB)")
    return dest


# ---------------------------------------------------------------------------
# 1. ACS commuting flows
# ---------------------------------------------------------------------------

def load_acs_flows() -> pd.DataFrame:
    print("\n=== ACS 2016-2020 county-to-county commuting flows ===")
    xlsx = download(ACS_URL, RAW_DIR / "acs_commuting_flows_2016_2020_table1.xlsx")
    raw = pd.read_excel(xlsx, header=None, dtype=str)

    # The sheet has several title rows. Data rows start where column 0 is a
    # 2-digit state FIPS code and column 8 (workers) is numeric.
    is_data = raw[0].str.fullmatch(r"\d{2}", na=False) & pd.to_numeric(raw[8], errors="coerce").notna()
    df = raw[is_data].iloc[:, :10].copy()
    df.columns = ["res_state_fips", "res_county_fips", "res_state", "res_county",
                  "work_state_fips", "work_county_fips", "work_state", "work_county",
                  "workers", "moe"]
    df["res_fips"] = df["res_state_fips"].str.zfill(2) + df["res_county_fips"].str.zfill(3)
    # Workplace state codes are 3 digits in this table (e.g. "026"); keep the last 2.
    df["work_fips"] = df["work_state_fips"].str[-2:] + df["work_county_fips"].fillna("").str.zfill(3)
    df["workers"] = pd.to_numeric(df["workers"])
    df["moe"] = pd.to_numeric(df["moe"], errors="coerce")

    keep = df["work_fips"].isin(TRI) | df["res_fips"].isin(TRI)
    out = df.loc[keep, ["res_fips", "res_state", "res_county", "work_fips", "work_state",
                        "work_county", "workers", "moe"]].copy()
    out["source"] = "ACS 2016-2020 5-year commuting flows, Census table1.xlsx"
    path = HERE / "acs_commuting_flows_2016_2020_tri.csv"
    out.to_csv(path, index=False)

    # Diagnostics so the user can confirm the parse worked
    print(f"  parsed {len(df):,} national flow rows; kept {len(out):,} touching the 3 counties")
    for fips, name in TRI.items():
        w = out[out.work_fips == fips]
        same = w.loc[w.res_fips == fips, "workers"].sum()
        tri = w.loc[w.res_fips.isin(TRI), "workers"].sum()
        tot = w["workers"].sum()
        print(f"  work in {name:8s}: {tot:>8,.0f} workers | same county {same/tot:6.1%} | 3-county {tri/tot:6.1%}")
    print(f"  wrote {path.name}")
    return out


# ---------------------------------------------------------------------------
# 2. LODES block-level origin-destination
# ---------------------------------------------------------------------------

def load_lodes_od() -> pd.DataFrame:
    print(f"\n=== LODES8 Michigan OD {LODES_YEAR} (main + aux) ===")
    paths = {k: download(u, RAW_DIR / Path(u).name) for k, u in LODES_FILES.items()}

    xw = pd.read_csv(paths["xwalk"], dtype=str, compression="gzip",
                     usecols=["tabblk2020", "cty", "stplc", "stplcname", "ctycsub", "ctycsubname",
                              "trct", "blklatdd", "blklondd"])
    xw = xw.set_index("tabblk2020")

    od_cols = ["w_geocode", "h_geocode", "S000", "SE01", "SE02", "SE03"]
    parts = []
    for key in ["od_main", "od_aux"]:
        n_in = 0
        for chunk in pd.read_csv(paths[key], dtype={"w_geocode": str, "h_geocode": str},
                                 usecols=od_cols, compression="gzip", chunksize=500_000):
            n_in += len(chunk)
            parts.append(chunk[chunk["w_geocode"].str[:5].isin(TRI)].assign(file=key))
        print(f"  {key}: scanned {n_in:,} rows")
    od = pd.concat(parts, ignore_index=True)

    # Residence geography: county from the code itself (works for other states too);
    # place (city) and county subdivision from the Michigan crosswalk when available.
    od["h_county"] = od["h_geocode"].str[:5]
    od["h_place"] = od["h_geocode"].map(xw["stplcname"]).fillna("Outside Michigan / not in a place")
    od["h_ctycsub"] = od["h_geocode"].map(xw["ctycsubname"]).fillna("Outside Michigan")

    agg = (od.groupby(["w_geocode", "h_county", "h_place", "h_ctycsub"], as_index=False)
             [["S000", "SE01", "SE02", "SE03"]].sum())
    # Attach workplace block coordinates and geography for institution footprints
    w = xw.loc[xw.index.intersection(agg["w_geocode"].unique()),
               ["cty", "stplcname", "ctycsubname", "trct", "blklatdd", "blklondd"]]
    w.columns = ["w_county", "w_place", "w_ctycsub", "w_tract", "w_lat", "w_lon"]
    agg = agg.merge(w, left_on="w_geocode", right_index=True, how="left")

    path = HERE / f"lodes_od_tri_workplace_{LODES_YEAR}_agg.csv.gz"
    agg.to_csv(path, index=False, compression="gzip")

    tot = agg["S000"].sum()
    in_tri = agg.loc[agg["h_county"].isin(TRI), "S000"].sum()
    print(f"  jobs with workplace in 3 counties: {tot:,.0f} | resident in 3 counties: {in_tri/tot:.1%}")
    print(f"  wrote {path.name} ({path.stat().st_size/1e6:.1f} MB, {len(agg):,} rows)")
    return agg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-lodes", action="store_true", help="only download the ACS commuting flows")
    args = ap.parse_args()
    load_acs_flows()
    if not args.skip_lodes:
        load_lodes_od()
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
