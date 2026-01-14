import requests
import pandas as pd
import os

# Sumber Proxy Publik (Updated Daily/Hourly)
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt"
]

OUTPUT_DIR = './list-proxy'
OUTPUT_FILE = f'{OUTPUT_DIR}/auto_downloaded.csv'

def download_proxies():
    print("=== MENGUNDUH PROXY TERBARU ===")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    all_proxies = []
    
    for url in PROXY_SOURCES:
        try:
            print(f"Downloading from: {url.split('/')[-1]}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Memisahkan baris dan membersihkan spasi
                lines = response.text.strip().split('\n')
                proxies = [line.strip() for line in lines if ':' in line]
                all_proxies.extend(proxies)
                print(f"  -> Mendapat {len(proxies)} IP")
        except Exception as e:
            print(f"  -> Gagal: {e}")

    # Hapus duplikat
    unique_proxies = list(set(all_proxies))
    print(f"\nTotal Proxy Unik: {len(unique_proxies)}")
    
    # Simpan ke format CSV sesuai bot Anda
    df = pd.DataFrame(unique_proxies, columns=['ip_address'])
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"[SUKSES] Tersimpan di: {OUTPUT_FILE}")
    print("SEKARANG: Jalankan 'checker.py' untuk memfilter IP yang hidup!")

if __name__ == "__main__":
    download_proxies()