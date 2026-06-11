# RIGAZUP: Forecasting Penjualan dan Restock Planner Berbasis Machine Learning

## Deskripsi Singkat
**RIGAZUP** adalah aplikasi cerdas (*dashboard* SaaS) yang membantu pelaku bisnis dan ritel untuk mengendalikan tingkat persediaan barang di gudang. Aplikasi ini memanfaatkan arsitektur algoritma Kecerdasan Buatan (AI) untuk melakukan peramalan (*forecasting*) penjualan dan memberikan jadwal rekomendasi restock (belanja barang) secara otomatis dan sangat presisi.

## Latar Belakang
Kesulitan dalam menyeimbangkan persediaan barang seringkali menjadi sumber kebocoran finansial bagi para pengusaha. Kekurangan stok (*stockout*) menyebabkan hilangnya potensi penjualan dan merusak retensi kepercayaan pelanggan, sedangkan kelebihan stok (*overstock*) akan menahan likuiditas modal kas dan memperparah risiko penyusutan nilai barang. Oleh karena itu, pendekatan berbasis *Machine Learning* sangat dibutuhkan untuk menjembatani ketidakpastian *supply and demand* ini.

## Tujuan
1. Memvisualisasikan performa penjualan operasional dan kesehatan metrik gudang secara interaktif.
2. Memprediksi tingkat penjualan (*demand*) masa depan menggunakan sistem lelang akurasi (*Model Comparison*).
3. Merumuskan rekomendasi "Restock Planner" per spesifik SKU untuk mencegah kerugian finansial.

## Fitur Utama Terintegrasi
1. **Business Dashboard**: Visualisasi ringkasan omset dan grafik penjualan dinamis berbasis waktu.
2. **Product Analysis**: Melacak klasifikasi matriks produk terlaris dan paling menguntungkan.
3. **Stock Risk Monitoring**: Detektor barang mana yang rawan habis (*High Risk Stockout*) dan yang menumpuk tak terjual (*Overstock*).
4. **Machine Learning Forecasting**: Mesin pemroses kecerdasan buatan (*auto-ML*) tanpa keharusan *coding* manual.
5. **Model Comparison**: Papan skor objektif untuk mendemonstrasikan transparansi pemilihan model terbaik berdasarkan skor kesalahan terkecil.
6. **Restock Planner**: Kalkulator sistem yang merancang logistik gudang: *berapa banyak unit yang wajib dibeli minggu ini?*
7. **AI Insight Generator**: Narator otomatis yang mengekstrak ribuan baris matriks angka menjadi narasi *actionable* berbahasa Indonesia sehari-hari.

## Spesifikasi Format Dataset
Dataset yang dikonsumsi aplikasi ini mengandalkan standar *file* tabular berbentuk `dataset.csv`.  
Setiap set data wajib mengandung struktur 7 kolom inti di bawah ini:
- `Tanggal` *(Waktu transaksi dilakukan)*
- `Produk` *(Nama spesifik barang)*
- `Kategori` *(Grup departemen penjualan)*
- `Qty_Terjual` *(Volume/kuantitas yang dilepas)*
- `Harga_Satuan` *(Nilai eceran produk)*
- `Total_Penjualan` *(Akumulasi revenue kasir)*
- `Stok_Setelah_Transaksi` *(Log pencatatan perpindahan stok aktual)*

## Teknologi yang Digunakan
Keseluruhan infrastruktur RIGAZUP dijalankan menggunakan fondasi bahasa Python berserta kapabilitas ekosistem komputasi ilmiahnya:
- **Python**: Bahasa landasan (*Core*).
- **Streamlit**: *Framework Backend* dan *Frontend UI/UX Reactive*.
- **pandas**: Mesin manipulasi DataFrame berkinerja tinggi.
- **numpy**: *Library* operasional komputasi aljabar kompleks.
- **plotly**: Modul visualisasi analitik interaktif kelas-industri.
- **scikit-learn**: Induk permesinan algoritma pembelajaran terstruktur (Linear Regression & Random Forest).
- **xgboost**: Eksekutor algoritma gradien penambah mutakhir (*Gradient Boosting*).

## Struktur Folder Repositori
```text
rigazup/
│
├── app.py                      # Halaman Pendaratan (Entry point Streamlit)
├── requirements.txt            # Daftar pustaka sistem Python untuk Deployment
├── README.md                   # Repositori informasi (Panduan Dokumentasi)
├── PROJECT_SPEC.md             # Dokumen spesifikasi rincian aplikasi
├── .gitignore                  # Filter pengecualian komit GitHub
│
├── data/
│   └── dataset.csv             # Direktori penyimpanan contoh/template dataset
│
├── assets/
│   └── style.css               # Kode sumber estetika (Premium Custom CSS)
│
├── pages/                      # Antarmuka menu modular (Navigasi Multi-Halaman)
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
└── src/                        # Modul permesinan logika dan komputasi murni
    ├── validation.py
    ├── preprocessing.py
    ├── feature_engineering.py
    ├── visualization.py
    ├── modeling.py
    ├── evaluation.py
    ├── restock.py
    └── insight_generator.py
```

