# Phase 12 — Hostile Review (disconfirmation-seeking)

Simulated referee report. Each point states the attack, then how it stands after checking.

## Major objections

**1. The 0.53 elasticity is cross-country, not causal.** cf FE absorbs country×field level; fy absorbs global shocks — but identification still comes from countries with persistently different resource levels trending differently. A country with flat HERD and flat output contributes "zero deviations" — the β may be driven by co-trended levels rather than response.
*Standing:* partly valid. This is why the ΔlogR distributed-lag spec is reported: year-to-year changes show ~0 effect, so the claim is stated as a *level association* consistent with a realization stage, not a causal shock response. The intensity interaction (+0.19) is harder to explain by co-trending — a generic omitted variable would need to also vary by field intensity. Verdict: level claim retained with calibrated language ("is associated with / is consistent with", never "causes").

**2. PPML with two-way FE and clustered SE — but the elasticity could be a composition artifact.** As China's share grows, field×year FE should absorb that. If high-resource countries specialize in high-output fields, cf FE absorbs it. Remaining channel: fields differ in their growth rates by country — that's exactly what the intensity interaction tests.
*Standing:* the interaction result survives precisely this objection; it is the strongest evidence. Reported prominently.

**3. Japan 2021–23 decline is a global post-COVID artifact, not Japan.** US/DE/GB also fell 8–13% from 2020/21 peaks.
*Standing:* correct and we say it. The paper never claims a Japan-unique contraction; the model is cross-national and Japan is "an informative case".

**4. group_by counts ≠ publications.** OpenAlex `institutions.country_code` attribution counts any affiliated author; multi-country papers count fully in each country — inflating collaboration economies.
*Standing:* stated in methods (full counting, per indicator convention); funnel stage y3 isolates the collaborative component explicitly.

**5. Field "resource intensity" is a proxy of proxies.** PCA-1 on authorship/funding shares = 89% variance — it may just measure "team science" not money sensitivity.
*Standing:* acknowledged; equal-weight index replicates the interaction; interpretation kept as "resource intensity/sensitivity" (never "capital intensity" per plan). Sample-based estimate carries sampling error — n=3,000/field.

**6. Top-200 subfield truncation.** group_by caps at 200 groups; persistence uses the top 200 of 252 — tail subfields (low volume, possibly higher churn) omitted uniformly.
*Standing:* disclosed. Bias direction: persistence is likely *overstated* in all countries equally — flagged as a limitation, and the Japan-vs-mean contrast remains informative.

**7. Mobility "14%" depends on window/tercile/country choices.**
*Standing:* single window, 6 focus countries, documented as bounded sensitivity per plan option A — not a population estimate; the full transition model is explicitly deferred to Paper 2.

**8. OA-share regression is ecological.** sh_oa_gold correlated with resources at country×year level — could reflect income, not APC constraint.
*Standing:* associational language used; reported under "bounded feasibility" heading only.

**9. Reverse causality: strong output attracts funding.**
*Standing:* lag-2 helps; cannot exclude fully. States explicitly in Limitations; ΔlogR spec also bounds a fast reverse channel (immediate output→funding response would show up in contemporaneous coefficients — they are ~0, which actually argues against fast feedback).

**10. Missing countries / selection.** 52 included; Switzerland, Australia, Taiwan, Indonesia excluded on the ≥15y rule — includes some genuinely data-rich countries with periodic surveys.
*Standing:* disclosed in DATA_QA; OECD-only sensitivity replicates the main effect at 0.38.

**11. p-hacking across 20 specs.** Robustness matrix pre-committed in ANALYSIS_PLAN_FROZEN before results were known; all p-values retained, including the null ΔlogR row that cuts against the causal reading.

**12. "Capacity preserved" is unfalsifiable.** The paper would be stronger claiming nothing about C.
*Standing:* we do not claim capacity is preserved — only that output decline does not uniquely identify its decline; persistence evidence is offered as necessary-not-sufficient.

## Outcome

Two objections changed the manuscript's claims: (1) causal language downgraded to association + mechanism-consistency; (9) the null distributed-lag result is featured as a finding, not buried. None overturns the adjudication.

