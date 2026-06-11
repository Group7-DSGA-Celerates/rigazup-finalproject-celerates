import pandas as pd
df = pd.read_csv('data/dataset.csv')
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['is_weekend'] = df['Tanggal'].dt.dayofweek >= 5

teh = df[df['Produk'] == 'Teh Celup']
kopi = df[df['Produk'] == 'Kopi Botol']

print("Teh Celup Weekday mean:", teh[~teh['is_weekend']]['Qty_Terjual'].mean())
print("Teh Celup Weekend mean:", teh[teh['is_weekend']]['Qty_Terjual'].mean())

print("Kopi Botol Weekday mean:", kopi[~kopi['is_weekend']]['Qty_Terjual'].mean())
print("Kopi Botol Weekend mean:", kopi[kopi['is_weekend']]['Qty_Terjual'].mean())
