# Live Camera Object Tracking with Trajectory Visualization
# Author: Suhas Uppala
# GitHub: https://github.com/Suhas-Uppala
# Educational Purpose Only

import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
print("Initializing Object Detection for Live Camera...")
od = ObjectDetection()

# Camera settings
CAMERA_INDEX = 0  # 0 for default webcam, 1 for external camera
CAMERA_WIDTH = 640  # Reduced resolution for better FPS (was 1280)
CAMERA_HEIGHT = 480  # Reduced resolution for better FPS (was 720)
CAMERA_FPS = 30  # Desired FPS

# Detection settings for better performance
PROCESS_EVERY_N_FRAMES = 2  # Process every 2nd frame for faster performance
NMS_THRESHOLD = 0.3  # Non-maximum suppression (lower = less overlapping boxes)
CONFIDENCE_THRESHOLD = 0.4  # Detection confidence (lower = more detections, higher = more accurate)

# Initialize camera
cap = cv2.VideoCapture(CAMERA_INDEX)

# Set camera properties for better quality
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

# Check if camera opened successfully
if not cap.isOpened():
    print(f"Error: Could not open camera {CAMERA_INDEX}")
    print("Troubleshooting:")
    print("  1. Check if camera is connected")
    print("  2. Try changing CAMERA_INDEX to 1 or 2")
    print("  3. Close other applications using the camera")
    exit()

# Get actual camera properties
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f"Camera initialized: {actual_width}x{actual_height} @ {actual_fps} FPS")
print("Press ESC to exit, P to pause, S to screenshot, C to clear trails")

# Initialize tracking variables
count = 0
frame_skip_counter = 0
center_points_prev_frame = []
tracking_objects = {}
track_id = 0
last_detected_objects = []  # Cache last detection results

# Store object information (class_id, confidence)
object_info = {}

# Store trajectory history for each object
# Format: {object_id: [(x1, y1), (x2, y2), ...]}
trajectory_history = {}
MAX_TRAJECTORY_POINTS = 50  # Longer trails for live camera (adjust as needed)

# Performance tracking
import time
fps_start_time = time.time()
fps_counter = 0
current_fps = 0

