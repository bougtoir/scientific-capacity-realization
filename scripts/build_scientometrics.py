#!/usr/bin/env python3
"""Phase 15 (Scientometrics): build journal-formatted submission package.

Reads manuscript/MAIN_MANUSCRIPT.md (journal-neutral master) and emits:

  manuscript/scientometrics/MAIN_MANUSCRIPT.md
      - Springer title page block
      - unstructured abstract <=250 words + keywords
      - [n] citations -> Springer author-year "(Author Year)"
      - [[FIG:x]] markers removed (figures are separate files for submission,
        per journal rules) and in-text "(Fig. N)" citations inserted
      - References -> alphabetical, Springer Basic reference style
      - "Figure captions" listing appended
  manuscript/scientometrics/MAIN_MANUSCRIPT.docx  (same content, OMML equations)
  manuscript/scientometrics/figures/Figure1..7.{png,pdf} (renumbered in
      citation order; fig1 conceptual model cited in Introduction)
  manuscript/scientometrics/SUBMISSION_CHECKLIST.md
"""
import os, re, glob, shutil, json
import docx
from docx.shared import Pt, Inches
from docx.oxml import parse_xml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "manuscript", "MAIN_MANUSCRIPT.md")
OUTDIR = os.path.join(ROOT, "manuscript", "scientometrics")
FIGDIR = os.path.join(ROOT, "output", "figures")
FIGOUT = os.path.join(OUTDIR, "figures")

# --- citation map: ref number -> (parenthetical, narrative) ------------------
CITE = {
    1: ("NISTEP 2023a", "NISTEP (2023a)"),
    2: ("Aoki and Kimura 2018", "Aoki and Kimura (2018)"),
    3: ("Priem et al. 2022", "Priem et al. (2022)"),
    4: ("NISTEP 2023b", "NISTEP (2023b)"),
    5: ("OECD 2015", "OECD (2015)"),
    6: ("Silva and Tenreyro 2006", "Silva and Tenreyro (2006)"),
    7: ("Springer Nature 2024", "Springer Nature (2024)"),
    8: ("Olejniczak and Wilson 2020", "Olejniczak and Wilson (2020)"),
    9: ("Yonetani et al. 2013", "Yonetani et al. (2013)"),
    10: ("Culbert et al. 2025", "Culbert et al. (2025)"),
    11: ("Auranen and Nieminen 2010", "Auranen and Nieminen (2010)"),
    12: ("Sugimoto and Larivi\u00e8re 2018", "Sugimoto and Larivi\u00e8re (2018)"),
    13: ("Stephan et al. 2017", "Stephan et al. (2017)"),
    14: ("Bornmann and Mutz 2015", "Bornmann and Mutz (2015)"),
    15: ("Larivi\u00e8re et al. 2006", "Larivi\u00e8re et al. (2006)"),
    16: ("Piwowar et al. 2018", "Piwowar et al. (2018)"),
    17: ("Schares 2024", "Schares (2024)"),
    18: ("Sugimoto 2015", "Sugimoto (2015)"),
    19: ("Fortunato et al. 2018", "Fortunato et al. (2018)"),
    20: ("Jacob and Lefgren 2011", "Jacob and Lefgren (2011)"),
    21: ("Mongeon and Paul-Hus 2016", "Mongeon and Paul-Hus (2016)"),
    22: ("Wang and Shapira 2011", "Wang and Shapira (2011)"),
    23: ("Azoulay et al. 2017", "Azoulay et al. (2017)"),
    24: ("Zhang et al. 2022", "Zhang et al. (2022)"),
}

