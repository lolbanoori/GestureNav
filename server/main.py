import cv2
import time
import socket
import json
import threading

from server.config import settings
from server.vision.hand_tracking import HandTracker
from server.networking.udp_server import GestureSender
from server.vision.gesture_analysis import GestureDecider

# Global State for graceful shutdown
stop_server = False

def config_listener(decider: GestureDecider):
    """Listens for configuration updates from Blender on Port 5556."""
    UDP_PORT_CONFIG = settings.CONFIG_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((settings.DEFAULT_IP, UDP_PORT_CONFIG))
        sock.setblocking(False)
        print(f"Config Listener started on port {UDP_PORT_CONFIG}")
    except Exception as e:
        print(f"Config Listener Error: {e}")
        return

    while not stop_server:
        try:
            data, addr = sock.recvfrom(1024)
            new_config = json.loads(data.decode('utf-8'))
            
            # Update decider config safely
            decider.update_config(new_config)
            
        except BlockingIOError:
            time.sleep(0.1)
        except Exception as e:
            print(f"Config Parse Error: {e}")
            
    sock.close()

def main():
    global stop_server
    print(f"Starting GestureNav Server (v1.8.0) on {settings.DEFAULT_IP}:{settings.DEFAULT_PORT}")

    # 1. Initialize Components
    tracker = HandTracker()
    sender = GestureSender()
    decider = GestureDecider()

    # 2. Start Config Thread
    cfg_thread = threading.Thread(target=config_listener, args=(decider,), daemon=True)
    cfg_thread.start()

    # 3. Setup Webcam
    cap = cv2.VideoCapture(0)
    
    # Setup Window
    window_name = 'GestureNav Vision (Tasks)'
    cv2.namedWindow(window_name)
    
    # Initial Wait to allow camera to warm up
    time.sleep(1.0)
    
    start_time = time.time()

    try:
        while cap.isOpened():
            # Check for Window Close (X button)
            try:
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    stop_server = True
            except:
                pass 

            if stop_server:
                break

            success, raw_image = cap.read()
            if not success:
                continue

            # 4. Process Frame
            # process_frame returns the image that was processed (flipped) and the result
            processed_image, detection_result = tracker.process_frame(raw_image)
            
            # 5. Determine Gesture
            hand_landmarks = detection_result.hand_landmarks[0] if detection_result and detection_result.hand_landmarks else None
            gesture_data = decider.analyze(hand_landmarks)
            
            # 6. Send Data
            sender.send_gesture(
                state=gesture_data['state'],
                x=gesture_data['orbit_x'],
                y=gesture_data['orbit_y'],
                zoom=gesture_data['zoom_val']
            )

            # 7. Visualization
            # Draw Landmarks
            tracker.draw_landmarks(processed_image, detection_result)
            
            # Draw UI Overlays (Text, Deadzone) from logic
            h, w, _ = processed_image.shape
            
            # Deadzone Visual
            dcx = int(w * decider.config['deadzone_offset_x'])
            dcy = int(h * decider.config['deadzone_offset_y'])
            dr = int(w * decider.config['deadzone_radius'])
            cv2.circle(processed_image, (dcx, dcy), dr, (0, 255, 0), 1)
            
            # Status Text
            joy_text = f"Joy: {gesture_data['orbit_x']:.2f}, {gesture_data['orbit_y']:.2f}"
            cv2.putText(processed_image, joy_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Conditional Overlays (Errors/Warnings)
            for text, pos, color in gesture_data['text_overlays']:
                 cv2.putText(processed_image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            cv2.imshow(window_name, processed_image)
            
            # Check Exit Key
            key = cv2.waitKey(5) & 0xFF
            if key == 27 or key == ord('q') or key == ord('Q'):
                stop_server = True
                break

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Main Loop Error: {e}")
    finally:
        stop_server = True
        cap.release()
        cv2.destroyAllWindows()
        sender.close()
        tracker.close()
        print("Server shutdown complete.")

if __name__ == "__main__":
    main()
