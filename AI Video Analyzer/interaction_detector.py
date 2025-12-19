import cv2
import numpy as np
from collections import deque

class InteractionDetector:
    def __init__(self):
        self.student_interaction_history = {}
        self.history_length = 30
        self.hand_raise_threshold = 0.3
    
    def detect_hand_raise(self, frame, face_bbox):
        """Detect potential hand raise above face"""
        x, y, w, h = face_bbox
        
        # Check region above face for skin-colored objects
        above_y = max(0, y - h)
        above_region = frame[above_y:y, x:x+w]
        
        if above_region.size == 0:
            return False
        
        # Convert to HSV for skin detection
        hsv = cv2.cvtColor(above_region, cv2.COLOR_BGR2HSV)
        
        # Skin color range
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin_ratio = np.sum(mask > 0) / mask.size
        
        return skin_ratio > self.hand_raise_threshold
    
    def analyze_interaction(self, student_id, frame, face_data):
        """Analyze student interaction (hand raises, movement)"""
        if student_id not in self.student_interaction_history:
            self.student_interaction_history[student_id] = {
                'hand_raises': 0,
                'last_hand_raise_frame': -100,
                'interactions': deque(maxlen=self.history_length)
            }
        
        history = self.student_interaction_history[student_id]
        
        # Detect hand raise
        hand_raised = self.detect_hand_raise(frame, face_data['bbox'])
        
        # Count hand raise (with cooldown to avoid duplicates)
        current_frame = len(history['interactions'])
        if hand_raised and (current_frame - history['last_hand_raise_frame']) > 30:
            history['hand_raises'] += 1
            history['last_hand_raise_frame'] = current_frame
        
        history['interactions'].append(1 if hand_raised else 0)
        
        return hand_raised, history['hand_raises']
    
    def get_total_interactions(self, student_id):
        """Get total interaction count"""
        if student_id not in self.student_interaction_history:
            return 0
        return self.student_interaction_history[student_id]['hand_raises']
