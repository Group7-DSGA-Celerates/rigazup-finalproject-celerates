# PRODUCT REQUIREMENT DOCUMENT (PRD)

## RIGAZUP: Forecasting Penjualan dan Restock Planner Berbasis Machine Learning

**Versi:** 2.0  
**Status:** Updated PRD  
**Dataset utama:** `dataset.csv`  
**Framework aplikasi:** Python + Streamlit  
**Output utama:** Dashboard penjualan, forecasting penjualan, stock risk monitoring, dan restock planner  

---

## 1. Ringkasan Produk

**RIGAZUP** adalah aplikasi dashboard interaktif berbasis **Python** dan **Streamlit** yang digunakan untuk membantu UMKM atau toko retail kecil dalam menganalisis data penjualan, memantau performa produk, memprediksi penjualan, serta memberikan rekomendasi restock berdasarkan data historis.

Aplikasi ini menggunakan dataset utama bernama **`dataset.csv`**. Dataset tersebut berisi data penjualan produk dari beberapa tahun, dengan informasi tanggal transaksi, nama produk, kategori, jumlah terjual, harga satuan, total penjualan, dan stok setelah transaksi.

Pengembangan RIGAZUP juga mengambil ide fungsi awal dari file **`app.py`** dan **`dashboard.py`**, seperti fitur upload dataset, validasi kolom, preview data, dashboard penjualan, KPI, grafik penjualan bulanan, top produk, kategori terlaris, dan analisis jumlah barang terjual. Namun, fungsi tersebut hanya digunakan sebagai inspirasi awal dan akan dikembangkan menjadi aplikasi yang lebih rapi, modern, modular, dan sesuai kebutuhan final project.

---

## 2. Latar Belakang

UMKM dan toko retail kecil sering mengalami kesulitan dalam mengelola stok barang. Banyak keputusan restock masih dilakukan secara manual berdasarkan perkiraan atau pengalaman sebelumnya. Cara tersebut berisiko menyebabkan dua masalah utama:

1. **Stockout**, yaitu stok habis ketika permintaan masih tinggi.
2. **Overstock**, yaitu stok terlalu banyak padahal permintaan rendah.

Selain itu, pemilik usaha sering kali belum memiliki dashboard yang mudah digunakan untuk membaca performa produk, tren penjualan, dan kebutuhan stok. Oleh karena itu, RIGAZUP dibuat untuk membantu pemilik usaha melihat data penjualan secara visual, memahami produk yang paling berkontribusi terhadap revenue, memprediksi demand, dan menentukan rekomendasi restock yang lebih berbasis data.

---

## 3. Problem Statement

Bagaimana membantu UMKM atau toko retail kecil dalam menganalisis data penjualan, memprediksi permintaan produk, dan menentukan rekomendasi restock menggunakan dataset historis penjualan berbasis machine learning?

---

## 4. Tujuan Produk

Tujuan utama RIGAZUP adalah:

1. Membuat aplikasi Streamlit yang mampu membaca dataset penjualan `dataset.csv`.
2. Menampilkan dashboard penjualan yang mudah dipahami.
3. Menampilkan total penjualan, total transaksi, total unit terjual, dan jumlah produk.
4. Menampilkan tren penjualan berdasarkan waktu.
5. Menampilkan produk dengan performa penjualan terbaik.
6. Menampilkan kategori produk dengan kontribusi penjualan tertinggi.
7. Mendeteksi risiko stockout berdasarkan stok terakhir dan pola penjualan.
8. Mendeteksi potensi overstock berdasarkan stok tinggi dan penjualan rendah.
9. Membangun model machine learning untuk forecasting penjualan.
10. Membandingkan minimal 3 model machine learning.
11. Memilih model terbaik berdasarkan metrik evaluasi.
12. Menghasilkan rekomendasi restock berbasis hasil forecasting dan stok saat ini.
13. Membuat aplikasi dengan desain modern, rapi, dan memiliki value design tinggi.

---

## 5. Target User

Target pengguna RIGAZUP adalah:

1. **Pemilik UMKM**  
   Membutuhkan dashboard sederhana untuk memahami penjualan dan stok.

2. **Pemilik toko retail kecil**  
   Membutuhkan alat bantu untuk mengetahui produk mana yang perlu diprioritaskan.

3. **Staf operasional stok**  
   Membutuhkan rekomendasi restock agar pengelolaan stok lebih efisien.

