# 🎯 Trajectory Tracking Feature Guide

## New Feature: Visual Object Trajectory Tracking

Your object tracking system now draws colorful trajectory lines showing the path each tracked object has taken!

## 🌟 What's New

### Visual Trajectory Lines
- ✅ **Colored paths** - Each object gets a unique color for its trajectory
- ✅ **Historical tracking** - Shows last 30 positions (configurable)
- ✅ **Progressive thickness** - Lines get thicker as they approach current position
- ✅ **Point markers** - Small dots mark each recorded position
- ✅ **Clear trails** - Press 'C' to clear all trajectory history

## 🎮 Updated Controls

| Key | Function | Description |
|-----|----------|-------------|
| `ESC` | Exit | Close the application |
| `P` | Pause | Pause/Resume video playback |
| `S` | Screenshot | Save current frame with trajectories |
| `C` | Clear Trails | **NEW!** Clear all trajectory lines |

## 🎨 Visual Elements

### What You'll See:

1. **Green Boxes** - Object detection bounding boxes
2. **Colored Lines** - Trajectory paths (unique color per object)
3. **Small Colored Dots** - Historical position markers
4. **Large Red Dot** - Current object center position
5. **White Outline** - Circle around current position
6. **Labels** - ID, class name, and confidence score

### Color System:
- Each object ID gets a **unique, consistent color**
- Colors remain the same throughout the object's lifetime
- Different objects have different colored trails

## ⚙️ Configuration Options

### Adjust Trajectory Length

Open `object_tracking.py` and find this line (around line 37):

```python
MAX_TRAJECTORY_POINTS = 30  # Maximum points to keep in trajectory
```

**Adjust the value:**
- `10` - Short trails (fast-moving scenes)
- `30` - Medium trails (default, balanced)
- `50` - Long trails (detailed tracking)
- `100` - Very long trails (full path history)

**Note:** Higher values use more memory but show longer paths.

### Adjust Line Thickness

Find the trajectory drawing code (around line 140):

```python
thickness = max(1, int(2 * (i / len(trajectory))))
```

**Modify for different effects:**
- `thickness = 2` - Constant thickness (simple)
- `thickness = max(1, int(3 * (i / len(trajectory))))` - Thicker lines
- `thickness = 1` - Thin lines throughout

### Change Trajectory Colors

The current system generates colors based on object ID:

```python
color_seed = object_id * 50
trajectory_color = (
    (color_seed * 67) % 256,
    (color_seed * 137) % 256,
    (color_seed * 211) % 256
)
```

**Use fixed colors instead:**
```python
# Predefined color palette
colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Cyan
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Yellow
]
trajectory_color = colors[object_id % len(colors)]
```

## 📊 How It Works

### Trajectory Storage
```python
# Each object stores its last N positions
trajectory_history = {
    0: [(100, 200), (105, 205), (110, 210), ...],  # Object ID 0's path
    1: [(300, 400), (295, 395), (290, 390), ...],  # Object ID 1's path
    # ... more objects
}
```

### Update Process
1. Object is detected and tracked
2. Current position is added to trajectory list
3. If list exceeds MAX_TRAJECTORY_POINTS, oldest point is removed
4. Lines are drawn connecting all points in the list
5. When object is lost, its trajectory can remain (or be cleared)

## 🎯 Use Cases

### Traffic Analysis
- See vehicle movement patterns
- Identify common routes
- Analyze turning behavior

### Sports Analysis
- Track player movements
- Visualize running paths
- Study play patterns

### Surveillance
- Monitor person movement
- Detect unusual paths
- Track object flow

### Wildlife Tracking
- Follow animal movements
- Study migration patterns
- Analyze behavior

## 💡 Tips & Tricks

### 1. Clear Trails When Needed
Press `C` to clear trajectory history if:
- Screen becomes too cluttered
- Starting a new section of video
- Want to focus on current movements

### 2. Adjust Trail Length for Your Needs
- **Short videos**: Use longer trails (50-100 points)
- **Busy scenes**: Use shorter trails (10-20 points)
- **Fast motion**: Use medium trails (30-40 points)

### 3. Save Interesting Trajectories
Press `S` to save a screenshot showing:
- All current trajectories
- Object positions
- Tracking information

