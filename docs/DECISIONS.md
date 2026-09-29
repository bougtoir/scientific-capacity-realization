# Decisions Log

Project initialized: 2026-09-29 (UTC). Random seed convention: `20260929`.
No-fabrication rule: every reported estimate must trace to pipeline output under `output/` built from persisted raw data under `data/raw/` (ledger: `data/raw/ACQUISITION_LEDGER.csv`).

| Date (UTC) | Phase | Decision | Rationale / class |
|---|---|---|---|
| 2026-09-29 | 0 | Canonical tree created under `wip/scientific_capacity_realization/` | per prompt, single working tree |
| 2026-09-29 | 3 | OpenAlex shared-IP daily budget exhausted mid-pull after jp/kr/gb/de (+fr partial); user chose no-API-key path: deferred resumable fetch waits for UTC-midnight reset and resumes slowly; error responses purged from raw store, manifest rebuilt | data-necessity |
| 2026-09-29 | 3 | resource measure hierarchy implemented: HERD real USD_PPP/V primary with GERD fallback per country-year | per frozen plan |
| 2026-09-29 | 4 | fr country-year bundle written partially before budget loss; incomplete cells re-fetched at resume | data-necessity |

## 2026-09-29 Phase 3 acquisition notes

- OpenAlex shared-IP daily budget exhausted mid-acquisition (429). User elected deferred no-key resume; subsequently found pre-provisioned `OPENALEX_API_KEY` secret works — all fetches now run with the key. Recorded in ledger notes.
- `has_doi` is not a valid `select` field (API returns "Invalid query parameters"); replaced with `doi` and derive has_doi as non-null.
- Awards/funders are not filterable in the Works endpoint (`has_award`, `grants.funder`, `awards_count` rejected) → field funding intensity is estimated from seeded random samples (N_PER_FIELD=3000 stratified over 2004-2023), not population aggregates.
- Funnel bundles that were written while the API returned errors were purged and the manifest rebuilt (957 good keys retained).

| 2026-09-29 | 15 | Journal target changed QSS → Scientometrics (user instruction). `scripts/build_scientometrics.py` emits journal package under `manuscript/scientometrics/`: author-year (Springer Basic) citations verified against Springer guidance; ≤250-word unstructured abstract; figures as separate Figure1-7 files (PNG+PDF) cited in-text; Springer declarations block | journal-specific |
