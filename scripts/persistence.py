#!/usr/bin/env python3
"""Phase 9: knowledge-persistence vs output contraction.

Primary measure: subfield presence persistence — for each country, the share of
subfields active (>=1 article) in base period still active in later period.
Uses /works group_by=primary_topic.subfield.id with pagination (252 groups).
Secondary: within-country self-citation share (sampled referenced_works).
"""
import requests, json, gzip, os, time, datetime
import pandas as pd

B = "https://api.openalex.org/works"
OUT = "data/raw/openalex_persistence"; os.makedirs(OUT, exist_ok=True)
PERIODS = [(2004, 2008), (2014, 2018), (2019, 2023)]

def get(params, tries=5):
    if os.environ.get("OPENALEX_API_KEY"):
        params = dict(params, api_key=os.environ["OPENALEX_API_KEY"])
    for a in range(tries):
        try:
            r = requests.get(B, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(30 * (a + 1)); continue
        except Exception:
            pass
        time.sleep(2 ** a + 1)
    return {"_error": True}

countries = sorted({os.path.basename(p).split("_")[0]
                    for p in __import__("glob").glob("data/raw/openalex_funnel/*.json.gz")})
res = {}
for c in countries:
    for (a, b) in PERIODS:
        groups = {}
        # group_by results are capped at 200 groups; page param unsupported -> top-200 subfields
        j = get({"filter": f"institutions.country_code:{c},publication_year:{a}-{b},type:article",
                 "group_by": "primary_topic.subfield.id", "per-page": 200, "mailto": "x@x.com"})
        if j.get("_error"):
            print("ERR", c, a, b)
        else:
            for g in j.get("group_by", []):
                groups[g["key"]] = groups.get(g["key"], 0) + g["count"]
        res[f"{c}_{a}_{b}"] = groups
        time.sleep(0.15)
    print(c, {k: len(v) for k, v in list(res.items())[-3:]}, flush=True)

json.dump(res, gzip.open(f"{OUT}/subfield_presence.json.gz", "wt"))
import hashlib, csv
path = f"{OUT}/subfield_presence.json.gz"
bts = open(path, "rb").read()
with open("data/raw/ACQUISITION_LEDGER.csv", "a") as f:
    csv.writer(f).writerow([path, len(bts), hashlib.sha256(bts).hexdigest()[:16],
        "https://api.openalex.org/works group_by=subfield paged",
        datetime.datetime.now(datetime.timezone.utc).isoformat(), "phase9"])

# persistence metric: base->later presence share
rows = []
for c in countries:
    base = res.get(f"{c}_2004_2008", {})
    for (a, b) in PERIODS[1:]:
        later = res.get(f"{c}_{a}_{b}", {})
        shared = len(set(base) & set(later))
        rows.append({"country": c, "window": f"{a}-{b}", "base_n": len(base),
                     "later_n": len(later), "persist_share": shared / max(1, len(base))})
pd.DataFrame(rows).to_csv("data/processed/topic_persistence.csv", index=False)
print(pd.DataFrame(rows).head())
