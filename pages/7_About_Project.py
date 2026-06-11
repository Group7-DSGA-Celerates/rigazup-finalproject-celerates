import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header

st.set_page_config(page_title="About Project - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Tentang Proyek", "Informasi latar belakang, spesifikasi, dan susunan tim pembuat RIGAZUP.")

with st.container(border=True):
    st.markdown("""
    ### 📌 Nama Aplikasi
    **RIGAZUP: Forecasting Penjualan dan Restock Planner Berbasis Machine Learning**

    ---

    ### 📖 Latar Belakang
    Banyak pelaku usaha ritel yang sering mengalami kesulitan dalam menyeimbangkan persediaan barang di gudang. Kekurangan stok (*stockout*) menyebabkan hilangnya pendapatan yang signifikan, sedangkan penumpukan stok (*overstock*) menahan kas finansial dan merugikan manajemen penyusutan. **RIGAZUP** diarsiteki dengan DNA analitik data *Machine Learning* yang kokoh untuk menakar tingkat kesalahan stok serta menciptakan penjadwalan restock kuantitatif yang transparan.

    ---

    ### 🎯 Objektif Platform
    1. Memvisualisasikan sirkulasi penjualan riil melalui *Dashboard* reaktif.
    2. Mensimulasikan algoritma probabilitas prediksi/peramalan *demand* dengan AI.
    3. Merumuskan rekomendasi pemesanan logistik *(Restock)* otomatis harian yang tidak mengawang-awang.

    ---

    ### 📂 Profil Dataset
    Aplikasi diuji coba pada berkas masukan `dataset.csv` dengan struktur:
    - `Tanggal` *(Waktu transaksi)*
    - `Produk` *(Identitas unik SKU)*
    - `Kategori` *(Grup klasifikasi rak)*
    - `Qty_Terjual` *(Volume serapan)*
    - `Harga_Satuan` *(Eceran tertinggi)*
    - `Total_Penjualan` *(Arus kas / Omset)*
    - `Stok_Setelah_Transaksi` *(Arsip ketersediaan terakhir)*

    ---

    ### 💻 Teknologi & Algoritma Internal
    - **Ekosistem Aplikasi:** Python, Streamlit, Pandas, Plotly.
    - **Komponen ML Forecasting:** Linear Regression, Random Forest, XGBoost.
    - **Komponen Validasi Model:** MAE, RMSE, MAPE.

    ---

    ### 👥 Tim Arsitektur Sistem Kelompok 7
    Inovasi *Data Science* dan *Generative AI* ini direalisasikan atas kolaborasi dari:
    - **Rian Sholihan**
    - **Maulana Jalba Rizka**
    - **Muhammad Thorieq Alfareza**
    - **Ryan Ferdiansyah Risnayadi**
    - **Muhammad Danil Ma'ruf**
    """)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 RIGAZUP Team - All Rights Reserved.")
