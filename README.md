# 🚀 RIGAZUP v2.0: ML-Powered Smart Inventory Planner

Halo! Selamat datang di repositori **RIGAZUP v2.0**. 
**RIGAZUP** adalah aplikasi perencanaan inventaris cerdas berbasis web (*Machine Learning*) yang dirancang khusus untuk membantu pelaku bisnis ritel dan UMKM di Indonesia dalam mengelola arus kas, memantau kondisi gudang, dan memprediksi kebutuhan stok (demand) di masa depan.

Dalam versi 2.0 ini, RIGAZUP telah dilengkapi dengan fitur **Sistem Kasir Terintegrasi**, **Database SQLite Lokal**, dan asisten **Gemini AI** untuk mempermudah pencatatan nota menggunakan bahasa natural.

---

## ✨ Fitur Baru di v2.0

1. **🧾 Mode Kasir (Manual & AI)**  
   Input transaksi harian secara instan. Tidak perlu lagi upload CSV setiap hari. Anda bisa menggunakan form kasir tradisional atau cukup ketik/paste nota dalam bahasa natural (contoh: "Tadi laku 5 teh pucuk harganya 3500") dan biarkan Gemini AI mengekstrak data penjualannya ke database.

2. **💾 Database SQLite Lokal**  
   Penyimpanan permanen tanpa ribet. RIGAZUP v2.0 kini memiliki `rigazup.db` sebagai *Single Source of Truth*. Segala aktivitas input, upload CSV, dan demo akan disinkronisasikan dan tidak akan hilang saat *refresh* browser.

3. **🎮 Data Demo 1-Klik**  
   Fitur *onboarding* super cepat! Hanya dengan satu klik, sistem akan diinjeksi 5.000+ baris data transaksi fiktif selama 1 tahun, memungkinkan Anda untuk langsung mencoba visualisasi BI Dashboard dan prediksi AI Forecaster tanpa harus menyiapkan data Anda sendiri.

4. **💡 AI Insight Generator & Interpretasi Model**  
   Tidak sekadar menampilkan angka metrik (MAE, RMSE, R²), asisten AI otomatis menerjemahkan kinerja algoritma ke dalam bahasa awam yang manusiawi dan memberikan saran strategis.

5. **📊 Business Intelligence & AI Forecasting (Klasik)**  
   Modul klasik yang mempertahankan algoritma Machine Learning (XGBoost, Random Forest, Linear Regression) untuk menghitung estimasi kuantitas permintaan barang di masa depan, serta visualisasi tren omset secara interaktif.

---

## 📂 Spesifikasi Dataset (Jika Menggunakan Upload CSV)

Untuk mengimpor data massal historis dari sistem lain, unggah file `dataset.csv` dengan **4 kolom wajib** berikut:
- `date` *(Format tanggal YYYY-MM-DD)*
- `product_name` *(Nama spesifik barang)*
- `quantity_sold` *(Volume/unit yang terjual)*
- `unit_price` *(Harga jual eceran)*

---

## 🛠️ Technology Stack

- **Backend/Frontend**: Python, Streamlit
- **Database**: SQLite (built-in)
- **AI & NLP**: Google Gemini API
- **Machine Learning**: Scikit-Learn, XGBoost
- **Data Processing**: Pandas, NumPy
- **Visualisasi**: Plotly

---

## 💻 Cara Menjalankan (Local Setup)

Ikuti langkah-langkah berikut untuk menjalankan RIGAZUP v2.0 secara lokal:

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/akun-anda/rigazup.git
   cd rigazup/
   ```

2. **Install dependensi Python:**
   *(Catatan: SQLite3 sudah terintegrasi secara bawaan di Python, tidak perlu instalasi tambahan)*
   ```bash
   pip install -r requirements.txt
   ```

3. **Atur API Key Gemini (Opsional, tapi wajib untuk fitur AI NLP dan Insights):**
   - Buat folder `.streamlit/` di root proyek.
   - Buat file `secrets.toml` di dalamnya dan tambahkan *key* Anda:
     ```toml
     GEMINI_API_KEY = "AIzaSy_YOUR_API_KEY_HERE"
     ```

4. **Jalankan Aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan terbuka otomatis di *browser* pada alamat `http://localhost:8501`.

---

### 👨‍💻 Pengembang

Proyek sains data, *Machine Learning*, dan *Generative AI* ini dikembangkan secara penuh oleh:

- **Rian Sholihan** (NIM: 23051204384)
- S1 Teknik Informatika, Fakultas Teknik, Universitas Negeri Surabaya
