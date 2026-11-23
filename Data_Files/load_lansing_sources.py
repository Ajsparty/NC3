#!/usr/bin/env python3
"""Load public Lansing Big-4 scorecard sources into pandas."""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

OUT_DIR = Path(__file__).resolve().parent / "lansing_data"
RAW_DIR = OUT_DIR / "raw"
TABLE_DIR = OUT_DIR / "tables"

COUNTY_FIPS = {"Ingham": "26065", "Eaton": "26045", "Clinton": "26037"}
MSA_QCEW = "C2962"
MSA_CENSUS = "29620"
STATE_FIPS = "26"
LODES_YEAR = "2021"
UA = "LansingWealthScorecard/1.0 (research; python; contact nc3now.org)"


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "*/*"})
    return s


def get(s: requests.Session, url: str, **kwargs) -> requests.Response:
    kwargs.setdefault("timeout", 120)
    r = s.get(url, **kwargs)
    r.raise_for_status()
    return r


def save_df(df: pd.DataFrame, name: str) -> Path:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLE_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"  saved {path}  rows={len(df):,}  cols={len(df.columns)}")
    return path


def load_qcew(s: requests.Session, year: int, qtr: str) -> pd.DataFrame:
    frames = []
    areas = {**COUNTY_FIPS, "Lansing_MSA": MSA_QCEW}
    for label, area in areas.items():
        url = f"https://data.bls.gov/cew/data/api/{year}/{qtr}/area/{area}.csv"
        print(f"QCEW  {label}  {url}")
        df = pd.read_csv(io.StringIO(get(s, url).text), dtype={"area_fips": str, "industry_code": str})
        df["area_name"] = label
        frames.append(df)
        time.sleep(0.2)
    out = pd.concat(frames, ignore_index=True)
    keep_ind = out["industry_code"].isin(["10", "31-33", "336", "3361", "33611", "336111", "3363", "611", "92", "921"])
    slim = out.loc[keep_ind | (out["industry_code"] == "10")].copy()
    save_df(out, f"qcew_{year}_{qtr}_full")
    save_df(slim if not slim.empty else out, f"qcew_{year}_{qtr}_focus")
    return out


def load_lodes(s: requests.Session) -> dict[str, pd.DataFrame]:
    base = f"https://lehd.ces.census.gov/data/lodes/LODES8/mi"
    urls = {
        "xwalk": f"{base}/mi_xwalk.csv.gz",
        "wac": f"{base}/wac/mi_wac_S000_JT00_{LODES_YEAR}.csv.gz",
        "rac": f"{base}/rac/mi_rac_S000_JT00_{LODES_YEAR}.csv.gz",
    }
    frames: dict[str, pd.DataFrame] = {}
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in urls.items():
        print(f"LODES {name}  {url}")
        raw = RAW_DIR / Path(url).name
        if not raw.exists():
            raw.write_bytes(get(s, url).content)
        frames[name] = pd.read_csv(raw, dtype=str, compression="gzip")
        time.sleep(0.3)
    xwalk = frames["xwalk"]
    county_mask = xwalk["cty"].isin(COUNTY_FIPS.values())
    local_blocks = set(xwalk.loc[county_mask, "tabblk2020"])
    wac_local = frames["wac"][frames["wac"]["w_geocode"].isin(local_blocks)].copy()
    rac_local = frames["rac"][frames["rac"]["h_geocode"].isin(local_blocks)].copy()
    block_county = xwalk.loc[county_mask, ["tabblk2020", "cty", "ctyname", "trct"]]
    wac_local = wac_local.merge(block_county, left_on="w_geocode", right_on="tabblk2020", how="left")
    rac_local = rac_local.merge(block_county, left_on="h_geocode", right_on="tabblk2020", how="left")
    for df in (wac_local, rac_local):
        for col in df.columns:
            if col.startswith("C") or col == "C000":
                df[col] = pd.to_numeric(df[col], errors="coerce")
    save_df(wac_local, f"lodes_wac_local_{LODES_YEAR}")
    save_df(rac_local, f"lodes_rac_local_{LODES_YEAR}")
    job_cols = [c for c in wac_local.columns if c.startswith("C")]
    county_jobs = wac_local.groupby(["cty", "ctyname"], dropna=False)[job_cols].sum(numeric_only=True).reset_index()
    save_df(county_jobs, f"lodes_wac_county_totals_{LODES_YEAR}")
    frames["wac_local"] = wac_local
    frames["rac_local"] = rac_local
    frames["county_jobs"] = county_jobs
    return frames


def load_acs(s: requests.Session) -> pd.DataFrame | None:
    geo_ids = ",".join([
        "31000US29620", "05000US26065", "05000US26045", "05000US26037",
        "16000US2646000", "16000US2624120",
    ])
    tables = "B01003,B19013,B19301,B17001,B08303,B08126"
    url = f"https://api.censusreporter.org/1.0/data/show/latest?table_ids={tables}&geo_ids={geo_ids}"
    print(f"ACS   Census Reporter  {url}")
    try:
        payload = get(s, url).json()
    except Exception as exc:
        print(f"  skip ACS: {exc}")
        return None
    rows = []
    geo_names = {gid: g.get("name") for gid, g in payload.get("geography", {}).items()}
    table_meta = payload.get("tables", {})
    for gid, tables_data in payload.get("data", {}).items():
        for table_id, block in tables_data.items():
            estimates = block.get("estimate", {})
            errors = block.get("error", {})
            cols = table_meta.get(table_id, {}).get("columns", {})
            for col_id, value in estimates.items():
                rows.append({
                    "geo_id": gid,
                    "geo_name": geo_names.get(gid),
                    "table_id": table_id,
                    "column_id": col_id,
                    "column_name": cols.get(col_id, {}).get("name"),
                    "estimate": value,
                    "moe": errors.get(col_id),
                    "release": payload.get("release", {}).get("id"),
                })
    if not rows:
        return None
    df = pd.DataFrame(rows)
    save_df(df, "acs_census_reporter_lansing")
    return df


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--qtr", default="a")
    parser.add_argument("--skip-lodes", action="store_true")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    s = session()
    print("\n=== QCEW ===")
    load_qcew(s, args.year, args.qtr)
    if not args.skip_lodes:
        print("\n=== LODES ===")
        load_lodes(s)
    print("\n=== ACS ===")
    load_acs(s)
    print(f"\nDone. CSVs are in {TABLE_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
