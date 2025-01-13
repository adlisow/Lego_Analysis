import pandas as pd
from config import PROCESSED_DATA_DIR, RESULTS_DIR

def prepare_data():
    """Przygotowuje dane do analizy PCA"""

    inventories = pd.read_csv(PROCESSED_DATA_DIR / "inventories.csv")
    sets = pd.read_csv(PROCESSED_DATA_DIR / "sets.csv")
    themes = pd.read_csv(PROCESSED_DATA_DIR / "themes.csv")
    inventory_minifigs = pd.read_csv(PROCESSED_DATA_DIR / "inventory_minifigs.csv")
    inventory_parts = pd.read_csv(PROCESSED_DATA_DIR / "inventory_parts.csv")

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
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_data.to_csv(RESULTS_DIR / "prepared_data.csv", index=False)

if __name__ == "__main__":
    prepare_data()
