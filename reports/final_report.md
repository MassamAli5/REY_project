
# Rock-Scale and Grain-Type Variation in REY Enrichment in Early Cambrian Phosphorites

**Massam Ali**

**Study area:** Kakul Garlaniyan, Hazara Basin, northeastern Pakistan

**Data source:** Ali et al. (2026), Supplementary Table S2

## Abstract

This study examines variations in total rare earth element and yttrium (REY) concentrations among phosphatic components of the Early Cambrian Kakul Garlaniyan phosphorites. The analysis uses 103 published in-situ geochemical measurements from three phosphorite layers. The research addresses two questions: whether oolites exhibit consistently higher mean REY concentrations than pellets within inferred parent rocks, and whether petrographic grain type provides useful information for predicting total REY concentrations.

Descriptive statistics, within-group comparisons, Ridge regression, grouped cross-validation, and an exploratory learning-curve analysis were conducted. Among 13 inferred rock groups containing both oolite and pellet measurements, 12 showed higher mean REY concentrations in oolites. The equal-group mean difference was +179.37 ppm. In the predictive comparison, the grain-type-only model achieved the lowest rock-weighted mean absolute error (97.68 ppm), compared with 124.79 ppm for the median baseline. Adding EPMA major-element measurements did not improve prediction beyond grain type alone under the tested settings.

These findings indicate a relationship between grain type and REY concentration in the analyzed dataset. However, parent-rock identifiers remain provisional, and the results cannot establish geological causation or predictive transfer beyond the studied locality.

## 1. Introduction

### 1.1 Geological background

Phosphorites are sedimentary deposits enriched in phosphate minerals, principally apatite. Their geochemical compositions provide information relevant to phosphorus cycling, marine sedimentary environments, and the processes accompanying phosphate mineralization.

Rare earth elements and yttrium (REY) are commonly investigated in phosphorites because their concentrations and distributions can vary with mineral formation, geochemical conditions, and subsequent modification.

However, REY concentrations are not controlled by a single geological process. Differences among phosphatic components may reflect variations in mineral growth, geochemical uptake, sedimentary reworking, and alteration. Consequently, variations in total REY concentration must be distinguished from interpretations concerning the processes responsible for enrichment.

The Early Cambrian Kakul Garlaniyan phosphorites in northeastern Pakistan contain different phosphatic components, including pseudo-oolites and pellets. Their mineralogical and geochemical characteristics were investigated by Ali et al. (2026).

The published study documented differences in REY concentrations among phosphatic components and examined the depositional conditions associated with phosphogenesis.

### 1.2 Research problem

The published geochemical data contain multiple analytical measurements from different phosphatic components and stratigraphic layers.

Directly comparing all individual measurements may obscure differences among rock samples because several analytical spots can originate from the same parent rock.

This creates two related analytical problems.

First, grain-type differences should be examined within inferred parent-rock groups rather than only through pooled comparisons across the complete dataset.

Second, predictive models should be evaluated without allowing analytical measurements assigned to the same inferred parent rock to appear simultaneously in the training and testing datasets.

These considerations are particularly important for small geological datasets containing repeated measurements.

### 1.3 Research objectives

The present study addresses two research questions:

1. Do oolites exhibit consistently higher mean total REY concentrations than pellets within the same inferred parent rocks?

2. Does petrographic grain type improve prediction of total REY concentrations relative to a simple baseline and EPMA major-element chemistry?

The first question concerns the distribution of REY among phosphatic components.

The second evaluates the predictive information associated with grain type and selected chemical measurements.

The study does not attempt to determine seawater redox conditions, identify REY sources, or establish the geological mechanism responsible for REY enrichment using machine learning.

## 2. Dataset and Data Preparation

### 2.1 Data source

The dataset was obtained from Supplementary Table S2 of Ali et al. (2026), published in the Journal of Asian Earth Sciences.

The supplementary measurements were originally collected for geological and geochemical investigation of the Kakul Garlaniyan phosphorites.

The present Data Science project reuses these published measurements for exploratory statistical comparisons and regression modelling.

