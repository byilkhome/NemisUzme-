from flask import Flask, request
import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route('/')
def home():
    return "NemisUz ist online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"].get("text", "")

        if user_msg:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Du bist NemisUz, ein zweisprachiger Usbekisch-Deutsch Lernassistent."},
                    {"role": "user", "content": user_msg}
                ]
            )
            bot_reply = reply.choices[0].message.content
            send_telegram_message(chat_id, bot_reply)

    return "ok", 200

if __name__ == '__main__':
    app.run()
