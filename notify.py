import os
import json
import requests

# === 環境変数 ===
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
SAM_API_KEY = os.environ["SAM_API_KEY"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    print("Telegram response:", r.text)

# === SAM.gov API呼び出し ===
def fetch_sam_data():
    url = "https://api.sam.gov/prod/opportunities/v2/search"
    params = {
        "api_key": SAM_API_KEY,
        "q": "Okinawa OR Kadena",  # 検索ワード
        "postedFrom": "2023-01-01",  # 古いデータを避けるため適当な開始日
        "limit": 10
    }
    r = requests.get(url, params=params)
    print("SAM API status:", r.status_code)
    data = r.json()
    results = []
    for item in data.get("opportunitiesData", []):
        results.append({
            "id": item.get("noticeId"),
            "title": item.get("title"),
            "status": item.get("type"),
            "postedDate": item.get("postedDate")
        })
    return results

# === 新しいデータを取得 ===
new_data = fetch_sam_data()

# === 過去データを読
