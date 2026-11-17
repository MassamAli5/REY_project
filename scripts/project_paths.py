
from pathlib import Path

# Main project directory
ROOT = Path(__file__).resolve().parents[1]

# Data
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
RAW_WORKBOOK = RAW_DIR / "Supplementray_files.xlsx"

# Analysis
SCRIPTS_DIR = ROOT / "scripts"
NOTEBOOKS_DIR = ROOT / "notebooks"

# Results
TABLES_DIR = ROOT / "results" / "tables"
FIGURES_DIR = ROOT / "results" / "figures"
METRICS_DIR = ROOT / "results" / "metrics"
MODELS_DIR = ROOT / "results" / "models"

# Reports and documentation
REPORTS_DIR = ROOT / "reports"
CONFIG_DIR = ROOT / "config"
DOCS_DIR = ROOT / "docs"

DIRECTORIES = [
    RAW_DIR,
    PROCESSED_DIR,
    SCRIPTS_DIR,
    NOTEBOOKS_DIR,
    TABLES_DIR,
    FIGURES_DIR,
    METRICS_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    CONFIG_DIR,
    DOCS_DIR,
]


def prepare_folders():
    for folder in DIRECTORIES:
        folder.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    prepare_folders()

    print("Project folders created successfully.")
    print("Project location:", ROOT)
    print("Raw data location:", RAW_DIR)
    print("Tables will be saved to:", TABLES_DIR)
    print("Figures will be saved to:", FIGURES_DIR)
    print("Reports will be saved to:", REPORTS_DIR)
