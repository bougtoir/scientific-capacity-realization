#!/usr/bin/env python3
"""Finishing pass D: weighted knowledge-persistence metric.

Presence-based persistence can ceiling at ~95%; add cosine similarity of the
subfield portfolio (count-weighted) between the 2004-2008 base period and each
later window, plus weighted Jaccard. Outputs:
output/tables/persistence_weighted.csv
"""
import gzip, json
import pandas as pd, numpy as np, os

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)
b = json.load(gzip.open("data/raw/openalex_persistence/subfield_presence.json.gz"))

rows = []
countries = sorted({k.rsplit("_", 2)[0] for k in b})
for c in countries:
    base = b.get(f"{c}_2004_2008", {})
    for win in ("2014_2018", "2019_2023"):
        lat = b.get(f"{c}_{win}", {})
        if not base or not lat:
            continue
        keys = set(base) | set(lat)
        vb = np.array([base.get(k, 0) for k in keys], dtype=float)
        vl = np.array([lat.get(k, 0) for k in keys], dtype=float)
        cos = float(vb @ vl / (np.linalg.norm(vb) * np.linalg.norm(vl)))
        wj = float(np.minimum(vb, vl).sum() / np.maximum(vb, vl).sum())
        rows.append({"country": c, "window": win.replace("_", "-"),
                     "cosine": cos, "weighted_jaccard": wj,
                     "n_sub_base": len(base), "n_sub_later": len(lat)})

res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/persistence_weighted.csv", index=False)
print(res.describe())
print(res[res.country.isin(["jp", "us", "kr", "de", "gb", "fr"])].to_string())
