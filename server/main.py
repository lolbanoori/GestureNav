import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import socket
import json
import math
import time
import os

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5555
DEADZONE = 0.1
MODEL_PATH = 'hand_landmarker.task'

def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def main():
    print(f"Starting GestureNav Vision Engine (Tasks API) on {UDP_IP}:{UDP_PORT}")

    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file {MODEL_PATH} not found. Please download it.")
        return

    # Initialize UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Initialize Hand Landmarker
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5)
    detector = vision.HandLandmarker.create_from_options(options)

    # Note: Drawing utils might still be in mp.solutions.drawing_utils? 
    # If solutions is missing, we might have to draw manually or use mp.tasks visualization tools?
    # Actually, mp.solutions might NOT be available at all. 
    # I will write a simple manual drawer to be safe.
    
    cap = cv2.VideoCapture(0)
    
    start_time = time.time()

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Create MP Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            
            # Detect
            timestamp_ms = int((time.time() - start_time) * 1000)
            detection_result = detector.detect(mp_image) # Using image mode for simplicity (or detect_for_video)
            # For video mode: detector.detect_for_video(mp_image, timestamp_ms)
            # Let's use detect() (Image mode) first as it doesn't require strict monotonic timestamps, simpler for debugging.
            
            orbit_x = 0.0
            orbit_y = 0.0
            zoom_dist = 0.0
            state = "idle"

            # Parse Results
            if detection_result.hand_landmarks:
                state = "active"
                hand_landmarks = detection_result.hand_landmarks[0] # List of NormalizedLandmark

                # 1. ORBIT (Wrist: 0)
                wrist = hand_landmarks[0]
                raw_x = wrist.x - 0.5
                raw_y = wrist.y - 0.5
                
                if abs(raw_x) > DEADZONE:
                    orbit_x = raw_x
                if abs(raw_y) > DEADZONE:
                    orbit_y = raw_y

                # 2. ZOOM (Thumb 4, Index 8)
                thumb = hand_landmarks[4]
                index = hand_landmarks[8]
                zoom_dist = calculate_distance(thumb, index)
                
                # Manual Drawing (since mp.solutions.drawing_utils is broken)
                h, w, _ = image.shape
                # Draw connections (subset for visuals)
                # Wrist to Index
                cv2.line(image, (int(wrist.x*w), int(wrist.y*h)), (int(index.x*w), int(index.y*h)), (0, 255, 255), 2)
                # Wrist to Thumb
                cv2.line(image, (int(wrist.x*w), int(wrist.y*h)), (int(thumb.x*w), int(thumb.y*h)), (0, 255, 255), 2)
                
                for lm in hand_landmarks:
                    cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 4, (0, 0, 255), -1)

            # Visualization
            h, w, _ = image.shape
            cv2.circle(image, (w//2, h//2), int(w * DEADZONE), (0, 255, 0), 1)
            
            cv2.putText(image, f"Orbit: {orbit_x:.2f}, {orbit_y:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f"Zoom: {zoom_dist:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('GestureNav Vision (Tasks)', image)

            # UDP Send
            payload = {
                'state': state,
                'orbit_x': orbit_x,
                'orbit_y': orbit_y,
                'zoom_dist': zoom_dist
            }
            
            sock.sendto(json.dumps(payload).encode('utf-8'), (UDP_IP, UDP_PORT))
            
            if cv2.waitKey(5) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        sock.close()

if __name__ == "__main__":
    main()
