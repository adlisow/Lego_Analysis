import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from config import PROCESSED_DATA_DIR, RESULTS_DIR, PLOTS_DIR

pca_data = pd.read_csv(RESULTS_DIR / "pca_results.csv")

def parts_by_year_intervals():
    """
    Funkcja generuje wykres słupkowy porównujący średnią liczbę elementów na zestaw w wybranych przedziałach czasowych,
    wykres typu .png zapisywany jest w folderze plots
    """

    sets = pd.read_csv(PROCESSED_DATA_DIR / 'sets.csv')

    # Obliczenie średniej liczby części w przedziałach
    sets_1990_1999 = sets[sets['year'].between(1990, 1999)]
    sets_2000_2009 = sets[sets['year'].between(2000, 2009)]
    sets_2010_2024 = sets[sets['year'].between(2010, 2024)]

    avg_parts_1990_1999 = sets_1990_1999['num_parts'].mean()
    avg_parts_2000_2009 = sets_2000_2009['num_parts'].mean()
    avg_parts_2010_2024 = sets_2010_2024['num_parts'].mean()

    # Przygotowanie danych do wykresu
    visual_data = pd.DataFrame({
        "Period": ["1990-1999", "2000-2009", "2010-2024"],
        "Average Parts": [avg_parts_1990_1999, avg_parts_2000_2009, avg_parts_2010_2024]
    })

    # Tworzenie wykresu słupkowego
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Period", y="Average Parts", hue="Period", data=visual_data, palette="viridis", dodge=False,
                legend=False)
    plt.title("Porównanie średniej liczby części w zestawach LEGO", fontsize=16)
    plt.ylabel("Średnia liczba części", fontsize=12)
    plt.xlabel("Przedziały czasowe", fontsize=12)

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plot_path = PLOTS_DIR / 'average_parts_comparison.png'
    plt.savefig(plot_path)


if __name__ == "__main__":
    parts_by_year_intervals()
