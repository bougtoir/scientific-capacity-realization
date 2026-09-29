#!/usr/bin/env python3
"""Phase 11 (bounded): publication-access / OA analysis + Japan TA feasibility check.

1. Country OA-status mix vs resource level (panel regression, shares).
2. Conversion Y2->Y6 (top10% share) vs country OA share.
3. Japan TA: institution-level OA share in Springer/Nature hybrid journals
   before/after 2023-2024 agreements — feasibility assessment only.
"""
import pandas as pd, numpy as np, os
from pyfixest.estimation import feols

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)
cy = pd.read_csv("data/processed/panel_country_year.csv")
r = pd.read_csv("data/processed/resources_country_year.csv"); r.columns=[c.lower() for c in r.columns]
MAP = {"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","it":"ita","es":"esp","nl":"nld","se":"swe",
       "ch":"che","at":"aut","be":"bel","dk":"dnk","fi":"fin","ie":"irl","no":"nor","pt":"prt","pl":"pol",
       "cz":"cze","gr":"grc","hu":"hun","sk":"svk","ca":"can","us":"usa","au":"aus","nz":"nzl","il":"isr",
       "cn":"chn","in":"ind","br":"bra","za":"zaf","ru":"rus","ir":"irn","eg":"egy","ar":"arg","cl":"chl",
       "th":"tha","my":"mys","id":"idn","sa":"sau","tw":"twn","hk":"hkg","sg":"sgp","pk":"pak","ng":"nga",
       "mx":"mex","tr":"tur","ua":"ukr","ro":"rou","bg":"bgr","hr":"hrv","si":"svn","ee":"est","lv":"lva",
       "lt":"ltu","lu":"lux","is":"isl","mt":"mlt","cy":"cyp"}
cy["iso3"]=cy.country.map(MAP)
oa_cols=[c for c in cy.columns if c.startswith("oa_") and c!="oa_"]
cy["oa_total"]=cy[oa_cols].sum(axis=1)
for c in oa_cols: cy["sh_"+c]=cy[c]/cy.oa_total
d=cy.merge(r[["iso3","year","h_usdppp","g_pct_gdp"]],on=["iso3","year"],how="left")
d["logHERD"]=np.log(d.h_usdppp)
d=d.dropna(subset=["logHERD"])
d["top10_share"]=d.y6/d.y2

rows=[]
for dep in ["sh_oa_gold","sh_oa_hybrid","sh_oa_closed","y2_oa"]:
    if dep in d and d[dep].notna().sum()>50:
        m=feols(f"{dep} ~ logHERD | country + year",data=d.dropna(subset=[dep]),vcov={"CRV1":"country"})
        t=m.tidy(); t["dep"]=dep; rows.append(t)
        print(dep); print(t)
res=pd.concat(rows) if rows else pd.DataFrame()
res.to_csv(f"{OUT}/oa_models.csv",index=False)

# conversion analysis
d2=d[d.year<=2021].dropna(subset=["top10_share","sh_oa_gold"])
if len(d2)>30:
    m=feols("top10_share ~ sh_oa_gold + sh_oa_hybrid | country + year",data=d2,vcov={"CRV1":"country"})
    print(m.tidy()); m.tidy().to_csv(f"{OUT}/oa_conversion.csv")
print("TA feasibility note -> docs/TA_FEASIBILITY.md")
