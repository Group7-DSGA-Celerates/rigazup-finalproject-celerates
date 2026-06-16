# 🚀 RIGAZUP: Sistem ERP Mini & AI Forecaster untuk UMKM

Halo! Selamat datang di repositori **RIGAZUP**. 
**RIGAZUP** adalah *dashboard* berbasis web (SaaS) yang dirancang khusus untuk membantu pelaku bisnis ritel dan UMKM dalam mengelola arus kas, memantau kondisi gudang, serta memprediksi masa depan penjualannya.

Aplikasi ini dipersenjatai dengan *Machine Learning* untuk memprediksi kapan barang akan habis dan otomatis meracik rekomendasi belanja barang. Semua informasi disajikan dalam antarmuka modern yang rapi, *sleek*, dan sangat mudah digunakan.

---

## 💡 Latar Belakang Proyek

Banyak pengusaha yang sering mengalami kesulitan dalam mengontrol perputaran barang di gudang. 
Kekurangan stok (*stockout*) menyebabkan hilangnya potensi penjualan, sedangkan penumpukan stok (*overstock*) menahan modal kas dan memperbesar risiko barang rusak. 

Oleh karena itu, **RIGAZUP** dikembangkan sebagai solusi analitik untuk menjembatani ketidakpastian *supply and demand* tersebut melalui perhitungan matematika dan *Machine Learning*. Pendekatan berbasis data ini memastikan perencanaan bisnis yang lebih akurat tanpa harus menebak-nebak.

---

## ✨ Fitur Utama Aplikasi

1. **🧹 Data Quality Studio**  
   Pembersihan data otomatis dari *missing values* serta pendeteksian anomali data ekstrem guna memastikan dataset yang akan diproses oleh AI dalam kondisi bersih dan reliabel.
   
2. **📊 Business Intelligence Dashboard**  
   Memantau indikator kinerja bisnis (KPI) secara terpusat, mulai dari tren omset, peringkat produk paling laris, hingga komposisi kategori penjualan, yang disajikan melalui grafik interaktif.
   
3. **📈 AI Forecasting**  
   Mesin prediktif cerdas (*Machine Learning*) yang meramalkan estimasi kuantitas permintaan barang di masa depan menggunakan kombinasi algoritma unggulan seperti *XGBoost*, *Random Forest*, dan *Linear Regression*.
   
4. **📦 Inventory Management & Restock Planner**  
   Mengkalkulasi batas *Safety Stock* harian dan memberikan peringatan dini terhadap risiko barang habis (*Stockout*) atau penumpukan barang di gudang (*Overstock*), sekaligus merekomendasikan jumlah belanja logistik.
   
5. **🧠 AI Insight Generator**  
   Sistem asisten virtual analitik yang otomatis menerjemahkan grafik dan angka numerik menjadi sebuah narasi ringkasan eksekutif yang deskriptif dan strategis.
   
6. **⚖️ Model Comparison**  
   Transparansi performa di balik layar, memungkinkan pengguna membandingkan secara ilmiah tingkat keakuratan masing-masing algoritma prediksi melalui evaluasi metrik *Mean Absolute Error* (MAE) dan *Root Mean Square Error* (RMSE).

---

## 📂 Spesifikasi Dataset

Untuk menjalankan aplikasi ini, Anda cukup mengunggah file `dataset.csv` dengan 7 kolom inti berikut:
- `Tanggal` *(Waktu terjadinya transaksi)*
- `Produk` *(Nama spesifik barang)*
- `Kategori` *(Grup klasifikasi barang)*
- `Qty_Terjual` *(Volume/unit yang terjual)*
- `Harga_Satuan` *(Harga jual eceran)*
- `Total_Penjualan` *(Total transaksi / omset)*
- `Stok_Setelah_Transaksi` *(Sisa stok aktual barang di gudang)*

> **Catatan:** Jika data Harga Pokok (modal) tidak tersedia, sistem memiliki *fallback* otomatis yang mengasumsikan margin keuntungan standar (30%) agar kalkulator keuangan tetap berfungsi.

---

## 🛠️ Teknologi Pendukung

Aplikasi ini dibangun menggunakan bahasa Python dan beberapa pustaka *Data Science* terkemuka:
- **Streamlit**: *Framework* antarmuka web yang interaktif.
- **Pandas & Numpy**: Mesin utama untuk komputasi matriks dan pemrosesan data.
- **Plotly**: Modul pembuat grafik analitik yang dinamis.
- **Scikit-Learn & XGBoost**: Mesin kecerdasan buatan untuk pemodelan prediksi.

---

## 💻 Cara Menjalankan Secara Lokal (Local Development)

Jika Anda ingin menjalankan aplikasi ini di komputer sendiri, ikuti langkah berikut:

1. *Clone* repositori ini ke komputer Anda.
   ```bash
   git clone https://github.com/akun-anda/rigazup.git
   cd rigazup/
   ```
2. Pastikan Python sudah terinstal, lalu pasang pustaka yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi melalui Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Aplikasi akan otomatis terbuka di *browser* Anda pada alamat `http://localhost:8501`.

---

## ☁️ Panduan Hosting Gratis (Streamlit Cloud)

RIGAZUP didesain tanpa menggunakan *database* eksternal (*stateless*), sehingga sangat mudah diunggah secara gratis.
1. Dorong (*Push*) kode Anda ke *repository* GitHub publik.
2. Masuk ke [Streamlit Community Cloud](https://share.streamlit.io/).
3. Klik **New App**, hubungkan dengan GitHub Anda, lalu pilih repositori `rigazup`.
4. Isi isian *Main file path* dengan `app.py`.
5. Klik **Deploy!** dan tunggu beberapa saat hingga proses instalasi selesai. 
6. Selesai! Tautan aplikasi Anda sudah aktif dan siap digunakan oleh tim bisnis Anda.

---

### 👨‍💻 Tim Pengembang (Kelompok 7)

Proyek sains data dan *Machine Learning* ini dikembangkan secara kolaboratif oleh mahasiswa dari **Universitas Negeri Surabaya**:

- **Rian Sholihan** (NIM: 23051204384)
- **Maulana Jalba Rizka** (NIM: 23051204369)
- **Muhammad Thorieq Alfareza** (NIM: 23051204363)
- **Ryan Ferdiansyah Risnayadi** (NIM: 23051204302)
- **Muhammad Danil Ma'ruf** (NIM: 23051204290)
