<div align="justify" markdown="1">

# 🎯 Object Tracking and Detection with Trajectory Visualization

**Author:** Suhas Uppala  
**GitHub:** [https://github.com/Suhas-Uppala](https://github.com/Suhas-Uppala)  
**License:** [MIT License](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful real-time object detection and tracking system using YOLOv4 and OpenCV. Features visual trajectory lines that show the complete path of tracked objects with unique colored trails.

---

## ✨ Features

- 🎯 **Real-time Object Detection** - Detects 80 different classes using YOLOv4
- 🔄 **Multi-Object Tracking** - Tracks multiple objects with unique IDs
- 🌈 **Trajectory Visualization** - Colored trails showing object movement paths
- 📊 **Confidence Scores** - Displays class names and detection confidence
- ⚡ **GPU Acceleration** - CUDA support for faster processing (optional)
- 🎮 **Interactive Controls** - Pause, screenshot, and clear trajectory trails
- 📹 **Multiple Video Sources** - Works with video files, webcam, and RTSP streams

---

## 📚 Complete Documentation

This project includes comprehensive documentation to guide you through every aspect:

### 🚀 Getting Started

| Document | Purpose | Read When |
|----------|---------|-----------|
| **[SETUP_INSTRUCTIONS.md](object-tracking-opencv/SETUP_INSTRUCTIONS.md)** | Complete installation and setup guide with troubleshooting | Setting up the project for the first time |
| **[USAGE_GUIDE.md](object-tracking-opencv/USAGE_GUIDE.md)** | Detailed usage manual covering all features and configurations | Learning how to use and customize the system |
| **[QUICK_REFERENCE.txt](object-tracking-opencv/QUICK_REFERENCE.txt)** | Quick command reference and keyboard shortcuts | Need a fast lookup during usage |

### 🎨 Trajectory Feature

| Document | Purpose | Read When |
|----------|---------|-----------|
| **[TRAJECTORY_GUIDE.md](object-tracking-opencv/TRAJECTORY_GUIDE.md)** | In-depth guide to trajectory visualization and customization | Want to understand or modify trajectory trails |
| **[TRAJECTORY_VISUAL_EXAMPLE.txt](object-tracking-opencv/TRAJECTORY_VISUAL_EXAMPLE.txt)** | ASCII art examples showing different tracking patterns | Visual reference for trajectory patterns |

### 📖 Project Information

| Document | Purpose | Read When |
|----------|---------|-----------|
| **[PROJECT_SUMMARY.md](object-tracking-opencv/PROJECT_SUMMARY.md)** | Overview of features, implementation details, and use cases | Understanding what the project offers |
| **[CHANGELOG.md](object-tracking-opencv/CHANGELOG.md)** | Complete version history and enhancement details | Tracking project evolution and updates |

### 🎯 Which Document Should I Start With?

- **👋 New User?** → Start with `SETUP_INSTRUCTIONS.md`
- **🎮 Ready to Use?** → Jump to `USAGE_GUIDE.md`
- **🌈 Want Trajectory Details?** → Read `TRAJECTORY_GUIDE.md`
- **⚡ Quick Help?** → Check `QUICK_REFERENCE.txt`
- **🔍 Project Overview?** → See `PROJECT_SUMMARY.md`

---

## 🚀 Quick Start

### Installation

```bash
# Install required packages
pip install opencv-python numpy

# Download YOLOv4 model files
python download_models.py

# Verify setup
python test_setup.py

# Run with video file
python object_tracking.py

# OR run with live camera
python live_camera_tracking.py
```

### Interactive Launcher

```powershell
.\run.ps1  # Windows PowerShell
```

Or use the menu-driven batch file:
```cmd
run.bat  # Windows Command Prompt
```

---

## 🎮 Keyboard Controls

| Key | Function | Description |
|-----|----------|-------------|
| **ESC** | Exit | Close the application |
| **P** | Pause | Pause/Resume video playback |
| **S** | Screenshot | Save current frame with trajectories |
| **C** | Clear Trails | Clear all trajectory history |

---

<div align="center" markdown="1">

## Object detection

For convenience, I have already written this part and you find everything in the object_detection.py file. To use it just a call in the main file

```python
...
from object_detection import ObjectDetection
...

# Initialize Object Detection
od = ObjectDetection()

while True:
...
    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy))
...
```

Here is the result in the video frame.

<a href="https://ibb.co/5xcsHJW"><img src="https://i.ibb.co/7Nyrm0J/object-tracking-from-scratch-opencv-and-python-object-detection-with-yolo-768x648.png" alt="object-tracking-from-scratch-opencv-and-python-object-detection-with-yolo-768x648" border="0"></a>

## Object Tracking
By saving the position of the center point of each object, you can trace the previous position of the objects and predict what the immediate next will be. Here is a small example in the image

<a href="https://ibb.co/fMYj0MV"><img src="https://i.ibb.co/kKgNcKV/object-tracking-from-scratch-opencv-and-python-point-tracking.png" alt="object-tracking-from-scratch-opencv-and-python-point-tracking" border="0"></a>

Before going on with the explanation, I must point out that object tracking is more complicated than that. Consider this tutorial as a simple exercise to understand the basics behind this algorithm. 

### Find the point and assign the ID

We don’t need the history of all the tracking but only the last points so Initialize an array to keep track of the previous points and then we need to calculate the distance between the points to make sure they all belong to the same object. The closer the points are, the greater the probability that we are tracking the same object.

```python

...
# Initialize count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0
...

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
...
```

As you can see from the portion of code above with the math.hypot() function the distance of the two points is calculated and if the distance is less than 20, an ID is associated with the position of the point.

<a href="https://ibb.co/z5KpXD3"><img src="https://i.ibb.co/YWvmcw5/object-tracking-from-scratch-opencv-and-python-assign-ID-1024x795.png" alt="object-tracking-from-scratch-opencv-and-python-assign-ID-1024x795" border="0"></a>

### Assign univocal ID

In this part of the code, we have to make sure to compare the previous object with the current one and update the position of the ID. In this way, the same object remains with the same ID for its entire path. When the object is no longer recognized, it loses the ID.

```python
...

    else:

        tracking_objects_copy = tracking_objects.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)
...
```

Now the tracking works quite well and as you can see from the image below, the white car has lost track because the object has not been identified anymore.

<a href="https://ibb.co/wrqyRHh"><img src="https://i.ibb.co/mFKJGs5/object-tracking-from-scratch-opencv-and-python-lost-ID-1024x601.png" alt="object-tracking-from-scratch-opencv-and-python-lost-ID-1024x601" border="0"></a>

### Add new ID to new cars

If a new object is identified, the list of points must also be updated. So here are the changes of the previous code that allow you to delete the old and add the points of the new cars identified.

```python
...

    else:
        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1
...
```

As can be seen from the image below, the id is kept until the object is recognized. In fact, in the central part of the video, it traces very well.

<a href="https://ibb.co/Fn39gbb"><img src="https://i.ibb.co/mSTm6CC/image.png" alt="image" border="0"></a>

### Trajectory Visualization

The enhanced version includes colorful trajectory trails:

```python
# Each object maintains a history of positions
trajectory_history = {
    0: [(100, 200), (105, 205), (110, 210), ...],  # Object 0's path
    1: [(300, 400), (295, 395), (290, 390), ...],  # Object 1's path
}

# Draw colored lines connecting historical positions
for object_id, trajectory in trajectory_history.items():
    # Each object gets a unique color
    trajectory_color = generate_color(object_id)
    # Draw lines connecting points
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i-1], trajectory[i], trajectory_color, 2)
```

This creates visual trails showing where each object has been, making it easy to analyze movement patterns.

For complete trajectory documentation, see [TRAJECTORY_GUIDE.md](object-tracking-opencv/TRAJECTORY_GUIDE.md).

---

## 🎯 Use Cases

- **🚗 Traffic Analysis** - Monitor vehicle flow and detect patterns
- **👥 Crowd Monitoring** - Track people movement in public spaces
- **🏃 Sports Analytics** - Analyze player movements and strategies
- **🐾 Wildlife Tracking** - Study animal behavior and migration
- **🏭 Industrial Safety** - Monitor restricted areas and equipment
- **🛒 Retail Analytics** - Understand customer movement patterns

---

## 🔧 Troubleshooting

### Common Issues

**Problem:** "Could not open video source"
- **Solution:** Verify video file exists or use webcam: `VIDEO_SOURCE = 0`

**Problem:** "Failed to open NetParameter file"
- **Solution:** Run `python download_models.py` to get model files

**Problem:** Slow performance
- **Solution:** Reduce `image_size` in `object_detection.py` to 320 or 416

**Problem:** Objects not detected
- **Solution:** Lower `confThreshold` to 0.3 in `object_detection.py`

For comprehensive troubleshooting, see [USAGE_GUIDE.md](object-tracking-opencv/USAGE_GUIDE.md#troubleshooting).

---

## 🤝 Contribute

If you encounter any bugs or have ideas for enhancements:

1. 🐛 **Report Issues** - Create an issue ticket on GitHub
2. 💡 **Suggest Features** - Share your ideas for improvements
3. 🔧 **Submit Pull Requests** - Contribute code improvements
4. 📚 **Improve Documentation** - Help make docs clearer

Your feedback and contributions help make this project better! 😊

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software with attribution.

---

## 🙏 Acknowledgments

- **YOLOv4** - Alexey Bochkovskiy for the YOLOv4 model
- **OpenCV** - Open Source Computer Vision Library
- **COCO Dataset** - For the 80 object classes

---

## 📞 Support

- **📖 Documentation** - Check the docs folder for detailed guides
- **🐛 Issues** - Report bugs on GitHub Issues
- **💬 Discussions** - Ask questions in GitHub Discussions
- **⭐ Star** - If you find this useful, give it a star!

---

<div align="center">

**Made with ❤️ by Suhas Uppala**

[GitHub](https://github.com/Suhas-Uppala) • [Report Bug](https://github.com/Suhas-Uppala/Object-detection-and-tracking/issues) • [Request Feature](https://github.com/Suhas-Uppala/Object-detection-and-tracking/issues)

</div>

---

## 📂 Project Structure

```
object-tracking-opencv/
├── 🎯 Core Application
│   ├── object_tracking.py       # Main tracking system (video files)
│   ├── live_camera_tracking.py  # Live camera tracking (NEW!)
│   ├── object_detection.py      # YOLOv4 detection wrapper
│   └── dnn_model/              # YOLOv4 model files
│       ├── yolov4.weights      # Model weights (download required)
│       ├── yolov4.cfg          # Configuration
│       └── classes.txt         # 80 COCO class names
│
├── 🛠️ Utilities
│   ├── download_models.py      # Auto-download model files
│   ├── test_setup.py          # Verify installation
│   ├── run.ps1                # PowerShell launcher
│   └── run.bat                # Batch file launcher
│
├── 📚 Documentation
│   ├── SETUP_INSTRUCTIONS.md   # Installation guide
│   ├── USAGE_GUIDE.md         # Complete usage manual
│   ├── TRAJECTORY_GUIDE.md    # Trajectory feature docs
│   ├── QUICK_REFERENCE.txt    # Quick command reference
│   ├── PROJECT_SUMMARY.md     # Project overview
│   ├── CHANGELOG.md           # Version history
│   └── TRAJECTORY_VISUAL_EXAMPLE.txt  # Visual examples
│
└── 📄 Project Files
    ├── LICENSE                # MIT License
    ├── .gitignore            # Git ignore rules
    └── README.md             # This file
```

---

## 🎯 What You'll See

When running the application, the display shows:

- **🟢 Green Boxes** - Object detection bounding boxes
- **🌈 Colored Lines** - Trajectory paths (unique color per object)
- **🔴 Red Dots** - Current object center positions
- **📝 Labels** - Object ID, class name, and confidence score
- **📊 Statistics** - Tracked object count and frame number

---

## ⚙️ Configuration

### Adjust Trajectory Length
```python
# In object_tracking.py (line ~37)
MAX_TRAJECTORY_POINTS = 30  # Default
# Change to 10 (short), 50 (long), or 100 (very long)
```

### Adjust Detection Sensitivity
```python
# In object_detection.py (line ~14)
self.confThreshold = 0.5  # Default
# Lower (0.3) = more detections
# Higher (0.7) = fewer, more confident detections
```

### Change Video Source
```python
# In object_tracking.py (line ~15)
VIDEO_SOURCE = "los_angeles.mp4"  # Video file
# Or
VIDEO_SOURCE = 0  # Webcam
# Or
VIDEO_SOURCE = "rtsp://camera_url"  # IP camera
```

For detailed configuration options, see [USAGE_GUIDE.md](object-tracking-opencv/USAGE_GUIDE.md).

---

## 🎓 How It Works

### Object Detection (YOLOv4)
