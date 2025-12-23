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
            zoom_val = 0
            state = "idle"

            # Parse Results
            if detection_result.hand_landmarks:
                state = "active"
                hand_landmarks = detection_result.hand_landmarks[0] # List of NormalizedLandmark

                # 1. ORBIT (Joystick Logic)
                wrist = hand_landmarks[0]
                
                # Offset Center (Move Deadzone to Right-Bottom side to clear view)
                CENTER_X = 0.75
                CENTER_Y = 0.6
                
                raw_x = wrist.x - CENTER_X
                raw_y = wrist.y - CENTER_Y
                
                # Vector Magnitude
                magnitude = math.sqrt(raw_x**2 + raw_y**2)
                
                # Joystick Math
                DEADZONE_THRESH = 0.15
                SENSITIVITY = 5.0
                
                if magnitude > DEADZONE_THRESH:
                    # Normalize direction
                    dir_x = raw_x / magnitude
                    dir_y = raw_y / magnitude
                    
                    # Ramp up from 0
                    strength = (magnitude - DEADZONE_THRESH) * SENSITIVITY
                    
                    orbit_x = dir_x * strength
                    orbit_y = dir_y * strength
                else:
                    orbit_x = 0.0
                    orbit_y = 0.0

                # 2. ZOOM (Discrete Trigger Logic)
                thumb = hand_landmarks[4]
                index = hand_landmarks[8]
                dist = calculate_distance(thumb, index)
                
                # Widened Sweet Spot
                PINCH_IN_THRESH = 0.04
                PINCH_OUT_THRESH = 0.12
                
                if dist < PINCH_IN_THRESH:
                    zoom_val = 1  # Zoom In
                    cv2.putText(image, "ZOOM IN", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif dist > PINCH_OUT_THRESH:
                    zoom_val = -1 # Zoom Out
                    cv2.putText(image, "ZOOM OUT", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                else:
                    zoom_val = 0  # Idle

                # Visualization Vectors
                # Wrist to Index
                h, w, _ = image.shape
                cv2.line(image, (int(wrist.x*w), int(wrist.y*h)), (int(index.x*w), int(index.y*h)), (0, 255, 255), 2)
                
                for lm in hand_landmarks:
                    cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 4, (0, 0, 255), -1)

            # Visualization
            h, w, _ = image.shape
            # Draw Deadzone
            # Convert CENTER_X/Y to pixels
            cx, cy = int(w * 0.75), int(h * 0.6)
            cv2.circle(image, (cx, cy), int(w * 0.15), (0, 255, 0), 1)
            
            cv2.putText(image, f"Joy: {orbit_x:.2f}, {orbit_y:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('GestureNav Vision (Tasks)', image)

            # UDP Send
            payload = {
                'state': state,
                'x': orbit_x,
                'y': orbit_y,
                'zoom': zoom_val
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
