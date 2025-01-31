import pandas as pd
from config import PROCESSED_DATA_DIR, RESULTS_DIR

def p_colors(color_name: str):
    """
    The function generates a csv file of sets sorted by the percentage of the selected color given as an argument
    and saves the results to a csv file in the results folder.
    """

    inventory_parts = pd.read_csv(PROCESSED_DATA_DIR / "inventory_parts.csv")
    colors = pd.read_csv(PROCESSED_DATA_DIR / "colors.csv")
    inventories = pd.read_csv(PROCESSED_DATA_DIR / "inventories.csv")
    sets = pd.read_csv(PROCESSED_DATA_DIR / "sets.csv")

    # Znalezienie ID kolorów, których nazwa zawiera nazwę podaną jako argument (string np. 'green')
    color_filter = colors[colors['name'].str.contains(color_name, case=False, na=False)]
    color_ids = color_filter['id'].tolist()
    print(f"Kolory: {color_ids}")

    # Połączenie inventory_parts z inventories i sets
    inventory_parts = inventory_parts.merge(inventories, left_on="inventory_id", right_on="id")
    inventory_parts = inventory_parts.merge(sets, left_on="set_num", right_on="set_num")

    # Filtrujemy elementy na podstawie koloru
    colored_parts = inventory_parts[inventory_parts['color_id'].isin(color_ids)]

    # Grupowanie i sumowanie części,
    # (liczymy ręcznie liczbę elementów, gdyż liczba num_parts w sets nieznacznie różni się)
    total_parts_per_set = inventory_parts.groupby("set_num")['quantity'].sum().reset_index(name="total_parts")
    colored_parts_per_set = colored_parts.groupby("set_num")['quantity'].sum().reset_index(name="colored_parts")

    # Obliczenie procentowego udziału wybranego koloru
    result = total_parts_per_set.merge(colored_parts_per_set, on="set_num", how="left")
    result['colored_parts'] = result['colored_parts'].fillna(0)
    result['colored_percentage'] = (result['colored_parts'] / result['total_parts']) * 100

    # Sortowanie wyników
    result = result.sort_values(by="colored_percentage", ascending=False)

    # Łączenie z nazwami zestawów oraz linkami do zdjęć
    result = result.merge(sets[['set_num', 'name', 'img_url', 'num_parts']], on="set_num", how="left")

    # Utworzenie wyników do zapisania
    output_data = result[['set_num', 'name', 'colored_percentage', 'img_url', 'num_parts']].to_string(index=False)

    # Zapisujemy w ten sposób dla lepszej czytelności, nie będziemy używać wynikowego csv w kodzie
    with open(RESULTS_DIR / f"{color_name}_sets_result.csv", 'w', encoding='utf-8') as f:
        f.write(output_data)

if __name__ == "__main__":
    p_colors("green")

