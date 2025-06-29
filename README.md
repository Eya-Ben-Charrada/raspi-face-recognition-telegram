# 🎥 Raspberry Pi Face Recognition with Telegram Alerts

## 📌 Overview

```bash
raspi-face-recognition-telegram/
├── known_faces/              # Store images of known people
│   └── photo1.jpg ..
├── logs/                     # Logs of detections (auto-generated)
├── snapshots/                # Snapshots of unknown faces (auto-generated)
├── main.py                   # Main face recognition and alert script
├── telegram_config.py        # Your bot token and chat ID
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md                 # Full setup instructions
```

This project uses a **Raspberry Pi 5**, **Picamera2**, and **Face Recognition** to:
- Detect and recognize known faces in real time
- Capture snapshots of unknown people
- Instantly alert you on Telegram with an image of the intruder

## 🔧 Requirements

- Raspberry Pi 5 with Raspberry Pi OS Bookworm
- PiCamera module (v2 or HQ)
- Python 3.11+
- Internet connection

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/raspi-face-recognition-telegram.git
cd raspi-face-recognition-telegram
```

2.Install dependencies

```bash
pip3 install -r requirements.txt --break-system-packages
```

3. Add at least one image to known_faces/ (e.g., person1.jpg)
4. Set up telegram_config.py

```bash
BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_telegram_chat_id_here"
```

## 🤖 Get Telegram Bot Token
1. Search for @BotFather on Telegram

2. Create a new bot → copy the token

3. Start a chat with your bot

4. Visit https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates to get your chat ID

## ▶️ Run the Project

```bash
python3 main.py
```

## 📂 Output
- All alerts for unknown people go to Telegram with photo

- Each detection (known or unknown) is logged in logs/recognitions.csv

- Unknown face snapshots are saved to snapshots/

## 🛡️ Features
- Realtime detection using face_recognition and OpenCV

- Lightweight enough for Raspberry Pi 5

- Easy alerting with requests + Telegram Bot API



---

## 🐍 `main.py`, `telegram_config.py`, `requirements.txt`

These are exactly the files we already finalized in your project. You can copy-paste them directly.

---

## 📄 `.gitignore`

```gitignore
__pycache__/
logs/
snapshots/
*.pyc
.env
