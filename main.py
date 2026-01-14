import os
import glob
import time
import random
import pandas as pd
import concurrent.futures
import gc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
MAX_THREADS = 15         
PAGES_PER_THREAD = 20    
MIN_DELAY = 5            
MAX_DELAY = 8
RESOLUTIONS = [
    (1920, 1080), (1366, 768), (1536, 864), (1440, 900),  
    (1280, 720), (1600, 900), (360, 800), (390, 844)      
]
def load_data(path_pattern, col_name):
    """Load data CSV dengan aman"""
    data_list = []
    files = glob.glob(path_pattern)
    if not files: return []
    for file in files:
        if os.path.getsize(file) > 0:
            try:
                df = pd.read_csv(file)
                if col_name in df.columns:
                    data_list.extend(df[col_name].dropna().astype(str).str.strip().tolist())
            except: pass
    unique = list(set(data_list))
    random.shuffle(unique)
    return unique
def get_fingerprint_script():
    """
    Script JS untuk memalsukan Canvas Fingerprint.
    Menambahkan sedikit noise pada fungsi toDataURL dan getImageData.
    """
    return """
    (() => {
        const toBlob = HTMLCanvasElement.prototype.toBlob;
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        const getImageData = CanvasRenderingContext2D.prototype.getImageData;
        var noise = Math.floor(Math.random() * 10) - 5; 
        HTMLCanvasElement.prototype.toBlob = function(callback, type, quality) {
            return toBlob.apply(this, [callback, type, quality]);
        };
        HTMLCanvasElement.prototype.toDataURL = function(type, quality) {
            const result = toDataURL.apply(this, [type, quality]);
            return result;
        };
        CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
            const image = getImageData.apply(this, [x, y, w, h]);
            for (let i = 0; i < image.data.length; i += 4) {
                image.data[i+2] = image.data[i+2] + noise; 
            }
            return image;
        };
    })();
    """
def get_driver(user_agents, proxies, driver_path):
    options = Options()
    width, height = random.choice(RESOLUTIONS)
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    prefs = {
        "profile.managed_default_content_settings.images": 2,      
        "profile.managed_default_content_settings.stylesheets": 2, 
        "profile.managed_default_content_settings.fonts": 2,       
        "profile.default_content_setting_values.notifications": 2, 
        "profile.managed_default_content_settings.popups": 2,      
    }
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    if user_agents:
        ua = random.choice(user_agents)
        options.add_argument(f'user-agent={ua}')
    proxy_ip = None
    if proxies:
        proxy_ip = random.choice(proxies)
        options.add_argument(f'--proxy-server={proxy_ip}')
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver, proxy_ip, f"{width}x{height}"
    except Exception as e:
        return None, None, None
def worker(thread_id, urls, user_agents, proxies, driver_path):
    if not urls: return
    driver, current_proxy, res = get_driver(user_agents, proxies, driver_path)
    if not driver: return
    try:
        driver.set_page_load_timeout(20) 
        for i in range(PAGES_PER_THREAD):
            target_url = random.choice(urls)
            delay = random.uniform(MIN_DELAY, MAX_DELAY) 
            try:
                driver.get(target_url)
                driver.execute_script("window.scrollTo(0, 500);") 
                time.sleep(1) 
                driver.execute_script("window.scrollTo(0, 0);")
                print(f"[T-{thread_id}] HIT! {target_url} | Proxy: {current_proxy}")
                time.sleep(delay)
            except Exception:
                pass 
    except Exception as e:
        print(f"[T-{thread_id}] Error: {e}")
    finally:
        try:
            driver.quit()
        except: pass
def main():
    print("=== ADVANCED BOT TRAFFIC (FINGERPRINT SPOOFING) ===")
    try:
        driver_path = ChromeDriverManager().install()
    except Exception as e:
        print(f"Driver Error: {e}")
        return
    batch = 0
    while True:
        batch += 1
        print(f"\n--- BATCH #{batch} ---")
        user_agents = load_data('./user_agent.csv', 'user_agent')
        proxies = load_data('./proxy-aktif.csv', 'ip_address') 
        urls = load_data('./sitemap/*.csv', 'sitemap')
        if not urls:
            time.sleep(30)
            continue
        if not proxies:
            print("[INFO] Tidak ada proxy. Menggunakan IP Server (Resiko terdeteksi tinggi).")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = []
            for i in range(MAX_THREADS):
                futures.append(
                    executor.submit(worker, i+1, urls, user_agents, proxies, driver_path)
                )
            concurrent.futures.wait(futures)
        gc.collect() 
        time.sleep(2)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[STOP] Bye.")