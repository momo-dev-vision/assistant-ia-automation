import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]

    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload, headers=headers
    )
    reply = response.json()["choices"][0]["message"]["content"]
    send_message(chat_id, reply)

    return "ok"
