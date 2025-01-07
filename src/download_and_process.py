import os
import gzip
import shutil
import requests
from src.utils import get_repo_path
from config import FILES, BASE_URL, RAW_DATA_DIR, PROCESSED_DATA_DIR

# Funkcja pobierająca pliki do folderu data/raw
def download_files():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    for file_name in FILES:
        url = f"{BASE_URL}{file_name}"
        output_path = RAW_DATA_DIR / file_name
        print(f"Downloading {file_name}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {file_name} to {output_path}")
        else:
            print(f"Failed to download {file_name}: {response.status_code}")

# Funkcja rozpakowująca pliki do folderu data/processed
def process_files():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    for file_name in FILES:
        raw_file_path = RAW_DATA_DIR / file_name
        if not os.path.exists(raw_file_path):
            print(f"File {raw_file_path} does not exist. Skipping.")
            continue

        processed_file_name = file_name.replace(".gz", "")
        processed_file_path = PROCESSED_DATA_DIR / processed_file_name

        print(f"Processing {file_name}...")
        try:
            with gzip.open(raw_file_path, "rb") as gz_file:
                with open(processed_file_path, "wb") as csv_file:
                    shutil.copyfileobj(gz_file, csv_file)
            print(f"Saved processed file to {processed_file_path}")
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

if __name__ == "__main__":
    print("Starting download...")
    download_files()
    print("\nStarting processing...")
    process_files()
    print("\nAll done!")
