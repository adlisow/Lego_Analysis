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


def prepare_data():
    # Wczytanie danych
    data = load_processed_data()
    inventories = data["inventories"]
    sets = data["sets"]
    themes = data["themes"]
    inventory_minifigs = data["inventory_minifigs"]
    inventory_parts = data["inventory_parts"]

    # Łączenie tabel
    sets_themes = pd.merge(sets, themes, left_on="theme_id", right_on="id", suffixes=("_set", "_theme"))
    sets_inventories = pd.merge(sets_themes, inventories, left_on="set_num", right_on="set_num", suffixes=("", "_inventory"))

    # Liczba minifigurek
    minifigs_per_set = pd.merge(sets_inventories, inventory_minifigs, left_on="id_inventory", right_on="inventory_id", how="left")
    minifigs_per_set = minifigs_per_set.groupby(["theme_id", "name_theme", "set_num", "year"]).agg(
        total_minifigs=("quantity", "sum")
    ).reset_index()

    # Ogólna liczba elementów
    parts_per_set = pd.merge(sets_inventories, inventory_parts, left_on="id_inventory", right_on="inventory_id", how="left")
    total_elements_per_set = parts_per_set.groupby(["theme_id", "name_theme", "set_num", "year"]).agg(
        total_elements=("quantity", "sum")
    ).reset_index()

    # Liczba unikalnych elementów
    unique_elements_per_set = parts_per_set.groupby(["theme_id", "name_theme", "set_num", "year"]).agg(
        unique_elements=("part_num", "nunique")
    ).reset_index()

    # Połączenie danych
    final_data = pd.merge(minifigs_per_set, total_elements_per_set, on=["theme_id", "name_theme", "set_num", "year"], how="outer")
    final_data = pd.merge(final_data, unique_elements_per_set, on=["theme_id", "name_theme", "set_num", "year"], how="outer")

    # Uzupełnienie brakujących wartości zerami
    final_data = final_data.fillna(0)

    # Usunięcie niepotrzebnych kolumn
    final_data = final_data.drop(columns=["set_num", "theme_id"])

    # Zapisanie przetworzonych danych
    PREPARED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    final_data.to_csv(PREPARED_FILE_PATH, index=False)

    print(f"Dane przygotowane i zapisane w {PREPARED_FILE_PATH}")

if __name__ == "__main__":
    prepare_data()
