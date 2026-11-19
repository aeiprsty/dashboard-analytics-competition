import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Baca sebagai teks agar tanda "-" atau sel kosong tetap terlihat
sinyal = pd.read_csv(
    RAW_DIR / "tabel_07_sinyal.csv",
    dtype=str,
    keep_default_na=False
)

komputer = pd.read_csv(
    RAW_DIR / "tabel_25_komputer.csv",
    header=2,
    dtype=str,
    keep_default_na=False
)

print("=" * 60)
print("PEMERIKSAAN DATA ASLI: SINYAL")
print("=" * 60)

provinsi_sinyal = [
    "KEP. BANGKA BELITUNG",
    "KEP. RIAU",
    "DKI JAKARTA",
    "BALI"
]

for provinsi in provinsi_sinyal:
    baris = sinyal[
        sinyal.iloc[:, 0].str.strip().str.upper() == provinsi
    ]
    print(f"\n{provinsi}:")
    if not baris.empty:
        print(baris.to_string(index=False))
    else:
        print("Provinsi tidak ditemukan")

print("\n" + "=" * 60)
print("PEMERIKSAAN DATA ASLI: KOMPUTER")
print("=" * 60)

baris = komputer[
    komputer.iloc[:, 0].str.strip().str.upper() == "DKI JAKARTA"
]

if not baris.empty:
    print(baris.to_string(index=False))
else:
    print("DKI Jakarta tidak ditemukan")
