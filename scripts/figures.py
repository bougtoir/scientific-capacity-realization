#!/usr/bin/env python3
"""Publication-quality figures (Phase 6/T). PNG+PDF at 300dpi equivalent."""
import pandas as pd, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = "output/figures"; os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
                     "figure.dpi": 150, "savefig.dpi": 300, "font.family": "DejaVu Sans"})

p = pd.read_csv("data/processed/panel_country_field_year.csv")
r = pd.read_csv("data/processed/resources_country_year.csv"); r.columns=[c.lower() for c in r.columns]
MAP2 = {"jp":"jpn","kr":"kor","gb":"gbr","de":"deu","fr":"fra","it":"ita","es":"esp","nl":"nld","se":"swe",
        "ch":"che","at":"aut","be":"bel","dk":"dnk","fi":"fin","ie":"irl","no":"nor","pt":"prt","pl":"pol",
        "cz":"cze","gr":"grc","hu":"hun","sk":"svk","ca":"can","us":"usa","au":"aus","nz":"nzl","il":"isr",
        "cn":"chn","in":"ind","br":"bra","za":"zaf","ru":"rus","ir":"irn","eg":"egy","ar":"arg","cl":"chl",
        "th":"tha","my":"mys","id":"idn","sa":"sau","tw":"twn","hk":"hkg","sg":"sgp","pk":"pak","ng":"nga",
        "mx":"mex","tr":"tur","ua":"ukr","ro":"rou","bg":"bgr","hr":"hrv","si":"svn","ee":"est","lv":"lva",
        "lt":"ltu","lu":"lux","is":"isl","mt":"mlt","cy":"cyp"}
p["iso3"] = p.country.map(MAP2)
cy = p.groupby(["country","iso3","year"],as_index=False)[["y1","y2","y3","y4","y5","y6","y7"]].sum()
cy = cy.merge(r[["iso3","year","h_usdppp","g_pct_gdp","g_usdppp","t_rs_fte"]],on=["iso3","year"],how="left")

def save(fig, name):
    fig.tight_layout(); fig.savefig(f"{FIG}/{name}.png"); fig.savefig(f"{FIG}/{name}.pdf"); plt.close(fig)
    print("wrote", name)

# Figure 1: conceptual compartment model (matplotlib, no graphviz)
fig, ax = plt.subplots(figsize=(8.5, 3.4)); ax.axis("off")
boxes = [("Latent scientific\ncapacity stock $C$", 0.02, "stock"),
         ("Active\nresearch $A$", 0.27, "state"),
         ("Publishable\nproduction $P$", 0.52, "state"),
         ("Visible output $Y$\n(indexed/international)", 0.77, "emission")]
for txt, x, kind in boxes:
    fc = {"stock": "#eaf2fb", "state": "#f4f4f4", "emission": "#fdeee4"}[kind]
    ax.add_patch(plt.Rectangle((x, 0.42), 0.2, 0.34, fc=fc, ec="k", lw=1))
    ax.text(x+0.1, 0.59, txt, ha="center", va="center", fontsize=9)
for x in (0.22, 0.47, 0.72):
    ax.annotate("", xy=(x+0.05, 0.59), xytext=(x, 0.59),
                arrowprops=dict(arrowstyle="-|>", lw=1.4))
ax.text(0.245, 0.67, "$k_{CA}(R)$", ha="center", fontsize=9)
ax.text(0.495, 0.67, "$k_{AP}(R)$", ha="center", fontsize=9)
ax.text(0.745, 0.67, "$k_{PV}(V)$", ha="center", fontsize=9)
ax.add_patch(plt.Rectangle((0.27, 0.05), 0.45, 0.2, fc="#f9f9f0", ec="grey", lw=0.8))
ax.text(0.495, 0.15, "Resource environment $R$: funding, labour, infrastructure, time\n"
        "acts on transitions (realization), not directly on the stock", ha="center", va="center", fontsize=8)
ax.annotate("", xy=(0.42, 0.42), xytext=(0.42, 0.25), arrowprops=dict(arrowstyle="-|>", lw=1.1, color="grey"))
ax.annotate("", xy=(0.67, 0.42), xytext=(0.67, 0.25), arrowprops=dict(arrowstyle="-|>", lw=1.1, color="grey"))
ax.text(0.02, 0.90, "Observed bibliometric output $Y$ is a downstream emission of a multi-stage system;\n"
        "a fall in $Y$ does not uniquely identify a fall in $C$.", fontsize=9, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
save(fig, "fig1_conceptual_model")

# Figure 2: resource vs output trajectories, indexed (2015=100)
sel = [c for c in cy.iso3.dropna().unique()][:12]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharex=True)
for c in sel:
    d = cy[cy.iso3==c].sort_values("year")
    if len(d) < 8 or d.y2.max()==0: continue
    axes[0].plot(d.year, d.h_usdppp/d[d.year==2015].h_usdppp.iloc[0]*100 if (d.year==2015).any() else d.h_usdppp/d.h_usdppp.iloc[0]*100, lw=1, label=c)
    axes[1].plot(d.year, d.y2/d[d.year==2015].y2.iloc[0]*100 if (d.year==2015).any() else d.y2/d.y2.iloc[0]*100, lw=1, label=c)
axes[0].set_title("HERD (real USD PPP, 2015=100)"); axes[1].set_title("Articles (2015=100)")
axes[0].legend(fontsize=6, ncol=2)
for a in axes: a.set_xlabel("year")
save(fig, "fig2_resource_vs_output")
print(cy.iso3.unique())
