from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env laden
load_dotenv()

app = Flask(__name__)

# API-Keys laden
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini-Key prüfen und debuggen
if not GEMINI_API_KEY:
    raise ValueError("❌ Der GEMINI_API_KEY wurde nicht gefunden. Bitte als Environment Variable in Render setzen.")

print("✅ DEBUG: Gemini-Key geladen:", GEMINI_API_KEY[:6] + "..." if GEMINI_API_KEY else "FEHLT")

# Gemini konfigurieren
genai.configure(api_key=GEMINI_API_KEY)

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❗ Fehler beim Senden an Telegram: {e}")

def get_gemini_reply(user_msg):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-pro")
        response = model.generate_content(user_msg)
        return response.text
    except Exception as e:
        print(f"❗ Fehler bei Gemini-Antwort: {e}")
        return "⚠️ Entschuldigung, es gab ein Problem bei der Antwortgenerierung."

@app.route('/')
def home():
    return "NemisUz (Gemini) ist online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_msg = data["message"].get("text", "")

        if user_msg:
            bot_reply = get_gemini_reply(user_msg)
            send_telegram_message(chat_id, bot_reply)

    return "ok", 200

if __name__ == '__main__':
    app.run()