4. **Manajer bisnis kecil**  
   Membutuhkan ringkasan performa produk dan kategori untuk pengambilan keputusan.

5. **Penilai final project**  
   Membutuhkan aplikasi yang menunjukkan pemahaman data, visualisasi, modeling, evaluasi model, dan implementasi Streamlit.

---

## 6. Dataset Utama

Dataset utama yang digunakan adalah:

```text
dataset.csv
```

Dataset ini berisi **5000 baris data** dan **7 kolom utama**.

---

## 7. Struktur Kolom Dataset

| Kolom | Tipe Data | Deskripsi |
|---|---|---|
| `Tanggal` | Date | Tanggal transaksi penjualan |
| `Produk` | String | Nama produk yang terjual |
| `Kategori` | String | Kategori dari produk |
| `Qty_Terjual` | Integer | Jumlah unit produk yang terjual |
| `Harga_Satuan` | Numeric | Harga satuan produk |
| `Total_Penjualan` | Numeric | Total nilai penjualan |
| `Stok_Setelah_Transaksi` | Integer | Jumlah stok setelah transaksi terjadi |

---

## 8. Perubahan dari PRD Sebelumnya

Pada PRD sebelumnya, dataset masih mengacu pada struktur 12 kolom seperti:

- `transaction_id`
- `transaction_date`
- `branch`
- `product_name`
- `category`
- `quantity_sold`
- `unit_price`
- `total_sales`
- `stock_before_sale`
- `stock_after_sale`
- `payment_method`
- `reorder_status`

Pada PRD versi update ini, struktur dataset disesuaikan dengan file **`dataset.csv`**, sehingga aplikasi harus menggunakan kolom:

1. `Tanggal`
2. `Produk`
3. `Kategori`
4. `Qty_Terjual`
5. `Harga_Satuan`
6. `Total_Penjualan`
7. `Stok_Setelah_Transaksi`

Beberapa fitur yang sebelumnya membutuhkan kolom yang tidak tersedia harus disesuaikan:

| Fitur Lama | Status Update |
|---|---|
| Analisis cabang | Dihapus dari MVP karena tidak ada kolom cabang |
| Analisis metode pembayaran | Dihapus dari MVP karena tidak ada kolom payment method |
| Reorder status | Diganti dengan perhitungan risiko berbasis stok dan penjualan |
| Stock before sale | Dihapus karena tidak tersedia |
| Forecasting per cabang | Dihapus dari MVP |
| Forecasting per produk/kategori | Tetap digunakan |
| Restock planner | Tetap digunakan, dihitung dari forecast demand dan stok setelah transaksi |

---

## 9. Ide Fungsi dari `app.py` dan `dashboard.py`

File `app.py` dan `dashboard.py` digunakan sebagai referensi ide awal, bukan sebagai final code yang wajib dipertahankan.

### 9.1 Ide dari `app.py`

Fungsi yang dijadikan ide:

1. Halaman awal aplikasi.
2. Upload file CSV.
3. Validasi kolom dataset.
4. Menampilkan preview dataset.
5. Menyimpan dataset ke session state.
6. Menghapus dataset dari session state.
7. Menjelaskan fitur utama aplikasi:
   - Dashboard Penjualan
   - Forecasting Penjualan
   - Restock Planner
   - AI Insight Generator

### 9.2 Ide dari `dashboard.py`

Fungsi yang dijadikan ide:

1. Menampilkan preview dataset.
2. Mengubah kolom `Tanggal` menjadi datetime.
3. Membuat kolom waktu:
   - `Tahun`
   - `Bulan`
   - `Hari`
4. Menampilkan KPI:
   - Total Penjualan
   - Total Transaksi
   - Total Unit Terjual
   - Jumlah Produk
5. Menampilkan total penjualan per bulan.
6. Menampilkan total penjualan per tahun.
7. Menampilkan top 10 produk terlaris.
8. Menampilkan kategori terlaris.
9. Menampilkan jumlah barang terjual per kategori.
10. Menampilkan total unit terjual per bulan.
11. Menambahkan filter tahun.

### 9.3 Pengembangan dari Ide Awal

Fungsi dari `app.py` dan `dashboard.py` akan dikembangkan menjadi:

1. Struktur project yang lebih modular.
2. Validasi dataset yang lebih kuat.
3. Error handling yang lebih aman.
4. Dashboard yang lebih modern.
5. Visualisasi yang lebih informatif.
6. Forecasting berbasis machine learning.
7. Restock planner berbasis hasil prediksi.
8. AI insight generator sebagai fitur opsional.
9. Desain aplikasi dengan custom CSS agar tidak terlihat seperti Streamlit default.

