#!/usr/bin/env python3
"""Publication-behavior models at author_key-portfolio level."""
import pandas as pd, numpy as np, statsmodels.formula.api as smf, os
D="public_micro/data"; OUT="public_micro/output/tables"; os.makedirs(OUT,exist_ok=True)
P1="data/processed"
P=pd.read_csv(f"{D}/author_period_panel.csv.gz")
res=pd.read_csv(f"{P1}/resources_country_year.csv"); MAP2={"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","us":"usa"}
res=pd.read_csv(f"{P1}/resources_country_year.csv"); res.columns=[c.lower() for c in res.columns]
res=res.rename(columns={"iso3":"country_i3"})
res=res.sort_values(["country_i3","year"])
res["l2"]=res.groupby("country_i3")["h_usdppp"].shift(2).fillna(res.groupby("country_i3")["g_usdppp"].shift(2))
res["herd"]=res.l2
P["country_i3"]=P.country.map(MAP2)
P=P.merge(res[["country_i3","year","herd"]],left_on=["country_i3","t"],right_on=["country_i3","year"],how="left")
A=P[P.state!="S5"].dropna(subset=["herd"]).copy(); A["logR"]=np.log(A.herd)
rows=[]
for y in ["oa","gold","hybrid","corr","intl"]:
    m=smf.ols(f"{y} ~ logR + C(country) + C(t)",data=A).fit(cov_type="cluster",cov_kwds={"groups":A.author_key})
    rows.append(dict(outcome=y,coef=m.params["logR"],se=m.bse["logR"],p=m.pvalues["logR"],n=len(A)))
    print(y,m.params["logR"],m.pvalues["logR"])
pd.DataFrame(rows).to_csv(f"{OUT}/publication_behavior.csv",index=False)
