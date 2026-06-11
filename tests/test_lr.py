import pandas as pd
import numpy as np
import datetime
from src.preprocessing import clean_data
from src.feature_engineering import prepare_sales_time_series, create_forecasting_features, encode_categorical_features, split_features_target
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/dataset.csv")
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df_clean = clean_data(df)

df_ts = prepare_sales_time_series(df_clean)
df_features = create_forecasting_features(df_ts)
df_encoded = encode_categorical_features(df_features)

X, y = split_features_target(df_encoded)
model = LinearRegression()
model.fit(X, y)

current_df = df_ts.copy()
last_date_db = df_clean['Tanggal'].max()
unique_prods = current_df['Produk'].unique()
prod_to_cat = current_df.drop_duplicates(subset=['Produk']).set_index('Produk')['Kategori'].to_dict()

future_rows = []

for i in range(23):
    next_date = last_date_db + datetime.timedelta(days=i+1)
    new_rows = []
    for prod in unique_prods:
        new_rows.append({'Tanggal': next_date, 'Produk': prod, 'Kategori': prod_to_cat.get(prod, ''), 'Qty_Terjual': np.nan})
    current_df = pd.concat([current_df, pd.DataFrame(new_rows)], ignore_index=True)
    
    curr_features = create_forecasting_features(current_df)
    curr_encoded = encode_categorical_features(curr_features)
    next_date_mask = curr_encoded['Tanggal'] == next_date
    X_next, _ = split_features_target(curr_encoded[next_date_mask])
    
    preds = model.predict(X_next)
    
    prod_names = curr_encoded.loc[next_date_mask, 'Produk'].values
    for p_idx, p_name in enumerate(prod_names):
        pred_val = max(0, round(preds[p_idx]))
        mask = (current_df['Tanggal'] == next_date) & (current_df['Produk'] == p_name)
        current_df.loc[mask, 'Qty_Terjual'] = pred_val
        
        future_rows.append({
            'Tanggal': next_date,
            'Produk': p_name,
            'Kategori': prod_to_cat.get(p_name, ''),
            'Predicted_Qty': pred_val
        })

res_df = pd.DataFrame(future_rows)
print("Air Mineral LR Preds:")
print(res_df[res_df['Produk'] == 'Air Mineral']['Predicted_Qty'].tolist())
