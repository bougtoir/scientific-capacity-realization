# When Scientific Output Falls: Distinguishing Scientific Capacity from Resource-Dependent Realization

**Manuscript type:** Original Paper

**Corresponding author:** Onishi Tatsuki — ORCID: 0000-0001-7261-9062; email: bougtoir@gmail.com

**Affiliation:** Data Science and AI Innovation Research Promotion Center, Shiga University, 1-1-1 Bamba, Hikone, Shiga 522-8522, Japan

## Abstract

National bibliometric decline is often read as declining scientific capacity, yet indicators record realized output, not latent capability. We distinguish the two on an international country-by-field-by-year panel (52 countries, 26 OpenAlex fields, 2004-2023) combining seven outcome strata spanning production, collaboration, dissemination, accessibility, and citation visibility with OECD and World Bank resource series. In Poisson pseudo-maximum-likelihood models with two-way fixed effects, the elasticity of article output with respect to higher-education R&D two years prior is 0.526 (95% CI 0.387-0.665). The association is significantly stronger in resource-intensive fields (interaction 0.190, p=0.023) and for high-visibility outcomes (1.065 for top-decile output). The heterogeneity pattern survives index-construction, trend, and mobility-restriction checks; the level estimate is best read as a long-run association, since short-run resource changes do not detectably move output. Declining visible scientific output therefore does not uniquely identify declining underlying scientific capacity; concurrent deterioration cannot be excluded.

**Keywords:** scientometrics; research funding; scientific capacity; bibliometrics; higher-education R&D; Japan

**Declarations**

- Funding: No funding was received for this work.
- Competing interests: The author declares no competing interests.
- Data availability: All data are derived from public sources (OpenAlex, OECD MSTI, World Bank); acquisition manifests, checksums, and retrieval timestamps are recorded in the acquisition ledger.
- Code availability: The analysis code and reproducibility materials will be made publicly available in a permanent repository upon publication.
- Author contribution: Single-author work; T.O. designed the study, acquired and analyzed data, and wrote the manuscript.

## 1. Introduction

National scientific output is routinely interpreted as if it measured scientific capacity directly (Sugimoto and Larivière 2018). When a country's internationally visible publication or citation indicators fall, the inference is usually immediate: the science system is losing what it can do. Japan is the canonical case — successive editions of the national Science and Technology Indicators document falling ranks in top-decile papers and have been widely read as evidence of eroding research capability (NISTEP 2023a). That interpretation embeds a strong assumption: that the conversion of capability into observable output is constant, or at least orthogonal to the resource environment (Stephan et al. 2017).

We formalize the alternative. Observed scientific output is the emission of a staged system (Fig. 1):

{{EQ:operational}}

where *C* denotes the latent capacity stock (people, knowledge, instruments, research lineages), *R* the resource environment, *T* the transition structure that converts capacity and resources into publishable production, and *V* the visibility environment that determines which production becomes internationally indexed output. Under this representation, a fall in *Y* is observationally consistent with at least three distinct generating processes: capacity loss (a smaller *C*), resource-dependent realization (a smaller effective *R* acting on the transitions), and visibility constraint (changes in *V*). The first reading is not wrong — it is simply not unique.

The distinction matters because the remedies differ. If capacity has degraded, rebuilding it is a generational project. If the binding margin is the resource-dependent conversion of capacity into output, the same latent capability can produce more measured science with changed funding allocation — a claim with precedent in the Japanese literature, where declining research time rather than declining researcher numbers accounts for much of the stagnation in paper counts (Aoki and Kimura 2018), and with the international evidence that research funding shapes publication performance (Auranen and Nieminen 2010; Jacob and Lefgren 2011). And if visibility is the binding margin, the indicator itself is part of the phenomenon.

Resource allocation now sits near the center of the science-of-science research agenda (Fortunato et al. 2018). This paper makes four contributions. First, it separates these accounts formally on an international country x field x year panel rather than on a single national time series. Second, it measures seven outcome strata spanning production, collaboration, dissemination, accessibility, and citation visibility — from all indexed works to top-percentile cited articles — and shows where resource constraints bind most strongly. These strata are conceptually distinct outcome dimensions rather than a strictly nested sequence, a distinction we make explicit. Third, it constructs a field-level resource-intensity index from the internal attributes of sampled publications (team size, institutional multiplicity, funding acknowledgements, collaboration structure) and tests whether resource effects are concentrated where the resource dependence is largest — a falsification-relevant signature that a pure capacity story does not produce. Fourth, it reports bounded sensitivity analyses on the two alternative channels that are hardest to rule out in bibliometric data: within-author reallocation across fields, and persistence of the subfield structure through output contraction.

