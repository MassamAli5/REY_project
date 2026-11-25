
# Progress Review: Grain-Type Variation and Prediction of REY Enrichment in Early Cambrian Phosphorites

**Dataset:** Kakul Garlaniyan phosphorites, northeastern Pakistan

**Reporting date:** November 17, 2026

## 1. Research Objective and Current Progress

This project examines the variation of total rare earth element and yttrium (REY) concentrations among phosphatic components in the Early Cambrian Kakul Garlaniyan phosphorites.

The primary geological question is whether oolites exhibit higher mean total REY concentrations than pellets when measurements are compared within the same inferred parent rocks.

The predictive question is whether petrographic grain type improves the estimation of total REY concentrations relative to a simple baseline and EPMA major-element chemistry.

The work completed so far includes data import and initial auditing, descriptive analysis, geochemical visualization, comparison of grain types within inferred parent-rock groups, and preliminary regression-model evaluation.

## 2. Dataset and Exploratory Data Analysis

The dataset was obtained from Supplementary Table S2 of Ali et al. (2026). It comprises 103 in-situ analytical measurements from the lower (LPL), middle (MPL), and upper (UPL) phosphorite layers.

The analyzed components comprise 35 oolite cores, 27 oolite rims, 20 pellet cores, and 21 pellet rims.

Total REY concentrations range from 222.77 to 922.74 ppm, with a mean of 587.87 ppm and standard deviation of 152.21 ppm.

Initial boxplots show overlapping REY distributions among the three phosphorite layers. Oolites exhibit higher mean total REY concentrations than pellets in each layer.

These differences are descriptive observations and cannot independently establish the processes responsible for REY enrichment.

The dataset includes repeated analytical measurements that may originate from the same parent rock. Consequently, individual measurements cannot automatically be treated as independent geological samples.

A complete predictor missingness and analytical-quality assessment remains to be documented.

## 3. Baseline and Prediction Methods

The prediction target is total REY concentration (ppm).

The candidate predictors include petrographic grain type and nine EPMA variables: F, Na2O, MgO, FeO, P2O5, CaO, MnO, Al2O3, and SiO2.

Four approaches were compared:

1. Training-set median baseline.
2. Grain-type-only Ridge regression.
3. EPMA major-element Ridge regression.
4. Combined EPMA and grain-type Ridge regression.

Ridge regression used a fixed regularization parameter of alpha = 10.0. This parameter was not independently optimized.

Missing predictor values were imputed using training-set medians. Numerical features were standardized, and categorical grain type was encoded.

Preprocessing was fitted inside the training portion of each evaluation fold.

Individual REY concentrations, REY-derived indicators, analytical identifiers, and inferred rock-group labels were excluded from the predictor set.

## 4. Evaluation Protocol

Five-fold GroupKFold cross-validation was used to estimate prediction errors.

Provisional parent-rock groups were inferred by combining stratigraphic-layer labels with the numerical prefixes of analytical-point identifiers.

The 103 records were assigned to 26 provisional rock groups. The script confirmed that no inferred group was shared between training and testing partitions.

The primary evaluation metric was rock-weighted mean absolute error (MAE), which gives equal weight to each inferred rock group.

Spot-weighted MAE and root mean squared error (RMSE) were also calculated.

The grouping procedure must be verified against original sample records before the resulting evaluation can be described as a confirmed independent-rock assessment.

## 5. Preliminary Results

### 5.1 Within-group REY differences

Thirteen inferred parent-rock groups contain both oolite and pellet measurements.

Of these groups, 12 exhibit higher mean total REY concentrations in oolites.

The equal-group mean oolite-minus-pellet difference is +179.37 ppm, and the median difference is +194.01 ppm.

An exploratory bootstrap using 10,000 group-level resamples and random seed 42 produced a percentile interval of +93.70 to +247.77 ppm.

One inferred group exhibits the opposite relationship, indicating that the observed enrichment pattern is not uniform.

The bootstrap interval depends on provisional grouping and sampling assumptions and is not evidence of geological causation.

