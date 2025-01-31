import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from config import RESULTS_DIR

data = pd.read_csv(RESULTS_DIR / "sets_info.csv")
features = ['num_minifigs', 'num_parts', 'unique_parts']
target = "theme"

def perform_pca(n_components=2):
    """Performs PCA analysis on the determined data and saves the results to a csv file in the results folder."""

    x = data.loc[:, features].values
    y = data.loc[:, [target]]

    # Standaryzacja
    x = StandardScaler().fit_transform(x)

    # Analiza PCA
    pca = PCA(n_components)
    principal_components = pca.fit_transform(x)

    principal_df = pd.DataFrame(data=principal_components, columns=['principal_component_1', 'principal_component_2'])
    final_df = pd.concat([principal_df, y.reset_index(drop=True)], axis=1)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(RESULTS_DIR / "pca_results.csv", index=False)

    print(f"Liczba komponentów: {pca.n_components_}")
    print(f"Zachowana wariancja: {sum(pca.explained_variance_ratio_):.2f}")

if __name__ == "__main__":
    perform_pca()






