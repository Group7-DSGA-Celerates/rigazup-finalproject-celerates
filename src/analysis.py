import pandas as pd

def calculate_market_basket(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Menghitung pasangan produk yang paling sering dibeli pada periode waktu yang sama (Market Basket Analysis).
    Menggunakan 'Tanggal' sebagai proxy untuk ID Transaksi keranjang belanja UMKM.
    """
    basket = df.groupby('Tanggal')['Produk'].apply(list).reset_index()
    
    pair_counts = {}
    for items in basket['Produk']:
        unique_items = list(set(items))
        for i in range(len(unique_items)):
            for j in range(i+1, len(unique_items)):
                itemA = unique_items[i]
                itemB = unique_items[j]
                
                # Urutkan secara alfabetis agar (A,B) terhitung sama dengan (B,A)
                pair = tuple(sorted([itemA, itemB]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1
                
    if not pair_counts:
        return pd.DataFrame(columns=["Produk A", "Produk B", "Frekuensi Bersamaan", "Rekomendasi Bundling"])
        
    pairs_list = []
    for p, c in pair_counts.items():
        pairs_list.append({
            "Produk A": p[0], 
            "Produk B": p[1], 
            "Frekuensi Bersamaan": c,
            "Rekomendasi Bundling": f"Promo Paket: {p[0]} + {p[1]}"
        })
        
    pairs_df = pd.DataFrame(pairs_list)
    pairs_df = pairs_df.sort_values(by="Frekuensi Bersamaan", ascending=False).head(top_n)
    
    return pairs_df
