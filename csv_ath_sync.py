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
TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")

# Load or initialize logo cache
def load_logo_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_logo_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

# Logo fetcher (LogoKit fallback)
def get_logo_url(symbol, cache):
    symbol = symbol.upper()
    if symbol in cache:
        return cache[symbol]

    # Try LogoKit
    logo_url = f"https://img.logokit.com/token/{symbol}"
    test = requests.get(logo_url)
    if test.status_code == 200:
        cache[symbol] = logo_url
        return logo_url

    # Fallback: monogram or skip
    cache[symbol] = None
    return None

# Telegram alert with logo
def send_logo_alert(symbol, ath, logo_url):
    if logo_url:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": logo_url,
            "caption": f"🚀 {symbol} hit a new ATH: {ath:.4f}"
        }
        requests.post(url, json=payload)
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚀 {symbol} hit a new ATH: {ath:.4f} (no logo found)"
        }
        requests.post(url, json=payload)

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

    print("🖼️ Fetching logos and sending alerts...")
    cache = load_logo_cache()
    for symbol, ath in aths.items():
        logo_url = get_logo_url(symbol, cache)
        send_logo_alert(symbol, ath, logo_url)

    save_logo_cache(cache)

if __name__ == "__main__":
    main()
