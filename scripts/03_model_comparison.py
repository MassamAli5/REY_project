
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from project_paths import (
    RAW_WORKBOOK,
    METRICS_DIR,
    prepare_folders
)


# --------------------------------------------------
# 1. Read the published geochemical dataset
# --------------------------------------------------

prepare_folders()

df = pd.read_excel(
    RAW_WORKBOOK,
    sheet_name="Supplementary file 2",
    header=2
)

df.columns = df.columns.astype(str).str.strip()

df = df.rename(columns={
    df.columns[0]: "Layer"
})

df = df.dropna(subset=["Points"]).copy()

# Recover labels from merged Excel cells.
df["Layer"] = (
    df["Layer"]
    .ffill()
    .astype(str)
    .str.strip()
)

df["Mineral phase"] = (
    df["Mineral phase"]
    .ffill()
    .astype(str)
    .str.strip()
    .str.lower()
)


# --------------------------------------------------
# 2. Identify phosphatic grain types
# --------------------------------------------------

df["Grain type"] = (
    df["Mineral phase"]
    .str.extract(
        r"^(oolite|pellet)",
        expand=False
    )
)

if df["Grain type"].isna().any():
    raise ValueError(
        "Some grain types could not be identified."
    )


# --------------------------------------------------
# 3. Define provisional parent-rock groups
# --------------------------------------------------

# Example:
# Point 2-1 -> rock-number prefix 2.
# Combine with the phosphorite layer to avoid
# confusing similarly numbered records in
# different layers.

rock_number = (
    df["Points"]
    .astype(str)
    .str.extract(
        r"^(\d+)-",
        expand=False
    )
)

if rock_number.isna().any():
    raise ValueError(
        "Some analytical point identifiers "
        "do not match the expected format."
    )

df["Rock group"] = (
    df["Layer"] + "_KG_" + rock_number
)

# IMPORTANT:
# These are provisional groups inferred from
# analytical identifiers, not independently
# verified parent-rock identities.


# --------------------------------------------------
# 4. Define prediction target and input variables
# --------------------------------------------------

# Target: total REY concentration (ppm).
df["∑REY"] = pd.to_numeric(
    df["∑REY"],
    errors="raise"
)

# Candidate EPMA major-element measurements.
chemistry = [
    "F",
    "Na2O",
    "MgO",
    "FeO",
    "P2O5",
    "CaO",
    "MnO",
    "Al2O3",
    "SiO2"
]

for column in chemistry:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

features = chemistry + ["Grain type"]

X = df[features].reset_index(drop=True)

y = df["∑REY"].to_numpy()

groups = df["Rock group"].reset_index(drop=True)

if not np.isfinite(y).all():
    raise ValueError(
        "The total REY target contains missing "
        "or non-finite values."
    )

print("\nKAKUL GARLANIYAN PHOSPHORITES")
print("---------------------------------------")
print("Analytical records:", len(df))
print("Provisional rock groups:", groups.nunique())
print("Prediction target: Total REY (ppm)")


# --------------------------------------------------
# 5. Prepare grouped cross-validation
# --------------------------------------------------

# Five-fold GroupKFold keeps all measurements
# assigned to one rock group in the same fold.

cv = GroupKFold(n_splits=5)


# --------------------------------------------------
# 6. Define the regression models
# --------------------------------------------------

def create_model(use_chemistry, use_texture):

    transformers = []

    if use_chemistry:

        numerical = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scale",
                StandardScaler()
            )
        ])

        transformers.append(
            ("chemistry", numerical, chemistry)
        )

    if use_texture:

        categorical = OneHotEncoder(
            handle_unknown="ignore"
        )

        transformers.append(
            (
                "texture",
                categorical,
                ["Grain type"]
            )
        )

    preprocessing = ColumnTransformer(
        transformers
    )

    return Pipeline([
        ("preprocessing", preprocessing),
        ("regression", Ridge(alpha=10.0))
    ])


model_settings = {
    "Grain type only": (False, True),
    "EPMA chemistry only": (True, False),
    "EPMA + grain type": (True, True)
}


# --------------------------------------------------
# 7. Train and evaluate each model
# --------------------------------------------------

records = []

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups),
    start=1
):

    train_groups = set(
        groups.iloc[train_idx]
    )

    test_groups = set(
        groups.iloc[test_idx]
    )

    # Prevent inferred parent-rock groups from
    # appearing in both training and test data.
    assert train_groups.isdisjoint(test_groups)

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y[train_idx]

    # Baseline:
    # Predict the median total REY concentration
    # calculated from training data only.
    predictions = {
        "Median baseline": np.full(
            len(test_idx),
            np.median(y_train)
        )
    }

    # Train each Ridge regression model.
    for name, settings in model_settings.items():

        model = create_model(*settings)

        model.fit(
            X_train,
            y_train
        )

        predictions[name] = model.predict(
            X_test
        )

    # Save individual held-out predictions.
    for name, predicted in predictions.items():

        for position, estimate in zip(
            test_idx,
            predicted
        ):

            records.append({
                "fold": fold,
                "model": name,
                "rock_group": groups.iloc[position],
                "actual_rey": float(y[position]),
                "predicted_rey": float(estimate)
            })


# --------------------------------------------------
# 8. Save the predictions
# --------------------------------------------------

predictions_df = pd.DataFrame(records)

predictions_file = (
    METRICS_DIR / "grouped_predictions.csv"
)

predictions_df.to_csv(
    predictions_file,
    index=False
)


# --------------------------------------------------
# 9. Calculate model errors
# --------------------------------------------------

summary_rows = []

for name, subset in predictions_df.groupby("model"):

    absolute_error = (
        subset["actual_rey"] -
        subset["predicted_rey"]
    ).abs()

    subset = subset.assign(
        absolute_error=absolute_error
    )

    # Give each provisional rock group equal weight.
    rock_mae = (
        subset.groupby("rock_group")["absolute_error"]
        .mean()
        .mean()
    )

    # Give each individual analytical spot equal weight.
    spot_mae = mean_absolute_error(
        subset["actual_rey"],
        subset["predicted_rey"]
    )

    # Root mean squared error.
    rmse = np.sqrt(
        np.mean(
            (
                subset["actual_rey"] -
                subset["predicted_rey"]
            ) ** 2
        )
    )

    summary_rows.append({
        "model": name,
        "rock_weighted_mae_ppm": rock_mae,
        "spot_mae_ppm": spot_mae,
        "rmse_ppm": rmse
    })


# --------------------------------------------------
# 10. Save and display model comparison
# --------------------------------------------------

results = pd.DataFrame(summary_rows)

results = results.sort_values(
    "rock_weighted_mae_ppm"
)

comparison_file = (
    METRICS_DIR / "model_comparison.csv"
)

results.round(3).to_csv(
    comparison_file,
    index=False
)

print("\nGROUPED MODEL COMPARISON")
print("---------------------------------------")
print("Cross-validation folds: 5")
print("Training/test group overlap: None")

print("\nPrediction errors (ppm):")
print(
    results.round(2).to_string(index=False)
)

print("\nResults saved to:")
print(predictions_file)
print(comparison_file)

print(
    "\nIMPORTANT: Parent-rock grouping is "
    "provisional and requires verification "
    "against original sample records."
)