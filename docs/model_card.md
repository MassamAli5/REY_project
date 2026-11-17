
# Model Card: Prediction of Total REY Concentrations in Early Cambrian Phosphorites

## 1. Model Overview

**Project:** Grain-Type Variation and Prediction of REY Enrichment in Early Cambrian Phosphorites

**Team:** T06 — Massam Ali and Hussain Rabani

**Model type:** Ridge regression

**Prediction target:** Total rare earth element and yttrium (REY) concentration, expressed in ppm.

**Dataset:** Published in-situ geochemical measurements from the Kakul Garlaniyan phosphorites, northeastern Pakistan (Ali et al., 2026).

**Status:** Exploratory model comparison; no final model has been selected or deployed.

## 2. Research Purpose

The predictive analysis investigates whether petrographic grain type provides useful information for estimating total REY concentrations in the studied phosphorites.

The central question is whether models using grain type perform better than a simple baseline and whether major-element chemistry improves prediction.

The models are intended to evaluate statistical associations within the available dataset, not to establish the geological mechanisms responsible for REY enrichment.

## 3. Dataset and Observation Units

The dataset contains 103 in-situ analytical measurements from three phosphorite layers: LPL, MPL, and UPL.

The analytical measurements include oolite cores, oolite rims, pellet cores, and pellet rims.

For the predictive comparison, the four original categories were reduced to two grain types:

- Oolite
- Pellet

Each record represents an analytical spot rather than necessarily an independent geological rock sample.

Using stratigraphic labels and analytical-point prefixes, 26 provisional parent-rock groups were inferred. These group identities require verification against original sample records.

## 4. Input Features

The following feature combinations were evaluated.

### Grain-type-only model

Uses the categorical variable:

- Grain type: oolite or pellet

### EPMA chemistry model

Uses nine numerical predictors:

- F
- Na2O
- MgO
- FeO
- P2O5
- CaO
- MnO
- Al2O3
- SiO2

### Combined model

Uses both grain type and the nine EPMA measurements.

### Excluded variables

Individual REY element concentrations, total REY, and REY-derived indices were excluded from predictors to prevent target leakage.

Analytical-point identifiers and inferred rock-group labels were used for data grouping but were not model predictors.

## 5. Baseline and Model Architecture

Four approaches were compared:

1. Training-set median baseline
2. Grain-type-only Ridge regression
3. EPMA-only Ridge regression
4. Combined EPMA and grain-type Ridge regression

The median baseline predicts the median total REY concentration of the training data.

All Ridge regression models used a fixed regularization parameter:

alpha = 10.0

The parameter was selected for exploratory evaluation and was not independently optimized through nested cross-validation.

No trained production model was saved. The scripts fit models within evaluation folds and save their predictions and performance metrics.

## 6. Data Preprocessing

Numerical predictor values were processed using:

1. Median imputation for missing values.
2. StandardScaler for feature standardization.

Categorical grain-type labels were processed using OneHotEncoder.

Preprocessing was included within scikit-learn pipelines and fitted using training-fold data only.

The original workbook was not modified by these transformations.

## 7. Evaluation Strategy

Five-fold GroupKFold cross-validation was used.

The groups were constructed from the stratigraphic-layer labels and numerical prefixes of analytical-point identifiers.

The implementation checked that no inferred rock group appeared simultaneously in the training and testing partitions.

However, this check does not independently establish that the inferred identifiers represent the true geological parent rocks.

### Primary metric

Rock-weighted mean absolute error (MAE), expressed in ppm.

For each inferred rock group, the mean absolute prediction error was calculated. The overall metric gives equal weight to each inferred group.

### Secondary metrics

- Spot-weighted mean absolute error (MAE)
- Root mean squared error (RMSE)

Lower values indicate smaller prediction errors.

## 8. Model Performance

**Table 1. Prediction errors from five-fold grouped cross-validation. All values are in ppm.**