---

## 10. Value Proposition

RIGAZUP memberikan nilai utama berupa:

1. **Membantu membaca performa penjualan secara cepat**  
   User dapat melihat total penjualan, jumlah transaksi, jumlah unit terjual, dan jumlah produk.

2. **Membantu memahami tren penjualan**  
   User dapat melihat pola penjualan berdasarkan bulan dan tahun.

3. **Membantu mengetahui produk terlaris**  
   User dapat melihat produk dengan kontribusi penjualan tertinggi.

4. **Membantu menentukan kategori prioritas**  
   User dapat mengetahui kategori yang menghasilkan revenue paling besar.

5. **Membantu mengurangi risiko stockout**  
   Produk dengan stok rendah dan penjualan tinggi dapat diberi label risiko.

6. **Membantu mengurangi overstock**  
   Produk dengan stok tinggi tetapi penjualan rendah dapat terdeteksi.

7. **Membantu membuat keputusan restock berbasis data**  
   Rekomendasi restock dihitung berdasarkan forecast demand dan stok saat ini.

8. **Mudah digunakan oleh user non-teknis**  
   User cukup upload dataset, membaca dashboard, menjalankan forecasting, dan melihat rekomendasi restock.

---

## 11. Scope Produk

### 11.1 In Scope

Fitur yang masuk dalam ruang lingkup RIGAZUP:

1. Upload dataset CSV.
2. Validasi kolom wajib dataset.
3. Preview dataset.
4. Data quality checking.
5. Data preprocessing.
6. Dashboard KPI penjualan.
7. Analisis tren penjualan bulanan dan tahunan.
8. Analisis produk terlaris.
9. Analisis kategori dengan penjualan tertinggi.
10. Analisis jumlah unit terjual.
11. Deteksi risiko stockout.
12. Deteksi potensi overstock.
13. Forecasting penjualan produk.
14. Perbandingan minimal 3 model machine learning.
15. Evaluasi model dengan MAE, RMSE, dan MAPE.
16. Pemilihan model terbaik otomatis.
17. Rekomendasi restock.
18. Export hasil rekomendasi ke CSV.
19. Desain Streamlit modern dengan custom CSS.
20. Deployment ke Streamlit Cloud.

### 11.2 Out of Scope

Fitur yang tidak masuk MVP:

1. Login user.
2. Multi-role user.
3. Database PostgreSQL sebagai backend aplikasi utama.
4. Integrasi real-time dengan kasir.
5. Integrasi supplier.
6. Analisis cabang.
7. Analisis metode pembayaran.
8. Forecasting per cabang.
9. Notifikasi WhatsApp atau email.
10. Sistem inventory management full-scale.
11. Integrasi API eksternal.
12. PDF report otomatis.

---

## 12. User Flow

Alur utama aplikasi:

```text
User membuka aplikasi
        ↓
User melihat landing page RIGAZUP
        ↓
User upload dataset.csv
        ↓
Sistem validasi kolom dataset
        ↓
Sistem menampilkan preview dataset
        ↓
User membuka Data Quality
        ↓
Sistem melakukan preprocessing
        ↓
User membuka Sales Dashboard
        ↓
User melihat KPI dan visualisasi penjualan
        ↓
User membuka Stock Risk Monitoring
        ↓
Sistem menampilkan risiko stockout dan overstock
        ↓
User membuka Forecasting
        ↓
Sistem menjalankan 3 model machine learning
        ↓
Sistem memilih model terbaik
        ↓
User membuka Restock Planner
        ↓
Sistem menghasilkan rekomendasi restock
        ↓
User download hasil rekomendasi
```

---

## 13. Fitur Produk

### 13.1 Landing Page / Overview

#### Tujuan

Memberikan gambaran awal tentang fungsi RIGAZUP.

#### Komponen

1. Hero section.
2. Judul: **RIGAZUP**
3. Subtitle: **Forecasting Penjualan dan Restock Planner Berbasis Machine Learning**
4. Deskripsi singkat aplikasi.
5. Value cards:
   - Dashboard Penjualan
   - Forecasting Penjualan
   - Restock Planner
   - AI Insight Generator
6. Informasi singkat alur penggunaan aplikasi.

#### Acceptance Criteria