while True:
    ret, frame = cap.read()
    count += 1
    frame_skip_counter += 1
    
    if not ret:
        print("Error: Failed to grab frame from camera")
        break

    # Calculate FPS
    fps_counter += 1
    if (time.time() - fps_start_time) > 1:
        current_fps = fps_counter / (time.time() - fps_start_time)
        fps_counter = 0
        fps_start_time = time.time()

    # Point current frame
    center_points_cur_frame = []
    detected_objects = []  # Store (center, class_id, score, box)

    # PERFORMANCE BOOST: Only run detection every N frames
    if frame_skip_counter >= PROCESS_EVERY_N_FRAMES:
        frame_skip_counter = 0
        # Detect objects on frame with optimized thresholds
        (class_ids, scores, boxes) = od.detect(frame, nmsThreshold=NMS_THRESHOLD, confThreshold=CONFIDENCE_THRESHOLD)
        last_detected_objects = []  # Reset cache
        
        for i, box in enumerate(boxes):
            (x, y, w, h) = box
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)
            
            class_id = class_ids[i]
            score = scores[i]
            
            # FILTER: Skip 'person' class (class_id = 0)
            # This makes the tracker focus on objects only (bottles, phones, cups, etc.)
            if class_id == 0:  # 'person' is class ID 0
                continue
            
            obj_data = {
                'center': (cx, cy),
                'box': (x, y, w, h),
                'class_id': class_id,
                'score': score
            }
            
            center_points_cur_frame.append((cx, cy))
            detected_objects.append(obj_data)
            last_detected_objects.append(obj_data)  # Cache for skipped frames
            
            # Draw detection box (green)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        # Use cached detections for skipped frames (improves FPS)
        detected_objects = last_detected_objects
        for obj in detected_objects:
            (x, y, w, h) = obj['box']
            cx, cy = obj['center']
            center_points_cur_frame.append((cx, cy))
            # Draw cached detection box (cyan to show it's cached)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # Tracking algorithm
    if count <= 2:
        # First frames: initialize tracking
        for i, obj in enumerate(detected_objects):
            tracking_objects[track_id] = obj['center']
            object_info[track_id] = {
                'class_id': obj['class_id'],
                'score': obj['score'],
                'class_name': od.classes[obj['class_id']]
            }
            # Initialize trajectory for this object
            trajectory_history[track_id] = [obj['center']]
            track_id += 1
    else:
        # Match detected objects with tracked objects
        tracking_objects_copy = tracking_objects.copy()
        detected_objects_copy = detected_objects.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            
            for obj in detected_objects_copy:
                pt = obj['center']
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update tracked object position if close enough
                if distance < 80:  # Increased threshold for better tracking across frames
                    tracking_objects[object_id] = pt
                    object_info[object_id] = {
                        'class_id': obj['class_id'],
                        'score': obj['score'],
                        'class_name': od.classes[obj['class_id']]
                    }
                    
                    # Update trajectory history
                    if object_id not in trajectory_history:
                        trajectory_history[object_id] = []
                    trajectory_history[object_id].append(pt)
                    
                    # Keep only last N points to prevent memory overflow
                    if len(trajectory_history[object_id]) > MAX_TRAJECTORY_POINTS:
                        trajectory_history[object_id].pop(0)
                    
                    object_exists = True
                    
                    # Remove from detected list
                    if obj in detected_objects:
                        detected_objects.remove(obj)
                    break

            # Remove lost objects
            if not object_exists:
                tracking_objects.pop(object_id)
                if object_id in object_info:
                    object_info.pop(object_id)
                # Keep trajectory for a bit even after object is lost (optional)
                # Or remove it immediately: trajectory_history.pop(object_id, None)

        # Add new detected objects that weren't matched
        for obj in detected_objects:
            tracking_objects[track_id] = obj['center']
            object_info[track_id] = {
                'class_id': obj['class_id'],
                'score': obj['score'],
                'class_name': od.classes[obj['class_id']]
            }
            # Initialize trajectory for new object
            trajectory_history[track_id] = [obj['center']]
            track_id += 1

    # Draw trajectory lines for each tracked object
    for object_id, trajectory in trajectory_history.items():
        if len(trajectory) > 1:
            # Generate a unique color for each object ID (consistent color per ID)
            color_seed = object_id * 50
            trajectory_color = (
                (color_seed * 67) % 256,
                (color_seed * 137) % 256,
                (color_seed * 211) % 256
            )
            
            # Draw lines connecting trajectory points
            for i in range(1, len(trajectory)):
                # Make lines progressively thicker toward current position
                thickness = max(1, int(3 * (i / len(trajectory))))
                cv2.line(frame, trajectory[i-1], trajectory[i], trajectory_color, thickness)
            
            # Draw small circles at trajectory points for better visualization
            for point in trajectory[:-1]:  # Don't draw on current position
                cv2.circle(frame, point, 3, trajectory_color, -1)
    
    # Draw tracking information
    for object_id, pt in tracking_objects.items():
        # Draw center point (larger and more visible)
        cv2.circle(frame, pt, 7, (0, 0, 255), -1)
        cv2.circle(frame, pt, 9, (255, 255, 255), 2)  # White outline
        
        # Get object information
        if object_id in object_info:
            info = object_info[object_id]
            label = f"ID:{object_id} {info['class_name']} {info['score']:.2f}"
            
            # Draw label with background
            (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (pt[0] - 5, pt[1] - label_height - 12), 
                         (pt[0] + label_width + 5, pt[1] - 5), (0, 0, 255), -1)
            cv2.putText(frame, label, (pt[0], pt[1] - 8), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(frame, f"ID:{object_id}", (pt[0], pt[1] - 7), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Display information overlay
    overlay_y = 30
    
    # Tracking count with optimization info
    tracking_text = f"Live Camera | Objects: {len(tracking_objects)} | Frame: {count}"
    cv2.putText(frame, tracking_text, (10, overlay_y), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # FPS display with performance color coding
    fps_color = (0, 255, 0) if current_fps > 20 else (0, 165, 255) if current_fps > 15 else (0, 0, 255)
    fps_text = f"FPS: {current_fps:.1f}"
    cv2.putText(frame, fps_text, (10, overlay_y + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, fps_color, 2)
    
    # Performance settings info
    perf_text = f"Resolution: {actual_width}x{actual_height} | Conf: {CONFIDENCE_THRESHOLD}"
    cv2.putText(frame, perf_text, (10, overlay_y + 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Display controls hint
    controls_text = "ESC:Exit | P:Pause | S:Screenshot | C:Clear Trails"
    cv2.putText(frame, controls_text, (10, actual_height - 15), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("Live Camera Object Tracking", frame)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        print("Exiting...")
        break
    elif key == ord('p') or key == ord('P'):  # Pause
        print("Paused - Press any key to continue")
        cv2.waitKey(0)
    elif key == ord('s') or key == ord('S'):  # Save screenshot
        screenshot_name = f"live_camera_frame_{count}.jpg"
        cv2.imwrite(screenshot_name, frame)
        print(f"Screenshot saved: {screenshot_name}")
    elif key == ord('c') or key == ord('C'):  # Clear trajectory trails
        trajectory_history.clear()
        print("Trajectory trails cleared")

print(f"\nLive camera session complete!")
print(f"Total frames processed: {count}")
print(f"Total unique objects tracked: {track_id}")

cap.release()
cv2.destroyAllWindows()
