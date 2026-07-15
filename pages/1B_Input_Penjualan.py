import streamlit as st
import pandas as pd
from datetime import datetime
import time

from src.database import (
    get_products, get_product_price, insert_transaction, 
    add_product, get_today_transactions, load_data_to_session
)
from src.visualization import load_css, apply_theme, render_sidebar_theme_toggle

# Konfigurasi halaman
# (Catatan: st.set_page_config biasanya hanya bekerja jika dipanggil paling awal.
#  Karena app.py memanggilnya, kita cukup import styling di sini)
load_css()
apply_theme()
render_sidebar_theme_toggle()

st.title("🧾 Input Penjualan Baru")

# 2 Tab Utama
tab1, tab2 = st.tabs(["📝 Form Manual", "💬 Catat Nota Cepat (AI)"])

with tab1:
    st.markdown("### 🛒 Form Transaksi Harian")
    
    # 1. Tambah Produk Baru (Expander, di luar form utama agar tidak bentrok dengan st.form)
    with st.expander("➕ Tambah Produk Baru ke Master Data"):
        new_prod_name = st.text_input("Nama Produk Baru")
        new_prod_price = st.number_input("Harga Satuan Default (Rp)", min_value=0.0, step=500.0)
        if st.button("Simpan Produk Baru"):
            if not new_prod_name.strip():
                st.error("Nama produk tidak boleh kosong.")
            elif new_prod_price <= 0:
                st.error("Harga harus lebih dari 0.")
            else:
                existing = get_products()
                # Cek duplikasi case-insensitive
                if new_prod_name.strip().lower() in [p.lower() for p in existing]:
                    st.error(f"Produk '{new_prod_name}' sudah ada di database!")
                else:
                    add_product(new_prod_name.strip(), new_prod_price)
                    st.success(f"✅ Produk '{new_prod_name}' berhasil ditambahkan!")
                    time.sleep(1)
                    st.rerun()

    # 2. Form Input Transaksi Utama
    product_list = get_products()
    
    if not product_list:
        st.warning("Master data produk masih kosong. Silakan tambah produk baru melalui form di atas atau muat Data Demo.")
    else:
        # Selectbox diletakkan di luar st.form agar bisa men-trigger auto-fill harga secara real-time
        selected_product = st.selectbox("📦 Pilih Produk", options=product_list)
        default_price = get_product_price(selected_product)
        
        with st.form("input_transaksi"):
            tanggal = st.date_input("📅 Tanggal", value=datetime.today())
            qty = st.number_input("🔢 Jumlah", min_value=1, step=1, value=1)
            harga = st.number_input("💰 Harga Satuan", min_value=0.0, step=500.0, value=float(default_price))
            
            submitted = st.form_submit_button("💾 Simpan Transaksi", use_container_width=True)
            
            if submitted:
                # Validasi
                if tanggal > datetime.today().date():
                    st.error("Tanggal tidak boleh di masa depan.")
                elif qty < 1:
                    st.error("Jumlah minimal 1.")
                elif harga <= 0:
                    st.error("Harga harus lebih dari 0.")
                else:
                    insert_transaction(
                        date=tanggal.strftime("%Y-%m-%d"),
                        product=selected_product,
                        qty=qty,
                        price=harga,
                        source='manual'
                    )
                    load_data_to_session() # Sinkronisasi session state
                    st.success("✅ Transaksi tersimpan!")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
                    
    st.divider()
    
    # 3. Riwayat Transaksi Hari Ini
    st.markdown("### 📋 Riwayat Transaksi Hari Ini")
    today_df = get_today_transactions()
    
    if today_df.empty:
        st.info("Belum ada transaksi yang dicatat hari ini.")
    else:
        # Kalkulasi Total Pendapatan & Qty
        today_df['Total'] = today_df['quantity_sold'] * today_df['unit_price']
        total_revenue = today_df['Total'].sum()
        total_items = today_df['quantity_sold'].sum()
        
        # Format tabel agar lebih enak dilihat
        st.dataframe(
            today_df[['id', 'product_name', 'quantity_sold', 'unit_price', 'Total', 'source']],
            use_container_width=True,
            column_config={
                "id": "No",
                "product_name": "Produk",
                "quantity_sold": "Qty",
                "unit_price": st.column_config.NumberColumn("Harga Satuan", format="Rp %d"),
                "Total": st.column_config.NumberColumn("Total", format="Rp %d"),
                "source": "Sumber"
            }
        )
        
        st.markdown(f"**📊 Total Hari Ini: Rp {total_revenue:,.0f} ({total_items} item)**")
        
        # 4. Tombol Export CSV
        csv = today_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Transaksi Hari Ini (CSV)",
            data=csv,
            file_name=f"transaksi_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

