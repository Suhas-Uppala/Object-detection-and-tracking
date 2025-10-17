# 📹 Live Camera Tracking Guide

## Overview

`live_camera_tracking.py` is designed specifically for real-time object detection and tracking using your webcam or external camera with visual trajectory trails.

## 🚀 Quick Start

### Run the Live Camera Tracker

```bash
python live_camera_tracking.py
```

That's it! The application will automatically:
- 🎥 Open your default webcam
- 🎯 Start detecting objects in real-time
- 🌈 Draw colored trajectory trails
- 📊 Display FPS and tracking statistics

## 🎮 Controls

| Key | Function | Description |
|-----|----------|-------------|
| **ESC** | Exit | Close the application |
| **P** | Pause | Freeze current frame (press any key to resume) |
| **S** | Screenshot | Save current frame with trajectories |
| **C** | Clear Trails | Clear all trajectory history |

## ⚙️ Configuration

### Camera Settings

Edit these variables in `live_camera_tracking.py`:

```python
# Camera selection
CAMERA_INDEX = 0        # 0 = default webcam, 1 = external camera, 2 = second external

# Resolution
CAMERA_WIDTH = 1280     # Width in pixels
CAMERA_HEIGHT = 720     # Height in pixels

# Frame rate
CAMERA_FPS = 30         # Desired frames per second
```

### Trajectory Settings

```python
# Trail length
MAX_TRAJECTORY_POINTS = 50  # Longer = longer trails
                            # 20 = short, 50 = medium, 100 = long

# Tracking sensitivity
if distance < 60:  # Increase for fast-moving objects
                   # 40 = strict, 60 = balanced, 80 = loose
```

## 🎯 Features Specific to Live Camera

### 1. Real-Time FPS Display
Shows actual processing speed in the top-left corner

### 2. Optimized for Live Feed
- Longer trajectory trails (50 points default)
- Larger distance threshold (60 pixels)
- Thicker trajectory lines for visibility

### 3. Higher Resolution Support
- Default: 1280x720
- Easily adjustable for 1920x1080 or lower resolutions

### 4. Live Statistics
- Current frame count
- Number of tracked objects
- Real-time FPS

## 📊 Display Elements

When running, you'll see:

