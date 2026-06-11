import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

def calculate_mae(y_true, y_pred):
    """Menghitung Mean Absolute Error."""
    return mean_absolute_error(y_true, y_pred)

def calculate_rmse(y_true, y_pred):
    """Menghitung Root Mean Squared Error."""
    return np.sqrt(mean_squared_error(y_true, y_pred))

def calculate_mape(y_true, y_pred):
    """
    Menghitung Mean Absolute Percentage Error.
    Secara proaktif menangani pencegahan division by zero.
    """
    # Gantikan 0 dengan nilai desimal yang sangat kecil agar tidak infinite
    y_true_safe = np.where(y_true == 0, 1e-10, y_true)
    mape = np.mean(np.abs((y_true - y_pred) / y_true_safe)) * 100
    
    # Filter hasil ekstrim dari data yang anomali
    if np.isinf(mape):
        mape = np.nan
        
    return mape

def evaluate_predictions(y_test, predictions: dict) -> pd.DataFrame:
    """
    Mengevaluasi seluruh array prediksi yang dihasilkan oleh model.
    Menghasilkan rangkuman metrik dalam bentuk DataFrame.
    """
    results = []
    
    for model_name, y_pred in predictions.items():
        mae = calculate_mae(y_test, y_pred)
        rmse = calculate_rmse(y_test, y_pred)
        mape = calculate_mape(y_test, y_pred)
        
        results.append({
            "model_name": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })
        
    evaluation_df = pd.DataFrame(results)
    return evaluation_df
