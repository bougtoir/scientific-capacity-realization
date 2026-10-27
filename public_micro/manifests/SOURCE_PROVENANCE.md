# Source provenance

- Derived from an OpenAlex author-work cohort: 2,500 author IDs per focus
  country stratified over 26 fields on 2008-2011 works (seed 11); full
  2004-2023 work histories; eligibility >=3 works + >=2 active baseline years
  -> 12,361 authors, 196,937 author-year portfolio rows (222,498 windows incl.
  S5), 210,137 year-consecutive transitions.
- OpenAlex is a living index: records change over time. This released layer is
  pinned to the retained acquisition snapshot recorded in
  data/raw/ACQUISITION_LEDGER.csv (repo root). Do NOT re-fetch OpenAlex and
  expect identical author histories; historical identity is not guaranteed.
- Macro inputs (resources_country_year, panel_country_year, topic_persistence,
  field_resource_intensity) are in the repository-level data/processed/.
