
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from project_paths import (
    RAW_WORKBOOK,
    METRICS_DIR,
    FIGURES_DIR,
    prepare_folders
)


# --------------------------------------------------
# 1. Read the published dataset
# --------------------------------------------------

prepare_folders()

df = pd.read_excel(
    RAW_WORKBOOK,
    sheet_name="Supplementary file 2",
    header=2
)

df.columns = df.columns.astype(str).str.strip()
df = df.rename(columns={df.columns[0]: "Layer"})
df = df.dropna(subset=["Points"]).copy()

df["Layer"] = df["Layer"].ffill().astype(str).str.strip()

df["Mineral phase"] = (
    df["Mineral phase"]
    .ffill()
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Grain type"] = (
    df["Mineral phase"]
    .str.extract(r"^(oolite|pellet)", expand=False)
)

rock_number = (
    df["Points"]
    .astype(str)
    .str.extract(r"^\s*(\d+)\s*-", expand=False)
)

if rock_number.isna().any():
    raise ValueError("Unrecognized analytical-point identifiers.")

if df["Grain type"].isna().any():
    raise ValueError("Unrecognized grain-type labels.")

df["Rock group"] = df["Layer"] + "_KG_" + rock_number

df["∑REY"] = pd.to_numeric(
    df["∑REY"],
    errors="raise"
)

if not np.isfinite(df["∑REY"]).all():
    raise ValueError("Invalid total REY measurements.")

X = df[["Grain type"]].reset_index(drop=True)
y = df["∑REY"].to_numpy()
groups = df["Rock group"].reset_index(drop=True)


# --------------------------------------------------
# 2. Define the grain-type regression model
# --------------------------------------------------

def make_model():

    preprocessing = ColumnTransformer([
        (
            "grain_type",
            OneHotEncoder(handle_unknown="ignore"),
            ["Grain type"]
        )
    ])

    return Pipeline([
        ("preprocessing", preprocessing),
        ("regression", Ridge(alpha=10.0))
    ])


# --------------------------------------------------
# 3. Define rock-weighted prediction error
# --------------------------------------------------

def rock_weighted_mae(actual, predicted, rock_labels):

    errors = pd.DataFrame({
        "rock_group": np.asarray(rock_labels),
        "absolute_error": np.abs(
            np.asarray(actual) - np.asarray(predicted)
        )
    })

    return float(
        errors.groupby("rock_group")["absolute_error"]
        .mean()
        .mean()
    )


# --------------------------------------------------
# 4. Learning-curve evaluation
# --------------------------------------------------

training_fractions = [0.25, 0.50, 0.75, 1.00]

random_seed = 42
repetitions = 3

cv = GroupKFold(n_splits=5)

records = []

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups),
    start=1
):

    available_groups = np.unique(
        groups.iloc[train_idx].to_numpy()
    )

    test_groups = set(
        groups.iloc[test_idx]
    )

    for repetition in range(repetitions):

        # The full training set is identical across
        # repetitions, so evaluate it only once.
        if repetition > 0:
            fractions_to_use = training_fractions[:-1]
        else:
            fractions_to_use = training_fractions

        rng = np.random.default_rng(
            random_seed + fold * 100 + repetition
        )

        # Smaller training sets are nested within
        # larger ones for this fold and repetition.
        shuffled_groups = rng.permutation(
            available_groups
        )

        for fraction in fractions_to_use:

            number_of_groups = max(
                2,
                int(np.ceil(
                    len(available_groups) * fraction
                ))
            )

            selected_groups = shuffled_groups[
                :number_of_groups
            ]

            selected_mask = groups.iloc[
                train_idx
            ].isin(selected_groups).to_numpy()

            selected_indices = train_idx[
                selected_mask
            ]

            assert set(
                groups.iloc[selected_indices]
            ).isdisjoint(test_groups)

            X_train = X.iloc[selected_indices]
            y_train = y[selected_indices]

            X_test = X.iloc[test_idx]
            y_test = y[test_idx]

            test_rock_labels = groups.iloc[
                test_idx
            ].to_numpy()

            # Baseline: median of selected training data.
            baseline_prediction = np.full(
                len(test_idx),
                np.median(y_train)
            )

            # Grain-type-only Ridge regression.
            model = make_model()

            model.fit(
                X_train,
                y_train
            )

            model_prediction = model.predict(
                X_test
            )

            predictions = {
                "Median baseline": baseline_prediction,
                "Grain type only": model_prediction
            }

            for name, predicted in predictions.items():

                error = rock_weighted_mae(
                    y_test,
                    predicted,
                    test_rock_labels
                )

                records.append({
                    "fold": fold,
                    "repetition": repetition + 1,
                    "training_fraction": fraction,
                    "training_rock_groups": number_of_groups,
                    "training_spots": len(selected_indices),
                    "model": name,
                    "held_out_rock_mae_ppm": error
                })


# --------------------------------------------------
# 5. Save raw evaluation results
# --------------------------------------------------

raw_results = pd.DataFrame(records)

raw_file = (
    METRICS_DIR / "learning_curve_raw.csv"
)

raw_results.to_csv(
    raw_file,
    index=False
)


# --------------------------------------------------
# 6. Summarize prediction errors
# --------------------------------------------------

summary = (
    raw_results
    .groupby(
        ["model", "training_fraction"]
    )
    .agg(
        mean_mae_ppm=(
            "held_out_rock_mae_ppm", "mean"
        ),
        std_mae_ppm=(
            "held_out_rock_mae_ppm", "std"
        ),
        evaluations=(
            "held_out_rock_mae_ppm", "size"
        )
    )
    .reset_index()
)

summary_file = (
    METRICS_DIR / "learning_curve_summary.csv"
)

summary.round(3).to_csv(
    summary_file,
    index=False
)


# --------------------------------------------------
# 7. Generate the learning-curve figure
# --------------------------------------------------

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 12,
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "pdf.fonttype": 42
})

fig, ax = plt.subplots(figsize=(7, 5))

model_styles = {
    "Median baseline": {
        "marker": "s",
        "linestyle": "--"
    },
    "Grain type only": {
        "marker": "o",
        "linestyle": "-"
    }
}

for name, style in model_styles.items():

    subset = summary[
        summary["model"] == name
    ].sort_values("training_fraction")

    
ax.plot(
    subset["training_fraction"] * 100,
    subset["mean_mae_ppm"],
    color=("#5B9BD5" if name == "Grain type only" else "#EDAA60"),
    marker=style["marker"],
    linestyle=style["linestyle"],
    linewidth=1.5,
    markersize=6,
    label=name
)


ax.set_xlabel("Available training rock groups used (%)")
ax.set_ylabel("Held-out rock-weighted MAE (ppm)")
ax.set_xticks([25, 50, 75, 100])

ax.legend(frameon=False)

fig.tight_layout()

figure_file = (
    FIGURES_DIR / "learning_curve.png"
)

fig.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 8. Display the results
# --------------------------------------------------

print("\nKAKUL GARLANIYAN: LEARNING CURVE")
print("---------------------------------------")

print("Analytical records:", len(df))
print("Provisional rock groups:", groups.nunique())
print("Cross-validation folds: 5")
print("Random seed:", random_seed)

print("\nLearning-curve results:")

print(
    summary.round(2).to_string(index=False)
)

print("\nSaved results:")
print(raw_file)
print(summary_file)
print(figure_file)

print(
    "\nIMPORTANT: This is an exploratory learning "
    "curve using provisional parent-rock groups."
)

print(
    "Repeated subsamples and folds are not "
    "independent experiments."
)

print(
    "Model selection was informed by earlier "
    "exploratory results on the same dataset."
)
