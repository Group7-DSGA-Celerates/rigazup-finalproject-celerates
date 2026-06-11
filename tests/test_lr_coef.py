import pandas as pd
from src.preprocessing import clean_data
from src.feature_engineering import prepare_sales_time_series, create_forecasting_features, encode_categorical_features, split_features_target
from sklearn.linear_model import LinearRegression

def create_forecasting_features_modified(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df_feat = df.copy()
    df_feat = df_feat.sort_values(by=["Produk", "Tanggal"])
    df_feat["Tahun"] = df_feat["Tanggal"].dt.year
    df_feat["Bulan"] = df_feat["Tanggal"].dt.month
    df_feat["Hari"] = df_feat["Tanggal"].dt.day
    df_feat["day_of_week"] = df_feat["Tanggal"].dt.dayofweek
    df_feat["is_weekend"] = df_feat["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)
    df_feat["is_month_start"] = df_feat["Tanggal"].dt.is_month_start.astype(int)
    df_feat["is_month_end"] = df_feat["Tanggal"].dt.is_month_end.astype(int)
    
    df_feat["lag_1"] = df_feat.groupby("Produk")["Qty_Terjual"].shift(1)
    df_feat["lag_7"] = df_feat.groupby("Produk")["Qty_Terjual"].shift(7)
    df_feat["rolling_mean_7"] = df_feat.groupby("Produk")["Qty_Terjual"].transform(lambda x: x.shift(1).rolling(7).mean())
    df_feat["rolling_mean_14"] = df_feat.groupby("Produk")["Qty_Terjual"].transform(lambda x: x.shift(1).rolling(14).mean())
    
    feature_cols = ["lag_1", "lag_7", "rolling_mean_7", "rolling_mean_14"]
    df_feat = df_feat.dropna(subset=feature_cols)
    return df_feat

df = pd.read_csv("data/dataset.csv")
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df_clean = clean_data(df)

df_ts = prepare_sales_time_series(df_clean)
df_features = create_forecasting_features_modified(df_ts)
df_encoded = encode_categorical_features(df_features)

X, y = split_features_target(df_encoded)
model = LinearRegression()
model.fit(X, y)

print(list(zip(X.columns, model.coef_)))
