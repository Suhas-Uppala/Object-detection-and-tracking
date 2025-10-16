"""
Download YOLOv4 model files for object detection
Run this script to automatically download the required model files
"""

import os
import urllib.request
import sys

def download_file(url, destination):
    """Download file with progress indicator"""
    print(f"\nDownloading: {os.path.basename(destination)}")
    print(f"From: {url}")
    
    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\rProgress: {percent}% ")
        sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, destination, reporthook)
        print("\n✓ Download complete!")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading: {e}")
        return False

def main():
    # Create dnn_model directory if it doesn't exist
    model_dir = "dnn_model"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"Created directory: {model_dir}")
    
    files_to_download = [
        {
            'url': 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights',
            'path': os.path.join(model_dir, 'yolov4.weights'),
            'size': '245 MB'
        },
        {
            'url': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg',
            'path': os.path.join(model_dir, 'yolov4.cfg'),
            'size': '12 KB'
        },
        {
            'url': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names',
            'path': os.path.join(model_dir, 'classes.txt'),
            'size': '1 KB'
        }
    ]
    
    print("=" * 60)
    print("YOLOv4 Model Downloader")
    print("=" * 60)
    
    for file_info in files_to_download:
        file_path = file_info['path']
        
        # Check if file already exists
        if os.path.exists(file_path):
            print(f"\n✓ {os.path.basename(file_path)} already exists (skipping)")
            continue
        
        print(f"\nFile: {os.path.basename(file_path)} ({file_info['size']})")
        success = download_file(file_info['url'], file_path)
        
        if not success:
            print(f"\n✗ Failed to download {os.path.basename(file_path)}")
            print("Please try downloading manually or check your internet connection")
            return False
    
    print("\n" + "=" * 60)
    print("✓ All model files downloaded successfully!")
    print("=" * 60)
    print("\nYou can now run: python object_tracking.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