```
┌─────────────────────────────────────────────┐
│ Live Camera | Objects: 3 | Frame: 1234     │
│ FPS: 28.5                                   │
│                                             │
│     🟢 ← Detection box                     │
│     🔵━━━━━━━━⚪ ← Trajectory + current    │
│     ID:1 person 0.89 ← Label               │
│                                             │
│ ESC:Exit | P:Pause | S:Screenshot | C:Clear│
└─────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### Camera Not Opening

**Problem:** "Error: Could not open camera 0"

**Solutions:**
1. Check if camera is connected and enabled
2. Close other applications using the camera (Zoom, Teams, Skype)
3. Try different camera indices:
   ```python
   CAMERA_INDEX = 1  # or 2, 3, etc.
   ```
4. Check camera permissions in Windows Settings

### Low FPS / Laggy Performance

**Solutions:**

1. **Reduce resolution:**
   ```python
   CAMERA_WIDTH = 640
   CAMERA_HEIGHT = 480
   ```

2. **Lower detection quality:**
   In `object_detection.py`:
   ```python
   self.image_size = 320  # Instead of 608
   ```

3. **Reduce trajectory points:**
   ```python
   MAX_TRAJECTORY_POINTS = 20
   ```

4. **Close other programs** to free up CPU/GPU resources

### Camera Shows Wrong Device

**Problem:** Opens wrong camera (e.g., front instead of back)

**Solution:** Change camera index:
```python
CAMERA_INDEX = 0  # Try 0, 1, 2, 3 until correct camera opens
```

### Objects Not Being Detected

**Solutions:**

1. **Lower confidence threshold:**
   In `object_detection.py`:
   ```python
   self.confThreshold = 0.3  # Lower from 0.5
   ```

2. **Ensure good lighting** - Poor lighting reduces detection accuracy

3. **Keep objects in frame** - Objects need to be fully visible

### Trails Too Long/Short

**Adjust trail length:**
```python
MAX_TRAJECTORY_POINTS = 30  # Short trails
MAX_TRAJECTORY_POINTS = 50  # Medium trails (default)
MAX_TRAJECTORY_POINTS = 100 # Long trails
```

## 💡 Tips for Best Results

### 1. Lighting
- ✅ Good natural or artificial lighting
- ✅ Avoid backlighting (light behind objects)
- ✅ Consistent lighting across scene

### 2. Camera Position
- ✅ Stable mounting (avoid shaking)
- ✅ Good viewing angle
- ✅ Appropriate distance from subjects

### 3. Environment
- ✅ Uncluttered background
- ✅ Clear view of objects
- ✅ Minimal occlusions

### 4. Performance
- ✅ Close unnecessary applications
- ✅ Use lower resolution for better FPS
- ✅ GPU acceleration helps significantly

## 🎯 Use Cases

### Home Security
Monitor your home entrance or specific areas:
```python
CAMERA_INDEX = 0  # USB camera at entrance
MAX_TRAJECTORY_POINTS = 100  # Long trails to see paths
```

### Traffic Monitoring
Track vehicles or pedestrians:
```python
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
MAX_TRAJECTORY_POINTS = 50
```

### Workspace Monitoring
Track people or objects in workspace:
```python
CAMERA_INDEX = 1  # External camera
MAX_TRAJECTORY_POINTS = 30
```

### Pet Monitoring
Track pet movements:
```python
CAMERA_FPS = 30
MAX_TRAJECTORY_POINTS = 60  # Medium-long trails
```

## 📸 Saving Recordings

### Save Screenshots
Press **S** during operation to save individual frames.

### Record Video (Advanced)
Add this code after camera initialization:

```python
# After cap = cv2.VideoCapture(CAMERA_INDEX)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('live_recording.mp4', fourcc, 20.0, 
                     (actual_width, actual_height))

# In the main loop, before cv2.imshow()
out.write(frame)

# Before cap.release()
out.release()
```

## 🔄 Differences from Video File Version

| Feature | live_camera_tracking.py | object_tracking.py |
|---------|------------------------|-------------------|
| Input Source | Live camera feed | Video files |
| Trajectory Length | 50 points (longer) | 30 points |
| Distance Threshold | 60 pixels | 50 pixels |
| FPS Display | ✅ Real-time FPS shown | ❌ Frame count only |
| Resolution Control | ✅ Configurable | Uses video resolution |
| Continuous | ✅ Runs until stopped | Ends with video |

## 🚀 Advanced Configuration

### Multiple Cameras

To use multiple cameras simultaneously, run multiple instances:

**Terminal 1:**
```bash
python live_camera_tracking.py  # Uses CAMERA_INDEX = 0
```

**Terminal 2:**
Modify the file to use `CAMERA_INDEX = 1` and run again

### Custom Object Filtering

To track only specific objects (e.g., only people):

```python
# After line: class_id = class_ids[i]
if od.classes[class_id] not in ['person', 'car']:
    continue  # Skip objects that aren't person or car
```

### Adjusting Trajectory Colors

For brighter trails:
```python
trajectory_color = (
    255,  # Full red
    (color_seed * 137) % 256,
    (color_seed * 211) % 256
)
```

## 📞 Support

For issues specific to live camera tracking:

1. Check camera permissions in OS settings
2. Verify camera works in other applications
3. Try different camera indices (0, 1, 2)
4. Check USB connections for external cameras
5. Review [TROUBLESHOOTING.md](USAGE_GUIDE.md#troubleshooting)

## 🎉 You're Ready!

Start tracking objects in real-time:

```bash
cd "Object detection and tracking"
python live_camera_tracking.py
```

Press **ESC** to exit when done. Happy tracking! 🎯
