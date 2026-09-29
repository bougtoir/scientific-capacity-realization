# Data Feasibility (Phase 1)

Verified live on 2026-09-29 against production endpoints.

## 1. OpenAlex (api.openalex.org, polite pool via mailto)

Schema audit on live `/works` records confirmed:

- `primary_topic.field.id` / `subfield` / `domain` — 26 fields, 252 subfields. `group_by=primary_topic.field.id` returns all 26 groups (must set per-page=200; group results are capped by per-page).
- Filters verified working: `institutions.country_code:XX`, `publication_year`, `type:article`, `countries_distinct_count:>1`, `citation_normalized_percentile.is_in_top_10_percent|is_in_top_1_percent`, `language:en`, `open_access.is_oa`, `open_access.oa_status`, `locations.source.is_in_doaj`, `authors_count:>N`, `fwci:>1`, `has_doi`, `apc_list.currency`, `corresponding_author_ids`/`corresponding_institution_ids` (record-level, not filterable by country).
- Group_bys verified: `primary_topic.field.id`, `open_access.oa_status`, `type`, `language`, `publication_year`.
- `awards`/`funders` present on work records but **not filterable** (`has_award`, `has_funder`, `grants.funder` all invalid). → Field-level funding intensity must be estimated from **random samples of works per field** (`sample=` param + `select=`), not API aggregates. Coverage of awards is partial (sample test showed 0/5 awards in physics 2020) — record as a limitation; award-share is one component among several, not the whole intensity score.
- `apc_list`/`apc_paid` exist on records but are sparse → publication-access analysis uses **source-level** APC/OA attributes (`locations.source.is_in_doaj`, `open_access.oa_status`, source `apc` data on `/sources`) rather than per-work paid APC.
- Right-censoring: `citation_normalized_percentile` is field+year normalized by OpenAlex but recent vintages are immature → restrict citation outcomes to ≤2023/2022 as decided at freeze; keep 2024+ descriptive only.
- Estimated call volume for country×field×year funnel: ~45 countries × 26 years × ~7 variants ≈ 8k requests — feasible within polite-pool limits.

## 2. National R&D resource data

- **World Bank API**: verified for JPN/KOR/DEU 2000–2024 — `GB.XPD.RSDV.GD.ZS` (GERD %GDP), `SP.POP.SCIE.RD.P6` (researchers/million), `NY.GDP.MKTP.PP.KD` (real GDP PPP), `SP.POP.TOTL`. Near-complete.
- **OECD SDMX**: dataflow `DSD_MSTI@DF_MSTI` (Main Science and Technology Indicators) live at sdmx.oecd.org — provides HERD, GERD by sector, GBARD (`DSD_RDS_GOV@DF_GBARD_NABS07`), R&D personnel (`DSD_RDS_PERS@…`) with sector breakdowns. Key structure to be resolved at acquisition (standard SDMX key+filter syntax verified reachable).
- HERD (higher-education R&D) is the preferred *construct* for academic resource environment vs GERD (includes business R&D); hierarchy defined in ANALYSIS_PLAN.
- UNESCO UIS available as fallback for non-OECD coverage gaps.

## 3. Publication access / OA / APC

- OpenAlex `oa_status` mix per country×year — verified.
- Source-level DOAJ flag verified; `/sources` endpoint carries `apc_prices`/`apc_usd` where reported.
- OpenAPC dataset (github.com/OpenAPC) legally accessible — optional enrichment.

## 4. Transformative agreements

- **Japan**: Springer Nature press release (2024-01-22) documents expansion from 10-institution 2023 pilot to 21 RUC universities in 2024 + new J-SPRINTA model (13 institutions). Official participating-institution lists published on springernature.com OA-agreements pages. → A compact institution×year eligible-vs-noneligible journal-strata check is *feasible* for 2023→2024 adoption; limited window = underpowered for full causal claims → bounded mechanism analysis only, per prompt.
- **International**: ESAC registry (esac-initiative.org) catalogs agreements — multi-country TA design deferred to Paper 2 as required.

## 5. Country inclusion feasibility

Pre-screened availability: OECD members + major research economies have MSTI+WB coverage. Final inclusion rules at Phase 2 freeze: OpenAlex article volume ≥ threshold, GERD/researcher series ≥ ~15 of 26 years, stable country code.

## 6. Journal landscape (preliminary — full gate at Phase 15)

Candidates: *Journal of Informetrics*, *Quantitative Science Studies* (OA, no author APC — platinum), *Scientometrics*, *Research Evaluation*, *Science and Public Policy*, *Research Policy*. Scope fit strongest for JOI/QSS/Scientometrics; Research Policy needs policy-allocation framing. APC-free routes exist for all (hybrid subscription w/o OA, or QSS platinum).

## Feasibility verdict

All required measurement layers are obtainable reproducibly. Known constraints: awards/funding data partial (sampled, not aggregate); per-work APC sparse (use source-level); recent citation years immature (windowed); 2026 excluded.
