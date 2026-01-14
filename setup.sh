#!/bin/bash

# --- KONFIGURASI NAMA FILE ---
PROXY_SCRIPT="proxy.py"
CHECKER_SCRIPT="checker.py"
MAIN_BOT_SCRIPT="main.py"
ENV_DIR="env"

# Fungsi untuk menangani Ctrl+C (Exit Gracefully)
trap "echo -e '\n[STOP] Script dihentikan user.'; exit" SIGINT

echo "==========================================="
echo "   AUTO TRAFFIC BOT SETUP (DEBIAN)       "
echo "==========================================="

# 1. Cek & Buat Virtual Environment
if [ ! -d "$ENV_DIR" ]; then
    echo "[INFO] Membuat Virtual Environment ($ENV_DIR)..."
    python3 -m venv $ENV_DIR
fi

# 2. Aktifkan Environment
echo "[INFO] Mengaktifkan Environment..."
source $ENV_DIR/bin/activate

# 3. Cek & Install Dependencies
echo "[INFO] Cek & Install Library Python..."
pip install --upgrade pip > /dev/null
# Install library tanpa output berisik (-q)
pip install selenium pandas webdriver-manager requests -q

# 4. LOOP UTAMA (OTOMATISASI)
while true; do
    echo ""
    echo "#############################################"
    echo "   MEMULAI SIKLUS BARU (Update -> Check -> Run)"
    echo "#############################################"
    
    # --- STEP A: DOWNLOAD PROXY ---
    if [ -f "$PROXY_SCRIPT" ]; then
        echo "[STEP 1] Menjalankan $PROXY_SCRIPT..."
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $PROXY_SCRIPT
    else
        echo "[ERROR] File $PROXY_SCRIPT tidak ditemukan!"
        exit 1
    fi
    
    echo "---------------------------------------------"

    # --- STEP B: CHECK PROXY ---
    if [ -f "$CHECKER_SCRIPT" ]; then
        echo "[STEP 2] Menjalankan $CHECKER_SCRIPT..."
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $CHECKER_SCRIPT
    else
        echo "[ERROR] File $CHECKER_SCRIPT tidak ditemukan!"
        exit 1
    fi

    echo "---------------------------------------------"

    # --- STEP C: JALANKAN BOT UTAMA ---
    if [ -f "$MAIN_BOT_SCRIPT" ]; then
        echo "[STEP 3] Menjalankan $MAIN_BOT_SCRIPT..."
        echo "Bot sedang berjalan. Tekan Ctrl+C untuk berhenti."
        
        # Jalankan bot
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $MAIN_BOT_SCRIPT
        
        # Jika bot script utama Anda crash atau selesai (misal karena error fatal),
        # script ini akan lanjut ke bawah.
        echo ""
        echo "[WARNING] Bot utama berhenti/crash."
    else
        echo "[ERROR] File $MAIN_BOT_SCRIPT tidak ditemukan!"
        exit 1
    fi

    echo "Restarting System dalam 10 detik..."
    echo "Mencari proxy baru agar IP tetap segar..."
    sleep 10
done
