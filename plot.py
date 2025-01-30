import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from config import PROCESSED_DATA_DIR, RESULTS_DIR, PLOTS_DIR

pca_data = pd.read_csv(RESULTS_DIR / "pca_results.csv")

def parts_by_year_intervals():

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

def plot_pca(pca_data, x_col='principal_component_1', y_col='principal_component_2', theme_col='theme'):
    """
    Wizualizacja PCA z adnotacjami punktów odstających.
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set(xlabel='Principal Component 1', ylabel='Principal Component 2', title='2 Component PCA')

    # Tworzenie mapy kolorów dla unikalnych tematów
    themes = pca_data[theme_col].unique()
    colors = sns.color_palette('hsv', len(themes))
    color_map = dict(zip(themes, colors))

    # Lista do przechowywania adnotacji
    texts = []

    # Rysowanie punktów i adnotacji dla odstających elementów
    for theme, group in pca_data.groupby(theme_col):
        ax.scatter(group[x_col], group[y_col], color=color_map[theme], s=30)

        # Wybór odstających punktów
        outliers = group[group[x_col] > 15]
        for _, row in outliers.iterrows():
            texts.append(ax.annotate(row[theme_col],
                                     (row[x_col], row[y_col]),
                                     xytext=(row[x_col] + 0.5, row[y_col] + 0.5),
                                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),
                                     ha='center'))

    # Dopasowanie pozycji tekstów
    adjust_text(texts, only_move={'points': 'y', 'text': 'y'}, autoalign='x')

    ax.grid()
    ax.set_facecolor((0.96, 0.96, 0.96))

    plt.savefig(PLOTS_DIR / 'pca2.png')


def plot_pca_top5(pca_data, x_col='principal_component_1', y_col='principal_component_2', theme_col='theme'):
    """
    Wykres PCA dla 5 najczęściej występujących tematów.
    """
    # Wybór 5 najczęściej występujących tematów
    top_themes = pca_data[theme_col].value_counts().head(5).index

    # Przygotowanie wykresu
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 Component PCA (Top 5 Themes)', fontsize=20)

    # Kolory dla top 5 tematów
    colors = ['r', 'g', 'b', 'c', 'm']  # Stała paleta kolorów
    for theme, color in zip(top_themes, colors):
        indices = pca_data[theme_col] == theme
        ax.scatter(pca_data.loc[indices, x_col],
                   pca_data.loc[indices, y_col],
                   c=color,
                   s=50,  # Rozmiar punktów
                   alpha=0.5,  # Przezroczystość
                   label=theme)

    # Dodanie legendy
    ax.legend(loc='best', fontsize=12)

    # Dodanie siatki
    ax.grid()
    ax.set_facecolor((0.96, 0.96, 0.96))  # Jasne tło

    # Zapisanie wykresu do folderu 'plots'
    plot_path = PLOTS_DIR / 'pca2_top5.png'
    plt.savefig(plot_path)



def starwars():
    """
    Tworzy wykres liczby zestawów LEGO Star Wars na przestrzeni lat z oznaczeniem premier filmowych.
    """
    sets_info = pd.read_csv(RESULTS_DIR / 'sets_info.csv')

    # Filtrowanie zestawów Star Wars
    star_wars_sets = sets_info[sets_info['theme'].str.contains('Star Wars', na=False)]

    # Grupowanie liczby zestawów po roku
    sets_by_year = star_wars_sets.groupby('year').size().reset_index(name='count')

    important_years = [
        {"year": 2015, "label": "The Force Awakens", "color": "r"},
        {"year": 2018, "label": "Solo: A Star Wars Story", "color": "y"}
    ]

    # Tworzenie wykresu
    plt.figure(figsize=(12, 6))
    plt.bar(sets_by_year['year'], sets_by_year['count'], color='blue')

    # Dodanie pionowych linii dla premier filmowych
    for event in important_years:
        plt.axvline(
            x=event["year"],
            color=event["color"],
            linestyle="--",
            label=f'{event["label"]} ({event["year"]})'
        )

    # Dodanie tytułu i etykiet osi
    plt.title('Liczba zestawów LEGO Star Wars na przestrzeni lat')
    plt.xlabel('Rok')
    plt.ylabel('Liczba zestawów')
    plt.legend()

    plt.savefig(PLOTS_DIR / 'star_wars_sets_with_films.png')
    plt.close()



def average_parts_histogram():

    sets = pd.read_csv(PROCESSED_DATA_DIR / 'sets.csv')

    # Grupowanie danych po roku i obliczanie średniej liczby części
    avg_parts_per_year = sets.groupby("year")['num_parts'].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x="year", y="num_parts", data=avg_parts_per_year, palette="viridis", hue="year", legend=False)

    plt.title("Średnia liczba części w zestawach LEGO na przestrzeni lat", fontsize=16)
    plt.xlabel("Rok", fontsize=12)
    plt.ylabel("Średnia liczba części", fontsize=12)
    plt.xticks(rotation=90)

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plot_path = PLOTS_DIR / 'average_parts_histogram.png'
    plt.savefig(plot_path)

if __name__ == "__main__":
    parts_by_year_intervals()
    plot_pca(pca_data)
    plot_pca_top5(pca_data)
    starwars()
    average_parts_histogram()