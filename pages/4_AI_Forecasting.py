import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle, render_page_header, render_kpi_card, render_insight_box
from src.feature_engineering import (
    prepare_sales_time_series, 
    create_forecasting_features, 
    encode_categorical_features, 
    split_features_target
)
from src.modeling import (
    prepare_train_test_data, 
    train_models, 
    predict_models, 
    select_best_model
)
from src.evaluation import evaluate_predictions

st.set_page_config(page_title="Forecasting - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Forecasting Penjualan", "Simulasi AI prediktif untuk meninjau estimasi tren permintaan (demand) harian secara otomatis.")

from src.validation import check_required_state
check_required_state(["clean_data"])

df_clean = st.session_state["clean_data"].copy()

st.sidebar.header("⚙️ Konfigurasi AI")

# 1. Pilihan Kategori dan Produk (Saling berkaitan)
available_cats = ["Semua Kategori"] + sorted(df_clean["Kategori"].dropna().unique().tolist())
selected_cat = st.sidebar.selectbox("Pilih Kategori", available_cats)

if selected_cat != "Semua Kategori":
    prod_choices = df_clean[df_clean["Kategori"] == selected_cat]["Produk"].dropna().unique().tolist()
else:
    prod_choices = df_clean["Produk"].dropna().unique().tolist()

available_prods = ["Semua Produk"] + sorted(prod_choices)
selected_prod = st.sidebar.selectbox("Pilih Produk", available_prods)

# 2. Input Periode Target Masa Depan
import datetime
import numpy as np

last_date_db = df_clean["Tanggal"].max()
min_allowed_date = last_date_db + datetime.timedelta(days=1)
default_target_date = min_allowed_date + datetime.timedelta(days=13)

target_date = st.sidebar.date_input("Target Tanggal Akhir Forecast", min_value=min_allowed_date, value=default_target_date)
forecast_period = (pd.to_datetime(target_date).date() - last_date_db.date()).days

