import os
import json
import requests

# ----------------------------
# Telegram 設定
# ----------------------------
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=payload)
    print(r.text)  # デバッグ用

# ----------------------------
# SAM.gov API から沖縄/Kadena案件取得
# ----------------------------
def fetch_okinawa_projects():
    url = "https://api.sam.gov/opportunities/v2/search"
    params = {
        "api_key": os.environ["SAM_API_KEY"],  # GitHub Secrets に登録済み
        "limit": 50,
        "postedFrom": "2025-01-01",
        "q": "Okinawa OR Kadena"  # ← ここで地名検索
    }
    response = requests.get(url, params=params)
    data = response.json()
    projects = []

    for item in data.get("opportunities", []):
        city = item.get("placeOfPerformance", {}).get("city", "")
        state = item.get("placeOfPerformance", {}).get("state", "")
        projects.append({
            "案件番号": item.get("solicitationNumber"),
            "工事名": item.get("title"),
            "場所": f"{city}, {state}",
            "予定額": item.get("estimatedAmount"),
        })
    return projects

# ----------------------------
# 前回データ読み込み
# ----------------------------
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        old_data = json.load(f)
except FileNotFoundError:
    old_data_