Japan enters as an informative case — large, well-instrumented, and recently declining in visible output — but not as the sole object of study. 52 countries meet the frozen inclusion rules.

## 2. Data and measurement

### 2.1 Outcome strata

From the OpenAlex index (Priem et al. 2022) we extract, for each country-year and each of the 26 first-level fields, seven outcome strata — all defined on article-level or work-level counts rather than as a nested sequence: (Y1) all works; (Y2) journal articles; (Y3) articles with authors affiliated to institutions in more than one country; (Y4) English-language articles; (Y5) articles with field-normalized citation impact above the field average; (Y6) articles in the top decile of the citation-normalized distribution; (Y7) articles in the top percentile. Citation-dependent strata (Y5-Y7) are restricted to publication years through 2021 to allow citation maturation. Because the strata measure parallel attributes of the article population — collaboration, language, access, and citation position are properties of the same works, not sequential gates — we report each stratum on its own denominator rather than as a funnel conversion rate. Counting is full (non-fractional) attribution to the institutional country, consistent with international indicator practice (NISTEP 2023b); aggregate output trajectories themselves are documented to evolve slowly and differently across fields and countries (Bornmann and Mutz 2015). Japan's article output peaked in 2021 and in 2023 stood -12.8% below that peak — a pattern shared with the United States, Germany, and the United Kingdom in the same window, a fact that already suggests system-level rather than purely national drivers.

### 2.2 Resource environment

The primary resource measure is real higher-education R&D expenditure (HERD), in constant purchasing-power-parity US dollars, from the OECD Main Science and Technology Indicators; gross domestic expenditure on R&D (GERD) serves as fallback where HERD is unavailable, and World Bank series as robustness checks (OECD 2015). HERD is preferred because it isolates the academic resource envelope from business-sector R&D, which constitutes most of total national R&D in large economies; using total national R&D as a proxy for academic resources would misallocate the dominant share. Inclusion requires at least 15 years of resource coverage, yielding 52 countries.

### 2.3 Field resource intensity

Because funders and grants cannot be filtered directly in the OpenAlex API, the resource-intensity index is estimated from stratified random samples: 3,000 works per field (seeded, balanced across 2004-2023). The primary index deliberately uses only upstream resource proxies — mean author count, institutional multiplicity, international collaboration share, and funder-acknowledgement share — and excludes publication-side attributes (English-language share, DOI coverage, open-access status) that sit downstream in the visibility chain and would contaminate later visibility-stage comparisons. The first principal component of the upstream attributes explains 89.2% of common variance with approximately equal loadings and orders fields exactly as the physics-vs-humanities intuition requires (Larivière et al. 2006) — physics and astronomy highest, arts and humanities lowest. The index measures resource demands proxied by publication attributes — not monetary capital directly (Wang and Shapira 2011). An index that includes the publication-side attributes is retained only as a secondary robustness comparator (Spearman rank correlation 0.96 with the primary index), and leave-one-component-out variants are reported in the results.

## 3. Methods

The primary specification is a Poisson pseudo-maximum-likelihood (PPML) model with high-dimensional fixed effects:

{{EQ:main_model}}

with country x field fixed effects absorbing persistent heterogeneity in both capacity and field structure, field x year fixed effects absorbing global field-specific shocks (including field-specific citation inflation and indexing changes), and two-way demand for identification coming from within-country deviations in resource trajectories. Standard errors are clustered by country. PPML is preferred over log-linear OLS because output is a count with heteroskedastic multiplicative errors and zero mass in small country x field cells (Silva and Tenreyro 2006).

