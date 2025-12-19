import cv2
import numpy as np
import csv
import pickle
import os
from collections import defaultdict, deque
from datetime import datetime

class AccurateStudentAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Load trained hand raise model if exists
        self.hand_raise_model = None
        if os.path.exists('hand_raise_model.pkl'):
            with open('hand_raise_model.pkl', 'rb') as f:
                self.hand_raise_model = pickle.load(f)
        
        self.students = {}
        self.next_id = 1
        self.frame_count = 0
    
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
        
        vertical_profile = np.sum(skin_mask, axis=1)
        if len(vertical_profile) > 0:
            top = np.sum(vertical_profile[:len(vertical_profile)//3])
            mid = np.sum(vertical_profile[len(vertical_profile)//3:2*len(vertical_profile)//3])
            bot = np.sum(vertical_profile[2*len(vertical_profile)//3:])
            total = top + mid + bot
            features.extend([top/total if total > 0 else 0, mid/total if total > 0 else 0, bot/total if total > 0 else 0])
        else:
            features.extend([0, 0, 0])
        
        horizontal_profile = np.sum(skin_mask, axis=0)
        if len(horizontal_profile) > 0:
            left = np.sum(horizontal_profile[:len(horizontal_profile)//2])
            right = np.sum(horizontal_profile[len(horizontal_profile)//2:])
            total = left + right
            features.extend([left/total if total > 0 else 0.5, right/total if total > 0 else 0.5])
        else:
            features.extend([0.5, 0.5])
        
        gray_above = cv2.cvtColor(above_region, cv2.COLOR_BGR2GRAY)
        features.append(np.mean(gray_above) / 255.0)
        
        edges = cv2.Canny(gray_above, 50, 150)
        features.append(np.sum(edges > 0) / edges.size)
        features.append(above_region.shape[0] / above_region.shape[1] if above_region.shape[1] > 0 else 1)
        
        return np.array(features)
    
    def track_student(self, center, faces_data):
        """Track students across frames"""
        min_dist = 80
        matched_id = None
        
        for sid, data in self.students.items():
            if len(data['positions']) > 0:
                last_pos = data['positions'][-1]
                dist = np.sqrt((center[0] - last_pos[0])**2 + (center[1] - last_pos[1])**2)
                if dist < min_dist:
                    min_dist = dist
                    matched_id = sid
        
        if matched_id is None:
            matched_id = f"Student_{self.next_id}"
            self.next_id += 1
            self.students[matched_id] = {
                'positions': deque(maxlen=50),
                'eye_visibility': deque(maxlen=50),
                'movement': deque(maxlen=50),
                'engagement_score': deque(maxlen=50),
                'attention_score': deque(maxlen=50),
                'hand_raises': 0,
                'last_hand_raise': -100
            }
        
        return matched_id
    
    def calculate_engagement(self, student_id):
        """Calculate engagement based on eye visibility and movement"""
        data = self.students[student_id]
        
        if len(data['eye_visibility']) == 0:
            return 0
        
        # Eyes visible = engaged
        eye_score = np.mean(data['eye_visibility']) * 100
        
        # Less movement = more focused
        if len(data['movement']) > 5:
            avg_movement = np.mean(list(data['movement'])[-10:])
            movement_score = max(0, 100 - avg_movement * 2)
        else:
            movement_score = 50
        
        engagement = (eye_score * 0.7 + movement_score * 0.3)
        return engagement
    
    def calculate_attention(self, student_id, frame_center):
        """Calculate attention based on position stability"""
        data = self.students[student_id]
        
        if len(data['positions']) < 10:
            return 50
        
        recent_positions = list(data['positions'])[-10:]
        
        # Position variance (lower = more stable = more attentive)
        x_coords = [p[0] for p in recent_positions]
        y_coords = [p[1] for p in recent_positions]
        
        x_var = np.var(x_coords)
        y_var = np.var(y_coords)
        
        stability_score = max(0, 100 - (x_var + y_var) / 10)
        
        return stability_score
    
    def process_video(self, video_path, output_path):
        """Process video with accurate detection"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Cannot open: {video_path}")
            return None
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_center = (width // 2, height // 2)
        
        print(f"🎬 Processing: {video_path}")
        print(f"📊 Frames: {total_frames}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                center = (x + w//2, y + h//2)
                student_id = self.track_student(center, faces)
                data = self.students[student_id]
                
                # Track position
                data['positions'].append(center)
                
                # Calculate movement
                if len(data['positions']) > 1:
                    prev_pos = data['positions'][-2]
                    movement = np.sqrt((center[0] - prev_pos[0])**2 + (center[1] - prev_pos[1])**2)
                    data['movement'].append(movement)
                
                # Detect eyes
                face_roi = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
                eye_visible = len(eyes) >= 2
                data['eye_visibility'].append(1 if eye_visible else 0)
                
                # Hand raise detection
                hand_raised = False
                if self.hand_raise_model is not None:
                    features = self.extract_hand_features(frame, (x, y, w, h))
                    if features is not None:
                        pred = self.hand_raise_model.predict([features])[0]
                        prob = self.hand_raise_model.predict_proba([features])[0][1]
                        hand_raised = pred == 1 and prob > 0.6
                        
                        if hand_raised and (self.frame_count - data['last_hand_raise']) > 30:
                            data['hand_raises'] += 1
                            data['last_hand_raise'] = self.frame_count
                
                # Calculate scores
                engagement = self.calculate_engagement(student_id)
                attention = self.calculate_attention(student_id, frame_center)
                
                data['engagement_score'].append(engagement)
                data['attention_score'].append(attention)
                
                # Draw annotations
                color = (0, 255, 0) if engagement > 60 else (0, 165, 255) if engagement > 40 else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                cv2.putText(frame, student_id.replace('Student_', 'S'), (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                status = "Engaged" if engagement > 60 else "Moderate" if engagement > 40 else "Distracted"
                cv2.putText(frame, status, (x, y+h+15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                
                if hand_raised:
                    cv2.putText(frame, "HAND UP!", (x, y+h+30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 2)
            
            # Draw stats
            self.draw_stats(frame, len(faces))
            
            out.write(frame)
            
            if self.frame_count % 30 == 0:
                print(f"Progress: {(self.frame_count/total_frames)*100:.1f}%", end='\r')
        
        cap.release()
        out.release()
        
        print(f"\n✅ Complete! Output: {output_path}")
        return self.generate_report(fps, total_frames)
    
    def draw_stats(self, frame, face_count):
        """Draw statistics overlay"""
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        cv2.putText(frame, f"Students: {face_count}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        if self.students:
            avg_engagement = np.mean([np.mean(d['engagement_score']) for d in self.students.values() if d['engagement_score']])
            avg_attention = np.mean([np.mean(d['attention_score']) for d in self.students.values() if d['attention_score']])
            total_hands = sum(d['hand_raises'] for d in self.students.values())
            
            cv2.putText(frame, f"Avg Engagement: {avg_engagement:.1f}%", (20, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Avg Attention: {avg_attention:.1f}%", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(frame, f"Hand Raises: {total_hands}", (20, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    def generate_report(self, fps, total_frames):
        """Generate CSV report"""
        duration = total_frames / fps if fps > 0 else 0
        
        student_reports = []
        for sid, data in self.students.items():
            engagement = np.mean(data['engagement_score']) if data['engagement_score'] else 0
            attention = np.mean(data['attention_score']) if data['attention_score'] else 0
            
            student_reports.append({
                'student_id': sid,
                'engagement_score': round(engagement, 2),
                'attention_score': round(attention, 2),
                'hand_raises': data['hand_raises']
            })
        
        return {
            'duration': round(duration, 2),
            'total_students': len(self.students),
            'frames': self.frame_count,
            'students': student_reports
        }
    
    def save_report(self, report, path):
        """Save to CSV"""
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Duration (seconds)', report['duration']])
            writer.writerow(['Total Students', report['total_students']])
            writer.writerow(['Frames Processed', report['frames']])
            writer.writerow([])
            
            writer.writerow(['Student ID', 'Engagement Score', 'Attention Score', 'Hand Raises'])
            for s in report['students']:
                writer.writerow([s['student_id'], s['engagement_score'], s['attention_score'], s['hand_raises']])
        
        print(f"📄 Report saved: {path}")
    
    def display_video(self, video_path):
        """Display video"""
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        delay = int(1000 / fps) if fps > 0 else 30
        
        print("\n🎬 Playing... (SPACE=Pause, Q=Quit)")
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Student Analysis', frame)
            
            key = cv2.waitKey(delay if not paused else 1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                paused = not paused
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print("🎓 Accurate Student Engagement Analyzer")
    print("=" * 60)
    
    # First train the model
    print("\n📚 Step 1: Training hand raise detection...")
    os.system("python hand_raise_trainer.py")
    
    # Then analyze
    print("\n📊 Step 2: Analyzing video...")
    analyzer = AccurateStudentAnalyzer()
    
    report = analyzer.process_video("assets/215475_small.mp4", "output_accurate.mp4")
    
    if report:
        analyzer.save_report(report, "accurate_report.csv")
        
        print("\n" + "=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(f"Students Detected: {report['total_students']}")
        for s in report['students']:
            print(f"{s['student_id']}: Engagement={s['engagement_score']}%, Attention={s['attention_score']}%, Hands={s['hand_raises']}")
        print("=" * 60)
        
        input("\nPress ENTER to play video...")
        analyzer.display_video("output_accurate.mp4")
