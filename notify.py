import os
import requests

# GitHub Secretsから情報を取得
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# テスト通知
message = "[テスト通知] このメッセージはTelegramに届きます"
send_telegram(message)
