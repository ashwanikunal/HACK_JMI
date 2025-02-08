#include <WiFi.h>
#include <HTTPClient.h>

#define TRIG_PIN 5    // Ultrasonic Sensor Trigger
#define ECHO_PIN 18   // Ultrasonic Sensor Echo
#define BUZZER_PIN 19 // Optional Buzzer for Alert

const char* ssid = "GROUND FLOOR WI-FI 4G";         // WiFi SSID
const char* password = "Jitesh@airtel"; // WiFi Password
const char* startURL = "http://192.168.1.8:5000/start_intruder";  // Flask start endpoint
const char* stopURL  = "http://192.168.1.8:5000/stop_intruder";   // Flask stop endpoint

bool capturing = false;  // Tracks if continuous capture has been started

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  Serial.print("Connecting to WiFi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to WiFi!");
}

void loop() {
  long duration;
  int distance;
  
  // Trigger the ultrasonic sensor
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Calculate distance in cm
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;
  
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // If an object is within 10 cm and continuous capture is not active
  if (distance <= 10 && !capturing) {
    Serial.println("🚨 Object detected within 10 cm. Starting continuous capture...");
    
    // Optional: Sound the buzzer briefly
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    
    sendRequest(startURL);
    capturing = true;
  }
  // If no object is detected (distance > 10 cm) and we are capturing, stop capture
  else if (distance > 10 && capturing) {
    Serial.println("Object no longer within 10 cm. Stopping continuous capture...");
    sendRequest(stopURL);
    capturing = false;
  }
  
  // If invalid reading (e.g., distance too large or zero), assume sensor is disconnected
  if (distance <= 0 || distance > 400) {
    Serial.println("❌ Invalid distance detected. Stopping continuous capture...");
    if (capturing) {
      sendRequest(stopURL);
      capturing = false;
    }
  }
  
  delay(1000); // Check every second
}

void sendRequest(const char* url) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(url);
    int httpResponseCode = http.GET();
    if(httpResponseCode > 0) {
      Serial.print("✅ Request sent to ");
      Serial.println(url);
    } else {
      Serial.print("❌ Failed to send request to ");
      Serial.println(url);
    }
    http.end();
  } else {
    Serial.println("❌ WiFi not connected. Request not sent.");
  }
}
