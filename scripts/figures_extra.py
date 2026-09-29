#!/usr/bin/env python3
"""Figures 3,5,6,7: intensity index, output funnel, mobility, persistence."""
import pandas as pd, numpy as np, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

FIG="output/figures"; os.makedirs(FIG,exist_ok=True)
D="data/processed"

# fig3: field resource-intensity index
ri=pd.read_csv(f"{D}/field_resource_intensity.csv").sort_values("ri_z")
fig,ax=plt.subplots(figsize=(6.5,5.2))
ax.barh(ri.field_name,ri.ri_z,color=["#888" if v<0 else "#2a6" for v in ri.ri_z])
ax.set_xlabel("Resource-intensity index (PC1, z-score)")
ax.set_title("Field resource intensity (sampled OpenAlex attributes)")
fig.tight_layout(); fig.savefig(f"{FIG}/fig3_field_intensity.png"); fig.savefig(f"{FIG}/fig3_field_intensity.pdf"); plt.close(fig)

# fig5: outcome-strata composition for selected countries
p=pd.read_csv(f"{D}/panel_country_year.csv")
sel=["jp","us","cn","de","gb","kr"]
fig,axes=plt.subplots(1,2,figsize=(9,3.6))
for c in sel:
    s=p[p.country==c].sort_values("year")
    if len(s)==0: continue
    axes[0].plot(s.year,s.y2/s.y1,label=c)
    axes[1].plot(s.year,s.y4/s.y2,label=c)
axes[0].set_title("articles / all works"); axes[1].set_title("English / articles")
for a in axes: a.set_ylim(0,1); a.legend(fontsize=7)
fig.suptitle("Outcome-strata composition by country (each stratum on its own denominator)")
fig.tight_layout(); fig.savefig(f"{FIG}/fig5_funnel_composition.png"); fig.savefig(f"{FIG}/fig5_funnel_composition.pdf"); plt.close(fig)

# fig6: mobility — share moved to low-intensity tercile
mob=pd.read_csv("output/tables/mobility_summary.csv")
g=mob.groupby("country")[["share_moved_lo","d_ri"]].mean().sort_values("share_moved_lo")
fig,ax=plt.subplots(figsize=(5.5,3.2))
ax.bar(g.index,g.share_moved_lo,color="#b46")
ax.set_ylabel("share of post-window output in low-intensity tercile")
ax.set_title("Within-author field reallocation (pre: high-intensity dominant)")
fig.tight_layout(); fig.savefig(f"{FIG}/fig6_mobility.png"); fig.savefig(f"{FIG}/fig6_mobility.pdf"); plt.close(fig)

# fig7: subfield persistence
tp=pd.read_csv(f"{D}/topic_persistence.csv")
pv=tp.pivot(index="country",columns="window",values="persist_share").dropna()
pv=pv.sort_values(pv.columns[0])
fig,ax=plt.subplots(figsize=(6,3.6))
x=np.arange(len(pv))
for i,c in enumerate(pv.columns):
    ax.scatter(x,pv[c],s=12,label=c)
ax.set_xticks(x); ax.set_xticklabels(pv.index,fontsize=6,rotation=90)
ax.set_ylabel("persist_share"); ax.set_ylim(0,1.02); ax.legend(fontsize=7)
ax.set_title("Subfield presence persistence (base 2004-2008)")
fig.tight_layout(); fig.savefig(f"{FIG}/fig7_persistence.png"); fig.savefig(f"{FIG}/fig7_persistence.pdf"); plt.close(fig)
print("figs done")
