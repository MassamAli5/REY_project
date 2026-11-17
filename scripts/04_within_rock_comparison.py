
import numpy as np
import pandas as pd

from project_paths import (
    RAW_WORKBOOK,
    TABLES_DIR,
    METRICS_DIR,
    prepare_folders
)


# --------------------------------------------------
# 1. Read the published supplementary measurements
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

df["Layer"] = (
    df["Layer"].ffill().astype(str).str.strip()
)

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
    .str.title()
)

df["∑REY"] = pd.to_numeric(
    df["∑REY"],
    errors="raise"
)

if df["Grain type"].isna().any():
    raise ValueError("Unrecognized grain type.")

if not df["Layer"].isin(["LPL", "MPL", "UPL"]).all():
    raise ValueError("Unexpected phosphorite layer.")


# --------------------------------------------------
# 2. Identify provisional parent-rock groups
# --------------------------------------------------

# Example: analytical point 2-1 has prefix 2.
# Combine the prefix with its stratigraphic layer.

rock_number = (
    df["Points"]
    .astype(str)
    .str.extract(r"^\s*(\d+)\s*-", expand=False)
)

if rock_number.isna().any():
    raise ValueError(
        "Some analytical-point identifiers could not "
        "be interpreted. Check the source workbook."
    )

df["Rock group"] = (
    df["Layer"] + "_KG_" + rock_number
)

# IMPORTANT:
# These identifiers are inferred from Table S2.
# They are not yet independently verified.


# --------------------------------------------------
# 3. Calculate mean REY within each rock and type
# --------------------------------------------------

group_summary = (
    df.groupby(
        ["Layer", "Rock group", "Grain type"]
    )
    .agg(
        mean_rey_ppm=("∑REY", "mean"),
        spot_count=("∑REY", "size")
    )
    .reset_index()
)

# Put oolite and pellet means into separate columns.
means = group_summary.pivot(
    index=["Layer", "Rock group"],
    columns="Grain type",
    values="mean_rey_ppm"
)

counts = group_summary.pivot(
    index=["Layer", "Rock group"],
    columns="Grain type",
    values="spot_count"
)

# Only compare groups containing both grain types.
matched = (
    means.dropna(subset=["Oolite", "Pellet"])
    .copy()
)

matched = matched.rename(columns={
    "Oolite": "oolite_mean_ppm",
    "Pellet": "pellet_mean_ppm"
})

matched["oolite_spots"] = counts.loc[
    matched.index, "Oolite"
].astype(int)

matched["pellet_spots"] = counts.loc[
    matched.index, "Pellet"
].astype(int)

# Difference for each provisional parent rock.
matched["difference_ppm"] = (
    matched["oolite_mean_ppm"] -
    matched["pellet_mean_ppm"]
)

matched = matched.reset_index()

matched = matched.sort_values(
    ["Layer", "Rock group"]
).reset_index(drop=True)


# --------------------------------------------------
# 4. Calculate overall descriptive results
# --------------------------------------------------

differences = matched["difference_ppm"].to_numpy()

n_rocks = len(differences)

if n_rocks < 2:
    raise ValueError(
        "Not enough matched rock groups "
        "for a within-group comparison."
    )

mean_difference = np.mean(differences)
median_difference = np.median(differences)

positive_rocks = np.sum(differences > 0)
negative_rocks = np.sum(differences < 0)
equal_rocks = np.sum(differences == 0)


# --------------------------------------------------
# 5. Exploratory bootstrap interval
# --------------------------------------------------

# Resample inferred parent-rock differences,
# not individual analytical spots.

random_seed = 42
n_bootstrap = 10000

rng = np.random.default_rng(random_seed)

bootstrap_samples = rng.choice(
    differences,
    size=(n_bootstrap, n_rocks),
    replace=True
)

bootstrap_means = bootstrap_samples.mean(axis=1)

ci_lower, ci_upper = np.percentile(
    bootstrap_means,
    [2.5, 97.5]
)

# This interval is descriptive and depends on
# the provisional grouping and sampling assumptions.


# --------------------------------------------------
# 6. Save detailed results
# --------------------------------------------------

detail_file = (
    TABLES_DIR / "within_rock_rey_comparison.csv"
)

matched.round(3).to_csv(
    detail_file,
    index=False
)

summary = pd.DataFrame([{
    "analytical_spots": len(df),
    "provisional_rock_groups": df["Rock group"].nunique(),
    "matched_rock_groups": n_rocks,
    "positive_differences": int(positive_rocks),
    "negative_differences": int(negative_rocks),
    "equal_differences": int(equal_rocks),
    "mean_difference_ppm": mean_difference,
    "median_difference_ppm": median_difference,
    "bootstrap_ci_lower_ppm": ci_lower,
    "bootstrap_ci_upper_ppm": ci_upper,
    "bootstrap_seed": random_seed,
    "bootstrap_repetitions": n_bootstrap
}])

summary_file = (
    METRICS_DIR / "within_rock_summary.csv"
)

summary.round(3).to_csv(
    summary_file,
    index=False
)


# --------------------------------------------------
# 7. Display results
# --------------------------------------------------

print("\nKAKUL GARLANIYAN PHOSPHORITES")
print("---------------------------------------")

print("Total analytical spots:", len(df))
print(
    "Provisional parent-rock groups:",
    df["Rock group"].nunique()
)

print(
    "Groups with both grain types:",
    n_rocks
)

print("\nWITHIN-GROUP REY COMPARISON")
print("---------------------------------------")

print(
    "Groups with higher oolite REY:",
    int(positive_rocks)
)

print(
    "Groups with higher pellet REY:",
    int(negative_rocks)
)

print(
    "Groups with equal mean REY:",
    int(equal_rocks)
)

print(
    f"\nMean oolite-minus-pellet difference: "
    f"{mean_difference:.2f} ppm"
)

print(
    f"Median difference: "
    f"{median_difference:.2f} ppm"
)

print(
    f"Exploratory bootstrap 95% interval: "
    f"{ci_lower:.2f} to {ci_upper:.2f} ppm"
)

print("\nDIFFERENCES BY INFERRED ROCK GROUP")
print("---------------------------------------")

print(
    matched[
        ["Layer", "Rock group", "difference_ppm"]
    ].round(2).to_string(index=False)
)

print("\nResults saved to:")
print(detail_file)
print(summary_file)

print(
    "\nCAUTION: Parent-rock IDs are inferred "
    "from analytical-point prefixes. "
    "Verify against original records before "
    "making independent-rock claims."
)