1. User langsung memahami fungsi aplikasi.
2. Tampilan terlihat rapi dan profesional.
3. Landing page tidak terlihat seperti Streamlit default.

---

### 13.2 Upload Dataset

#### Tujuan

Memungkinkan user mengunggah file `dataset.csv`.

#### Functional Requirements

1. User dapat upload file CSV.
2. Sistem membaca dataset menggunakan pandas.
3. Sistem memvalidasi kolom wajib:
   - `Tanggal`
   - `Produk`
   - `Kategori`
   - `Qty_Terjual`
   - `Harga_Satuan`
   - `Total_Penjualan`
   - `Stok_Setelah_Transaksi`
4. Sistem menampilkan preview dataset.
5. Sistem menampilkan jumlah baris dan kolom.
6. Sistem menampilkan daftar kolom dataset.
7. Sistem menyimpan data ke session state.
8. User dapat menghapus dataset dari session state.

#### Acceptance Criteria

1. Jika kolom tidak lengkap, sistem menampilkan error.
2. Jika dataset valid, sistem menampilkan success message.
3. Dataset tersimpan dan bisa dipakai halaman lain.
4. Aplikasi tidak crash jika user belum upload dataset.

---

### 13.3 Data Quality & Preprocessing

#### Tujuan

Memastikan dataset siap digunakan untuk dashboard dan machine learning.

#### Functional Requirements

1. Mengubah `Tanggal` menjadi datetime.
2. Membuat kolom:
   - `Tahun`
   - `Bulan`
   - `Hari`
   - `Nama_Hari`
3. Mengecek missing value.
4. Mengecek data duplikat.
5. Mengecek nilai negatif pada:
   - `Qty_Terjual`
   - `Harga_Satuan`
   - `Total_Penjualan`
   - `Stok_Setelah_Transaksi`
6. Mengecek kesesuaian:
   - `Total_Penjualan = Qty_Terjual × Harga_Satuan`
7. Membuat kolom:
   - `Total_Penjualan_Hitung`
   - `Selisih_Total_Penjualan`
8. Menyimpan hasil preprocessing ke session state.

#### Acceptance Criteria

1. Data berhasil diproses.
2. User dapat melihat status kualitas data.
3. Data hasil preprocessing digunakan oleh dashboard, forecasting, dan restock planner.

---

### 13.4 Sales Dashboard

#### Tujuan

Menampilkan performa penjualan secara visual dan interaktif.

#### Functional Requirements

1. Menampilkan KPI:
   - Total Penjualan
   - Total Transaksi
   - Total Unit Terjual
   - Jumlah Produk
   - Produk dengan penjualan tertinggi
   - Kategori dengan revenue tertinggi
2. Menampilkan visualisasi:
   - Total Penjualan per Bulan
   - Total Penjualan per Tahun
   - Top 10 Produk Terlaris
   - Kategori Terlaris
   - Jumlah Barang Terjual per Kategori
   - Total Unit Terjual per Bulan
3. Menyediakan filter:
   - Tahun
   - Kategori
   - Produk
   - Rentang tanggal
4. Semua grafik harus mengikuti filter yang dipilih.

#### Acceptance Criteria

1. Dashboard menampilkan insight utama dari dataset.
2. Filter berjalan dengan baik.
3. Grafik interaktif menggunakan Plotly.
4. Jika data kosong setelah filter, sistem menampilkan warning.

---

### 13.5 Product Analysis

#### Tujuan

Menganalisis performa produk secara lebih detail.

#### Functional Requirements

1. Menampilkan ranking produk berdasarkan:
   - Total Penjualan
   - Qty_Terjual
   - Frekuensi transaksi
   - Rata-rata penjualan
   - Stok rata-rata setelah transaksi
2. Menampilkan:
   - Top produk berdasarkan revenue
   - Top produk berdasarkan unit terjual
   - Produk dengan performa rendah
3. Menampilkan insight otomatis sederhana:
   - Produk terlaris
   - Produk dengan revenue tertinggi
   - Produk dengan unit terjual tertinggi
   - Produk dengan stok tinggi tetapi penjualan rendah

#### Acceptance Criteria

1. User dapat melihat produk prioritas.
2. Analisis produk dapat digunakan untuk mendukung restock planner.
3. Data ditampilkan dalam chart dan tabel yang mudah dibaca.

---

### 13.6 Stockout & Overstock Monitoring

#### Tujuan

