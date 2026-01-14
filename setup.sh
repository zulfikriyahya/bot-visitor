#!/bin/bash


PROXY_SCRIPT="proxy.py"
CHECKER_SCRIPT="checker.py"
MAIN_BOT_SCRIPT="main.py"
ENV_DIR="env"


trap "echo -e '\n[STOP] Script dihentikan user.'; exit" SIGINT

echo "==========================================="
echo "   AUTO TRAFFIC BOT SETUP (DEBIAN)       "
echo "==========================================="


if [ ! -d "$ENV_DIR" ]; then
    echo "[INFO] Membuat Virtual Environment ($ENV_DIR)..."
    python3 -m venv $ENV_DIR
fi


echo "[INFO] Mengaktifkan Environment..."
source $ENV_DIR/bin/activate


echo "[INFO] Cek & Install Library Python..."
pip install --upgrade pip > /dev/null

pip install selenium pandas webdriver-manager requests -q


while true; do
    echo ""
    echo "#############################################"
    echo "   MEMULAI SIKLUS BARU (Update -> Check -> Run)"
    echo "#############################################"
    
    
    if [ -f "$PROXY_SCRIPT" ]; then
        echo "[STEP 1] Menjalankan $PROXY_SCRIPT..."
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $PROXY_SCRIPT
    else
        echo "[ERROR] File $PROXY_SCRIPT tidak ditemukan!"
        exit 1
    fi
    
    echo "---------------------------------------------"

    
    if [ -f "$CHECKER_SCRIPT" ]; then
        echo "[STEP 2] Menjalankan $CHECKER_SCRIPT..."
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $CHECKER_SCRIPT
    else
        echo "[ERROR] File $CHECKER_SCRIPT tidak ditemukan!"
        exit 1
    fi

    echo "---------------------------------------------"

    
    if [ -f "$MAIN_BOT_SCRIPT" ]; then
        echo "[STEP 3] Menjalankan $MAIN_BOT_SCRIPT..."
        echo "Bot sedang berjalan. Tekan Ctrl+C untuk berhenti."
        
        
        /home/zulfikriyahya/bot-visitor/env/bin/python3 $MAIN_BOT_SCRIPT
        
        
        
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