The dataset contains 103 in-situ analytical records distributed among three phosphorite layers:

- Lower phosphorite layer (LPL)
- Middle phosphorite layer (MPL)
- Upper phosphorite layer (UPL)

### 2.2 Analytical components

The measurements comprise four original petrographic categories.

**Table 1. Distribution of in-situ analytical measurements among phosphatic components.**

| Phosphatic component | Number of measurements |
|---|---:|
| Oolite core | 35 |
| Oolite rim | 27 |
| Pellet core | 20 |
| Pellet rim | 21 |
| **Total** | **103** |

For the principal comparisons, the original categories were combined into two grain types: oolite and pellet.

This grouping follows the component labels in the published supplementary data. It does not represent automated petrographic image classification.

### 2.3 Geochemical variables

The principal response variable is total REY concentration, expressed in parts per million (ppm).

Nine EPMA chemical variables were considered as candidate predictors:

F, Na2O, MgO, FeO, P2O5, CaO, MnO, Al2O3, and SiO2.

Petrographic grain type was included as a categorical predictor.

Individual REY concentrations and REY-derived indices were not used as predictors because they could introduce information directly related to the calculated total REY target.

Analytical-point identifiers and inferred parent-rock labels were used for grouping and evaluation rather than as predictive features.

### 2.4 Data import and preparation

The supplementary workbook was imported using Python and pandas.

The analysis used the worksheet named `Supplementary file 2`, with the analytical column headers identified in the third spreadsheet row.

Some stratigraphic-layer and mineral-phase labels were represented by merged cells in the original workbook. These labels were recovered using forward filling after import.

Records without analytical-point identifiers were excluded from the analysis table.

The resulting dataset contained 103 analytical measurements.

For predictive modelling, numerical variables were converted into numerical data types. Missing predictor values were handled through median imputation within the training-fold preprocessing pipeline.

Numerical predictors were standardized, while the grain-type variable was encoded categorically.

The original workbook was not modified.

A complete assessment of missing values, analytical quality flags, and possible inconsistencies between published tables remains necessary before stronger scientific conclusions can be considered.

### 2.5 Observation units and inferred rock groups

An important distinction is that 103 analytical measurements do not necessarily represent 103 independent geological samples.

The analytical-point identifiers contain numerical prefixes that may correspond to individual parent-rock samples.

For this project, provisional rock groups were constructed by combining each numerical prefix with its stratigraphic-layer label.

This procedure identified 26 inferred parent-rock groups.

These assignments are operational group labels derived from the supplementary spreadsheet. They have not yet been independently confirmed against original sample documentation.

The distinction is important because the reliability of within-rock comparisons and grouped model validation depends on whether these labels represent the actual geological sampling structure.

## 3. Exploratory Geochemical Analysis

### 3.1 Distribution of total REY concentrations

The 103 analytical measurements have total REY concentrations ranging from 222.77 to 922.74 ppm.

The mean total REY concentration is 587.87 ppm, with a standard deviation of 152.21 ppm.

Figure 1 presents the distribution of total REY concentrations across the three phosphorite layers.

![Total REY concentrations among phosphorite layers](../results/figures/rey_by_layer.png)

*Figure 1. Distribution of total REY concentrations in the lower, middle, and upper phosphorite layers of the Kakul Garlaniyan section.*

The distributions overlap among the three layers, indicating substantial variation within the measured components.

These descriptive results do not establish statistically significant differences between stratigraphic units or identify the processes responsible for the observed variability.

### 3.2 REY concentrations among phosphatic components

Figure 2 compares the distribution of total REY concentrations between oolites and pellets within each phosphorite layer.

![Total REY concentrations by grain type](../results/figures/rey_by_grain_type_and_layer.png)

*Figure 2. Distribution of total REY concentrations in oolites and pellets from the lower, middle, and upper phosphorite layers.*

Mean concentrations for the two grain types are summarized in Table 2.

**Table 2. Mean total REY concentrations in oolites and pellets from the three phosphorite layers.**