The identifying assumption deserves statement, not concealment: lagged HERD is treated as predetermined, but reverse causality (output success attracting funding) and confounding (a common shock moving both) cannot be fully excluded on these data; the interaction with field resource intensity, where the effect should be concentrated if the realization channel is operative, is the sharper test than the level coefficient alone. A directed acyclic graph disciplining which variables enter and which are mediators (and are therefore excluded from the conditioning set) is reported in the supplementary material; per the frozen analysis plan we do not control for variables on the causal path, including author counts and field composition.

The distributed-lag specification replaces the single lag with year-over-year changes at lags 0-8 to trace the timing of resource effects. Two pre-committed sensitivity analyses bound the hardest alternative explanations: (i) an author-mobility test that samples authors whose pre-window dominant field sits in the high-intensity tercile and measures how much of their post-window output migrates to low-intensity fields — the within-author version of the transition story; and (ii) a subfield-persistence measure comparing the share of subfields active in 2004-2008 that remain active in later windows, an output-flow-versus-lineage-stock contrast. The transformative-agreement mechanism for Japan is examined only at feasibility level: Japan's Springer Nature agreements expanded from a 10-university pilot in 2023 to 21 RUC universities plus the J-SPRINTA consortium in 2024 (Springer Nature 2024), but institution-level participation and agreement-year variation are too thin for identification, and we report this boundedly.

## 4. Results

### 4.1 Resource levels and realized output

The elasticity of article output with respect to HERD two years prior is 0.526 (95% CI 0.387 to 0.665, p=1.09e-13) across the full panel. The estimate is stable under alternate resource measures (per-capita, per-researcher, lags 0-4), alternate samples (excluding the US and China, 0.335 (95% CI 0.071 to 0.598, p=0.0127); OECD members only, 0.380 (95% CI 0.154 to 0.605, p=0.000965); excluding COVID years; pre-2020, 0.516 (95% CI 0.397 to 0.635, p=0)), and alternate outcomes (all works 0.538 (95% CI 0.383 to 0.693, p=9.61e-12); internationally collaborative articles 0.549 (95% CI 0.267 to 0.831, p=0.000133); English-language articles 0.543 (95% CI 0.416 to 0.671, p=0)). (Fig. 2)


### 4.2 Resource-intensity heterogeneity

If resources fund the conversion of capacity into output, the resource elasticity should be largest where resource dependence is largest. It is: the interaction between log-HERD and the field resource-intensity index is 0.190 (95% CI 0.026 to 0.353, p=0.0233), positive and significant. Leave-one-component-out indices replicate the interaction (coefficients 0.172 to 0.194, all p<0.05), the secondary index that includes publication-side attributes gives 0.145 (95% CI -0.000 to 0.290, p=0.05), and the interaction is unchanged when country-specific linear trends are added (0.190 (95% CI 0.024 to 0.356, p=0.0249)). This cross-field gradient is the paper's main falsification-relevant result — this cross-field heterogeneity is less readily explained by a uniform capacity-loss model alone. (Fig. 3)


### 4.3 Lag structure

Contemporaneous and lagged *changes* in resources do not predict output changes: the distributed-lag coefficients at lags 0-8 are individually and jointly small (cumulative estimate -0.021), and a first-difference log-log specification confirms the null short-run response (0.063 (95% CI -0.023 to 0.150, p=0.145)). The *level* association is sensitive to slow-moving confounding in the expected direction: adding country-specific linear trends attenuates it (0.470 (95% CI -0.034 to 0.973, p=0.0675)), while a long-difference specification (2004-2008 to 2014-2018 mean changes) retains a strong long-run association (0.473 (95% CI 0.313 to 0.633, p=1.44e-06)). Read together, the panel supports a long-run association between persistent resource environments and realized output differences; it does not establish that short-term funding changes causally move output. (Fig. 4)


### 4.4 Heterogeneity across outcome strata

Resource sensitivity is not uniform across the outcome strata. The elasticity rises from 0.538 (95% CI 0.383 to 0.693, p=9.61e-12) for all works to 0.549 (95% CI 0.267 to 0.831, p=0.000133) for internationally collaborative articles, 0.543 (95% CI 0.416 to 0.671, p=0) for English-language articles, 0.861 (95% CI 0.401 to 1.322, p=0.000248) for open-access output, and 1.065 (95% CI 0.479 to 1.650, p=0.000364) for top-decile output. The highest-visibility strata — internationally collaborative, English-language, open-access, and top-decile output, the outcomes national indicators track — are the most resource-sensitive strata measured. Resource-sensitive visibility outcomes may therefore amplify the apparent contraction in headline indicators; part of what indicators record as decline reflects differential visibility. (Fig. 5)


