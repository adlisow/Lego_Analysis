import pandas as pd
from src.utils import get_repo_path

# Ścieżki do katalogów
REPO_PATH = get_repo_path()
PROCESSED_DATA_DIR = REPO_PATH / "data/processed"
PREPARED_DATA_DIR = REPO_PATH / "data/prepared"
PREPARED_FILE_PATH = PREPARED_DATA_DIR / "prepared_data.csv"


def load_processed_data():
    files = ["inventories.csv", "sets.csv",
             "themes.csv", "inventory_minifigs.csv", "inventory_parts.csv"]

    dataframes = {
        file.split(".")[0]: pd.read_csv(PROCESSED_DATA_DIR / file)
        for file in files
    }
    return dataframes
