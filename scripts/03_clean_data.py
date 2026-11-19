import pandas as pd
from pathlib import Path

# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# STANDARDISASI NAMA PROVINSI
# ==========================================

PROVINCES = {
    "ACEH": "Aceh",
    "SUMATERA UTARA": "Sumatera Utara",
    "SUMATERA BARAT": "Sumatera Barat",
    "RIAU": "Riau",
    "JAMBI": "Jambi",
    "SUMATERA SELATAN": "Sumatera Selatan",
    "BENGKULU": "Bengkulu",
    "LAMPUNG": "Lampung",
    "KEP. BANGKA BELITUNG": "Kepulauan Bangka Belitung",
    "KEPULAUAN BANGKA BELITUNG": "Kepulauan Bangka Belitung",
    "KEP. RIAU": "Kepulauan Riau",
    "KEPULAUAN RIAU": "Kepulauan Riau",
    "DKI JAKARTA": "DKI Jakarta",
    "JAWA BARAT": "Jawa Barat",
    "JAWA TENGAH": "Jawa Tengah",
    "DI YOGYAKARTA": "DI Yogyakarta",
    "JAWA TIMUR": "Jawa Timur",
    "BANTEN": "Banten",
    "BALI": "Bali",
    "NUSA TENGGARA BARAT": "Nusa Tenggara Barat",
    "NUSA TENGGARA TIMUR": "Nusa Tenggara Timur",
    "KALIMANTAN BARAT": "Kalimantan Barat",
    "KALIMANTAN TENGAH": "Kalimantan Tengah",
    "KALIMANTAN SELATAN": "Kalimantan Selatan",
    "KALIMANTAN TIMUR": "Kalimantan Timur",
    "KALIMANTAN UTARA": "Kalimantan Utara",
    "SULAWESI UTARA": "Sulawesi Utara",
    "SULAWESI TENGAH": "Sulawesi Tengah",
    "SULAWESI SELATAN": "Sulawesi Selatan",
    "SULAWESI TENGGARA": "Sulawesi Tenggara",
    "GORONTALO": "Gorontalo",
    "SULAWESI BARAT": "Sulawesi Barat",
    "MALUKU": "Maluku",
    "MALUKU UTARA": "Maluku Utara",
    "PAPUA BARAT": "Papua Barat",
    "PAPUA BARAT DAYA": "Papua Barat Daya",
    "PAPUA": "Papua",
    "PAPUA SELATAN": "Papua Selatan",
    "PAPUA TENGAH": "Papua Tengah",
    "PAPUA PEGUNUNGAN": "Papua Pegunungan",
}

def standardize_province(series):
    return series.astype("string").str.strip().str.upper().map(PROVINCES)


# ==========================================
# LOAD TABEL 7
# ==========================================

def clean_sinyal():
    df = pd.read_csv(
        RAW_DIR / "tabel_07_sinyal.csv",
        encoding="utf-8-sig"
    )

    df = df.rename(columns={
        df.columns[0]: "Provinsi",
        df.columns[1]: "Desa_3G",
        df.columns[2]: "Desa_2_5G",
        df.columns[3]: "Desa_Tanpa_Sinyal",
        df.columns[4]: "Desa_4G_5G"
    })

    df["Provinsi"] = standardize_province(df["Provinsi"])

    df = df.dropna(subset=["Provinsi"]).copy()

    numeric_cols = [
        "Desa_3G",
        "Desa_2_5G",
        "Desa_Tanpa_Sinyal",
        "Desa_4G_5G"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df[["Provinsi"] + numeric_cols]


# ==========================================
# LOAD TABEL 13, 14, DAN 25
# ==========================================

def clean_other_table(filename, columns):
    df = pd.read_csv(
        RAW_DIR / filename,
        encoding="utf-8-sig",
        header=2
    )

    df = df.rename(columns={
        df.columns[0]: "Provinsi"
    })

    df["Provinsi"] = standardize_province(df["Provinsi"])

    # Hanya mempertahankan 38 provinsi
    df = df.dropna(subset=["Provinsi"]).copy()

    # Konversi nilai menjadi numerik
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df[["Provinsi"] + columns]


# ==========================================
# MAIN PROCESS
# ==========================================

def main():

    datasets = {
        "sinyal_clean.csv": clean_sinyal(),

        "akses_jenjang_clean.csv": clean_other_table(
            "tabel_13_akses_jenjang.csv",
            ["SD", "SMP", "SMA", "D1-D3", "S1 ke atas"]
        ),

        "partisipasi_clean.csv": clean_other_table(
            "tabel_14_partisipasi.csv",
            [
                "Tidak/Belum Pernah Sekolah",
                "Masih Bersekolah",
                "Tidak Sekolah Lagi"
            ]
        ),

        "komputer_clean.csv": clean_other_table(
            "tabel_25_komputer.csv",
            ["Perkotaan", "Perdesaan", "Perkotaan+Perdesaan"]
        )
    }

    for filename, df in datasets.items():

        # Validasi jumlah provinsi
        assert len(df) == 38, (
            f"{filename}: jumlah baris bukan 38, "
            f"melainkan {len(df)}"
        )

        # Validasi duplikasi
        assert df["Provinsi"].is_unique, (
            f"{filename}: terdapat provinsi duplikat"
        )

        # Validasi missing value
        print("\n" + "=" * 50)
        print(f"FILE: {filename}")
        print("=" * 50)
        print("Jumlah baris:", len(df))
        print("Jumlah kolom:", len(df.columns))
        print("Missing value:\n", df.isnull().sum())

        # Simpan hasil
        df.to_csv(
            OUTPUT_DIR / filename,
            index=False,
            encoding="utf-8-sig"
        )

if __name__ == "__main__":
    main()
