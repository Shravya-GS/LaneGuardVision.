import cv2
import time
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
from .alerts import alert_system

class LaneDetector:
    def __init__(self, source=0):
        # Load the YOLOv8 model
        self.model = YOLO("yolov8n.pt")
        
        # Heavy Vehicle Classes in COCO: 5 (bus), 7 (truck)
        # For Testing: Adding 0 (person) and 2 (car) to verify webcam works
        self.HV_CLASSES = [0, 2, 5, 7]
        
        # Tracking data
        self.track_history = defaultdict(lambda: [])
        self.violation_start_times = {}
        self.violation_durations = {} # Store completed violation durations or current
        self.active_violations = set()
        
        # Stats
        self.stats = {
            "total_hvs": 0,
            "active_violations": 0,
            "total_violations": 0,
            "lane_occupancy": "Low"
        }

        # Fast Lane Definition (Polygon)
        # Normalized coordinates (0-1) to handle different resolutions
        # Assuming left lane is fast lane in this view
        self.fast_lane_poly_norm = np.array([
            [0.10, 0.90], # Bottom Left
            [0.35, 0.90], # Bottom Right
            [0.45, 0.30], # Top Right
            [0.35, 0.30]  # Top Left
        ], np.float32)
        
        self.frame_count = 0

    def is_inside_lane(self, center_point, frame_shape):
        h, w = frame_shape[:2]
        # Convert normalized poly to pixel coords
        poly_pixels = (self.fast_lane_poly_norm * [w, h]).astype(np.int32)
        
        # Check if point is inside polygon (returns +1, -1, or 0)
        result = cv2.pointPolygonTest(poly_pixels, center_point, False)
        return result >= 0, poly_pixels

    def process_frame(self, frame):
        self.frame_count += 1
        h, w = frame.shape[:2]
        
        # Run YOLOv8 tracking
        if self.frame_count % 300 == 0:
            print(f"Processing frame {self.frame_count}")
        results = self.model.track(frame, persist=True, verbose=False, classes=self.HV_CLASSES)
        
        current_ids = set()
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.int().cpu().tolist()

            for box, track_id, cls in zip(boxes, track_ids, clss):
                current_ids.add(track_id)
                x, y, w_box, h_box = box
                center = (float(x), float(y))
                
                # Check Lane Violation
                in_lane, poly_pixels = self.is_inside_lane(center, frame.shape)
                
                # Draw Lane (only once per frame essentially, but cheap to redraw)
                cv2.polylines(frame, [poly_pixels], isClosed=True, color=(0, 255, 255), thickness=2)
                
                color = (0, 255, 0) # Green (Safe)
                
                if in_lane:
                    if track_id not in self.violation_start_times:
                        self.violation_start_times[track_id] = time.time()
                    
                    duration = time.time() - self.violation_start_times[track_id]
                    self.violation_durations[track_id] = duration
                    
                    if duration > 5: # Demo Threshold: 5 seconds (Real: 30s)
                        color = (0, 0, 255) # Red (Violation)
                        if track_id not in self.active_violations:
                            self.active_violations.add(track_id)
                            self.stats["total_violations"] += 1
                            alert_system.send_alert({"id": track_id, "duration": duration})
                    else:
                        color = (0, 165, 255) # Orange (Warning)
                else:
                    # Reset if left lane
                    if track_id in self.violation_start_times:
                        del self.violation_start_times[track_id]
                    if track_id in self.active_violations:
                        self.active_violations.remove(track_id)

                # Draw Bounding Box
                x1, y1 = int(x - w_box/2), int(y - h_box/2)
                x2, y2 = int(x + w_box/2), int(y + h_box/2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Label
                label = f"ID: {track_id} {self.model.names[cls]}"
                if track_id in self.violation_durations and track_id in self.violation_start_times:
                     label += f" | {self.violation_durations[track_id]:.1f}s"
                
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Update Stats
        self.stats["active_violations"] = len(self.active_violations)
        self.stats["total_hvs"] = len(current_ids) if results[0].boxes.id is not None else 0
        
        # Cleanup missing IDs
        for tid in list(self.violation_start_times.keys()):
            if tid not in current_ids:
                del self.violation_start_times[tid]
                if tid in self.active_violations:
                    self.active_violations.remove(tid)

        return frame

detector = LaneDetector()