| Phosphorite layer | Oolites (ppm) | Pellets (ppm) |
|---|---:|---:|
| LPL | 648.81 | 488.60 |
| MPL | 612.02 | 425.33 |
| UPL | 704.21 | 500.37 |

Oolites exhibit higher mean total REY concentrations than pellets in all three layers.

This pattern is consistent with grain-type differences described in the published geological study.

Nevertheless, these are pooled comparisons among individual analytical measurements. They do not account directly for the possibility that multiple measurements originate from the same rock.

A within-group comparison is therefore needed to examine whether the observed relationship persists among inferred parent rocks.

## 4. Within-Group Comparison of REY Concentrations

### 4.1 Analytical approach

To examine grain-type differences within inferred parent rocks, analytical measurements were grouped according to their provisional parent-rock identifiers.

Only groups containing both oolite and pellet measurements were retained.

For each eligible group, mean total REY concentrations were calculated separately for oolites and pellets.

The within-group difference was defined as:

**REY difference (ppm) = Mean oolite REY - Mean pellet REY**

A positive value indicates higher mean REY concentration in oolites, whereas a negative value indicates higher mean concentration in pellets.

The overall mean difference was calculated by assigning equal weight to each eligible inferred rock group.

This approach prevents groups containing more analytical measurements from automatically contributing greater weight to the overall mean difference.

### 4.2 Results

Thirteen inferred parent-rock groups contained both oolite and pellet measurements.

Of these, 12 exhibited higher mean total REY concentrations in oolites.

One group, LPL_KG_5, showed the opposite relationship.

**Table 3. Summary of the within-group REY comparison.**

| Measurement | Result |
|---|---:|
| Matched inferred rock groups | 13 |
| Groups with higher oolite mean REY | 12 |
| Groups with higher pellet mean REY | 1 |
| Mean oolite-minus-pellet difference | +179.37 ppm |
| Median difference | +194.01 ppm |
| Exploratory bootstrap lower limit | +93.70 ppm |
| Exploratory bootstrap upper limit | +247.77 ppm |

The equal-group mean difference was +179.37 ppm, indicating higher average REY concentrations in oolites across most matched inferred groups.

An exploratory bootstrap analysis was performed using 10,000 resamples of the group-level differences with random seed 42.

The resulting percentile interval extended from +93.70 to +247.77 ppm.

This interval summarizes uncertainty under the assumed grouping and resampling procedure. It should not be considered definitive inferential evidence while the underlying parent-rock identities remain unverified.

### 4.3 Geological implications and limitations

The within-group results suggest that higher REY concentrations in oolites are not restricted to comparisons involving pooled measurements from different phosphorite layers.

Nevertheless, the negative difference observed in LPL_KG_5 demonstrates that the relationship is not uniform.

The results cannot independently determine whether differences in REY concentration developed during phosphate mineral formation, subsequent geochemical uptake, sedimentary reworking, or later modification.

Furthermore, the comparisons involve inferred rock-group means rather than verified paired measurements from individual grains.

The evidence therefore supports an exploratory association between grain type and REY concentration, not a unique geological explanation.

## 5. Predictive Modelling

### 5.1 Prediction target and modelling objective

The predictive analysis estimates total REY concentration in ppm from petrographic grain type and selected EPMA measurements.

The modelling objective is to determine whether grain type provides useful predictive information compared with a simple baseline and whether major-element chemistry improves prediction.

A small set of relatively simple models was selected because the number of observations and inferred independent geological groups is limited.

### 5.2 Baseline and regression models

Four approaches were evaluated:

1. Training-set median baseline.
2. Grain-type-only Ridge regression.
3. EPMA major-element Ridge regression.
4. Combined EPMA and grain-type Ridge regression.

The median baseline predicts the median REY concentration calculated using the training data.

Ridge regression was selected as a regularized linear modelling approach.

A fixed regularization parameter of alpha = 10.0 was used in all Ridge models.

This value was used for exploratory comparison and was not independently selected using nested cross-validation.

Therefore, differences in performance should be interpreted within the present fixed modelling configuration.

