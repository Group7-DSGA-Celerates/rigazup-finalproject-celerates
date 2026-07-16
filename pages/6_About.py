import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle

st.set_page_config(page_title="About RIGAZUP", layout="wide")
load_css()
apply_theme()
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_b64 = get_base64_image("assets/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 3.5rem; margin-right: 15px; vertical-align: middle;">'

st.markdown(f"""
<div style='text-align: center; padding-top: 1rem; padding-bottom: 3rem;'>
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 0;">
        {logo_html}
        <h1 style='font-size: 3.5rem; font-weight: 800; margin-bottom: 0; background: -webkit-linear-gradient(45deg, #0EA5E9, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>RIGAZUP</h1>
    </div>
    <h3 style='color: #64748b; font-weight: 400; margin-top: 0.5rem; font-size: 1.5rem;'>AI-Powered Smart Retail & Forecasting Platform</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 📋 Deskripsi Proyek")
    st.info(
        "**RIGAZUP** adalah aplikasi perencanaan inventaris cerdas berbasis *Machine Learning* "
        "yang dirancang khusus untuk UMKM (Usaha Mikro, Kecil, dan Menengah) di Indonesia. "
        "Aplikasi ini membantu pemilik bisnis mengelola stok barang secara otomatis "
        "menggunakan prediksi algoritma AI untuk meramalkan tren penjualan di masa depan."
    )
    
    st.markdown("#### ✨ Fitur Utama")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
        - 📂 **Ekstraksi Data:** Upload dataset CSV massal
        - 🧾 **Sistem POS:** Mode kasir untuk input harian
        - 🤖 **NLP Engine:** Input nota pakai bahasa natural
        - 📊 **BI Dashboard:** Analisis data interaktif
        """)
    with col_f2:
        st.markdown("""
        - 📈 **AI Forecaster:** Prediksi dengan 4 Model ML
        - 🧠 **Gen-AI Insights:** Kesimpulan otomatis Gemini
        - 🛒 **Market Basket:** Deteksi bundling otomatis
        - 🎮 **Demo Mode:** Onboarding instan 1-klik
        """)

with col2:
    st.markdown("#### 👨‍💻 Profil Pengembang")
    with st.container(border=True):
        st.markdown("### Rian Sholihan")
        st.markdown("**NIM:** 23051204384")
        st.markdown("**Program Studi:** S1 Teknik Informatika")
        st.markdown("**Fakultas:** Teknik")
        st.markdown("**Universitas:** Universitas Negeri Surabaya")

st.markdown("---")
st.markdown("#### 🛠️ Technology Stack")

col_t1, col_t2, col_t3, col_t4 = st.columns(4)
with col_t1:
    st.success("**Backend & Data**\n- Python 3.12\n- Pandas\n- NumPy\n- SQLite3")
with col_t2:
    st.info("**Machine Learning**\n- Scikit-Learn\n- XGBoost\n- Statsmodels")
with col_t3:
    st.warning("**Frontend & UI**\n- Streamlit\n- Plotly Graph Objects\n- CSS Animations")
with col_t4:
    st.error("**Generative AI**\n- Google Gemini API\n- Natural Language Processing")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 RIGAZUP — Developed by Rian Sholihan. All Rights Reserved.")
