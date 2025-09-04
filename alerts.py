from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    # Extract nested "data" dictionary from payload
    trade_data = data.get("data", {})
    
    symbol = trade_data.get("symbol", "N/A")
    price = trade_data.get("price", "N/A")
    volume = trade_data.get("volume", "N/A")
    time = trade_data.get("time", "N/A")
    timeframe = trade_data.get("timeframe", "N/A")
    
    message = (f"📢 Trading Alert:\n"
               f"Symbol: {symbol}\n"
               f"Price: {price}\n"
               f"Volume: {volume}\n"
               f"Time: {time}\n"
               f"Timeframe: {timeframe}")
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}
    requests.post(url, json=payload)
    
    return jsonify({"status": "ok", "sent": message})

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200
