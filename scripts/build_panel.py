#!/usr/bin/env python3
"""Build the country x field x year analysis panel from raw OpenAlex funnel pulls.
Outputs data/processed/panel_country_field_year.csv and data/processed/panel_country_year.csv
"""
import gzip, json, os, glob
import pandas as pd

RAW = "data/raw/openalex_funnel"
OUT = "data/processed"
os.makedirs(OUT, exist_ok=True)
CITE_CUTOFF = 2021

rows = []
c_rows = []
for path in sorted(glob.glob(f"{RAW}/*.json.gz")):
    b = json.load(gzip.open(path))
    c, y = b["country"], b["year"]
    q = b["queries"]
    def grp(name):
        j = q.get(name)
        if not j or "_error" in j or "group_by" not in j:
            return {}
        return {g["key"]: g["count"] for g in j["group_by"]}
    y1 = grp("y1_all"); y2 = grp("y2_article"); y3 = grp("y3_intl")
    y4 = grp("y4_english"); y5 = grp("y5_fwci1"); y6 = grp("y6_top10")
    y7 = grp("y7_top1"); oaf = grp("oa_field"); oam = grp("oa_mix")
    fields = set(y1) | set(y2)
    for f in fields:
        rows.append({"country": c, "field": f.split("/")[-1], "year": y,
                     "y1": y1.get(f, 0), "y2": y2.get(f, 0), "y3": y3.get(f, 0),
                     "y4": y4.get(f, 0), "y5": y5.get(f, 0), "y6": y6.get(f, 0),
                     "y7": y7.get(f, 0), "y2_oa": oaf.get(f, 0)})
    # country-year OA mix
    rec = {"country": c, "year": y}
    for k, v in oam.items():
        rec["oa_" + k] = v
    rec.update({lvl: sum(d.values()) for lvl, d in
                [("y1", y1), ("y2", y2), ("y3", y3), ("y4", y4), ("y5", y5), ("y6", y6), ("y7", y7), ("y2_oa", oaf)]})
    c_rows.append(rec)

df = pd.DataFrame(rows)
df.to_csv(f"{OUT}/panel_country_field_year.csv", index=False)
cy = pd.DataFrame(c_rows)
cy.to_csv(f"{OUT}/panel_country_year.csv", index=False)
print(df.shape, cy.shape)
print(df.head())
