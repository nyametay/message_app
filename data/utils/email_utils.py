import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv()  # Load environment variables

# SendGrid setup
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_SENDER = os.getenv("SENDGRID_SENDER_EMAIL")

# SMTP config
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")


def send_email(to_email, content):
    """Send an email using SendGrid."""
    message = Mail(
        from_email=SENDGRID_SENDER,
        to_emails=to_email,
        subject=content['subject'],
        plain_text_content=content['message'],
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email} : Status={response.status_code}")
    except Exception as e:
        print(f"Email failed: {str(e)}")
        raise


def send_email_smtp(to_email, content):
    """Send email via SMTP."""
    try:
        msg = MIMEText(content['message'])
        msg['Subject'] = content['subject']
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
            print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Email sending failed: {e}")
        raise

