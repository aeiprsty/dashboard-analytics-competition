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

# Menyeragamkan nama kolom hasil penggabungan
final = final.rename(columns={
    "Total_Distribusi_x": "Total_Distribusi_Jenjang",
    "Total_Distribusi_y": "Total_Distribusi_Partisipasi"
})

# Standarisasi nama kolom ke format snake_case
rename_columns = {
    "Provinsi": "provinsi",
    "Desa_3G": "desa_3g",
    "Desa_2_5G": "desa_2_5g",
    "Desa_Tanpa_Sinyal": "desa_tanpa_sinyal",
    "Desa_4G_5G": "desa_4g_5g",
    "Jumlah_Kategori_Tersedia": "jumlah_kategori_tersedia",
    "Total_Desa": "total_desa",
    "Desa_Dengan_Sinyal": "desa_dengan_sinyal",
    "Persentase_Desa_4G_5G": "persentase_desa_4g_5g",
    "Total_Kategori": "total_kategori",
    "Selisih_Total": "selisih_total",
    "SD": "sd",
    "SMP": "smp",
    "SMA": "sma",
    "D1-D3": "d1_d3",
    "S1 ke atas": "s1_ke_atas",
    "Total_Distribusi_Jenjang": "total_distribusi_jenjang",
    "Jenjang_Dominan": "jenjang_dominan",
    "Persentase_Jenjang_Dominan": "persentase_jenjang_dominan",
    "Tidak/Belum Pernah Sekolah": "tidak_belum_pernah_sekolah",
    "Masih Bersekolah": "masih_bersekolah",
    "Tidak Sekolah Lagi": "tidak_sekolah_lagi",
    "Total_Distribusi_Partisipasi": "total_distribusi_partisipasi",
    "Kategori_Dominan": "kategori_dominan",
    "Persentase_Kategori_Dominan": "persentase_kategori_dominan",
    "Perkotaan": "perkotaan",
    "Perdesaan": "perdesaan",
    "Perkotaan+Perdesaan": "perkotaan_perdesaan",
    "Selisih_Kota_Desa": "selisih_kota_desa",
    "Wilayah_Lebih_Tinggi": "wilayah_lebih_tinggi"
}

final = final.rename(columns=rename_columns)

# Menentukan urutan kolom dataset final
final_columns = [
    "provinsi",
    "desa_3g",
    "desa_2_5g",
    "desa_tanpa_sinyal",
    "desa_4g_5g",
    "jumlah_kategori_tersedia",
    "total_desa",
    "desa_dengan_sinyal",
    "persentase_desa_4g_5g",
    "total_kategori",
    "selisih_total",
    "sd",
    "smp",
    "sma",
    "d1_d3",
    "s1_ke_atas",
    "total_distribusi_jenjang",
    "jenjang_dominan",
    "persentase_jenjang_dominan",
    "tidak_belum_pernah_sekolah",
    "masih_bersekolah",
    "tidak_sekolah_lagi",
    "total_distribusi_partisipasi",
    "kategori_dominan",
    "persentase_kategori_dominan",
    "perkotaan",
    "perdesaan",
    "perkotaan_perdesaan",
    "selisih_kota_desa",
    "wilayah_lebih_tinggi"
]

# Memastikan seluruh kolom yang dibutuhkan tersedia
missing_columns = [
    col for col in final_columns if col not in final.columns
]

assert not missing_columns, (
    f"Kolom yang dibutuhkan tidak ditemukan: {missing_columns}"
)

# Memilih dan mengurutkan kolom final
final = final[final_columns]

# Validasi hasil penggabungan
print("=" * 60)
print("VALIDASI DATASET FINAL")
print("=" * 60)

print("Jumlah baris:", len(final))
print("Jumlah provinsi unik:", final["provinsi"].nunique())
print("Jumlah kolom:", len(final.columns))

print("\nJumlah missing value:")
print(final.isna().sum()[final.isna().sum() > 0])

print("\nDaftar kolom final:")
print(final.columns.tolist())

assert len(final) == 38, "Jumlah provinsi tidak sesuai!"
assert final["provinsi"].nunique() == 38, "Ada provinsi duplikat!"
assert len(final.columns) == 30, "Jumlah kolom tidak sesuai!"

# Simpan dataset final
output_path = FINAL_DIR / "dashboard_pendidikan_final.csv"

final.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset final berhasil disimpan:")
print(output_path)

print("\nPreview:")
print(final.head().to_string(index=False))