import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_feature_card

# 1. Terapkan Tema dan CSS Global
load_css()
apply_theme()
render_sidebar_theme_toggle()

# 2. Render Hero Section (Custom HTML)
st.markdown("""
<div class="hero-container">
    <h1>RIGAZUP</h1>
    <p class="subtitle">Forecasting Penjualan dan Restock Planner Berbasis Machine Learning</p>
    <p class="desc">Aplikasi cerdas untuk membantu UMKM menganalisis penjualan, memprediksi demand masa depan, dan menentukan rekomendasi pengadaan logistik berbasis data secara mutakhir.</p>
</div>
""", unsafe_allow_html=True)

# 3. Mini Workflow (Steps)
st.markdown("### 🚦 Alur Kerja Sistem")
wf_cols = st.columns(5)
steps = [
    ("1️⃣ Upload Dataset", "Unggah data historis (CSV)"),
    ("2️⃣ Data Quality", "Pembersihan & validasi"),
    ("3️⃣ Dashboard", "Visualisasi performa"),
    ("4️⃣ Forecasting", "Prediksi AI masa depan"),
    ("5️⃣ Restock Planner", "Rekomendasi belanja")
]

for i, col in enumerate(wf_cols):
    with col:
        with st.container(border=True):
            st.markdown(f"**{steps[i][0]}**<br><span style='color:var(--text-secondary); font-size:0.85rem;'>{steps[i][1]}</span>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Render Value Proposition Cards
st.markdown("### ✨ Menu Utama Platform")

col1, col2 = st.columns(2)
with col1:
    render_feature_card("Dashboard Penjualan", "Akses KPI interaktif dan tren pendapatan dari waktu ke waktu.", icon="📊")
    render_feature_card("Stock Risk Monitoring", "Deteksi dini terhadap ancaman stockout & tumpukan overstock.", icon="🚨")
    render_feature_card("Model Comparison", "Transparansi kompetisi 3 algoritma Machine Learning.", icon="⚖️")
    render_feature_card("AI Insight Generator", "Eksekutif ringkasan naratif dari keseluruhan metrik.", icon="🤖")

with col2:
    render_feature_card("Product Analysis", "Temukan kategori dan produk penyumbang omset terbesar.", icon="🏆")
    render_feature_card("Forecasting Penjualan", "Algoritma prediktif (XGBoost, RF, Linear Regression) beraksi.", icon="🧠")
    render_feature_card("Restock Planner", "Rekomendasi jumlah pengadaan stok berdasarkan Safety Stock.", icon="📦")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 📋 Persyaratan Dataset")
    st.markdown("Agar terhindar dari bias prediksi, aplikasi ini secara ketat hanya dapat memproses data transaksional dengan **7 Kolom Wajib** berikut:")
    cols = ["Tanggal", "Produk", "Kategori", "Qty_Terjual", "Harga_Satuan", "Total_Penjualan", "Stok_Setelah_Transaksi"]
    st.code(", ".join(cols), language="text")
