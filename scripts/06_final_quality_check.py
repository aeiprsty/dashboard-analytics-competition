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
print("Provinsi unik:", df["provinsi"].nunique())
print("Duplikasi provinsi:", df["provinsi"].duplicated().sum())
print("Duplikasi nama kolom:", df.columns.duplicated().sum())

assert len(df) == 38, "Jumlah baris tidak sesuai!"
assert df["provinsi"].nunique() == 38, "Jumlah provinsi unik tidak sesuai!"
assert not df["provinsi"].isna().any(), "Ada provinsi kosong!"
assert not df.columns.duplicated().any(), "Ada nama kolom duplikat!"

# Memastikan nama kolom sesuai standar dataset final
expected_columns = [
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

assert df.columns.tolist() == expected_columns, (
    "Nama atau urutan kolom tidak sesuai standar!"
)

print("Kesesuaian nama dan urutan kolom: Sesuai")

# 2. Pemeriksaan tipe data
print("\n2. PEMERIKSAAN TIPE DATA")
print("-" * 40)

print(df.dtypes.to_string())

# Kolom yang seharusnya numerik
numeric_columns = [
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
    "sd", "smp", "sma", "d1_d3", "s1_ke_atas",
    "total_distribusi_jenjang",
    "persentase_jenjang_dominan",
    "tidak_belum_pernah_sekolah",
    "masih_bersekolah",
    "tidak_sekolah_lagi",
    "total_distribusi_partisipasi",
    "persentase_kategori_dominan",
    "perkotaan",
    "perdesaan",
    "perkotaan_perdesaan",
    "selisih_kota_desa"
]

non_numeric = [
    col for col in numeric_columns
    if not pd.api.types.is_numeric_dtype(df[col])
]

print("Kolom numerik yang bermasalah:", non_numeric)
assert len(non_numeric) == 0, "Ada kolom numerik dengan tipe data tidak sesuai!"

# 3. Pemeriksaan nilai negatif
print("\n3. PEMERIKSAAN NILAI NEGATIF")
print("-" * 40)

negative_counts = (
    df[numeric_columns]
    .lt(0)
    .sum()
)

print(negative_counts[negative_counts > 0])

assert not (df[numeric_columns] < 0).any().any(), (
    "Ditemukan nilai negatif pada kolom numerik!"
)

# 4. Pemeriksaan rentang persentase
print("\n4. PEMERIKSAAN RENTANG PERSENTASE")
print("-" * 40)

percentage_columns = [
    "persentase_desa_4g_5g",
    "sd", "smp", "sma", "d1_d3", "s1_ke_atas",
    "persentase_jenjang_dominan",
    "tidak_belum_pernah_sekolah",
    "masih_bersekolah",
    "tidak_sekolah_lagi",
    "persentase_kategori_dominan",
    "perkotaan",
    "perdesaan",
    "perkotaan_perdesaan"
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

print(df["total_distribusi_jenjang"].describe())

assert df["total_distribusi_jenjang"].between(
    99.9, 100.1
).all(), "Total distribusi pendidikan tidak sesuai!"

# 6. Pemeriksaan total distribusi partisipasi
print("\n6. VALIDASI DISTRIBUSI PARTISIPASI")
print("-" * 40)

print(df["total_distribusi_partisipasi"].describe())

assert df["total_distribusi_partisipasi"].between(
    99.9, 100.1
).all(), "Total distribusi partisipasi tidak sesuai!"

# 7. Validasi konsistensi data sinyal
print("\n7. VALIDASI KONSISTENSI DATA SINYAL")
print("-" * 40)

signal_columns = [
    "desa_3g",
    "desa_2_5g",
    "desa_tanpa_sinyal",
    "desa_4g_5g"
]

expected_available = df[signal_columns].notna().sum(axis=1)

print(
    "Kesesuaian jumlah kategori:",
    (expected_available == df["jumlah_kategori_tersedia"]).all()
)

assert (
    expected_available == df["jumlah_kategori_tersedia"]
).all(), "Jumlah kategori sinyal tidak sesuai!"

complete_signal = df["total_desa"].notna()

print(
    "Provinsi dengan data sinyal lengkap:",
    complete_signal.sum()
)

print(
    "Selisih total terbesar pada provinsi lengkap:",
    df.loc[complete_signal, "selisih_total"].abs().max()
)

assert (
    df.loc[complete_signal, "selisih_total"] == 0
).all(), "Ditemukan selisih pada total kategori sinyal!"

# 8. Validasi perhitungan selisih perkotaan dan perdesaan
print("\n8. VALIDASI DATA PERKOTAAN DAN PERDESAAN")
print("-" * 40)

comparable = (
    df["perkotaan"].notna()
    & df["perdesaan"].notna()
)

calculated_difference = (
    df.loc[comparable, "perkotaan"]
    - df.loc[comparable, "perdesaan"]
)

difference_matches = (
    calculated_difference.round(2)
    == df.loc[comparable, "selisih_kota_desa"].round(2)
)

print("Provinsi yang dapat dibandingkan:", comparable.sum())
print("Selisih sesuai perhitungan:", difference_matches.all())

assert difference_matches.all(), (
    "Perhitungan selisih perkotaan dan perdesaan tidak sesuai!"
)

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

print("Seluruh pemeriksaan berhasil dilewati.")
print("Dataset siap digunakan untuk Power BI.")