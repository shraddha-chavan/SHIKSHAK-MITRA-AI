import cv2
import numpy as np
from collections import deque

class SentimentAnalyzer:
    def __init__(self):
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        self.student_sentiment_history = {}
        self.history_length = 30
    
    def analyze_sentiment(self, student_id, face_roi):
        """Analyze sentiment from facial features"""
        if student_id not in self.student_sentiment_history:
            self.student_sentiment_history[student_id] = {
                'sentiments': deque(maxlen=self.history_length),
                'emotions': deque(maxlen=self.history_length)
            }
        
        history = self.student_sentiment_history[student_id]
        
        # Detect smile
        smiles = self.smile_cascade.detectMultiScale(face_roi, 1.8, 20)
        
        # Analyze brightness (darker = possibly sad/bored)
        brightness = np.mean(face_roi)
        
        # Analyze contrast (low contrast = neutral/bored)
        contrast = np.std(face_roi)
        
        # Determine emotion and sentiment score
        if len(smiles) > 0:
            emotion = 'happy'
            sentiment_score = 85 + np.random.randint(-5, 10)
        elif brightness < 80:
            emotion = 'confused'
            sentiment_score = 40 + np.random.randint(-10, 10)
        elif contrast < 30:
            emotion = 'bored'
            sentiment_score = 35 + np.random.randint(-10, 10)
        else:
            emotion = 'neutral'
            sentiment_score = 60 + np.random.randint(-10, 10)
        
        sentiment_score = max(0, min(100, sentiment_score))
        
        history['sentiments'].append(sentiment_score)
        history['emotions'].append(emotion)
        
        return sentiment_score, emotion
    
    def get_average_sentiment(self, student_id):
        """Get average sentiment score"""
        if student_id not in self.student_sentiment_history:
            return 0.0
        scores = list(self.student_sentiment_history[student_id]['sentiments'])
        return np.mean(scores) if scores else 0.0
    
    def get_emotion_distribution(self, student_id):
        """Get emotion distribution for student"""
        if student_id not in self.student_sentiment_history:
            return {}
        emotions = list(self.student_sentiment_history[student_id]['emotions'])
        if not emotions:
            return {}
        
        unique, counts = np.unique(emotions, return_counts=True)
        return dict(zip(unique, counts))
