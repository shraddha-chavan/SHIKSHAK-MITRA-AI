import cv2
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class HandRaiseTrainer:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def extract_features(self, frame, face_bbox):
        """Extract features for hand raise detection"""
        x, y, w, h = face_bbox
        
        # Region above face (where hand would be)
        above_h = int(h * 1.5)
        above_y = max(0, y - above_h)
        above_region = frame[above_y:y, max(0, x-w//2):min(frame.shape[1], x+w+w//2)]
        
        if above_region.size == 0:
            return None
        
        # Convert to HSV for skin detection
        hsv = cv2.cvtColor(above_region, cv2.COLOR_BGR2HSV)
        
        # Skin color masks
        lower_skin1 = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin1 = np.array([20, 255, 255], dtype=np.uint8)
        lower_skin2 = np.array([0, 40, 60], dtype=np.uint8)
        upper_skin2 = np.array([25, 255, 255], dtype=np.uint8)
        
        mask1 = cv2.inRange(hsv, lower_skin1, upper_skin1)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        skin_mask = cv2.bitwise_or(mask1, mask2)
        
        # Features
        features = []
        
        # 1. Skin ratio in upper region
        skin_ratio = np.sum(skin_mask > 0) / skin_mask.size
        features.append(skin_ratio)
        
        # 2. Vertical distribution of skin pixels
        vertical_profile = np.sum(skin_mask, axis=1)
        if len(vertical_profile) > 0:
            top_third = np.sum(vertical_profile[:len(vertical_profile)//3])
            middle_third = np.sum(vertical_profile[len(vertical_profile)//3:2*len(vertical_profile)//3])
            bottom_third = np.sum(vertical_profile[2*len(vertical_profile)//3:])
            total = top_third + middle_third + bottom_third
            if total > 0:
                features.extend([top_third/total, middle_third/total, bottom_third/total])
            else:
                features.extend([0, 0, 0])
        else:
            features.extend([0, 0, 0])
        
        # 3. Horizontal spread
        horizontal_profile = np.sum(skin_mask, axis=0)
        if len(horizontal_profile) > 0:
            left_half = np.sum(horizontal_profile[:len(horizontal_profile)//2])
            right_half = np.sum(horizontal_profile[len(horizontal_profile)//2:])
            total = left_half + right_half
            if total > 0:
                features.extend([left_half/total, right_half/total])
            else:
                features.extend([0.5, 0.5])
        else:
            features.extend([0.5, 0.5])
        
        # 4. Brightness in upper region
        gray_above = cv2.cvtColor(above_region, cv2.COLOR_BGR2GRAY)
        features.append(np.mean(gray_above) / 255.0)
        
        # 5. Edge density (movement indicator)
        edges = cv2.Canny(gray_above, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        features.append(edge_density)
        
        # 6. Aspect ratio of region
        features.append(above_region.shape[0] / above_region.shape[1] if above_region.shape[1] > 0 else 1)
        
        return np.array(features)
    
    def train_from_video(self, video_path, is_hand_raise_video=True):
        """Train model from labeled video"""
        cap = cv2.VideoCapture(video_path)
        
        features_list = []
        labels_list = []
        
        print(f"🎓 Training from: {video_path}")
        print(f"Label: {'HAND RAISE' if is_hand_raise_video else 'NO HAND RAISE'}")
        
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            for face in faces:
                features = self.extract_features(frame, face)
                if features is not None:
                    features_list.append(features)
                    labels_list.append(1 if is_hand_raise_video else 0)
            
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames, collected {len(features_list)} samples")
        
        cap.release()
        
        print(f"✅ Collected {len(features_list)} training samples")
        return features_list, labels_list
    
    def train_model(self, hand_raise_videos, no_hand_raise_videos):
        """Train the classifier"""
        all_features = []
        all_labels = []
        
        # Train on hand raise videos
        for video in hand_raise_videos:
            features, labels = self.train_from_video(video, is_hand_raise_video=True)
            all_features.extend(features)
            all_labels.extend(labels)
        
        # Train on normal videos
        for video in no_hand_raise_videos:
            features, labels = self.train_from_video(video, is_hand_raise_video=False)
            all_features.extend(features)
            all_labels.extend(labels)
        
        if len(all_features) == 0:
            print("❌ No training data collected!")
            return False
        
        X = np.array(all_features)
        y = np.array(all_labels)
        
        print(f"\n📊 Training model with {len(X)} samples")
        print(f"Hand raise samples: {np.sum(y == 1)}")
        print(f"No hand raise samples: {np.sum(y == 0)}")
        
        # Train model
        self.model.fit(X, y)
        
        # Save model
        with open('hand_raise_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        print("✅ Model trained and saved as 'hand_raise_model.pkl'")
        return True
    
    def predict(self, frame, face_bbox):
        """Predict if hand is raised"""
        features = self.extract_features(frame, face_bbox)
        if features is None:
            return False, 0.0
        
        prediction = self.model.predict([features])[0]
        probability = self.model.predict_proba([features])[0][1]
        
        return prediction == 1, probability


if __name__ == "__main__":
    trainer = HandRaiseTrainer()
    
    # Train on BOTH hand raise videos
    hand_raise_videos = [
        "assets/handraise tranning/handraise tranning.mp4",
        "assets/handraise tranning/handraise .mp4"
    ]
    
    # Train on normal classroom video (no hand raises)
    normal_videos = ["assets/215475_small.mp4"]
    
    print("🎓 Hand Raise Detection - AI Training")
    print("=" * 60)
    print(f"Training on {len(hand_raise_videos)} hand raise videos")
    print(f"Training on {len(normal_videos)} normal videos")
    print("=" * 60 + "\n")
    
    success = trainer.train_model(hand_raise_videos, normal_videos)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Training Complete!")
        print("Model saved: hand_raise_model.pkl")
        print(f"Trained on {len(hand_raise_videos)} hand raise videos")
        print("=" * 60)
