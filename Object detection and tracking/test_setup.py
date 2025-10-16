"""
Quick Test Script for Object Detection and Tracking
Run this to verify your setup is working correctly
"""

import sys
import os

def test_imports():
    """Test if required libraries are installed"""
    print("=" * 60)
    print("Testing Python Package Imports...")
    print("=" * 60)
    
    try:
        import cv2
        print(f"✓ OpenCV installed: version {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy installed: version {np.__version__}")
    except ImportError:
        print("✗ NumPy not found. Install with: pip install numpy")
        return False
    
    return True

def test_model_files():
    """Test if YOLOv4 model files exist"""
    print("\n" + "=" * 60)
    print("Checking Model Files...")
    print("=" * 60)
    
    model_dir = "dnn_model"
    files_to_check = {
        'yolov4.weights': 245_000_000,  # ~245 MB
        'yolov4.cfg': 10_000,           # ~10 KB
        'classes.txt': 500              # ~500 bytes
    }
    
    all_exist = True
    
    for filename, min_size in files_to_check.items():
        filepath = os.path.join(model_dir, filename)
        
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            
            if size > min_size:
                print(f"✓ {filename} found ({size_mb:.1f} MB)")
            else:
                print(f"⚠ {filename} found but seems too small ({size_mb:.1f} MB)")
                print(f"  Expected at least {min_size / (1024*1024):.1f} MB")
                all_exist = False
        else:
            print(f"✗ {filename} not found")
            print(f"  Should be in: {filepath}")
            all_exist = False
    
    return all_exist

def test_object_detection():
    """Test if ObjectDetection class works"""
    print("\n" + "=" * 60)
    print("Testing Object Detection Class...")
    print("=" * 60)
    
    try:
        from object_detection import ObjectDetection
        print("✓ ObjectDetection class imported successfully")
        
        # Try to initialize
        od = ObjectDetection()
        print("✓ ObjectDetection initialized successfully")
        print(f"✓ Loaded {len(od.classes)} object classes")
        
        # Show first 10 classes
        print("\nFirst 10 detectable classes:")
        for i, class_name in enumerate(od.classes[:10], 1):
            print(f"  {i}. {class_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing ObjectDetection: {e}")
        return False

def test_video_source():
    """Test if video source is available"""
    print("\n" + "=" * 60)
    print("Testing Video Sources...")
    print("=" * 60)
    
    import cv2
    
    # Check for video file
    video_file = "los_angeles.mp4"
    if os.path.exists(video_file):
        print(f"✓ Video file found: {video_file}")
        cap = cv2.VideoCapture(video_file)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"  Resolution: {width}x{height}")
            print(f"  FPS: {fps}")
            print(f"  Total frames: {frame_count}")
            cap.release()
        else:
            print(f"⚠ Video file exists but cannot be opened")
    else:
        print(f"⚠ Video file not found: {video_file}")
        print("  You can either:")
        print("  1. Add a video file named 'los_angeles.mp4'")
        print("  2. Use webcam instead (set VIDEO_SOURCE = 0)")
    
    # Check for webcam
    print("\nChecking webcam...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✓ Webcam is available")
        ret, frame = cap.read()
        if ret:
            height, width = frame.shape[:2]
            print(f"  Webcam resolution: {width}x{height}")
        cap.release()
    else:
        print("✗ Webcam not available")
    
    return True

def test_cuda_support():
    """Test if CUDA is available"""
    print("\n" + "=" * 60)
    print("Testing CUDA GPU Support...")
    print("=" * 60)
    
    try:
        import cv2
        
        # Check if CUDA is available
        cuda_count = cv2.cuda.getCudaEnabledDeviceCount()
        
        if cuda_count > 0:
            print(f"✓ CUDA is available! {cuda_count} GPU(s) detected")
            print("  Your application will use GPU acceleration")
        else:
            print("⚠ CUDA not available")
            print("  Your application will use CPU (slower but works)")
            
    except:
        print("⚠ CUDA support not compiled in OpenCV")
        print("  Your application will use CPU (slower but works)")
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "OBJECT TRACKING SETUP VERIFICATION" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Model Files", test_model_files()))
    results.append(("Object Detection", test_object_detection()))
    results.append(("Video Sources", test_video_source()))
    results.append(("CUDA Support", test_cuda_support()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    # Overall result
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou're ready to run the application:")
        print("  python object_tracking.py")
    else:
        print("⚠ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the application.")
        print("\nCommon fixes:")
        print("  • Install packages: pip install opencv-python numpy")
        print("  • Download models: python download_models.py")
        print("  • Add video file or use webcam (VIDEO_SOURCE = 0)")
    
    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
