from ultralytics import YOLO
import os

print("Downloading YOLOv8n model...")
try:
    if os.path.exists("yolov8n.pt"):
        os.remove("yolov8n.pt")
        print("Removed existing model file.")
        
    model = YOLO("yolov8n.pt")
    print("Model downloaded successfully.")
except Exception as e:
    print(f"Error downloading model: {e}")
