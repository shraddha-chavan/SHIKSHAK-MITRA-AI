import cv2
import numpy as np
from collections import deque

class FocusAnalyzer:
    def __init__(self):
        self.student_focus_history = {}
        self.history_length = 30
    
    def analyze_focus(self, student_id, face_data, frame_center):
        """Analyze student focus based on eyes, position, and movement"""
        if student_id not in self.student_focus_history:
            self.student_focus_history[student_id] = {
                'positions': deque(maxlen=self.history_length),
                'eye_detections': deque(maxlen=self.history_length),
                'focus_scores': deque(maxlen=self.history_length)
            }
        
        history = self.student_focus_history[student_id]
        
        # Eye detection score (both eyes visible = focused)
        eye_score = 1.0 if len(face_data['eyes']) >= 2 else 0.3
        
        # Position score (centered = more focused)
        face_center = face_data['center']
        distance_from_center = np.sqrt((face_center[0] - frame_center[0])**2 + 
                                       (face_center[1] - frame_center[1])**2)
        max_distance = np.sqrt(frame_center[0]**2 + frame_center[1]**2)
        position_score = 1.0 - (distance_from_center / max_distance)
        
        # Movement score (less movement = more focused)
        history['positions'].append(face_center)
        if len(history['positions']) > 5:
            recent_positions = list(history['positions'])[-5:]
            movement = sum(np.sqrt((recent_positions[i][0] - recent_positions[i-1][0])**2 + 
                                   (recent_positions[i][1] - recent_positions[i-1][1])**2) 
                          for i in range(1, len(recent_positions)))
            movement_score = max(0, 1.0 - (movement / 100))
        else:
            movement_score = 0.5
        
        # Combined focus score
        focus_score = (eye_score * 0.5 + position_score * 0.3 + movement_score * 0.2) * 100
        
        history['eye_detections'].append(len(face_data['eyes']))
        history['focus_scores'].append(focus_score)
        
        return focus_score
    
    def get_average_focus(self, student_id):
        """Get average focus score for student"""
        if student_id not in self.student_focus_history:
            return 0.0
        scores = list(self.student_focus_history[student_id]['focus_scores'])
        return np.mean(scores) if scores else 0.0
