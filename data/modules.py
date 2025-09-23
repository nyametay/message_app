from flask import flash, redirect, url_for
from data.models import Users, Contacts, Messages
import string
from _datetime import datetime


def is_logged_in(session):
    if 'logged_in' not in session:
        flash('Please Login User', 'danger')
        return redirect(url_for('login'))
    return None


def exception_error(e, url):
    print(str(e))
    flash('Error Occurred', 'danger')
    return redirect(url_for(url))


def get_login_info(body):
    try:
        username = body.get('username', None)
        username = username.strip() if username else None
        password = body.get('password', None)
        password = password.strip() if password else None
        if username and password:
            return username, password
        print(f'Username: {username}, password: {password}')
        return username, password
    except Exception as e:
        print(str(e))


def get_signup_info(body):
    try:
        username = body.get('username', None)
        username = username.strip() if username else None
        name = body.get('name', None)
        name = name.strip() if name else None
        email = body.get('email', None)
        email = email.strip() if email else None
        password = body.get('password', None)
        password = password.strip() if password else None
        if username and name and email and password:
            return username, name, email, password
        print(f'username: {username}, name: {name}, email: {email}, password: {password}')
        return username, name, email, password
    except Exception as e:
        print(str(e))


def strong_password(password):
    if len(password) < 8:
        return False
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    if has_lower and has_upper and has_digit and has_special:
        return True
    return False


def get_contact_info(body):
    try:
        name = body.get('name', None)
        name = name.strip() if name else None
        email = body.get('email', None)
        email = email.strip() if email else None
        phone = body.get('phone', None)
        phone = phone.strip() if phone else None
        return name, phone, email
    except Exception as e:
        print(str(e))


def get_contact_info_(body):
    try:
        contact_id = body.get('id', None)
        name = body.get('name', None)
        name = name.strip() if name else None
        email = body.get('email', None)
        email = email.strip() if email else None
        phone = body.get('phone', None)
        phone = phone.strip() if phone else None
        return contact_id, name, phone, email
    except Exception as e:
        print(str(e))


def get_message_info(body):
    try:
        channel = body.get('message_type', None)
        channel = channel.strip() if channel else None
        message = body.get('message', None)
        message = message.strip() if message else None
        subject = ''
        if 'subject' in body:
            subject = body.get('subject', None)
            subject = subject.strip() if subject else None
        schedule_time = body.get('schedule_time', None)
        action = body.get('action', None)
        schedule_time = datetime.fromisoformat(schedule_time)
        status = 'pending'
        if action == 'save':
            status = 'Not Scheduled'
        if channel == 'email':
            content = {
                'message': message,
                'subject': subject
            }
        else:
            content = {
                'message': message,
                'subject': subject
            }
        return channel, content, schedule_time, status, action
    except Exception as e:
        print(str(e))


def get_updated_message_info(body):
    try:
        channel = body.get('message_type', None)
        channel = channel.strip() if channel else None
        message = body.get('content', None)
        message = message.strip() if message else None
        subject = ''
        if 'subject' in body:
            subject = body.get('subject', None)
            subject = subject.strip() if subject else None
        schedule_time = body.get('schedule_time', None)
        schedule_time = datetime.fromisoformat(schedule_time)
        if channel == 'email':
            content = {
                'message': message,
                'subject': subject
            }
        else:
            content = {
                'message': message,
                'subject': subject
            }
        return content, schedule_time
    except Exception as e:
        print(str(e))


def get_passwords(body):
    try:
        new_password = body.get('new_password', None)
        new_password = new_password.strip() if new_password else None
        old_password = body.get('old_password', None)
        old_password = old_password.strip() if old_password else None
        return new_password, old_password

    except Exception as e:
        print(str(e))


def group_contacts(contacts):
    phones = []
    emails = []
    for contact in contacts:
        if contact.phone:
            phones.append(contact)
        if contact.email:
            emails.append(contact)
    return {
        'Phone': phones,
        'Email': emails
    }


def get_user(username):
    user = Users.query.filter_by(username=username).first()
    return user
