# Data QA / Coverage Audit (Phase 4)

Generated: 2026-09-29 12:44:20.003111+00:00


## Panel dimensions

- country x field x year rows: 39,613
- countries: 59 | fields: 26 | years: 2000–2025

## Country inclusion screen (frozen rules)

| country   |    works | iso3   |   gerd_years | include   |
|:----------|---------:|:-------|-------------:|:----------|
| us        | 21569161 | usa    |           28 | True      |
| cn        | 14884158 | chn    |           28 | True      |
| gb        |  6185356 | gbr    |           28 | True      |
| de        |  5411898 | deu    |           28 | True      |
| fr        |  5065926 | fra    |           28 | True      |
| jp        |  4767287 | jpn    |           28 | True      |
| in        |  4203511 | ind    |           25 | True      |
| br        |  3473798 | bra    |           24 | True      |
| id        |  3213460 | idn    |            9 | False     |
| it        |  3144847 | ita    |           28 | True      |
| ca        |  3094186 | can    |           29 | True      |
| es        |  2813226 | esp    |           28 | True      |
| au        |  2635307 | aus    |           14 | False     |
| ru        |  2621196 | rus    |           29 | True      |
| kr        |  2104801 | kor    |           28 | True      |
| nl        |  1740909 | nld    |           28 | True      |
| ir        |  1597779 | irn    |           15 | True      |
| tr        |  1577818 | tur    |           28 | True      |
| pl        |  1563417 | pol    |           28 | True      |
| ch        |  1355032 | che    |           10 | False     |
| se        |  1114425 | swe    |           24 | True      |
| be        |  1111501 | bel    |           28 | True      |
| tw        |  1012776 | twn    |            0 | False     |
| dk        |   923590 | dnk    |           28 | True      |
| ua        |   913511 | ukr    |           28 | True      |
| mx        |   862679 | mex    |           29 | True      |
| eg        |   774493 | egy    |           26 | True      |
| my        |   758322 | mys    |           17 | True      |
| at        |   746702 | aut    |           28 | True      |
| pt        |   737237 | prt    |           28 | True      |
| sa        |   684746 | sau    |           16 | True      |
| za        |   634503 | zaf    |           22 | True      |
| hk        |   628802 | hkg    |           27 | True      |
| il        |   620263 | isr    |           28 | True      |
| no        |   584309 | nor    |           25 | True      |
| fi        |   577574 | fin    |           28 | True      |
| gr        |   563775 | grc    |           24 | True      |
| sg        |   559158 | sgp    |           27 | True      |
| pk        |   558421 | pak    |           16 | True      |
| cz        |   535996 | cze    |           28 | True      |
| ar        |   505703 | arg    |           28 | True      |
| ng        |   463732 | nga    |            2 | False     |
| ie        |   423328 | irl    |           28 | True      |
| th        |   415395 | tha    |           25 | True      |
| nz        |   412601 | nzl    |           14 | False     |
| cl        |   405473 | chl    |           16 | True      |
| ro        |   402502 | rou    |           28 | True      |
| hu        |   362283 | hun    |           28 | True      |
| hr        |   216324 | hrv    |           25 | True      |
| sk        |   178199 | svk    |           28 | True      |
| si        |   165425 | svn    |           28 | True      |
| bg        |   156507 | bgr    |           28 | True      |
| lt        |   115374 | ltu    |           28 | True      |
| cy        |    87943 | cyp    |           26 | True      |
| ee        |    80552 | est    |           26 | True      |
| lu        |    78127 | lux    |           22 | True      |
| lv        |    59450 | lva    |           28 | True      |
| is        |    41248 | isl    |           24 | True      |
| mt        |    20064 | mlt    |           22 | False     |

Included: 52 / 59

## Funnel consistency

- rows violating Y-level nesting (y2>y1 or y3>y2 or y4>y2): 0
- zero-y2 rows (country-field-year with no articles): 51

## Citation maturity

- citation outcomes (y5 fwci>1, y6 top10%, y7 top1%) collected only for publication_year <= 2021; later years are censored.
|   year |          y2 |               y6 |   top10_share |
|-------:|------------:|-----------------:|--------------:|
|   2000 | 1.16053e+06 | 265728           |         0.229 |
|   2001 | 1.19983e+06 | 267755           |         0.223 |
|   2002 | 1.28912e+06 | 294344           |         0.228 |
|   2003 | 1.42277e+06 | 329931           |         0.232 |
|   2004 | 1.55314e+06 | 344005           |         0.221 |
|   2005 | 1.74366e+06 | 394831           |         0.226 |
|   2006 | 1.95456e+06 | 445336           |         0.228 |
|   2007 | 2.10978e+06 | 484278           |         0.23  |
|   2008 | 2.31958e+06 | 550695           |         0.237 |
|   2009 | 2.4498e+06  | 577328           |         0.236 |
|   2010 | 2.63938e+06 | 623369           |         0.236 |
|   2011 | 2.86399e+06 | 677963           |         0.237 |
|   2012 | 3.01141e+06 | 712731           |         0.237 |
|   2013 | 3.23869e+06 | 792528           |         0.245 |
|   2014 | 3.41469e+06 | 829268           |         0.243 |
|   2015 | 3.48354e+06 | 897238           |         0.258 |
|   2016 | 3.5631e+06  | 967131           |         0.271 |
|   2017 | 3.74852e+06 | 901532           |         0.241 |
|   2018 | 3.96814e+06 | 905452           |         0.228 |
|   2019 | 4.25937e+06 | 961381           |         0.226 |
|   2020 | 4.7762e+06  |      1.032e+06   |         0.216 |
|   2021 | 5.00913e+06 |      1.02585e+06 |         0.205 |
Expected ~0.10 share if percentile normalization holds across years; drift flags normalization issues.

## Resource series coverage

- h_usdppp: 808 obs, 0–31 years/country
- g_usdppp: 828 obs, 0–31 years/country
- g_pct_gdp: 828 obs, 0–31 years/country
- t_rs_fte: 709 obs, 0–30 years/country
- gb_xpd_rsdv_gd_zs: 1422 obs, 2–29 years/country
- sp_pop_scie_rd_p6: 1280 obs, 0–29 years/country

## Known limitations

- awards/funders not API-filterable; field funding intensity is sample-based
- author-ID disambiguation quality unknown until Phase 10 audit
- full vs fractional counting: primary is full counting; fractional sensitivity via author-share subsample
- 2025 rows may be affected by source-ingest lag; flagged in results