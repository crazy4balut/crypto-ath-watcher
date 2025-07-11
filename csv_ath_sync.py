import subprocess
from csv_parser import parse_crypto_app_csv
import requests
import os

# Configuration
DROPBOX_CMD = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh"
DROPBOX_PATH = "/crypto_exports/latest.csv"
LOCAL_PATH = "/home/pi/crypto_exports/latest.csv"
TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")

def download_from_dropbox():
    subprocess.run([DROPBOX_CMD, "download", DROPBOX_PATH, LOCAL_PATH])

def extract_ath(csv_path):
    df = parse_crypto_app_csv(csv_path)
    aths = {}

    for symbol in df['symbol'].unique():
        coin_df = df[df['symbol'] == symbol]
        high = coin_df['amount'].max()
        aths[symbol] = high

    return aths

def send_alert(aths):
    message = "🚀 New ATH Snapshot:\n"
    for symbol, ath in aths.items():
        message += f"{symbol}: {ath:.4f}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

def main():
    print("🔄 Syncing CSV from Dropbox...")
    download_from_dropbox()

    print("📈 Parsing CSV for ATH data...")
    aths = extract_ath(LOCAL_PATH)

    print("📢 Sending Telegram alert...")
    send_alert(aths)

if __name__ == "__main__":
    main()
