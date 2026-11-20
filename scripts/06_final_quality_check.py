import pandas as pd
from pathlib import Path

# Direktori
BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_DIR = BASE_DIR / "data" / "final"

FILE_PATH = FINAL_DIR / "dashboard_pendidikan_final.csv"

df = pd.read_csv(FILE_PATH)

print("=" * 60)
print("FINAL QUALITY CHECK - DASHBOARD PENDIDIKAN")
print("=" * 60)

# 1. Pemeriksaan struktur dataset
print("\n1. PEMERIKSAAN STRUKTUR")
print("-" * 40)

print("Jumlah baris:", len(df))
print("Jumlah kolom:", len(df.columns))
print("Provinsi unik:", df["Provinsi"].nunique())
print("Duplikasi provinsi:", df["Provinsi"].duplicated().sum())
print("Duplikasi nama kolom:", df.columns.duplicated().sum())

assert len(df) == 38
assert df["Provinsi"].nunique() == 38
assert not df["Provinsi"].isna().any()
assert not df.columns.duplicated().any()

# 2. Pemeriksaan tipe data
print("\n2. PEMERIKSAAN TIPE DATA")
print("-" * 40)

print(df.dtypes.to_string())

# Kolom yang seharusnya numerik
numeric_columns = [
    "Desa_3G",
    "Desa_2_5G",
    "Desa_Tanpa_Sinyal",
    "Desa_4G_5G",
    "Jumlah_Kategori_Tersedia",
    "Total_Desa",
    "Desa_Dengan_Sinyal",
    "Persentase_Desa_4G_5G",
    "Total_Kategori",
    "Selisih_Total",
    "SD", "SMP", "SMA", "D1-D3", "S1 ke atas",
    "Total_Distribusi_Jenjang",
    "Persentase_Jenjang_Dominan",
    "Tidak/Belum Pernah Sekolah",
    "Masih Bersekolah",
    "Tidak Sekolah Lagi",
    "Total_Distribusi_Partisipasi",
    "Persentase_Kategori_Dominan",
    "Perkotaan",
    "Perdesaan",
    "Perkotaan+Perdesaan",
    "Selisih_Kota_Desa"
]

non_numeric = [
    col for col in numeric_columns
    if not pd.api.types.is_numeric_dtype(df[col])
]

print("Kolom numerik yang bermasalah:", non_numeric)
assert len(non_numeric) == 0

# 3. Pemeriksaan nilai negatif
print("\n3. PEMERIKSAAN NILAI NEGATIF")
print("-" * 40)

negative_counts = (
    df[numeric_columns]
    .lt(0)
    .sum()
)

print(negative_counts[negative_counts > 0])

assert not (df[numeric_columns] < 0).any().any()

# 4. Pemeriksaan rentang persentase
print("\n4. PEMERIKSAAN RENTANG PERSENTASE")
print("-" * 40)

percentage_columns = [
    "Persentase_Desa_4G_5G",
    "SD", "SMP", "SMA", "D1-D3", "S1 ke atas",
    "Persentase_Jenjang_Dominan",
    "Tidak/Belum Pernah Sekolah",
    "Masih Bersekolah",
    "Tidak Sekolah Lagi",
    "Persentase_Kategori_Dominan",
    "Perkotaan",
    "Perdesaan",
    "Perkotaan+Perdesaan"
]

for col in percentage_columns:
    minimum = df[col].min()
    maximum = df[col].max()

    print(f"{col}: {minimum:.2f} - {maximum:.2f}")

    assert df[col].dropna().between(0, 100).all(), (
        f"Persentase di luar rentang 0-100: {col}"
    )

# 5. Pemeriksaan total distribusi pendidikan
print("\n5. VALIDASI DISTRIBUSI PENDIDIKAN")
print("-" * 40)

print(df["Total_Distribusi_Jenjang"].describe())

assert df["Total_Distribusi_Jenjang"].between(
    99.9, 100.1
).all()

# 6. Pemeriksaan total distribusi partisipasi
print("\n6. VALIDASI DISTRIBUSI PARTISIPASI")
print("-" * 40)

print(df["Total_Distribusi_Partisipasi"].describe())

assert df["Total_Distribusi_Partisipasi"].between(
    99.9, 100.1
).all()

# 7. Validasi konsistensi data sinyal
print("\n7. VALIDASI KONSISTENSI DATA SINYAL")
print("-" * 40)

signal_columns = [
    "Desa_3G",
    "Desa_2_5G",
    "Desa_Tanpa_Sinyal",
    "Desa_4G_5G"
]

expected_available = df[signal_columns].notna().sum(axis=1)

print(
    "Kesesuaian jumlah kategori:",
    (expected_available == df["Jumlah_Kategori_Tersedia"]).all()
)

assert (
    expected_available == df["Jumlah_Kategori_Tersedia"]
).all()

complete_signal = df["Total_Desa"].notna()

print(
    "Provinsi dengan data sinyal lengkap:",
    complete_signal.sum()
)

print(
    "Selisih total seluruh provinsi lengkap:",
    df.loc[complete_signal, "Selisih_Total"].abs().max()
)

assert (
    df.loc[complete_signal, "Selisih_Total"] == 0
).all()

# 8. Validasi perhitungan selisih perkotaan dan perdesaan
print("\n8. VALIDASI DATA PERKOTAAN DAN PERDESAAN")
print("-" * 40)

comparable = df["Perkotaan"].notna() & df["Perdesaan"].notna()

calculated_difference = (
    df.loc[comparable, "Perkotaan"]
    - df.loc[comparable, "Perdesaan"]
)

difference_matches = (
    calculated_difference.round(2)
    == df.loc[comparable, "Selisih_Kota_Desa"].round(2)
)

print("Provinsi yang dapat dibandingkan:", comparable.sum())
print("Selisih sesuai perhitungan:", difference_matches.all())

assert difference_matches.all()

# 9. Pemeriksaan missing value
print("\n9. PEMERIKSAAN MISSING VALUE")
print("-" * 40)

missing = df.isna().sum()
print(missing[missing > 0])

print("\nTotal missing value:", missing.sum())

# 10. Hasil akhir
print("\n" + "=" * 60)
print("HASIL FINAL QUALITY CHECK")
print("=" * 60)

print("Seluruh pemeriksaan berhasil dilewati")
