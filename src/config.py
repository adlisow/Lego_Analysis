from pathlib import Path
from src.utils import get_repo_path

# Lista plików do pobrania
FILES = [
    "themes.csv.gz",
    "colors.csv.gz",
    "part_categories.csv.gz",
    "parts.csv.gz",
    "part_relationships.csv.gz",
    "elements.csv.gz",
    "sets.csv.gz",
    "minifigs.csv.gz",
    "inventories.csv.gz",
    "inventory_parts.csv.gz",
    "inventory_sets.csv.gz",
    "inventory_minifigs.csv.gz",
]

BASE_URL = "https://cdn.rebrickable.com/media/downloads/"

# Ścieżki do folderów
repo_path = get_repo_path()
RAW_DATA_DIR = repo_path / "data/raw"
PROCESSED_DATA_DIR = repo_path / "data/processed"