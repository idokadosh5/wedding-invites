from flask import Flask, request
from twilio.rest import Client
import re
import os

app = Flask(__name__)

# Twilio credentials from environment variables
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")  # e.g., 'whatsapp:+14155238886'

client = Client(TWILIO_SID, TWILIO_AUTH)

# Send message route (e.g. manually or from admin dashboard)
@app.route('/send', methods=['POST'])
def send():
    data = request.json
    to = data['to']  # WhatsApp number like 'whatsapp:+972501234567'
    name = data.get('name', 'Guest')

    body = f"Hello {name}, please confirm your attendance to the wedding. How many people will be coming?"

    message = client.messages.create(
        from_=TWILIO_PHONE,
        to=to,
        body=body
    )
    return {"sid": message.sid}, 200

# Webhook route to receive replies
@app.route('/webhook', methods=['POST'])
def webhook():
    sender = request.form.get("From")
    msg = request.form.get("Body")

    # Extract number from reply
    match = re.search(r'\b\d+\b', msg)
    count = int(match.group()) if match else 1

    print(f"{sender} is bringing {count} guest(s). Message: {msg}")

    return "Thank you for confirming!", 200
