import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Ensures env vars are loaded

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")


def send_whatsapp(phone_number, message):
    """Send a WhatsApp message using Twilio."""
    message = twilio_client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{phone_number}'
    )
    print(f"WhatsApp message sent: SID={message.sid}")