Mendeteksi produk yang berisiko kekurangan stok atau kelebihan stok.

#### Functional Requirements

1. Menghitung ringkasan stok per produk:
   - Total `Qty_Terjual`
   - Rata-rata `Qty_Terjual`
   - Total `Total_Penjualan`
   - Jumlah Transaksi
   - Stok Terakhir
   - Rata-rata Stok Setelah Transaksi
2. Menghitung risiko stockout.
3. Menghitung risiko overstock.
4. Memberikan label risiko:
   - Low
   - Medium
   - High
5. Menampilkan produk dengan risiko stockout tertinggi.
6. Menampilkan produk dengan potensi overstock tertinggi.
7. Menampilkan rekomendasi tindakan sederhana.

#### Logic Awal Stockout Risk

Produk dianggap berisiko stockout jika:

1. Stok terakhir rendah.
2. Rata-rata penjualan tinggi.
3. Jumlah transaksi tinggi.

#### Logic Awal Overstock Risk

Produk dianggap berisiko overstock jika:

1. Stok terakhir tinggi.
2. Rata-rata penjualan rendah.
3. Jumlah transaksi rendah.

#### Acceptance Criteria

1. Sistem dapat menampilkan daftar produk berisiko.
2. Risk badge mudah dibaca.
3. User dapat memahami produk mana yang perlu segera di-restock atau dikurangi restock-nya.

---

### 13.7 Forecasting Penjualan

#### Tujuan

Memprediksi jumlah penjualan produk pada periode berikutnya.

#### Functional Requirements

1. User dapat memilih:
   - Produk
   - Kategori
   - Periode forecasting
2. Sistem menyiapkan data modeling berdasarkan `Tanggal`, `Produk`, `Kategori`, dan `Qty_Terjual`.
3. Sistem melakukan agregasi penjualan harian atau bulanan.
4. Sistem membuat fitur waktu:
   - `Tahun`
   - `Bulan`
   - `Hari`
   - `Nama_Hari`
5. Sistem membuat fitur tambahan:
   - Lag sales
   - Rolling average
   - Encoded product
   - Encoded category
6. Sistem menjalankan minimal 3 model:
   - Linear Regression
   - Random Forest Regressor
   - XGBoost Regressor
7. Sistem mengevaluasi model menggunakan:
   - MAE
   - RMSE
   - MAPE
8. Sistem memilih model terbaik secara otomatis.
9. Sistem menampilkan grafik actual vs predicted.
10. Sistem menampilkan forecast demand.

#### Acceptance Criteria

1. Minimal 3 model berhasil diuji.
2. Model terbaik dipilih berdasarkan metrik evaluasi.
3. Forecast demand dapat digunakan untuk restock planner.
4. Jika data produk terlalu sedikit, sistem menampilkan warning.

---

### 13.8 Model Comparison

#### Tujuan

Menampilkan transparansi hasil evaluasi model.

#### Functional Requirements

1. Menampilkan tabel evaluasi model:
   - Model
   - MAE
   - RMSE
   - MAPE
2. Menampilkan model terbaik.
3. Menampilkan grafik perbandingan error.
4. Memberikan penjelasan sederhana tentang metrik:
   - MAE semakin kecil semakin baik.
   - RMSE semakin kecil semakin baik.
   - MAPE semakin kecil semakin baik.

#### Acceptance Criteria

1. Penilai dapat melihat bahwa aplikasi menguji minimal 3 model.
2. Model terbaik dapat dijelaskan secara sederhana.
3. Model terbaik digunakan untuk forecasting utama.

---

### 13.9 Restock Planner

#### Tujuan

Memberikan rekomendasi jumlah restock berdasarkan forecast demand dan stok saat ini.

#### Formula Rekomendasi Restock

```text
recommended_restock = max(0, forecast_demand + safety_stock - current_stock)
```

Keterangan:

| Variabel | Deskripsi |
|---|---|
| `forecast_demand` | Prediksi jumlah permintaan produk |
| `safety_stock` | Cadangan stok minimum |
| `current_stock` | Stok terakhir dari `Stok_Setelah_Transaksi` |
| `recommended_restock` | Jumlah produk yang disarankan untuk restock |

#### Functional Requirements

1. User memilih produk.
2. User memilih kategori.
3. User mengatur safety stock.
4. Sistem mengambil forecast demand.
5. Sistem mengambil current stock dari `Stok_Setelah_Transaksi`.
6. Sistem menghitung recommended restock.
7. Sistem menampilkan priority level:
   - Low
   - Medium
   - High
