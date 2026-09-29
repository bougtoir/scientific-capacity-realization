#!/usr/bin/env python3
"""Phase 8: distributed-lag resource->output models -> output/tables/lag_models.csv + fig4."""
import pandas as pd, numpy as np, os
from pyfixest.estimation import fepois
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

OUT="output/tables"; FIG="output/figures"; os.makedirs(OUT,exist_ok=True); os.makedirs(FIG,exist_ok=True)
MAP = {"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","it":"ita","es":"esp","nl":"nld","se":"swe",
       "ch":"che","at":"aut","be":"bel","dk":"dnk","fi":"fin","ie":"irl","no":"nor","pt":"prt","pl":"pol",
       "cz":"cze","gr":"grc","hu":"hun","sk":"svk","ca":"can","us":"usa","au":"aus","nz":"nzl","il":"isr",
       "cn":"chn","in":"ind","br":"bra","za":"zaf","ru":"rus","ir":"irn","eg":"egy","ar":"arg","cl":"chl",
       "th":"tha","my":"mys","id":"idn","sa":"sau","tw":"twn","hk":"hkg","sg":"sgp","pk":"pak","ng":"nga",
       "mx":"mex","tr":"tur","ua":"ukr","ro":"rou","bg":"bgr","hr":"hrv","si":"svn","ee":"est","lv":"lva",
       "lt":"ltu","lu":"lux","is":"isl","mt":"mlt","cy":"cyp"}
p = pd.read_csv("data/processed/panel_country_field_year.csv")
r = pd.read_csv("data/processed/resources_country_year.csv"); r.columns=[c.lower() for c in r.columns]
p["iso3"]=p.country.map(MAP)
r=r.sort_values(["iso3","year"])
r["R"]=r.h_usdppp.fillna(r.g_usdppp)
r["dlogR_0"]=r.groupby("iso3")["R"].transform(lambda s:np.log(s).diff())
for k in range(1,9):
    r[f"dlogR_{k}"]=r.groupby("iso3")["dlogR_0"].shift(k)
lags=r[["iso3","year"]+[f"dlogR_{k}" for k in range(9)]]
df=p.merge(lags,on=["iso3","year"],how="left").dropna(subset=[f"dlogR_{k}" for k in range(0,9)])
df=df[df.y2>0]
df["cf"]=df.country+"_"+df.field.astype(str); df["fy"]=df.field.astype(str)+"_"+df.year.astype(str)
rhs=" + ".join(f"dlogR_{k}" for k in range(9))
m=fepois(f"y2 ~ {rhs} | cf + fy",data=df,vcov={"CRV1":"country"})
t=m.tidy(); t.to_csv(f"{OUT}/lag_models.csv")
print(t)
ks=list(range(9)); est=[t.loc[f"dlogR_{k}","Estimate"] for k in ks]
lo=[t.loc[f"dlogR_{k}","2.5%"] for k in ks]; hi=[t.loc[f"dlogR_{k}","97.5%"] for k in ks]
fig,ax=plt.subplots(figsize=(5.5,3.4))
ax.fill_between(ks,lo,hi,alpha=.25); ax.plot(ks,est,marker="o")
ax.axhline(0,color="k",lw=.8); ax.set_xlabel("lag (years)"); ax.set_ylabel("PPML coefficient on Δlog HERD")
ax.set_title("Distributed lag: resource change → article output")
fig.tight_layout(); fig.savefig(f"{FIG}/fig4_distributed_lag.png"); fig.savefig(f"{FIG}/fig4_distributed_lag.pdf")
cum=np.nansum(est); print("cumulative:",cum)