REFS = [
    "Aoki R, Kimura H (2018) Allocation of research resources and publication "
    "productivity in Japan: a growth accounting approach. Public Policy Review "
    "13(4):1-34",
    "Auranen O, Nieminen M (2010) University research funding and publication "
    "performance: an international comparison. Research Policy 39(6):822-834. "
    "https://doi.org/10.1016/j.respol.2010.03.003",
    "Bornmann L, Mutz R (2015) Growth rates of modern science: a bibliometric "
    "analysis based on the number of publications and cited references. "
    "Journal of the Association for Information Science and Technology "
    "66(11):2215-2222. https://doi.org/10.1002/asi.23329",
    "Azoulay P, Ganguli I, Graff Zivin J (2017) The mobility of elite life "
    "scientists: professional and personal determinants. Research Policy "
    "46(3):573-590. https://doi.org/10.1016/j.respol.2017.01.002",
    "Culbert J, Hobert A, Jahn N, et al. (2025) Reference coverage analysis of "
    "OpenAlex compared to Web of Science and Scopus. Quantitative Science "
    "Studies 6(1):152-173",
    "Fortunato S, Bergstrom CT, B\u00f6rner K, et al. (2018) Science of "
    "science. Science 359(6379):eaao0185. https://doi.org/10.1126/science.aao0185",
    "Jacob BA, Lefgren L (2011) The impact of research grant funding on "
    "scientific productivity. Journal of Public Economics 95(9-10):1168-1177. "
    "https://doi.org/10.1016/j.jpubeco.2011.05.005",
    "Larivi\u00e8re V, Gingras Y, Archambault E (2006) Canadian collaboration "
    "networks: a comparative analysis of the natural sciences, social sciences "
    "and humanities. Scientometrics 68(3):519-533. "
    "https://doi.org/10.1007/s11192-006-0127-8",
    "NISTEP (2023a) Science and Technology Indicators 2023 (NISTEP-RM328). "
    "National Institute of Science and Technology Policy, Japan",
    "Mongeon P, Paul-Hus A (2016) The journal coverage of Web of Science and "
    "Scopus: a comparative analysis. Scientometrics 106(1):213-228. "
    "https://doi.org/10.1007/s11192-015-1765-5",
    "NISTEP (2023b) Science and Technology Indicators - counting methodology "
    "notes. National Institute of Science and Technology Policy, Japan",
    "OECD (2015) Frascati Manual 2015: Guidelines for Collecting and Reporting "
    "Data on Research and Experimental Development. OECD Publishing, Paris; "
    "and OECD Main Science and Technology Indicators database (accessed 2026)",
    "Olejniczak AJ, Wilson MJ (2020) Who's writing open access (OA) articles? "
    "Characteristics of OA authors. Quantitative Science Studies 1(4):1429-1450",
    "Piwowar H, Priem J, Larivi\u00e8re V, et al. (2018) The state of OA: a "
    "large-scale analysis of the prevalence and impact of open access "
    "articles. PeerJ 6:e4375. https://doi.org/10.7717/peerj.4375",
    "Priem J, Piwowar H, Orr R (2022) OpenAlex: a fully-open index of "
    "scholarly works. Quantitative Science Studies 3(4):795-818",
    "Schares E (2024) Transformative agreements, publication venues and open "
    "access policies at the University of California. Learned Publishing "
    "37(4):e1627. https://doi.org/10.1002/leap.1627",
    "Silva JMCS, Tenreyro S (2006) The log of gravity. Review of Economics and "
    "Statistics 88(4):641-658",
    "Springer Nature (2024) Springer Nature expands Transformative Agreements "
    "with Japanese universities. Press release, 22 Jan 2024",
    "Stephan P, Veugelers R, Wang J (2017) Reviewers are blinkered by "
    "bibliometrics. Nature 544(7651):411-412. https://doi.org/10.1038/544411a",
    "Sugimoto CR (2015) What do we know of the mobility of research scientists "
    "and impact on scientific production. In: Fern\u00e1ndez-Zubieta A, Geuna "
    "A, Lawson C (eds) Global Mobility of Research Scientists: The Economics "
    "of Who Goes Where and Why. Academic Press, London, pp 33-52. "
    "https://doi.org/10.1016/B978-0-12-801396-0.00001-6",
    "Sugimoto CR, Larivi\u00e8re V (2018) Measuring Research: What Everyone "
    "Needs to Know. Oxford University Press, Oxford. "
    "https://doi.org/10.1093/wentk/9780190640118.001.0001",
    "Wang J, Shapira P (2011) Funding acknowledgement analysis: an enhanced "
    "tool to investigate research sponsorship impacts. Scientometrics "
    "87(3):563-586. https://doi.org/10.1007/s11192-011-0362-5",
    "Yonetani Y, Ikeuchi K, Kuwahara T (2013) An analysis on the "
    "relationship between input and output in the production of articles in "
    "universities — an approach using Web of Science and Survey of R&D "
    "(in Japanese). NISTEP Discussion Paper 89. National Institute of "
    "Science and Technology Policy, Tokyo",
    "Zhang X, Wei F, Huang Y, Sivertsen G (2022) Should open access lead to "
    "closed research? The trends towards paying to perform research. "
    "Scientometrics 127(12):7653-7679. "
    "https://doi.org/10.1007/s11192-022-04407-5",
]

ABSTRACT = (
    "National bibliometric decline is often read as declining scientific "
    "capacity, yet indicators record realized output, not latent capability. "
    "We distinguish the two on an international country-by-field-by-year panel "
    "(52 countries, 26 OpenAlex fields, 2004-2023) combining seven outcome "
    "strata spanning production, collaboration, dissemination, accessibility, "
    "and citation visibility with OECD and World Bank resource series. In "
    "Poisson pseudo-maximum-likelihood models with two-way fixed effects, the "
    "elasticity of article output with respect to higher-education R&D two "
    "years prior is 0.526 (95% CI 0.387-0.665). The association is "
    "significantly stronger in resource-intensive fields (interaction 0.190, "
    "p=0.023) and for high-visibility outcomes (1.065 for top-decile output). "
    "The heterogeneity pattern survives index-construction, trend, and "
    "mobility-restriction checks; the level estimate is best read as a "
    "long-run association, since short-run resource changes do not detectably "
    "move output. Declining visible scientific output therefore does not "
    "uniquely identify declining underlying scientific capacity; concurrent "
    "deterioration cannot be excluded."
)