### 5.3 Preprocessing and target-leakage prevention

Numerical predictor values were processed using median imputation and standardization.

Grain type was encoded using OneHotEncoder.

These transformations were placed inside scikit-learn pipelines so that preprocessing parameters were estimated using training data only.

The total REY target, its constituent individual REY measurements, and REY-derived indices were excluded from the predictor variables.

Analytical-point identifiers and provisional rock-group labels were not used as predictive features.

These procedures were intended to reduce target leakage and prevent preprocessing information from the held-out records entering the fitted model.

### 5.4 Cross-validation design

Five-fold GroupKFold cross-validation was used to evaluate the regression models.

The group labels were based on the provisionally inferred parent-rock identifiers.

All measurements assigned to an inferred rock group were kept together within a fold, rather than being randomly distributed between training and testing.

The Python script explicitly checked that the training and test partitions did not share inferred rock-group labels.

This establishes separation according to the constructed identifiers, although it does not independently prove that the identifiers correspond to the true parent-rock relationships.

### 5.5 Performance metrics

The principal evaluation metric was rock-weighted mean absolute error (MAE), expressed in ppm.

The absolute errors were first averaged within each inferred rock group. The resulting group-level errors were then averaged, giving each inferred rock equal weight.

Two supplementary metrics were calculated:

- Spot-weighted MAE, in which each analytical measurement contributes equally.
- Root mean squared error (RMSE), which places greater weight on larger prediction errors.

Lower values indicate smaller errors.

These evaluation metrics measure predictive performance rather than the ability of the model to explain geological processes.

## 6. Predictive Model Results

### 6.1 Comparison of predictive performance

The results of five-fold grouped cross-validation are presented in Table 4.

**Table 4. Prediction errors obtained using five-fold grouped cross-validation. All values are in ppm.**

| Model | Rock-weighted MAE | Spot MAE | RMSE |
|---|---:|---:|---:|
| Grain type only | 97.68 | 95.78 | 122.62 |
| EPMA + grain type | 100.78 | 102.40 | 131.31 |
| EPMA chemistry only | 123.70 | 129.08 | 163.60 |
| Median baseline | 124.79 | 126.86 | 157.51 |

The grain-type-only Ridge regression model produced the lowest rock-weighted MAE among the evaluated approaches.

Its error of 97.68 ppm was approximately 21.7% lower than the median baseline error of 124.79 ppm.

The combined EPMA and grain-type model had a rock-weighted MAE of 100.78 ppm.

Although this was lower than the EPMA-only model error of 123.70 ppm, it was slightly higher than the grain-type-only model error.

Thus, the inclusion of the selected major-element measurements did not improve prediction beyond grain type alone under the present modelling settings.

### 6.2 Feature-ablation comparison

The model comparisons also provide a direct assessment of the predictive contribution of grain type.

Removing grain type from the combined model increased rock-weighted MAE from 100.78 to 123.70 ppm.

Conversely, adding the selected EPMA chemical variables to the grain-type-only model increased MAE from 97.68 to 100.78 ppm.

These results suggest that the petrographic grain-type label contains useful predictive information for total REY concentrations within the present dataset.

However, the comparison does not demonstrate that major-element chemistry is geologically unimportant.

The EPMA variables may have limited variation, correlated values, analytical uncertainties, or relationships not adequately represented by the present linear models.

The findings are therefore restricted to the tested variables, model structure, and evaluation procedure.

### 6.3 Interpretation of model performance

The predictive results are broadly consistent with the descriptive observation that total REY concentrations differ between oolites and pellets.

A model using only grain type can exploit this difference when estimating the total REY concentration of held-out measurements.

Nevertheless, successful prediction from a categorical petrographic label does not establish the cause of the concentration difference.

It also does not demonstrate that equivalent predictive relationships exist in phosphorites from other geological settings.

The available evidence supports a limited conclusion: grain type provides predictive information within this dataset under the selected validation procedure.

## 7. Learning-Curve Analysis

### 7.1 Experimental design

An exploratory learning-curve experiment was conducted to assess how prediction error changes with the number of training rock groups.

