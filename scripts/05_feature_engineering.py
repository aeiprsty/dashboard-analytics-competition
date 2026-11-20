import pandas as pd
from pathlib import Path

# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(PROCESSED_DIR / "sinyal_clean.csv")

# ==========================================
# FEATURE ENGINEERING
# ==========================================

# Total desa dengan data sinyal yang lengkap
signal_columns = [
    "Desa_3G",
    "Desa_2_5G",
    "Desa_Tanpa_Sinyal",
    "Desa_4G_5G"
]

# Jumlah kategori yang memiliki nilai
df["Jumlah_Kategori_Tersedia"] = df[signal_columns].notna().sum(axis=1)

# Total desa hanya dihitung jika seluruh kategori tersedia
df["Total_Desa"] = df[signal_columns].sum(axis=1, min_count=4)

# Jumlah desa yang memiliki sinyal
signal_available = [
    "Desa_3G",
    "Desa_2_5G",
    "Desa_4G_5G"
]

df["Desa_Dengan_Sinyal"] = df[signal_available].sum(
    axis=1,
    min_count=3
)

# Persentase desa dengan sinyal 4G/5G
df["Persentase_Desa_4G_5G"] = (
    df["Desa_4G_5G"] / df["Total_Desa"] * 100
)

# ==========================================
# VALIDASI KONSISTENSI
# ==========================================

df["Total_Kategori"] = (
    df["Desa_Dengan_Sinyal"] + df["Desa_Tanpa_Sinyal"]
)

df["Selisih_Total"] = df["Total_Desa"] - df["Total_Kategori"]

print("\nVALIDASI KONSISTENSI DATA")
print("=" * 60)

print(df[[
    "Provinsi",
    "Total_Desa",
    "Total_Kategori",
    "Selisih_Total"
]].to_string(index=False))

# ==========================================
# VALIDASI
# ==========================================

print("\nHASIL FEATURE ENGINEERING SINYAL")
print("=" * 60)

print(df[[
    "Provinsi",
    "Jumlah_Kategori_Tersedia",
    "Total_Desa",
    "Desa_Dengan_Sinyal",
    "Persentase_Desa_4G_5G"
]].to_string(index=False))

print("\nJumlah missing value:")
print(df[[
    "Total_Desa",
    "Desa_Dengan_Sinyal",
    "Persentase_Desa_4G_5G"
]].isna().sum())

# ==========================================
# SIMPAN HASIL
# ==========================================

output_file = OUTPUT_DIR / "sinyal_feature.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nFile berhasil disimpan: {output_file}")

# ==========================================
# FEATURE ENGINEERING AKSES JENJANG
# ==========================================

df_jenjang = pd.read_csv(
    PROCESSED_DIR / "akses_jenjang_clean.csv"
)

education_columns = [
    "SD",
    "SMP",
    "SMA",
    "D1-D3",
    "S1 ke atas"
]

# Menghitung total distribusi
df_jenjang["Total_Distribusi"] = df_jenjang[
    education_columns
].sum(axis=1)

# Menentukan jenjang pendidikan dengan persentase terbesar
df_jenjang["Jenjang_Dominan"] = df_jenjang[
    education_columns
].idxmax(axis=1)

# Mengambil persentase dari jenjang dominan
df_jenjang["Persentase_Jenjang_Dominan"] = df_jenjang[
    education_columns
].max(axis=1)

# ==========================================
# VALIDASI AKSES JENJANG
# ==========================================

print("\nHASIL FEATURE ENGINEERING AKSES JENJANG")
print("=" * 60)

print(df_jenjang[[
    "Provinsi",
    "Total_Distribusi",
    "Jenjang_Dominan",
    "Persentase_Jenjang_Dominan"
]].to_string(index=False))

print("\nPemeriksaan total distribusi:")
print("Minimum:", df_jenjang["Total_Distribusi"].min())
print("Maksimum:", df_jenjang["Total_Distribusi"].max())

print("\nJumlah missing value:")
print(df_jenjang.isnull().sum())

# ==========================================
# SIMPAN HASIL AKSES JENJANG
# ==========================================

