from flask import Flask, request, jsonify
import requests
import os

# === Your Telegram details ===
#TG_CHAT_ID = "1225164824"
#TG_BOT_TOKEN = "8282035808:AAED2id4cHSMCo0cF_SXmGmgun-MnMoN3e0"

app = Flask(__name__)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = f"📢 Trading Alert: {data}"
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}
    requests.post(url, json=payload)

    return jsonify({"status": "ok", "sent": message})

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200
