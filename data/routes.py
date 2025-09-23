from twilio.rest.conversations.v1.conversation.message.delivery_receipt import DeliveryReceiptInstance
from data import app, db
from flask import request, render_template, redirect, url_for, session, flash
from data.models import Users, Messages, Contacts, ScheduledMessages, DeliveryLogs
from data.modules import get_login_info, get_signup_info, strong_password, get_contact_info, is_logged_in, exception_error, \
    get_message_info, get_passwords, get_user, get_contact_info_, get_updated_message_info
from data.tasks import send_scheduled_message


# Welcome page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# signup page
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('signup.html')
    try:
        username, name, email, password = get_signup_info(request.form)
        user = Users.query.filter_by(username=username).all()
        if len(user) != 0:
            flash('Account Exist', 'danger')
            return redirect(url_for('login'))
        if not strong_password(password):
            flash('Weak Password', 'danger')
            return redirect(url_for('register'))
        if len(Users.query.filter_by(email=email).all()) != 0:
            flash('Email Already In Use', 'danger')
            return redirect(url_for('register'))
        new_user = Users(username=username, name=name, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        flash('User Created Successfully', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        return exception_error(e, 'register')


# Sign in page and user authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')

    try:
        username, password = get_login_info(request.form)
        user = get_user(username)
        if not user:
            flash('User Not Found', 'danger')
            return redirect(url_for('login'))
        if user and not user.check_password(password):
            flash('Wrong User Credentials', 'danger')
            return redirect(url_for('login'))
        session['user'] = user.to_dict()
        session['logged_in'] = True
        flash('Login Successfully', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        return exception_error(e, 'login')


# Displays the home page
@app.route('/home', methods=['GET'])
def home():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        user_id = session.get('user').get('id')
        scheduled_messages = Messages.query.filter_by(user_id=user_id, status='sent').all()
        return render_template('home.html', messages=scheduled_messages)
    except Exception as e:
        return exception_error(e, 'home')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# Displays the profile feature
@app.route('/profile', methods=['GET'])
def profile():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        user = session['user']
        user_id = user.get('id')
        # Stats
        total_messages = Messages.query.filter_by(user_id=user_id).count()
        sent_messages = Messages.query.filter_by(user_id=user_id, status='sent').count()
        failed_messages = Messages.query.filter_by(user_id=user_id, status='failed').count()
        return render_template(
            'profile.html',
            user=user,
            total_messages=total_messages,
            sent_messages=sent_messages,
            failed_messages=failed_messages
        )
    except Exception as e:
        return exception_error(e, 'profile')


# Displays the logs of scheduled messages
@app.route('/logs')
def logs():
    resp = is_logged_in(session)
    if resp:
        return resp

    user_id = session.get('user').get('id')
    status_filter = request.args.get('status')

    query = DeliveryLogs.query.filter_by(user_id=user_id).order_by(DeliveryLogs.delivery_time.desc())
    if status_filter:
        query = query.filter_by(delivery_status=status_filter)

    log = query.all()
    return render_template("logs.html", logs=log)


# Displays settings feature
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':
            user = session['user']
            return render_template('settings.html', user=user)
    except Exception as e:
        return exception_error(e, 'settings')


# Edits the users email
@app.route('/settings/email', methods=['POST'])
def update_email():
    try:
        user = Users.query.get_or_404(session['user']['id'])
        new_email = request.form['email']
        password = request.form['password']
        if not user.check_password(password):
            flash("Wrong Credentials", "danger")
            return redirect(url_for('settings'))
        if user.email == new_email:
            flash("Email Already In Use", "danger")
            return redirect(url_for('settings'))
        user.email = new_email
        db.session.commit()
        session['user']['email'] = new_email
        flash("Email updated successfully!", "success")
        return redirect(url_for('settings'))
    except Exception as e:
        return exception_error(e, 'settings')


# Edits the password of the user
@app.route('/settings/password', methods=['POST'])
def update_password():
    try:
        user = Users.query.get_or_404(session['user']['id'])
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if user.check_password(current_password):
            user.password = new_password
            db.session.commit()
            session['user']['password'] = new_password
            flash("Password updated successfully!", "success")
        else:
            flash("Current password is incorrect.", "danger")
        return redirect(url_for('settings'))
    except Exception as e:
        return exception_error(e, 'settings')


# Create a new contacts and view existing ones
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':
            user_id = session['user']['id']
            contact = Contacts.query.filter_by(user_id=user_id).all()
            contact = contact if len(contact) != 0 else None
            return render_template('contacts.html', contacts=contact)

        username = session['user']['username']
        user = get_user(username)
        name, phone, email = get_contact_info(request.form)
        new_contacts = Contacts(name=name, phone=phone, email=email, user=user)
        db.session.add(new_contacts)
        db.session.commit()
        flash('Contact Saved Successfully', 'success')
        return redirect(url_for('contacts'))
    except Exception as e:
        return exception_error(e, 'contacts')


# Edits an existing contact
@app.route('/contacts/edit/', methods=['POST'])
def update_contact():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        contact_id, name, phone, email = get_contact_info_(request.form)
        contact = Contacts.query.get_or_404(contact_id)
        contact.name = name
        contact.email = email
        contact.phone = phone
        db.session.commit()
        flash('Contact Updated Successfully', 'success')
        return redirect(url_for('contacts'))
    except Exception as e:
        return exception_error(e, 'contact')


@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        contact = Contacts.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact Deleted Successfully', 'success')
        return redirect(url_for('contacts'))
    except Exception as e:
        return exception_error(e, 'contacts')


# Creates and displays messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        if request.method == 'GET':
            user_id = session['user']['id']
            message = Messages.query.filter_by(user_id=user_id).all()
            message = message if len(message) != 0 else None
            return render_template('message.html', messages=message)

        channel, content, schedule_time, status, action = get_message_info(request.form)
        user_id = session['user']['id']
        message = Messages(channel=channel, content=content, status=status, schedule_time=schedule_time, user_id=user_id)
        db.session.add(message)
        db.session.commit()
        flash('Message Saved Successfully', 'success')
        if action == 'save':
            return redirect(url_for('messages'))
        return redirect(url_for('schedule', message_id=message.id))
    except Exception as e:
        return exception_error(e, 'messages')


@app.route('/schedule/<int:message_id>', methods=['GET', 'POST'])
def schedule(message_id):
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        message = Messages.query.get_or_404(message_id)
        channel = message.channel.lower()

        # Fetch contacts with required data only
        contacts_data = Contacts.query.filter_by(user_id=session['user']['id']).all()

        if request.method == 'POST':
            contact_ids = request.form.getlist('contacts')

            for cid in contact_ids:
                schedule_ = ScheduledMessages(message_id=message.id, contact_id=cid, schedule_time=message.schedule_time)
                db.session.add(schedule_)

            db.session.commit()

            user_id = session['user']['id']
            # Pass list of contact IDs to Celery task and schedule it
            send_scheduled_message.apply_async(
                args=[message.id, contact_ids, user_id],
                eta=message.schedule_time
            )

            flash('Message scheduled successfully!', 'success')
            return redirect(url_for('messages'))

        return render_template('schedule.html', message=message, contacts=contacts_data, channel=channel)
    except Exception as e:
        print(str(e))
        flash(f"Error: {str(e)}", 'danger')
        return redirect(url_for('schedule', message_id=message_id))


# Edits existing messages
@app.route('/messages/edit/<int:message_id>', methods=['GET', 'POST'])
def update_message(message_id):
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        message = Messages.query.get_or_404(message_id)
        if request.method == 'GET':
            return render_template('update_message.html', message=message)

        content, schedule_time = get_updated_message_info(request.form)
        message.content = content
        message.schedule_time = schedule_time
        db.session.commit()
        flash('Message Changed Successfully', 'success')
        return redirect(url_for('messages'))
    except Exception as e:
        return exception_error(e, f'update_message/{message_id}')


# Deletes a message that has been saved
@app.route('/messages/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        message = Messages.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        flash('Message Deleted Successfully', 'success')
        return redirect(url_for('messages'))
    except Exception as e:
        return exception_error(e, 'messages')


# Helps the user log out of the system
@app.route('/logout', methods=['GET'])
def logout():
    resp = is_logged_in(session)
    if resp:
        return resp
    try:
        session.pop('logged_in', None)
        session.pop('user', None)
        flash('Logged Out Successfully', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        return exception_error(e, 'logout')
