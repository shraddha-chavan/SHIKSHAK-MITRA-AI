import numpy as np
from collections import deque

class DoubtEstimator:
    def __init__(self):
        self.student_doubt_history = {}
        self.history_length = 30
    
    def estimate_doubts(self, student_id, emotion, focus_score, hand_raised):
        """Estimate doubts based on confusion, low focus, and hand raises"""
        if student_id not in self.student_doubt_history:
            self.student_doubt_history[student_id] = {
                'doubt_indicators': deque(maxlen=self.history_length),
                'doubt_count': 0,
                'last_doubt_frame': -100
            }
        
        history = self.student_doubt_history[student_id]
        
        # Doubt indicators
        is_confused = emotion in ['confused', 'bored']
        is_unfocused = focus_score < 50
        
        # Calculate doubt probability
        doubt_score = 0
        if is_confused:
            doubt_score += 0.5
        if is_unfocused:
            doubt_score += 0.3
        if hand_raised:
            doubt_score += 0.4
        
        # Register doubt if score is high
        current_frame = len(history['doubt_indicators'])
        if doubt_score > 0.7 and (current_frame - history['last_doubt_frame']) > 50:
            history['doubt_count'] += 1
            history['last_doubt_frame'] = current_frame
        
        history['doubt_indicators'].append(doubt_score)
        
        return history['doubt_count'], doubt_score > 0.7
    
    def get_total_doubts(self, student_id):
        """Get total estimated doubts"""
        if student_id not in self.student_doubt_history:
            return 0
        return self.student_doubt_history[student_id]['doubt_count']
