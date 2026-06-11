import pandas as pd

def format_currency(value):
    """Fungsi helper internal untuk format Rupiah."""
    return f"Rp {value:,.0f}".replace(",", ".")

def generate_sales_insight(df: pd.DataFrame) -> str:
    """Menghasilkan narasi ringkasan total penjualan bisnis."""
    total_revenue = df["Total_Penjualan"].sum()
    total_qty = df["Qty_Terjual"].sum()
    total_trx = df.shape[0]
    
    return (f"Sepanjang periode data yang tersedia, bisnis Anda telah mencatatkan **{total_trx:,} baris data penjualan** "
            f"dengan melepaskan total barang sebanyak **{total_qty:,.0f} unit**. "
            f"Pendapatan kotor (revenue) keseluruhan mencapai **{format_currency(total_revenue)}**.")

def generate_product_insight(df_prod: pd.DataFrame) -> str:
    """Menghasilkan narasi seputar produk paling laris dan kategori top."""
    top_rev_prod = df_prod.loc[df_prod["total_penjualan"].idxmax()]
    top_qty_prod = df_prod.loc[df_prod["total_qty_terjual"].idxmax()]
    
    cat_rev = df_prod.groupby("Kategori")["total_penjualan"].sum()
    top_cat = cat_rev.idxmax()
    
    return (f"Kategori **{top_cat}** merupakan pilar utama penopang omset bisnis Anda. "
            f"Untuk satuan barang, produk **{top_qty_prod['Produk']}** adalah favorit pelanggan karena paling banyak dibeli ({top_qty_prod['total_qty_terjual']:,.0f} unit). "
            f"Namun, jika dilihat dari kacamata nilai uang, **{top_rev_prod['Produk']}** adalah kontributor terbaik yang menyumbang pemasukan sebesar {format_currency(top_rev_prod['total_penjualan'])}.")

def generate_stock_insight(df_stock: pd.DataFrame) -> str:
    """Menghasilkan narasi terkait peringatan bahaya Stockout dan Overstock."""
    df_so = df_stock[df_stock["stockout_risk"] == "High"]
    df_os = df_stock[df_stock["overstock_risk"] == "High"]
    
    insight = ""
    
    # Stockout Logic
    if not df_so.empty:
        prod_so = df_so.sort_values(by="transaction_count", ascending=False).iloc[0]["Produk"]
        insight += f"Segera amankan suplai Anda! Terdapat **{len(df_so)} produk** yang sangat berisiko kehabisan stok (Stockout). Contoh utamanya adalah **{prod_so}** di mana laju pembelinya tinggi sementara cadangan gudang sangat menipis. "
    else:
        insight += "Secara keseluruhan suplai gudang Anda cukup aman karena tidak ada produk yang kritis kehabisan stok. "
        
    # Overstock Logic
    if not df_os.empty:
        prod_os = df_os.sort_values(by="transaction_count", ascending=True).iloc[0]["Produk"]
        insight += f"\n\nNamun, perhatikan juga pengeluaran modal mati. Terdapat **{len(df_os)} produk** yang menumpuk tinggi tanpa adanya pembeli (Overstock). Perhatikan produk **{prod_os}**, hentikan restock dan pertimbangkan membuat diskon cuci gudang."
    else:
        insight += "\n\nKabar baiknya, sistem tidak mendeteksi adanya tumpukan stok mati (Overstock) berskala besar. Manajemen inventaris berjalan sehat."
        
    return insight

def generate_restock_insight(df_restock: pd.DataFrame) -> str:
    """Menghasilkan kesimpulan actionable dari data rekomendasi restock."""
    df_high = df_restock[df_restock["priority_level"] == "High"]
    
    if df_high.empty:
        return "Berdasarkan hitungan sistem terhadap prediksi masa depan, belum ada keharusan untuk merestock barang dengan prioritas tinggi hari ini. Anda bisa menghemat anggaran kas untuk sementara."
        
    total_units_needed = df_high["recommended_restock"].sum()
    top_priority_prod = df_high.sort_values(by="recommended_restock", ascending=False).iloc[0]["Produk"]
    
    return (f"Saatnya bertindak: Terdapat **{df_high.shape[0]} tipe produk** yang wajib Anda restock (Prioritas High). "
            f"Berdasarkan prediksi permintaan, persiapkan pesanan pembelian kurang lebih sebesar **{total_units_needed:,.0f} unit** total. "
            f"Prioritas utama pembelanjaan harus difokuskan pada produk **{top_priority_prod}**.")
