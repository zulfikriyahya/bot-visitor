# Website Traffic Automation Tool

Alat simulasi kunjungan situs web berbasis Python yang dirancang untuk pengujian beban server dan analisis statistik lalu lintas. Perangkat lunak ini memanfaatkan Selenium WebDriver dengan dukungan multi-threading, rotasi proxy, dan manipulasi sidik jari digital (fingerprint spoofing) untuk mensimulasikan perilaku pengguna secara anonim dan efisien.

## Fitur Utama

- **Simulasi Trafik Masif:** Mendukung eksekusi multi-thread untuk menghasilkan volume kunjungan yang tinggi dalam waktu singkat.
- **Rotasi Identitas Penuh:** Mengacak alamat IP (melalui Proxy) dan User-Agent pada setiap sesi kunjungan untuk meminimalkan deteksi pola bot.
- **Manipulasi Sidik Jari (Anti-Fingerprint):**
  - Canvas Spoofing: Menyuntikkan noise pada data elemen Canvas HTML5.
  - Resolution Spoofing: Menyesuaikan resolusi layar browser dengan User-Agent yang digunakan.
  - Timezone Override: Memaksa zona waktu browser sesuai target lokasi (Asia/Jakarta).
- **Optimasi Sumber Daya:** Berjalan dalam mode Headless Chrome dengan strategi pemuatan halaman "Eager" dan pemblokiran aset berat (gambar/font) untuk kinerja maksimal pada server berspesifikasi rendah.
- **Sistem Otomatisasi Penuh:** Dilengkapi skrip bash untuk mengelola siklus unduh proxy, validasi koneksi, dan eksekusi bot secara berkelanjutan.

## Struktur Direktori

Pastikan struktur direktori proyek Anda disusun sebagai berikut:

```text
/project-root
│
├── main.py              # Skrip utama bot pengunjung
├── checker.py           # Skrip validasi koneksi proxy
├── proxy.py             # Skrip pengunduh daftar proxy publik
├── setup.sh             # Skrip manajemen otomatisasi (Bash)
│
├── user_agent.csv       # Daftar User-Agent
├── proxy-aktif.csv      # Daftar proxy valid (dihasilkan oleh checker.py)
│
├── sitemap/             # Folder berisi daftar URL target
│   ├── urls_1.csv
│   └── urls_2.csv
│
└── list-proxy           # Folder penyimpanan sementara unduhan proxy
```

## Prasyarat Sistem

- Sistem Operasi: Linux (Debian/Ubuntu disarankan) atau Windows.
- Python 3.8 atau versi lebih baru.
- Google Chrome (Versi Stable).
- Koneksi internet yang stabil.

## Instalasi

1.  **Perbarui Repository Sistem & Instal Google Chrome**
    Pastikan Google Chrome terinstal pada server Anda karena alat ini menggunakan ChromeDriver.

    ```bash
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
    ```

2.  **Kloning Repository & Instal Dependensi Python**

    ```bash
    pip install selenium pandas webdriver-manager requests
    ```

3.  **Persiapan Data**
    Buat file `user_agent.csv` dan file CSV di dalam folder `sitemap/` sesuai dengan format yang dibutuhkan (header: `user_agent` dan `sitemap`).

## Panduan Penggunaan

Terdapat dua metode untuk menjalankan alat ini: secara manual per modul atau otomatis penuh menggunakan skrip pembungkus.

### Metode 1: Otomatisasi Penuh (Disarankan)

Gunakan `setup.sh` untuk menjalankan siklus pengunduhan proxy, pengecekan validitas proxy, dan eksekusi bot secara berurutan dan berulang (loop).

1.  Berikan izin eksekusi pada skrip:

    ```bash
    chmod +x setup.sh
    ```

2.  Jalankan skrip di latar belakang (background process):

    ```bash
    nohup ./setup.sh > bot.log 2>&1 &
    ```

3.  Pantau aktivitas melalui log:
    ```bash
    tail -f bot.log
    ```

### Metode 2: Eksekusi Manual

Anda dapat menjalankan setiap modul secara terpisah sesuai kebutuhan:

1.  **Unduh Proxy:** Mengambil daftar proxy terbaru dari sumber publik.

    ```bash
    python3 proxy.py
    ```

2.  **Validasi Proxy:** Memeriksa koneksi proxy dan menyimpan IP yang valid ke `proxy-aktif.csv`.

    ```bash
    python3 checker.py
    ```

3.  **Jalankan Bot:** Memulai simulasi kunjungan menggunakan proxy yang valid.
    ```bash
    python3 main.py
    ```

## Konfigurasi Lanjutan

Anda dapat menyesuaikan parameter kinerja pada bagian atas file `main.py`:

- `MAX_THREADS`: Jumlah browser yang berjalan bersamaan (sesuaikan dengan RAM server).
- `PAGES_PER_THREAD`: Jumlah halaman yang dikunjungi sebelum browser dimuat ulang.
- `MIN_DELAY` / `MAX_DELAY`: Rentang waktu tunggu acak antar kunjungan (dalam detik).

## Penafian (Disclaimer)

Perangkat lunak ini dikembangkan hanya untuk tujuan pendidikan, pengujian beban (stress testing), dan simulasi analitik. Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini untuk tujuan ilegal, termasuk namun tidak terbatas pada penipuan iklan (ad fraud), serangan DDoS, atau pelanggaran ketentuan layanan pihak ketiga. Harap gunakan dengan bijak dan bertanggung jawab.
