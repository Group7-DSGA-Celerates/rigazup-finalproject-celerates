import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header

st.set_page_config(page_title="About Project - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Tentang Proyek", "Informasi latar belakang, spesifikasi sistem, dan susunan tim pengembang RIGAZUP.")

with st.container(border=True):
    st.markdown("""
    ### 🚀 RIGAZUP: Sistem ERP & AI Forecaster
    
    **RIGAZUP** adalah *dashboard* berbasis web yang dirancang khusus untuk membantu pelaku bisnis ritel dan UMKM dalam mengelola arus kas, memantau kondisi persediaan barang (stok), serta memprediksi tren penjualan di masa depan menggunakan bantuan *Machine Learning*.

    ---

    ### 💡 Latar Belakang Proyek
    Banyak pengusaha ritel yang sering mengalami kesulitan dalam menyeimbangkan persediaan barang di gudang. Di satu sisi, kekurangan barang (*stockout*) menyebabkan hilangnya potensi pendapatan. Namun di sisi lain, kelebihan barang (*overstock*) dapat menahan modal dan meningkatkan risiko barang rusak. 
    
    Oleh karena itu, RIGAZUP dikembangkan untuk menjembatani ketidakpastian logistik tersebut secara matematis. Aplikasi ini menggantikan pendekatan *feeling* atau tebak-tebakan dengan analisis data yang konkret dan akurat.

    ---

    ### ✨ Fitur Utama Aplikasi
    1. **Data Quality Studio:** Pembersihan data otomatis dari *missing values* serta pendeteksian anomali data ekstrem guna memastikan dataset yang akan diproses oleh AI dalam kondisi bersih dan reliabel.
    2. **Business Intelligence Dashboard:** Memantau indikator kinerja bisnis (KPI) secara terpusat, mulai dari tren omset, peringkat produk paling laris, hingga komposisi kategori penjualan, yang disajikan melalui grafik interaktif.
    3. **AI Forecasting:** Mesin prediktif cerdas (*Machine Learning*) yang meramalkan estimasi kuantitas permintaan barang di masa depan menggunakan kombinasi algoritma unggulan seperti *XGBoost*, *Random Forest*, dan *Linear Regression*.
    4. **Inventory Management & Restock Planner:** Mengkalkulasi batas *Safety Stock* harian dan memberikan peringatan dini terhadap risiko barang habis (*Stockout*) atau penumpukan barang di gudang (*Overstock*), sekaligus merekomendasikan jumlah belanja logistik.
    5. **AI Insight Generator:** Sistem asisten virtual analitik yang otomatis menerjemahkan grafik dan angka numerik menjadi sebuah narasi ringkasan eksekutif yang deskriptif dan strategis.
    6. **Model Comparison:** Transparansi performa di balik layar, memungkinkan pengguna membandingkan secara ilmiah tingkat keakuratan masing-masing algoritma prediksi melalui evaluasi metrik *Mean Absolute Error* (MAE) dan *Root Mean Square Error* (RMSE).

    ---

    ### 📂 Kebutuhan Data
    Aplikasi ini beroperasi menggunakan *file* data `dataset.csv` sederhana dari sistem kasir POS yang mencakup: `Tanggal`, `Produk`, `Kategori`, `Qty_Terjual`, `Harga_Satuan`, `Total_Penjualan`, dan `Stok_Setelah_Transaksi`. 
    
    *(Catatan: Jika data Harga Pokok Penjualan tidak tersedia, sistem memiliki fungsi bawaan untuk mengestimasi margin keuntungan secara otomatis).*

    ---

    ### 🛠️ Teknologi Pendukung
    - **Bahasa & Antarmuka:** Python, Streamlit
    - **Pengolahan Data:** Pandas, Numpy
    - **Visualisasi:** Plotly
    - **Algoritma Machine Learning:** Linear Regression, Random Forest, XGBoost

    ---

    ### 👨‍💻 Tim Pengembang (Kelompok 7)
    Proyek sains data dan kecerdasan buatan ini dikembangkan secara kolaboratif oleh mahasiswa **Universitas Negeri Surabaya**:
    
    * **Rian Sholihan** (NIM: 23051204384)
    * **Maulana Jalba Rizka** (NIM: 23051204369)
    * **Muhammad Thorieq Alfareza** (NIM: 23051204363)
    * **Ryan Ferdiansyah Risnayadi** (NIM: 23051204302)
    * **Muhammad Danil Ma'ruf** (NIM: 23051204290)
    """)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 RIGAZUP Team - Universitas Negeri Surabaya. All Rights Reserved.")
