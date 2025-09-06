from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load secrets from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("API_KEY")

@app.route('/alert', methods=['POST'])
def receive_alert():
    """
    Receives alerts from TradingView, validates the API key,
    and sends a formatted message to a Telegram chat.
    """
    # 1. Security Check: Validate the API key from the request header
    if request.headers.get('X-API-KEY') != API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 401

    try:
        # 2. Extract Data: Get the nested "data" dictionary from the payload
        payload = request.json
        trade_data = payload.get("data", {})
        
        symbol = trade_data.get("symbol", "N/A")
        price = trade_data.get("price", "N/A")
        volume = trade_data.get("volume", "N/A")
        time = trade_data.get("time", "N/A")
        timeframe = trade_data.get("timeframe", "N/A")
        
        # 3. Format Message for Telegram
        message = (
            f"🔔 TradingView Alert 🔔\n"
            f"---------------------------\n"
            f"📈 Symbol: {symbol}\n"
            f"💰 Price: {price}\n"
            f"📊 Volume: {volume}\n"
            f"⏰ Time: {time}\n"
            f"⏱️ Timeframe: {timeframe}\n"
        )
        
        # 4. Send the message to Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        
        # Use a timeout to prevent the request from hanging
        response = requests.post(telegram_url, json=telegram_payload, timeout=5)

        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Alert sent to Telegram successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send message to Telegram"}), 500

    except Exception as e:
        # 5. Error Handling: Catch any exceptions and return a helpful error message
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint to check the application's health.
    """
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
