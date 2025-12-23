import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import socket
import json
import math
import time
import os

# State and Config
UDP_IP = "127.0.0.1"
UDP_PORT = 5555
MODEL_PATH = 'hand_landmarker.task'

config = {
    'deadzone_radius': 0.12,
    'deadzone_offset_x': 0.75,
    'deadzone_offset_y': 0.6,
    'zoom_thresh_in': 0.05,
    'zoom_thresh_out': 0.15,
    'orbit_sens_server': 3.0,
    'use_fist_safety': True,
    'use_open_hand_safety': False
}

def config_listener():
    """Listens for configuration updates from Blender on Port 5556."""
    UDP_PORT_CONFIG = 5556
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT_CONFIG))
        sock.setblocking(False)
        print(f"Config Listener started on port {UDP_PORT_CONFIG}")
    except Exception as e:
        print(f"Config Listener Error: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            new_config = json.loads(data.decode('utf-8'))
            
            # Update global config safely
            for key, value in new_config.items():
                if key in config:
                    config[key] = value
            
            
        except BlockingIOError:
            time.sleep(0.1)
        except Exception as e:
            print(f"Config Parse Error: {e}")

import threading

def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def main():
    print(f"Starting GestureNav Vision Engine (Tasks API) on {UDP_IP}:{UDP_PORT}")

    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file {MODEL_PATH} not found. Please download it.")
        return

    # Start Config Thread
    cfg_thread = threading.Thread(target=config_listener, daemon=True)
    cfg_thread.start()

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

    cap = cv2.VideoCapture(0)
    
    start_time = time.time()

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            
            timestamp_ms = int((time.time() - start_time) * 1000)
            detection_result = detector.detect(mp_image)
            
            orbit_x = 0.0
            orbit_y = 0.0
            zoom_val = 0
            state = "idle"

            # Parse Results
            if detection_result.hand_landmarks:
                state = "active"
                hand_landmarks = detection_result.hand_landmarks[0]

                # 1. ORBIT (Joystick Logic)
                wrist = hand_landmarks[0]
                
                # Dynamic Deadzone Position
                cx = config['deadzone_offset_x']
                cy = config['deadzone_offset_y']
                
                raw_x = wrist.x - cx
                raw_y = wrist.y - cy
                
                # Vector Magnitude
                magnitude = math.sqrt(raw_x**2 + raw_y**2)
                
                # Dynamic Thresholds
                DEADZONE_THRESH = config['deadzone_radius']
                SENSITIVITY = config['orbit_sens_server']
                MAX_SPEED = 0.5 
                
                # OPEN HAND SAFETY
                # If palm is open/flat and safety enabled, disable orbit.
                # Heuristic: Check fingers extended.
                # Average distance of Middle(12), Ring(16), Pinky(20) from Wrist(0).
                # If large (>0.35 approx), handle is "Open".
                tips = [12, 16, 20]
                avg_tip_dist = sum([calculate_distance(hand_landmarks[i], wrist) for i in tips]) / 3.0
                IS_OPEN = avg_tip_dist > 0.35
                IS_FIST = avg_tip_dist < 0.25
                
                ORBIT_ALLOWED = True
                if config['use_open_hand_safety'] and IS_OPEN:
                    ORBIT_ALLOWED = False
                    cv2.putText(image, "OPEN HAND (ORBIT LOCKED)", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                
                if magnitude > DEADZONE_THRESH and ORBIT_ALLOWED:
                    dir_x = raw_x / magnitude
                    dir_y = raw_y / magnitude
                    
                    raw_strength = (magnitude - DEADZONE_THRESH) * SENSITIVITY
                    strength = min(raw_strength, MAX_SPEED)
                    
                    orbit_x = dir_x * strength
                    orbit_y = dir_y * strength
                else:
                    orbit_x = 0.0
                    orbit_y = 0.0

                # 2. ZOOM
                thumb = hand_landmarks[4]
                index = hand_landmarks[8]
                
                ZOOM_ALLOWED = True
                if config['use_fist_safety'] and IS_FIST:
                     ZOOM_ALLOWED = False
                     cv2.putText(image, "FIST (ZOOM LOCKED)", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                if ZOOM_ALLOWED:
                    dist = calculate_distance(thumb, index)
                    
                    PINCH_IN = config['zoom_thresh_in']
                    PINCH_OUT = config['zoom_thresh_out']
                    
                    if dist < PINCH_IN:
                        zoom_val = 1
                        cv2.putText(image, "ZOOM IN", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    elif dist > PINCH_OUT:
                        zoom_val = -1
                        cv2.putText(image, "ZOOM OUT", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    else:
                        zoom_val = 0

                # Visualization Vectors
                h, w, _ = image.shape
                cv2.line(image, (int(wrist.x*w), int(wrist.y*h)), (int(index.x*w), int(index.y*h)), (0, 255, 255), 2)
                
                for lm in hand_landmarks:
                    cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 4, (0, 0, 255), -1)

            # Visualization
            h, w, _ = image.shape
            
            # Dynamic Deadzone Visual
            dcx, dcy = int(w * config['deadzone_offset_x']), int(h * config['deadzone_offset_y'])
            dr = int(w * config['deadzone_radius'])
            cv2.circle(image, (dcx, dcy), dr, (0, 255, 0), 1)
            
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
