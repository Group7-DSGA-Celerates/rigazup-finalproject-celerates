import streamlit as st
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle

st.set_page_config(page_title="About RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

st.title("ℹ️ About RIGAZUP")

st.markdown("""
## 📦 RIGAZUP — ML-Powered Smart Inventory Planner

### 📋 Deskripsi Proyek
RIGAZUP adalah aplikasi perencanaan inventaris cerdas berbasis Machine Learning 
yang dirancang khusus untuk UMKM (Usaha Mikro, Kecil, dan Menengah) di Indonesia.
Aplikasi ini membantu pemilik bisnis mengelola stok barang secara otomatis 
menggunakan prediksi AI dan memberikan rekomendasi reorder point yang optimal.

### 👨‍💻 Pengembang
| Nama | NIM | Program Studi | Fakultas | Universitas |
|---|---|---|---|---|
| **Rian Sholihan** | 23051204384 | S1 Teknik Informatika | Fakultas Teknik | Universitas Negeri Surabaya |

### ✨ Fitur Utama
- 📂 Upload data historis via CSV
- 🧾 Mode kasir untuk input transaksi harian
- 💬 Catat nota cepat dengan bahasa natural (AI-powered)
- 📊 Dashboard Business Intelligence interaktif
- 🤖 AI Forecasting dengan 4 model ML
- 💡 AI Insights menggunakan Google Gemini
- 🎮 Data demo untuk onboarding instan

### 🛠️ Technology Stack
- **Backend:** Python, Pandas, NumPy
- **Frontend:** Streamlit
- **ML:** Scikit-Learn, XGBoost
- **AI:** Google Gemini API
- **Visualisasi:** Plotly
- **Database:** SQLite
""")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 RIGAZUP — Developed by Rian Sholihan. All Rights Reserved.")