8. Sistem memberikan alasan rekomendasi.
9. Sistem menampilkan tabel rekomendasi untuk semua produk.
10. User dapat download hasil rekomendasi ke CSV.

#### Acceptance Criteria

1. Nilai restock tidak boleh negatif.
2. Produk prioritas tinggi muncul di bagian atas.
3. Rekomendasi mudah dipahami user.
4. Hasil dapat diunduh.

---

### 13.10 AI Insight Generator

#### Status

Fitur ini masuk kategori **Nice-to-Have**, bukan MVP utama.

#### Tujuan

Memberikan ringkasan insight otomatis berdasarkan hasil dashboard, forecasting, dan restock planner.

#### Functional Requirements Opsional

1. Menghasilkan ringkasan performa penjualan.
2. Menghasilkan insight produk terlaris.
3. Menghasilkan insight kategori paling potensial.
4. Menghasilkan rekomendasi bisnis sederhana.
5. Menghasilkan warning stok.

#### Catatan

Jika waktu pengerjaan terbatas, fitur ini cukup dibuat sebagai **rule-based insight generator**, tidak wajib memakai API LLM.

Contoh output:

- Produk dengan penjualan tertinggi adalah X.
- Kategori dengan kontribusi revenue terbesar adalah Y.
- Produk Z memiliki risiko stockout karena stok rendah dan rata-rata penjualan tinggi.
- Produk A berpotensi overstock karena stok tinggi tetapi penjualan rendah.

---

## 14. Machine Learning Requirement

### 14.1 Pendekatan

RIGAZUP menggunakan pendekatan **predictive modeling** untuk forecasting penjualan.

### 14.2 Target Prediksi

Target prediksi utama:

```text
Qty_Terjual
```

### 14.3 Fitur Modeling

Fitur yang dapat digunakan:

1. `Tahun`
2. `Bulan`
3. `Hari`
4. `Nama_Hari`
5. Produk encoded
6. Kategori encoded
7. `Harga_Satuan`
8. `Total_Penjualan`
9. `Stok_Setelah_Transaksi`
10. Lag `Qty_Terjual`
11. Rolling Mean `Qty_Terjual`

### 14.4 Model yang Diuji

Minimal 3 model:

1. **Linear Regression**  
   Sebagai baseline model.

2. **Random Forest Regressor**  
   Untuk menangkap pola non-linear.

3. **XGBoost Regressor**  
   Untuk model boosting yang lebih kuat.

### 14.5 Evaluation Metrics

Metrik evaluasi:

1. **MAE**
2. **RMSE**
3. **MAPE**

### 14.6 Model Selection

Model terbaik dipilih berdasarkan:

1. MAPE paling rendah.
2. Jika MAPE tidak valid, gunakan RMSE paling rendah.
3. Jika hasil terlalu tidak stabil, gunakan model yang paling konsisten pada data testing.

---

## 15. Design Requirement

RIGAZUP harus memiliki tampilan yang rapi, modern, dan profesional. Aplikasi tidak boleh terlihat seperti Streamlit default.

### 15.1 Style

Gaya desain:

1. Modern business dashboard.
2. Clean layout.
3. Rounded card.
4. Soft shadow.
5. Gradient accent.
6. Spacing rapi.
7. Font mudah dibaca.
8. Warna konsisten.
9. Visualisasi tidak terlalu ramai.

### 15.2 Color Palette

| Fungsi | Warna |
|---|---|
| Primary | Navy / Deep Blue |
| Accent | Cyan / Electric Blue |
| Background | Soft Gray |
| Card | White |
| Success | Green |
| Warning | Orange |
| Danger | Red |
| Text Primary | Dark Navy |
| Text Secondary | Gray |

### 15.3 Komponen UI

Komponen yang harus tersedia:

1. Sidebar navigation.
2. Hero section.
3. KPI card.
4. Metric card.
5. Chart container.
6. Risk badge.
7. Info box.
8. Warning box.
9. Data table.
10. Download button.
11. Model comparison table.
12. Restock recommendation card.

---

## 16. Struktur Halaman Aplikasi

Rekomendasi halaman:

1. **Overview**
2. **Upload Dataset**
3. **Data Quality**
4. **Sales Dashboard**
5. **Product Analysis**
6. **Stock Risk Monitoring**
7. **Forecasting**
8. **Model Comparison**
9. **Restock Planner**
10. **AI Insight Generator**
11. **About Project**

