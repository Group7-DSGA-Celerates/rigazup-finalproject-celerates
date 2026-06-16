import streamlit as st
import pandas as pd
from src.validation import check_required_state
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, render_status_badge, render_kpi_card, render_insight_box
from src.restock import create_stock_summary, calculate_recommended_restock, determine_restock_priority, generate_restock_reason

st.set_page_config(page_title="Inventory Management - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()
check_required_state(["clean_data"])

render_page_header("Inventory Management", "Pemantauan ancaman krisis gudang dan rekomendasi pengadaan logistik otomatis berbasis AI.")

df = st.session_state["clean_data"].copy()

# Auto-migrate legacy state cache to include new Cashflow & Lead Time features
if "Lead_Time_Hari" not in df.columns:
    from src.preprocessing import clean_data
    df = clean_data(df)
    st.session_state["clean_data"] = df

# ================= GLOBAL STATE UPDATE =================
# Selalu generate stock_summary dari data yang fresh agar aman untuk AI Insight Generator
stock_summary = create_stock_summary(df)
st.session_state["stock_summary"] = stock_summary

# ================= KPI CARDS =================
total_products = len(stock_summary)
high_stockout = len(stock_summary[stock_summary["stockout_risk"] == "High"])
high_overstock = len(stock_summary[stock_summary["overstock_risk"] == "High"])

col1, col2, col3 = st.columns(3)
with col1:
    render_kpi_card("Produk Dipantau", str(total_products), icon="📦")
with col2:
    render_kpi_card("Risiko Stockout Tinggi", str(high_stockout), subtitle="Rawan kehabisan mendadak", icon="⚠️")
with col3:
    render_kpi_card("Risiko Overstock Tinggi", str(high_overstock), subtitle="Barang menumpuk lama", icon="📉")

st.markdown("<br>", unsafe_allow_html=True)

import io

def df_to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Helper function untuk format tabel
def highlight_risk(val):
    if val == "High":
        return 'color: #DC2626; font-weight: bold'
    elif val == "Medium":
        return 'color: #F59E0B; font-weight: bold'
    return 'color: #16A34A'

tab1, tab2 = st.tabs(["⚠️ Pantauan Risiko Gudang", "🛒 Saran Restock AI"])

with tab1:
    st.markdown("### Produk Rawan Habis (Stockout Risk)")
    st.markdown("Produk dengan stok terakhir menipis, namun memiliki intensitas penjualan dan jumlah unit terjual historis yang sangat tinggi.")
    
    with st.container(border=True):
        stockout_df = stock_summary.sort_values(
            by=["stockout_risk", "latest_stock"], 
            ascending=[False, True]
        )[["Produk", "Kategori", "latest_stock", "avg_qty_terjual", "transaction_count", "stockout_risk"]]
        
        display_stockout = stockout_df.copy()
        display_stockout.columns = ["Produk", "Kategori", "Sisa Stok", "Rata-rata Kuantitas Terjual", "Jumlah Transaksi", "Risiko Stockout"]
        
        st.dataframe(
            display_stockout.style.map(highlight_risk, subset=['Risiko Stockout']).format({
                "Sisa Stok": "{:,.0f}",
                "Rata-rata Kuantitas Terjual": lambda x: f"{x:g}",
                "Jumlah Transaksi": "{:,.0f}"
            }),
            use_container_width=True
        )
        
        excel_stockout = df_to_excel(display_stockout)
        st.download_button(
            label="⬇️ Export Data Stockout (Excel)",
            data=excel_stockout,
            file_name="RIGAZUP_Stockout_Risk.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Produk Kurang Laku (Overstock Risk)")
    st.markdown("Produk dengan persediaan di gudang berlimpah, namun frekuensi perputaran pembelinya sangat rendah.")
    
    with st.container(border=True):
        overstock_df = stock_summary.sort_values(
            by=["overstock_risk", "latest_stock"], 
            ascending=[False, False]
        )[["Produk", "Kategori", "latest_stock", "avg_qty_terjual", "transaction_count", "overstock_risk"]]
        
        display_overstock = overstock_df.copy()
        display_overstock.columns = ["Produk", "Kategori", "Sisa Stok", "Rata-rata Kuantitas Terjual", "Jumlah Transaksi", "Risiko Overstock"]
        
        st.dataframe(
            display_overstock.style.map(highlight_risk, subset=['Risiko Overstock']).format({
                "Sisa Stok": "{:,.0f}",
                "Rata-rata Kuantitas Terjual": lambda x: f"{x:g}",
                "Jumlah Transaksi": "{:,.0f}"
            }),
            use_container_width=True
        )
        
        excel_overstock = df_to_excel(display_overstock)
        st.download_button(
            label="⬇️ Export Data Overstock (Excel)",
            data=excel_overstock,
            file_name="RIGAZUP_Overstock_Risk.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with tab2:
    if "forecast_result" not in st.session_state:
        st.warning("⚠️ Data Prediksi AI belum tersedia. Silakan buka menu **4. AI Forecasting** dan eksekusi algoritma peramalan untuk melihat saran restock.")
    else:
        st.markdown("### Kalkulator Rekomendasi Pengadaan Logistik")
        forecast_df = st.session_state["forecast_result"].copy()
        
        st.sidebar.markdown("---")
        st.sidebar.header("⚙️ Konfigurasi Gudang (Restock)")
        
        # 1. Agregasi Forecast Demand 
        forecast_agg = forecast_df.groupby(["Produk", "Kategori"])["Predicted_Qty"].sum().reset_index()
        forecast_agg.rename(columns={"Predicted_Qty": "forecast_demand"}, inplace=True)
        
        # 2. Gabung Data 
        merged_df = pd.merge(
            stock_summary[["Produk", "Kategori", "latest_stock", "avg_qty_terjual", "lead_time_hari", "harga_modal"]], 
            forecast_agg, 
            on=["Produk", "Kategori"], 
            how="left"
        ).fillna({"forecast_demand": 0, "latest_stock": 0, "avg_qty_terjual": 0, "lead_time_hari": 3, "harga_modal": 0})
        
        merged_df.rename(columns={"latest_stock": "current_stock"}, inplace=True)
        
        # 3. Filter Sidebar
        available_cats = ["Semua Kategori"] + sorted(merged_df["Kategori"].dropna().unique().tolist())
        selected_cat = st.sidebar.selectbox("Filter Kategori", available_cats)
        
        if selected_cat != "Semua Kategori":
            prod_choices = merged_df[merged_df["Kategori"] == selected_cat]["Produk"].unique().tolist()
        else:
            prod_choices = merged_df["Produk"].unique().tolist()
        
        available_prods = ["Semua Produk"] + sorted(prod_choices)
        selected_prod = st.sidebar.selectbox("Filter Produk Spesifik", available_prods)
        
        # 4. Parameter Setting: Safety Stock
        safety_stock = st.sidebar.number_input("Limit Batas Aman (Safety Stock)", min_value=0, value=10, step=1)
        
        # Terapkan Filter
        filtered_df = merged_df.copy()
        if selected_cat != "Semua Kategori":
            filtered_df = filtered_df[filtered_df["Kategori"] == selected_cat]
        if selected_prod != "Semua Produk":
            filtered_df = filtered_df[filtered_df["Produk"] == selected_prod]
        
        if filtered_df.empty:
            st.warning("⚠️ Produk yang dipilih tidak memiliki data historis yang relevan.")
        else:
            # 5. Eksekusi Rumus Matematika
            filtered_df["safety_stock"] = safety_stock
            filtered_df["recommended_restock"] = filtered_df.apply(
                lambda r: calculate_recommended_restock(
                    r["forecast_demand"], 
                    r["current_stock"], 
                    r["safety_stock"],
                    r["avg_qty_terjual"],
                    r["lead_time_hari"]
                ), 
                axis=1
            )
            filtered_df["estimasi_modal"] = filtered_df["recommended_restock"] * filtered_df["harga_modal"]
            filtered_df["priority_level"] = filtered_df.apply(
                lambda r: determine_restock_priority(r["recommended_restock"], r["current_stock"], r["safety_stock"]), 
                axis=1
            )
            filtered_df["alasan_rekomendasi"] = filtered_df.apply(
                lambda r: generate_restock_reason(r["priority_level"], r["current_stock"], r["forecast_demand"]), 
                axis=1
            )
            
            # Simpan secara global untuk AI Insight Generator
            st.session_state["restock_recommendation"] = filtered_df
            
            if selected_prod != "Semua Produk":
                # Mode Fokus 1 Item
                from typing import cast
                row = cast(pd.DataFrame, filtered_df).iloc[0]
                st.markdown(f"#### 📦 {row['Produk']}")
                
                col_c1, col_c2, col_c3, col_c4 = st.columns(4)
                with col_c1:
                    render_kpi_card("Estimasi Terjual", f"{row['forecast_demand']:,.0f}", icon="📈")
                with col_c2:
                    render_kpi_card("Sisa Gudang", f"{row['current_stock']:,.0f}", icon="🏢")
                with col_c3:
                    render_kpi_card("Batas Aman", f"{row['safety_stock']}", icon="🛡️")
                with col_c4:
                    val = f"{row['recommended_restock']:,.0f}"
                    if row['recommended_restock'] > 0:
                        st.markdown(f"""
                        <div class="custom-kpi-card" style="border-left: 5px solid var(--danger);">
                            <div class="kpi-header"><p class="kpi-title">Rekomendasi Beli</p><div class="kpi-icon">🛒</div></div>
                            <h3 style="color: var(--danger); margin:0; font-size: 2.8rem;">{val}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        render_kpi_card("Rekomendasi Beli", val, icon="🛒")
                        
                st.markdown("<br>", unsafe_allow_html=True)
                render_insight_box("Analisis Sistem", f"**Prioritas {row['priority_level']}** — {row['alasan_rekomendasi']}", icon="🤖")

            else:
                # Mode Summary All
                high_priority = filtered_df[filtered_df["priority_level"] == "High"].shape[0]
                total_restock = filtered_df["recommended_restock"].sum()
                total_budget = filtered_df["estimasi_modal"].sum()
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    render_kpi_card("Darurat Restock (High Priority)", str(high_priority), subtitle="Item rawan kehabisan", icon="🚨")
                with c2:
                    render_kpi_card("Total Pembelian Eksekusi", f"{total_restock:,.0f} Unit", subtitle="Estimasi kuantitas belanja logistik", icon="🚚")
                with c3:
                    from src.visualization import format_currency
                    render_kpi_card("Estimasi Modal Restock", format_currency(total_budget), subtitle="Anggaran HPP wajib keluar", icon="💰")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- EARLY WARNING SYSTEM (Simulasi) ---
            with st.expander("📲 Kirim Peringatan Dini (WhatsApp)", expanded=False):
                if high_priority > 0:
                    urgent_items = filtered_df[filtered_df["priority_level"] == "High"]
                    wa_text = "🚨 *PERINGATAN DARURAT STOK BARANG* 🚨\n\nHalo, tolong segera lakukan pengadaan (restock) untuk barang-barang berikut sebelum kehabisan:\n\n"
                    import math
                    for _, urow in urgent_items.iterrows():
                        sisa_stok = int(urow['current_stock'])
                        butuh_stok = math.ceil(urow['recommended_restock'])
                        wa_text += f"- *{urow['Produk']}*: Sisa {sisa_stok} Unit (Butuh {butuh_stok} Unit)\n"
                    wa_text += "\nMohon segera diproses. Terima kasih! - _Sistem RIGAZUP_"
                    
                    st.info("Pesan otomatis telah dibuat berdasarkan data inventaris. Silakan salin (copy) teks di bawah ini dan kirimkan ke WhatsApp operasional atau supplier.")
                    st.code(wa_text, language="markdown")
                else:
                    st.success("🎉 Tidak ada produk dalam status darurat (High Priority). Gudang aman!")
                    
            st.markdown("<br>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown("### 📋 Daftar Transaksi Restock")
                
                display_cols = [
                    "Produk", "Kategori", "forecast_demand", "current_stock", 
                    "safety_stock", "recommended_restock", "estimasi_modal", "priority_level", "alasan_rekomendasi"
                ]
                df_view = filtered_df[display_cols].copy()
                
                rank_map = {"High": 1, "Medium": 2, "Low": 3}
                from typing import cast
                df_view_cast = cast(pd.DataFrame, df_view)
                df_view_cast["Rank"] = df_view_cast["priority_level"].map(rank_map)
                df_view = df_view_cast.sort_values(["Rank", "recommended_restock"], ascending=[True, False]).drop(columns=["Rank"])
                
                def format_risk_badge(val):
                    if val == "High": return "🔴 High"
                    elif val == "Medium": return "🟠 Medium"
                    else: return "🟢 Low"
                    
                df_view["priority_level"] = df_view["priority_level"].apply(format_risk_badge)
                
                df_view.columns = [
                    "Produk", "Kategori", "Estimasi Terjual", "Sisa Stok", 
                    "Batas Aman", "Wajib Beli", "Modal Keluar", "Prioritas", "Deskripsi Sistem"
                ]
                
                # Membulatkan nilai kuantitas ke atas (ceil) jika ada sisa desimal
                import math
                df_view["Sisa Stok"] = df_view["Sisa Stok"].apply(lambda x: int(x))
                df_view["Estimasi Terjual"] = df_view["Estimasi Terjual"].apply(lambda x: math.ceil(x))
                df_view["Wajib Beli"] = df_view["Wajib Beli"].apply(lambda x: math.ceil(x))
                
                # Format ke tampilan web: Rupiah untuk nominal, dan hapus desimal koma untuk unit barang
                from src.visualization import format_currency
                st.dataframe(
                    df_view.style.format({
                        "Modal Keluar": lambda x: format_currency(x),
                        "Sisa Stok": "{:,.0f}",
                        "Estimasi Terjual": "{:,.0f}",
                        "Wajib Beli": "{:,.0f}",
                        "Batas Aman": "{:,.0f}"
                    }), 
                    use_container_width=True
                )
                
                excel_restock = df_to_excel(df_view)
                st.download_button(
                    label="⬇️ Export Data Restock (Excel)",
                    data=excel_restock,
                    file_name="RIGAZUP_Restock_Logistik.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
