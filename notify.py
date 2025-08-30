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
        "postedFrom": "2023-01-01",  # 過去データの開始日
        "limit": 10
    }
    r = requests.get(url, params=params)
    print("SAM API status:", r.status_code)
    try:
        data = r.json()
    except Exception as e:
        print("JSON取得失敗:", e)
        data = {}
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

# デバッグ出力：取得データを表示
print("取得した案件データ:", new_data)

# === 過去データを読み込み ===
if os.path.exists("last_data.json"):
    with open("last_data.json", "r") as f:
        old_data = json.load(f)
else:
    old_data = []

new_dict = {d["id"]: d for d in new_data}
old_dict = {d["id"]: d for d in old_data}

messages = []

# 🆕 新規案件
for nid, n in new_dict.items():
    if nid not in old_dict:
        messages.append(f"🆕 新着: {n['title']} ({n['postedDate']})")

# ✏️ 更新案件
for nid, n in new_dict.items():
    if nid in old_dict and n != old_dict[nid]:
        messages.append(f"✏️ 更新: {n['title']} ({n['postedDate']})")

# デバッグ出力：送信予定メッセージ
print("送信するメッセージ:", messages)

# 通知
if messages:
    for msg in messages:
        send_telegram(msg)
else:
    send_telegram("特になし")

# === 最新データを保存 ===
with open("last_data.json", "w") as f:
    json.dump(new_data, f, indent=2)
