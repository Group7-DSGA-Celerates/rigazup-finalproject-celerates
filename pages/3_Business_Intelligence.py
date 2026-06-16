import streamlit as st
import pandas as pd
from src.visualization import (
    load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, 
    format_currency, create_line_chart, create_bar_chart, create_donut_chart, render_kpi_card, render_insight_box
)
from src.validation import check_required_state
from src.preprocessing import generate_product_summary
from src.analysis import calculate_market_basket

st.set_page_config(page_title="Business Intelligence - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

check_required_state(["clean_data"])

df = st.session_state["clean_data"].copy()

# Auto-migrate legacy state cache to include new Cashflow & Lead Time features
if "Total_Keuntungan" not in df.columns:
    from src.preprocessing import clean_data
    df = clean_data(df)
    st.session_state["clean_data"] = df

# ================= FILTERS =================
st.sidebar.header("⚙️ Filter Dashboard")

min_date = df["Tanggal"].min().date()
max_date = df["Tanggal"].max().date()
date_range = st.sidebar.date_input("Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["Tanggal"].dt.date >= start_date) & (df["Tanggal"].dt.date <= end_date)]

available_years = sorted(df["Tahun"].dropna().unique().tolist())
selected_years = st.sidebar.multiselect("Tahun", available_years, default=available_years)
if selected_years:
    df = df[df["Tahun"].isin(selected_years)]

available_cats = sorted(df["Kategori"].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect("Kategori", available_cats, default=available_cats)
if selected_cats:
    df = df[df["Kategori"].isin(selected_cats)]

available_prods = sorted(df["Produk"].dropna().unique().tolist())
selected_prods = st.sidebar.multiselect("Produk", available_prods, default=[]) 
if selected_prods:
    df = df[df["Produk"].isin(selected_prods)]

render_page_header("Business Intelligence", "Pantau performa penjualan holistik dan performa spesifik setiap SKU dalam satu panel terpusat.")

if df.empty:
    st.warning("⚠️ Pilihan filter tidak menghasilkan data. Silakan ubah rentang waktu atau pilihan di sidebar.")
    st.stop()

# ================= GLOBAL STATE UPDATE =================
# Pastikan AI Insight Generator mendapatkan data product summary terbaru dari filter yang dipilih
product_summary = generate_product_summary(df)
st.session_state["product_summary"] = product_summary

# ================= GLOBAL KPI CARDS =================
total_sales = df["Total_Penjualan"].sum()
total_profit = df["Total_Keuntungan"].sum()
total_trx = df.shape[0]
total_qty = df["Qty_Terjual"].sum()

top_prod_sales = df.groupby("Produk")["Total_Penjualan"].sum()
top_product = top_prod_sales.idxmax() if not top_prod_sales.empty else "-"

top_cat_sales = df.groupby("Kategori")["Total_Penjualan"].sum()
top_category = top_cat_sales.idxmax() if not top_cat_sales.empty else "-"

col1, col2 = st.columns(2)
with col1:
    render_kpi_card("Total Omset", format_currency(total_sales), icon="💰")
with col2:
    render_kpi_card("Net Profit (Keuntungan)", format_currency(total_profit), icon="💸")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    render_kpi_card("Unit Terjual", f"{int(total_qty):,}".replace(",", "."), icon="📦")
with col4:
    render_kpi_card("Total Transaksi", f"{int(total_trx):,}".replace(",", "."), icon="🧾")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    render_kpi_card("Top Produk (Omset)", top_product, icon="🏆")
with col6:
    render_kpi_card("Top Kategori (Omset)", top_category, icon="👑")

st.markdown("<br>", unsafe_allow_html=True)

# ================= TAB SYSTEM =================
tab1, tab2, tab3 = st.tabs(["📊 Ringkasan Finansial", "📦 Analisis Produk", "🛒 Asosiasi Bundling (AI)"])

with tab1:
    st.markdown("### 📈 Tren Waktu")
    col_tren1, col_tren2 = st.columns(2)

    with col_tren1:
        with st.container(border=True):
            st.markdown("**Tren Total Penjualan Bulanan**")
            sales_per_month = df.groupby(["Tahun", "Bulan"])["Total_Penjualan"].sum().reset_index()
            sales_per_month["Bulan-Tahun"] = sales_per_month["Tahun"].astype(str) + "-" + sales_per_month["Bulan"].astype(str).str.zfill(2)
            sales_per_month = sales_per_month.sort_values(["Tahun", "Bulan"])
            sales_per_month.rename(columns={"Total_Penjualan": "Total Omset"}, inplace=True)
            fig_sales_month = create_line_chart(sales_per_month, "Bulan-Tahun", "Total Omset")
            st.plotly_chart(fig_sales_month, use_container_width=True)

    with col_tren2:
        with st.container(border=True):
            st.markdown("**Tren Unit Terjual Bulanan**")
            qty_per_month = df.groupby(["Tahun", "Bulan"])["Qty_Terjual"].sum().reset_index()
            qty_per_month["Bulan-Tahun"] = qty_per_month["Tahun"].astype(str) + "-" + qty_per_month["Bulan"].astype(str).str.zfill(2)
            qty_per_month = qty_per_month.sort_values(["Tahun", "Bulan"])
            qty_per_month.rename(columns={"Qty_Terjual": "Total Unit"}, inplace=True)
            fig_qty_month = create_line_chart(qty_per_month, "Bulan-Tahun", "Total Unit", line_color="#0EA5E9")
            st.plotly_chart(fig_qty_month, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Analisis Komposisi")
    col_cat1, col_cat2, col_cat3 = st.columns(3)

    with col_cat1:
        with st.container(border=True):
            st.markdown("**Penjualan per Tahun**")
            sales_per_year = df.groupby("Tahun")["Total_Penjualan"].sum().reset_index()
            sales_per_year.rename(columns={"Total_Penjualan": "Total Omset"}, inplace=True)
            fig_year = create_bar_chart(sales_per_year, "Tahun", "Total Omset")
            fig_year.update_xaxes(type='category')
            st.plotly_chart(fig_year, use_container_width=True)
        
    with col_cat2:
        with st.container(border=True):
            st.markdown("**Distribusi Revenue Kategori**")
            cat_sales = df.groupby("Kategori")["Total_Penjualan"].sum().reset_index()
            cat_sales.rename(columns={"Total_Penjualan": "Total Omset"}, inplace=True)
            fig_cat_sales = create_donut_chart(cat_sales, "Kategori", "Total Omset")
            st.plotly_chart(fig_cat_sales, use_container_width=True)

    with col_cat3:
        with st.container(border=True):
            st.markdown("**Distribusi Kuantitas Kategori**")
            cat_qty = df.groupby("Kategori")["Qty_Terjual"].sum().reset_index()
            cat_qty.rename(columns={"Qty_Terjual": "Total Unit"}, inplace=True)
            fig_cat_qty = create_donut_chart(cat_qty, "Kategori", "Total Unit")
            st.plotly_chart(fig_cat_qty, use_container_width=True)

with tab2:
    st.markdown("### 🏆 Peringkat SKU Terlaris")
    col_prod1, col_prod2 = st.columns(2)

    with col_prod1:
        with st.container(border=True):
            st.markdown("**Top 10 Produk (Total Omset)**")
            top_10_rev = product_summary.sort_values("total_penjualan", ascending=False).head(10).copy()
            top_10_rev.rename(columns={"total_penjualan": "Total Omset"}, inplace=True)
            fig_top_rev = create_bar_chart(top_10_rev, "Produk", "Total Omset", orientation='h')
            st.plotly_chart(fig_top_rev, use_container_width=True)
        
    with col_prod2:
        with st.container(border=True):
            st.markdown("**Top 10 Produk (Unit Terjual)**")
            top_10_qty = product_summary.sort_values("total_qty_terjual", ascending=False).head(10).copy()
            top_10_qty.rename(columns={"total_qty_terjual": "Unit Terjual"}, inplace=True)
            fig_top_qty = create_bar_chart(top_10_qty, "Produk", "Unit Terjual", orientation='h', color_seq=["#0EA5E9"])
            st.plotly_chart(fig_top_qty, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Tabel Performa Lengkap")
    with st.container(border=True):
        formatted_summary = product_summary.copy()
        formatted_summary["total_penjualan"] = formatted_summary["total_penjualan"].apply(lambda x: format_currency(x))
        formatted_summary.columns = ["Produk", "Kategori", "Total Unit Terjual", "Rata-rata Kuantitas", "Total Omset", "Total Modal", "Total Keuntungan", "Frekuensi Transaksi", "Lead Time", "Profit Margin (%)"]
        st.dataframe(formatted_summary, use_container_width=True)

with tab3:
    st.markdown("### 🛒 Deteksi Asosiasi Keranjang Belanja (Market Basket Analysis)")
    st.write("Algoritma deteksi asosiasi menelusuri nota transaksi untuk menemukan barang-barang yang sering dibeli secara bersamaan oleh pelanggan UMKM Anda.")
    
    with st.container(border=True):
        mba_df = calculate_market_basket(df, top_n=10)
        
        if mba_df.empty:
            st.warning("⚠️ Tidak ada asosiasi keranjang belanja yang kuat ditemukan pada data historis ini.")
        else:
            st.markdown("**Top 10 Rekomendasi Bundling / Cross-Selling**")
            st.dataframe(mba_df, use_container_width=True)
            
            top_pair = mba_df.iloc[0]
            render_insight_box(
                "Saran Taktis (Cross-Selling)", 
                f"Statistik membuktikan pelanggan sangat sering membeli **{top_pair['Produk A']}** dan **{top_pair['Produk B']}** secara bersamaan. "
                "Disarankan untuk menempatkan kedua produk ini bersebelahan di rak pajangan, atau membuat 'Promo Paket Spesial' untuk mengatrol omset secara instan.", 
                icon="💡"
            )
