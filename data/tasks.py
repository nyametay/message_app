from data import app, db
from data.models import Messages, DeliveryLogs, Contacts
from celery import shared_task
from datetime import datetime


@shared_task
def send_scheduled_message(message_id, contact_ids, user_id):
    from data.utils_ import send_message  # import here if you have a utility

    with app.app_context():  # ✅ ensures Flask context is available
        message = Messages.query.get(message_id)
        if not message:
            return

        now = datetime.utcnow()
        status = 'sent'
        error_message = None

        try:
            for contact_id in contact_ids:
                contact = Contacts.query.get_or_404(contact_id)
                send_message(message.channel, contact, message.content)
            message.status = 'sent'
        except Exception as e:
            status = 'failed'
            error_message = str(e)
            message.status = 'failed'

        # Log delivery attempt
        log = DeliveryLogs(
            message_id=message.id,
            user_id=user_id,
            delivery_time=now,
            delivery_status=status,
            error_message=error_message
        )

        db.session.add(log)
        db.session.commit()