The analysis compared the median baseline and the grain-type-only Ridge regression model.

Five-fold GroupKFold validation was retained.

Within each training partition, inferred rock groups were subsampled at 25%, 50%, 75%, and 100% of the available groups.

Three subsamples were evaluated at the smaller training fractions, while the complete training partition was evaluated once per fold.

The random seed was fixed at 42.

The test groups remained separate from the selected training groups.

### 7.2 Learning-curve results

**Table 5. Mean held-out fold-level rock-weighted MAE at different training-group fractions (ppm).**

| Training fraction | Grain-type model | Median baseline |
|---|---:|---:|
| 25% | 110.75 | 129.80 |
| 50% | 102.62 | 125.14 |
| 75% | 98.97 | 123.34 |
| 100% | 96.58 | 123.51 |

![Learning curve for total REY prediction](../results/figures/learning_curve.png)

*Figure 3. Exploratory learning curve showing mean held-out rock-weighted prediction errors for the grain-type-only Ridge regression model and the training-set median baseline.*

The grain-type-only model showed decreasing average prediction error as the proportion of available training groups increased.

Mean error decreased from 110.75 ppm at the 25% training fraction to 96.58 ppm at the full training fraction.

The median baseline showed a smaller overall reduction, from 129.80 to 123.51 ppm.

The grain-type-only model achieved a lower average error at every tested training fraction.

These findings suggest that the model benefits from the additional training groups included in this particular experiment.

### 7.3 Relationship to the principal model comparison

The full-training learning-curve result of 96.58 ppm differs slightly from the primary model-comparison result of 97.68 ppm.

This difference reflects the aggregation procedures used in the two scripts.

The principal model-comparison script calculates rock-weighted MAE from the combined held-out predictions.

The learning-curve script calculates fold-level rock-weighted MAE before averaging across folds.

Because different folds may contain different numbers of rock groups, the resulting averages can differ.

The principal model-comparison result remains the primary predictive estimate.

### 7.4 Limitations of the learning curve

Repeated subsamples within the same cross-validation folds are not statistically independent experiments.

The available groups are few, and the parent-rock identities remain provisional.

Furthermore, the grain-type-only model was selected for this learning-curve examination after reviewing earlier exploratory results.

The learning curve therefore provides a diagnostic assessment of training-size sensitivity, not independent confirmation of predictive performance.

## 8. Discussion

### 8.1 Relationship between geological and predictive results

The geological comparison and regression results are related but address different questions.

The within-group analysis examines whether oolites have higher mean REY concentrations than pellets within inferred geological samples.

The predictive analysis evaluates whether grain type reduces prediction errors on held-out inferred groups.

The within-group results show positive oolite-minus-pellet differences in 12 of 13 matched groups.

The grain-type-only regression also produces the lowest prediction error among the tested models.

Together, these findings suggest that the distinction between oolites and pellets is associated with total REY variation in the analyzed Kakul Garlaniyan measurements.

However, the same underlying dataset supports both analyses. They should not be treated as independent confirmation of the geological relationship.

### 8.2 Scientific interpretation

The observed differences in total REY concentration may reflect differences associated with the formation or subsequent modification of phosphatic components.

The available statistical analyses do not distinguish among these possible explanations.

In particular, the predictive model does not include a physical or geochemical representation of phosphate formation, sedimentary transport, or diagenetic reactions.

A relationship between grain type and total REY concentration therefore cannot be interpreted as direct evidence of a particular enrichment mechanism.

The results may help identify which petrographic distinctions are useful for organizing further geochemical investigation.

Their geological significance must be assessed alongside petrographic observations, analytical quality, and independent geological evidence.

### 8.3 Predictive limitations

The model comparisons are restricted to a small dataset from one locality.

Although the grouped validation procedure prevents overlap between constructed group labels, the true independence of these groups has not yet been verified.

Furthermore, the results were obtained using fixed modelling settings rather than fully independent model selection.

The observed differences in prediction error should therefore not be generalized to other phosphorite deposits or geological environments.