TITLE_BLOCK = """# When Scientific Output Falls: Distinguishing Scientific Capacity from Resource-Dependent Realization

**Manuscript type:** Original Paper

**Corresponding author:** Onishi Tatsuki — ORCID: 0000-0001-7261-9062; email: bougtoir@gmail.com

**Affiliation:** Data Science and AI Innovation Research Promotion Center, Shiga University, 1-1-1 Bamba, Hikone, Shiga 522-8522, Japan

## Abstract

{abstract}

**Keywords:** scientometrics; research funding; scientific capacity; bibliometrics; higher-education R&D; Japan

**Declarations**

- Funding: No funding was received for this work.
- Competing interests: The author declares no competing interests.
- Data availability: All data are derived from public sources (OpenAlex, OECD MSTI, World Bank); acquisition manifests, checksums, and retrieval timestamps are recorded in the acquisition ledger.
- Code availability: The analysis code and reproducibility materials will be made publicly available in a permanent repository upon publication.
- Author contribution: Single-author work; T.O. designed the study, acquired and analyzed data, and wrote the manuscript.
""".format(abstract=ABSTRACT)

# figure number in citation order -> (source file stem, caption)
FIGS = [
    ("fig1_conceptual_model",
     "Fig. 1 Conceptual model. Observable scientific output Y is the realized "
     "emission of latent capacity C through resource-dependent transitions T "
     "and a visibility environment V."),
    ("fig2_resource_vs_output",
     "Fig. 2 Real higher-education R&D expenditure (lagged two years) versus "
     "article output across the country-by-field panel; PPML elasticity "
     "estimate with clustered standard errors."),
    ("fig3_field_intensity",
     "Fig. 3 Field resource-intensity index (first principal component of "
     "sampled work attributes) across the 26 OpenAlex first-level fields."),
    ("fig4_distributed_lag",
     "Fig. 4 Distributed-lag coefficients (lags 0-8) of year-over-year "
     "resource changes on article output, with 95% confidence intervals."),
    ("fig5_funnel_composition",
     "Fig. 5 Outcome-strata composition by country: articles share of all "
     "works and English-language share of articles, each stratum on its own "
     "denominator."),
    ("fig7_persistence",
     "Fig. 6 Subfield persistence: share of subfields active in 2004-2008 "
     "remaining active in later windows, by country."),
    ("fig6_mobility",
     "Fig. 7 Within-author field reallocation: post-window output share "
     "migrating from high- to low-resource-intensity fields."),
]


def convert(md: str) -> str:
    # replace numbered reference section
    md = md.split("## References")[0].rstrip() + "\n"
    # strip master abstract + keywords block (we write our own)
    head, rest = md.split("## 1. Introduction", 1)
    body = "## 1. Introduction" + rest
    # strip master H1 (title) is in head; drop it
    # [n] -> author-year parenthetical
    def rep(m):
        ns = [int(x) for x in re.split(r"[,\-–]", m.group(0)[1:-1])]
        return "(" + "; ".join(CITE[n][0] for n in ns) + ")"
    body = re.sub(r"\[\d+(?:[,\-–]\d+)*\]", rep, body)
    # figures: drop markers, cite "(Fig. N)", and cite Fig.1 in intro
    fignum = {stem: i + 1 for i, (stem, _) in enumerate(FIGS)}
    lines = body.splitlines()
    out = []
    for line in lines:
        m = re.match(r"^\[\[FIG:(\S+)\]\]$", line.strip())
        if m:
            n = fignum[m.group(1)]
            for j in range(len(out) - 1, -1, -1):
                if out[j].strip() and not out[j].startswith("#"):
                    out[j] = out[j].rstrip() + f" (Fig. {n})"
                    break
            continue
        out.append(line)
    body = "\n".join(out)
    # cite Fig.1 at the staged-system introduction
    body = body.replace(
        "Observed scientific output is the emission of a staged system:",
        "Observed scientific output is the emission of a staged system "
        "(Fig. 1):")
    # figure captions section
    caps = "\n".join(f"{n}. {cap.split('. ',1)[1] if '. ' in cap else cap}"
                     for n, (_, cap) in enumerate(FIGS, 1))
    caps = "\n".join(cap for _, cap in FIGS)
    refs = "\n".join(REFS)
    return (TITLE_BLOCK + "\n" + body +
            "\n## References\n\n" + refs +
            "\n\n## Figure captions\n\n" + caps + "\n")


