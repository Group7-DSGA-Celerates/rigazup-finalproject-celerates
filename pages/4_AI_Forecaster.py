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

def interpret_model_metrics(best_model_name, mae, rmse, accuracy_pct, avg_demand, product_name):
    """Generate human-friendly interpretation of model metrics."""
    if accuracy_pct >= 90:
        level = "sangat baik"
        emoji = "🟢"
        desc = "sangat akurat"
    elif accuracy_pct >= 75:
        level = "baik"
        emoji = "🟡"
        desc = "cukup akurat"
    elif accuracy_pct >= 50:
        level = "cukup"
        emoji = "🟠"
        desc = "masih perlu diperhatikan"
    else:
        level = "kurang"
        emoji = "🔴"
        desc = "perlu lebih banyak data"
    
    interpretation = f"""
{emoji} **Model {best_model_name}** menunjukkan performa **{level}** dengan tingkat akurasi **{accuracy_pct:.0f}%**.
    
📊 **Dalam bahasa bisnis:**
- Prediksi untuk **{product_name}** meleset rata-rata hanya **{mae:.0f} unit** dari permintaan aktual.
- Untuk produk yang rata-rata terjual **{avg_demand:.0f} unit/hari**, prediksi akan berkisar **{max(0, avg_demand-mae):.0f}–{avg_demand+mae:.0f} unit**.
- Tingkat kepercayaan model: **{desc}** untuk perencanaan stok.
    """
    return interpretation

st.set_page_config(page_title="Forecasting - RIGAZUP", layout="wide")
load_css()
apply_theme()
render_sidebar_theme_toggle()

render_page_header("Forecasting Penjualan", "Simulasi AI prediktif untuk meninjau estimasi tren permintaan (demand) harian secara otomatis.")

from src.validation import check_required_state
check_required_state(["clean_data"])

df_clean = st.session_state["clean_data"].copy()

st.sidebar.header("⚙️ Konfigurasi AI")

# Input API Key Gemini (Bisa dibagikan antar halaman via session_state)
st.sidebar.text_input(
    "Google Gemini API Key (Opsional)", 
    type="password", 
    help="Dibutuhkan jika Anda ingin menggunakan fitur 'Minta Penjelasan AI Lebih Detail' di bawah grafik evaluasi.",
    key="gemini_key_nlp"
)

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
default_start_date = min_allowed_date
default_end_date = min_allowed_date + datetime.timedelta(days=13)

start_date = st.sidebar.date_input("Target Tanggal Awal Forecast", min_value=min_allowed_date, value=default_start_date)
target_date = st.sidebar.date_input("Target Tanggal Akhir Forecast", min_value=start_date, value=default_end_date)
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
                # Filter hasil hanya untuk periode yang dipilih
                mask = (res_df["Tanggal"].dt.date >= pd.to_datetime(start_date).date()) & (res_df["Tanggal"].dt.date <= pd.to_datetime(target_date).date())
                res_df = res_df[mask]
                
                st.session_state["forecast_result"] = res_df
                st.success(f"🎉 Simulasi Masa Depan Rampung! AI berhasil meramal periode yang dipilih.")
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
            # Tambahkan kolom Akurasi % dan Bintang untuk model terbaik
            display_eval_df = eval_df.copy()
            if "R2" in display_eval_df.columns:
                display_eval_df["Akurasi %"] = display_eval_df["R2"].apply(lambda x: max(0, x * 100))
            else:
                display_eval_df["Akurasi %"] = display_eval_df["MAPE"].apply(lambda x: max(0, 100 - x))
                
            display_eval_df["Model"] = display_eval_df["model_name"].apply(lambda x: f"{x} ⭐" if x == best_name else x)
            display_eval_df = display_eval_df.drop(columns=["model_name"]).set_index("Model")
            
            st.dataframe(
                display_eval_df.style.highlight_max(subset=["Akurasi %"], color="#16A34A").highlight_min(subset=["MAE", "RMSE", "MAPE"], color="#16A34A").format(precision=3), 
                use_container_width=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 💡 Interpretasi Model Manusiawi
        st.markdown("### 💡 Apa Artinya untuk Bisnis Anda?")
        best_row = eval_df[eval_df["model_name"] == best_name].iloc[0]
        mae_val = best_row["MAE"]
        rmse_val = best_row["RMSE"]
        akurasi_val = max(0, best_row["R2"] * 100) if "R2" in eval_df.columns else max(0, 100 - best_row["MAPE"])
        
        filtered_df = df_clean.copy()
        if selected_cat != "Semua Kategori":
            filtered_df = filtered_df[filtered_df["Kategori"] == selected_cat]
        if selected_prod != "Semua Produk":
            filtered_df = filtered_df[filtered_df["Produk"] == selected_prod]
            
        avg_demand = filtered_df["Qty_Terjual"].mean() if not filtered_df.empty else 0
        product_name_display = selected_prod if selected_prod != "Semua Produk" else "Kategori Terpilih"
        
        interpretation = interpret_model_metrics(best_name, mae_val, rmse_val, akurasi_val, avg_demand, product_name_display)
        
        st.info(interpretation)
        
        if st.button("🤖 Minta Penjelasan AI Lebih Detail", icon="✨"):
            api_key = st.secrets.get("GEMINI_API_KEY", "")
            if "gemini_key_nlp" in st.session_state and st.session_state["gemini_key_nlp"]:
                api_key = st.session_state["gemini_key_nlp"]
                
            if not api_key:
                st.error("⚠️ API Key Gemini tidak ditemukan. Harap masukkan di halaman 'Input Penjualan Baru' (Tab AI) atau 'AI Insight Generator'.")
            else:
                with st.spinner("Memanggil Gemini AI..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        
                        prompt = f"""
Anda adalah analis sistem tingkat lanjut. Jelaskan hasil evaluasi model peramalan (forecasting) berikut dalam 2-3 kalimat lugas, profesional, dan universal. 

ATURAN KETAT:
1. JANGAN gunakan sapaan personal atau gender seperti "Bapak/Ibu", "Kakak", "Halo", dll. Gunakan sudut pandang objektif atau sapaan universal "Anda".
2. JANGAN gunakan kata "komputer", "tebakan", "AI", "bot", atau kata apa pun yang merujuk bahwa ini dikerjakan oleh mesin atau kecerdasan buatan. Gunakan istilah "sistem" atau "algoritma".
3. JANGAN gunakan istilah teknis statistik (seperti MAE/RMSE/R2) secara kaku, tapi terjemahkan langsung ke dampaknya pada manajemen stok dan bisnis.
4. Berikan insight yang bisa langsung ditindaklanjuti.

Data Evaluasi:
- Algoritma terbaik: {best_name}
- MAE (rata-rata selisih proyeksi): {mae_val:.0f} unit
- Akurasi: {akurasi_val:.2f}%
- Produk: {product_name_display}
- Rata-rata penjualan harian aktual: {avg_demand:.0f} unit
"""
                        response = model.generate_content(prompt)
                        st.success(response.text)
                    except Exception as e:
                        st.error(f"❌ Gagal memanggil Gemini: {str(e)}")
                        
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