output_file = OUTPUT_DIR / "akses_jenjang_feature.csv"

df_jenjang.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nFile berhasil disimpan: {output_file}")


# ==========================================
# FEATURE ENGINEERING PARTISIPASI SEKOLAH
# ==========================================

df_partisipasi = pd.read_csv(
    PROCESSED_DIR / "partisipasi_clean.csv"
)

participation_columns = [
    "Tidak/Belum Pernah Sekolah",
    "Masih Bersekolah",
    "Tidak Sekolah Lagi"
]

# Menghitung total distribusi
df_partisipasi["Total_Distribusi"] = df_partisipasi[
    participation_columns
].sum(axis=1)

# Menentukan kategori partisipasi dengan persentase terbesar
df_partisipasi["Kategori_Dominan"] = df_partisipasi[
    participation_columns
].idxmax(axis=1)

# Mengambil persentase dari kategori dominan
df_partisipasi["Persentase_Kategori_Dominan"] = df_partisipasi[
    participation_columns
].max(axis=1)

# ==========================================
# VALIDASI PARTISIPASI SEKOLAH
# ==========================================

print("\nHASIL FEATURE ENGINEERING PARTISIPASI SEKOLAH")
print("=" * 60)

print(df_partisipasi[[
    "Provinsi",
    "Total_Distribusi",
    "Kategori_Dominan",
    "Persentase_Kategori_Dominan"
]].to_string(index=False))

print("\nPemeriksaan total distribusi:")
print("Minimum:", df_partisipasi["Total_Distribusi"].min())
print("Maksimum:", df_partisipasi["Total_Distribusi"].max())

print("\nJumlah missing value:")
print(df_partisipasi.isnull().sum())

# ==========================================
# SIMPAN HASIL PARTISIPASI SEKOLAH
# ==========================================

output_file = OUTPUT_DIR / "partisipasi_feature.csv"

df_partisipasi.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nFile berhasil disimpan: {output_file}")



# ==========================================
# FEATURE ENGINEERING KEPEMILIKAN KOMPUTER
# ==========================================

df_komputer = pd.read_csv(
    PROCESSED_DIR / "komputer_clean.csv"
)

computer_columns = [
    "Perkotaan",
    "Perdesaan",
    "Perkotaan+Perdesaan"
]

# Menghitung selisih kepemilikan komputer perkotaan dan perdesaan
df_komputer["Selisih_Kota_Desa"] = (
    df_komputer["Perkotaan"] - df_komputer["Perdesaan"]
)

# Menentukan wilayah dengan persentase kepemilikan komputer lebih tinggi
df_komputer["Wilayah_Lebih_Tinggi"] = df_komputer.apply(
    lambda row: (
        "Perkotaan"
        if pd.notna(row["Perkotaan"])
        and pd.notna(row["Perdesaan"])
        and row["Perkotaan"] > row["Perdesaan"]
        else (
            "Perdesaan"
            if pd.notna(row["Perkotaan"])
            and pd.notna(row["Perdesaan"])
            and row["Perdesaan"] > row["Perkotaan"]
            else (
                "Sama"
                if pd.notna(row["Perkotaan"])
                and pd.notna(row["Perdesaan"])
                else "Tidak dapat dibandingkan"
            )
        )
    ),
    axis=1
)

# ==========================================
# VALIDASI KEPEMILIKAN KOMPUTER
# ==========================================

print("\nHASIL FEATURE ENGINEERING KEPEMILIKAN KOMPUTER")
print("=" * 60)

print(df_komputer[[
    "Provinsi",
    "Perkotaan",
    "Perdesaan",
    "Perkotaan+Perdesaan",
    "Selisih_Kota_Desa",
    "Wilayah_Lebih_Tinggi"
]].to_string(index=False))

print("\nJumlah missing value:")
print(df_komputer.isnull().sum())

print("\nStatistik deskriptif:")
print(df_komputer[computer_columns].describe())

# ==========================================
# SIMPAN HASIL KEPEMILIKAN KOMPUTER
# ==========================================

output_file = OUTPUT_DIR / "komputer_feature.csv"

df_komputer.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nFile berhasil disimpan: {output_file}")