### 4.5 Knowledge persistence

The subfield-persistence measure compares the share of active subfields in 2004-2008 that remain active in later windows. Mean presence-based persistence is 95.4% (mean across countries, window 2014-2018); for Japan 98.5%. Because presence is a coarse measure we also compute count-weighted similarity of the subfield portfolio: cosine similarity averages 0.92 across countries (Japan 0.98) and the weighted-Jaccard overlap is highest for Japan in the focus set (0.79). Weighted similarity therefore moves in the same direction as presence: topic and field structure persisted more strongly than publication volume, consistent with a distinction between knowledge-lineage continuity and realized output — without implying preservation of creativity, ideas, or educational quality, none of which these data measure. (Fig. 6)


### 4.6 Mobility sensitivity

Authors whose pre-window dominant field was in the high-intensity tercile allocated 14.1% of their post-window output to low-intensity fields on average (Japan largest, 15.6%) (Sugimoto 2015). A non-mover restriction shows most of this reallocation is carried by authors who actually switch fields: among authors whose post-window dominant field remained in the baseline tercile, the low-intensity output share is only 7.7% — the reallocation measure attenuates by roughly 45% once movers are removed. The fixed-portfolio counterfactual quantifies the drift directly: assigning each post-window work to the author's baseline dominant field, the mean resource-intensity of post output would have remained at 1.06 instead of the realized 0.58 (in index standard deviations). Researcher reallocation toward less resource-intensive fields is therefore real, concentrated in a mobile minority, and is best read as a mediator of the resource-realization channel — resource constraints may affect both output within a field and the movement of researchers between fields — rather than an independent rival explanation; a full multistate analysis of researcher adaptation is beyond the scope of the present study (Azoulay et al. 2017). (Fig. 7)


### 4.7 Publication-access mechanism

Within the visibility stage, the publication-cost environment is itself resource-sensitive: the gold-OA share of output correlates positively with resources (0.772 (95% CI 0.226 to 1.319, p=0.00728)), while the hybrid share does not (-0.183 (95% CI -0.422 to 0.056, p=0.128)) (Piwowar et al. 2018). This is consistent with resource-dependent access to paid OA channels (Olejniczak and Wilson 2020; Zhang et al. 2022) — financial conditions being associated with dissemination choices — not with a mandatory paywall: hybrid journals generally permit non-OA publication without an APC. The Japan transformative-agreement expansion of 2023-2024 (Springer Nature 2024; Schares 2024) provides too little institution-level and temporal variation to identify a causal visibility effect within this panel; we report it as a feasibility-bound result and reserve a stronger quasi-experimental test for future work.

## 5. Discussion

### 5.1 Adjudication

Against the pre-registered decision rules: the resource-realization hypothesis is *supported, with qualifications* — the elasticity is a robust long-run association concentrated in resource-intensive fields and in the highest-visibility outcome strata, but it attenuates under country-specific trends and shows no short-run dynamic response, so we interpret it as persistent-resource association rather than short-term funding causation. The visibility-constraint hypothesis is *partially supported* — the stratum gradient and the OA-mix correlation are consistent, but the TA mechanism is underpowered. The capacity-loss hypothesis is *not refuted but is not uniquely identified by output decline* — persistent subfield structure is consistent with knowledge-lineage continuity and shows no structural collapse, and we cannot exclude concurrent deterioration. The conjunction of these results substantiates the central distinction: the findings are consistent with the proposition that declining scientific output does not uniquely identify declining latent scientific capacity.

### 5.2 Interpretation

The staged model changes what a bibliometric decline means. If conversion is resource-dependent and the binding margin is downstream of capacity, then indicator trajectories measure realized science more directly than potential science. For Japan, where university research time has been squeezed by structural changes in funding allocation (Aoki and Kimura 2018; Yonetani et al. 2013), the results are consistent with a realization constraint operating alongside persistent knowledge-lineage structure — this does not show that latent capacity is preserved, but the decline-in-output → decline-in-capacity inference is not forced.

