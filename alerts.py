from flask import Flask, request
import requests
import os

# === Your Telegram details ===
#TG_CHAT_ID = "1225164824"
#TG_BOT_TOKEN = "8282035808:AAED2id4cHSMCo0cF_SXmGmgun-MnMoN3e0"

app = Flask(__name__)

TG_CHAT_ID = os.getenv("TG_CHAT_ID")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return {"status": "error", "message": "No data"}, 400

    message = f"📢 TradingView Alert:\n{data}"
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}

    try:
        r = requests.post(url, json=payload)
        return {"status": "success", "telegram_response": r.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/')
def home():
    return "🚀 Trading Alerts Bot Running on Render!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
