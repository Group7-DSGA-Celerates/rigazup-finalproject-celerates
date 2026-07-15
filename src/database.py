import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

DB_PATH = 'rigazup.db'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT UNIQUE NOT NULL,
        default_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        product_name TEXT NOT NULL,
        quantity_sold INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        source TEXT DEFAULT 'manual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_name) REFERENCES products(product_name)
    );
    """)
    
    conn.commit()
    conn.close()

def insert_transaction(date, product, qty, price, source='manual'):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure product exists
    cursor.execute("INSERT OR IGNORE INTO products (product_name, default_price) VALUES (?, ?)", (product, price))
    
    cursor.execute("""
    INSERT INTO transactions (date, product_name, quantity_sold, unit_price, source)
    VALUES (?, ?, ?, ?, ?)
    """, (date, product, qty, price, source))
    
    conn.commit()
    conn.close()

def insert_bulk_transactions(df, source='csv'):
    conn = get_connection()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        # Insert or ignore products
        cursor.execute("INSERT OR IGNORE INTO products (product_name, default_price) VALUES (?, ?)", 
                       (row['product_name'], row['unit_price']))
        
        cursor.execute("""
        INSERT INTO transactions (date, product_name, quantity_sold, unit_price, source)
        VALUES (?, ?, ?, ?, ?)
        """, (row['date'], row['product_name'], row['quantity_sold'], row['unit_price'], source))
        
    conn.commit()
    conn.close()

def get_all_transactions() -> pd.DataFrame:
    conn = get_connection()
    query = "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_products() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name FROM products ORDER BY product_name")
    products = [row[0] for row in cursor.fetchall()]
    conn.close()
    return products

def get_product_price(product_name: str) -> float:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT default_price FROM products WHERE product_name = ?", (product_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0.0

def add_product(name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO products (product_name, default_price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def get_today_transactions() -> pd.DataFrame:
    today = datetime.now().strftime('%Y-%m-%d')
    conn = get_connection()
    query = f"SELECT * FROM transactions WHERE date = '{today}' ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM products")
    conn.commit()
    conn.close()

def load_data_to_session():
    df = get_all_transactions()
    if not df.empty:
        st.session_state['uploaded_data'] = df
    else:
        st.session_state['uploaded_data'] = None

def has_real_data() -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE source != 'demo'")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def load_demo_data_routine():
    import os
    if not os.path.exists('data/demo_sales_data.csv'):
        st.error("File data/demo_sales_data.csv tidak ditemukan.")
        return
    clear_all_data()
    df = pd.read_csv('data/demo_sales_data.csv')
    insert_bulk_transactions(df, source='demo')
    load_data_to_session()
    st.success("🎮 Data demo berhasil dimuat! Anda dapat menjelajahi semua fitur sekarang.")
    st.balloons()

def render_demo_button(key_prefix=""):
    state_key = f"{key_prefix}confirm_demo"
    if state_key not in st.session_state:
        st.session_state[state_key] = False

    def handle_click():
        if has_real_data():
            st.session_state[state_key] = True
        else:
            load_demo_data_routine()

    if st.session_state[state_key]:
        st.warning("⚠️ Memuat data demo akan menghapus data saat ini. Lanjutkan?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ya", key=f"{key_prefix}btn_yes", use_container_width=True):
                load_demo_data_routine()
                st.session_state[state_key] = False
                st.rerun()
        with col2:
            if st.button("Batal", key=f"{key_prefix}btn_no", use_container_width=True):
                st.session_state[state_key] = False
                st.rerun()
    else:
        st.button("🚀 Gunakan Data Simulasi Demo", on_click=handle_click, key=f"{key_prefix}btn_main", use_container_width=True)