A second mechanism operates alongside the first: resource constraints may affect not only output within a field but also the movement of researchers between fields. The mobility sensitivity results show the reallocation is real but concentrated in a mobile minority of authors. Resource allocation therefore changes the composition of a science system as well as its productivity, and field-level resource contrasts partly reflect this adaptive movement rather than pure within-field realization.

A third distinction separates structure from volume. The weighted persistence metrics show that topic-portfolio continuity — the persistence of scientific thematic structure — can outlast changes in realized publication volume. We interpret persistent knowledge-lineage structure as evidence of continuity in what a system works on, not as direct measurement of preserved latent capacity; the two are related but not interchangeable constructs.

The policy reading follows the same logic: if the binding constraint sits in the resource-dependent conversion of capacity into visible output, intervention should target the limiting resource or transition rather than assuming that endpoint decline identifies the deficient upstream component. Output-based diagnosis alone cannot say which stock or transition is binding.

### 5.3 Limitations

Lagged resources may still proxy unobserved capacity trends, and the level estimate indeed attenuates under country-specific trends; the design does not exploit quasi-experimental resource shocks (a role for future author-level work), so causal language is inappropriate for the level association. Field resource intensity is estimated on samples and inherits sampling error, though leave-one-component-out indices replicate the interaction. The mobility analysis covers six countries, one fixed window, and a sampled-author design; its non-mover and fixed-portfolio results bound rather than settle the mediation question. Persistence metrics index portfolio continuity, not creativity or ideas. The visibility stage is the least identified component: APC expenditure at work level is sparse in OpenAlex, and TA variation is thin. Citation outcomes are cut at 2021 for maturation, so recent declines in the highest-visibility strata cannot be measured yet. Finally, database coverage, while broad in OpenAlex, is not neutral across languages and fields (Culbert et al. 2025; Mongeon and Paul-Hus 2016).

## 6. Conclusion

Scientific capacity is a stock; scientific output is a resource-dependent flow. This paper separated the two on an international panel and found a long-run resource association concentrated where a resource-dependent system predicts — in resource-intensive fields and in the high-visibility outcome strata national indicators track. Declining national output is informative, but it does not uniquely identify declining underlying capacity: a measurable resource-dependent realization stage intervenes between what a science system can do and what its indicators show, and a substantial component of cross-national and cross-field variation is consistent with differences in resource-dependent realization. Whether that stage fully accounts for the decline — and whether latent capacity is preserved — cannot be established here.

## Data availability

All inputs are public: OpenAlex API extracts (acquisition manifests, checksums, and retrieval timestamps in the acquisition ledger), OECD Main Science and Technology Indicators, and World Bank World Development Indicators.

## Code availability

The analysis code and reproducibility materials will be made publicly available in a permanent repository upon publication.

## Funding

None declared.

## Competing interests

None declared.
## References

