#!/usr/bin/env python3
"""Finishing pass A: revised resource-intensity index (upstream-only) + LOO sensitivity.

- ri_z (primary): PCA-1 on upstream proxies only (mean_authors, mean_inst,
  share_intl, share_funder) — already the production index; recomputed here with
  loadings/variance documented.
- ri_full: PCA-1 on all 9 attributes incl. visibility-side (share_en, share_doi,
  share_oa) — retained ONLY as secondary robustness comparator; rank corr vs ri_z.
- LOO: PCA on 3 of 4 upstream components each -> rank corr of scores and
  re-estimated HERD x RI interaction for each.
Outputs: data/processed/field_resource_intensity.csv (new cols),
         output/tables/intensity_revision.csv
"""
import json, gzip, glob, os
import pandas as pd, numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pyfixest.estimation import fepois

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)
UP = ["mean_authors", "mean_inst", "share_intl", "share_funder"]
VIS = ["share_en", "share_doi", "share_oa"]

ri = pd.read_csv("data/processed/field_resource_intensity.csv")

def pca1(df, cols):
    X = StandardScaler().fit_transform(df[cols].fillna(df[cols].median()))
    p = PCA(n_components=1)
    s = p.fit_transform(X).ravel()
    if np.corrcoef(s, df[cols[0]])[0, 1] < 0:
        s = -s
    return s, p.explained_variance_ratio_[0], p.components_[0]

# full (contaminated) comparator
ri["ri_full"], var_full, load_full = pca1(ri, UP + VIS)
ri["ri_full_z"] = (ri.ri_full - ri.ri_full.mean()) / ri.ri_full.std()
rho = ri.ri_z.corr(ri.ri_full_z, method="spearman")
var_up = ri.pca_var_explained.iloc[0]

# loadings of primary index
X = StandardScaler().fit_transform(ri[UP].fillna(ri[UP].median()))
p = PCA(n_components=1); p.fit(X)
load_up = p.components_[0]
if np.corrcoef(X @ load_up, ri.mean_authors)[0, 1] < 0:
    load_up = -load_up
print("primary PC1 var explained:", round(var_up, 3),
      "loadings:", dict(zip(UP, np.round(load_up, 3))))
print("full-index PC1 var explained:", round(var_full, 3),
      "Spearman ri_z vs ri_full_z:", round(rho, 3))

# LOO scores
for c in UP:
    cols = [x for x in UP if x != c]
    s, v, _ = pca1(ri, cols)
    col = f"loo_{c}"
    ri[col] = (s - s.mean()) / s.std()
    print(f"LOO {col}: var={v:.3f}, spearman vs ri_z={ri[col].corr(ri.ri_z, method='spearman'):.3f}")

ri.to_csv("data/processed/field_resource_intensity.csv", index=False)

# --- re-estimate interactions ----------------------------------------------
panel = pd.read_csv("data/processed/panel_country_field_year.csv")
res = pd.read_csv("data/processed/resources_country_year.csv")
res.columns = [c.lower() for c in res.columns]
MAP = {"jp": "jpn", "kr": "kor", "gb": "gbr", "de": "deu", "fr": "fra", "it": "ita", "es": "esp",
       "nl": "nld", "se": "swe", "ch": "che", "at": "aut", "be": "bel", "dk": "dnk", "fi": "fin",
       "ie": "irl", "no": "nor", "pt": "prt", "pl": "pol", "cz": "cze", "gr": "grc", "hu": "hun",
       "sk": "svk", "ca": "can", "us": "usa", "au": "aus", "nz": "nzl", "il": "isr", "cn": "chn",
       "in": "ind", "br": "bra", "za": "zaf", "ru": "rus", "ir": "irn", "eg": "egy", "ar": "arg",
       "cl": "chl", "th": "tha", "my": "mys", "id": "idn", "sa": "sau", "tw": "twn", "hk": "hkg",
       "sg": "sgp", "pk": "pak", "ng": "nga", "mx": "mex", "tr": "tur", "ua": "ukr", "ro": "rou",
       "bg": "bgr", "hr": "hrv", "si": "svn", "ee": "est", "lv": "lva", "lt": "ltu", "lu": "lux",
       "is": "isl", "mt": "mlt", "cy": "cyp"}
panel["iso3"] = panel.country.map(MAP)
res = res.sort_values(["iso3", "year"])
res["l2_h"] = res.groupby("iso3")["h_usdppp"].shift(2)
res["l2_g"] = res.groupby("iso3")["g_usdppp"].shift(2)
res["logR"] = np.log(res.l2_h.fillna(res.l2_g))
df = panel.merge(res[["iso3", "year", "logR"]], on=["iso3", "year"], how="left")
df = df[df.y2 > 0].dropna(subset=["logR"])
df["cf"] = df.country + "_" + df.field.astype(str)
df["fy"] = df.field.astype(str) + "_" + df.year.astype(str)
df = df.merge(ri[["field", "ri_z", "ri_full_z"] + [f"loo_{c}" for c in UP]],
              on="field", how="left")

def inter(df, vcol):
    d = df.copy()
    d["x"] = d.logR * d[vcol]
    m = fepois(f"y2 ~ logR + {vcol} + x | cf + fy", data=d, vcov={"CRV1": "country"})
    t = m.tidy()
    return dict(est=t.loc["x", "Estimate"], lo=t.loc["x", "2.5%"],
                hi=t.loc["x", "97.5%"], p=t.loc["x", "Pr(>|t|)"], n=int(m._N))

rows = []
r = inter(df, "ri_z"); r.update(spec="primary upstream index (PC1, 4 vars)", index="ri_z"); rows.append(r)
r = inter(df, "ri_full_z"); r.update(spec="secondary full index incl. visibility vars", index="ri_full_z"); rows.append(r)
for c in UP:
    r = inter(df, f"loo_{c}"); r.update(spec=f"leave-one-out: drop {c}", index=f"loo_{c}"); rows.append(r)
pd.DataFrame(rows).to_csv(f"{OUT}/intensity_revision.csv", index=False)
print(pd.DataFrame(rows).to_string())
print("meta:", json.dumps({"var_up": var_up, "var_full": var_full,
      "spearman_primary_vs_full": rho,
      "loadings_up": dict(zip(UP, load_up.tolist()))}))
