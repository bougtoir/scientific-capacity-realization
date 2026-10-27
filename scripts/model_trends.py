#!/usr/bin/env python3
"""Finishing pass C: slow-moving trend confounding.

Specifications on the frozen panel (y2 articles, PPML):
  C1 baseline           : y2 ~ logR2 | cf + fy
  C2 country trends     : adds country-specific linear trend (year x country
                          parametrized as a continuous regressor per country via
                          `yr:c(country)`)
  C3 first difference   : feols on within country-field first differences
                          (dy2 growth ~ dlogR2), field x year FE
  C4 long difference    : 5-year changes in log y2 vs 5-year change in logR,
                          pooled OLS with field FE, clustered by country
Outputs: output/tables/trend_models.csv
"""
import pandas as pd, numpy as np, os
from pyfixest.estimation import fepois, feols

OUT = "output/tables"; os.makedirs(OUT, exist_ok=True)

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
df = df[df.y2 > 0].dropna(subset=["logR"]).copy()
df["cf"] = df.country + "_" + df.field.astype(str)
df["fy"] = df.field.astype(str) + "_" + df.year.astype(str)
df["yr"] = df.year - 2004

rows = []
def rec(spec, m, term):
    t = m.tidy()
    rows.append(dict(spec=spec, term=term, est=t.loc[term, "Estimate"],
                     lo=t.loc[term, "2.5%"], hi=t.loc[term, "97.5%"],
                     p=t.loc[term, "Pr(>|t|)"], n=int(m._N)))

# C1 baseline
m = fepois("y2 ~ logR | cf + fy", data=df, vcov={"CRV1": "country"})
rec("C1 baseline", m, "logR")

# C2 country-specific linear trends: interact continuous year with each country.
# Implement as within-country demeaned... PPML cannot demean; use explicit
# country x year-trend regressors via formula C(country):yr
m2 = fepois("y2 ~ logR + C(country):yr | cf + fy", data=df, vcov={"CRV1": "country"})
rec("C2 +country linear trends", m2, "logR")

# C3 within-change (first difference) on logs, field x year FE
d = df.sort_values(["cf", "year"]).copy()
d["ly2"] = np.log(d.y2)
d["dly2"] = d.groupby("cf")["ly2"].diff()
d["dlogR"] = d.groupby("cf")["logR"].diff()
d3 = d.dropna(subset=["dly2", "dlogR"])
m3 = feols("dly2 ~ dlogR | fy", data=d3, vcov={"CRV1": "country"})
rec("C3 first-diff (log-log)", m3, "dlogR")

# C4 long difference: 2014-2018 vs 2004-2008 mean change per country x field
d["period"] = np.select([d.year <= 2008, (d.year >= 2014) & (d.year <= 2018)],
                        ["p0", "p1"], default=None)
ld = d.dropna(subset=["period"]).groupby(["country", "field", "period"]).agg(
    ly2=("ly2", "mean"), logR=("logR", "mean")).reset_index()
w = ld.pivot_table(index=["country", "field"], columns="period", values=["ly2", "logR"])
w.columns = ["_".join(c) for c in w.columns]
w = w.dropna().reset_index()
w["dly2"] = w.ly2_p1 - w.ly2_p0
w["dlogR"] = w.logR_p1 - w.logR_p0
w["field"] = w.field.astype(str)
m4 = feols("dly2 ~ dlogR | field", data=w, vcov={"CRV1": "country"})
rec("C4 long-diff 04-08 to 14-18", m4, "dlogR")

# C2i as C2 plus the field resource-intensity interaction
fri = pd.read_csv("data/processed/field_resource_intensity.csv")
fmap = dict(zip(fri.field.astype(str), fri.ri_z))
df["ri_z"] = df.field.astype(str).map(fmap)
df["logR_x_ri"] = df.logR * df.ri_z
m2i = fepois("y2 ~ logR + logR_x_ri + C(country):yr | cf + fy",
             data=df, vcov={"CRV1": "country"})
rec("C2i interaction +country trends", m2i, "logR_x_ri")
rec("C2i interaction +country trends", m2i, "logR")

pd.DataFrame(rows).to_csv(f"{OUT}/trend_models.csv", index=False)
print(pd.DataFrame(rows).to_string())
print("C4 cells:", len(w))