if st.sidebar.button("🚀 Eksekusi Forecasting"):
    if forecast_period <= 0:
        st.error("❌ Tanggal target harus melebihi tanggal data terakhir.")
        st.stop()
        
    with st.spinner("Menyiapkan pipeline data historis..."):
        cat_filter = selected_cat if selected_cat != "Semua Kategori" else None
        prod_filter = selected_prod if selected_prod != "Semua Produk" else None
        
        df_ts = prepare_sales_time_series(df_clean, product=prod_filter, category=cat_filter)
        
        if df_ts.empty or len(df_ts) < 20:
            st.error("❌ Data mentah tidak mencukupi untuk melakukan pelatihan model algoritma yang valid. Harap pilih produk yang memiliki historis lebih panjang.")
            st.stop()
            
        df_features = create_forecasting_features(df_ts)
        df_encoded = encode_categorical_features(df_features)
        
        if df_encoded.empty or len(df_encoded) < 15:
            st.error("❌ Dataset mengalami deplesi akibat komputasi jeda waktu (Lagging/Rolling). Tidak cukup data untuk diproses lanjut.")
            st.stop()
            
        df_ml = df_encoded.copy()
        tanggal_index = df_ml["Tanggal"].copy() 
        X, y = split_features_target(df_ml)
        
        # Fase Ujian (Evaluasi Internal) - Menggunakan 20% data akhir
        unique_dates = sorted(tanggal_index.unique())
        test_days = max(1, int(len(unique_dates) * 0.2))
        test_start_date = unique_dates[-test_days]
        test_mask = tanggal_index >= test_start_date
        
        X_train, X_test = X[~test_mask], X[test_mask]
        y_train, y_test = y[~test_mask], y[test_mask]
        
    with st.spinner("Menguji Kompetisi Model AI..."):
        try:
            trained_models = train_models(X_train, y_train)
            if not trained_models:
                st.error("❌ Mesin gagal mengekstrak struktur pohon keputusan. Batalkan proses.")
                st.stop()
                
            predictions = predict_models(trained_models, X_test)
            eval_df = evaluate_predictions(y_test, predictions)
            
            best_model_name, best_model_raw = select_best_model(eval_df, trained_models)
            
            if best_model_raw is None:
                st.error("❌ Gagal menemukan model terbaik.")
                st.stop()
                
            from typing import Any, cast
            best_model = cast(Any, best_model_raw)
            
            st.session_state["model_evaluation"] = eval_df
            st.session_state["best_model"] = best_model
            st.session_state["best_model_name"] = best_model_name
            
        except Exception as e:
            st.error(f"❌ Terjadi anomali pada fase Ujian: {str(e)}")
            st.stop()
            
    with st.spinner(f"Memprediksi Masa Depan Asli dengan {best_model_name}... (Ini bisa memakan waktu)"):
        try:
            # Fase Retrain dengan 100% data
            best_model.fit(X, y)
            
            current_df = df_ts.copy()
            unique_prods = current_df["Produk"].unique()
            
            # Buat kamus kategori agar cepat
            prod_to_cat = current_df.drop_duplicates(subset=["Produk"]).set_index("Produk")["Kategori"].to_dict()
            
            future_rows = []
            
            # Autoregressive Loop
            for i in range(forecast_period):
                next_date = last_date_db + datetime.timedelta(days=i+1)
                
                # Append blank rows for next_date
                new_rows = []
                for prod in unique_prods:
                    new_rows.append({
                        "Tanggal": next_date, 
                        "Produk": prod, 
                        "Kategori": prod_to_cat.get(prod, ""), 
                        "Qty_Terjual": np.nan
                    })
                current_df = pd.concat([current_df, pd.DataFrame(new_rows)], ignore_index=True)
                
                # Re-calculate features
                curr_features = create_forecasting_features(current_df)
                curr_encoded = encode_categorical_features(curr_features)
                
                # Filter for next_date
                next_date_mask = curr_encoded["Tanggal"] == next_date
                if not next_date_mask.any():
                    continue
                    
                X_next, _ = split_features_target(curr_encoded[next_date_mask])
                
                # Predict
                preds = best_model.predict(X_next)
                
                # Update current_df missing values
                prod_names = curr_encoded.loc[next_date_mask, "Produk"].values
                for p_idx, p_name in enumerate(prod_names):
                    pred_val = max(0, round(preds[p_idx]))
                    mask = (current_df["Tanggal"] == next_date) & (current_df["Produk"] == p_name)
                    current_df.loc[mask, "Qty_Terjual"] = pred_val
                    
                    future_rows.append({
                        "Tanggal": next_date,
                        "Produk": p_name,
                        "Kategori": prod_to_cat.get(p_name, ""),
                        "Predicted_Qty": pred_val
                    })
            
            if future_rows:
                res_df = pd.DataFrame(future_rows)
                st.session_state["forecast_result"] = res_df
                st.success(f"🎉 Simulasi Masa Depan Rampung! AI berhasil meramal {forecast_period} hari ke depan.")
            else:
                st.error("Gagal melakukan iterasi prediksi masa depan.")
                
        except Exception as e:
            st.error(f"❌ Terjadi anomali pada siklus runtime masa depan: {str(e)}")
            st.stop()

