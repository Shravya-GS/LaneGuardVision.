# LaneGuard Vision 🛣️👁️
> **AI-Powered Highway Lane Enforcement System MVP**

A real-time computer vision system built for **Smart India Hackathon** to detect heavy vehicles illegally occupying fast lanes on National Highways.

---

### 🚨 FOR HACKATHON EVALUATORS
**This project requires a Python backend to run AI models.**
*   **Live Demo**: [Click here to check if the session is active](YOUR_NGROK_LINK_HERE) *(Session depends on the developer's machine being online)*.
*   **Video Walkthrough**: [Watch Demo Video](YOUR_YOUTUBE_OR_DRIVE_LINK_HERE)
*   **Backend Code**: See the `backend/` folder for the YOLOv8 + FastAPI logic.
*   **Frontend Code**: See the `frontend/index.html` for the React-based dashboard.

---

## 🚀 Features
*   **Live Vehicle Detection**: Uses **YOLOv8** + **OpenCV** to detect Trucks, Buses, Cars, and People.
*   **Virtual Lane Enforcement**: Monitors a defined "Fast Lane" zone and tracks vehicle duration.
*   **Smart Alerts**: Triggers **MQTT Alerts** when a Heavy Vehicle stays in the fast lane for >5 seconds.
*   **Real-time Dashboard**: A futuristic, dark-mode **React** UI (served via CDN) showing live video and violation stats.
*   **Dynamic Logging**: Logs violations with timestamps and vehicle IDs.

## 🛠️ Tech Stack
*   **Backend**: Python, FastAPI, Uvicorn
*   **AI/CV**: YOLOv8 (Ultralytics), OpenCV
*   **Frontend**: HTML5, React.js (CDN), TailwindCSS
*   **Data**: MQTT (Paho), JSON

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/LaneGuard.git
    cd LaneGuard
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```
    *(Note: If strict versions fail, just install: `ultralytics opencv-python fastapi uvicorn paho-mqtt`)*

3.  **Setup Models**:
    *   The app uses `yolov8n.pt`. If it's missing, run:
        ```bash
        python download_model.py
        ```

## 🚥 How to Run

1.  **Start the Application**:
    Double-click **`run_app.bat`** (Windows) 
    
    OR run via terminal:
    ```bash
    python -m backend.main
    ```

2.  **Open Dashboard**:
    Go to 👉 **[http://localhost:8000](http://localhost:8000)**

## 🌐 Sharing with Evaluators (ngrok)
If you need to show the app to someone else (hackathon judges) without them installing anything:
1.  Run `run_app.bat` to start the server.
2.  Run `python start_share.py` in a separate terminal.
3.  Copy the **Public Link** generated and paste it into the "Live Demo" section of this README.

## ⚙️ Configuration

### 📹 Video Source
*   **Webcam**: To use your webcam, **delete** `highway_sample.mp4` from the root folder.
*   **Video File**: To use a video, place any MP4 file named `highway_sample.mp4` in the root folder. (The app currently includes a sample video).

### 🚛 Detection Logic
**Debug Mode (Current)**:
The `backend/detector.py` is currently configured to detect **Everything** (Cars, Persons, Trucks) for demo purposes.

**Strict Mode (Heavy Vehicles Only)**:
Edit `backend/detector.py`:
```python
# Change this line:
self.HV_CLASSES = [0, 2, 5, 7] 
# To this (Bus & Truck only):
self.HV_CLASSES = [5, 7]
```

## 📡 MQTT Alerts
Alerts are published to `highway/enforcement/alerts` on `broker.hivemq.com` (Public Broker).

## 📄 License
MIT License. Built for Hackathon purposes.