# Finishing-pass addendum (Scientometrics targeting)

Updated after the targeted analyses A-D. For each required hostile question: concern → analysis performed → residual limitation.

**1. Could HERD simply proxy persistent national scientific capability?**
Analysis: added country-specific linear trends to the PPML — the level elasticity attenuated to 0.470 (95% CI -0.034 to 0.973, p=0.068) from 0.526. Long-difference model (2004-08 vs 2014-18) retained 0.473 (95% CI 0.313 to 0.633, p=1.4e-6); first-difference log-log is null (0.063, p=0.145).
Residual: the level estimate is a long-run association, not short-term causation; manuscript language recalibrated accordingly ("persistent resource environments are associated with realized output differences").

**2. Could the resource-intensity PCA still be conceptually contaminated?**
Analysis: primary index uses only upstream proxies (team size, institutional multiplicity, international collaboration, funder acknowledgement); publication-side attributes (English share, DOI, OA) excluded. Leave-one-component-out interactions 0.172-0.194, all p<0.05; full index (incl. visibility vars) 0.145, p=0.050; Spearman 0.958.
Residual: "resource intensity" still bundles team-science and money sensitivity; wording kept as resource intensity/sensitivity.

**3. Could researcher movement generate the observed low-resource resilience?**
Analysis: non-mover restriction and fixed-portfolio counterfactual on the 6-country author sample. Post-window low-intensity share falls from 14.1% (full) to 7.7% (stable-field authors) — ~45% attenuation; fixed-portfolio mean RI would stay at 1.06 vs realized 0.58.
Residual: reallocation is a genuine mediator concentrated in a mobile minority; the field-level interaction (+0.19) is a panel result unaffected by author-level composition within cells, but the two channels are linked — both reported. The sampled-author design cannot fully reconstruct country aggregates.

**4. Does weak short-run lag evidence undermine the resource interpretation?**
Analysis: distributed-lag, first-difference, and country-trend models all agree the response is not short-run; long-difference retains a strong association.
Residual: interpretation restricted to long-run resource environments; no claim that appropriations shocks change output.

**5. Does OpenAlex coverage change explain trends?**
Analysis: field x year FE absorbs global indexing/composition shifts; citation stages truncated at 2021; coverage-bias reference [10] added.
Residual: country-specific coverage drift cannot be fully excluded.

**6. Are high-impact outcomes more resource-sensitive merely because of collaboration/team size?**
Analysis: international collaboration share is a component of the intensity index — the funnel result (top-decile elasticity 1.065) is consistent with both collaboration burden and funding intensity. LOO dropping share_intl still gives interaction 0.194 (p=0.021).
Residual: the index cannot fully separate money from team science; stated as such.

**7. Is knowledge persistence too close to a ceiling measure?**
Analysis: added count-weighted similarity — cosine 0.92 mean (Japan 0.98), weighted Jaccard Japan highest in focus set (0.79). Presence measure is ceiling-prone; weighted metrics are not and point the same way.
Residual: weighted similarity still measures portfolio continuity, not ideas or creativity — language calibrated.

**8. Are OA/APC findings confounded by journal/publisher composition?**
Analysis: hybrid-share coefficient is null (-0.183, p=0.128); gold share positive (0.772, p=0.007). "APC-as-paywall" phrasing removed; hybrid journals permit non-OA publication — noted in text.
Residual: composition confounding not excluded; feasibility-level framing retained.

**9. Could reverse causality operate from output to funding?**
Analysis: lag-2 baseline plus lags 0-4 reported; identification relies on predetermination, not instruments.
Residual: cannot be excluded; acknowledged explicitly.

**10. Are country-specific institutional trajectories driving results?**
Analysis: country linear trends attenuate the level (0.470, p=0.068) but leave the interaction unchanged (0.190, p=0.025).
Residual: trajectory-driven level co-movement remains plausible; the heterogeneity gradient survives it.

## Final classification

B — ROBUST BUT MORE QUALIFIED. The falsification-relevant interaction is unchanged by every targeted correction; the level elasticity is reframed as a long-run association; mobility is reframed as a real mediator, not a bound that "cannot account".
