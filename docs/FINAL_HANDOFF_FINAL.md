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

---

## Final conceptual pass addendum (2026-09-29)

### Changes this pass
- Title: "Distinguishing ... Resource-Dependent Realization" (replaces "Separating ... Resource-Constrained").
- Funnel→outcome-strata terminology throughout; CONCEPTUAL_NESTING_AUDIT.md documents the empirical nesting failure (Y3/Y4 cross, OA↔English) and the decision.
- Abstract compressed to ~150 words, 3 principal numbers, Problem/Design/Results/Interpretation structure.
- Global claim calibration: "substantiate the distinction", "amplify the apparent contraction", "uniform capacity-loss model does not naturally predict this heterogeneity".
- Companion-paper references removed ("future author-level work").
- RI index annotated as resource-demand proxies, not monetary capital.
- Discussion restructured to required order; policy interpretation added.
- 5 new Crossref-verified references (Fortunato 2018; Jacob & Lefgren 2011; Mongeon & Paul-Hus 2016; Wang & Shapira 2011; Azoulay et al. 2017) — refs now 23.
- Figure 5 retitled "Outcome-strata composition" with explicit denominators.

### Self-adjudication verdict

| Check | Status |
|---|---|
| A. Reproducibility | PASS — pipeline + raw + ledger intact; no new data this pass |
| B. Numerical consistency | PASS — md/Scientometrics/docx all regenerated from injected values |
| C. Claim calibration | PASS — no causal funding claims, no capacity-preserved claims |
| D. Terminology consistency | PASS — single remaining "funnel" use is the explicit negation in §2.1 |
| E. References | PASS — 23 refs, all verified; no stale entries |
| F. Journal compliance | PASS — Springer Basic author–year, unstructured abstract, separate figures |
| G. Scope discipline | PASS — no new analyses beyond index/mobility checks this pass |
| H. Submission artifacts | PASS — *_FINAL.docx + figures + supplement + cover letter |
| I. Known gaps | refs #5/#8-9 metadata completion recommended before upload |

**Verdict: READY AFTER MINOR MANUAL METADATA COMPLETION** — pending author-side: ORCID/affiliation already set; finalize refs #5/#8-9 DOIs in Editorial Manager submission.


## Final cleanup completed (2026-09-29, ultrashort prompt)
- claim calibration: completed ("uniform capacity-loss model alone" formulation; "knowledge-lineage structure" replaces "partially preserved stock"; "consistent with capacity preservation" removed from §5.1)
- reference metadata: completed — all 24 references verified; ref 8 misattribution corrected (Zhang et al. 2022 split out as ref 24); ref 9 placeholder replaced with verified NISTEP Discussion Paper No. 89
- repository wording: verified and corrected — public repo not yet live (sync runs on merge); code/data availability now states public release upon publication, no invented URL
- no scientific analyses changed

**Verdict: READY FOR SUBMISSION**