### 4. Performance Optimization
If experiencing slowdowns with many tracked objects:
- Reduce `MAX_TRAJECTORY_POINTS` to 15-20
- Use constant thickness (faster rendering)
- Skip drawing small trajectory dots

## 🔧 Advanced Customization

### Add Fading Effect (Older Trails Fade Out)

Replace the line drawing code with:

```python
# Draw lines with alpha blending for fade effect
for i in range(1, len(trajectory)):
    alpha = i / len(trajectory)  # 0 to 1
    # Blend with black for fade effect
    faded_color = tuple(int(c * alpha) for c in trajectory_color)
    thickness = max(1, int(2 * alpha))
    cv2.line(frame, trajectory[i-1], trajectory[i], faded_color, thickness)
```

### Draw Arrows Showing Direction

Add after trajectory lines:

```python
# Draw arrow at current position showing direction
if len(trajectory) >= 2:
    # Get last two points to determine direction
    start_point = trajectory[-2]
    end_point = trajectory[-1]
    cv2.arrowedLine(frame, start_point, end_point, trajectory_color, 2, tipLength=0.3)
```

### Display Speed/Velocity

Calculate and display object speed:

```python
# Calculate speed based on last two positions
if len(trajectory) >= 2:
    pt1, pt2 = trajectory[-2], trajectory[-1]
    distance = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
    speed = distance * fps  # pixels per second
    speed_text = f"Speed: {speed:.1f} px/s"
    cv2.putText(frame, speed_text, (pt[0], pt[1] + 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
```

## 📈 Performance Impact

### Memory Usage
- Each trajectory point: ~16 bytes (two integers)
- 30 points per object: ~480 bytes
- 50 tracked objects: ~24 KB (minimal)

### Processing Time
- Drawing trajectories adds ~1-3ms per frame
- Negligible impact on overall performance
- Main bottleneck remains object detection

## 🐛 Troubleshooting

### Issue: Trajectories Not Showing
**Check:**
- Objects are being detected and tracked
- `MAX_TRAJECTORY_POINTS` is not set to 0
- Trajectory colors are not same as background

### Issue: Lines Look Choppy
**Solution:**
- Increase detection frequency
- Reduce distance threshold for better tracking
- Use more trajectory points

### Issue: Too Many Lines, Cluttered Screen
**Solutions:**
- Press `C` to clear trails
- Reduce `MAX_TRAJECTORY_POINTS` to 10-15
- Increase confidence threshold to track fewer objects

### Issue: Trails Disappear Too Quickly
**Solution:**
- Increase `MAX_TRAJECTORY_POINTS` to 50 or more
- Make sure objects aren't losing tracking

## 📸 Example Output

```
┌─────────────────────────────────────────┐
│  Tracked Objects: 5 | Frame: 234       │
│                                         │
│    🟢 Car (Box)                        │
│    🔴 (Current position)               │
│    🔵━━━━ (Trajectory line)           │
│    · · · (Position markers)           │
│                                         │
│  ID:1 car 0.89                         │
│                                         │
└─────────────────────────────────────────┘
ESC:Exit | P:Pause | S:Screenshot | C:Clear
```

## 🎓 Learning From Trajectories

### Patterns You Can Observe:
1. **Straight lines** - Consistent direction/speed
2. **Curved paths** - Turning or circling
3. **Zigzag patterns** - Erratic movement
4. **Crossing lines** - Objects passing each other
5. **Parallel lines** - Objects moving together

### Analysis Possibilities:
- Count objects passing through an area
- Measure average path lengths
- Identify collision near-misses
- Study crowd flow patterns
- Detect anomalous behavior

## 🚀 Next Steps

Try these enhancements:
1. Add heatmap showing frequently traveled areas
2. Implement path prediction using trajectory data
3. Create zones and count entries/exits
4. Export trajectory data to CSV for analysis
5. Add trajectory smoothing for cleaner lines

---

**Enjoy tracking with visual trajectories! 🎯**

For questions or issues, refer to:
- `USAGE_GUIDE.md` - Complete usage manual
- `QUICK_REFERENCE.txt` - Quick command reference
- `README.md` - Project overview

---

**Author:** Suhas Uppala  
**GitHub:** [https://github.com/Suhas-Uppala](https://github.com/Suhas-Uppala)
