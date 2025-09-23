import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Ensures env vars are loaded

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

TWILIO_SMS_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_sms(phone_number, content):
    """Send an SMS using Twilio."""
    message = twilio_client.messages.create(
        body=content['message'],
        from_=TWILIO_SMS_NUMBER,
        to=phone_number
    )
    print(f"SMS sent: SID={message.sid}")
