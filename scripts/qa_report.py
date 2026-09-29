#!/usr/bin/env python3
"""Phase 4: data QA / coverage audit -> docs/DATA_QA_REPORT.md (+ csv tables)."""
import pandas as pd, numpy as np, os, glob

p = pd.read_csv("data/processed/panel_country_field_year.csv")
r = pd.read_csv("data/processed/resources_country_year.csv")
r.columns = [c.lower() for c in r.columns]

lines = []
lines.append("# Data QA / Coverage Audit (Phase 4)\n")
lines.append(f"Generated: {pd.Timestamp.utcnow()}\n")

lines.append("\n## Panel dimensions\n")
lines.append(f"- country x field x year rows: {len(p):,}")
lines.append(f"- countries: {p.country.nunique()} | fields: {p.field.nunique()} | years: {p.year.min()}–{p.year.max()}")

lines.append("\n## Country inclusion screen (frozen rules)\n")
vol = p.groupby("country").y1.sum()
cov = r.groupby("iso3").gb_xpd_rsdv_gd_zs.apply(lambda s: s.notna().sum())
MAP2 = {"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","it":"ita","es":"esp","nl":"nld","se":"swe",
        "ch":"che","at":"aut","be":"bel","dk":"dnk","fi":"fin","ie":"irl","no":"nor","pt":"prt","pl":"pol",
        "cz":"cze","gr":"grc","hu":"hun","sk":"svk","ca":"can","us":"usa","au":"aus","nz":"nzl","il":"isr",
        "cn":"chn","in":"ind","br":"bra","za":"zaf","ru":"rus","ir":"irn","eg":"egy","ar":"arg","cl":"chl",
        "th":"tha","my":"mys","id":"idn","sa":"sau","tw":"twn","hk":"hkg","sg":"sgp","pk":"pak","ng":"nga",
        "mx":"mex","tr":"tur","ua":"ukr","ro":"rou","bg":"bgr","hr":"hrv","si":"svn","ee":"est","lv":"lva",
        "lt":"ltu","lu":"lux","is":"isl","mt":"mlt","cy":"cyp"}
scr = pd.DataFrame({"works": vol})
scr["iso3"] = scr.index.map(MAP2)
scr["gerd_years"] = scr.iso3.map(cov).fillna(0).astype(int)
scr["include"] = (scr.works >= 30000) & (scr.gerd_years >= 15)
scr.to_csv("data/processed/country_inclusion.csv")
lines.append(scr.sort_values("works", ascending=False).to_markdown())
lines.append(f"\nIncluded: {scr.include.sum()} / {len(scr)}")

lines.append("\n## Funnel consistency\n")
bad = (p.y2 > p.y1).sum() + (p.y3 > p.y2).sum() + (p.y4 > p.y2).sum()
lines.append(f"- rows violating Y-level nesting (y2>y1 or y3>y2 or y4>y2): {bad}")
lines.append(f"- zero-y2 rows (country-field-year with no articles): {(p.y2==0).sum()}")

lines.append("\n## Citation maturity\n")
lines.append("- citation outcomes (y5 fwci>1, y6 top10%, y7 top1%) collected only for publication_year <= 2021; later years are censored.")
mat = p[p.year<=2021].groupby("year")[["y5","y6","y7"]].sum().join(p[p.year<=2021].groupby("year").y2.sum().rename("y2"))
mat["top10_share"] = mat.y6/mat.y2
lines.append(mat[["y2","y6","top10_share"]].round(3).to_markdown())
lines.append("Expected ~0.10 share if percentile normalization holds across years; drift flags normalization issues.")

lines.append("\n## Resource series coverage\n")
for c in ["h_usdppp","g_usdppp","g_pct_gdp","t_rs_fte","gb_xpd_rsdv_gd_zs","sp_pop_scie_rd_p6"]:
    if c in r:
        lines.append(f"- {c}: {r[c].notna().sum()} obs, {r.groupby('iso3')[c].apply(lambda s:s.notna().sum()).describe()['min']:.0f}–{r.groupby('iso3')[c].apply(lambda s:s.notna().sum()).max():.0f} years/country")

lines.append("\n## Known limitations\n")
lines.append("- awards/funders not API-filterable; field funding intensity is sample-based")
lines.append("- author-ID disambiguation quality unknown until Phase 10 audit")
lines.append("- full vs fractional counting: primary is full counting; fractional sensitivity via author-share subsample")
lines.append("- 2025 rows may be affected by source-ingest lag; flagged in results")
open("docs/DATA_QA_REPORT.md","w").write("\n".join(lines))
print("written docs/DATA_QA_REPORT.md")
