#!/usr/bin/env python3
"""Macro-micro partial decomposition + model-country structural profiles + headroom."""
import pandas as pd, numpy as np, os
D="public_micro/data"; OUT="public_micro/output/tables"; os.makedirs(OUT,exist_ok=True)
P1="data/processed"

P=pd.read_csv(f"{D}/author_period_panel.csv.gz")
T=pd.read_csv(f"{D}/transition_panel.csv.gz")
res=pd.read_csv(f"{P1}/resources_country_year.csv"); MAP2={"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","us":"usa"}
res=pd.read_csv(f"{P1}/resources_country_year.csv"); res.columns=[c.lower() for c in res.columns]
res=res.rename(columns={"iso3":"country_i3"})
res=res.sort_values(["country_i3","year"])
res["l2"]=res.groupby("country_i3")["h_usdppp"].shift(2).fillna(res.groupby("country_i3")["g_usdppp"].shift(2))
res["herd"]=res.l2
pan=pd.read_csv(f"{P1}/panel_country_year.csv"); pan["country"]=pan.country.str.lower()
pers=pd.read_csv(f"{P1}/topic_persistence.csv")

# --- partial decomposition: pre(2009-2011 centers) vs post(2015-2017 centers) ---
A=P[P.state!="S5"].copy()
pre=A[(A.t>=2009)&(A.t<=2011)]; post=A[(A.t>=2015)&(A.t<=2017)]
rows=[]
for c in A.country.unique():
    d=[]
    pm=pre[pre.country==c].groupby("author_key").agg(ri=("ri","mean"),n=("n","sum"),intl=("intl","mean"))
    qm=post[post.country==c].groupby("author_key").agg(ri=("ri","mean"),n=("n","sum"),intl=("intl","mean"))
    both=pm.join(qm,lsuffix="_a",rsuffix="_b",how="inner")
    d_ri=(both.ri_b-both.ri_a).mean()             # within-author_key RI change
    d_n=(both.n_b-both.n_a).mean()                # within-author_key output change
    excl=len(pm)-len(both)
    rows.append(dict(country=c,authors_paired=len(both),exited_share=excl/len(pm),
                     d_ri_within=float(d_ri),d_output_within=float(d_n),d_intl=(both.intl_b-both.intl_a).mean()))
dec=pd.DataFrame(rows); dec.to_csv(f"{OUT}/decomposition.csv",index=False); print(dec)

# --- transition concentration per country ---
tr=T.groupby("country").apply(lambda g: pd.Series({
    "share_S1toS3":((g.state=="S1")&(g.s1=="S3")).mean(),
    "share_S1toS4":((g.state=="S1")&(g.s1=="S4")).mean(),
    "share_S1toS5":((g.state=="S1")&(g.s1=="S5")).mean(),
    "share_any_move":(g.state!=g.s1).mean()}),include_groups=False)
tr.to_csv(f"{OUT}/country_transition_shares.csv"); print(tr)

# --- model-country profile table ---
prof=[]
pers_latest=pers[pers.window==pers.window.max()].set_index("country").persist_share
for c in ["jp","kr","de","gb","us","fr"]:
    pcy=pan[pan.country==c].sort_values("year")
    y2trend=float(pcy[pcy.year>=2016].y2.pct_change().add(1).prod()-1) if len(pcy) else np.nan
    i3=MAP2[c]; rH=res[res.country_i3==i3].sort_values("year"); herdtrend=float(rH[rH.year>=2016].h_usdppp.pct_change().add(1).prod()-1)
    prof.append(dict(country=c,output_trend_2016_23=round(y2trend,3),herd_trend_2016_23=round(herdtrend,3),
                     persistence=round(float(pers_latest.get(c,np.nan)),3),
                     any_move=round(float(tr.loc[c,"share_any_move"]),3),
                     S1toS3=round(float(tr.loc[c,"share_S1toS3"]),3),
                     S1toS5=round(float(tr.loc[c,"share_S1toS5"]),3),
                     d_ri_within=round(float(dec.set_index("country").loc[c,"d_ri_within"]),3),
                     d_intl=round(float(dec.set_index("country").loc[c,"d_intl"]),3)))
pr=pd.DataFrame(prof); pr.to_csv(f"{OUT}/model_country_profiles.csv",index=False); print(pr)
