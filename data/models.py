from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from data import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    _password_hash = db.Column("password", db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_text_password):
        self._password_hash = generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return check_password_hash(self._password_hash, plain_text_password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'password': self._password_hash
        }


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))  # Use string to handle country codes and formatting
    email = db.Column(db.String(50))

    user = db.relationship('Users', backref='contacts')


message_recipients = db.Table('message_recipients',
                              db.Column('message_id', db.Integer, db.ForeignKey('messages.id')),
                              db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'))
                              )


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel = db.Column(db.String(20), nullable=False)  # e.g., 'SMS', 'WhatsApp', 'Email'
    content = db.Column(db.JSON, nullable=False)  # Can hold long messages
    schedule_time = db.Column(db.DateTime, nullable=False)  # Better than string for datetime
    status = db.Column(db.String(10), nullable=False)  # e.g., 'pending', 'sent', 'failed'

    user = db.relationship('Users', backref='messages')
    recipients = db.relationship('Contacts', secondary=message_recipients, backref='messages')

    # Only here we define the relationship + cascade
    delivery_logs = db.relationship(
        'DeliveryLogs',
        back_populates='message',
        cascade="all, delete-orphan"
    )


class DeliveryLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ✅ fix here
    delivery_time = db.Column(db.DateTime, nullable=False)
    delivery_status = db.Column(db.String(10), nullable=False)  # e.g., 'pending', 'sent', 'failed'
    error_message = db.Column(db.Text)  # Optional field for logging failures

    message = db.relationship('Messages', back_populates='delivery_logs')
    user = db.relationship('Users', backref='delivery_logs')


class ScheduledMessages(db.Model):
    __tablename__ = 'scheduled_messages'

    id = db.Column(db.Integer, primary_key=True)

    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)

    schedule_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (optional but useful)
    message = db.relationship('Messages', backref=db.backref('scheduled', cascade='all, delete-orphan'))
    contact = db.relationship('Contacts', backref=db.backref('scheduled', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<ScheduledMessages message_id={self.message_id} contact_id={self.contact_id} at={self.schedule_time}>'
