
# REY Enrichment in Early Cambrian Phosphorites

**Projec**

** Massam Ali

## Research Objective

This project examines grain-type variation in total rare earth element and yttrium (REY) concentrations in the Early Cambrian Kakul Garlaniyan phosphorites of northeastern Pakistan.

The analysis addresses two questions:

1. Do oolites exhibit higher mean total REY concentrations than pellets within the same inferred parent-rock groups?
2. Does petrographic grain type improve prediction of total REY concentrations relative to a simple baseline and EPMA major-element chemistry?

The project combines descriptive geochemical analysis with exploratory statistical learning. Prediction results are not interpreted as evidence of geological causation.

## Data Source

The dataset originates from Supplementary Table S2 associated with:

Ali, M., et al. (2026). Phosphogenesis of Kakul Garlaniyan phosphorites during the early Cambrian in northeastern Pakistan. Journal of Asian Earth Sciences, 298, 106927.

DOI: https://doi.org/10.1016/j.jseaes.2025.106927

The dataset contains:

- 103 in-situ analytical measurements
- Three phosphorite layers: LPL, MPL, and UPL
- Four component classes: oolite core, oolite rim, pellet core, and pellet rim
- Major-element and trace-element measurements

The original workbook is stored locally at:

`data/raw/Supplementray_files.xlsx`

The workbook is not included in the public repository. Users must obtain an authorized copy to reproduce the full analysis. Data redistribution and applicable reuse permissions must be verified.

## Project Structure

```text
REY_project/
    data/
        raw/
        processed/
    scripts/
        project_paths.py
        01_data_audit.py
        02_rey_figures.py
        03_model_comparison.py
        04_within_rock_comparison.py
        05_learning_curve.py
    results/
        tables/
        figures/
        metrics/
        models/
    reports/
        proposal.md
        progress_review.md
        01_initial_observations.md
        02_model_comparison.md
        03_within_rock_comparison.md
        04_learning_curve.md
    docs/
    config/
    notebooks/
    requirements.txt
    requirements-lock.txt
    README.md
```

## Python Environment

The analysis was developed and tested using Python 3.13 in a project-specific virtual environment.

Required packages include:

- pandas
- numpy
- scipy
- matplotlib
- openpyxl
- scikit-learn

Package dependencies are listed in `requirements.txt`.

The exact installed dependency versions are recorded in `requirements-lock.txt`.

### Environment setup on Windows

Create a virtual environment using a compatible Python installation:

```powershell
python -m venv .venv
```

Install the recorded dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Confirm the Python interpreter and installed packages before running the analysis.

## Running the Analysis

Run the following commands from the main project directory.

### 1. Data audit

```powershell
.\.venv\Scripts\python.exe scripts/01_data_audit.py
```

Reads the supplementary data and summarizes analytical records and REY concentrations.

Output:

`results/tables/initial_rey_summary.csv`

### 2. Exploratory figures

```powershell
.\.venv\Scripts\python.exe scripts/02_rey_figures.py
```

Generates boxplots of REY concentrations by phosphorite layer and grain type.

Outputs:

- `results/figures/rey_by_layer.png`
- `results/figures/rey_by_grain_type_and_layer.png`

### 3. Predictive model comparison

```powershell
.\.venv\Scripts\python.exe scripts/03_model_comparison.py
```

Compares a training-set median baseline with grain-type-only, EPMA-only, and combined Ridge regression models.

Uses five-fold group-aware cross-validation with provisional rock-group identifiers.

Outputs:

- `results/metrics/grouped_predictions.csv`
- `results/metrics/model_comparison.csv`

### 4. Within-group REY comparison

```powershell
.\.venv\Scripts\python.exe scripts/04_within_rock_comparison.py
```

Compares mean oolite and pellet REY concentrations within inferred parent-rock groups containing both grain types.

Outputs:

- `results/tables/within_rock_rey_comparison.csv`
- `results/metrics/within_rock_summary.csv`

### 5. Learning-curve analysis

```powershell
.\.venv\Scripts\python.exe scripts/05_learning_curve.py
```

Evaluates prediction errors using different fractions of available training rock groups.

Outputs:

- `results/metrics/learning_curve_raw.csv`
- `results/metrics/learning_curve_summary.csv`
- `results/figures/learning_curve.png`

## Model Evaluation

The prediction target is total REY concentration in ppm.

The main evaluation metric is rock-weighted mean absolute error (MAE).

Additional metrics include spot-weighted MAE and root mean squared error (RMSE).

The regression models use Ridge regularization with a fixed alpha value of 10.0.

Numerical preprocessing is fitted within training folds. Individual REY elements and REY-derived indices are excluded from predictors to avoid predicting total REY using its constituent measurements.

Parent-rock groups are provisionally inferred from stratigraphic labels and analytical-point prefixes. Their identities must be verified against original sample records.

## Preliminary Findings

The initial descriptive analysis includes 103 analytical measurements with a mean total REY concentration of 587.87 ppm.

Among 13 matched inferred parent-rock groups, 12 show higher mean REY concentrations in oolites than pellets. The equal-group mean difference is +179.37 ppm.

In the preliminary grouped model comparison, grain-type-only Ridge regression achieved the lowest rock-weighted MAE of 97.68 ppm, compared with 124.79 ppm for the median baseline.

These findings are exploratory and specific to the present dataset and evaluation protocol.

## Limitations

- Parent-rock identifiers are inferred and remain unverified.
- Multiple analytical measurements may originate from the same geological sample.
- The dataset represents one locality.
- Model settings were not selected through nested hyperparameter optimization.
- Cross-validation does not provide independent external validation.
- REY concentration differences and statistical model performance do not independently establish enrichment mechanisms.

## Reproducibility and Research Documentation

Supporting Markdown documents are stored in `reports/`.

The original data should remain outside public version control until applicable permissions are confirmed.

The project requires documentation of data provenance, modelling assumptions, individual team contributions, and AI assistance. These records must be reviewed and completed before final submission.
