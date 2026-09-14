from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data, timeout=15)
    return response.json()


@app.route("/", methods=["GET"])
def home():
    return "XAUUSD Telegram Bot is running."


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    message = data.get("message", "XAUUSD Signal")

    telegram_message = f"""
🤖 <b>XAUUSD PRO ANALYST</b>

{message}

⚠️ <b>Manual Confirmation Required</b>
"""

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({"error": "Telegram credentials are not configured"}), 500

    result = send_telegram(telegram_message)

    return jsonify({
        "status": "sent",
        "telegram": result
    })
@app.route("/test-telegram", methods=["GET"])
def test_telegram():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({"error": "Telegram credentials are not configured"}), 500

    result = send_telegram("✅ XAUUSD Telegram Bot test message")

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
