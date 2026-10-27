#!/usr/bin/env python3
"""Multistate transition models + within-author_key adaptation + publication behavior."""
import pandas as pd, numpy as np, statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
import warnings; warnings.filterwarnings("ignore")
D="public_micro/data"; OUT="public_micro/output/tables"; import os; os.makedirs(OUT,exist_ok=True)
P1="data/processed"

T=pd.read_csv(f"{D}/transition_panel.csv.gz")
res=pd.read_csv(f"{P1}/resources_country_year.csv")
MAP2={"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","us":"usa"}
res=pd.read_csv(f"{P1}/resources_country_year.csv"); res.columns=[c.lower() for c in res.columns]
res=res.rename(columns={"iso3":"country_i3"})
res=res.sort_values(["country_i3","year"])
res["l2"]=res.groupby("country_i3")["h_usdppp"].shift(2).fillna(res.groupby("country_i3")["g_usdppp"].shift(2))
res["herd"]=res.l2
T["country_i3"]=T.country.map(MAP2)
T=T.merge(res[["country_i3","year","herd"]],left_on=["country_i3","t"],right_on=["country_i3","year"],how="left")
T["logR"]=np.log(T.herd.shift(0)) if "herd" in T else np.nan
T=T.dropna(subset=["herd"]); T["logR"]=np.log(T.herd)
T["dRl"]=T.groupby(["country","author_key"]).logR.diff()  # within-author_key country res change
print("T rows",len(T),"authors",T.author_key.nunique())
print(T.groupby(["state","s1"]).size().unstack(fill_value=0).to_string())

# transition matrix summary
tm=pd.crosstab(T.state,T.s1,normalize="index")
tm.to_csv(f"{OUT}/transition_matrix.csv")

# multinomial logit: destination state ~ origin state + logR (+ year FE, country FE)
import statsmodels.formula.api as smf
ST_ORDER=["S2","S1","S3","S4","S5"]
T["s1n"]=T.s1.map({k:i for i,k in enumerate(ST_ORDER)})
import statsmodels.api as smx
X=pd.get_dummies(T[["state","logR","country","t"]],columns=["state","country","t"],drop_first=True,dtype=float)
X=smx.add_constant(X.assign(logR=T.logR.values),has_constant="add")
X=X.drop(columns=["logR_1"],errors="ignore")
m=smx.MNLogit(T.s1n,X).fit(disp=0,maxiter=300,method="bfgs")
summ=pd.concat({"coef":m.params,"se":m.bse,"p":m.pvalues},axis=1)
summ.to_csv(f"{OUT}/mnlogit_transitions.csv")
print(m.summary().tables[0])

# key coefficient: logR effect on P(S1|S_j) vs baseline
# also within-author_key adaptation: portfolio RI change ~ logR within author_key
Pn=pd.read_csv(f"{D}/author_period_panel.csv.gz")
Pn["country_i3"]=Pn.country.map(MAP2)
Pn=Pn.merge(res[["country_i3","year","herd"]],left_on=["country_i3","t"],right_on=["country_i3","year"],how="left")
A=Pn[Pn.state!="S5"].dropna(subset=["herd","ri"]).copy(); A["logR"]=np.log(A.herd)
for y in ["ri","intl","team","oa","corr"]:
    mm=smf.ols(f"{y} ~ logR + C(country) + C(t)",data=A).fit(cov_type="cluster",cov_kwds={"groups":A.author_key})
    print(y,mm.params["logR"],mm.bse["logR"],mm.pvalues["logR"])
    pd.DataFrame({"var":[y],"coef":[mm.params["logR"]],"se":[mm.bse["logR"]],"p":[mm.pvalues["logR"]],"n":[len(A)]}).to_csv(f"{OUT}/within_author_{y}.csv",index=False)
# memory test: 2nd order
T["s0"]=T.groupby(["country","author_key"]).state.shift(1)
T2=T.dropna(subset=["s0"])
X1=pd.get_dummies(T2[["state","country","t"]],columns=["state","country","t"],drop_first=True,dtype=float)
X1=smx.add_constant(X1,has_constant="add")
X2=pd.get_dummies(T2[["state","s0","country","t"]],columns=["state","s0","country","t"],drop_first=True,dtype=float)
X2=smx.add_constant(X2,has_constant="add")
y2=T2.s1.map({k:i for i,k in enumerate(ST_ORDER)})
m1=smx.MNLogit(y2,X1).fit(disp=0,maxiter=300,method="bfgs")
m2=smx.MNLogit(y2,X2).fit(disp=0,maxiter=300,method="bfgs")
from scipy.stats import chi2
lr=2*(m2.llf-m1.llf); dfp=m2.df_model-m1.df_model
pd.DataFrame({"stat":[lr],"df":[dfp],"p":[chi2.sf(lr,dfp)],"llf1":[m1.llf],"llf2":[m2.llf]}).to_csv(f"{OUT}/markov_memory_test.csv",index=False)
print("memory LR",lr,dfp,chi2.sf(lr,dfp))
