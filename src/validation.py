import pandas as pd
import streamlit as st

def get_required_columns() -> list:
    """Mengembalikan list berisi 7 kolom wajib."""
    return [
        "Tanggal",
        "Produk",
        "Kategori",
        "Qty_Terjual",
        "Harga_Satuan",
        "Total_Penjualan",
        "Stok_Setelah_Transaksi"
    ]

def get_missing_columns(df: pd.DataFrame) -> list:
    """Mengembalikan list kolom yang kurang dari dataframe."""
    required = get_required_columns()
    return [col for col in required if col not in df.columns]

def validate_required_columns(df: pd.DataFrame) -> bool:
    """Mengecek apakah seluruh kolom wajib ada di dataframe."""
    return len(get_missing_columns(df)) == 0

def clear_dataset_state():
    """
    Fungsi sentral untuk menyapu bersih semua data state dari memori
    saat user memutuskan menghapus dataset.
    """
    keys_to_remove = [
        "raw_data",
        "dataset_ready",
        "clean_data",
        "product_summary",
        "stock_summary",
        "forecast_result",
        "best_model",
        "model_evaluation",
        "restock_recommendation"
    ]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

def check_required_state(required_keys: list):
    """
    Mengecek apakah session_state yang dibutuhkan sudah tersedia.
    Jika belum, akan menampilkan warning terstruktur dan menghentikan eksekusi halaman.
    Sistem mengecek dependensi secara otomatis (hierarchy).
    """
    dependencies = {
        "restock_recommendation": ["stock_summary", "forecast_result"],
        "forecast_result": ["clean_data"],
        "model_evaluation": ["clean_data"],
        "best_model": ["clean_data"],
        "stock_summary": ["clean_data"],
        "product_summary": ["clean_data"],
        "clean_data": ["raw_data"]
    }
    
    # 1. Bentuk set penuh (resolving dependencies berantai)
    full_requirements = set(required_keys)
    added = True
    while added:
        added = False
        for key in list(full_requirements):
            if key in dependencies:
                for dep in dependencies[key]:
                    if dep not in full_requirements:
                        full_requirements.add(dep)
                        added = True
                        
    # 2. Cari mana state yang bolong / tidak ada
    missing = [key for key in full_requirements if key not in st.session_state or st.session_state[key] is None]
    
    if not missing:
        return True
        
    # 3. Tampilkan pesan kesalahan dari tingkatan yang paling akar (root issue)
    if "raw_data" in missing:
        st.warning("⚠️ Dataset mentah belum tersedia. Silakan unggah `dataset.csv` Anda di menu **1. Upload Dataset** terlebih dahulu.")
        st.stop()
        
    if "clean_data" in missing:
        st.warning("⚠️ Dataset belum dibersihkan. Silakan jalankan *preprocessing* di menu **2. Data Quality**.")
        st.stop()
        
    if "stock_summary" in missing:
        st.warning("⚠️ Data risiko stok belum diproses. Silakan buka menu **5. Inventory Management** untuk mengekstrak riwayat perputaran gudang.")
        st.stop()
        
    if "product_summary" in missing:
        st.warning("⚠️ Data analisis produk belum siap. Silakan buka menu **3. Business Intelligence** terlebih dahulu.")
        st.stop()
        
    if "forecast_result" in missing or "model_evaluation" in missing or "best_model" in missing:
        st.warning("💡 Hasil peramalan (*Forecasting*) Machine Learning belum tersedia. Silakan jalankan simulasi algoritma di menu **4. AI Forecasting**.")
        st.stop()
        
    if "restock_recommendation" in missing:
        st.warning("💡 Jadwal dan kuantitas rekomendasi belanja belum diformulasikan. Silakan proses di menu **5. Inventory Management** terlebih dahulu.")
        st.stop()
