#!/usr/bin/env python3
"""Public micro reproduction: regenerate Paper 1'' author-level tables from the
pseudonymized public panels + repo-level macro processed inputs.
Run from repo root: python public_micro/scripts/reproduce_micro.py
Outputs: public_micro/output/tables/*.csv (compare to canonical)."""
import pandas as pd, numpy as np, os
import statsmodels.api as smx, statsmodels.formula.api as smf
from scipy.stats import chi2

D="public_micro/data"; OUT="public_micro/output/tables"; os.makedirs(OUT,exist_ok=True)
P=pd.read_csv(f"{D}/author_period_panel.csv.gz")
T=pd.read_csv(f"{D}/transition_panel.csv.gz")
res=pd.read_csv("data/processed/resources_country_year.csv"); res.columns=[c.lower() for c in res.columns]
MAP2={"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","us":"usa"}
res["country"]=res.country_i3.map({v:k for k,v in MAP2.items()})
r=res[res.country.notna()][["country","year","h_usdppp"]].rename(columns={"year":"t","h_usdppp":"herd"})

# --- transition matrix + S5 re-entry ---
tm=pd.crosstab(T.state,T.s1,normalize="index").reindex(index=[f"S{i}" for i in range(1,6)],columns=[f"S{i}" for i in range(1,6)])
tm.to_csv(f"{OUT}/transition_matrix.csv")
s5_re=T[T.state=="S5"]; reentry=(s5_re.s1!="S5").mean()
pd.DataFrame({"s5_reentry":[reentry]}).to_csv(f"{OUT}/s5_reentry.csv",index=False)

# --- cohort counts ---
cf=pd.read_csv(f"{D}/cohort_flow.csv")
pd.DataFrame({"n_authors":[P.author_key.nunique()],"portfolio_windows":[len(P)],"transitions":[len(T)]}).to_csv(f"{OUT}/cohort_counts.csv",index=False)

# --- join HERD ---
P=P.merge(r,on=["country","t"],how="left"); T=T.merge(r,on=["country","t"],how="left")
A=P[P.state!="S5"].dropna(subset=["herd","ri"]).copy(); A["logR"]=np.log(A.herd)

# within-author FE-approx models (OLS + country/year FE, author-clustered)
for y in ["ri","intl","team","oa","corr"]:
    mm=smf.ols(f"{y} ~ logR + C(country) + C(t)",data=A).fit(cov_type="cluster",cov_kwds={"groups":A.author_key})
    pd.DataFrame({"var":[y],"coef":[mm.params["logR"]],"se":[mm.bse["logR"]],"p":[mm.pvalues["logR"]],"n":[len(A)]}).to_csv(f"{OUT}/within_author_{y}.csv",index=False)

# publication behavior incl gold/hybrid
rows=[]
for y in ["intl","oa","gold","hybrid","corr"]:
    m=smf.ols(f"{y} ~ logR + C(country) + C(t)",data=A).fit(cov_type="cluster",cov_kwds={"groups":A.author_key})
    rows.append(dict(outcome=y,coef=m.params["logR"],se=m.bse["logR"],p=m.pvalues["logR"],n=len(A)))
pd.DataFrame(rows).to_csv(f"{OUT}/publication_behavior.csv",index=False)

# --- MNLogit destination states ---
TT=T.dropna(subset=["herd"]).copy(); TT["logR"]=np.log(TT.herd)
TT["s1n"]=pd.Categorical(TT.s1).codes
X=pd.get_dummies(TT[["state","country","t"]],drop_first=True,dtype=float)
X=smx.add_constant(X.assign(logR=TT.logR.values),has_constant="add")
m=smx.MNLogit(TT.s1n,X).fit(disp=0,maxiter=300,method="bfgs")
summ=m.summary2().tables[1] if hasattr(m,"summary2") else None
pd.DataFrame(m.params).to_csv(f"{OUT}/mnlogit_transitions_params.csv")
pd.DataFrame(m.bse).to_csv(f"{OUT}/mnlogit_transitions_se.csv")

# --- Markov memory LR test: s1 ~ state vs s1 ~ state+lag history proxy ---
X1=pd.get_dummies(TT[["state"]],drop_first=True,dtype=float); X1=smx.add_constant(X1)
X2=pd.get_dummies(TT[["state","country","t"]],drop_first=True,dtype=float); X2=smx.add_constant(X2.assign(logR=TT.logR.values))
m1=smx.MNLogit(TT.s1n,X1).fit(disp=0,maxiter=300,method="bfgs"); m2=m
lr=2*(m2.llf-m1.llf); dfp=X2.shape[1]-X1.shape[1]
pd.DataFrame({"stat":[lr],"df":[dfp],"p":[chi2.sf(lr,dfp)],"llf1":[m1.llf],"llf2":[m2.llf]}).to_csv(f"{OUT}/markov_memory_test.csv")
print("done; reentry",round(reentry,4),"LR",round(lr,2))
