
# Preliminary Model Comparison

## Research objective

The predictive analysis examines whether petrographic grain type and major-element chemistry provide useful information for estimating total rare earth element and yttrium (REY) concentrations in the Early Cambrian Kakul Garlaniyan phosphorites.

The objective is to compare simple prediction methods and evaluate whether the inclusion of grain-type information reduces prediction errors.

## Dataset and prediction target

The dataset consists of 103 in-situ analytical measurements from Supplementary Table S2 of Ali et al. (2026).

The prediction target is total REY concentration (ppm).

The candidate predictors are:

- Petrographic grain type: oolite or pellet.
- Major-element chemistry: F, Na2O, MgO, FeO, P2O5, CaO, MnO, Al2O3, and SiO2.

Individual REY concentrations and REY-derived indices were not included as predictors because these variables could introduce target leakage.

## Model comparison

Four predictive approaches were evaluated:

1. Median baseline: predicts the median REY concentration calculated from the training data.
2. Grain-type-only Ridge regression.
3. EPMA major-element Ridge regression.
4. Combined EPMA and grain-type Ridge regression.

Ridge regression used a fixed regularization parameter of alpha = 10.0. This was an exploratory modelling choice rather than an independently optimized parameter.

Missing numerical predictor values were imputed using training-set medians. Numerical variables were standardized, while grain type was encoded as a categorical predictor.

Preprocessing was fitted within the training portion of each cross-validation fold.

## Cross-validation and evaluation

Five-fold GroupKFold cross-validation was applied using provisional parent-rock groups inferred from analytical-point identifiers and stratigraphic layers.

The dataset contains 103 analytical measurements assigned to 26 provisional rock groups.

The script confirmed that no inferred rock group appeared simultaneously in the training and testing sets.

However, these groups have not yet been independently verified against the original sample records.

The principal evaluation metric was rock-weighted mean absolute error (MAE), which gives equal weight to each inferred rock group.

Spot-weighted MAE and root mean squared error (RMSE) were also calculated.

## Model performance

**Table 1. Prediction errors obtained using five-fold grouped cross-validation. All values are in ppm.**

| Model | Rock-weighted MAE | Spot MAE | RMSE |
|---|---:|---:|---:|
| Grain type only | 97.68 | 95.78 | 122.62 |
| EPMA + grain type | 100.78 | 102.40 | 131.31 |
| EPMA chemistry only | 123.70 | 129.08 | 163.60 |
| Median baseline | 124.79 | 126.86 | 157.51 |

The grain-type-only model produced the lowest prediction errors among the evaluated methods.

Relative to the median baseline, this model reduced rock-weighted MAE from 124.79 to 97.68 ppm, representing an improvement of approximately 21.7%.

The combined model performed better than the EPMA-only model but did not outperform the grain-type-only model.

EPMA-only Ridge regression provided little improvement over the median baseline according to rock-weighted MAE.

## Preliminary interpretation

The results suggest that petrographic grain type contains useful information for predicting total REY concentrations within the analyzed Kakul Garlaniyan dataset.

The limited performance of the EPMA-only model indicates that the selected major-element measurements did not provide a substantial predictive improvement under the present modelling conditions.

However, these results describe statistical prediction rather than geological causation. The models cannot independently determine the processes responsible for REY enrichment.

## Limitations

The dataset contains a limited number of independent geological samples, with multiple analytical measurements potentially originating from the same parent rock.

The parent-rock grouping remains provisional and requires verification.

The results are based on one geological locality and cannot establish predictive transfer to other phosphorite deposits.

The Ridge regularization parameter was fixed without nested model selection. Model uncertainty and sensitivity to alternative evaluation settings have not yet been fully assessed.

The model comparison should therefore be regarded as an exploratory assessment rather than definitive evidence of predictive generalization.

## Reproducibility

Python script:

`scripts/03_model_comparison.py`

Generated outputs:

- `results/metrics/grouped_predictions.csv`
- `results/metrics/model_comparison.csv`

The experiment was executed using the project's Python virtual environment. Dependency versions are recorded in `requirements-lock.txt`.

## Reference

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. Journal of Asian Earth Sciences, 298, 106927.

https://doi.org/10.1016/j.jseaes.2025.106927