# ================= TAMPILAN HASIL FORECAST =================
if "forecast_result" in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    eval_df = st.session_state["model_evaluation"]
    res_df = st.session_state["forecast_result"]
    best_name = st.session_state.get("best_model_name", "Unknown Model")
    
    total_forecast = res_df["Predicted_Qty"].sum()
    
    tab1, tab2 = st.tabs(["📈 Proyeksi Masa Depan", "🤖 Evaluasi Model"])
    
    with tab1:
        colA, colB = st.columns([1, 2.5])
        
        with colA:
            st.markdown("### 🏆 Pemenang Algoritma")
            render_kpi_card("Algoritma Utama", best_name, subtitle="Terpilih berdasarkan akurasi tertinggi", icon="🧠")
            st.markdown("<br>", unsafe_allow_html=True)
            
            best_row = eval_df[eval_df["model_name"] == best_name]
            akurasi_persen = 0
            if not best_row.empty:
                mape = best_row["MAPE"].values[0]
                akurasi_persen = max(0, 100 - mape)
                
            render_kpi_card("Estimasi Keakuratan", f"{akurasi_persen:.1f}%", subtitle="Berdasarkan pengujian historis", icon="🎯")
            st.markdown("<br>", unsafe_allow_html=True)
            
            render_insight_box("Fakta Sistem", f"Model {best_name} dipilih secara otomatis karena memiliki tingkat akurasi peramalan masa depan yang paling presisi dibandingkan algoritma lainnya.", icon="💡")

        with colB:
            with st.container(border=True):
                st.markdown(f"### 📈 Grafik Proyeksi Masa Depan ({best_name})")
                
                # Header untuk memecah metrik
                c1, c2 = st.columns(2)
                with c1:
                    unique_future_dates = res_df["Tanggal"].nunique()
                    st.metric("Total Estimasi Demand", f"{total_forecast:,.0f} Unit", delta=f"{unique_future_dates} Hari")
                
                # Dynamic Colors for Plotly based on Theme
                is_dark = st.session_state.get("theme_mode", "Light Mode") == "Dark Mode"
                text_color = "#CBD5E1" if is_dark else "#64748B"
                grid_color = "#334155" if is_dark else "#F1F5F9"
                
                def draw_product_chart(data, title_suffix):
                    fig = go.Figure()
                    unique_prods = data["Produk"].unique()
                    colors = px.colors.qualitative.Pastel if is_dark else px.colors.qualitative.Bold
                    
                    for i, prod in enumerate(unique_prods):
                        prod_df = data[data["Produk"] == prod]
                        c = colors[i % len(colors)]
                        fig.add_trace(go.Scatter(
                            x=prod_df["Tanggal"], y=prod_df["Predicted_Qty"], 
                            mode='lines+markers', name=prod, 
                            line=dict(color=c, width=3),
                            marker=dict(size=6, color=c),
                            hovertemplate='<b>%{x}</b><br>Estimasi: %{y:.0f} Unit<extra></extra>'
                        ))
                        
                    fig.update_layout(
                        title=f"Trend Prediksi AI - Kategori: {title_suffix}",
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        hovermode="x unified",
                        margin=dict(l=10, r=10, t=40, b=10),
                        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
                        font=dict(family="Inter, sans-serif", color=text_color),
                        xaxis=dict(showgrid=True, gridcolor=grid_color, zeroline=False),
                        yaxis=dict(showgrid=True, gridcolor=grid_color, zeroline=False)
                    )
                    return fig

                if selected_cat == "Semua Kategori":
                    unique_cats = res_df["Kategori"].unique()
                    for kat in unique_cats:
                        kat_df = res_df[res_df["Kategori"] == kat]
                        fig = draw_product_chart(kat_df, kat)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = draw_product_chart(res_df, selected_cat)
                    st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("### 📋 Tabel Proyeksi Harian")
        display_res_df = res_df.copy()
        display_res_df.columns = [col.replace("_", " ").replace("Qty", "Kuantitas").replace("Predicted", "Estimasi") for col in display_res_df.columns]
        st.dataframe(display_res_df, use_container_width=True)
        
    with tab2:
        st.markdown("### 📉 Kesenjangan Kompetisi Algoritma (Data Science Area)")
        st.write("Area ini ditujukan untuk analisis teknikal untuk membandingkan metrik nilai simpangan error riil (RMSE, MAE, MAPE).")
        
        with st.expander("⚙️ Tampilkan Papan Skor Metrik Teknis Lengkap"):
            st.dataframe(
                eval_df.style.highlight_min(subset=["MAE", "RMSE", "MAPE"], color="#16A34A").format(precision=3), 
                use_container_width=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        def plot_comparison(df, metric_name, title):
            is_dark = st.session_state.get("theme_mode", "Light Mode") == "Dark Mode"
            candidate_color = "#334155" if is_dark else "#1E293B"
            best_color = "#22C55E" if is_dark else "#16A34A"
            text_color = "#CBD5E1" if is_dark else "#64748B"
            
            df_plot = df.copy()
            df_plot["Status"] = df_plot["model_name"].apply(lambda x: "Model Terbaik" if x == best_name else "Kandidat")
            color_map = {"Model Terbaik": best_color, "Kandidat": candidate_color}
            
            fig = px.bar(
                df_plot, x="model_name", y=metric_name, 
                title=title, color="Status", color_discrete_map=color_map, text_auto=".2f"
            )
            fig.update_traces(hovertemplate='<b>%{x}</b><br>' + metric_name + ': %{y:.3f}<extra></extra>')
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=30, b=10), xaxis_title="", yaxis_title="",
                showlegend=False,
                font=dict(family="Inter, sans-serif", color=text_color),
                title_font=dict(size=16, color=text_color)
            )
            return fig

        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(plot_comparison(eval_df, "MAE", "MAE (Selisih Murni)"), use_container_width=True)
        with c2:
            st.plotly_chart(plot_comparison(eval_df, "RMSE", "RMSE (Outlier Penalty)"), use_container_width=True)
        with c3:
            st.plotly_chart(plot_comparison(eval_df, "MAPE", "MAPE (%)"), use_container_width=True)
else:
    st.info("💡 Tekan tombol **Eksekusi Forecasting** di bilah kiri untuk memutar algoritma peramalan masa depan.")
