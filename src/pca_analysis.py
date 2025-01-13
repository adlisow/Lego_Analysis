import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.utils import get_repo_path

# Ścieżki do katalogów
REPO_PATH = get_repo_path()
PREPARED_DATA_FILE = REPO_PATH / "data/prepared/prepared_data.csv"
RESULTS_DIR = REPO_PATH / "results"


def perform_pca(n_components=2):
    """Wykonuje analize PCA dla ustalonych danych i zapisuje wyniki w pliku csv w folderze results"""

    data = pd.read_csv(PREPARED_DATA_FILE)

    features = ['year', 'total_minifigs', 'total_elements', 'unique_elements']
    target = "name_theme"

    x = data.loc[:, features].values
    y = data.loc[:, [target]]

    # Standaryzacja
    x = StandardScaler().fit_transform(x)

    # Analiza PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)

    principal_df = pd.DataFrame(data=principal_components, columns=['principal_component_1', 'principal_component_2'])
    final_df = pd.concat([principal_df, y.reset_index(drop=True)], axis=1)

    # Zapis wyników do pliku
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(RESULTS_DIR / "pca_results.csv", index=False)

if __name__ == "__main__":
    perform_pca()






