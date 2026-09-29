#!/usr/bin/env python3
"""Phase 10 data: author-level mobility sensitivity pulls (minimal, prompt option A).

For each focus country and a pre-specified contraction window, sample authors whose
pre-window dominant field sits in the TOP resource-intensity tercile, then fetch the
field composition of their post-window output. Persist raw work records.
"""
import requests, json, gzip, os, time, sys, datetime

B = "https://api.openalex.org/works"
OUT = "data/raw/openalex_mobility"; os.makedirs(OUT, exist_ok=True)
LED = "data/raw/ACQUISITION_LEDGER.csv"
SEL = "id,publication_year,primary_topic,authorships"
FOCUS = {"jp": [(2008, 2010, 2013, 2016)],  # pre_years(2), post_years(3) — finalize from resource shocks
         "kr": [(2008, 2010, 2013, 2016)],
         "gb": [(2008, 2010, 2013, 2016)],
         "de": [(2008, 2010, 2013, 2016)],
         "fr": [(2008, 2010, 2013, 2016)],
         "us": [(2008, 2010, 2013, 2016)]}
HIGH_INT_FIELDS = None  # set from field_resource_intensity at runtime
SAMPLE_AUTH = 1500

def get(params, tries=4):
    if os.environ.get("OPENALEX_API_KEY"):
        params = dict(params, api_key=os.environ["OPENALEX_API_KEY"])
    for a in range(tries):
        try:
            r = requests.get(B, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(2 ** a + 1)
    return {"_error": True}

import pandas as pd
ri = pd.read_csv("data/processed/field_resource_intensity.csv")
t_hi = set(ri.nlargest(9, "ri_z").field.astype(str))
t_lo = set(ri.nsmallest(9, "ri_z").field.astype(str))
json.dump({"hi": sorted(t_hi), "lo": sorted(t_lo)}, open(f"{OUT}/_terciles.json", "w"))

for c, windows in FOCUS.items():
    for (y0, y1, y2, y3) in windows:
        rows = {}
        # 1) sample pre-window works in high-intensity fields for country c
        pre = []
        for f in t_hi:
            j = get({"filter": f"institutions.country_code:{c},publication_year:{y0}-{y1},"
                               f"primary_topic.field.id:fields/{f},type:article",
                     "sample": 60, "seed": 7, "per-page": 60, "select": SEL, "mailto": "x@x.com"})
            if j.get("_error"): print("ERR pre", c, f); continue
            pre += j["results"]
            time.sleep(0.15)
        # author -> dominant field in pre window (among sampled)
        auth_field = {}
        for w in pre:
            fld = str((w.get("primary_topic") or {}).get("field", {}).get("id", "").split("/")[-1])
            for a in w.get("authorships") or []:
                au = (a.get("author") or {}).get("id")
                if not au:
                    continue
                aid = au.split("/")[-1]
                auth_field.setdefault(aid, []).append(fld)
        authors = [a for a, fs in auth_field.items() if len(fs) >= 1][:SAMPLE_AUTH]
        # 2) pull their post-window works
        post = []
        for i in range(0, len(authors), 50):
            ids = "|".join(authors[i:i+50])
            j = get({"filter": f"author.id:{ids},publication_year:{y2}-{y3},type:article",
                     "per-page": 200, "select": SEL, "mailto": "x@x.com", "cursor": "*"})
            # cursor pagination
            while True:
                if j.get("_error"): break
                post += j["results"]
                cur = j["meta"].get("next_cursor")
                if not cur or not j["results"]: break
                j = get({"filter": f"author.id:{ids},publication_year:{y2}-{y3},type:article",
                         "per-page": 200, "select": SEL, "mailto": "x@x.com", "cursor": cur})
            time.sleep(0.15)
        path = f"{OUT}/{c}_{y0}_{y1}_{y2}_{y3}.json.gz"
        with gzip.open(path, "wt") as fh:
            json.dump({"country": c, "pre": pre, "post": post,
                       "authors": authors, "window": [y0, y1, y2, y3],
                       "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}, fh)
        import csv, hashlib
        b = open(path, "rb").read()
        with open(LED, "a") as fh2:
            csv.writer(fh2).writerow([path, len(b), hashlib.sha256(b).hexdigest()[:16],
                "https://api.openalex.org/works (author mobility sample)",
                datetime.datetime.now(datetime.timezone.utc).isoformat(), "phase10"])
        print(c, "pre:", len(pre), "authors:", len(authors), "post:", len(post), flush=True)
print("DONE")
