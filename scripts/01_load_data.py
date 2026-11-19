import pandas as pd
from pathlib import Path

# Root project
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Daftar dataset
FILES = {
    "sinyal": "tabel_07_sinyal.csv",
    "akses_jenjang": "tabel_13_akses_jenjang.csv",
    "partisipasi": "tabel_14_partisipasi.csv",
    "komputer": "tabel_25_komputer.csv"
}

def load_csv(filename):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    return pd.read_csv(file_path, encoding="utf-8-sig")

def main():
    datasets = {}

    for name, filename in FILES.items():
        try:
            df = load_csv(filename)
            datasets[name] = df

            print(f"\n{'=' * 50}")
            print(f"DATASET: {name.upper()}")
            print(f"{'=' * 50}")

            print(f"Jumlah baris  : {df.shape[0]}")
            print(f"Jumlah kolom  : {df.shape[1]}")
            print(f"Nama kolom    : {df.columns.tolist()}")
            print(f"Missing value : {df.isnull().sum().sum()}")

            print("\nPreview:")
            print(df.head())

        except Exception as e:
            print(f"\nGagal membaca {filename}: {e}")

if __name__ == "__main__":
    main()