---

## 17. Struktur Folder Project

```text
rigazup/
│
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_SPEC.md
│
├── data/
│   └── dataset.csv
│
├── models/
│   └── .gitkeep
│
├── pages/
│   ├── 1_upload_dataset.py
│   ├── 2_data_quality.py
│   ├── 3_sales_dashboard.py
│   ├── 4_product_analysis.py
│   ├── 5_stock_risk.py
│   ├── 6_forecasting.py
│   ├── 7_model_comparison.py
│   ├── 8_restock_planner.py
│   ├── 9_ai_insight_generator.py
│   └── 10_about_project.py
│
├── src/
│   ├── validation.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── visualization.py
│   ├── modeling.py
│   ├── evaluation.py
│   ├── restock.py
│   └── insight_generator.py
│
└── assets/
    ├── style.css
    └── logo.png
```

---

## 18. Tech Stack

| Kebutuhan | Teknologi |
|---|---|
| Bahasa utama | Python |
| Framework aplikasi | Streamlit |
| Data processing | pandas, numpy |
| Visualisasi | Plotly |
| Machine learning | scikit-learn, xgboost |
| Model saving | joblib |
| Deployment | Streamlit Cloud |
| Version control | GitHub |

---

## 19. Functional Requirement Summary

| Kode | Requirement | Prioritas |
|---|---|---|
| FR-001 | User dapat upload `dataset.csv` | Must Have |
| FR-002 | Sistem validasi 7 kolom wajib | Must Have |
| FR-003 | Sistem menampilkan preview dataset | Must Have |
| FR-004 | Sistem melakukan preprocessing data | Must Have |
| FR-005 | Sistem menampilkan KPI penjualan | Must Have |
| FR-006 | Sistem menampilkan tren penjualan bulanan | Must Have |
| FR-007 | Sistem menampilkan top produk | Must Have |
| FR-008 | Sistem menampilkan kategori terlaris | Must Have |
| FR-009 | Sistem menampilkan jumlah unit terjual | Must Have |
| FR-010 | Sistem mendeteksi risiko stockout | Must Have |
| FR-011 | Sistem mendeteksi potensi overstock | Must Have |
| FR-012 | Sistem menjalankan minimal 3 model ML | Must Have |
| FR-013 | Sistem mengevaluasi model dengan MAE, RMSE, MAPE | Must Have |
| FR-014 | Sistem memilih model terbaik | Must Have |
| FR-015 | Sistem menghasilkan forecast demand | Must Have |
| FR-016 | Sistem menghasilkan rekomendasi restock | Must Have |
| FR-017 | User dapat download hasil rekomendasi | Should Have |
| FR-018 | Sistem memiliki UI modern | Must Have |
| FR-019 | AI insight generator sederhana | Nice to Have |
| FR-020 | Aplikasi deploy ke Streamlit Cloud | Must Have |

---

## 20. Non-Functional Requirements

| Kategori | Requirement |
|---|---|
| Usability | Aplikasi mudah digunakan oleh user non-teknis |
| Performance | Dataset 5000 baris harus dapat diproses dengan cepat |
| Reliability | Sistem tidak crash saat dataset belum diupload |
| Maintainability | Kode modular dan mudah dikembangkan |
| Readability | Nama variabel menggunakan snake_case |
| Design | Tampilan modern dan tidak seperti Streamlit default |
| Deployment | Aplikasi dapat berjalan di Streamlit Cloud |
| Error Handling | Pesan error harus jelas dan user-friendly |

---

## 21. Acceptance Criteria Utama

Produk dinyatakan selesai apabila:

1. Aplikasi dapat dijalankan dengan `streamlit run app.py`.
2. User dapat upload `dataset.csv`.
3. Sistem memvalidasi 7 kolom wajib.
4. Sistem menampilkan preview dataset.
5. Sistem melakukan preprocessing.
6. Dashboard menampilkan KPI utama.
7. Dashboard menampilkan grafik penjualan bulanan.
8. Dashboard menampilkan top produk.
9. Dashboard menampilkan kategori terlaris.
10. Product analysis tersedia.
11. Stockout monitoring tersedia.
12. Overstock monitoring tersedia.
13. Forecasting berjalan menggunakan minimal 3 model.
14. Evaluasi model menggunakan MAE, RMSE, dan MAPE.
15. Model terbaik dipilih otomatis.
16. Restock planner menghasilkan rekomendasi restock.
17. Hasil rekomendasi dapat diunduh dalam CSV.
18. UI terlihat modern, rapi, dan profesional.
19. Aplikasi siap deploy ke Streamlit Cloud.