### 5.2 Regression model comparison

**Table 1. Prediction errors from five-fold grouped cross-validation. All values are in ppm.**

| Model | Rock-weighted MAE | Spot MAE | RMSE |
|---|---:|---:|---:|
| Grain type only | 97.68 | 95.78 | 122.62 |
| EPMA + grain type | 100.78 | 102.40 | 131.31 |
| EPMA chemistry only | 123.70 | 129.08 | 163.60 |
| Median baseline | 124.79 | 126.86 | 157.51 |

The grain-type-only model produced the lowest rock-weighted prediction error.

Its MAE was approximately 21.7% lower than that of the median baseline.

The combined EPMA and grain-type model improved upon EPMA chemistry alone but did not outperform the grain-type-only model.

These results suggest that grain-type information is associated with variation in total REY concentrations within the present dataset.

They do not demonstrate the model's reliability at other geological localities.


## 6. Ablation, Learning Curve, and Remaining Evaluation

### 6.1 Feature-ablation comparison

The comparison between EPMA-only and combined EPMA-plus-grain-type models provides an initial assessment of the additional predictive information associated with grain type.

Removing grain type increased rock-weighted MAE from 100.78 to 123.70 ppm.

Adding the selected EPMA major-element measurements to the grain-type-only model did not improve prediction under the present modelling settings.

### 6.2 Learning-curve analysis

An exploratory learning-curve analysis was conducted using five-fold grouped cross-validation.

The training rock groups were subsampled at 25%, 50%, 75%, and 100% of the groups available within each training fold.

**Table 2. Mean held-out fold-level rock-weighted MAE at different training fractions (ppm).**

| Training fraction | Grain-type model | Median baseline |
|---|---:|---:|
| 25% | 110.75 | 129.80 |
| 50% | 102.62 | 125.14 |
| 75% | 98.97 | 123.34 |
| 100% | 96.58 | 123.51 |

![Learning-curve analysis](../results/figures/learning_curve.png)

*Figure 3. Mean held-out rock-weighted MAE for grain-type-only Ridge regression and the median baseline at different fractions of available training groups.*

The grain-type-only model showed decreasing mean prediction errors as the number of training groups increased. Its error was lower than the median baseline at every tested fraction.

The full-training learning-curve result differs slightly from the principal model comparison because the two scripts use different error-aggregation procedures. The principal model-comparison result of 97.68 ppm remains the primary reported estimate.

The learning-curve results are exploratory. Repeated subsamples are not independent experiments, and the provisional parent-rock grouping remains unverified.

### 6.3 Remaining evaluation

Further work should examine sensitivity to individual rock groups, the stability of model performance, and the validity of the inferred parent-rock identifiers.

These checks have not yet been completed.


## 7. Limitations and Risks

The principal limitation is the small number of inferred independent geological samples relative to the number of analytical measurements.

Parent-rock identifiers were reconstructed from supplementary analytical labels and require verification.

All measurements originate from one geological locality, limiting claims about predictive transfer.

The study is also sensitive to differences in grain-type representation, analytical variability, model settings, and the sampling of parent rocks.

The observed prediction patterns do not establish whether REY enrichment reflects depositional, early-diagenetic, or later geological processes.

The original published workbook should not be redistributed publicly until applicable data-use permissions have been confirmed.

## 8. Reproducibility and Next Work

The current VS Code project contains executable Python scripts for data auditing, exploratory figures, model comparison, and within-group REY analysis.

The Python environment has been recorded in requirements.txt and requirements-lock.txt.

Model predictions, numerical summaries, and graphical results are saved in the project's results directory.

Remaining priorities include verifying parent-rock identifiers, evaluating model sensitivity and learning-curve behavior, documenting the source-data permissions, and consolidating the final report.

AI assistance was used to draft Python code. The scripts were executed locally, and their numerical outputs were checked against saved results.

## Reference

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. Journal of Asian Earth Sciences, 298, 106927.

https://doi.org/10.1016/j.jseaes.2025.106927
