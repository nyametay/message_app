from data.utils.sms_utils import  send_sms
from data.utils.email_utils import send_email, send_email_smtp
from data.utils.whatsapp_utils import send_whatsapp


def send_message(channel, contact, content):
    if channel.lower() == 'email' and contact.email:
        send_email(contact.email, content)
    elif channel.lower() == 'sms' and contact.phone:
        send_sms(contact.phone, content)
    elif channel.lower() == 'whatsapp' and contact.phone:
        send_whatsapp(contact.phone, content)
    else:
        raise ValueError(f"No valid contact method for channel: {channel}")

