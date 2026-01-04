import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import threading
import time
import os

from backend.detector import detector
# Mock weather for now
weather_data = {"temp": 28, "condition": "Sunny", "location": "Hyderabad, IN"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Video Source
VIDEO_PATH = "highway_sample.mp4"
if not os.path.exists(VIDEO_PATH):
    print(f"Warning: {VIDEO_PATH} not found. Using Webcam (0).")
    video_source = 0
else:
    video_source = VIDEO_PATH

cap = cv2.VideoCapture(video_source)
if not cap.isOpened():
    print(f"CRITICAL ERROR: Could not open video source {video_source}")
    print("If using a webcam, check that no other app is using it and you have granted permissions.")
else:
    print(f"Successfully opened video source: {video_source}")

def generate_frames():
    global cap
    while True:
        success, frame = cap.read()
        if not success:
            # Loop video
            if isinstance(video_source, str):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                print("Failed to read frame from webcam.")
                # Try to re-open or just break?
                # For debugging, let's keep trying or just sleep
                time.sleep(1)
                continue
        
        # Process Frame
        processed_frame = detector.process_frame(frame)
        
        # Encode
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Limit FPS slightly to save resources
        time.sleep(0.01)

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/stats")
async def get_stats():
    return JSONResponse(content={
        "detector": detector.stats,
        "weather": weather_data
    })

# Serve Frontend (No-Build)
@app.get("/")
async def read_index():
    with open("frontend/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
