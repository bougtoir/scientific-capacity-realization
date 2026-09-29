# Final handoff — Scientometrics finishing pass

## Final classification: B — ROBUST BUT MORE QUALIFIED

The central interpretation survives every targeted correction; the required recalibration is in the *type* of association claimed (long-run resource association, not short-term causation), not in the headline numbers.

## Which original claims changed

1. Level elasticity reframed: "robust elasticity" → "long-run association between persistent resource environments and realized output differences" (attenuates to 0.470, p=0.068 under country trends; long-difference 0.473, p=1.4e-6; first-diff null 0.063).
2. Mobility: "bounded, cannot account for the pattern" → "real mediator concentrated in a mobile minority" (14.1% full vs 7.7% non-mover; ~45% attenuation; fixed-portfolio RI 1.06 vs realized 0.58). New paragraph in Discussion: resource constraints affect output within fields AND movement between fields.
3. OA/APC: "APC-as-paywall" removed → "resource-dependent access to paid OA channels"; hybrid non-OA path acknowledged; TA kept feasibility-bound.
4. Persistence: presence-only → presence + weighted cosine/Jaccard (JP cosine 0.98, WJ 0.79).
5. Index: documented upstream-only construction (already implemented); LOO sensitivity added (0.172-0.194); full index demoted to secondary robustness (0.145, p=0.050).

## Which coefficients changed

None on the primary estimates — the index was already upstream-only (interaction 0.190, p=0.023; unchanged under country trends 0.190, p=0.025). Newly reported: C2 0.470 (p=0.068), C3 0.063 (n.s.), C4 0.473 (p=1.4e-6), LOO 0.172-0.194, full-index 0.145 (p=0.050), mobility attenuation 45%, weighted persistence.

## Newly added analyses

- field_intensity_revision.py (LOO + contaminated comparator + rank corr)
- mobility_sensitivity2.py (non-mover restriction + fixed portfolio)
- model_trends.py (country trends, first-diff, long-diff, trend-adjusted interaction)
- persistence_weighted.py (cosine + weighted Jaccard)
- fig6 rebuilt (full vs non-mover bars)

## Remaining limitations

- Level association is associational; no quasi-experimental resource shock (reserved for Paper 2).
- Mobility sample: 6 countries, one window, sampled authors.
- TA visibility mechanism underpowered.
- Top-200 subfield truncation in persistence.

## Scientometrics readiness

Package complete at manuscript/scientometrics/: MAIN_MANUSCRIPT.{md,docx} (author-year, alphabetical refs, ≤250-word abstract, declarations), MAIN_MANUSCRIPT_inline.docx (figures embedded), COVER_LETTER.docx, SUPPLEMENT.docx, figures/Figure1-7 (PNG 300dpi + PDF), SUBMISSION_CHECKLIST.md. Ready for Editorial Manager upload after author review.
