#!/usr/bin/env python3
"""Phase 10 analysis: does resource contraction predict within-author shift from
high- to lower-resource-intensity fields? Minimal per frozen plan (option A)."""
import gzip, json, glob, os
import pandas as pd, numpy as np

OUT="output/tables"; os.makedirs(OUT,exist_ok=True)
ri=pd.read_csv("data/processed/field_resource_intensity.csv")
ri_map=dict(zip(ri.field.astype(str),ri.ri_z))
ter=json.load(open("data/raw/openalex_mobility/_terciles.json"))
t_hi,t_lo=set(ter["hi"]),set(ter["lo"])

rows=[]
for p in glob.glob("data/raw/openalex_mobility/*.json.gz"):
    if "_terciles" in p: continue
    b=json.load(gzip.open(p)); c=b["country"]; w=b["window"]
    pre_auth={}
    for wk in b["pre"]:
        f=str((wk.get("primary_topic") or {}).get("field",{}).get("id","").split("/")[-1])
        for a in wk.get("authorships") or []:
            au=(a.get("author") or {}).get("id")
            if au: pre_auth.setdefault(au.split("/")[-1],[]).append(f)
    post_fields={}
    for wk in b["post"]:
        f=str((wk.get("primary_topic") or {}).get("field",{}).get("id","").split("/")[-1])
        for a in wk.get("authorships") or []:
            au=(a.get("author") or {}).get("id")
            if au: post_fields.setdefault(au.split("/")[-1],[]).append(f)
    for aid,fs in pre_auth.items():
        if aid not in post_fields or not fs: continue
        pf=post_fields[aid]
        rows.append({"country":c,"author":aid,"pre_hi":np.mean([x in t_hi for x in fs]),
                     "pre_meanri":np.mean([ri_map.get(x,np.nan) for x in fs]),
                     "post_share_lo":np.mean([x in t_lo for x in pf]),
                     "post_meanri":np.mean([ri_map.get(x,np.nan) for x in pf]),
                     "post_n":len(pf),"window":"_".join(map(str,w))})
a=pd.DataFrame(rows)
a.to_csv("data/processed/author_mobility.csv",index=False)
if len(a):
    summ=a.groupby(["country","window"]).agg(
        n=("author","count"),pre_hi=("pre_hi","mean"),
        share_moved_lo=("post_share_lo","mean"),d_ri=("post_meanri",lambda s:(s-a.loc[s.index,"pre_meanri"]).mean()))
    summ.to_csv(f"{OUT}/mobility_summary.csv")
    print(summ)
    # authors with dominant pre field in high tercile
    hi=a[a.pre_hi>=0.5]
    print("high-tercile authors:",len(hi),"mean post share in low tercile:",hi.post_share_lo.mean())
