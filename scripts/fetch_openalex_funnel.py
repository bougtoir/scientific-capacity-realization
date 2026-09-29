#!/usr/bin/env python3
"""Fetch country x field x year output-funnel counts from OpenAlex.

For each candidate country and year, run a small battery of group_by
queries on /works with group_by=primary_topic.field.id (per-page=200).

Variants (per ANALYSIS_PLAN_FROZEN.md):
  y1_all        : all works
  y2_article    : type:article
  y3_intl       : type:article, countries_distinct_count:>1
  y4_english    : type:article, language:en
  y5_fwci1      : type:article, fwci:>1                       (<= 2021 only)
  y6_top10      : type:article, top-10% cited                 (<= 2021 only)
  y7_top1       : type:article, top-1% cited                  (<= 2021 only)
  oa_mix        : all works, group_by open_access.oa_status
  oa_field      : type:article, open_access.is_oa:true, group_by field

Raw responses persisted gzipped under data/raw/openalex_funnel/.
"""
import requests, json, gzip, time, os, sys, hashlib, csv, datetime

BASE = "https://api.openalex.org/works"
MAILTO = "devin-research@cognition.ai"
API_KEY = os.environ.get("OPENALEX_API_KEY")
OUT = "data/raw/openalex_funnel"
os.makedirs(OUT, exist_ok=True)

COUNTRIES = (os.environ.get("FUNNEL_COUNTRIES") or """jp kr gb de fr it es nl se ch at be dk fi ie no pt pl cz gr hu sk
ca us au nz il cn in br za ru ir eg ar cl th my id sa tw hk sg pk ng mx tr ua
ro bg hr si ee lv lt lu is mt cy""").split()
YEARS = list(range(2000, 2026))

VARIANTS = [
    ("y1_all",     "",                                             "primary_topic.field.id"),
    ("y2_article", "type:article",                                 "primary_topic.field.id"),
    ("y3_intl",    "type:article,countries_distinct_count:>1",     "primary_topic.field.id"),
    ("y4_english", "type:article,language:en",                     "primary_topic.field.id"),
    ("y5_fwci1",   "type:article,fwci:>1",                         "primary_topic.field.id"),
    ("y6_top10",   "type:article,citation_normalized_percentile.is_in_top_10_percent:true", "primary_topic.field.id"),
    ("y7_top1",    "type:article,citation_normalized_percentile.is_in_top_1_percent:true",  "primary_topic.field.id"),
    ("oa_mix",     "",                                             "open_access.oa_status"),
    ("oa_field",   "type:article,open_access.is_oa:true",          "primary_topic.field.id"),
]
CITE_CUTOFF = 2021  # maturity per frozen plan

def get(params, tries=4):
    for a in range(tries):
        try:
            r = requests.get(BASE, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503):
                time.sleep(2 ** a + 1)
                continue
            return {"_error": r.status_code, "_body": r.text[:500]}
        except Exception:
            time.sleep(2 ** a + 1)
    return {"_error": "max_retries"}

done = set()
manifest_path = os.path.join(OUT, "_manifest_done.txt")
if os.path.exists(manifest_path):
    done = set(open(manifest_path).read().split())
mf = open(manifest_path, "a")

n = 0
t0 = time.time()
errs = 0
for c in COUNTRIES:
    if os.path.exists(manifest_path):  # refresh cross-worker progress per country
        done |= set(open(manifest_path).read().split())
    for y in YEARS:
        bundle = {}
        for name, extra, gb in VARIANTS:
            if name in ("y5_fwci1", "y6_top10", "y7_top1") and y > CITE_CUTOFF:
                continue
            key = f"{c}_{y}_{name}"
            if key in done:
                continue
            filt = f"institutions.country_code:{c},publication_year:{y}"
            if extra:
                filt += "," + extra
            params = {"filter": filt, "group_by": gb, "per-page": 200, "mailto": MAILTO}
            if API_KEY:
                params["api_key"] = API_KEY
            j = get(params)
            if "_error" in j or j.get("error"):
                print(f"ERR {key}: {str(j)[:120]}", flush=True)
                errs += 1
                if errs > 20:
                    print("too many consecutive errors; exiting for deferred retry", flush=True)
                    sys.exit(3)
                continue
            errs = 0
            bundle[name] = j
            mf.write(key + "\n"); mf.flush()
            n += 1
            time.sleep(0.12)
        if bundle:
            path = os.path.join(OUT, f"{c}_{y}.json.gz")
            prev = {}
            if os.path.exists(path):
                prev = json.load(gzip.open(path))["queries"]
            prev.update(bundle)
            with gzip.open(path, "wt") as f:
                json.dump({"country": c, "year": y, "queries": prev,
                           "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}, f)
            n_b = os.path.getsize(path)
    print(f"[{time.strftime('%H:%M:%S')}] {c} done, api calls so far={n}, elapsed={time.time()-t0:.0f}s", flush=True)

# ledger entry (one per file set)
with open("data/raw/ACQUISITION_LEDGER.csv", "a") as f:
    w = csv.writer(f)
    total = sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT) if x.endswith(".json.gz"))
    h = hashlib.sha256()
    for x in sorted(os.listdir(OUT)):
        if x.endswith(".json.gz"):
            h.update(open(os.path.join(OUT, x), "rb").read())
    w.writerow(["data/raw/openalex_funnel/*.json.gz", total, h.hexdigest()[:16],
                "https://api.openalex.org/works (group_by battery, filters per ANALYSIS_PLAN_FROZEN.md)",
                datetime.datetime.now(datetime.timezone.utc).isoformat(),
                f"countries={len(COUNTRIES)} years=2000-2025 calls={n}"])
print("DONE", n)
