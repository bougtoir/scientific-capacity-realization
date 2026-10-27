# Author-level public release plan

## Class A — released (safe, derived)
- Pseudonymized author-period panel (yearly aggregates; shares/means/state)
- Pseudonymized transition panel (state->state with aggregates)
- Cohort funnel counts; state definitions; SHA256 manifest; reproduction scripts
## Class B — not released (derivable only after transformation)
- Raw work-level histories (author_works_*.parquet): would reconstruct
  identifiable bibliographies under persistent OpenAlex IDs.
- Author<->key mapping file (private, salted).
## Class C — never released
- Author names/ORCIDs/emails/affiliations, internal paths, session URLs, notes.
## Privacy rationale
Yearly share aggregates at the author level are not directly identifying; a
deterministic non-published mapping prevents ID lookup. Residual
re-identification via unusual aggregate patterns is mitigated by releasing
no work IDs, titles, venues, or DOIs.
