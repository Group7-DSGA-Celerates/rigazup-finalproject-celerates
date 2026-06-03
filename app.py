import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Forecasting Penjualan & Restock Planner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Forecasting Penjualan & Restock Planner")

st.markdown("""
Aplikasi ini digunakan untuk membantu analisis data penjualan,
melakukan forecasting penjualan, memberikan rekomendasi restock,
serta menghasilkan insight otomatis menggunakan AI.

### Fitur Utama
- 📊 Dashboard Penjualan
- 📈 Forecasting Penjualan
- 📦 Restock Planner
- 💀 AI Insight Generator

Silakan upload dataset penjualan terlebih dahulu sebelum menggunakan fitur lainnya.
""")

st.divider()

if "df" in st.session_state:

    st.subheader("Preview Dataset")

    st.dataframe(
        st.session_state.df.head(),
        width='stretch'
    )

    if st.button("🗑️ Hapus Dataset"):

        del st.session_state.df
        st.rerun()

else:

    st.header("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Pilih file CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            required_columns = [
                'Tanggal',
                'Produk',
                'Kategori',
                'Qty_Terjual',
                'Harga_Satuan',
                'Total_Penjualan',
                'Stok_Setelah_Transaksi'
            ]

            missing_columns = []

            for col in required_columns:
                if col not in df.columns:
                    missing_columns.append(col)

            if missing_columns:

                st.error(
                    f"❌ Kolom tidak sesuai. Kolom yang tidak ditemukan: {', '.join(missing_columns)}"
                )

            else:

                st.session_state.df = df

                st.success("✅ Dataset berhasil dimuat.")

                st.subheader("Preview Dataset")

                st.dataframe(
                    df.head(),
                    width='stretch'
                )

        except Exception as e:

            st.error("❌ Gagal membaca file CSV.")
            st.error(str(e))

    else:

        st.warning(
            "⚠️ Silakan upload dataset terlebih dahulu untuk menggunakan seluruh fitur aplikasi."
        )
