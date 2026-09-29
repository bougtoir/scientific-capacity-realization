#!/usr/bin/env python3
"""Update fig6: mobility sensitivity — full vs non-mover low-intensity share."""
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, os

FIG = "output/figures"; os.makedirs(FIG, exist_ok=True)
m = pd.read_csv("output/tables/mobility_sensitivity.csv").sort_values("country")
x = np.arange(len(m)); w = 0.38
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(x - w/2, 100*m.post_share_lo_full, w, label="All baseline high-intensity authors")
ax.bar(x + w/2, 100*m.post_share_lo_nonmover, w, label="Stable-field (non-mover) authors")
ax.set_xticks(x); ax.set_xticklabels(m.country.str.upper())
ax.set_ylabel("Post-window output share in low-intensity fields (%)")
ax.set_title("Within-author reallocation: full sample vs non-mover restriction")
for i, r in enumerate(m.itertuples()):
    ax.annotate(f"{abs(r.attenuation_pct):.0f}%", (x[i], 100*max(r.post_share_lo_full, r.post_share_lo_nonmover)+0.4),
                ha="center", fontsize=8)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(f"{FIG}/fig6_mobility.png", dpi=300); fig.savefig(f"{FIG}/fig6_mobility.pdf")
print("fig6 updated")
