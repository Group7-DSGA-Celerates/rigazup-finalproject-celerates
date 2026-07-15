import streamlit as st
import pandas as pd
import io
import time
from src.database import get_all_transactions, insert_bulk_transactions, load_data_to_session, clear_all_data
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, render_empty_state

st.set_page_config(page_title="Upload Data Historis - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("📂 Upload Data Historis", "Unggah file log transaksi (.csv) Anda untuk diimpor ke database. Ini melengkapi fitur Mode Kasir (input manual) untuk memuat data historis secara masal.")

REQUIRED_COLS = ['date', 'product_name', 'quantity_sold', 'unit_price']

# 1. Info jumlah data di database saat ini
current_db_df = st.session_state.get('uploaded_data', None)
if current_db_df is not None and not current_db_df.empty:
    total_db_rows = len(current_db_df)
    st.info(f"📊 **Status Database Saat Ini:** {total_db_rows:,} baris transaksi tersimpan.")
else:
    render_empty_state(
        "Database Kosong", 
        "Sistem membutuhkan data historis penjualan untuk melakukan analisis dan prediksi. Silakan unggah file CSV Anda atau gunakan Mode Kasir.",
        icon="📂"
    )

st.markdown("### 📥 Import Data Baru")
st.info(f"💡 Kolom wajib untuk file CSV: {', '.join(REQUIRED_COLS)}")

# Download template Excel
template_df = pd.DataFrame(columns=REQUIRED_COLS)
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    template_df.to_excel(writer, index=False, sheet_name='Sheet1')
template_excel = output.getvalue()

st.download_button(
    label="📥 Download Template Excel",
    data=template_excel,
    file_name="Template_Dataset_RIGAZUP.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    help="Gunakan template Excel ini (tabel rapi) untuk memastikan nama kolom sudah sesuai dengan format sistem baru."
)

st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Pilih file dataset (.csv / .xlsx)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
        
        if len(missing_cols) > 0:
            st.error(f"❌ Dataset tidak valid! Kolom wajib tidak ditemukan: **{', '.join(missing_cols)}**")
        else:
            st.success("✅ Dataset tervalidasi! Silakan cek preview di bawah sebelum mengimpor.")
            
            with st.container(border=True):
                st.markdown("### Preview Dataset yang Diunggah")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Total Baris:** {df.shape[0]:,}")
                    st.write(f"**Total Kolom:** {df.shape[1]}")
                with col2:
                    st.write("**Skema (Daftar Kolom):**")
                    st.write(", ".join(df.columns))
                    
                st.dataframe(df, use_container_width=True)
                
            if st.button("💾 Import ke Database", type="primary"):
                with st.spinner("Mengimpor data ke database..."):
                    # Insert to db (yang secara internal mengekstrak produk unik via INSERT OR IGNORE)
                    insert_bulk_transactions(df, source='csv')
                    load_data_to_session()
                    st.success("🎉 Dataset berhasil diimpor ke dalam database!")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
                    
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {str(e)}")

# Tampilkan preview database keseluruhan jika sudah ada data
if current_db_df is not None and not current_db_df.empty:
    st.markdown("---")
    st.markdown("### 🗄️ Preview Seluruh Data di Database")
    st.dataframe(current_db_df, use_container_width=True)

st.markdown("---")
st.warning("Menghapus dataset akan me-reset seluruh halaman analisis dan prediksi.")
if st.button("🗑️ Kosongkan Database (Reset Aplikasi)"):
    clear_all_data()
    load_data_to_session()
    st.rerun()
