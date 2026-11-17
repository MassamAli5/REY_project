
# Within-Rock Comparison of REY Concentrations

## Research objective

This analysis examines whether differences in total rare earth element and yttrium (REY) concentrations between oolites and pellets are maintained when measurements are compared within the same inferred parent-rock groups.

The comparison uses the published in-situ geochemical dataset from the Early Cambrian Kakul Garlaniyan phosphorites (Ali et al., 2026).

## Data and grouping

The original dataset contains 103 in-situ analytical measurements from three phosphorite layers: LPL, MPL, and UPL.

Analytical-point identifiers were used to infer provisional parent-rock groups. Each group was identified by combining the phosphorite layer with the numerical prefix of the analytical-point identifier.

Only groups containing both oolite and pellet measurements were included in the within-group comparison.

Thirteen inferred rock groups met this requirement.

The grouping is provisional and must be verified against the original sample records before making definitive independent-rock claims.

## Analytical method

For each eligible inferred rock group, mean total REY concentrations were calculated separately for oolites and pellets.

The difference was defined as:

REY difference (ppm) = Mean oolite REY - Mean pellet REY

A positive difference indicates higher mean REY concentrations in oolites, whereas a negative difference indicates higher mean concentrations in pellets.

The overall mean difference was calculated by assigning equal weight to each eligible inferred rock group.

An exploratory bootstrap analysis was performed using 10,000 resamples of the group-level differences, with random seed 42. The 2.5th and 97.5th percentiles were used to summarize the bootstrap distribution.

## Results

**Table 1. Differences in mean total REY concentrations between oolites and pellets within inferred rock groups.**

| Layer | Inferred rock group | Oolite minus pellet (ppm) |
|---|---|---:|
| LPL | LPL_KG_4 | 166.01 |
| LPL | LPL_KG_5 | -237.35 |
| LPL | LPL_KG_6 | 418.41 |
| MPL | MPL_KG_13 | 165.16 |
| MPL | MPL_KG_14 | 194.01 |
| MPL | MPL_KG_15 | 283.53 |
| MPL | MPL_KG_17 | 190.04 |
| MPL | MPL_KG_20 | 176.84 |
| UPL | UPL_KG_23 | 247.34 |
| UPL | UPL_KG_24 | 86.41 |
| UPL | UPL_KG_25 | 215.25 |
| UPL | UPL_KG_27 | 219.52 |
| UPL | UPL_KG_29 | 206.68 |

Of the 13 inferred rock groups containing both phosphatic components, 12 exhibit higher mean total REY concentrations in oolites than in pellets.

One group, LPL_KG_5, exhibits the opposite relationship, with a difference of -237.35 ppm.

The equal-group mean difference is +179.37 ppm, while the median difference is +194.01 ppm.

The exploratory bootstrap 95% interval for the mean difference ranges from +93.70 to +247.77 ppm.

## Discussion

The results indicate that higher mean REY concentrations in oolites are observed in most of the matched inferred rock groups.

This provides a more detailed assessment than comparisons based only on pooled analytical measurements from individual phosphorite layers.

However, the negative difference observed in LPL_KG_5 shows that the relationship is not uniform across all groups.

The measurements do not establish whether these differences originated during phosphate formation, subsequent modification, or other geological processes.

The bootstrap interval provides an exploratory measure of variation under the assumed grouping and resampling procedure. It should not be interpreted as definitive statistical evidence until the parent-rock assignments and their independence are verified.

## Limitations

The main limitations are:

- Parent-rock groups are inferred from analytical identifiers rather than independently verified records.
- The number of matched inferred rock groups is small.
- Each group may contain unequal numbers of analytical spots.
- The analysis compares group means rather than confirmed paired grains.
- The dataset represents a single geological locality.
- The results do not independently establish geological causation.

Further verification of sample identifiers is necessary before stronger conclusions are drawn.

## Reproducibility

Python script:

`scripts/04_within_rock_comparison.py`

Generated output files:

- `results/tables/within_rock_rey_comparison.csv`
- `results/metrics/within_rock_summary.csv`

The bootstrap procedure used 10,000 resamples and random seed 42.

## Reference

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. Journal of Asian Earth Sciences, 298, 106927.

https://doi.org/10.1016/j.jseaes.2025.106927
