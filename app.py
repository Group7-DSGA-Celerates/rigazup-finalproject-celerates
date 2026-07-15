import streamlit as st
from src.database import init_db, load_data_to_session

st.set_page_config(
    page_title="RIGAZUP - ML Inventory Planner",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Database
init_db()
load_data_to_session()

from src.database import render_demo_button

with st.sidebar:
    st.markdown("### 🎮 MODE DEMO")
    render_demo_button(key_prefix="sidebar_")
    st.markdown("<small>Data fiktif toko kelontong 1 tahun</small>", unsafe_allow_html=True)
    st.divider()

# Initialize Streamlit Navigation (v1.36+)
pages = {
    "Menu Utama": [
        st.Page("src/overview.py", title="RIGAZUP", icon="🏠", default=True),
        st.Page("pages/1_Upload_Dataset.py", title="Upload Data Historis", icon="📂"),
        st.Page("pages/1B_Input_Penjualan.py", title="Input Penjualan Baru", icon="🧾"),
        st.Page("pages/2_Data_Quality.py", title="Data Quality", icon="🔍"),
        st.Page("pages/3_BI_Dashboard.py", title="BI Dashboard", icon="📊"),
        st.Page("pages/4_AI_Forecaster.py", title="AI Forecaster", icon="🤖"),
        st.Page("pages/5_AI_Insights.py", title="AI Insights", icon="💡"),
        st.Page("pages/6_About.py", title="About RIGAZUP", icon="ℹ️"),
    ]
}

pg = st.navigation(pages)
pg.run()
