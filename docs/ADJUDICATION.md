# Phase 13 — Integrated Adjudication

Competing models: **C** capacity loss, **R** resource-constrained realization, **V** visibility constraint.
Verdicts per the pre-registered scale: SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / UNIDENTIFIABLE.
All estimates below are produced by `scripts/` outputs in `output/tables/` (robustness_matrix.csv, lag_models.csv, mobility_summary.csv, oa_conversion.csv, topic_persistence.csv); no value is hand-entered.

## Evidence summary

- Primary elasticity (y2 articles on log HERD, lag 2, cf+fy FE, PPML, clustered by country):
  0.526 (95% CI 0.387–0.665, p≈1e-13), n=19,152 cells, 52 included countries.
- Stability: lags 0–4 → 0.48–0.54; excl. US/CN 0.335 (p=0.013); OECD only 0.380 (p≈0.001); pre-2020 0.516; excl. COVID 0.554. WB GERD%GDP proxy 0.253 (n.s.) — expected, since the GDP share conflates the denominator; level/levels variants agree.
- Funnel gradient: all-works 0.538 → international 0.549 → English 0.543 → OA 0.861 → top-10% 1.065 (all significant). Resource sensitivity increases toward the internationally visible stages national indicators track.
- Intensity interaction: +0.190 (0.026–0.353, p=0.023); equal-weight index replicates (+0.190).
- Distributed lags on ΔlogR 0–8y: all small/n.s.; cumulative −0.021. Level association ≠ year-to-year shock response.
- Mobility (option A): authors with pre-window dominant field in high-intensity tercile put 14.1% (mean) of post-window output into low-intensity fields; Japan highest (15.6%); Δ field intensity ≈ −0.45 to −0.57 z.
- Persistence: share of subfields active in 2004–2008 still active in 2014–2018: mean 95.4%, Japan 98.5%; 2019–2023: mean 94.1%, Japan 97.0% (top-200 subfields by volume, uniform cap).
- Visibility mix: gold-OA share responds to resources (+0.772, p=0.007); hybrid share does not (−0.183, p=0.128). TA check: feasibility-bounded, not identified.
- Context: article counts peaked 2020–2021 for JP, US, DE, GB and fell 8–13% through 2023 — a shared post-2020 contraction, not a Japan-only event.

## Verdicts

### R — resource-constrained realization: SUPPORTED
Robust positive level elasticity, stable across measures, samples, and lags; concentrated where the model predicts (resource-intensive fields, deeper funnel stages). The Δ-specification shows the mechanism operates on persistent resource levels, which is what a staged stock→flow model implies.

### V — visibility constraint: PARTIALLY SUPPORTED
Funnel gradient (elasticity rising toward visible stages) and the gold-OA/resource correlation are consistent with a resource-sensitive visibility margin. Direct TA/APC mechanism is underpowered (institution lists JS-rendered; 2023–24 window too short) — reported as feasibility-bound, not as an estimate.

### C — capacity loss: CANNOT BE EXCLUDED / NOT UNIQUELY IDENTIFIED
Output decline does not uniquely identify capacity decline: subfield structure is nearly fully preserved (Japan 97–98.5%), within-author reallocation is bounded (~14%), and the contraction is internationally shared. These are consistent with partly preserved capacity — they do not prove it. Absence of capacity decline is not claimed.

### Central proposition
"Declining scientific output does not uniquely identify declining underlying scientific capacity."
**SUPPORTED** — a measurable resource-dependent realization stage intervenes between capacity and indicators, and its observational signature (intensity gradient, funnel gradient, level-vs-change asymmetry) is present while structural-persistence measures show no collapse.
