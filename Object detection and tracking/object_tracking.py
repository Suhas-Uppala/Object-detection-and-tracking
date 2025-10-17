# Object Tracking with Trajectory Visualization
# Author: Suhas Uppala
# GitHub: https://github.com/Suhas-Uppala
# Educational Purpose Only

import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
od = ObjectDetection()

# Video source - you can change this to:
# 0 for webcam, or path to video file
VIDEO_SOURCE = "los_angeles.mp4"
# Change to 0 for webcam
cap = cv2.VideoCapture(VIDEO_SOURCE)

# Check if video opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video source '{VIDEO_SOURCE}'")
    print("If using a video file, make sure it exists in the project directory")
    print("Or change VIDEO_SOURCE to 0 to use your webcam")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f"Video Info: {frame_width}x{frame_height} @ {fps} FPS")

# Initialize tracking variables
count = 0
center_points_prev_frame = []
tracking_objects = {}
track_id = 0

# Store object information (class_id, confidence)
object_info = {}

# Store trajectory history for each object
# Format: {object_id: [(x1, y1), (x2, y2), ...]}
trajectory_history = {}
MAX_TRAJECTORY_POINTS = 30  # Maximum points to keep in trajectory (adjust for longer/shorter trails)

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        print("End of video or cannot read frame")
        break

    # Point current frame
    center_points_cur_frame = []
    detected_objects = []  # Store (center, class_id, score, box)

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    
    for i, box in enumerate(boxes):
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        
        class_id = class_ids[i]
        score = scores[i]
        
        center_points_cur_frame.append((cx, cy))
        detected_objects.append({
            'center': (cx, cy),
            'box': (x, y, w, h),
            'class_id': class_id,
            'score': score
        })
        
        # Draw detection box (green)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
                if distance < 50:  # Increased threshold for better tracking
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
                # Make older points more transparent (thinner) - optional
                thickness = max(1, int(2 * (i / len(trajectory))))
                cv2.line(frame, trajectory[i-1], trajectory[i], trajectory_color, thickness)
            
            # Draw small circles at trajectory points for better visualization
            for point in trajectory[:-1]:  # Don't draw on current position
                cv2.circle(frame, point, 2, trajectory_color, -1)
    
    # Draw tracking information
    for object_id, pt in tracking_objects.items():
        # Draw center point (larger and more visible)
        cv2.circle(frame, pt, 6, (0, 0, 255), -1)
        cv2.circle(frame, pt, 8, (255, 255, 255), 1)  # White outline
        
        # Get object information
        if object_id in object_info:
            info = object_info[object_id]
            label = f"ID:{object_id} {info['class_name']} {info['score']:.2f}"
            
            # Draw label with background
            (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (pt[0] - 5, pt[1] - label_height - 10), 
                         (pt[0] + label_width, pt[1] - 5), (0, 0, 255), -1)
            cv2.putText(frame, label, (pt[0], pt[1] - 7), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        else:
            cv2.putText(frame, f"ID:{object_id}", (pt[0], pt[1] - 7), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display tracking count and controls
    tracking_text = f"Tracked Objects: {len(tracking_objects)} | Frame: {count}"
    cv2.putText(frame, tracking_text, (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Display controls hint
    controls_text = "ESC:Exit | P:Pause | S:Screenshot | C:Clear Trails"
    cv2.putText(frame, controls_text, (10, frame_height - 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show frame
    cv2.imshow("Object Detection and Tracking", frame)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        print("Exiting...")
        break
    elif key == ord('p'):  # Pause
        print("Paused - Press any key to continue")
        cv2.waitKey(0)
    elif key == ord('s'):  # Save screenshot
        screenshot_name = f"screenshot_frame_{count}.jpg"
        cv2.imwrite(screenshot_name, frame)
        print(f"Screenshot saved: {screenshot_name}")
    elif key == ord('c'):  # Clear trajectory trails
        trajectory_history.clear()
        print("Trajectory trails cleared")

print(f"\nProcessing complete!")
print(f"Total frames processed: {count}")
print(f"Total unique objects tracked: {track_id}")

cap.release()
cv2.destroyAllWindows()
