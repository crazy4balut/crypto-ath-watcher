import subprocess
from csv_parser import parse_crypto_app_csv
import requests
import os
import json

# Config
DROPBOX_CMD = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh"
DROPBOX_PATH = "/crypto_exports/latest.csv"
LOCAL_PATH = "/home/pi/crypto_exports/latest.csv"
CACHE_PATH = "/home/pi/crypto_exports/logo_cache.json"
ATH_MEMORY_PATH = "/home/pi/crypto_exports/ath_memory.json"
TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")

# Load or initialize logo cache
def load_logo_cache():
    return json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}

def save_logo_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

# Load or initialize ATH memory
def load_ath_memory():
    return json.load(open(ATH_MEMORY_PATH)) if os.path.exists(ATH_MEMORY_PATH) else {}

def save_ath_memory(memory):
    with open(ATH_MEMORY_PATH, "w") as f:
        json.dump(memory, f)

# Logo fetcher (LogoKit fallback)
def get_logo_url(symbol, cache):
    symbol = symbol.upper()
    if symbol in cache:
        return cache[symbol]

    logo_url = f"https://img.logokit.com/token/{symbol}"
    if requests.get(logo_url).status_code == 200:
        cache[symbol] = logo_url
        return logo_url

    cache[symbol] = None
    return None

# Telegram alert with logo
def send_logo_alert(symbol, ath, logo_url):
    if logo_url:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "photo": logo_url,
                "caption": f"🚀 {symbol} hit a new ATH: {ath:.4f}"
            }
        )
    else:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": f"🚀 {symbol} hit a new ATH: {ath:.4f} (no logo found)"
            }
        )

def main():
    print("🔄 Syncing CSV from Dropbox...")
    subprocess.run([DROPBOX_CMD, "download", DROPBOX_PATH, LOCAL_PATH])

    print("📈 Parsing CSV for ATH data...")
    df = parse_crypto_app_csv(LOCAL_PATH)
    aths = {}
    for symbol in df['symbol'].unique():
        coin_df = df[df['symbol'] == symbol]
        high = coin_df['amount'].max()
        aths[symbol] = high

    print("🧠 Comparing with ATH memory...")
    ath_memory = load_ath_memory()
    logo_cache = load_logo_cache()

    for symbol, ath in aths.items():
        prev_ath = ath_memory.get(symbol, 0)
        if ath > prev_ath:
            logo_url = get_logo_url(symbol, logo_cache)
            send_logo_alert(symbol, ath, logo_url)
            ath_memory[symbol] = ath

    save_logo_cache(logo_cache)
    save_ath_memory(ath_memory)

if __name__ == "__main__":
    main()
