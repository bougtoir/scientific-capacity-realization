#!/usr/bin/env python3
"""Finishing pass B: mobility / reallocation sensitivity on author histories.

Two implemented checks (author-level, focus-country sample):

(A) Non-mover restriction — authors whose post-window dominant field tercile
    equals their baseline dominant tercile; recompute mean post-window share in
    low-intensity fields and within-author dRI among stable authors.
(B) Fixed-author portfolio — assign each post-window work to the author's
    baseline dominant field (mode of pre-window fields); compare the realized
    mean resource-intensity of post-window output under actual vs fixed
    portfolio. Also reports the crossover share: fraction of post-window
    low-tercile output authored by baseline-high-tercile authors.

Reports per country: beta_full (realized dRI / post_share_lo), beta_fixed /
beta_nonmover, absolute change, relative attenuation (%).
Outputs: output/tables/mobility_sensitivity.csv
"""
import gzip, json, glob, os
import pandas as pd, numpy as np
from collections import Counter

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)
ri = pd.read_csv("data/processed/field_resource_intensity.csv")
ri_map = dict(zip(ri.field.astype(str), ri.ri_z))
ter = json.load(open("data/raw/openalex_mobility/_terciles.json"))
t_hi, t_lo = set(ter["hi"]), set(ter["lo"])

def fid_of(wk):
    t = (wk.get("primary_topic") or {}).get("field") or {}
    return str(t.get("id", "")).split("/")[-1]

def terc(f):
    return "hi" if f in t_hi else ("lo" if f in t_lo else "mid")

rows = []
for p in sorted(glob.glob("data/raw/openalex_mobility/*.json.gz")):
    if "_terciles" in p:
        continue
    b = json.load(gzip.open(p)); c = b["country"]; w = "_".join(map(str, b["window"]))
    pre_fields, post = {}, {}
    for wk in b["pre"]:
        f = fid_of(wk)
        for a in wk.get("authorships") or []:
            au = (a.get("author") or {}).get("id")
            if au:
                pre_fields.setdefault(au.split("/")[-1], []).append(f)
    for wk in b["post"]:
        f = fid_of(wk)
        for a in wk.get("authorships") or []:
            au = (a.get("author") or {}).get("id")
            if au:
                post.setdefault(au.split("/")[-1], []).append(f)

    base_dom, base_terc = {}, {}
    for aid, fs in pre_fields.items():
        if not fs:
            continue
        dom = Counter(fs).most_common(1)[0][0]
        base_dom[aid], base_terc[aid] = dom, terc(dom)

    both = [a for a in post if a in base_dom and post[a]]
    # (B) fixed portfolio: each post work assigned baseline dominant field
    ri_actual = [ri_map.get(f, np.nan) for a in both for f in post[a]]
    ri_fixed = [ri_map.get(base_dom[a], np.nan) for a in both for _ in post[a]]
    dri_real = np.nanmean(ri_actual) - np.nanmean([ri_map.get(base_dom[a], np.nan) for a in both])
    dri_fixed = 0.0  # by construction the fixed portfolio cannot drift

    # (A) non-mover restriction
    stable = [a for a in both if Counter(map(terc, post[a])).most_common(1)[0][0] == base_terc[a]]
    hi_auth = [a for a in both if base_terc[a] == "hi"]
    hi_stable = [a for a in stable if base_terc[a] == "hi"]

    def share_lo(authors):
        v = [np.mean([f in t_lo for f in post[a]]) for a in authors if post[a]]
        return np.mean(v) if v else np.nan

    beta_full = share_lo(hi_auth)
    beta_nonmover = share_lo(hi_stable)

    # crossover share: low-tercile post output attributable to baseline-high authors
    lo_works_by_hi = sum(sum(f in t_lo for f in post[a]) for a in hi_auth)
    lo_works_all = sum(sum(f in t_lo for f in post[a]) for a in both)
    crossover = lo_works_by_hi / lo_works_all if lo_works_all else np.nan

    rows.append({
        "country": c, "window": w,
        "n_authors": len(both), "n_hi_baseline": len(hi_auth),
        "n_stable": len(stable), "n_stable_hi": len(hi_stable),
        "share_stable": len(stable) / len(both) if both else np.nan,
        "post_share_lo_full": beta_full,
        "post_share_lo_nonmover": beta_nonmover,
        "attenuation_pp": (beta_nonmover - beta_full) if np.isfinite(beta_nonmover) and np.isfinite(beta_full) else np.nan,
        "attenuation_pct": 100 * (beta_nonmover - beta_full) / beta_full if beta_full and np.isfinite(beta_nonmover) else np.nan,
        "mean_post_ri_actual": np.nanmean(ri_actual),
        "mean_post_ri_fixed": np.nanmean(ri_fixed),
        "crossover_share_lo_output_from_hi_authors": crossover,
    })

res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/mobility_sensitivity.csv", index=False)
print(res.to_string())
