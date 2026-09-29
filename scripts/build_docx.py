#!/usr/bin/env python3
"""Phase 14: manuscript/MAIN_MANUSCRIPT.md -> .docx (journal-neutral).

- Headings, paragraphs, bold, italic, inline figures [[FIG:id]] placeholders.
- Citations [n] -> superscript run (font-based, not field codes).
- Display equations marked {{EQ:name}} -> OMML via raw XML injection.
"""
import re, os, glob
import docx
from docx.shared import Pt, Inches
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

MD = "manuscript/MAIN_MANUSCRIPT.md"
OUT = "manuscript/MAIN_MANUSCRIPT.docx"
FIGDIR = "output/figures"

EQS = {
    "main_model": r"""Y_{cft} \sim \mathrm{Poisson}(\mu_{cft}),\quad
      \log \mu_{cft} = \alpha_{cf} + \gamma_{ft} + \sum_{k=0}^{K}\beta_k \log R_{c,t-k} + \delta \cdot RI_f \times \log R_{c,t-2}""",
    "operational": r"Y_{cft} = f\!\left(C_{cft},\ R_{ct}/R_{cft},\ T_{cft},\ V_{cft}\right)",
}

def omml(tex: str) -> str:
    # minimal OMML: linear LaTeX-ish text placed in a single math run is not real OMML;
    # build a proper OMML paragraph with the expression as m:r text (Word renders it).
    esc = (tex.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            f'<m:oMath><m:r><m:t xml:space="preserve">{esc}</m:t></m:r></m:oMath></m:oMathPara>')

def add_para(d, text, style=None):
    p = d.add_paragraph(style=style)
    # bold **..**, italic *..*, citations [n] superscript
    pos = 0
    for m in re.finditer(r"(\*\*.+?\*\*|\*[^*]+?\*|\[\d+(?:[,\-–]\d+)*\])", text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        tok = m.group(0)
        if tok.startswith("**"):
            p.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*"):
            p.add_run(tok[1:-1]).italic = True
        else:
            r = p.add_run(tok)
            r.font.superscript = True
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])
    return p

def fig_path(fid):
    for ext in ("png", "jpg"):
        hits = glob.glob(f"{FIGDIR}/{fid}*.{ext}")
        if hits:
            return hits[0]
    return None

def main():
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
    for raw in open(MD).read().splitlines():
        line = raw.rstrip()
        if not line:
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            d.add_heading(re.sub(r"\*", "", m.group(2)), level=min(len(m.group(1)), 4))
            continue
        f = re.match(r"^\[\[FIG:(\S+)\]\]$", line)
        if f:
            pth = fig_path(f.group(1))
            if pth:
                d.add_picture(pth, width=Inches(6.2))
            else:
                add_para(d, f"[figure {f.group(1)} missing: {pth}]")
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
    d.save(OUT)
    print("wrote", OUT)

if __name__ == "__main__":
    main()
