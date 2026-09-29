#!/usr/bin/env python3
"""Finishing pass: cover letter + supplement docx for Scientometrics submission."""
import docx, os
from docx.shared import Pt
import pandas as pd

OUT = "manuscript/scientometrics"; os.makedirs(OUT, exist_ok=True)

def doc():
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
    return d

def paras(d, blocks):
    for kind, text in blocks:
        if kind == "h":
            d.add_heading(text, level=2)
        else:
            d.add_paragraph(text)

# ---------------- COVER LETTER ----------------
d = doc()
d.add_heading("Cover letter — submission to Scientometrics", level=1)
paras(d, [
    ("p", "Date: 2026-09-29"),
    ("p", "To the Editors of Scientometrics,"),
    ("p", "We submit the manuscript \"When Scientific Output Falls: Distinguishing "
          "Scientific Capacity from Resource-Dependent Realization\" for "
          "consideration as an Original Paper in Scientometrics."),
    ("p", "The paper's central contribution is a measurement distinction that is "
          "directly relevant to the journal's readership: national bibliometric "
          "indicators record realized scientific output, not latent scientific "
          "capacity, and the two diverge when the conversion of capability into "
          "visible publication is resource-dependent. Falling output therefore "
          "does not uniquely identify falling capacity — an interpretive issue "
          "at the core of national indicator use, exemplified by, but not "
          "limited to, the widely discussed Japanese case."),
    ("p", "Four aspects may interest Scientometrics reviewers and readers: (1) "
          "the analysis runs on an international country-by-field-by-year panel "
          "(52 countries, 26 OpenAlex fields, 2004-2023) rather than a single "
          "national series, with seven outcome strata spanning production, collaboration, "
          "dissemination, accessibility, and citation visibility — conceptually "
          "a state pathway from capacity to visibility, empirically a set of "
          "parallel outcome dimensions rather than a strictly nested sequence; (2) a field-level resource-intensity "
          "index built from seeded random samples of publication attributes "
          "shows that resource sensitivity concentrates exactly where resource "
          "dependence is largest, a gradient robust to index construction and "
          "to country-specific trends; (3) bounded author-level analyses "
          "quantify within-author reallocation between fields and show it is "
          "real but concentrated in a mobile minority; and (4) the "
          "interpretation is deliberately cautious — the level association is "
          "presented as a long-run relationship between persistent resource "
          "environments and realized output, not as evidence that short-term "
          "funding changes causally move output, and concurrent capacity "
          "deterioration cannot be excluded."),
    ("p", "All inputs are public (OpenAlex, OECD MSTI, World Bank); the full "
          "reproducibility pipeline, acquisition ledger, and processed datasets "
          "accompany the submission."),
    ("p", "The manuscript is original, is not under consideration elsewhere, "
          "and the author declares no competing interests."),
    ("p", "Sincerely,"),
    ("p", "Onishi Tatsuki\nData Science and AI Innovation Research Promotion "
          "Center, Shiga University\n1-1-1 Bamba, Hikone, Shiga 522-8522, "
          "Japan\nbougtoir@gmail.com\nORCID: 0000-0001-7261-9062"),
])
d.save(f"{OUT}/COVER_LETTER.docx")

# ---------------- SUPPLEMENT ----------------
d = doc()
d.add_heading("Supplementary material", level=1)

trend = pd.read_csv("output/tables/trend_models.csv")
rev = pd.read_csv("output/tables/intensity_revision.csv")
mobs = pd.read_csv("output/tables/mobility_sensitivity.csv")
pw = pd.read_csv("output/tables/persistence_weighted.csv")
lag = pd.read_csv("output/tables/lag_models.csv")

paras(d, [
    ("h", "S1. Resource-intensity index construction"),
    ("p", "The primary index is the first principal component of four upstream "
          "resource proxies estimated from 3,000 seeded random works per field: "
          "mean author count, institutional multiplicity, international "
          "collaboration share, and funder-acknowledgement share. Publication-"
          "side attributes (English-language share, DOI coverage, open-access "
          "status) are excluded from the primary index to avoid circularity "
          "with the visibility-stage outcomes. PC1 explains 89.2% of variance "
          "with loadings 0.48 (authors), 0.52 (institutions), 0.49 "
          "(international), 0.51 (funder share)."),
    ("p", "Secondary comparator: PC1 of all nine attributes (including the "
          "publication-side variables), Spearman rank correlation 0.958 with "
          "the primary index."),
    ("h", "Table S1. Leave-one-component-out and secondary-index interactions"),
])
t = d.add_table(rows=1, cols=6); t.style = "Table Grid"
for i, h in enumerate(["spec", "index", "estimate", "95% CI lo", "95% CI hi", "p"]):
    t.rows[0].cells[i].text = h
