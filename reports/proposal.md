# Rock-Scale and Grain-Type Variation in REY Enrichment in Early Cambrian Phosphorites

Research Proposal

**Team T06:** Massam Ali and Hussain Rabani

**Date:** November 17, 2026

## 1. Research Problem and Motivation

Sedimentary phosphorites contain rare earth elements and yttrium (REY), which are widely investigated to understand phosphate mineral formation and marine geochemical conditions. However, REY concentrations can vary among phosphatic components, and their distributions may reflect several geological processes rather than a single enrichment mechanism.

Ali et al. (2026) reported differences in REY concentrations between phosphatic grains in the Early Cambrian Kakul Garlaniyan phosphorites of northeastern Pakistan. This provides an opportunity to examine whether these differences remain consistent when analytical measurements are compared within individual parent rocks.

Our primary research question is: **Do oolites consistently exhibit higher total REY concentrations than pellets within the same parent rocks?**

A related data science question is whether petrographic grain type improves the prediction of total REY concentration beyond models using major-element chemistry alone.

## 2. Related Research

Ali et al. (2026) investigated phosphogenesis at Kakul Garlaniyan using petrographic and geochemical evidence, including in-situ REY measurements. Lumiste et al. (2019) demonstrated the importance of REY uptake and diagenetic modification in sedimentary apatite. Tahar-Belkacem et al. (2024) applied machine-learning approaches to predict REE concentrations in Tethyan phosphorites using major-element chemistry.

These studies establish that grain-scale REY variability and machine-learning prediction are existing research topics. Our project does not claim to introduce either concept. Instead, it evaluates grain-type differences while accounting for the grouping of analytical measurements by parent rock and examines whether grain type provides additional predictive information in this dataset.

## 3. Dataset and Preliminary Observations

The dataset comes from Supplementary Table S2 of Ali et al. (2026). It contains **103 in-situ analytical measurements** from three phosphorite layers: lower (LPL), middle (MPL), and upper (UPL).

The measurements comprise 35 oolite cores, 27 oolite rims, 20 pellet cores, and 21 pellet rims. Available variables include petrographic component labels, analytical identifiers, major-element compositions, and REY concentrations.

Our initial descriptive analysis gives total REY concentrations of 222.77–922.74 ppm, averaging 587.87 ppm. Oolites have higher mean total REY concentrations than pellets in each phosphorite layer. These observations are consistent with the published data but do not establish statistical significance or geological causation.

The analytical identifiers suggest approximately 26 parent-rock groups; this grouping remains provisional until checked against the original sample records.

## 4. Research Hypotheses and Methods

**H1 — Grain-type differences:** Mean total REY concentrations are higher in oolites than pellets within parent rocks containing both components.


**H2 — Predictive information:** Adding petrographic grain type to major-element measurements may improve prediction of total REY in held-out parent rocks. No improvement is also a valid outcome.The analysis will first compare mean concentrations of oolites and pellets within each eligible parent rock. Independent parent rocks, rather than individual analytical spots, will be the units used to summarize these differences.

For prediction, we plan to compare a training-set median baseline, a grain-type-only model, a major-element Ridge regression model, and a combined Ridge regression model.

Five-fold group-aware cross-validation will be used, subject to verification of the parent-rock identifiers. Measurements assigned to one parent rock will not be divided between training and testing folds. Data preprocessing will be fitted using training data only.

Individual REY concentrations and REY-derived indices will be excluded from predictors of total REY to prevent target leakage.

## 5. Evaluation and Success Criteria

The primary predictive metric will be parent-rock-weighted mean absolute error (MAE, ppm). Spot-weighted MAE and root mean squared error (RMSE) will provide supplementary comparisons.

A practical benchmark is a 10% reduction in rock-weighted MAE relative to the median baseline. This is a post-exploratory benchmark, not a preregistered significance threshold.

A useful outcome is a reproducible comparison that establishes whether the additional variables improve prediction, even if the improvement is absent or uncertain.

## 6. Ethics, Limitations, and Responsibilities

The project uses published geological measurements and does not involve human participants. Permission to redistribute the underlying workbook or use it for machine-learning purposes must be checked before public sharing. The original data will remain outside the public repository unless reuse rights are confirmed.

The main limitations are the small number of independent rocks, potentially correlated measurements, uncertain parent-rock identifiers, and restriction to one locality. Statistical associations or model performance cannot independently establish the processes responsible for REY enrichment.

Proposed responsibilities, subject to team confirmation, are: Massam Ali—geological interpretation, dataset review, and scientific writing; Hussain Rabani—computational implementation and model evaluation. Both members will review the results, verify their contributions, and document any AI assistance.

## References

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. *Journal of Asian Earth Sciences*, 298, 106927. https://doi.org/10.1016/j.jseaes.2025.106927

Lumiste, K., et al. (2019). REE+Y uptake and diagenesis in Recent sedimentary apatites. *Chemical Geology*, 525, 268–281. https://doi.org/10.1016/j.chemgeo.2019.07.034

Tahar-Belkacem, N., et al. (2024). Machine learning models to predict rare earth elements distribution in Tethyan phosphate ore deposits: Geochemical and depositional environment implications. *Geochemistry*, 84, 126128. https://doi.org/10.1016/j.chemer.2024.126128