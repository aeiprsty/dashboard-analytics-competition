import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FILES = [
    "sinyal_clean.csv",
    "akses_jenjang_clean.csv",
    "partisipasi_clean.csv",
    "komputer_clean.csv"
]

for filename in FILES:
    df = pd.read_csv(PROCESSED_DIR / filename)

    missing = df[df.isnull().any(axis=1)]

    print("\n" + "=" * 60)
    print(f"DATASET: {filename}")
    print("=" * 60)

    if missing.empty:
        print("Tidak ada missing value")
    else:
        print(missing.to_string(index=False))