---

## 22. MVP Scope

Fitur minimum yang wajib selesai:

1. Upload dataset.
2. Validasi kolom dataset.
3. Data preprocessing.
4. Sales dashboard.
5. Product analysis.
6. Stockout monitoring.
7. Overstock monitoring.
8. Forecasting dengan 3 model.
9. Model comparison.
10. Restock planner.
11. Download rekomendasi CSV.
12. UI polishing.
13. Deployment preparation.

---

## 23. Nice-to-Have Features

Fitur tambahan jika waktu cukup:

1. AI Insight Generator.
2. Dark mode.
3. What-if restock simulation.
4. Download report PDF.
5. Forecasting per kategori.
6. Insight otomatis per tahun.
7. Executive summary otomatis.
8. Rekomendasi strategi bisnis sederhana.

---

## 24. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Dataset hanya memiliki 7 kolom | Fitur cabang dan payment tidak bisa dibuat | Fokus analisis produk, kategori, waktu, dan stok |
| Forecasting produk tertentu datanya sedikit | Model kurang akurat | Beri warning dan gunakan agregasi bulanan |
| XGBoost error saat deployment | Aplikasi gagal berjalan | Siapkan fallback ke Random Forest |
| UI terlihat default | Nilai aplikasi turun | Gunakan custom CSS dan layout premium |
| Restock terlalu sederhana | Kurang bernilai bisnis | Tambahkan safety stock dan priority level |
| Filter menghasilkan data kosong | Aplikasi error | Tampilkan warning yang jelas |

---

## 25. Timeline Pengembangan

| Tahap | Aktivitas | Output |
|---|---|---|
| 1 | Setup project | Struktur folder dan `app.py` |
| 2 | UI global | Style CSS dan landing page |
| 3 | Upload dataset | Upload dan validasi CSV |
| 4 | Data quality | Preprocessing dan validasi data |
| 5 | Dashboard | KPI dan visualisasi utama |
| 6 | Product analysis | Analisis produk dan kategori |
| 7 | Stock risk | Stockout dan overstock monitoring |
| 8 | Feature engineering | Dataset modeling |
| 9 | Modeling | 3 model ML |
| 10 | Evaluation | MAE, RMSE, MAPE |
| 11 | Forecasting page | Actual vs predicted |
| 12 | Restock planner | Rekomendasi restock |
| 13 | AI insight | Insight otomatis sederhana |
| 14 | UI polishing | Tampilan final |
| 15 | Testing | Error handling |
| 16 | Deployment | Streamlit Cloud |

---

## 26. Definition of Done

Project dianggap selesai jika:

1. Semua fitur MVP berjalan.
2. Tidak ada error saat membuka halaman aplikasi secara acak.
3. Dataset dapat diupload dan divalidasi.
4. Dashboard dapat menampilkan insight utama.
5. Forecasting dapat menjalankan minimal 3 model.
6. Model comparison menampilkan MAE, RMSE, dan MAPE.
7. Restock planner dapat menghasilkan rekomendasi.
8. UI sudah terlihat modern.
9. Project siap dijalankan lokal dan siap deploy.
10. Dokumentasi README sudah lengkap.

---

## 27. Kesimpulan PRD Update

PRD versi update ini menyesuaikan RIGAZUP dengan dataset utama **`dataset.csv`** yang memiliki 7 kolom penjualan. Aplikasi tidak lagi bergantung pada kolom lama seperti cabang, metode pembayaran, transaction_id, stock_before_sale, dan reorder_status.

Fungsi dari file `app.py` dan `dashboard.py` digunakan sebagai inspirasi awal, terutama untuk upload dataset, validasi kolom, preview data, KPI penjualan, grafik penjualan bulanan, top produk, kategori terlaris, dan jumlah unit terjual. Namun, pengembangan final harus dibuat lebih baik melalui struktur modular, desain modern, forecasting machine learning, model comparison, stock risk monitoring, dan restock planner.

Dengan PRD ini, RIGAZUP tetap sesuai sebagai final project Data Science berbasis Streamlit karena mencakup data preprocessing, eksplorasi data, visualisasi, machine learning, evaluasi model, integrasi aplikasi, dan rekomendasi bisnis berbasis data.