## Arsitektur ML (Algoritma Model & Metrik Evaluasi)
Sistem ini me-*run* 3 kontestan model di belakang layar secara paralel:
1. **Linear Regression:** Teknik statistika historis linier untuk menggali akar pola lurus yang terikat waktu.
2. **Random Forest Regressor:** Formasi "Hutan Keputusan" acak yang ampuh menjinakkan distorsi lonjakan musiman tanpa menderita anomali *overfitting*.
3. **XGBoost Regressor:** Model artifisial kelas-kompetisi dunia yang sangat presisi menangkap fluktuasi pola penjualan abstrak harian melalui optimalisasi ekstrim.

### Penjurian Metrik Evaluasi:
Sistem memilih algoritma paling dominan berdasar kriteria ketat ini:
- **MAE (Mean Absolute Error):** Menghitung nilai selisih murni antara tebakan AI vs Penjualan Riil.
- **RMSE (Root Mean Squared Error):** Bertugas menghukum keras algoritma apabila ia meramalkan suatu pola menyimpang (*outlier*) terlalu meleset.
- **MAPE (Mean Absolute Percentage Error):** Presentase bias (*error rate*). Semakin mendekati angka mutlak `0%`, maka hasil simulasi dinobatkan sebagai "Pemenang".

## Logika Mekanik Restock Planner
Rancangan kuantitas persediaan digerakkan oleh perumusan:
> **`Rekomendasi Restock = Max(0, Forecast Demand + Safety Stock - Current Stock)`**

Dimana:
- **Forecast Demand:** Ramalan volume laku (unit) hasil ekstrak prediksi model ML Pemenang.
- **Safety Stock:** Tabungan penyangga untuk menutupi bahaya (*buffer threshold*) jika laju pesanan pasar mendadak di luar nalar.
- **Current Stock:** Realita stok yang tengah tertidur di dalam gudang.

## Cara Menjalankan Secara Lokal (Local Development)
1. *Clone* repositori ini / unduh ke dalam direktori *Local Disk* komputer Anda.
2. Buka terminal favorit Anda (CMD / PowerShell / Bash), pindahkan lokasi kerja ke dalam folder proyek:
   ```bash
   cd rigazup/
   ```
3. *(Opsional)* Buat dan aktifkan *Virtual Environment* untuk lingkungan bersih.
4. **Install Modul Esensial**: Pasang seluruh kerangka peranti yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
5. **Launch Application**: Jalankan mesin Streamlit menggunakan *entry-point* utama:
   ```bash
   streamlit run app.py
   ```
6. Jendela aplikasi akan terbuka secara instan di peramban sistem Anda: `http://localhost:8501`.

## Panduan Deployment ke Streamlit Cloud (Gratis & Bebas Server)
Sebagai aplikasi ramah ekosistem awan (*Cloud Native*), perangkat lunak RIGAZUP dirancang terisolasi (*Stateless Session*) sehingga mulus untuk diterbangkan secara gratis.
1. Pastikan seluruh berkas arsitektur kode di repositori ini telah berhasil **di-push** ke dalam [Akun GitHub Public Anda].
2. Registrasi / Log-in ke dalam konsol administrasi [Streamlit Community Cloud](https://share.streamlit.io/).
3. Buka *Workspace*, klik menu raksasa bertuliskan **"New App"** di pojok kanan atas.
4. Hubungkan (*Authorize*) *bridge* ke akun GitHub Anda, pilih Repositori `rigazup` dari daftar jatuhan (*dropdown*).
5. Pada isian kolom **Main file path**, definisikan pintu utamanya yaitu: `app.py`.
6. Klik **Deploy!** dan tunggu sekian menit hingga mesin server pusat selesai men-*download* berkas pustaka dari `requirements.txt`.
7. Voila! Tautan (*Link URL*) aplikasi Anda telah hidup 24/7 dan siap dikirimkan kepada tim internal bisnis Anda untuk digunakan.

---

### Tim Pengembang Mahasiswa Universitas (Group Developer)
Proyek saintifik sains data ini diajukan, didesain, dan diselesaikan oleh kolaborasi mahasiswa:
- **Rian Sholihan**
- **Maulana Jalba Rizka**
- **Muhammad Thorieq Alfareza**
- **Ryan Ferdiansyah Risnayadi**
- **Muhammad Danil Ma'ruf**
