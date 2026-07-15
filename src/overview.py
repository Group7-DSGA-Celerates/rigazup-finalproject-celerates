import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_feature_card

# 1. Terapkan Tema dan CSS Global
load_css()
apply_theme()
render_sidebar_theme_toggle()

# 2. Render Hero Section (Custom HTML)
from streamlit_theme import st_theme

theme = st_theme()
is_dark = True
if theme and theme.get("base") == "light":
    is_dark = False

if is_dark:
    st.markdown("""
    <div class="hero-container-dark">
        <h1>RIGAZUP</h1>
        <p class="subtitle">Forecasting Penjualan dan Restock Planner Berbasis Machine Learning</p>
        <p class="desc">Aplikasi cerdas untuk membantu UMKM menganalisis penjualan, memprediksi demand masa depan, dan menentukan rekomendasi pengadaan logistik berbasis data secara mutakhir.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-container-light">
        <h1>RIGAZUP</h1>
        <p class="subtitle">Forecasting Penjualan dan Restock Planner Berbasis Machine Learning</p>
        <p class="desc">Aplikasi cerdas untuk membantu UMKM menganalisis penjualan, memprediksi demand masa depan, dan menentukan rekomendasi pengadaan logistik berbasis data secara mutakhir.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Mini Workflow (Steps)
st.markdown("### 🚦 Alur Kerja Sistem")
wf_cols1 = st.columns(3)
wf_cols2 = st.columns(3)
steps = [
    ("1️⃣ Input Data (Kasir/Upload/Demo)", "Sumber data masuk"),
    ("2️⃣ Data Quality Studio", "Pembersihan & deteksi anomali"),
    ("3️⃣ Business Intelligence", "Visualisasi performa KPI"),
    ("4️⃣ AI Forecasting", "Prediksi demand masa depan"),
    ("5️⃣ AI Insight Generator", "Ringkasan eksekutif via Gemini"),
    ("6️⃣ Export & Laporan", "Aksi keputusan logistik")
]

for i, col in enumerate(wf_cols1):
    with col:
        with st.container(border=True):
            st.markdown(f"**{steps[i][0]}**<br><span style='color:var(--text-secondary); font-size:0.85rem;'>{steps[i][1]}</span>", unsafe_allow_html=True)

for i, col in enumerate(wf_cols2):
    with col:
        with st.container(border=True):
            st.markdown(f"**{steps[i+3][0]}**<br><span style='color:var(--text-secondary); font-size:0.85rem;'>{steps[i+3][1]}</span>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Demo Button Section ---
from src.database import render_demo_button
with st.container(border=True):
    st.markdown("### 🎮 Baru pertama kali? Coba langsung!")
    st.markdown("Dataset berisi data penjualan fiktif toko kelontong selama 1 tahun. Anda bisa langsung mencoba semua fitur!")
    render_demo_button(key_prefix="landing_")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Render Value Proposition Cards
st.markdown("### ✨ Modul Utama Platform")

col1, col2 = st.columns(2)
with col1:
    render_feature_card("Mode Kasir & Data Demo", "Input transaksi manual harian atau manfaatkan 1 klik Data Demo simulasi untuk langsung mencoba semua fitur.", icon="🧾")
    render_feature_card("Data Quality Studio", "Pembersihan dataset otomatis, penanganan missing values, dan deteksi anomali harga.", icon="🧹")
    render_feature_card("Business Intelligence", "Visualisasi interaktif tren omset, analisis kategori produk, dan pemantauan KPI secara real-time.", icon="📊")

with col2:
    render_feature_card("Catat Nota AI (NLP)", "Tidak perlu repot input manual, cukup ketik bahasa kasual dan Gemini AI akan mengekstraknya ke database.", icon="🤖")
    render_feature_card("AI Forecasting", "Prediksi omset dan permintaan barang di masa depan dengan algoritma Machine Learning.", icon="📈")
    render_feature_card("AI Insight Generator", "Narasi cerdas Gemini yang merangkum kondisi kesehatan bisnis layaknya asisten analis data pribadi.", icon="💡")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### 📋 Persyaratan Dataset")
    st.markdown("Agar terhindar dari bias prediksi, fitur Upload CSV secara ketat hanya memproses **4 Kolom Wajib** berikut:")
    cols = ["date", "product_name", "quantity_sold", "unit_price"]
    st.code(", ".join(cols), language="text")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--text-secondary); font-size: 0.9rem;'>
    <p>© 2026 RIGAZUP — Developed by Rian Sholihan</p>
    <p>S1 Teknik Informatika • Universitas Negeri Surabaya</p>
</div>
""", unsafe_allow_html=True)
