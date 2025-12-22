import socket
import time
import json
import random

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5555

def main():
    print(f"Starting Dummy GestureNav Server on {UDP_IP}:{UDP_PORT}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            # Create dummy payload
            payload = {
                'state': 'active',
                'test_val': random.random()
            }
            
            # Encode and Send
            message = json.dumps(payload).encode('utf-8')
            sock.sendto(message, (UDP_IP, UDP_PORT))
            
            print(f"Sent: {payload}")
            
            # Approx 30 FPS
            time.sleep(0.033)
            
    except KeyboardInterrupt:
        print("\nStopping server...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
