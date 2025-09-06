from flask import Flask, request, jsonify
import requests
import os
import json
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route('/alert', methods=['POST'])
def receive_alert():
    try:
        payload_raw = request.data.decode("utf-8")  # raw body
        logger.info(f"📥 Received payload: {payload_raw}")

        payload_json = None
        try:
            payload_json = json.loads(payload_raw)
        except json.JSONDecodeError:
            logger.warning("⚠️ Payload is not valid JSON, treating as text")

        if payload_json and "data" in payload_json:
            trade_data = payload_json.get("data", {})

            symbol = trade_data.get("symbol", "N/A")
            exchange = trade_data.get("exchange", "N/A")
            timeframe = trade_data.get("timeframe", "N/A")
            datetime = trade_data.get("datetime", "N/A")
            side = trade_data.get("side", "N/A")
            entry = trade_data.get("entry", "N/A")
            stoploss = trade_data.get("sl", "N/A")
            tp1 = trade_data.get("tp1", "N/A")
            tp2 = trade_data.get("tp2", "N/A")
            rr = trade_data.get("rr", "N/A")
            tradetype = trade_data.get("tradetype", "N/A")
            expiry = trade_data.get("expiry", "N/A")
            prob = trade_data.get("probability", "N/A")
            reason = trade_data.get("reason", "N/A")

            message = (
                f"🔔 {side} | {symbol}:{exchange} | {timeframe}\n"
                f"📅 {datetime}\n\n"
                f"💵 Entry: {entry}\n"
                f"🛡️ SL: {stoploss}\n"
                f"🎯 TP1: {tp1} | TP2: {tp2}\n"
                f"📊 Prob: {prob}\n"
                f"⚖️ RR: {rr}\n"
                f"📌 Type: {tradetype} | Exp: {expiry}\n\n"
                f"🔎 {reason}"
            )
            logger.info("✅ Structured JSON alert parsed successfully")
        else:
            message = f"🔔 TradingView Alert 🔔\n{payload_raw}"
            logger.info("✅ Plain text alert processed")

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(telegram_url, json=telegram_payload, timeout=5)

        if response.status_code == 200:
            logger.info("📤 Sent alert to Telegram successfully")
            return jsonify({"status": "success", "message": "Alert sent to Telegram"}), 200
        else:
            logger.error(f"❌ Telegram send failed: {response.text}")
            return jsonify({"status": "error", "message": "Failed to send message to Telegram"}), 500

    except Exception as e:
        logger.exception("🔥 Exception in /alert endpoint")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    logger.debug("Health check called")
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
