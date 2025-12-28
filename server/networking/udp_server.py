import socket
import json
from server.config import settings

class GestureSender:
    """
    Handles UDP communication for sending gesture data to the client (e.g., Blender).
    """
    def __init__(self):
        self.ip = settings.DEFAULT_IP
        self.port = settings.DEFAULT_PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"GestureSender initialized with target {self.ip}:{self.port}")

    def send_gesture(self, state, x, y, zoom):
        """
        Serializes and sends gesture data over UDP.
        
        Args:
            state (str): The state of the gesture (e.g., "idle", "active").
            x (float): The x-coordinate (orbit).
            y (float): The y-coordinate (orbit).
            zoom (int): The zoom value (-1, 0, 1).
        """
        payload = {
            'state': state,
            'x': x,
            'y': y,
            'zoom': zoom
        }
        
        try:
            self.sock.sendto(json.dumps(payload).encode('utf-8'), (self.ip, self.port))
        except Exception as e:
            print(f"Error sending gesture data: {e}")

    def close(self):
        """Closes the socket."""
        if self.sock:
            self.sock.close()
