import pandas as pd
import numpy as np
import os
import argparse

def generate_demo_data(start_date='2024-01-01', end_date='2024-12-31'):
    """Generate realistic sales data for a fictional mini market over a specified date range."""
    # Seed for reproducibility
    np.random.seed(42)
    
    products = {
        "Indomie Goreng": {"price": 3500, "lam": 11.5, "is_food": True},
        "Minyak Goreng Bimoli 1L": {"price": 18000, "lam": 5, "is_food": True},
        "Beras Premium 5kg": {"price": 65000, "lam": 3, "is_food": True},
        "Gula Pasir 1kg": {"price": 15000, "lam": 4.5, "is_food": True},
        "Kopi Kapal Api Sachet": {"price": 1500, "lam": 15, "is_food": True},
        "Sabun Mandi Lifebuoy": {"price": 4500, "lam": 5.5, "is_food": False},
        "Deterjen Rinso 800g": {"price": 12000, "lam": 3.5, "is_food": False},
        "Air Mineral Aqua 600ml": {"price": 3000, "lam": 20, "is_food": True},
        "Teh Pucuk Harum 350ml": {"price": 4000, "lam": 11.5, "is_food": True},
        "Rokok Gudang Garam": {"price": 28000, "lam": 8.5, "is_food": False}, 
        "Telur Ayam (butir)": {"price": 2500, "lam": 15, "is_food": True},
        "Susu Ultra Milk 250ml": {"price": 5500, "lam": 7.5, "is_food": True},
        "Roti Tawar Sari Roti": {"price": 15000, "lam": 3.5, "is_food": True},
        "Mie Sedaap Goreng": {"price": 3200, "lam": 9, "is_food": True},
        "Sambal ABC Sachet": {"price": 2000, "lam": 11.5, "is_food": True},
    }
    
    dates = pd.date_range(start_date, end_date)
    
    records = []
    for date in dates:
        # Weekend boost (+20%)
        is_weekend = date.weekday() >= 5
        weekend_mult = 1.2 if is_weekend else 1.0
        
        # Seasonal boost for food items (simplification: assume March/April as high demand month for demo)
        is_ramadan = date.month in [3, 4]
        
        # Year end boost (December)
        is_december = date.month == 12
        
        for product, info in products.items():
            base_lam = info["lam"]
            
            # Apply multipliers
            lam = base_lam * weekend_mult
            
            if is_ramadan and info["is_food"]:
                lam *= 1.3 # +30% during seasonal high
                
            if is_december:
                lam *= 1.2 # +20% in December
                
            qty = np.random.poisson(lam=lam)
            
            if qty > 0:
                records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'product_name': product,
                    'quantity_sold': qty,
                    'unit_price': info["price"]
                })
    
    df = pd.DataFrame(records)
    
    # Save
    os.makedirs('data', exist_ok=True)
    out_path = 'data/demo_sales_data.csv'
    df.to_csv(out_path, index=False)
    
    print(f"File saved to {out_path}")
    print(f"Total rows: {len(df)}")
    print(f"Unique products: {df['product_name'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate demo sales data.")
    parser.add_argument('--start', type=str, default='2024-01-01', help="Start date (YYYY-MM-DD)")
    parser.add_argument('--end', type=str, default='2024-12-31', help="End date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    generate_demo_data(args.start, args.end)