| Model | Rock-weighted MAE | Spot MAE | RMSE |
|---|---:|---:|---:|
| Grain type only | 97.68 | 95.78 | 122.62 |
| EPMA + grain type | 100.78 | 102.40 | 131.31 |
| EPMA chemistry only | 123.70 | 129.08 | 163.60 |
| Median baseline | 124.79 | 126.86 | 157.51 |

The grain-type-only Ridge regression model achieved the lowest rock-weighted MAE among the four evaluated approaches.

Relative to the median baseline, its rock-weighted MAE was approximately 21.7% lower.

Including grain type improved performance relative to EPMA chemistry alone. However, the combined model did not outperform the grain-type-only model.

The EPMA-only model offered little improvement over the median baseline under the present model settings.

These findings are exploratory results for the studied dataset, not independent confirmation of model generalization.

## 9. Learning-Curve Evaluation

An exploratory learning-curve analysis compared the grain-type-only model with the median baseline.

Training groups were subsampled at 25%, 50%, 75%, and 100% of the groups available within each training fold.

**Table 2. Mean held-out fold-level rock-weighted MAE (ppm).**

| Training fraction | Grain-type-only model | Median baseline |
|---|---:|---:|
| 25% | 110.75 | 129.80 |
| 50% | 102.62 | 125.14 |
| 75% | 98.97 | 123.34 |
| 100% | 96.58 | 123.51 |

The grain-type-only model showed lower average prediction error as the proportion of training groups increased.

The full-training result of 96.58 ppm differs slightly from the primary model-comparison result of 97.68 ppm because the learning-curve script averages fold-level errors, whereas the principal comparison gives equal weight to each inferred rock across the combined held-out predictions.

The main model-comparison value of 97.68 ppm remains the primary reported result.

Repeated subsamples and folds are not independent experiments. This learning curve does not establish performance on external geological datasets.

## 10. Intended Uses

These models are intended for:

- Exploratory investigation of REY concentration variation.
- Comparing the predictive contributions of grain type and EPMA chemistry.
- Evaluating grouped cross-validation procedures for geological measurements.
- Identifying methodological limitations and possible directions for further research.

## 11. Limitations and Inappropriate Uses

The principal limitations are:

1. The dataset contains only 103 analytical spots and a limited number of inferred independent rock groups.
2. Parent-rock identities have not been verified against original records.
3. The analysis represents a single geological locality.
4. Model regularization was fixed without nested hyperparameter optimization.
5. Prediction uncertainty and sensitivity to alternative grouping assumptions have not been fully investigated.
6. Model selection and interpretation were informed by earlier exploratory examination of the same dataset.
7. The models have not been independently validated on another phosphorite deposit.

The models should not be used to determine seawater redox conditions, identify REY sources, infer the timing of phosphate mineral formation, or establish a geological enrichment mechanism.

Prediction accuracy and statistical association do not demonstrate causation.

The models are not validated for mineral-resource estimation or operational prediction outside the studied dataset.

## 12. Reproducibility

The model comparison is implemented in:

`scripts/03_model_comparison.py`

The learning-curve evaluation is implemented in:

`scripts/05_learning_curve.py`

Saved evaluation outputs include:

- `results/metrics/grouped_predictions.csv`
- `results/metrics/model_comparison.csv`
- `results/metrics/learning_curve_raw.csv`
- `results/metrics/learning_curve_summary.csv`
- `results/figures/learning_curve.png`

The Python environment is documented in `requirements.txt` and `requirements-lock.txt`.

Instructions for running the scripts are provided in the project README.

The original dataset is not included in the public repository unless applicable redistribution and reuse permissions are confirmed.

## 13. Model Status and Next Verification

The current models are experimental and have not been deployed.

Before stronger conclusions can be considered, the following checks remain necessary:

- Verify the parent-rock identifiers against original sample records.
- Assess sensitivity to individual rock groups and alternative model settings.
- Investigate uncertainty in the predictive comparisons.
- Evaluate transfer to independent geological samples if suitable data become available.

These are outstanding verification tasks, not completed experimental results.

## Reference

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. *Journal of Asian Earth Sciences*, 298, 106927.

https://doi.org/10.1016/j.jseaes.2025.106927
