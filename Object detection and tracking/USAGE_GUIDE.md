# Complete Usage Guide - Object Detection & Tracking

## 🎯 What This Project Does

This project performs **real-time object detection and tracking** in videos using:
- **YOLOv4** for detecting objects (cars, people, animals, etc.)
- **Custom tracking algorithm** to follow objects across frames with unique IDs

## 📋 Prerequisites Checklist

- [ ] Python 3.7 or higher installed
- [ ] OpenCV library installed
- [ ] NumPy library installed
- [ ] YOLOv4 model files downloaded
- [ ] Video file or webcam available

## 🚀 Step-by-Step Setup

### Step 1: Install Python Dependencies

```powershell
# Install required packages
pip install opencv-python opencv-contrib-python numpy

# Verify installation
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

### Step 2: Download Model Files

**Automatic Method (Recommended):**
```powershell
python download_models.py
```

**Manual Method:**
If automatic download fails, manually download and place these files in `dnn_model/`:

1. **yolov4.weights** (245 MB)
   - Download: https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

2. **yolov4.cfg** (12 KB)
   - Download: https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg

3. **classes.txt** (1 KB)
   - Download: https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names

### Step 3: Choose Your Video Source

#### Option A: Use Video File
1. Place your video file in the project directory
2. Open `object_tracking.py`
3. Set the video filename:
```python
VIDEO_SOURCE = "your_video.mp4"
```

#### Option B: Use Webcam
1. Open `object_tracking.py`
2. Change to:
```python
VIDEO_SOURCE = 0  # 0 is usually the default webcam
```

#### Option C: Use IP Camera/RTSP Stream
```python
VIDEO_SOURCE = "rtsp://username:password@ip_address:port/stream"
```

### Step 4: Run the Application

```powershell
cd "e:\object tracking\object-tracking-opencv"
python object_tracking.py
```

## 🎮 Using the Application

### Display Information

When running, you'll see:
- **Green boxes**: Detected objects
- **Red dots**: Center points of tracked objects
- **Labels**: Show `ID:X ClassName Confidence`
- **Top overlay**: Total tracked objects and frame count

### Keyboard Controls

| Key | Function | Description |
|-----|----------|-------------|
| `ESC` | Exit | Close the application |
| `P` | Pause | Pause video playback (press any key to resume) |
| `S` | Screenshot | Save current frame as JPG file |

### Example Session

```
1. Application starts
   → "Loading Object Detection"
   → "Running opencv dnn with YOLOv4"
   → "Video Info: 1920x1080 @ 30 FPS"

2. Video plays with detections
   → Objects get green bounding boxes
   → Each object receives unique ID number
   → IDs persist as objects move

3. Console output shows:
   → Tracked Objects: 5 | Frame: 234
   → Object positions and IDs

4. Press 'S' to save screenshot
   → "Screenshot saved: screenshot_frame_234.jpg"

5. Press ESC to exit
   → "Exiting..."
   → "Processing complete!"
```

## ⚙️ Configuration & Tuning

### Adjust Detection Confidence

**File:** `object_detection.py`

```python
# Lower value = more detections (but more false positives)
# Higher value = fewer detections (but more accurate)
self.confThreshold = 0.5  # Range: 0.0 to 1.0
```

**Recommended values:**
- `0.3` - Detect almost everything (noisy)
- `0.5` - Balanced (default)
- `0.7` - Only confident detections (conservative)

### Adjust Tracking Distance

**File:** `object_tracking.py`

```python
# Distance threshold for matching objects between frames
if distance < 50:  # Pixels
```

**Recommended values:**
- Fast-moving objects: `80-100`
- Normal speed: `50` (default)
- Slow-moving: `30-40`

### Change Detection Size

**File:** `object_detection.py`

```python
# Image size for detection (larger = more accurate but slower)
self.image_size = 608  # Options: 320, 416, 512, 608
```

**Performance guide:**
- `320` - Fastest, least accurate
- `416` - Balanced
- `608` - Most accurate, slowest (default)

## 🎯 Detected Object Classes

The system can detect 80 object types from the COCO dataset:

**Vehicles:** car, truck, bus, motorcycle, bicycle, airplane, train, boat

**People:** person

**Animals:** bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

**Sports:** sports ball, baseball bat, tennis racket, frisbee, skis, snowboard, skateboard, surfboard

**Household:** chair, couch, potted plant, bed, dining table, toilet, TV, laptop, mouse, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase

**Food:** bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

**And more!** See `dnn_model/classes.txt` for complete list.

## 📊 Performance Optimization

### For Slow Systems

1. **Reduce video resolution:**
```python
# In object_tracking.py, after cap = cv2.VideoCapture(...)
frame = cv2.resize(frame, (640, 360))
```

2. **Process every Nth frame:**
```python
if count % 2 == 0:  # Process every 2nd frame
    (class_ids, scores, boxes) = od.detect(frame)
