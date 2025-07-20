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

    body = f"Hello {name}, שלום רב, בבקשה אשר את ההזמנה לחתונה של ליאל ועידוא ב14.9 באולם נסיה וכמה אנשים יגיעו?"

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

    try:
        client.messages.create(
            from_=TWILIO_PHONE,
            to=sender,  # Reply to the same number that sent the message
            body=confirmation_msg
        )
        print(f"Confirmation sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send confirmation to {phone_number}: {e}")
    
    return "OK", 200
