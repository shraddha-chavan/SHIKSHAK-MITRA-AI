import cv2
import numpy as np
import pickle
import os
from collections import defaultdict, deque
from pathlib import Path

class RealTimeMetricsExtractor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Face tracking for stable student count
        self.face_tracker = {}
        self.next_face_id = 1
        self.face_positions = deque(maxlen=30)  # Track last 30 frames
        
        # Load hand raise model if exists
        self.hand_raise_model = None
        model_path = Path(__file__).parent.parent / "AI Video Analyzer" / "hand_raise_model.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                self.hand_raise_model = pickle.load(f)
    
    def track_faces(self, faces):
        """Track faces across frames for stable student count"""
        current_faces = {}
        
        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            
            # Find closest existing face
            min_dist = 100
            matched_id = None
            
            for face_id, last_pos in self.face_tracker.items():
                dist = np.sqrt((center[0] - last_pos[0])**2 + (center[1] - last_pos[1])**2)
                if dist < min_dist:
                    min_dist = dist
                    matched_id = face_id
            
            if matched_id is None:
                matched_id = self.next_face_id
                self.next_face_id += 1
            
            current_faces[matched_id] = center
        
        # Update tracker with current faces
        self.face_tracker = current_faces
        self.face_positions.append(len(current_faces))
        
        # Return stable count (median of recent frames)
        if len(self.face_positions) > 5:
            return int(np.median(list(self.face_positions)))
        return len(current_faces)
    
    def extract_hand_features(self, frame, face_bbox):
        """Extract features for hand raise detection"""
        x, y, w, h = face_bbox
        above_h = int(h * 1.5)
        above_y = max(0, y - above_h)
        above_region = frame[above_y:y, max(0, x-w//2):min(frame.shape[1], x+w+w//2)]
        
        if above_region.size == 0:
            return None
        
        hsv = cv2.cvtColor(above_region, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        features = []
        skin_ratio = np.sum(skin_mask > 0) / skin_mask.size
        features.append(skin_ratio)
        
        # Add more features for better detection
        vertical_profile = np.sum(skin_mask, axis=1)
        if len(vertical_profile) > 0:
            top = np.sum(vertical_profile[:len(vertical_profile)//3])
            mid = np.sum(vertical_profile[len(vertical_profile)//3:2*len(vertical_profile)//3])
            bot = np.sum(vertical_profile[2*len(vertical_profile)//3:])
            total = top + mid + bot
            features.extend([top/total if total > 0 else 0, mid/total if total > 0 else 0, bot/total if total > 0 else 0])
        else:
            features.extend([0, 0, 0])
        
        return np.array(features[:6])  # Use first 6 features
    
    def analyze_frame(self, frame):
        """Analyze single frame and return metrics"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        # Get stable student count
        student_count = self.track_faces(faces)
        
        engagement_scores = []
        attention_scores = []
        hand_raises = 0
        
        for (x, y, w, h) in faces:
            # Eye detection for engagement
            face_roi = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
            
            # Engagement based on eye visibility and face quality
            eye_score = min(len(eyes) * 50, 100)  # 2 eyes = 100%
            
            # Face quality score (contrast, sharpness)
            face_contrast = np.std(face_roi)
            quality_score = min(face_contrast * 2, 100)
            
            engagement = (eye_score * 0.7 + quality_score * 0.3)
            engagement_scores.append(engagement)
            
            # Attention based on face position (center = more attentive)
            frame_center_x = frame.shape[1] // 2
            face_center_x = x + w // 2
            distance_from_center = abs(face_center_x - frame_center_x)
            attention = max(0, 100 - (distance_from_center / frame_center_x) * 100)
            attention_scores.append(attention)
            
            # Hand raise detection
            if self.hand_raise_model is not None:
                features = self.extract_hand_features(frame, (x, y, w, h))
                if features is not None and len(features) >= 6:
                    try:
                        pred = self.hand_raise_model.predict([features])[0]
                        if pred == 1:
                            hand_raises += 1
                    except:
                        pass  # Model prediction failed
        
        # Calculate averages
        avg_engagement = np.mean(engagement_scores) if engagement_scores else 0
        avg_attention = np.mean(attention_scores) if attention_scores else 0
        
        return {
            'students': student_count,
            'engagement': int(avg_engagement),
            'attention': int(avg_attention),
            'hand_raises': hand_raises
        }
    
    def draw_annotations(self, frame, metrics):
        """Draw face detection boxes and scores on frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        student_id = 1
        for (x, y, w, h) in faces:
            # Draw face rectangle
            color = (0, 255, 0) if metrics['engagement'] > 70 else (0, 165, 255) if metrics['engagement'] > 50 else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw student ID
            cv2.putText(frame, f'S{student_id}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw engagement status
            status = "Engaged" if metrics['engagement'] > 70 else "Moderate" if metrics['engagement'] > 50 else "Low"
            cv2.putText(frame, status, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            student_id += 1
        
        # Draw overall metrics overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw metrics text
        cv2.putText(frame, f"Students: {metrics['students']}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Engagement: {metrics['engagement']}%", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Attention: {metrics['attention']}%", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"Hand Raises: {metrics['hand_raises']}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        return frame

# Global extractor instance
extractor = RealTimeMetricsExtractor()