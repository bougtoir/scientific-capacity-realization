# Pseudonymization method

- Real OpenAlex author IDs are replaced by per-country sequential keys
  `<country>_aNNNNN` assigned after sorting the country-author ID list.
- The mapping is one-way for the public release: the private mapping file
  (`paper1prime/data/processed/_author_pseudo_map_PRIVATE.json`, salted, not
  published) is required to recover OpenAlex IDs. No salt or reversible hash
  is published.
- Keys are stable across `author_period_panel.csv.gz` and
  `transition_panel.csv.gz`, enabling author-level longitudinal linkage.
- Panels contain only derived yearly aggregates (shares, means, state labels).
  No names, ORCIDs, emails, affiliations, institutions, work titles, DOIs, or
  work-level histories are released.