with tab2:
    st.markdown("### 💬 Catat Nota Cepat (AI-Powered)")
    st.markdown("Ketik nota penjualan Anda dengan bahasa bebas:")
    
    # Gunakan key unik agar tidak bentrok dengan halaman insight
    api_key = st.sidebar.text_input(
        "Google Gemini API Key (Untuk NLP)", 
        type="password", 
        key="gemini_key_nlp",
        help="Dapatkan kunci gratis di aistudio.google.com"
    )
    
    user_input = st.text_area(
        "Teks Penjualan", 
        placeholder="Minyak goreng laku 3, indomie dibeli orang 5 biji, sabun mandi 2", 
        height=100
    )
    
    if st.button("🤖 Proses dengan AI", type="primary"):
        if not api_key:
            st.error("⚠️ Masukkan Google Gemini API Key di sidebar terlebih dahulu.")
        elif not user_input.strip():
            st.error("⚠️ Teks penjualan tidak boleh kosong.")
        else:
            with st.spinner("Menganalisis teks nota..."):
                import google.generativeai as genai
                import json
                import difflib
                
                genai.configure(api_key=api_key)
                
                try:
                    # Menggunakan gemini-pro atau gemini-1.5-flash
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    EXTRACTION_PROMPT = f"""
Kamu adalah asisten kasir toko kelontong Indonesia.
Ekstrak teks penjualan berikut menjadi format JSON array.
Setiap item harus memiliki field: "nama_barang" (string, capitalized) dan "quantity" (integer).

ATURAN PENTING:
1. Jika tidak ada angka disebutkan, anggap quantity = 1
2. Abaikan kata-kata seperti "laku", "dibeli orang", "biji", "buah", "karung", "pcs"
3. Normalisasi nama barang (contoh: "mie goreng" → "Indomie Goreng", "migor" → "Minyak Goreng")
4. Jangan tambahkan field lain selain "nama_barang" dan "quantity"
5. Output HANYA JSON array, tanpa penjelasan atau markdown

Teks penjualan:
"{user_input}"
"""
                    response = model.generate_content(EXTRACTION_PROMPT)
                    
                    # Bersihkan markdown formatting yang dikembalikan Gemini
                    json_str = response.text.strip()
                    if json_str.startswith("```json"):
                        json_str = json_str[7:-3].strip()
                    elif json_str.startswith("```"):
                        json_str = json_str[3:-3].strip()
                        
                    parsed_data = json.loads(json_str)
                    
                    if not isinstance(parsed_data, list):
                        st.error("Format respons API tidak sesuai (bukan JSON array).")
                    else:
                        st.session_state['nlp_parsed_data'] = parsed_data
                        
                except json.JSONDecodeError:
                    st.error("❌ Gagal melakukan parsing data. Respons API bukan format JSON yang valid. Harap ubah kata-kata Anda atau gunakan form manual.")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan koneksi atau API: {str(e)}")

    if 'nlp_parsed_data' in st.session_state:
        st.markdown("---")
        st.markdown("### 📝 Preview Hasil Parsing")
        
        parsed_data = st.session_state['nlp_parsed_data']
        product_master = get_products()
        
        import difflib
        
        preview_rows = []
        for item in parsed_data:
            extracted_name = item.get("nama_barang", "")
            qty = item.get("quantity", 1)
            
            # 4. Fuzzy Matching dengan difflib.get_close_matches
            matches = difflib.get_close_matches(extracted_name, product_master, n=1, cutoff=0.5)
            
            matched_product = matches[0] if matches else None
            default_price = get_product_price(matched_product) if matched_product else 0.0
            
            preview_rows.append({
                "Produk (Extracted)": extracted_name,
                "Produk (Matched)": matched_product,
                "Qty": qty,
                "Harga Satuan": default_price,
                "Status": "✅ Sesuai" if matched_product else "⚠️ Tidak Dikenal"
            })
        
        preview_df = pd.DataFrame(preview_rows)
        
        st.info("Cek kembali hasil pencocokan produk. Anda bisa **mengedit** kolom 'Produk (Matched)', 'Qty', dan 'Harga Satuan' langsung pada tabel di bawah ini.")
        
        # 5. Tampilkan hasil di st.data_editor
        edited_df = st.data_editor(
            preview_df,
            column_config={
                "Produk (Extracted)": st.column_config.TextColumn(disabled=True),
                "Produk (Matched)": st.column_config.SelectboxColumn(options=product_master, required=True),
                "Status": st.column_config.TextColumn(disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            key="nlp_data_editor"
        )
        
        has_unknown = any(pd.isna(row["Produk (Matched)"]) or not row["Produk (Matched)"] for _, row in edited_df.iterrows())
        has_zero_price = any(row["Harga Satuan"] <= 0 for _, row in edited_df.iterrows())
        has_invalid_qty = any(row["Qty"] < 1 for _, row in edited_df.iterrows())
        
        if has_unknown:
            st.warning("⚠️ Ada produk yang belum terisi (Tidak Dikenal). Silakan pilih dari daftar pada kolom 'Produk (Matched)'.")
        if has_zero_price:
            st.warning("⚠️ Ada produk dengan harga 0. Silakan isi harga yang sesuai.")
            
        # 6. Tombol Konfirmasi
        if st.button("✅ Konfirmasi & Simpan Semua", disabled=(has_unknown or has_zero_price or has_invalid_qty), type="primary"):
            tanggal = datetime.today().strftime("%Y-%m-%d")
            
            for _, row in edited_df.iterrows():
                insert_transaction(
                    date=tanggal,
                    product=row["Produk (Matched)"],
                    qty=row["Qty"],
                    price=row["Harga Satuan"],
                    source='nlp'
                )
            load_data_to_session()
            del st.session_state['nlp_parsed_data']
            st.success("✅ Semua transaksi dari NLP berhasil tersimpan!")
            st.balloons()
            time.sleep(1.5)
            st.rerun()
