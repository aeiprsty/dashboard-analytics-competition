import pandas as pd
from pathlib import Path

# Direktori
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FINAL_DIR = BASE_DIR / "data" / "final"

FINAL_DIR.mkdir(parents=True, exist_ok=True)

# Membaca empat dataset hasil feature engineering
sinyal = pd.read_csv(PROCESSED_DIR / "sinyal_feature.csv")
akses = pd.read_csv(PROCESSED_DIR / "akses_jenjang_feature.csv")
partisipasi = pd.read_csv(PROCESSED_DIR / "partisipasi_feature.csv")
komputer = pd.read_csv(PROCESSED_DIR / "komputer_feature.csv")

# Memastikan setiap dataset memiliki satu baris per provinsi
datasets = {
    "Sinyal": sinyal,
    "Akses pendidikan": akses,
    "Partisipasi": partisipasi,
    "Komputer": komputer
}

for nama, df in datasets.items():
    assert "Provinsi" in df.columns, f"Kolom Provinsi tidak ditemukan pada {nama}"
    assert df["Provinsi"].is_unique, f"Ada provinsi duplikat pada {nama}"

# Menggabungkan berdasarkan Provinsi
final = sinyal.merge(
    akses,
    on="Provinsi",
    how="inner",
    validate="one_to_one"
)

final = final.merge(
    partisipasi,
    on="Provinsi",
    how="inner",
    validate="one_to_one"
)

final = final.merge(
    komputer,
    on="Provinsi",
    how="inner",
    validate="one_to_one"
)

# Merapikan nama kolom hasil penggabungan
final = final.rename(columns={
    "Total_Distribusi_x": "Total_Distribusi_Jenjang",
    "Total_Distribusi_y": "Total_Distribusi_Partisipasi"
})

# Validasi hasil penggabungan
print("=" * 60)
print("VALIDASI DATASET FINAL")
print("=" * 60)

print("Jumlah baris:", len(final))
print("Jumlah provinsi unik:", final["Provinsi"].nunique())
print("Jumlah kolom:", len(final.columns))
print("\nJumlah missing value:")
print(final.isna().sum()[final.isna().sum() > 0])

assert len(final) == 38, "Jumlah provinsi tidak sesuai!"
assert final["Provinsi"].nunique() == 38, "Ada provinsi duplikat!"

# Simpan dataset final
output_path = FINAL_DIR / "dashboard_pendidikan_final.csv"
final.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nDataset final berhasil disimpan:")
print(output_path)
print("\nPreview:")
print(final.head().to_string(index=False))