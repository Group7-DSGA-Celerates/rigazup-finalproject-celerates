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
check_required_state(["clean_data", "product_summary", "forecast_result", "model_evaluation"])

df_clean = st.session_state["clean_data"]
df_prod = st.session_state["product_summary"]

best_name = st.session_state.get("best_model_name", "AI Model")
mape_score = "N/A"
if "model_evaluation" in st.session_state:
    eval_df = st.session_state["model_evaluation"]
    best_row = eval_df[eval_df["model_name"] == best_name]
    if not best_row.empty:
        mape_score = f"{best_row['MAPE'].values[0]:.2f}%"

# ================= KUMPULKAN KONTEKS DASAR =================
sales_insight = generate_sales_insight(df_clean)
product_insight = generate_product_insight(df_prod)

st.sidebar.markdown("---")
st.sidebar.header("🧠 Integrasi Gemini AI")
st.sidebar.caption("Gunakan kekuatan penalaran Generative AI gratis dari Google AI Studio.")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password", help="Dapatkan kunci gratis di aistudio.google.com")

st.markdown("Sistem menyaring titik data penjualan masa lampau dan proyeksi ke depan untuk mengukir ringkasan tindakan.")

if api_key:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    st.info("Kunci API terdeteksi. Silakan tekan tombol di bawah untuk membangkitkan laporan eksekutif cerdas menggunakan Gemini AI.")
    if st.button("Generate Smart Insight (Gemini)", type="primary"):
        with st.spinner("Memanggil Gemini AI..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
Anda adalah analis sistem dan ahli logistik dari platform bernama RIGAZUP.
Tugas Anda adalah merangkum data penjualan dan status inventaris ke dalam sebuah 'Executive Summary' yang profesional, ringkas, mudah dibaca, dan actionable (bisa langsung ditindaklanjuti).
Jangan membahas teknis kode atau database, bicaralah selayaknya laporan profesional. 
Gunakan bahasa Indonesia baku yang mengalir, dan gunakan markdown (huruf tebal, bullet points, emoji yang elegan).

ATURAN KETAT:
1. JANGAN gunakan sapaan personal atau gender seperti "Bapak/Ibu", "Kakak", "Halo", dll. Gunakan sapaan universal "Anda" jika diperlukan.
2. JANGAN gunakan kata "komputer", "tebakan", "AI", "bot", atau merujuk bahwa narasi ini dikerjakan oleh kecerdasan buatan. Sebut entitas analisis ini sebagai "sistem" atau "algoritma".
3. Jaga nada bicara (tone) agar terdengar analitis, berwibawa, dan seratus persen objektif (bukan seperti chatbot).

Berikut adalah kalkulasi data mentah yang harus Anda elaborasi menjadi analisis komprehensif:

1. Performa Penjualan & Finansial: {sales_insight}
2. Keunggulan Produk: {product_insight}
3. Evaluasi Performa AI: Model peramalan masa depan menggunakan algoritma {best_name} dengan skor Error (MAPE) sebesar {mape_score}.

Susun dalam format laporan dengan judul: "Laporan Eksekutif Analisis Penjualan & Proyeksi". Pisahkan ke dalam 3 bab utama berikut:
- Sorotan Utama (Highlight Finansial & Operasional)
- Strategi Promosi & Bundling (Berikan ide taktis cross-selling dengan mengawinkan produk Best-Seller agar stok cepat habis)
- Proyeksi & Tingkat Kepercayaan Keputusan (Berikan opini analitis apakah proyeksi ini bisa diandalkan berdasarkan skor MAPE {mape_score})

PENTING: Langsung mulai dari judul laporan.
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
