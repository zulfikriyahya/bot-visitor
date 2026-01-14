import requests
import concurrent.futures
import pandas as pd
import glob
import os
import time
import sys
INPUT_FOLDER = './list-proxy/*.csv'  
OUTPUT_FILE = 'proxy-aktif.csv'   
CHECK_URL = "https://mtsn1pandeglang.sch.id" 
TIMEOUT = 5                         
MAX_THREADS = 50                    
def load_proxies():
    """Membaca semua file CSV di folder list-proxy"""
    all_proxies = []
    files = glob.glob(INPUT_FOLDER)
    if not files:
        print(f"[ERROR] Tidak ada file csv di {INPUT_FOLDER}")
        return []
    print(f"Membaca file: {files}")
    for file in files:
        try:
            df = pd.read_csv(file)            
            if 'ip_address' in df.columns:
                ips = df['ip_address'].dropna().astype(str).str.strip().tolist()
                all_proxies.extend(ips)
        except Exception as e:
            print(f"[SKIP] Gagal baca {file}: {e}")
    unique_proxies = list(set(all_proxies))
    print(f"Total Proxy Ditemukan: {len(unique_proxies)}")
    return unique_proxies
def check_proxy(proxy):
    """Fungsi untuk mengetes satu proxy"""
    proxies_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        start = time.time()
        response = requests.get(CHECK_URL, proxies=proxies_dict, timeout=TIMEOUT)
        if response.status_code == 200:
            latency = (time.time() - start) * 1000 
            return {'ip_address': proxy, 'latency': latency}
    except:
        pass
    return None
def main():
    print("=== PROXY CHECKER MULTI-THREAD ===")
    proxies = load_proxies()
    if not proxies:
        return
    valid_proxies = []
    total = len(proxies)
    checked = 0
    print(f"\nMemulai pengecekan {total} proxy dengan {MAX_THREADS} threads...")
    print("Harap tunggu... (Simbol . = 10 proxy selesai diperiksa)")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            checked += 1
            if checked % 10 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            if result:
                valid_proxies.append(result)
    print(f"\n\n=== SELESAI ===")
    print(f"Waktu Proses: {time.time() - start_time:.2f} detik")
    print(f"Proxy Awal  : {total}")
    print(f"Proxy Aktif : {len(valid_proxies)}")
    if valid_proxies:
        df_valid = pd.DataFrame(valid_proxies)
        df_valid = df_valid.sort_values(by='latency')
        df_valid[['ip_address']].to_csv(OUTPUT_FILE, index=False)
        print(f"\n[SUKSES] Proxy aktif disimpan ke: {OUTPUT_FILE}")
        print("Anda sekarang bisa menjalankan bot utama.")
    else:
        print("\n[GAGAL] Tidak ada proxy yang aktif. Coba cari list proxy baru.")
if __name__ == "__main__":
    main()