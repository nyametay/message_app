# 🚀 MessageApp – Intelligent Message Automation Platform

MessageApp is a **Flask-based message automation platform** that allows users to **schedule and send SMS, Email, and WhatsApp messages** automatically.  
It features **real-time delivery logs**, **multi-channel communication**, **dark/light theme**, **user management**, and **Celery-based background task scheduling** powered by Redis.

---

## 🧩 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Environment Variables](#environment-variables)
7. [Running with Docker](#running-with-docker)
8. [Deploying to Railway](#deploying-to-railway)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)

---

## 📘 Overview

**MessageApp** helps individuals and teams **automate communication** using a unified, intuitive interface.  
You can compose messages, choose recipients, and schedule delivery across multiple channels (SMS, Email, WhatsApp).  
The backend uses **Celery workers** and **Redis queues** to handle asynchronous message dispatching efficiently — even at scale.

---

## ✨ Features

- ✅ **User Authentication** – Secure registration and login system.  
- ✅ **Multi-Channel Messaging** – Send messages via SMS, Email, or WhatsApp.  
- ✅ **Scheduling System** – Schedule messages for future delivery.  
- ✅ **Delivery Logs** – View message delivery history and status.  
- ✅ **Profile Page** – View user details and number of scheduled messages.  
- ✅ **Settings Page** – Update email, password, and toggle dark/light mode.  
- ✅ **Dark/Light Mode** – Persistent theme toggle with a modern UI.  
- ✅ **Filtering System** – Filter logs by delivery status or message type.  
- ✅ **Celery Task Queue** – Robust background processing for sending messages.  
- ✅ **Redis Integration** – Handles task queues and scheduling efficiently.  
- ✅ **Dockerized Setup** – Simple one-command local deployment.  
- ✅ **Railway Hosting Ready** – Deploy web + worker + Redis easily.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Flask (Python) |
| **Database** | SQLite (local) / PostgreSQL (production) |
| **Task Queue** | Celery |
| **Broker / Backend** | Redis |
| **Frontend** | Tailwind CSS |
| **SMS Service** | Twilio |
| **Email Service** | SendGrid |
| **Deployment** | Railway |
| **Containerization** | Docker & Docker Compose |
| **Environment Management** | python-dotenv |

---

## 🗂 Project Structure
```
MessageApp/
│
├── data/
│   ├── __init__.py         # Flask app, DB, and Celery initialization
│   ├── models.py           # SQLAlchemy models
│   ├── routes.py           # Flask routes and views
│   ├── tasks.py            # Celery background task definitions
│   ├── static/             # JS, CSS, icons
│   └── templates/          # HTML templates (Jinja2)
│
├── instance/
│   └── data.db             # SQLite DB (local development)
│
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup (web + worker + redis)
├── requirements.txt        # Python dependencies
├── Procfile                # Railway deployment process file
├── .env.example            # Environment variable sample
└── README.md               # This file 🚀
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/MessageApp.git
cd MessageApp
```

## 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

## 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 4️⃣ Create and configure your .env file
Copy .env.example to .env and fill in all required variables.

## 5️⃣ Initialize the database
```bash
flask shell
>>> from data import db
>>> db.create_all()
>>> exit()
```

## 6️⃣ Run the app
- Start the Flask app:
```bash
python run.py
```
- Start the Celery worker in another terminal:
```bash
celery -A data.celery worker --loglevel=info
```

## 🔐 Environment Variables
```ini
# Flask
SECRET_KEY=your_secret_key

# Database (Local)
SQLALCHEMY_DATABASE_URI=sqlite:///instance/data.db

# Database (Production)
DATABASE_URL=postgresql://username:password@host:port/dbname

# Redis
REDIS_URL=redis://default:<password>@<host>:<port>

# Celery
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_SENDER_EMAIL=you@example.com
```

## 🐳 Running with Docker
Build and start services
```bash
docker-compose up --build
```

This will start:
- Flask web server
- Celery worker
- Redis broker

Stop containers
```bash
docker-compose down
```

## ☁️ Deploying to Railway
- Create a new project on Railway.
- Add three services:
- Web Service → Flask app
- Worker Service → Celery worker
- Redis Service → Redis broker
- Add your environment variables (from .env) in the Variables tab.
- Add this Procfile:
```less
web: python run.py
worker: celery -A data.celery worker --loglevel=info --concurrency=1
```
- Deploy all services inside the same Railway project.

## 🧰 Troubleshooting
Problem	Possible Fix
- Celery crashes	Reduce concurrency to 1 (--concurrency=1)
- SQLite path not found	Use PostgreSQL with DATABASE_URL
- Worker memory crash	Use lower concurrency and small instance size
- Emails not received	Verify SendGrid sender and check spam
- Twilio trial messages	Upgrade Twilio or verify recipient
- Redis not connecting	Use the Redis public URL from Railway

## 🪪 License
MIT License

## 👨‍💻 Author
Isaac Nyame Taylor
📧 nyameget@gmail.com
💻 github.com/nyameget
