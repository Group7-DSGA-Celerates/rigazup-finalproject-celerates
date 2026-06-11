import streamlit as st
from src.validation import check_required_state
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header
from src.preprocessing import clean_data

st.set_page_config(page_title="Data Quality - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()
check_required_state(["raw_data"])

render_page_header("Data Quality & Preprocessing", "Mesin pembersih otomatis untuk menyempurnakan struktur dataset sebelum dianalisis algoritma.")

df_raw = st.session_state["raw_data"]

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("### 📥 Profil Data Mentah")
        st.write(f"**Baris Awal:** {df_raw.shape[0]:,}")
        st.write(f"**Missing Values:** {df_raw.isna().sum().sum():,}")

with col2:
    with st.container(border=True):
        st.markdown("### 🧽 Pipeline Eksekusi")
        st.markdown("- Hapus baris bernilai kosong (NaN)")
        st.markdown("- Hapus transaksi abnormal (Qty Negatif)")
        st.markdown("- Ekstraksi komponen kalender (Tahun, Bulan, Hari)")

st.markdown("---")

if st.button("🚀 Eksekusi Preprocessing Engine"):
    with st.spinner("Memproses data..."):
        clean_df = clean_data(df_raw)
        st.session_state["clean_data"] = clean_df
        
    st.success("✅ Preprocessing selesai! Data siap dianalisis ke tahap selanjutnya.")
    
    with st.container(border=True):
        st.markdown("### 📤 Profil Data Bersih")
        colA, colB = st.columns(2)
        with colA:
            st.write(f"**Baris Tersisa:** {clean_df.shape[0]:,}")
        with colB:
            st.write(f"**Kolom Terbentuk:** {clean_df.shape[1]}")
            
    st.dataframe(clean_df.head(10), use_container_width=True)
elif "clean_data" in st.session_state:
    st.info("💡 Data bersih sudah tersedia di dalam memori sesesi aktif.")
    with st.container(border=True):
        st.markdown("### 📤 Profil Data Bersih")
        clean_df = st.session_state["clean_data"]
        st.write(f"**Baris Tersisa:** {clean_df.shape[0]:,}")
        st.dataframe(clean_df.head(5), use_container_width=True)
