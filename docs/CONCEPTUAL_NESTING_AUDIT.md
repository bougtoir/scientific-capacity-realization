# Conceptual nesting audit — outcome "funnel" (2026-09-29)

## Empirical check (panel_country_field_year.csv, 39,613 cf-year cells)

| Stratum | Definition | Denominator implied | Strictly nested? |
|---|---|---|---|
| Y1 all works | all OpenAlex works | — | base |
| Y2 journal articles | type:article | ⊆ Y1 | YES (0 violations) |
| Y3 international collaboration | authors in >1 country | ⊆ Y2 | YES within Y2 (0 violations) |
| Y4 English-language | language=en | ⊆ Y2 | YES within Y2 (0 violations) |
| Y5 above-mean FNCI | fnci>1 | ⊆ Y2 | YES within Y2 (0 violations) |
| Y6 top-decile cited | top-10% normalized | ⊆ Y2 | YES within Y2 (0 violations) |
| Y7 top-percentile | top-1% normalized | ⊆ Y6 | YES within Y2 |
| Y2_oa open access | oa in {gold,hybrid,bronze,diamond} | ⊆ Y2 | YES within Y2 |

## Cross-stratum nesting — FAILS

- Y3 vs Y4: neither contains the other — 98.4% of cells have Y4>Y3 and 0.6% have Y3>Y4; overlapping attributes, not sequential stages.
- Y2_oa vs Y4: OA output exceeds English output in 8.9% of cells — OA is not downstream of English (non-English OA exists; English non-OA exists).

## Verdict

NOT strictly nested. Y2-Y7 form a one-sided inclusion cone around articles, but collaboration, language, and access strata are parallel attributes of the same article population, not sequential gates.

## Decision

"Seven-stage funnel" replaced throughout with **"seven outcome strata spanning production, collaboration, dissemination, accessibility, and citation visibility"** (shorthand: outcome strata). The conceptual state pathway (capacity → production → dissemination → visibility) is retained as a *theoretical* sequence and explicitly distinguished from the empirical strata.

## Manuscript locations changed (build_manuscript.py)

- Abstract Methods/Results: "seven-stage output funnel" → "seven outcome strata"; "deeper funnel stages" → "higher-visibility strata"
- §1 contributions: funnel claim → outcome-strata claim
- §2.1 heading "Output funnel" → "Outcome strata"; added explicit denominator note
- §4.4 heading "Where the funnel binds" → "Heterogeneity across outcome strata"
- §5.1, §5.3, §6: funnel → strata
- Figure 5 (fig5_funnel_composition): title/labels → "Outcome-strata composition"; caption states denominators
