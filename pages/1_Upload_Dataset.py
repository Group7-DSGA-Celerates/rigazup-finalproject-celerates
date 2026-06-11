import streamlit as st
import pandas as pd
from src.validation import get_required_columns, get_missing_columns, clear_dataset_state
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, render_empty_state

st.set_page_config(page_title="Upload Dataset - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Upload Dataset", "Unggah file log transaksi (.csv) Anda ke dalam memori sistem.")

if "raw_data" not in st.session_state:
    st.session_state["raw_data"] = None
if "dataset_ready" not in st.session_state:
    st.session_state["dataset_ready"] = False

if not st.session_state["dataset_ready"] or st.session_state["raw_data"] is None:
    render_empty_state(
        "Ruang Penyimpanan Kosong", 
        "Sistem membutuhkan data historis penjualan untuk melakukan analisis dan prediksi. Silakan unggah file CSV Anda.",
        icon="📂"
    )
    
    st.info(f"💡 Kolom wajib: {', '.join(get_required_columns())}")
    
    uploaded_file = st.file_uploader("Pilih file dataset.csv", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            missing_cols = get_missing_columns(df)
            
            if len(missing_cols) > 0:
                st.error(f"❌ Dataset tidak valid! Kolom tidak ditemukan: **{', '.join(missing_cols)}**")
            else:
                st.success("✅ Dataset tervalidasi! Menyimpan ke memori...")
                st.session_state["raw_data"] = df
                st.session_state["dataset_ready"] = True
                st.rerun()
                
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {str(e)}")

else:
    df = st.session_state["raw_data"]
    
    st.success("🎉 Dataset berhasil diunggah dan terkunci di dalam memori!")
    
    with st.container(border=True):
        st.markdown("### Metadata Dataset")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Total Baris:** {df.shape[0]:,}")
            st.write(f"**Total Kolom:** {df.shape[1]}")
        with col2:
            st.write("**Skema (Daftar Kolom):**")
            st.write(", ".join(df.columns.tolist()))
            
    st.markdown("### Preview Keseluruhan Data")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.warning("Menghapus dataset akan me-reset seluruh halaman analisis dan prediksi.")
    if st.button("🗑️ Hapus Dataset & Reset Aplikasi"):
        clear_dataset_state()
        st.rerun()
