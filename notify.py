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
# SAM.gov API から沖縄案件取得
# ----------------------------
def fetch_okinawa_projects():
    url = "https://api.sam.gov/opportunities/v2/search"
    params = {
        "api_key": os.environ["SAM_API_KEY"],  # GitHub Secrets に登録済み
        "placeOfPerformance.state": "OK",      # 沖縄の州コード（仮）
        "limit": 50,                            # 取得件数
        "postedFrom": "2025-01-01"             # 任意、最新案件のみ
    }
    response = requests.get(url, params=params)
    data = response.json()
    projects = []

    # 取得結果から必要項目だけ抽出
    for item in data.get("opportunities", []):
        projects.append({
            "案件番号": item.get("solicitationNumber"),
            "工事名": item.get("title"),
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
    old_data = []

# ----------------------------
# 今回データ取得
# ----------------------------
new_data = fetch_okinawa_projects()

# ----------------------------
# 新着・変更検出
# ----------------------------
old_dict = {c['案件番号']: c for c in old_data}
new_cases, updated_cases = [], []

for c in new_data:
    if c['案件番号'] not in old_dict:
        new_cases.append(c)
    elif c != old_dict[c['案件番号']]:
        updated_cases.append(c)

# ----------------------------
# Telegram に通知
# ----------------------------
for case in new_cases:
    send_telegram(f"🆕 新着案件: {case['工事名']} ({case['案件番号']})")

for case in updated_cases:
    send_telegram(f"✏️ 変更案件: {case['工事名']} ({case['案件番号']})")

# ----------------------------
# 今回データを保存
# ----------------------------
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
