from pathlib import Path
import pandas as pd
from utils import get_repo_path
from config import FILES, BASE_URL, REPO_PATH, RAW_DATA_DIR, PROCESSED_DATA_DIR, PREPARED_DATA_DIR, RESULTS_DIR, PCA_RESULTS_FILE, PLOTS_DIR

def get_star_wars_sets():
    """
    Filtruje zestawy LEGO związane z tematyką Star Wars i zapisuje wynikowy CSV do folderu data/results.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    sets_file = PROCESSED_DATA_DIR / 'sets.csv'
    themes_file = PROCESSED_DATA_DIR / 'themes.csv'
    output_file = RESULTS_DIR  / 'starwars_results.csv'

    # Wczytanie danych
    sets = pd.read_csv(sets_file)
    themes = pd.read_csv(themes_file)

    # Filtracja tematów "Star Wars"
    star_wars_related_themes = themes[themes['name'].str.contains('Star Wars', case=False, na=False)]
    all_star_wars_ids = star_wars_related_themes['id'].tolist()

    # Filtracja zestawów z tematami Star Wars
    star_wars_sets = sets[sets['theme_id'].isin(all_star_wars_ids)]

    # Zapis do pliku CSV
    star_wars_sets.to_csv(output_file, index=False)
    print(f"Zestawy Star Wars zapisano do {output_file}")

    return output_file

get_star_wars_sets()