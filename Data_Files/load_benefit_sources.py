#!/usr/bin/env python3
"""Download ACS 5-year data for 03_benefit (resident outcomes and mismatch).

Writes
  acs_tract_2020_2024.csv     tract level, 3 counties, ACS 2020-2024 (2020 tract boundaries)
  acs_places_2015_2019_2020_2024.csv
                              county / city / MSA / state level, two NON-overlapping periods
  lansing_data/raw/tl_2024_26_tract.zip   tract boundaries for maps (optional, not committed)

Usage (from the repo root):
    python Data_Files/load_benefit_sources.py
    python Data_Files/load_benefit_sources.py --skip-map
Two interchangeable sources for the same ACS tables:
  * Census Reporter API (default when no key is set; no key needed)
  * Official Census API (used when CENSUS_API_KEY is set):
        PowerShell: $env:CENSUS_API_KEY="your_key"
Force one with --source censusreporter | census.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
RAW_DIR = HERE / "lansing_data" / "raw"
COUNTIES = {"037": "Clinton", "045": "Eaton", "065": "Ingham"}
UA = "LansingWealthScorecard/1.0 (research; python; contact nc3now.org)"
KEY = os.environ.get("CENSUS_API_KEY")

# variable -> short name. Each estimate (E) is pulled with its margin of error (M).
VARS = {
    "B01003_001": "population",
    "B19013_001": "median_hh_income",
    "B17001_001": "poverty_universe",
    "B17001_002": "below_poverty",
    "B25003_001": "occupied_units",
    "B25003_002": "owner_occupied",
    "B25077_001": "median_home_value",
    "B19054_001": "households_c19054",
    "B19054_002": "hh_with_asset_income",
    "B14001_001": "pop_3plus_c14001",
    "B14001_008": "enrolled_undergrad",
    "B14001_009": "enrolled_grad",
    "B23025_003": "civilian_labor_force",
    "B23025_005": "unemployed",
}
RACE_VARS = {  # median household income by race/ethnicity of householder (place/county only; tract MOE too large)
    "B19013B_001": "median_hh_income_black",
    "B19013H_001": "median_hh_income_white_nh",
    "B19013I_001": "median_hh_income_hispanic",
}
SENTINELS = {-666666666, -888888888, -999999999, -222222222, -333333333, -555555555}


def api(year: int, get: list[str], geo_for: str, geo_in: str | None = None) -> pd.DataFrame:
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {"get": ",".join(["NAME"] + get), "for": geo_for}
    if geo_in:
        params["in"] = geo_in
    if KEY:
        params["key"] = KEY
    # Census API: default requests User-Agent (some gateways reject custom agents)
    r = requests.get(url, params=params, timeout=120)
    try:
        rows = r.json()
    except ValueError:
        raise RuntimeError(
            f"Census API did not return data (HTTP {r.status_code}) for {geo_for}, {year}.\n"
            f"URL: {r.url}\nFirst 500 characters of the reply:\n{r.text[:500]}\n"
            "If the reply mentions a key, get a free key at https://api.census.gov/data/key_signup.html "
            "and set CENSUS_API_KEY before running again.") from None
    if r.status_code != 200 or not isinstance(rows, list):
        raise RuntimeError(f"Census API {r.status_code} for {geo_for} {year}: {r.text[:300]}")
    df = pd.DataFrame(rows[1:], columns=rows[0])
    time.sleep(0.3)
    return df


def tidy(df: pd.DataFrame, codes: dict[str, str], year_label: str) -> pd.DataFrame:
    out = df.copy()
    for code, name in codes.items():
        for suffix, tag in (("E", ""), ("M", "_moe")):
            col = code + suffix
            if col in out:
                v = pd.to_numeric(out[col], errors="coerce")
                out[name + tag] = v.where(~v.isin(SENTINELS))
                out.drop(columns=col, inplace=True)
    out["acs_period"] = year_label
    return out


def get_vars(codes: dict[str, str]) -> list[str]:
    return [c + s for c in codes for s in ("E", "M")]


# ---------------------------------------------------------------------------
# Census Reporter (no key) - same ACS tables, different API
# ---------------------------------------------------------------------------
CR_URL = "https://api.censusreporter.org/1.0/data/show/{release}"


def cr_fetch(release: str, codes: dict[str, str], geo_ids: list[str]) -> pd.DataFrame:
    """Return one row per geography with <name> and <name>_moe columns."""
    tables = sorted({c.split("_")[0] for c in codes})
    rows: dict[str, dict] = {}
    # Summary-level requests ("140|<county>", all tracts in a county) go one at a time;
    # plain geographies are grouped. One table per request keeps responses small.
    batches = [[g] for g in geo_ids if "|" in g] + ([[g for g in geo_ids if "|" not in g]] if any("|" not in g for g in geo_ids) else [])
    for table, batch in [(t, b) for t in tables for b in batches]:
        r = requests.get(CR_URL.format(release=release),
                         params={"table_ids": table, "geo_ids": ",".join(batch)},
                         headers={"User-Agent": UA}, timeout=120)  # Census Reporter requires a project-specific agent
        try:
            payload = r.json()
        except ValueError:
            raise RuntimeError(f"Census Reporter did not return data (HTTP {r.status_code}) for {table}: {r.text[:300]}") from None
        if "data" not in payload:
            raise RuntimeError(f"Census Reporter error for {table}: {str(payload)[:300]}")
        names = {g: d.get("name") for g, d in payload.get("geography", {}).items()}
        for gid, tdata in payload["data"].items():
            row = rows.setdefault(gid, {"cr_geoid": gid, "NAME": names.get(gid)})
            est, err = tdata[table].get("estimate", {}), tdata[table].get("error", {})
            for code, name in codes.items():
                if code.split("_")[0] != table:
                    continue
                col = code.replace("_", "")  # B17001_002 -> B17001002
                row[name] = est.get(col)
                row[name + "_moe"] = err.get(col)
        time.sleep(0.3)
    out = pd.DataFrame(rows.values())
    for c in out.columns:
        if c not in ("cr_geoid", "NAME"):
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


SOURCE = "censusreporter"  # set in main()


def load_tracts() -> pd.DataFrame:
    print(f"\n=== ACS 2020-2024 tracts (Clinton, Eaton, Ingham) via {SOURCE} ===")
    if SOURCE == "census":
        parts = []
        for cfips, name in COUNTIES.items():
            df = api(2024, get_vars(VARS), "tract:*", f"state:26 county:{cfips}")
            parts.append(df)
            print(f"  {name:8s}: {len(df):3d} tracts")
        out = tidy(pd.concat(parts, ignore_index=True), VARS, "2020-2024")
    else:
        out = cr_fetch("acs2024_5yr", VARS, [f"140|05000US26{c}" for c in COUNTIES])
        out["state"] = out.cr_geoid.str[7:9]; out["county"] = out.cr_geoid.str[9:12]; out["tract"] = out.cr_geoid.str[12:18]
        out["acs_period"] = "2020-2024"
        for cfips, name in COUNTIES.items():
            print(f"  {name:8s}: {(out.county == cfips).sum():3d} tracts")
    out["geoid"] = out["state"] + out["county"] + out["tract"]
    out["county_name"] = out["county"].map(COUNTIES)
    path = HERE / "acs_tract_2020_2024.csv"
    out.to_csv(path, index=False)
    print(f"  wrote {path.name} ({len(out)} tracts, population {out.population.sum():,.0f})")
    return out


def load_places() -> pd.DataFrame:
    print(f"\n=== ACS county / city / MSA / state, 2015-2019 and 2020-2024 via {SOURCE} ===")
    codes = {**VARS, **RACE_VARS}
    frames = []
    if SOURCE == "censusreporter":
        level_of = {"050": "county", "160": "place", "310": "msa", "040": "state"}
        geo_ids = [f"05000US26{c}" for c in COUNTIES] + ["16000US2646000", "16000US2624120", "31000US29620", "04000US26"]
        for release, label in (("acs2019_5yr", "2015-2019"), ("acs2024_5yr", "2020-2024")):
            try:
                t = cr_fetch(release, codes, geo_ids)
            except RuntimeError as exc:
                if "isn't supported" in str(exc):
                    print(f"  {label}: not available from Census Reporter - skipped. "
                          "Set CENSUS_API_KEY and rerun to add this period from the official Census API.")
                    continue
                raise
            t["geo_level"] = t.cr_geoid.str[:3].map(level_of)
            t["acs_period"] = label
            frames.append(t)
            print(f"  {label}: {len(t)} geographies")
        out = pd.concat(frames, ignore_index=True)
        keep = ["NAME", "geo_level", "acs_period"] + [c for c in out.columns if c not in ("NAME", "geo_level", "acs_period")]
        out = out[keep]
        path = HERE / "acs_places_2015_2019_2020_2024.csv"
        out.to_csv(path, index=False)
        print(f"  wrote {path.name} ({len(out)} rows)")
        return out
    for year, label in ((2019, "2015-2019"), (2024, "2020-2024")):
        geos = [
            ("county", api(year, get_vars(codes), f"county:{','.join(COUNTIES)}", "state:26")),
            ("place", api(year, get_vars(codes), "place:46000,24120", "state:26")),  # Lansing, East Lansing
            ("msa", api(year, get_vars(codes), "metropolitan statistical area/micropolitan statistical area:29620")),
            ("state", api(year, get_vars(codes), "state:26")),
        ]
        for level, df in geos:
            t = tidy(df, codes, label)
            t["geo_level"] = level
            frames.append(t)
        print(f"  {label}: {sum(len(g[1]) for g in geos)} geographies")
    out = pd.concat(frames, ignore_index=True)
    keep = ["NAME", "geo_level", "acs_period"] + [c for c in out.columns if c not in ("NAME", "geo_level", "acs_period")]
    out = out[keep]
    path = HERE / "acs_places_2015_2019_2020_2024.csv"
    out.to_csv(path, index=False)
    print(f"  wrote {path.name} ({len(out)} rows)")
    return out


def load_map() -> None:
    print("\n=== TIGER 2024 tract boundaries, Michigan (optional, for maps) ===")
    url = "https://www2.census.gov/geo/tiger/TIGER2024/TRACT/tl_2024_26_tract.zip"
    dest = RAW_DIR / Path(url).name
    if dest.exists():
        print(f"  have {dest.name}")
        return
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=300)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"  saved {dest.name} ({dest.stat().st_size/1e6:.1f} MB)")
    except Exception as exc:  # maps are a stretch goal; never block the core data
        print(f"  skipped map download: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-map", action="store_true", help="do not download tract boundaries")
    ap.add_argument("--skip-tracts", action="store_true", help="keep the existing tract file")
    ap.add_argument("--source", choices=["auto", "census", "censusreporter"], default="auto",
                    help="auto = official Census API if CENSUS_API_KEY is set, else Census Reporter")
    args = ap.parse_args()
    global SOURCE
    SOURCE = args.source if args.source != "auto" else ("census" if KEY else "censusreporter")
    print(f"ACS source: {SOURCE}")
    t = pd.read_csv(HERE / "acs_tract_2020_2024.csv") if args.skip_tracts else load_tracts()
    load_places()
    if not args.skip_map:
        load_map()
    # quick sanity checks for the user
    print("\nChecks:")
    print(f"  tracts with missing median income: {t.median_hh_income.isna().sum()}")
    student = (t.enrolled_undergrad + t.enrolled_grad) / t.population
    print(f"  tracts where >40% of residents are enrolled in college: {(student > 0.4).sum()}")
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
