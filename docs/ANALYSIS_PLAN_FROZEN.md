# ANALYSIS PLAN — FROZEN (Phase 2)

Frozen: 2026-09-29, before primary results. Any later deviation is logged in DECISIONS.md as `data-necessity` | `robustness` | `exploratory`.

## 1. Countries (primary panel)

Data-driven inclusion rule (all must hold, audited in Phase 4):
- ≥30,000 OpenAlex works over 2000–2025 with `institutions.country_code = c`;
- World Bank GERD %GDP (`GB.XPD.RSDV.GD.ZS`) non-missing for ≥15 of 2000–2024;
- OECD MSTI HERD or equivalent academic-resource series available for ≥15 years **or** country flagged `resource_secondary=GERD` when HERD missing;
- stable ISO country code; not a city-state outlier (LU, SG handled but flagged; excluded only if they distort — decision logged).

Candidate universe (evaluated, not assumed): all OECD + CN, IN, BR, ZA, RU*, IR, EG, AR, CL, TW, HK, SG, TH, MY, ID, SA, IL, NZ. (*RU post-2022 data quality flagged.)

## 2. Primary period

- Descriptive: 2000–2025 (2025 included, flagged partial for citation outcomes).
- **Primary inferential window: 2004–2023** (allows lag-3 regressor back to 2000 within the panel and citation maturity for percentile outcomes).
- 2026 excluded entirely (incomplete).
- Citation-percentile outcomes (Y6/Y7): works published ≤2021 only (maturity).

## 3. Field taxonomy

- OpenAlex `primary_topic.field.id` (26 fields) — primary.
- Sensitivity: `domain` (4) aggregation; subfield-level (252) for intensity-score stability only.

## 4. Outcome funnel (per country × field × year, articles unless stated)

| Level | Definition | OpenAlex spec |
|---|---|---|
| Y1 | all indexed works | no type filter |
| Y2 | journal articles | `type:article` |
| Y3 | internationally collaborative articles | `type:article, countries_distinct_count:>1` |
| Y4 | English-language articles | `type:article, language:en` |
| Y5 | field-normalized above-average impact | `type:article, fwci:>1` (maturity ≤2021) |
| Y6 | top-10% cited | `citation_normalized_percentile.is_in_top_10_percent:true` (≤2021) |
| Y7 | top-1% cited | `citation_normalized_percentile.is_in_top_1_percent:true` (≤2021) |

Plus per country×year OA-status mix (`open_access.oa_status` group_by) and per country×field×year OA share (`open_access.is_oa:true`).

Counting method: **full counting** (work counted for every affiliated country) — primary; fractional counting = sensitivity via `institutions_distinct_count`/authorship-fraction sampling where feasible. Multi-affiliation work counted once per country.

## 5. Resource variables (hierarchy)

- **PRIMARY**: OECD MSTI **HERD** (higher-education R&D expenditure, constant PPP) — construct matches academic research resources; GERD fallback where HERD missing.
- **SECONDARY**: GERD %GDP (WB `GB.XPD.RSDV.GD.ZS`), researchers per million (WB `SP.POP.SCIE.RD.P6`), GBARD.
- **Normalization**: real PPP level per researcher where MSTI personnel data allow; otherwise log real level + log GDP.
- Model regressor: `log HERD_c,t-k` (and Δ variants for lag model).

## 6. Resource-intensity score (per OpenAlex field, global, 2004–2023 pooled + year-stratified for stability)

Inputs (from per-field random samples of works, `sample=`):
- mean/median authors per work (team scale);
- mean institutions per work (`institutions_distinct_count`);
- share of works with ≥1 award (funding intensity — flagged partial coverage);
- share internationally collaborative (`countries_distinct_count>1`);
- share with DOI + source-level median APC (listed, not paid) where available.

Primary score: **first principal component (PCA)** of standardized inputs = "resource sensitivity" index (continuous). Reported as `FIELD_RESOURCE_INTENSITY.csv`.
Sensitivities: equal-weighted z-score index; leave-one-component-out; rank-based score; score recomputed on two halves of the period.
Name: "resource intensity" (not "capital intensity" — inputs mix labor/team and funding, not capital stock).

## 7. Main model (Phase 7)

PPML with high-dimensional FE (pyfixest `fepois`):
`Y_cft ~ log R_c,t-2 + log R_c,t-2 × Intensity_f | country×field FE + field×year FE`, clustered by country.
Outcome: Y2 (articles). Secondary: each funnel level as share of Y2 or count.

## 8. Lag model (Phase 8)

Distributed lag k=0..8 on `Δlog R_ct` (and levels sensitivity); PPML + FE as above; report per-lag β_k, cumulative Σβ, 95% CI, p; alternate windows {0–4, 0–6, 0–8}; also long-lag (10–15) descriptive contrast vs human-capital lags.

## 9. Knowledge persistence (Phase 9)

Primary measure: **topic persistence** = share of OpenAlex topics (subfield level) present in country c's output in base period still present (≥1 work) in later window; plus within-country self-citation share trend (`referenced_works` of domestic works by domestic works — sampled). Compare output-flow change vs persistence change by country.

## 10. Mobility sensitivity (Phase 10, bounded)

For a fixed country set {JP, KR, UK, DE, FR, US} + contraction years identified from resource series: sample authors active (≥3 works) in a 3-yr pre-window with dominant field in top resource-intensity tercile; measure share of portfolio in lower terciles in post-window vs matched non-contraction cells. Approach = prompt option (A) rolling dominant-quantile transition share. Explicitly descriptive — not the Paper-2 Markov model.

## 11. Publication-access mechanism (Phase 11)

Bounded: country OA-status mix vs resource level; articles→top10% conversion by source DOAJ/APC strata; Japan TA 2023→2024 RUC/J-SPRINTA institutions event-check on OA share in eligible Springer/Nature hybrid journals (compact DiD-style descriptive; paper reserves full design for Paper 2).

## 12. Robustness matrix (Phase 12)

Pre-committed set (the 20 items in prompt §P), organized: measurement variants (resource measure, normalization, counting, taxonomy, intensity index), sample variants (US/CN excluded, OECD-only, high-income, COVID 2020–21 excluded, coverage), method variants (lag windows, citation maturity, collab adjustment), falsification battery (§Q items).

## 13. Reporting

Estimate + 95% CI + p + N + FE + cluster + model family for every inferential result. Raw and multiplicity-adjusted p where a family of tests is reported. No significance-only language; no causal claims from associational models.
