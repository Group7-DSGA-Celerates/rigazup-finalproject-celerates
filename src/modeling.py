import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

def prepare_train_test_data(X, y, test_size=0.2):
    """
    Membagi data time series menggunakan aturan shuffle=False.
    """
    # Pastikan data cukup untuk displit agar tidak crash
    if len(X) < 10:
        return None, None, None, None
        
    # Shuffle=False wajib dipakai pada timeseries agar urutan waktu tidak rusak
    return train_test_split(X, y, test_size=test_size, shuffle=False)

def get_models() -> dict:
    """
    Mendefinisikan arsitektur ML (Linear Regression, Random Forest, XGBoost).
    """
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, random_state=42)
    }

def train_models(X_train, y_train) -> dict:
    """
    Melatih list model pada X_train dan y_train.
    Akan dikembalikan dalam bentuk dictionary of trained models.
    """
    trained_models = {}
    
    # Menangani jika data training terlalu sedikit (kosong)
    if X_train is None or len(X_train) < 5:
        return trained_models
        
    models = get_models()
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            trained_models[name] = model
        except Exception as e:
            import streamlit as st
            st.warning(f"⚠️ Algoritma {name} gagal dilatih. Melanjutkan dengan model tersisa. Error: {str(e)}")
            
    return trained_models

def predict_models(trained_models: dict, X_test) -> dict:
    """
    Mencetak keluaran (prediction) dari test data.
    """
    predictions = {}
    
    if not trained_models or X_test is None:
        return predictions
        
    for name, model in trained_models.items():
        try:
            predictions[name] = model.predict(X_test)
        except Exception as e:
            import streamlit as st
            st.warning(f"⚠️ Algoritma {name} gagal memprediksi. Error: {str(e)}")
            
    return predictions

def select_best_model(evaluation_df: pd.DataFrame, trained_models: dict):
    """
    Memilih model ML terbaik secara objektif dari papan skor (evaluation_df).
    Aturan utama: MAPE terendah. Jika tidak valid/NaN, beralih pakai RMSE terendah.
    """
    if evaluation_df is None or evaluation_df.empty or not trained_models:
        return None, None
        
    df_eval = evaluation_df.copy()
    valid_mape = df_eval[df_eval["MAPE"].notna()]
    
    if not valid_mape.empty:
        # Utamakan MAPE terkecil
        from typing import cast, Any
        best_row = valid_mape.loc[cast(Any, valid_mape["MAPE"]).idxmin()]
    else:
        # Fallback metric (RMSE terkecil) jika semua MAPE division by zero / rusak
        from typing import cast, Any
        best_row = df_eval.loc[cast(Any, df_eval["RMSE"]).idxmin()]
        
    best_model_name = best_row["model_name"]
    return best_model_name, trained_models[best_model_name]
