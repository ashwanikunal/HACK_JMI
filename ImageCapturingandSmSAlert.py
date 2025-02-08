import cv2
import requests
import time
from flask import Flask
from threading import Thread
from twilio.rest import Client  # Twilio for SMS

# Telegram Bot Config
BOT_TOKEN = "8028762992:AAHlZp0Zqs62Oo5JO-f5NjcIVss_DwK7O_Y"
CHAT_ID = "1679951985"

# Twilio API Credentials
TWILIO_SID = "ACc427db8accbb063803c7a71eb481af6c"
TWILIO_AUTH_TOKEN = "7d8813849a6c19840ef0621c4e00c73c"
TWILIO_PHONE = "+16364225520"  # Twilio number
USER_PHONE = "+917900837275"  # Your phone number

app = Flask(__name__)

# Global flag for continuous capture
continuous_capture_flag = False

# Load the pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def send_sms(message):
    """Send SMS alert using Twilio."""
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=USER_PHONE
        )
        print(f"📩 SMS Sent! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending SMS: {e}")


def send_image_to_telegram(image_path, message):
    """Send the captured image and message to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": message}
        response = requests.post(url, files=files, data=data)
        print("📤 Telegram API Response:", response.json())


def detect_objects(frame):
    """Detect objects in the image (basic motion detection)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    return blurred


def detect_face(frame):
    """Detect faces in the image."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces


def continuous_capture():
    """Continuously capture images while the flag is True."""
    global continuous_capture_flag
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return
    
    first_frame = None
    
    while continuous_capture_flag:
        ret, frame = cap.read()
        if ret:
            image_path = "intruder.jpg"
            cv2.imwrite(image_path, frame)
            print("📷 Image captured!")
            
            # Detect motion
            gray_frame = detect_objects(frame)
            if first_frame is None:
                first_frame = gray_frame
                continue
            
            frame_diff = cv2.absdiff(first_frame, gray_frame)
            thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
            
            if thresh.sum() > 5000:  # If there is a significant difference (motion detected)
                print("🚨 Motion detected! Sending alerts...")
                send_image_to_telegram(image_path, "🚨 Someone is there!")
                send_sms("🚨 Someone is there! face not detected ")
            
            # Detect face
            faces = detect_face(frame)
            if len(faces) > 0:
                print("👤 Face detected! Sending alerts...")
                send_image_to_telegram(image_path, "🚨 Person is in front of the camera!")
                send_sms("🚨 Someone is at the door! Check Telegram for image.")
            
        else:
            print("❌ Failed to capture image.")
        time.sleep(0.200)  # Capture an image every 1 second
    cap.release()

@app.route("/start_intruder", methods=["GET"])
def start_intruder():
    """Start continuous image capture."""
    global continuous_capture_flag
    if not continuous_capture_flag:
        continuous_capture_flag = True
        Thread(target=continuous_capture).start()
        return "Started continuous capture.", 200
    else:
        return "Continuous capture already running.", 200

@app.route("/stop_intruder", methods=["GET"])
def stop_intruder():
    """Stop the continuous image capture."""
    global continuous_capture_flag
    continuous_capture_flag = False
    return "Stopped continuous capture.", 200

@app.route("/", methods=["GET"])
def home():
    """Health-check endpoint."""
    return "Server is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
