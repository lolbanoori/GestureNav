import urllib.request
import os

url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
filename = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

print(f"Downloading {filename}...")
try:
    urllib.request.urlretrieve(url, filename)
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print("Download successful.")
    else:
        print("Download failed (empty file).")
except Exception as e:
    print(f"Error: {e}")