for _, r in rev.iterrows():
    c = t.add_row().cells
    for i, v in enumerate([r.spec, r["index"], f"{r.est:.3f}", f"{r.lo:.3f}",
                           f"{r.hi:.3f}", f"{r.p:.3g}"]):
        c[i].text = str(v)

paras(d, [
    ("h", "S2. Trend-confounding robustness"),
    ("p", "PPML with country-by-field and field-by-year fixed effects; SEs "
          "clustered by country. C2 adds country-specific linear trends; C3 "
          "first-differences the log-log relation; C4 is a long-difference "
          "model on 2004-2008 vs 2014-2018 mean changes."),
    ("h", "Table S2. Trend-robustness models"),
])
t = d.add_table(rows=1, cols=6); t.style = "Table Grid"
for i, h in enumerate(["spec", "term", "estimate", "95% CI lo", "95% CI hi", "p"]):
    t.rows[0].cells[i].text = h
for _, r in trend.iterrows():
    c = t.add_row().cells
    for i, v in enumerate([r.spec, r.term, f"{r.est:.3f}", f"{r.lo:.3f}",
                           f"{r.hi:.3f}", f"{r.p:.3g}"]):
        c[i].text = str(v)

paras(d, [
    ("h", "S3. Mobility / reallocation sensitivity"),
    ("p", "Author-level analysis on the six focus countries (de, fr, gb, jp, "
          "kr, us), windows 2008/2010 vs 2013/2016. post_share_lo_full: mean "
          "post-window output share in the low resource-intensity tercile "
          "among authors whose baseline dominant field was in the high "
          "tercile. post_share_lo_nonmover: the same among stable-field "
          "authors. mean_post_ri_fixed assigns each post-window work to the "
          "author's baseline dominant field."),
    ("h", "Table S3. Mobility sensitivity"),
])
t = d.add_table(rows=1, cols=7); t.style = "Table Grid"
for i, h in enumerate(["country", "n", "share_lo full", "share_lo non-mover",
                       "attenuation %", "RI actual", "RI fixed"]):
    t.rows[0].cells[i].text = h
for _, r in mobs.iterrows():
    c = t.add_row().cells
    for i, v in enumerate([r.country, int(r.n_authors),
                           f"{r.post_share_lo_full:.3f}",
                           f"{r.post_share_lo_nonmover:.3f}",
                           f"{abs(r.attenuation_pct):.0f}",
                           f"{r.mean_post_ri_actual:.2f}",
                           f"{r.mean_post_ri_fixed:.2f}"]):
        c[i].text = str(v)

paras(d, [
    ("h", "S4. Weighted knowledge-persistence metrics"),
    ("p", "Cosine similarity and weighted Jaccard of the subfield portfolio "
          "(count-weighted, top-200 subfields by period volume) between the "
          "2004-2008 base period and each later window."),
    ("h", "Table S4. Weighted persistence"),
])
t = d.add_table(rows=1, cols=4); t.style = "Table Grid"
for i, h in enumerate(["country", "window", "cosine", "weighted Jaccard"]):
    t.rows[0].cells[i].text = h
for _, r in pw.iterrows():
    c = t.add_row().cells
    for i, v in enumerate([r.country, r.window, f"{r.cosine:.3f}",
                           f"{r.weighted_jaccard:.3f}"]):
        c[i].text = str(v)

paras(d, [
    ("h", "S5. Distributed-lag coefficients"),
    ("p", "Year-over-year changes in log HERD at lags 0-8 (PPML, same fixed-"
          "effect structure); cumulative sum -0.021."),
    ("h", "Table S5. Distributed lags"),
])
t = d.add_table(rows=1, cols=5); t.style = "Table Grid"
for i, h in enumerate(["term", "estimate", "95% CI lo", "95% CI hi", "p"]):
    t.rows[0].cells[i].text = h
for _, r in lag.iterrows():
    c = t.add_row().cells
    c[0].text = str(r["Coefficient"])
    c[1].text = f"{r['Estimate']:.3f}"
    c[2].text = f"{r['2.5%']:.3f}"
    c[3].text = f"{r['97.5%']:.3f}"
    c[4].text = f"{r['Pr(>|t|)']:.3g}"

d.save(f"{OUT}/SUPPLEMENT.docx")
print("wrote cover letter + supplement")
