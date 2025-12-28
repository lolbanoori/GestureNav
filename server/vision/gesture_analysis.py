import math
from server.config import settings

class GestureDecider:
    """
    Analyzes hand landmarks to determine gesture states (Orbit, Zoom) 
    based on configuration thresholds.
    """
    def __init__(self):
        # Initialize runtime config from settings (allows for future runtime updates)
        self.config = {
            'deadzone_radius': settings.DEFAULT_DEADZONE_RADIUS,
            'deadzone_offset_x': settings.DEFAULT_DEADZONE_OFFSET_X,
            'deadzone_offset_y': settings.DEFAULT_DEADZONE_OFFSET_Y,
            'zoom_thresh_in': settings.DEFAULT_ZOOM_THRESH_IN,
            'zoom_thresh_out': settings.DEFAULT_ZOOM_THRESH_OUT,
            'orbit_sens_server': settings.DEFAULT_ORBIT_SENSITIVITY,
            'use_fist_safety': settings.DEFAULT_USE_FIST_SAFETY,
            'use_open_hand_safety': settings.DEFAULT_USE_OPEN_HAND_SAFETY
        }

    def update_config(self, new_config):
        """Updates internal configuration (e.g. from UDP listener)."""
        for key, value in new_config.items():
            if key in self.config:
                self.config[key] = value

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def analyze(self, hand_landmarks):
        """
        Analyzes landmarks and returns gesture data.
        
        Returns:
            dict: {
                'orbit_x': float,
                'orbit_y': float,
                'zoom_val': int,
                'state': str,
                'text_overlays': list of (text, pos, color) # For UI feedback
            }
        """
        result = {
            'orbit_x': 0.0,
            'orbit_y': 0.0,
            'zoom_val': 0,
            'state': "idle",
            'text_overlays': []
        }
        
        if not hand_landmarks:
            return result

        result['state'] = "active"
        wrist = hand_landmarks[0]
        
        # --- 1. ORBIT (Joystick Logic) ---
        cx = self.config['deadzone_offset_x']
        cy = self.config['deadzone_offset_y']
        
        raw_x = wrist.x - cx
        raw_y = wrist.y - cy
        
        magnitude = math.sqrt(raw_x**2 + raw_y**2)
        
        DEADZONE_THRESH = self.config['deadzone_radius']
        SENSITIVITY = self.config['orbit_sens_server']
        MAX_SPEED = settings.DEFAULT_MAX_SPEED
        
        # Safety Heuristics
        tips = [12, 16, 20] # Middle, Ring, Pinky
        avg_tip_dist = sum([self.calculate_distance(hand_landmarks[i], wrist) for i in tips]) / 3.0
        
        IS_OPEN = avg_tip_dist > settings.OPEN_HAND_THRESH
        IS_FIST = avg_tip_dist < settings.FIST_THRESH
        
        ORBIT_ALLOWED = True
        if self.config['use_open_hand_safety'] and IS_OPEN:
            ORBIT_ALLOWED = False
            result['text_overlays'].append(("OPEN HAND (ORBIT LOCKED)", (10, 150), (255, 0, 0)))

        if magnitude > DEADZONE_THRESH and ORBIT_ALLOWED:
            dir_x = raw_x / magnitude
            dir_y = raw_y / magnitude
            
            raw_strength = (magnitude - DEADZONE_THRESH) * SENSITIVITY
            strength = min(raw_strength, MAX_SPEED)
            
            result['orbit_x'] = dir_x * strength
            result['orbit_y'] = dir_y * strength
        
        # --- 2. ZOOM ---
        thumb = hand_landmarks[4]
        index = hand_landmarks[8]
        
        ZOOM_ALLOWED = True
        if self.config['use_fist_safety'] and IS_FIST:
             ZOOM_ALLOWED = False
             result['text_overlays'].append(("FIST (ZOOM LOCKED)", (10, 120), (0, 0, 255)))

        if ZOOM_ALLOWED:
            dist = self.calculate_distance(thumb, index)
            
            PINCH_IN = self.config['zoom_thresh_in']
            PINCH_OUT = self.config['zoom_thresh_out']
            
            if dist < PINCH_IN:
                result['zoom_val'] = 1
                result['text_overlays'].append(("ZOOM IN", (10, 90), (0, 0, 255)))
            elif dist > PINCH_OUT:
                result['zoom_val'] = -1
                result['text_overlays'].append(("ZOOM OUT", (10, 90), (255, 0, 0)))

        return result
