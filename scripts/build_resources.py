#!/usr/bin/env python3
"""Build national resource panel: World Bank + OECD MSTI -> data/processed/resources_country_year.csv"""
import json, os, glob
import pandas as pd

OUT = "data/processed"; os.makedirs(OUT, exist_ok=True)

# --- World Bank ---
rows = []
for p in glob.glob("data/raw/worldbank/*.json"):
    ind = os.path.basename(p)[:-5]
    j = json.load(open(p))
    if len(j) < 2 or not j[1]:
        continue
    for r in j[1]:
        if r["value"] is None:
            continue
        rows.append({"iso3": r["countryiso3code"].lower(), "year": int(r["date"]),
                     "ind": ind, "val": r["value"]})
wb = pd.DataFrame(rows).pivot_table(index=["iso3", "year"], columns="ind", values="val").reset_index()
wb.columns = [c.replace(".", "_").lower() for c in wb.columns]
wb.to_csv(f"{OUT}/wb_country_year.csv", index=False)
print("WB", wb.shape, wb.columns.tolist())

# --- OECD MSTI ---
keep_units = {"USD_PPP", "PT_GERD", "PT_B1GQ", "PT_TOT_EMP", "PC_POP", "FTE", "PS", "10P3EMP"}
rows = []
for p in glob.glob("data/raw/oecd/msti_*.csv"):
    try:
        d = pd.read_csv(p, usecols=["REF_AREA", "MEASURE", "UNIT_MEASURE", "PRICE_BASE", "TIME_PERIOD", "OBS_VALUE"])
    except Exception:
        continue
    d = d[(d.UNIT_MEASURE.isin(keep_units)) & (d.PRICE_BASE.isin(["V", "_Z"]))].dropna(subset=["OBS_VALUE"])
    for r in d.itertuples():
        rows.append({"iso3": str(r.REF_AREA).lower(), "year": int(r.TIME_PERIOD),
                     "measure": r.MEASURE, "unit": r.UNIT_MEASURE, "pb": r.PRICE_BASE, "val": r.OBS_VALUE})
m = pd.DataFrame(rows)
m.to_csv(f"{OUT}/msti_long.csv", index=False)
print("MSTI long", m.shape)

# wide resource panel: prefer USD_PPP/V (constant real PPP USD) for levels
lev = m[m.unit == "USD_PPP"].pivot_table(index=["iso3", "year"], columns="measure", values="val")
lev.columns = [f"{c}_usdppp" for c in lev.columns]
shr = m[m.unit == "PT_GERD"].pivot_table(index=["iso3", "year"], columns="measure", values="val")
shr.columns = [f"{c}_pct_gerd" for c in shr.columns]
b1 = m[m.unit == "PT_B1GQ"].pivot_table(index=["iso3", "year"], columns="measure", values="val")
b1.columns = [f"{c}_pct_gdp" for c in b1.columns]
fte = m[m.unit == "FTE"].pivot_table(index=["iso3", "year"], columns="measure", values="val")
fte.columns = [f"{c}_fte" for c in fte.columns]

res = lev.join([shr, b1, fte], how="outer").reset_index()
res = res.merge(wb, on=["iso3", "year"], how="outer")
res.to_csv(f"{OUT}/resources_country_year.csv", index=False)
print("resources", res.shape)
print(res.columns.tolist())
