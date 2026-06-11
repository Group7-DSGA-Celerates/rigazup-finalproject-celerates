import pandas as pd
from src.preprocessing import clean_data
from src.feature_engineering import prepare_sales_time_series, create_forecasting_features, split_features_target
from sklearn.linear_model import LinearRegression

def encode_categorical_features_modified(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    dummies = pd.get_dummies(df[["Produk", "Kategori"]], drop_first=False)
    # Ensure they are numeric (0/1) instead of boolean
    dummies = dummies.astype(int)
    df_encoded = pd.concat([df, dummies], axis=1)
    return df_encoded

df = pd.read_csv("data/dataset.csv")
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df_clean = clean_data(df)
df_ts = prepare_sales_time_series(df_clean)
df_features = create_forecasting_features(df_ts)
df_encoded = encode_categorical_features_modified(df_features)

X, y = split_features_target(df_encoded)
model = LinearRegression()
model.fit(X, y)

print(X.columns.tolist()[:15])
print("Successfully trained with OHE!")
