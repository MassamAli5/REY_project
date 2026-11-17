
# Learning-Curve Analysis of REY Prediction

## Research objective

The learning-curve analysis examines how prediction error changes as the number of training rock groups increases.

The analysis uses the published Kakul Garlaniyan in-situ geochemical dataset and compares a grain-type-only Ridge regression model against a training-set median baseline.

The purpose is to assess the sensitivity of predictive performance to training-set size, rather than to establish geological causation or external model generalization.

## Dataset and evaluation method

The dataset contains 103 analytical measurements assigned to 26 provisionally inferred parent-rock groups.

Five-fold GroupKFold cross-validation was used. In each fold, the training rock groups were subsampled at four fractions: 25%, 50%, 75%, and 100%.

The test groups remained separate from training.

Three training-group subsamples were evaluated at 25%, 50%, and 75%. The complete training partition was evaluated once per fold.

The models were:

1. Training-set median baseline.
2. Grain-type-only Ridge regression, with alpha = 10.0.

The evaluation metric was held-out rock-weighted mean absolute error (MAE), expressed in ppm.

The subsampling procedure used random seed 42.

## Learning-curve results

**Table 1. Learning-curve prediction errors for different training-group fractions. Values are mean held-out fold-level rock-weighted MAE (ppm).**

| Training fraction | Grain-type-only model | Median baseline |
|---|---:|---:|
| 25% | 110.75 | 129.80 |
| 50% | 102.62 | 125.14 |
| 75% | 98.97 | 123.34 |
| 100% | 96.58 | 123.51 |

![Learning curve for total REY prediction](../results/figures/learning_curve.png)

*Figure 1. Exploratory learning curve showing mean held-out rock-weighted MAE for grain-type-only Ridge regression and a training-set median baseline. Training percentages refer to the rock groups available within each training partition.*

## Interpretation

The grain-type-only model achieved lower mean prediction errors than the median baseline at all four training fractions.

For the grain-type-only model, mean held-out rock-weighted MAE decreased from 110.75 ppm at 25% of the available training groups to 96.58 ppm at 100%.

The median baseline showed a smaller overall reduction in error, from 129.80 to 123.51 ppm.

These observations suggest that increasing the number of training rock groups improves the predictive performance of the grain-type-only model under the tested conditions.

However, the learning curve does not demonstrate whether additional independent geological samples would produce similar improvements.

## Relationship to the main model comparison

The principal model-comparison experiment reported a rock-weighted MAE of 97.68 ppm for the grain-type-only model and 124.79 ppm for the median baseline.

The corresponding full-training learning-curve errors were 96.58 ppm and 123.51 ppm.

This small difference arises from the error aggregation procedure.

The main model comparison calculates rock-weighted MAE from the combined held-out predictions, whereas the learning-curve analysis calculates an average of fold-level rock-weighted errors.

The original model-comparison values remain the primary reported predictive results.

## Limitations

The analysis has several limitations.

- Parent-rock groups were inferred from analytical identifiers and require verification.
- The dataset contains relatively few independent geological groups.
- Repeated training subsamples and cross-validation folds are not independent experiments.
- Smaller training fractions may produce differences in grain-type representation.
- The reported standard deviations describe variation among fold and subsample evaluations, not independent confidence intervals.
- The grain-type-only model was selected after reviewing previous exploratory results from the same dataset.
- The learning curve does not establish prediction accuracy for other geological localities.

The results are therefore considered exploratory.

## Reproducibility

Python script:

`scripts/05_learning_curve.py`

Generated output files:

- `results/metrics/learning_curve_raw.csv`
- `results/metrics/learning_curve_summary.csv`
- `results/figures/learning_curve.png`

Evaluation settings:

- GroupKFold: 5 folds
- Random seed: 42
- Training fractions: 0.25, 0.50, 0.75, 1.00
- Subsamples per fold: 3 for smaller fractions
- Ridge alpha: 10.0

## Reference

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. Journal of Asian Earth Sciences, 298, 106927.

https://doi.org/10.1016/j.jseaes.2025.106927
