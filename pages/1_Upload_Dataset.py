import streamlit as st
import pandas as pd
import io
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
        "Sistem membutuhkan data historis penjualan untuk melakukan analisis dan prediksi. Silakan unggah file Excel/CSV Anda.",
        icon="📂"
    )
    
    st.info(f"💡 Kolom wajib: {', '.join(get_required_columns())}")
    
    # Download template Excel
    template_df = pd.DataFrame(columns=get_required_columns())
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        template_df.to_excel(writer, index=False, sheet_name='Sheet1')
    template_excel = output.getvalue()
    
    st.download_button(
        label="📥 Download Template Excel",
        data=template_excel,
        file_name="Template_Dataset_RIGAZUP.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Gunakan template Excel ini (tabel rapi) untuk memastikan nama kolom sudah sesuai dengan format sistem."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Pilih file dataset (.csv / .xlsx)", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
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
            # Format UI columns to remove underscores and abbreviations
            ui_cols = [col.replace("_", " ").replace("Qty", "Kuantitas") for col in df.columns]
            st.write(", ".join(ui_cols))
            
    st.markdown("### Preview Keseluruhan Data")
    display_df = df.copy()
    display_df.columns = ui_cols
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    st.warning("Menghapus dataset akan me-reset seluruh halaman analisis dan prediksi.")
    if st.button("🗑️ Hapus Dataset & Reset Aplikasi"):
        clear_dataset_state()
        st.rerun()
