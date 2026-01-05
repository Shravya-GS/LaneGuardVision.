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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend", "index.html")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Video Source Configuration
# Priority: 1. Webcam (index 0), 2. Local file, 3. Error
def get_video_source():
    # Try webcam 0 first
    test_cap = cv2.VideoCapture(0)
    if test_cap.isOpened():
        success, _ = test_cap.read()
        test_cap.release()
        if success:
            print("INFO: Live Webcam detected. Using Camera Index 0.")
            return 0
    
    # Fallback to local file
    VIDEO_PATH = os.path.join(BASE_DIR, "highway_sample.mp4")
    if os.path.exists(VIDEO_PATH):
        print(f"INFO: No webcam active. Using sample video: {VIDEO_PATH}")
        return VIDEO_PATH
    
    print("CRITICAL ERROR: No video source (webcam or file) found!")
    return None

video_source = get_video_source()

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
    if not os.path.exists(FRONTEND_PATH):
        return HTMLResponse(content=f"<h1>Error: Frontend file not found at {FRONTEND_PATH}</h1>", status_code=404)
    with open(FRONTEND_PATH, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

if __name__ == "__main__":
    print("-" * 30)
    print("STARTING LANEGUARD VISION BACKEND")
    print("-" * 30)
    uvicorn.run(app, host="0.0.0.0", port=8000)
