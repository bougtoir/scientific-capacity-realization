#!/usr/bin/env python3
"""Primary panel models (Phase 7) — PPML with high-dimensional FE.

Prototype runs on available countries; final run covers the frozen panel.
Outputs: output/tables/primary_models.csv, output/tables/intensity_interaction.csv
"""
import pandas as pd, numpy as np, os
from pyfixest.estimation import fepois

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)

panel = pd.read_csv("data/processed/panel_country_field_year.csv")
res = pd.read_csv("data/processed/resources_country_year.csv")
res.columns = [c.lower() for c in res.columns]
# iso2 -> iso3 mapping for funnel countries
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

# primary resource regressor: log HERD real PPP (fallback GERD), lag 2
res = res.sort_values(["iso3", "year"])
for v in ["h_usdppp", "g_usdppp"]:
    res[f"l2_{v}"] = res.groupby("iso3")[v].shift(2)
res["logR"] = np.log(res["l2_h_usdppp"].fillna(res["l2_g_usdppp"]))
df = panel.merge(res[["iso3", "year", "logR", "h_usdppp", "g_usdppp", "t_rs_fte"]],
                 on=["iso3", "year"], how="left")
df = df[df.y2 > 0].dropna(subset=["logR"])
df["cf"] = df.country + "_" + df.field.astype(str)
df["fy"] = df.field.astype(str) + "_" + df.year.astype(str)

intensity = pd.read_csv("data/processed/field_resource_intensity.csv") if os.path.exists("data/processed/field_resource_intensity.csv") else None

m1 = fepois("y2 ~ logR | cf + fy", data=df, vcov={"CRV1": "country"})
print(m1.tidy())
res_rows = [{"model": "M1 baseline PPML", **{k: m1.tidy().loc[k].tolist() for k in m1.tidy().index}}
            ] if False else []
t = m1.tidy()
t["model"] = "M1_logHERD_lag2"
t.to_csv(f"{OUT}/primary_models.csv")

if intensity is not None:
    df = df.merge(intensity[["field", "ri_z"]], on="field", how="left")
    df["logR_x_ri"] = df.logR * df.ri_z
    m2 = fepois("y2 ~ logR + ri_z + logR_x_ri | cf + fy", data=df, vcov={"CRV1": "country"})
    t2 = m2.tidy(); t2["model"] = "M2_intensity"
    t2.to_csv(f"{OUT}/intensity_interaction.csv")
    print(t2)
