import pandas as pd
from config import PROCESSED_DATA_DIR, RESULTS_DIR

def prepare_data(sort_by="year", ascending=True):
    """Prepares a csv file with information about Lego sets that will be used in the analysis."""

    sets = pd.read_csv(PROCESSED_DATA_DIR / "sets.csv")
    themes = pd.read_csv(PROCESSED_DATA_DIR / "themes.csv")
    inventory_minifigs = pd.read_csv(PROCESSED_DATA_DIR / "inventory_minifigs.csv")
    inventories = pd.read_csv(PROCESSED_DATA_DIR / "inventories.csv")
    inventory_parts = pd.read_csv(PROCESSED_DATA_DIR / "inventory_parts.csv")

    sets = sets.merge(themes, left_on="theme_id", right_on="id", suffixes=("", "_theme"))
    sets = sets.rename(columns={"name_theme": "theme"})

    # Połączenie inventory_minifigs z inventories w celu uzyskania set_num
    inventory_minifigs = inventory_minifigs.merge(inventories, left_on="inventory_id", right_on="id", how="left")

    # Obliczenie liczby minifigurek na zestaw
    minifigs_count = inventory_minifigs.groupby("set_num")['quantity'].sum().reset_index(name="num_minifigs")

    # Połączenie liczby minifigurek z zestawami
    sets = sets.merge(minifigs_count, on="set_num", how="left")
    sets['num_minifigs'] = sets['num_minifigs'].fillna(0).astype(int)

    # Obliczenie liczby unikalnych kolorów na zestaw
    inventory_parts = inventory_parts.merge(inventories, left_on="inventory_id", right_on="id", how="left")
    unique_colors = inventory_parts.groupby("set_num")['color_id'].nunique().reset_index(name="unique_colors")

    # Połączenie liczby unikalnych kolorów z zestawami
    sets = sets.merge(unique_colors, on="set_num", how="left")
    sets['unique_colors'] = sets['unique_colors'].fillna(0).astype(int)

    # Obliczenie liczby unikalnych elementów na zestaw
    unique_parts = inventory_parts.groupby("set_num")['part_num'].nunique().reset_index(name="unique_parts")

    # Połączenie liczby unikalnych elementów z zestawami
    sets = sets.merge(unique_parts, on="set_num", how="left")
    sets['unique_parts'] = sets['unique_parts'].fillna(0).astype(int)

    # Wybór kolumn do zapisu w odpowiedniej kolejności
    result = sets[['set_num', 'name', 'num_parts', 'num_minifigs', 'theme', 'year', 'unique_colors', 'unique_parts', 'img_url']]

    # Sortowanie wyników po wybranym argumencie
    result = result.sort_values(by=sort_by, ascending=ascending)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(RESULTS_DIR / "sets_info.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    prepare_data(sort_by="num_parts", ascending=False)