```

3. **Lower detection size:**
```python
# In object_detection.py
self.image_size = 416  # Instead of 608
```

### For Better Accuracy

1. **Increase confidence threshold:**
```python
self.confThreshold = 0.6  # Reduce false positives
```

2. **Use larger detection size:**
```python
self.image_size = 608  # Maximum accuracy
```

3. **Adjust NMS threshold:**
```python
self.nmsThreshold = 0.3  # Stricter duplicate removal
```

## 🐛 Common Issues & Solutions

### Issue: "Could not open video source"

**Possible causes:**
- Video file doesn't exist
- Wrong file path
- Unsupported video format

**Solutions:**
```python
# Use absolute path
VIDEO_SOURCE = r"C:\Users\YourName\Videos\video.mp4"

# Or test with webcam
VIDEO_SOURCE = 0

# Check if file exists
import os
print(os.path.exists("los_angeles.mp4"))
```

### Issue: "Failed to open NetParameter file"

**Cause:** Model files not downloaded

**Solution:**
```powershell
# Run the downloader
python download_models.py

# Or manually verify files exist:
dir dnn_model
```

### Issue: Very Slow Performance

**Solutions:**

1. **Check if using CPU:**
   - Look for: "CUDA not available, using CPU backend"
   - This is normal but slower

2. **Optimize settings:**
```python
# Reduce image size
self.image_size = 320

# Process fewer frames
if count % 3 == 0:  # Every 3rd frame
    (class_ids, scores, boxes) = od.detect(frame)
```

3. **Use smaller video:**
   - Reduce resolution to 720p or 480p

### Issue: No Objects Detected

**Solutions:**

1. **Lower confidence threshold:**
```python
self.confThreshold = 0.3  # From 0.5
```

2. **Check video content:**
   - Make sure video contains detectable objects
   - Test with different video

3. **Verify model files:**
   - Ensure `yolov4.weights` is 245 MB
   - Redownload if corrupted

### Issue: Objects Losing IDs

**Solutions:**

1. **Increase tracking distance:**
```python
if distance < 80:  # From 50
```

2. **Process more frames:**
   - Don't skip frames in tracking

3. **Improve detection:**
```python
self.confThreshold = 0.4  # Lower value
```

## 📸 Saving Output

### Save Individual Frames

Press `S` during playback to save current frame.

### Save Entire Processed Video

Add this code after video initialization:

```python
# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Create video writer
out = cv2.VideoWriter('output.mp4',
                      cv2.VideoWriter_fourcc(*'mp4v'),
                      fps,
                      (frame_width, frame_height))

# In the main loop, before cv2.imshow():
out.write(frame)

# At the end, before cap.release():
out.release()
```

## 🎓 Understanding the Output

### Object Labels Format

```
ID:5 car 0.87
│   │    │
│   │    └─ Confidence score (87%)
│   └────── Object class name
└────────── Unique tracking ID
```

### Console Output

```
Tracked Objects: 3 | Frame: 145
│                   │
│                   └─ Current frame number
└───────────────────── Total objects being tracked
```

## 📚 Next Steps

### Enhance the Project

1. **Add object counting:**
   - Count objects crossing a line
   - Track total unique objects

2. **Add trajectory visualization:**
   - Draw paths of moving objects
   - Show movement history

3. **Filter specific objects:**
   - Track only cars, people, etc.
   - Ignore certain classes

4. **Add alerts:**
   - Notify when specific objects detected
   - Send notifications on events

### Learn More

- Study YOLOv4 architecture
- Explore OpenCV documentation
- Try other tracking algorithms (SORT, DeepSORT)
- Experiment with newer models (YOLOv5, YOLOv8)

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review `SETUP_INSTRUCTIONS.md`
3. Check the original README.md
4. Create an issue on GitHub
5. Contact the author

## 📝 Tips & Tricks

1. **Test with webcam first** - Easier than managing video files
2. **Start with default settings** - Optimize later if needed
3. **Monitor console output** - Helps understand what's happening
4. **Use absolute paths** - Avoids file not found errors
5. **Keep backup of original files** - Before modifying code

---

**Happy Tracking! 🎯**

---

**Author:** Suhas Uppala  
**GitHub:** [https://github.com/Suhas-Uppala](https://github.com/Suhas-Uppala)
