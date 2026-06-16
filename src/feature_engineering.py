import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import cast, Tuple, Any

def prepare_sales_time_series(df: pd.DataFrame, product: str | None = None, category: str | None = None) -> pd.DataFrame:
    """
    Memfilter dan melakukan agregasi data series waktu harian per produk dan kategori.
    Target utama adalah Qty_Terjual.
    """
    df_filtered = df.copy()
    
    # 1. Filter berdasarkan produk dan kategori jika dipilih
    if product:
        df_filtered = df_filtered[df_filtered["Produk"] == product]
    if category:
        df_filtered = df_filtered[df_filtered["Kategori"] == category]
        
    if df_filtered.empty:
        return df_filtered
        
    # 2. Urutkan berdasarkan tanggal
    df_filtered = cast(pd.DataFrame, df_filtered.sort_values("Tanggal"))
    
    # 3. Agregasi harian per produk & kategori
    df_agg = df_filtered.groupby(["Tanggal", "Produk", "Kategori"]).agg({
        "Qty_Terjual": "sum",
        "Total_Penjualan": "sum",
        "Harga_Satuan": "mean",
        "Stok_Setelah_Transaksi": "last"
    }).reset_index()
    
    return cast(pd.DataFrame, df_agg)

def create_forecasting_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membuat fitur forecasting (lag, rolling windows) dan fitur waktu berbasis kalender.
    """
    if df.empty:
        return df
        
    df_feat = df.copy()
    
    # Pastikan data diurutkan berdasarkan produk lalu tanggal agar fitur lag benar berurut
    df_feat = cast(pd.DataFrame, df_feat.sort_values(by=["Produk", "Tanggal"]))
    
    # Fitur waktu (wajib numeric numerik untuk ML)
    dates = pd.to_datetime(df_feat["Tanggal"])
    dates_any = cast(Any, dates.dt)
    df_feat["Tahun"] = dates_any.year
    df_feat["Bulan"] = dates_any.month
    df_feat["Hari"] = dates_any.day
    df_feat["day_of_week"] = dates_any.dayofweek
    
    # Fitur pendeteksi musim / kalender (Sangat penting untuk Linear Regression)
    df_feat["is_weekend"] = (dates_any.dayofweek >= 5).astype(int)
    df_feat["is_month_start"] = dates_any.is_month_start.astype(int)
    df_feat["is_month_end"] = dates_any.is_month_end.astype(int)
    
    # Event-Based Features (Siklus UMKM & Gajian)
    df_feat["is_payday"] = ((dates_any.day >= 25) | (dates_any.day <= 2)).astype(int) # Efek gajian
    df_feat["is_mid_month"] = ((dates_any.day >= 14) & (dates_any.day <= 16)).astype(int)
    
    # Fitur Time Series (Lag & Rolling Window) yang dihitung spesifik per Produk
    df_feat["lag_1"] = df_feat.groupby("Produk")["Qty_Terjual"].shift(1)
    df_feat["lag_7"] = df_feat.groupby("Produk")["Qty_Terjual"].shift(7)
    
    # Gunakan shift(1) sebelum rolling agar tidak bocor (data leakage) dan tidak menghasilkan NaN saat Qty_Terjual masa depan kosong
    df_feat["rolling_mean_7"] = df_feat.groupby("Produk")["Qty_Terjual"].transform(lambda x: x.shift(1).rolling(7).mean())
    df_feat["rolling_mean_14"] = df_feat.groupby("Produk")["Qty_Terjual"].transform(lambda x: x.shift(1).rolling(14).mean())
    
    # Hapus baris dengan missing value akibat pergeseran lag/rolling awal, tapi JANGAN hapus jika Qty_Terjual (Target) yang NaN
    feature_cols = ["lag_1", "lag_7", "rolling_mean_7", "rolling_mean_14"]
    df_feat = df_feat.dropna(subset=feature_cols)
    
    return cast(pd.DataFrame, df_feat)

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengubah variabel kategorikal (Teks) menjadi numerik agar siap dipakai Machine Learning.
    Menggunakan One-Hot Encoding agar Linear Regression bisa membedakan setiap produk.
    """
    if df.empty:
        return df
        
    # Buat salinan dan konversi kolom Produk & Kategori menjadi dummy variables (0/1)
    dummies = pd.get_dummies(df[["Produk", "Kategori"]], drop_first=False)
    dummies = dummies.astype(int) # Pastikan formatnya numerik, bukan boolean
    
    # Gabungkan dengan dataframe asli (kolom asli tetap dipertahankan untuk UI)
    df_encoded = pd.concat([df, dummies], axis=1)
        
    return cast(pd.DataFrame, df_encoded)

def split_features_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Memisahkan dataset menjadi X (Fitur Prediktor) dan y (Target Aktual = Qty_Terjual).
    """
    if df.empty:
        return pd.DataFrame(), pd.Series(dtype=float)
        
    # Buang target dan kolom non-numerik yang tidak dapat diolah model
    # Buang juga fitur yang mengandung data leakage (Total_Penjualan, Harga_Satuan, Stok_Setelah_Transaksi)
    drop_cols = [
        "Qty_Terjual", "Tanggal", "Produk", "Kategori", "Nama_Hari", 
        "Total_Penjualan", "Harga_Satuan", "Stok_Setelah_Transaksi"
    ]
    
    # Filter hanya kolom drop_cols yang masih ada di dataframe
    cols_to_drop = [col for col in drop_cols if col in df.columns]
    
    X = df.drop(columns=cols_to_drop)
    y = df["Qty_Terjual"]
    
    return X, y
