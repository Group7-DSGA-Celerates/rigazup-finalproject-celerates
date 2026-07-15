import os
import pandas as pd
import streamlit as st

# Mock Streamlit methods that are called inside the backend
st.error = lambda x, **kwargs: print(f"ERROR: {x}")
st.success = lambda x, **kwargs: print(f"SUCCESS: {x}")
st.balloons = lambda: print("BALLOONS!")

from src.database import init_db, insert_transaction, insert_bulk_transactions, get_today_transactions, add_product, get_products, load_data_to_session, clear_all_data, has_real_data, load_demo_data_routine

def run_tests():
    print("Testing Backend...")
    # Initialize DB
    init_db()
    
    # Clear all data
    clear_all_data()
    print("Cleared DB. Has real data?", has_real_data())
    
    # Load demo data
    load_demo_data_routine()
    print("Loaded Demo. Has real data?", has_real_data())
    
    # Add product
    add_product("Teh Pucuk", 3500)
    prods = get_products()
    print("Products count:", len(prods))
    assert "Teh Pucuk" in prods
    
    # Insert Transaction
    import datetime
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    insert_transaction(today_str, "Teh Pucuk", 5, 3500, "manual")
    
    # Get today transactions
    today = get_today_transactions()
    print("Today transactions:", len(today))
    assert len(today) >= 1
    
    print("Backend tests passed!")

if __name__ == "__main__":
    run_tests()
