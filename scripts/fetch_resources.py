#!/usr/bin/env python3
"""Fetch national R&D resource series: World Bank indicators + OECD MSTI (SDMX).
Persists raw JSON/CSV snapshots to data/raw/ with ledger entries."""
import requests, json, os, csv, hashlib, datetime, io

RAW = "data/raw"
LED = os.path.join(RAW, "ACQUISITION_LEDGER.csv")
os.makedirs(f"{RAW}/worldbank", exist_ok=True)
os.makedirs(f"{RAW}/oecd", exist_ok=True)

COUNTRIES = """jpn kor gbr deu fra ita esp nld swe che aut bel dnk fin irl nor prt pol cze grc hun svk
can usa aus nzl isr chn ind bra zaf rus irn egy arg chl tha mys idn sau twn hkg sgp pak nga mex tur ukr
rou bgr hrv svn est lva ltu lux isl mlt cyp""".split()

def ledger(path, url, note=""):
    b = open(path, "rb").read()
    with open(LED, "a") as f:
        csv.writer(f).writerow([path, len(b), hashlib.sha256(b).hexdigest()[:16], url,
                                datetime.datetime.now(datetime.timezone.utc).isoformat(), note])

WB = {
    "GB.XPD.RSDV.GD.ZS": "gerd_pct_gdp",
    "SP.POP.SCIE.RD.P6": "researchers_per_million",
    "NY.GDP.MKTP.PP.KD": "gdp_ppp_const",
    "SP.POP.TOTL": "population",
    "GB.XPD.RSDV.GD.ZS.md": None,
}
for ind, name in list(WB.items())[:4]:
    cc = ";".join(x.upper() for x in COUNTRIES)
    url = f"https://api.worldbank.org/v2/country/{cc}/indicator/{ind}?format=json&per_page=20000&date=1995:2025"
    r = requests.get(url, timeout=120)
    p = f"{RAW}/worldbank/{ind.replace('.','_')}.json"
    open(p, "wb").write(r.content)
    ledger(p, url.split("?")[0] + "?" + "&".join(url.split("?")[1].split("&")[:3]), name)
    try:
        j = r.json(); print(ind, "rows:", len(j[1]) if len(j) > 1 and j[1] else 0)
    except Exception:
        print(ind, "PARSE FAIL", r.status_code)

# OECD MSTI via SDMX-CSV. DF_MSTI: pull whole dataset slice for all countries may be huge;
# key: FREQ.MEASURE.UNIT...  first probe structure via a small filtered query.
probe_url = "https://sdmx.oecd.org/public/rest/v1/data/OECD.STI.STP,DSD_MSTI@DF_MSTI/JPN.........?startPeriod=2000&dimension_at_observation=AllDimensions"
r = requests.get(probe_url, headers={"Accept": "text/csv"}, timeout=120)
p = f"{RAW}/oecd/msti_jpn_probe.csv"
open(p, "wb").write(r.content)
ledger(p, probe_url, "MSTI structure probe JPN")
print("MSTI probe:", r.status_code, len(r.content))
print(r.text[:800])
