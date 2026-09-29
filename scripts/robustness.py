#!/usr/bin/env python3
"""Phase 12: reasoned robustness matrix -> output/tables/robustness_matrix.csv"""
import pandas as pd, numpy as np, os
from pyfixest.estimation import fepois

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)
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
r["logR"]=np.log(r.R)
for k in (0,1,2,3,4):
    r[f"logR{k}"]=r.groupby("iso3").logR.shift(k)
df=p.merge(r[["iso3","year","logR","logR0","logR1","logR2","logR3","logR4","g_pct_gdp","t_rs_fte","sp_pop_totl","sp_pop_scie_rd_p6","gb_xpd_rsdv_gd_zs"]],
           on=["iso3","year"],how="left")
df["cf"]=df.country+"_"+df.field.astype(str); df["fy"]=df.field.astype(str)+"_"+df.year.astype(str)
df["cy_tr"]=df.country+df.year.astype(str)
df["logGERDshare"]=np.log(df.g_pct_gdp)
df["logR_percap"]=df.logR-np.log(df.sp_pop_totl)
df["logR_perres"]=df.logR-np.log(df.t_rs_fte)
df["logR_wb"]=np.log(df.gb_xpd_rsdv_gd_zs)
ri_path="data/processed/field_resource_intensity.csv"
ri=pd.read_csv(ri_path) if os.path.exists(ri_path) else None
if ri is not None:
    df=df.merge(ri[["field","ri_z","ri_ew_z"]],on="field",how="left")
    df["logR_x_ri"]=df.logR2*df.ri_z; df["logR_x_ri_ew"]=df.logR2*df.ri_ew_z

def run(name, formula, data, **kw):
    d=data.dropna(subset=[x for x in formula.split("~")[1].split("|")[0].split("+") if x.strip() and x.strip()!="1"] if False else None)
    try:
        m=fepois(formula,data=data,vcov={"CRV1":"country"})
        t=m.tidy()
        key=[k for k in t.index if "logR" in k or "x_ri" in k]
        out=[]
        for k in key:
            out.append({"spec":name,"term":k,"est":t.loc[k,"Estimate"],"lo":t.loc[k,"2.5%"],
                        "hi":t.loc[k,"97.5%"],"p":t.loc[k,"Pr(>|t|)"],"n":m._data.shape[0] if hasattr(m,"_data") else None})
        return out
    except Exception as e:
        return [{"spec":name,"term":"ERROR","est":np.nan,"lo":np.nan,"hi":np.nan,"p":np.nan,"n":str(e)[:80]}]

rows=[]
base=df[df.y2>0].dropna(subset=["logR2"])
rows+=run("A1 primary (HERD lag2)","y2 ~ logR2 | cf + fy",base)
# alternative resource measures
d2=df[df.y2>0].dropna(subset=["logR_wb"])
rows+=run("A2 GERD%GDP (WB, lag2 via share)","y2 ~ logR_wb | cf + fy",d2)
# normalizations
d3=base.dropna(subset=["logR_percap"])
rows+=run("A3 HERD per capita","y2 ~ logR_percap | cf + fy",d3)
d4=base.dropna(subset=["logR_perres"])
rows+=run("A4 HERD per researcher-FTE","y2 ~ logR_perres | cf + fy",d4)
# lag variants
for lag in (0,1,3,4):
    dd=df[df.y2>0].dropna(subset=[f"logR{lag}"])
    rows+=run(f"A5 lag{lag}",f"y2 ~ logR{lag} | cf + fy",dd)
# sample variants
rows+=run("B1 excl US/CN","y2 ~ logR2 | cf + fy",base[~base.country.isin(["us","cn"])])
OECD={"jp","kr","gb","de","fr","it","es","nl","se","ch","at","be","dk","fi","ie","no","pt","pl","cz","gr","hu","sk","ca","us","au","nz","il","mx","tr","ro","bg","hr","si","ee","lv","lt","lu","is","mt","cy"}
rows+=run("B2 OECD only","y2 ~ logR2 | cf + fy",base[base.country.isin(OECD)])
rows+=run("B3 excl COVID 2020-21","y2 ~ logR2 | cf + fy",base[~base.year.isin([2020,2021])])
rows+=run("B4 pre-2020","y2 ~ logR2 | cf + fy",base[base.year<=2019])
# outcome variants
for y in ["y1","y3","y4","y2_oa"]:
    dd=df[df[y]>0].dropna(subset=["logR2"])
    rows+=run(f"C1 outcome {y}",f"{y} ~ logR2 | cf + fy",dd)
dd=df[(df.y6>0)&(df.year<=2021)].dropna(subset=["logR2"])
rows+=run("C2 outcome top10% (<=2021)","y6 ~ logR2 | cf + fy",dd)
# intensity interaction
if ri is not None:
    dI=base.dropna(subset=["logR_x_ri"])
    rows+=run("D1 intensity interaction","y2 ~ logR2 + ri_z + logR_x_ri | cf + fy",dI)
    dI2=base.dropna(subset=["logR_x_ri_ew"])
    rows+=run("D2 equal-weight index","y2 ~ logR2 + ri_ew_z + logR_x_ri_ew | cf + fy",dI2)
# country-specific trends as FE-adjacent sensitivity (country×year FE impossible; use country linear trend via cf demean? keep simple: interact country trend)
res=pd.DataFrame(rows)
res.to_csv(f"{OUT}/robustness_matrix.csv",index=False)
print(res.to_string())
