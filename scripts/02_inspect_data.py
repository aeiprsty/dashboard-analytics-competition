import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

FILES = {
    "SINYAL": ("tabel_07_sinyal.csv", 0),
    "AKSES JENJANG": ("tabel_13_akses_jenjang.csv", 3),
    "PARTISIPASI": ("tabel_14_partisipasi.csv", 3),
    "KOMPUTER": ("tabel_25_komputer.csv", 3),
}

for name, (filename, skip) in FILES.items():
    df = pd.read_csv(
        RAW_DIR / filename,
        encoding="utf-8-sig",
        skiprows=skip
    )

    print("\n" + "=" * 60)
    print(f"DATASET: {name}")
    print("=" * 60)

    print(f"Jumlah baris: {len(df)}")

    print("\nDaftar wilayah:")
    print(df.iloc[:, 0].to_list())

    print("\nBaris dengan missing value:")
    print(df[df.isnull().any(axis=1)].to_string(index=False))

    print("\nDuplikasi nama wilayah:")
    print(df[df.iloc[:, 0].duplicated(keep=False)].to_string(index=False))
