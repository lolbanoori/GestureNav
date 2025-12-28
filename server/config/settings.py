"""
Configuration settings for the GestureNav server.
"""
import os

# Networking
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 5555
CONFIG_PORT = 5556

# Paths
# settings.py is in server/config/, so we go up one level to reach server/
SERVER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(SERVER_DIR, 'hand_landmarker.task')

# Vision Model Options
MIN_HAND_DETECTION_CONFIDENCE = 0.7
MIN_HAND_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Control Logic Defaults
DEFAULT_DEADZONE_RADIUS = 0.12
DEFAULT_DEADZONE_OFFSET_X = 0.75
DEFAULT_DEADZONE_OFFSET_Y = 0.6
DEFAULT_ZOOM_THRESH_IN = 0.10
DEFAULT_ZOOM_THRESH_OUT = 0.35
DEFAULT_ORBIT_SENSITIVITY = 3.0
DEFAULT_MAX_SPEED = 0.5

# Safety Defaults
DEFAULT_USE_FIST_SAFETY = True
DEFAULT_USE_OPEN_HAND_SAFETY = False

# Heuristic Constants
OPEN_HAND_THRESH = 0.35
FIST_THRESH = 0.25
