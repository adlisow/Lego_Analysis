import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.utils import get_repo_path

# Ścieżki do katalogów
REPO_PATH = get_repo_path()
PREPARED_DATA_FILE = REPO_PATH / "data/prepared/prepared_data.csv"
RESULTS_DIR = REPO_PATH / "data/results"
PCA_RESULTS_FILE = RESULTS_DIR / "pca_results.csv"




