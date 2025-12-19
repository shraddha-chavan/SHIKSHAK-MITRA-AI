import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    def detect_faces(self, frame):
        """Detect all faces in frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        results = []
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
            
            results.append({
                'bbox': (x, y, w, h),
                'face_roi': face_roi,
                'eyes': eyes,
                'center': (x + w//2, y + h//2)
            })
        
        return results