### 8.4 Study boundaries

This study is exploratory.

The published data establish the measurement basis, while the new computational analysis provides an additional quantitative comparison of grain-type variation and predictive performance.

The project does not claim discovery of grain-type REY enrichment as a previously unknown phenomenon.

It also does not claim that its regression results independently establish the geological processes controlling phosphogenesis.

## 9. Reproducibility, Ethics, and Data Rights

### 9.1 Computational environment

The analyses were conducted in VS Code using Python and a project-specific virtual environment.

The workflow uses pandas, numpy, scipy, matplotlib, openpyxl, and scikit-learn.

The dependency files are:

- `requirements.txt`
- `requirements-lock.txt`

The project README provides instructions for setting up the environment and running the scripts.

### 9.2 Reproducibility of results

The computational workflow is organized into separate scripts for:

1. Data auditing.
2. Exploratory visualization.
3. Model comparison.
4. Within-group REY comparison.
5. Learning-curve evaluation.

The scripts save their outputs automatically to the appropriate result folders.

The main predictive evaluation uses five-fold GroupKFold validation with fixed model settings.

The within-group bootstrap uses random seed 42 and 10,000 repetitions.

The learning-curve experiment uses random seed 42.

Numerical results can be inspected through the generated CSV files, subject to access to the original published dataset.

### 9.3 Research ethics and data permissions

The dataset consists of geological measurements and contains no human-subject information.

However, publication of scientific data does not automatically establish unrestricted permission for redistribution or machine-learning use.

The original workbook is therefore retained locally unless the applicable permissions are confirmed.

The public project repository should provide source code, dependency information, methodology, and permitted supporting materials without exposing data that the team is not authorized to redistribute.

### 9.4 AI assistance and team responsibility

The research was conducted by Massam Ali and Hussain Rabani.

ChatGPT was used primarily to suggest and draft Python code and troubleshoot programming errors. Some written documentation also received drafting assistance.

The team created and managed the project files, executed the scripts locally, reviewed numerical outputs, examined figures, and remained responsible for the research questions, scientific interpretation, and reported conclusions.

The AI assistance record is maintained in `docs/ai_use_record.md`.

The final submission must also identify each member's actual individual contributions. These should be confirmed by the team rather than assigned retrospectively without evidence.

## 10. Conclusions and Remaining Work

The initial exploratory analysis of the Kakul Garlaniyan phosphorites supports three principal observations.

First, mean total REY concentrations are higher in oolites than pellets in each of the three studied phosphorite layers.

Second, within 13 matched inferred parent-rock groups, 12 show higher mean REY concentrations in oolites. The equal-group mean difference is +179.37 ppm.

Third, the grain-type-only Ridge regression model achieves the lowest rock-weighted prediction error among the four evaluated approaches. Its MAE of 97.68 ppm is lower than the median baseline error of 124.79 ppm.

The selected EPMA major-element measurements do not improve performance beyond grain type alone under the current settings.

These findings indicate that grain type is associated with total REY variation and contains useful predictive information within the analyzed dataset.

However, the results remain exploratory because inferred parent-rock groups are not independently verified, the number of geological groups is limited, and the models have not been externally validated.

The next scientific priorities are to verify parent-rock assignments, examine sensitivity to individual groups and alternative modelling settings, and evaluate whether similar relationships are present in independent geological samples.

The present findings do not independently establish the geological processes responsible for REY enrichment.

## References

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. *Journal of Asian Earth Sciences*, 298, 106927. https://doi.org/10.1016/j.jseaes.2025.106927

Lumiste, K., et al. (2019). REE+Y uptake and diagenesis in Recent sedimentary apatites. *Chemical Geology*, 525, 268–281. https://doi.org/10.1016/j.chemgeo.2019.07.034

Tahar-Belkacem, N., et al. (2024). Machine learning models to predict rare earth elements distribution in Tethyan phosphate ore deposits: Geochemical and depositional environment implications. *Geochemistry*, 84, 126128. https://doi.org/10.1016/j.chemer.2024.126128
