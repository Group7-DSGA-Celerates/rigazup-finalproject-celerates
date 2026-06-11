import streamlit as st
from src.insight_generator import (
    generate_sales_insight,
    generate_product_insight,
    generate_stock_insight,
    generate_restock_insight
)
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, render_insight_box

st.set_page_config(page_title="AI Insight Generator - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Executive Summary", "Asisten naratif berbasis AI untuk menerjemahkan kompleksitas metrik ke dalam rangkuman strategis yang siap dibaca.")

from src.validation import check_required_state
check_required_state(["clean_data", "product_summary", "stock_summary", "restock_recommendation"])

df_clean = st.session_state["clean_data"]
df_prod = st.session_state["product_summary"]
df_stock = st.session_state["stock_summary"]
df_restock = st.session_state["restock_recommendation"]

# ================= KUMPULKAN KONTEKS DASAR =================
sales_insight = generate_sales_insight(df_clean)
product_insight = generate_product_insight(df_prod)
stock_insight = generate_stock_insight(df_stock)
restock_insight = generate_restock_insight(df_restock)

st.sidebar.markdown("---")
st.sidebar.header("🧠 Integrasi Gemini AI")
st.sidebar.caption("Gunakan kekuatan penalaran Generative AI gratis dari Google AI Studio.")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password", help="Dapatkan kunci gratis di aistudio.google.com")

st.markdown("Sistem menyaring titik data penjualan masa lampau dan proyeksi ke depan untuk mengukir ringkasan tindakan.")

if api_key:
    # pyrefly: ignore [missing-import]
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    st.info("Kunci API terdeteksi. Silakan tekan tombol di bawah untuk membangkitkan laporan eksekutif cerdas menggunakan Gemini AI.")
    if st.button("Generate Smart Insight (Gemini)", type="primary"):
        with st.spinner("Memanggil Gemini AI..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
Anda adalah analis bisnis senior dan ahli logistik dari platform bernama RIGAZUP.
Tugas Anda adalah merangkum data penjualan dan status inventaris ke dalam sebuah 'Executive Summary' yang profesional, ringkas, mudah dibaca, dan actionable (bisa langsung ditindaklanjuti).
Jangan membahas teknis kode atau database, bicaralah selayaknya konsultan bisnis ke direktur. 
Gunakan bahasa Indonesia baku yang mengalir, dan gunakan markdown (huruf tebal, bullet points, emoji yang elegan).

Berikut adalah kalkulasi data mentah (dari Rule-based engine internal) yang harus Anda elaborasi menjadi analisis komprehensif:

1. Performa Penjualan & Finansial: {sales_insight}
2. Keunggulan Produk: {product_insight}
3. Risiko Stok Gudang (Stockout/Overstock): {stock_insight}
4. Strategi Restock (Dari algoritma Machine Learning): {restock_insight}

Susun dalam format laporan dengan judul: "Laporan Eksekutif Analisis Logistik". Pisahkan ke dalam beberapa bab seperti:
- Sorotan Utama (Highlight)
- Evaluasi Risiko Inventaris
- Rekomendasi Pengadaan Cerdas

PENTING: Langsung mulai dari judul laporan. JANGAN tambahkan salam pembuka seperti "Kepada Bapak/Ibu Direktur" atau semacamnya.
                """
                response = model.generate_content(prompt)
                
                # Menggunakan desain Insight Box yang sama dengan Rule-Based
                render_insight_box("Analisis Eksekutif Gemini AI", response.text, icon="🤖")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memanggil Gemini API: {str(e)}")
else:
    st.warning("⚠️ Mode Klasik (Rule-Based): Masukkan API Key Gemini di sidebar untuk mengaktifkan AI Generatif.")
    with st.container(border=True):
        st.markdown("### 📋 Laporan Situasi Berjalan")
        render_insight_box("Analisis Omset Finansial", sales_insight, icon="💰")
        render_insight_box("Analisis Keunggulan SKU", product_insight, icon="🏆")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 🚨 Laporan Risiko & Aksi Mitigasi")
        render_insight_box("Pantauan Risiko Gudang", stock_insight, icon="⚠️")
        render_insight_box("Strategi Pengadaan Darurat", restock_insight, icon="🛒")
