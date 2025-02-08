# HACK_JMI
 
Digital Theft Prevention Lock is an advanced AI-driven smart security system that captures an image when a person comes within 10 cm of the lock. Using ESP32, OpenCV, Flask, Telegram Bot, and Twilio SMS, it provides real-time intrusion detection with instant alerts to keep your valuables safe.

📌 Features
✔️ Proximity-Based Image Capture – Captures an intruder's image when they approach within 10 cm.
✔️ AI-Powered Motion & Face Detection – Detects unauthorized movement and identifies faces.
✔️ Instant Alerts – Sends Telegram notifications and SMS alerts (via Twilio) in real time.
✔️ Remote Monitoring & Control – Users can start/stop detection via a Flask web interface.
✔️ Secure IoT Integration – Works wirelessly with ESP32, making it ideal for smart home security.

⚙️ Technologies Used
ESP32 – IoT-based microcontroller for sensor integration.
OpenCV – Real-time motion and face detection.
Flask – Web interface for remote control.
Telegram Bot API – Sends images & intrusion alerts.
Twilio API – Sends SMS notifications in case of security breaches.

🚀 How It Works
The system continuously monitors the area using ESP32 and an ultrasonic sensor.
If a person comes within 10 cm, it captures an image using OpenCV.
The captured image is sent to a Telegram Bot along with an alert message.
If no face is detected, a Twilio SMS alert is sent to notify the owner.
The user can remotely start or stop monitoring using a Flask web interface.
