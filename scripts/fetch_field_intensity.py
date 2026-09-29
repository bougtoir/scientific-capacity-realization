#!/usr/bin/env python3
"""Random-sample works per OpenAlex field to build resource-intensity inputs.

For each of the 26 fields, draw stratified random samples (seeded) across
2004-2023, selecting attributes needed for the resource-intensity index:
team size, institutional multiplicity, international collaboration, awards,
work type, DOI, OA status, source id.
"""
import requests, json, gzip, os, csv, hashlib, datetime, time

B = "https://api.openalex.org/works"
OUT = "data/raw/openalex_field_samples"
os.makedirs(OUT, exist_ok=True)
LED = "data/raw/ACQUISITION_LEDGER.csv"
SELECT = "id,publication_year,primary_topic,type,language,doi,authorships,awards,funders,open_access,institutions_distinct_count,countries_distinct_count,primary_location"
API_KEY = os.environ.get("OPENALEX_API_KEY")
N_PER_FIELD = 3000          # pooled across 2004-2023 (~150/yr)
YEARS = list(range(2004, 2024))

def qp(d):
    if API_KEY:
        d = dict(d, api_key=API_KEY)
    return d

def ledger(path, url_note):
    b = open(path, "rb").read()
    with open(LED, "a") as f:
        csv.writer(f).write([]) if False else csv.writer(f).writerow(
            [path, len(b), hashlib.sha256(b).hexdigest()[:16],
             url_note, datetime.datetime.now(datetime.timezone.utc).isoformat(), "field intensity sample"])

# list fields
r = requests.get("https://api.openalex.org/fields", params=qp({"per-page": 200, "mailto": "x@x.com"}))
fields = [(f["id"].split("/")[-1], f["display_name"]) for f in r.json()["results"]]
json.dump(fields, open(f"{OUT}/_fields.json", "w"))
print(len(fields), "fields")

for fid, fname in fields:
    rows = []
    for y in YEARS:
        want = max(1, N_PER_FIELD // len(YEARS))
        got = 0
        for seed in (11, 22, 33, 44):
            if got >= want:
                break
            for a in range(4):
                try:
                    rr = requests.get(B, params=qp({
                        "filter": f"primary_topic.field.id:fields/{fid},publication_year:{y},type:article",
                        "sample": min(200, want - got), "seed": seed + y,
                        "per-page": min(200, want - got), "select": SELECT, "mailto": "x@x.com"}), timeout=60)
                    if rr.status_code == 200:
                        break
                except Exception:
                    pass
                time.sleep(2 ** a + 1)
            else:
                continue
            res = rr.json()["results"]
            got += len(res)
            for w in res:
                rows.append({
                    "id": w["id"], "year": w["publication_year"], "field": fid,
                    "n_authors": len(w.get("authorships") or []),
                    "n_inst": w.get("institutions_distinct_count"),
                    "n_countries": w.get("countries_distinct_count"),
                    "n_awards": len(w.get("awards") or []),
                    "n_funders": len(w.get("funders") or []),
                    "type": w.get("type"), "lang": w.get("language"),
                    "doi": bool(w.get("doi")), "oa": (w.get("open_access") or {}).get("oa_status"),
                    "src": ((w.get("primary_location") or {}).get("source") or {}).get("id"),
                })
            time.sleep(0.1)
        if y % 5 == 0:
            print(fid, y, len(rows), flush=True)
    path = f"{OUT}/field_{fid}.json.gz"
    with gzip.open(path, "wt") as f:
        json.dump({"field": fid, "name": fname, "n": len(rows), "rows": rows}, f)
    ledger(path, "https://api.openalex.org/works?sample (stratified by year, seeded)")
    print("field", fid, fname, len(rows), flush=True)
print("DONE")
