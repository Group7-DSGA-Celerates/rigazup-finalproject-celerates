import pandas as pd
from typing import cast, Any

def convert_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Mengubah kolom Tanggal ke tipe datetime."""
    df_clean = df.copy()
    df_clean["Tanggal"] = pd.to_datetime(df_clean["Tanggal"], errors="coerce")
    return df_clean

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Membuat kolom fitur waktu berdasarkan kolom Tanggal."""
    df_clean = df.copy()
    dates = pd.to_datetime(df_clean["Tanggal"])
    dates_any = cast(Any, dates.dt)
    df_clean["Tahun"] = dates_any.year
    df_clean["Bulan"] = dates_any.month
    df_clean["Hari"] = dates_any.day
    df_clean["Nama_Hari"] = dates_any.day_name()
    return df_clean

def check_data_quality(df: pd.DataFrame) -> dict:
    """Mengecek kualitas data dari df mentah."""
    quality = {}
    
    # Missing values
    quality["missing_values"] = df.isnull().sum().to_dict()
    quality["total_missing"] = df.isnull().sum().sum()
    
    # Duplicates
    quality["duplicates"] = df.duplicated().sum()
    
    # Anomali Negatif
    numeric_columns = ["Qty_Terjual", "Harga_Satuan", "Total_Penjualan", "Stok_Setelah_Transaksi"]
    for col in numeric_columns:
        if col in df.columns:
            # Konversi sementara ke numerik untuk mengecek jika ada yang negatif
            numeric_col = cast(pd.Series, pd.to_numeric(df[col], errors="coerce"))
            quality[f"negative_{col}"] = cast(Any, numeric_col < 0).sum()
        else:
            quality[f"negative_{col}"] = 0
            
    # Validasi format Tanggal
    if "Tanggal" in df.columns:
        parsed_dates = pd.to_datetime(df["Tanggal"], errors="coerce")
        quality["invalid_dates"] = parsed_dates.isnull().sum()
    else:
        quality["invalid_dates"] = 0
        
    return quality

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Melakukan pipeline data cleaning penuh."""
    df_clean = df.copy()
    
    # 1. Hapus data duplikat
    df_clean = df_clean.drop_duplicates()
    
    # 2. Convert Tanggal
    df_clean = convert_date_column(df_clean)
    
    # 3. Pastikan kolom numerik benar formatnya
    numeric_cols = ["Qty_Terjual", "Harga_Satuan", "Total_Penjualan", "Stok_Setelah_Transaksi"]
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        
    # 4. Tangani missing value (drop baris yang kolom wajibnya null)
    required_cols = ["Tanggal", "Produk", "Kategori"] + numeric_cols
    df_clean = df_clean.dropna(subset=required_cols)
    
    # 5. Hapus nilai negatif
    for col in numeric_cols:
        df_clean = df_clean[df_clean[col] >= 0]
        
    # 6. Buat fitur waktu
    df_clean = create_time_features(df_clean)
    
    # 7. Buat kolom hitungan
    df_clean["Total_Penjualan_Hitung"] = df_clean["Qty_Terjual"] * df_clean["Harga_Satuan"]
    df_clean["Selisih_Total_Penjualan"] = df_clean["Total_Penjualan"] - df_clean["Total_Penjualan_Hitung"]
    
    return df_clean

def generate_product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Mengagregasi data untuk mendapatkan ringkasan performa per produk."""
    summary = df.groupby(["Produk", "Kategori"]).agg(
        total_qty_terjual=("Qty_Terjual", "sum"),
        rata_rata_qty=("Qty_Terjual", "mean"),
        total_penjualan=("Total_Penjualan", "sum"),
        frekuensi_transaksi=("Tanggal", "count")
    ).reset_index()
    return summary