Aoki R, Kimura H (2018) Allocation of research resources and publication productivity in Japan: a growth accounting approach. Public Policy Review 13(4):1-34
Auranen O, Nieminen M (2010) University research funding and publication performance: an international comparison. Research Policy 39(6):822-834. https://doi.org/10.1016/j.respol.2010.03.003
Bornmann L, Mutz R (2015) Growth rates of modern science: a bibliometric analysis based on the number of publications and cited references. Journal of the Association for Information Science and Technology 66(11):2215-2222. https://doi.org/10.1002/asi.23329
Azoulay P, Ganguli I, Graff Zivin J (2017) The mobility of elite life scientists: professional and personal determinants. Research Policy 46(3):573-590. https://doi.org/10.1016/j.respol.2017.01.002
Culbert J, Hobert A, Jahn N, et al. (2025) Reference coverage analysis of OpenAlex compared to Web of Science and Scopus. Quantitative Science Studies 6(1):152-173
Fortunato S, Bergstrom CT, Börner K, et al. (2018) Science of science. Science 359(6379):eaao0185. https://doi.org/10.1126/science.aao0185
Jacob BA, Lefgren L (2011) The impact of research grant funding on scientific productivity. Journal of Public Economics 95(9-10):1168-1177. https://doi.org/10.1016/j.jpubeco.2011.05.005
Larivière V, Gingras Y, Archambault E (2006) Canadian collaboration networks: a comparative analysis of the natural sciences, social sciences and humanities. Scientometrics 68(3):519-533. https://doi.org/10.1007/s11192-006-0127-8
NISTEP (2023a) Science and Technology Indicators 2023 (NISTEP-RM328). National Institute of Science and Technology Policy, Japan
Mongeon P, Paul-Hus A (2016) The journal coverage of Web of Science and Scopus: a comparative analysis. Scientometrics 106(1):213-228. https://doi.org/10.1007/s11192-015-1765-5
NISTEP (2023b) Science and Technology Indicators - counting methodology notes. National Institute of Science and Technology Policy, Japan
OECD (2015) Frascati Manual 2015: Guidelines for Collecting and Reporting Data on Research and Experimental Development. OECD Publishing, Paris; and OECD Main Science and Technology Indicators database (accessed 2026)
Olejniczak AJ, Wilson MJ (2020) Who's writing open access (OA) articles? Characteristics of OA authors. Quantitative Science Studies 1(4):1429-1450
Piwowar H, Priem J, Larivière V, et al. (2018) The state of OA: a large-scale analysis of the prevalence and impact of open access articles. PeerJ 6:e4375. https://doi.org/10.7717/peerj.4375
Priem J, Piwowar H, Orr R (2022) OpenAlex: a fully-open index of scholarly works. Quantitative Science Studies 3(4):795-818
Schares E (2024) Transformative agreements, publication venues and open access policies at the University of California. Learned Publishing 37(4):e1627. https://doi.org/10.1002/leap.1627
Silva JMCS, Tenreyro S (2006) The log of gravity. Review of Economics and Statistics 88(4):641-658
Springer Nature (2024) Springer Nature expands Transformative Agreements with Japanese universities. Press release, 22 Jan 2024
Stephan P, Veugelers R, Wang J (2017) Reviewers are blinkered by bibliometrics. Nature 544(7651):411-412. https://doi.org/10.1038/544411a
Sugimoto CR (2015) What do we know of the mobility of research scientists and impact on scientific production. In: Fernández-Zubieta A, Geuna A, Lawson C (eds) Global Mobility of Research Scientists: The Economics of Who Goes Where and Why. Academic Press, London, pp 33-52. https://doi.org/10.1016/B978-0-12-801396-0.00001-6
Sugimoto CR, Larivière V (2018) Measuring Research: What Everyone Needs to Know. Oxford University Press, Oxford. https://doi.org/10.1093/wentk/9780190640118.001.0001
Wang J, Shapira P (2011) Funding acknowledgement analysis: an enhanced tool to investigate research sponsorship impacts. Scientometrics 87(3):563-586. https://doi.org/10.1007/s11192-011-0362-5
Yonetani Y, Ikeuchi K, Kuwahara T (2013) An analysis on the relationship between input and output in the production of articles in universities — an approach using Web of Science and Survey of R&D (in Japanese). NISTEP Discussion Paper 89. National Institute of Science and Technology Policy, Tokyo
Zhang X, Wei F, Huang Y, Sivertsen G (2022) Should open access lead to closed research? The trends towards paying to perform research. Scientometrics 127(12):7653-7679. https://doi.org/10.1007/s11192-022-04407-5

## Figure captions

Fig. 1 Conceptual model. Observable scientific output Y is the realized emission of latent capacity C through resource-dependent transitions T and a visibility environment V.
Fig. 2 Real higher-education R&D expenditure (lagged two years) versus article output across the country-by-field panel; PPML elasticity estimate with clustered standard errors.
Fig. 3 Field resource-intensity index (first principal component of sampled work attributes) across the 26 OpenAlex first-level fields.
Fig. 4 Distributed-lag coefficients (lags 0-8) of year-over-year resource changes on article output, with 95% confidence intervals.
Fig. 5 Outcome-strata composition by country: articles share of all works and English-language share of articles, each stratum on its own denominator.
Fig. 6 Subfield persistence: share of subfields active in 2004-2008 remaining active in later windows, by country.
Fig. 7 Within-author field reallocation: post-window output share migrating from high- to low-resource-intensity fields.
