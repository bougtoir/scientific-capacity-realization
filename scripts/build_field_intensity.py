#!/usr/bin/env python3
"""Phase 5: field resource-intensity index from sampled works -> FIELD_RESOURCE_INTENSITY.csv"""
import json, gzip, glob
import pandas as pd, numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

rows = []
for p in glob.glob("data/raw/openalex_field_samples/field_*.json.gz"):
    b = json.load(gzip.open(p))
    rows += b["rows"]
s = pd.DataFrame(rows)
print("sampled works:", len(s), "fields:", s.field.nunique())

def g(df):
    n = len(df)
    return pd.Series({
        "n": n,
        "mean_authors": df.n_authors.mean(), "med_authors": df.n_authors.median(),
        "mean_inst": df.n_inst.mean(),
        "share_intl": (df.n_countries > 1).mean(),
        "share_award": (df.n_awards > 0).mean(),
        "share_funder": (df.n_funders > 0).mean(),
        "share_en": (df.lang == "en").mean(),
        "share_doi": df.doi.mean(),
        "share_oa": df.oa.isin(["gold", "hybrid", "bronze", "diamond"]).mean(),
    })

agg = s.groupby("field").apply(g).reset_index()
names = dict(json.load(open("data/raw/openalex_field_samples/_fields.json")))
agg["field_name"] = agg.field.map(names)

# primary: PCA-1 of team/funding/collab inputs (not OA/lang/doi — those are visibility-side)
inp = ["mean_authors", "mean_inst", "share_intl", "share_funder"]
X = StandardScaler().fit_transform(agg[inp].fillna(agg[inp].median()))
pca = PCA(n_components=1)
agg["ri_pca"] = pca.fit_transform(X)
# orient so that higher = more resource-intensive (correlate with mean_authors)
if np.corrcoef(agg.ri_pca, agg.mean_authors)[0, 1] < 0:
    agg["ri_pca"] = -agg.ri_pca
agg["ri_z"] = (agg.ri_pca - agg.ri_pca.mean()) / agg.ri_pca.std()
agg["ri_rank"] = agg.ri_pca.rank() / len(agg)
# equal-weighted z index (sensitivity)
Z = (agg[inp] - agg[inp].mean()) / agg[inp].std()
agg["ri_ew"] = Z.mean(axis=1)
agg["ri_ew_z"] = (agg.ri_ew - agg.ri_ew.mean()) / agg.ri_ew.std()
agg["pca_var_explained"] = pca.explained_variance_ratio_[0]
agg.to_csv("data/processed/field_resource_intensity.csv", index=False)
print(agg[["field", "field_name", "n", "ri_z"]].sort_values("ri_z", ascending=False).to_string())
print("PCA var explained:", pca.explained_variance_ratio_[0])

# temporal stability: split 2004-2013 vs 2014-2023
s["half"] = np.where(s.year <= 2013, "a", "b")
h = s.groupby(["field", "half"]).apply(g).reset_index()
h = h.pivot(index="field", columns="half", values="share_funder")
print("half-period share_funder corr:", h.corr().iloc[0, 1] if h.notna().all(axis=1).sum() > 5 else "NA")
