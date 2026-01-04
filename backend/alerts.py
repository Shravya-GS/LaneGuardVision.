import paho.mqtt.client as mqtt
import json
import time
import threading

# Configuration
MQTT_BROKER = "broker.hivemq.com"  # Public broker for demo
MQTT_PORT = 1883
MQTT_TOPIC = "highway/enforcement/alerts"

class AlertSystem:
    def __init__(self):
        self.client = mqtt.Client()
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            self.connected = True
            print(f"Connected to MQTT Broker: {MQTT_BROKER}")
        except Exception as e:
            print(f"Failed to connect to MQTT: {e}")

    def send_alert(self, violation_data):
        if not self.connected:
            return
        
        payload = {
            "timestamp": time.time(),
            "type": "LANE_VIOLATION",
            "vehicle_id": violation_data.get("id"),
            "duration": violation_data.get("duration"),
            "location": "Sector 4 - Fast Lane",
            "image_available": False # Placeholder
        }
        
        try:
            self.client.publish(MQTT_TOPIC, json.dumps(payload))
            print(f"Alert sent: {payload}")
        except Exception as e:
            print(f"Failed to send alert: {e}")

alert_system = AlertSystem()
