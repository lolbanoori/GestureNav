import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from server.config import settings

class HandTracker:
    """
    Encapsulates MediaPipe Hand Object Detection and Tracking.
    """
    def __init__(self):
        self.model_path = settings.MODEL_PATH
        
        # Initialize Hand Landmarker
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.HandLandmarkerOptions(
                base_options=base_options,
                num_hands=1,
                min_hand_detection_confidence=settings.MIN_HAND_DETECTION_CONFIDENCE,
                min_hand_presence_confidence=settings.MIN_HAND_PRESENCE_CONFIDENCE,
                min_tracking_confidence=settings.MIN_TRACKING_CONFIDENCE
            )
            self.detector = vision.HandLandmarker.create_from_options(options)
            print("HandTracker initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize HandTracker: {e}")
            self.detector = None

    def process_frame(self, image):
        """
        Processes a raw OpenCV frame: flips, converts to RGB, and detects hands.
        
        Args:
            image: Raw BGR image from OpenCV.
            
        Returns:
            tuple: (processed_image, result)
                   processed_image is the flipped, potentially annotated image (though annotation happens later/separately depending on flow).
                   Actually, main.py flips then detects. So we return the flipped image so the UI can show what was actually processed.
        """
        if self.detector is None:
            return image, None

        # 1. Flip image (mirror effect)
        flipped_image = cv2.flip(image, 1)
        
        # 2. Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
        
        # 3. Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        # 4. Detect
        # Note: main.py uses strictly image mode (detect), not video mode (detect_for_video)
        detection_result = self.detector.detect(mp_image)
        
        return flipped_image, detection_result

    def draw_landmarks(self, image, detection_result):
        """
        Draws hand landmarks and connections on the image.
        
        Args:
            image: The BGR image to draw on.
            detection_result: The result object from process_frame.
        """
        if not detection_result or not detection_result.hand_landmarks:
            return

        hand_landmarks_list = detection_result.hand_landmarks
        
        # Loop through each detected hand
        for hand_landmarks in hand_landmarks_list:
            # We need to convert normalized coordinates to pixel coordinates
            h, w, _ = image.shape
            
            # Draw key points
            for lm in hand_landmarks:
                cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 4, (0, 0, 255), -1)
            
            # Simple connection drawing (wrist to index for validation from main.py, or full skeleton)
            # main.py drew specific lines:
            # cv2.line(image, (int(wrist.x*w), int(wrist.y*h)), (int(index.x*w), int(index.y*h)), (0, 255, 255), 2)
            # We can replicate that or be more generic. 
            # The prompt asks to "Ensure the drawing utilities... are either moved here..."
            # I will implement the generic full hand connections or similar to main.py to start.
            # main.py only drew: Wrist(0) -> Index(8) line. And circles for all landmarks.
            
            wrist = hand_landmarks[0]
            index = hand_landmarks[8]
            cv2.line(image, (int(wrist.x * w), int(wrist.y * h)), (int(index.x * w), int(index.y * h)), (0, 255, 255), 2)

    def close(self):
        if self.detector:
            self.detector.close()
