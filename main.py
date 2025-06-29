import face_recognition
import cv2
import os
import numpy as np
import csv
import time
from datetime import datetime
from picamera2 import Picamera2
import requests
from telegram_config import BOT_TOKEN, CHAT_ID

# Setup
os.makedirs("logs", exist_ok=True)
os.makedirs("snapshots", exist_ok=True)

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir("known_faces"):
    path = os.path.join("known_faces", filename)
    image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(os.path.splitext(filename)[0])

# Telegram image sender
def send_unknown_face_alert(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": "? Unknown person detected!"}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("? Unknown face alert sent.")
        else:
            print("? Failed to send alert.")

# Camera setup
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)

# Detection log
log_file = "logs/recognitions.csv"
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        csv.writer(f).writerow(["Time", "Name"])

print("? Face recognition running... Press Q to quit.")

while True:
    frame = picam2.capture_array()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        if matches:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Draw box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Log and alert
        with open(log_file, "a", newline="") as f:
            csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name])

        # If unknown, send alert with image
        if name == "Unknown":
            filename = f"snapshots/unknown_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            send_unknown_face_alert(filename)

    # Show live window
    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
