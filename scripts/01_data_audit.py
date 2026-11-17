
import pandas as pd
from project_paths import (
    RAW_WORKBOOK,
    TABLES_DIR,
    prepare_folders,
)

prepare_folders()

# Read the published in-situ geochemical data.
df = pd.read_excel(
    RAW_WORKBOOK,
    sheet_name="Supplementary file 2",
    header=2
)

# Remove unnecessary spaces from column names.
df.columns = df.columns.astype(str).str.strip()

# Name the first column as stratigraphic layer.
df = df.rename(columns={df.columns[0]: "Layer"})

# Remove empty analytical records.
df = df.dropna(subset=["Points"]).copy()

# Recover labels from merged Excel cells.
df["Layer"] = df["Layer"].ffill()
df["Mineral phase"] = df["Mineral phase"].ffill()

# Print basic information.
print("\nKAKUL GARLANIYAN PHOSPHORITES")
print("-----------------------------------")

print("Total analytical records:", len(df))
print("Total columns:", len(df.columns))

print("\nAnalyses by phosphorite layer:")
print(df["Layer"].value_counts().sort_index())

print("\nPhosphatic components:")
print(df["Mineral phase"].value_counts())

print("\nTotal REY concentration (ppm):")
print(df["∑REY"].describe().round(2))

# Save the initial summary automatically.
summary = (
    df.groupby(["Layer", "Mineral phase"])["∑REY"]
    .agg(["count", "mean", "std", "min", "max"])
    .round(2)
    .reset_index()
)

output_file = TABLES_DIR / "initial_rey_summary.csv"

summary.to_csv(output_file, index=False)

print("\nSummary saved to:")
print(output_file)