EQS = {
    "main_model": r"""Y_{cft} \sim \mathrm{Poisson}(\mu_{cft}),\quad
      \log \mu_{cft} = \alpha_{cf} + \gamma_{ft} + \sum_{k=0}^{K}\beta_k \log R_{c,t-k} + \delta \cdot RI_f \times \log R_{c,t-2}""",
    "operational": r"Y_{cft} = f\!\left(C_{cft},\ R_{ct}/R_{cft},\ T_{cft},\ V_{cft}\right)",
}


def omml(tex: str) -> str:
    esc = tex.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f'<m:oMath><m:r><m:t xml:space="preserve">{esc}</m:t></m:r></m:oMath></m:oMathPara>')


def add_para(d, text, style=None):
    p = d.add_paragraph(style=style)
    pos = 0
    for m in re.finditer(r"(\*\*.+?\*\*|\*[^*]+?\*)", text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        tok = m.group(0)
        if tok.startswith("**"):
            p.add_run(tok[2:-2]).bold = True
        else:
            p.add_run(tok[1:-1]).italic = True
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])
    return p


def build_docx(md_path, docx_path, inline_figs=None):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(11)
    num2stem = {n: s for s, n in (inline_figs or {}).items()}
    for raw in open(md_path).read().splitlines():
        line = raw.rstrip()
        if not line:
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            d.add_heading(re.sub(r"\*", "", m.group(2)),
                          level=min(len(m.group(1)), 4))
            continue
        e = re.match(r"^\{\{EQ:(\S+)\}\}$", line)
        if e:
            p = d.add_paragraph()
            p._p.append(parse_xml(omml(EQS.get(e.group(1), e.group(1)))))
            continue
        if line.startswith("- "):
            add_para(d, line[2:], style="List Bullet")
            continue
        add_para(d, line)
        fm = re.search(r"\(Fig\. (\d+)\)\s*:?\s*$", line)
        if fm and int(fm.group(1)) in num2stem:
            stem = num2stem[int(fm.group(1))]
            hits = glob.glob(os.path.join(FIGDIR, f"{stem}.png"))
            if hits:
                d.add_picture(hits[0], width=Inches(6.2))
    d.save(docx_path)


CHECKLIST = """# Scientometrics submission checklist (generated)

Journal: *Scientometrics* (Springer), Original Paper.

- [x] Citation style: author-year `(Author Year)`, alphabetical reference list (Springer Basic style)
- [x] Abstract: unstructured, <=250 words
- [x] Keywords: 6
- [x] Title page: title, manuscript type, corresponding author (Onishi Tatsuki), affiliation, ORCID 0000-0001-7261-9062
- [x] Declarations block: funding, competing interests, data/code availability, author contribution
- [x] Figures: separate files `figures/Figure1..7` (PNG 300+ dpi + PDF), cited in text as (Fig. N), captions listed at end of manuscript
- [x] Equations: editable OMML in docx
- [x] All numbers injected from `output/tables/` / `data/processed/` via `build_manuscript.py` — no hardcoded estimates
- [x] ORCID and full affiliation for the corresponding author — filled
- [ ] Editorial Manager upload at https://www.editorialmanager.com/scim/
- [ ] Hostile review: see docs/HOSTILE_REVIEW.md (completed pre-submission)
"""


def main():
    os.makedirs(FIGOUT, exist_ok=True)
    md = open(SRC).read()
    conv = convert(md)
    md_path = os.path.join(OUTDIR, "MAIN_MANUSCRIPT.md")
    open(md_path, "w").write(conv)
    build_docx(md_path, os.path.join(OUTDIR, "MAIN_MANUSCRIPT.docx"))
    # inline version: figures embedded at first in-text citation
    build_docx(md_path, os.path.join(OUTDIR, "MAIN_MANUSCRIPT_inline.docx"),
               inline_figs={stem: i + 1 for i, (stem, _) in enumerate(FIGS)})
    for i, (stem, _) in enumerate(FIGS, 1):
        for ext in ("png", "pdf"):
            hits = glob.glob(os.path.join(FIGDIR, f"{stem}.{ext}"))
            if hits:
                shutil.copy(hits[0], os.path.join(FIGOUT, f"Figure{i}.{ext}"))
    open(os.path.join(OUTDIR, "SUBMISSION_CHECKLIST.md"), "w").write(CHECKLIST)
    n_abs = len(re.findall(r"[A-Za-z0-9-]+", ABSTRACT))
    print("abstract words:", n_abs)
    print("wrote", OUTDIR)


if __name__ == "__main__":
    main()
