# Object Detection and Tracking Setup Instructions

## Quick Start Guide

### Step 1: Install Required Dependencies

```powershell
pip install opencv-python opencv-contrib-python numpy
```

### Step 2: Download YOLOv4 Model Files

**Option A: Automatic Download (Recommended)**
```powershell
python download_models.py
```

**Option B: Manual Download**

Download these files and place them in the `dnn_model` folder:

1. **YOLOv4 Weights** (~245 MB)
   - URL: https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
   - Save as: `dnn_model/yolov4.weights`

2. **YOLOv4 Config** (~12 KB)
   - URL: https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
   - Save as: `dnn_model/yolov4.cfg`

3. **COCO Classes** (~1 KB)
   - URL: https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names
   - Save as: `dnn_model/classes.txt`

### Step 3: Prepare Video Source

**Option A: Use a Video File**
- Place your video file (e.g., `los_angeles.mp4`) in the project root directory
- The code is already configured to use this file

**Option B: Use Webcam**
- Open `object_tracking.py`
- Change line: `VIDEO_SOURCE = "los_angeles.mp4"` to `VIDEO_SOURCE = 0`

### Step 4: Run the Application

```powershell
python object_tracking.py
```

## Features

### Object Detection
- Detects 80 different object classes (COCO dataset)
- Shows confidence scores for each detection
- Real-time bounding box visualization

### Object Tracking
- Assigns unique IDs to detected objects
- Tracks objects across frames
- Maintains object identity even with temporary occlusions

### Controls
- **ESC** - Exit the application
- **P** - Pause/Resume playback
- **S** - Save screenshot of current frame

## Expected Output

The application will display:
- Green bounding boxes around detected objects
- Red dots at object centers
- Object ID, class name, and confidence score
- Total count of tracked objects
- Current frame number

## Troubleshooting

### Error: "Could not open video source"
**Solution**: 
- Verify video file exists in the project directory
- Try using webcam instead: `VIDEO_SOURCE = 0`
- Check video file format (MP4, AVI, etc.)

### Error: "Failed to open NetParameter file"
**Solution**: 
- Run `python download_models.py` to download model files
- Verify all three files exist in `dnn_model/` folder

### CUDA Errors
**Solution**: 
- The code automatically falls back to CPU if CUDA is unavailable
- CPU processing is slower but will work on any system

### Slow Performance
**Solutions**:
- Reduce video resolution
- Lower `confThreshold` in `object_detection.py` (default: 0.5)
- Increase `image_size` in `object_detection.py` for faster processing
- Use GPU if available (requires OpenCV built with CUDA)

## File Structure

```
object-tracking-opencv/
├── object_tracking.py          # Main tracking script
├── object_detection.py         # YOLOv4 detection wrapper
├── download_models.py          # Model downloader utility
├── SETUP_INSTRUCTIONS.md       # This file
├── README.md                   # Project overview
├── los_angeles.mp4            # Video file (optional)
└── dnn_model/
    ├── yolov4.weights         # YOLOv4 model weights
    ├── yolov4.cfg             # YOLOv4 configuration
    └── classes.txt            # COCO class names
```

## Detected Object Classes

The model can detect 80 different objects including:
- People, vehicles (car, truck, bus, motorcycle, bicycle)
- Animals (dog, cat, horse, bird, etc.)
- Sports equipment (ball, bat, glove, etc.)
- Household items (chair, table, TV, laptop, etc.)
- And many more!

## Performance Tips

1. **Use GPU acceleration**: Install OpenCV with CUDA support for 10-30x faster processing
2. **Adjust detection threshold**: Lower `confThreshold` (0.3-0.4) for more detections
3. **Optimize tracking distance**: Modify distance threshold in tracking algorithm (currently 50 pixels)
4. **Process every Nth frame**: Skip frames for faster processing on slow systems

## Credits

- Author: Suhas Uppala
- GitHub: [Suhas-Uppala](https://github.com/Suhas-Uppala)
- YOLOv4: Alexey Bochkovskiy
- OpenCV: Open Source Computer Vision Library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Educational Purpose Only - Open Source Project
