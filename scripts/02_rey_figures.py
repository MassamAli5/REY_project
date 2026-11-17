
import pandas as pd
import matplotlib.pyplot as plt

from project_paths import (
    RAW_WORKBOOK,
    FIGURES_DIR,
    prepare_folders
)

prepare_folders()

# Use Times New Roman in all figures.
plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 12,
    "text.color": "black",
    "axes.labelcolor": "black",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "xtick.color": "black",
    "ytick.color": "black",
    "pdf.fonttype": 42
})

# Read the original published dataset.
df = pd.read_excel(
    RAW_WORKBOOK,
    sheet_name="Supplementary file 2",
    header=2
)

df.columns = df.columns.astype(str).str.strip()
df = df.rename(columns={df.columns[0]: "Layer"})

df = df.dropna(subset=["Points"]).copy()

# Recover merged Excel labels.
df["Layer"] = df["Layer"].ffill().astype(str).str.strip()

df["Mineral phase"] = (
    df["Mineral phase"]
    .ffill()
    .astype(str)
    .str.strip()
    .str.lower()
)

# Classify phosphate grain types.
df["Grain type"] = (
    df["Mineral phase"]
    .str.extract(r"^(oolite|pellet)", expand=False)
    .str.title()
)

df["∑REY"] = pd.to_numeric(df["∑REY"], errors="raise")

if df["Grain type"].isna().any():
    raise ValueError("Unrecognized mineral-phase label.")

layers = ["LPL", "MPL", "UPL"]

if not df["Layer"].isin(layers).all():
    raise ValueError("Unexpected stratigraphic layer.")

# Black-and-white boxplot formatting.
box_style = {
    "patch_artist": True,
    "boxprops": {
        "facecolor": "white",
        "edgecolor": "black"
    },
    "medianprops": {
        "color": "black",
        "linewidth": 2
    },
    "whiskerprops": {"color": "black"},
    "capprops": {"color": "black"},
    "flierprops": {
        "marker": "o",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 4
    }
}

# -------------------------------------------------
# Figure 1: REY concentrations across layers
# -------------------------------------------------

layer_data = [
    df.loc[df["Layer"] == layer, "∑REY"]
    for layer in layers
]

fig, ax = plt.subplots(figsize=(7, 5))


boxes = ax.boxplot(layer_data, **box_style)

# Three colors for the three phosphorite layers.
layer_colors = ["#BBD7EB", "#C5DFC6", "#F2D3B0"]

for patch, color in zip(boxes["boxes"], layer_colors):
    patch.set_facecolor(color)


ax.set_xticks([1, 2, 3])
ax.set_xticklabels(layers)

ax.set_xlabel("Phosphorite layer")
ax.set_ylabel("Total REY (ppm)")
ax.set_title("REY distribution across phosphorite layers")

fig.tight_layout()

file1 = FIGURES_DIR / "rey_by_layer.png"
fig.savefig(file1, dpi=300, bbox_inches="tight")

plt.close(fig)

# -------------------------------------------------
# Figure 2: REY concentrations by grain type
# -------------------------------------------------

grouped_data = []
group_labels = []

for layer in layers:
    for grain in ["Oolite", "Pellet"]:

        subset = df.loc[
            (df["Layer"] == layer) &
            (df["Grain type"] == grain),
            "∑REY"
        ]

        grouped_data.append(subset)
        group_labels.append(f"{layer}\n{grain}")

fig, ax = plt.subplots(figsize=(10, 5))


boxes = ax.boxplot(grouped_data, **box_style)

# Consistent colors for both grain types.
oolite_color = "#5B9BD5"
pellet_color = "#EDAA60"

for i, patch in enumerate(boxes["boxes"]):
    if i % 2 == 0:
        patch.set_facecolor(oolite_color)
    else:
        patch.set_facecolor(pellet_color)


ax.set_xticks(range(1, len(group_labels) + 1))
ax.set_xticklabels(group_labels)

ax.set_xlabel("Phosphorite layer and grain type")
ax.set_ylabel("Total REY (ppm)")
ax.set_title("REY concentrations in phosphatic components")

fig.tight_layout()

file2 = FIGURES_DIR / "rey_by_grain_type_and_layer.png"
fig.savefig(file2, dpi=300, bbox_inches="tight")

plt.close(fig)

print("\nFigures generated successfully.")
print("Figure 1:", file1)
print("Figure 2:", file2)

print("\nNumber of analyses:", len(df))
print("\nREY concentrations by layer and grain type:")

print(
    df.groupby(["Layer", "Grain type"])["∑REY"]
    .agg(["count", "mean", "median", "std"])
    .round(2)
)
