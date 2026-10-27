# public_micro — pseudonymized author-level reproduction layer

Reproduces the researcher-level (micro) analyses of the manuscript from
derived, pseudonymized panels only. No identifiable author histories.

## Run (from repository root)
    python public_micro/scripts/models_transitions.py
    python public_micro/scripts/pub_behavior.py
    python public_micro/scripts/decomposition_modelcountries.py

Outputs land in public_micro/output/tables/ and match the canonical tables
(transition matrix, MNLogit destinations, Markov memory test, within-author
models, publication behavior, decomposition, country transition shares,
model-country profiles). Mobility sensitivity is reproduced at repo level by
scripts/mobility_sensitivity2.py against data/raw/openalex_mobility.

Requires: pandas, numpy, statsmodels, scipy.
