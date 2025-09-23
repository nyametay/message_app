from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure "instance" directory exists
instance_dir = os.path.join(basedir, "instance")
os.makedirs(instance_dir, exist_ok=True)

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=10)

# Secret Key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database Path
db_path = os.path.join(instance_dir, "data.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Celery
celery = Celery(app.name, broker=os.getenv('CELERY_BROKER_URL'))
celery.conf.update(app.config)

# Import routes
from data import routes
