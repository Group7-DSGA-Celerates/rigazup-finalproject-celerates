import pandas as pd

def create_stock_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Membuat ringkasan stok per produk dan kategori berdasarkan riwayat penjualan."""
    # Pastikan data diurutkan berdasar tanggal agar .last() mendapatkan stok terkini
    df_sorted = df.sort_values(by=["Tanggal"])
    
    summary = df_sorted.groupby(["Produk", "Kategori"]).agg(
        total_qty_terjual=("Qty_Terjual", "sum"),
        avg_qty_terjual=("Qty_Terjual", "mean"),
        total_penjualan=("Total_Penjualan", "sum"),
        transaction_count=("Total_Penjualan", "count"),
        latest_stock=("Stok_Setelah_Transaksi", "last"),
        avg_stock=("Stok_Setelah_Transaksi", "mean"),
        lead_time_hari=("Lead_Time_Hari", "last"),
        harga_modal=("Harga_Modal", "last")
    ).reset_index()
    summary["stockout_risk"] = summary.apply(calculate_stockout_risk, axis=1)
    summary["overstock_risk"] = summary.apply(calculate_overstock_risk, axis=1)
    
    return summary

def calculate_stockout_risk(row) -> str:
    """
    Menghitung risiko kehabisan stok (Stockout).
    Kriteria prioritas: stok terkini rendah, namun laju penjualan dan transaksi historis tinggi.
    """
    stock = row["latest_stock"]
    avg_qty = row["avg_qty_terjual"]
    trx = row["transaction_count"]
    
    # Threshold kustom (Dapat disesuaikan)
    if stock <= 5 and avg_qty >= 2 and trx >= 5:
        return "High"
    elif stock <= 15 and avg_qty >= 1:
        return "Medium"
    else:
        return "Low"

def calculate_overstock_risk(row) -> str:
    """
    Menghitung risiko kelebihan stok (Overstock).
    Kriteria prioritas: stok terkini tinggi, namun laju penjualan dan transaksi historis rendah.
    """
    stock = row["latest_stock"]
    avg_qty = row["avg_qty_terjual"]
    trx = row["transaction_count"]
    
    # Threshold kustom (Dapat disesuaikan)
    if stock >= 40 and avg_qty < 1.5 and trx < 10:
        return "High"
    elif stock >= 20 and avg_qty < 2.5:
        return "Medium"
    else:
        return "Low"

def generate_stock_recommendation(row) -> str:
    """
    Memberikan teks rekomendasi aksi sederhana untuk user berdasarkan nilai risikonya.
    """
    s_risk = row["stockout_risk"]
    o_risk = row["overstock_risk"]
    
    if s_risk == "High":
        return "🔥 Prioritas Restock Segera! Permintaan tinggi & stok kritis."
    elif s_risk == "Medium":
        return "👀 Pantau ketat pergerakan, siapkan plan restock."
    elif o_risk == "High":
        return "🚨 Hentikan pengadaan! Coba program promo/diskon."
    elif o_risk == "Medium":
        return "⏳ Kurangi volume pengadaan selanjutnya."
    else:
        return "✅ Stok saat ini berimbang dengan demand."

def calculate_recommended_restock(forecast_demand, current_stock, safety_stock, avg_daily_sales=0.0, lead_time=3.0):
    """Menghitung jumlah unit yang harus dibeli ulang dengan Lead Time Supplier."""
    reorder_point = (avg_daily_sales * lead_time) + safety_stock
    target_stock = forecast_demand + reorder_point
    return max(0, target_stock - current_stock)

def determine_restock_priority(recommended, current_stock, safety_stock):
    """Menentukan tingkat urgensi restock."""
    if recommended > 0 and (current_stock <= (safety_stock * 0.5) or current_stock == 0):
        return "High"
    elif recommended > 0 and current_stock > (safety_stock * 0.5):
        return "Medium"
    else:
        return "Low"

def generate_restock_reason(priority, current_stock, forecast_demand):
    """Membuat deskripsi bahasa manusia atas alasan sistem menyarankan restock."""
    if priority == "High":
        return f"Kritis: Stok sisa {current_stock:,.0f}, sementara demand {forecast_demand:,.0f} unit."
    elif priority == "Medium":
        return f"Warning: Menuju kehabisan stok jika tidak restock."
    else:
        return "Aman: Stok di gudang mencukupi demand ke depan."

