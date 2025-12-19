import cv2
import numpy as np
import csv
import pickle
import os
from collections import defaultdict, deque

class FixedStudentAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        if os.path.exists('hand_raise_model.pkl'):
            with open('hand_raise_model.pkl', 'rb') as f:
                self.hand_raise_model = pickle.load(f)
        else:
            self.hand_raise_model = None
        
        self.students = {}
        self.frame_count = 0
        self.max_students = 6  # Fixed number
    
    def extract_hand_features(self, frame, face_bbox):
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
        
        features = [np.sum(skin_mask > 0) / skin_mask.size]
        
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
    
    def initialize_students(self, first_frame):
        """Initialize fixed student positions from first frame"""
        gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        # Sort faces left to right, top to bottom
        faces_sorted = sorted(faces, key=lambda f: (f[1], f[0]))
        
        for i, (x, y, w, h) in enumerate(faces_sorted[:self.max_students]):
            student_id = f"Student_{i+1}"
            center = (x + w//2, y + h//2)
            self.students[student_id] = {
                'base_position': center,
                'positions': deque(maxlen=50),
                'eye_visibility': deque(maxlen=50),
                'movement': deque(maxlen=50),
                'engagement_score': deque(maxlen=50),
                'attention_score': deque(maxlen=50),
                'hand_raises': 0,
                'last_hand_raise': -100
            }
        
        print(f"✓ Initialized {len(self.students)} students")
    
    def match_face_to_student(self, face_center):
        """Match detected face to closest student"""
        min_dist = float('inf')
        matched_id = None
        
        for sid, data in self.students.items():
            dist = np.sqrt((face_center[0] - data['base_position'][0])**2 + 
                          (face_center[1] - data['base_position'][1])**2)
            if dist < min_dist:
                min_dist = dist
                matched_id = sid
        
        return matched_id if min_dist < 150 else None
    
    def process_video(self, video_path, output_path):
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
        
        print(f"🎬 Processing: {video_path}")
        
        # Initialize students from first frame
        ret, first_frame = cap.read()
        if ret:
            self.initialize_students(first_frame)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            # Track which students were detected this frame
            detected_students = set()
            
            for (x, y, w, h) in faces:
                center = (x + w//2, y + h//2)
                student_id = self.match_face_to_student(center)
                
                if student_id and student_id not in detected_students:
                    detected_students.add(student_id)
                    data = self.students[student_id]
                    
                    data['positions'].append(center)
                    
                    if len(data['positions']) > 1:
                        prev_pos = data['positions'][-2]
                        movement = np.sqrt((center[0] - prev_pos[0])**2 + (center[1] - prev_pos[1])**2)
                        data['movement'].append(movement)
                    
                    face_roi = gray[y:y+h, x:x+w]
                    eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
                    data['eye_visibility'].append(1 if len(eyes) >= 2 else 0)
                    
                    # Hand raise detection
                    hand_raised = False
                    if self.hand_raise_model:
                        features = self.extract_hand_features(frame, (x, y, w, h))
                        if features is not None:
                            pred = self.hand_raise_model.predict([features])[0]
                            prob = self.hand_raise_model.predict_proba([features])[0][1]
                            hand_raised = pred == 1 and prob > 0.6
                            
                            if hand_raised and (self.frame_count - data['last_hand_raise']) > 30:
                                data['hand_raises'] += 1
                                data['last_hand_raise'] = self.frame_count
                    
                    # Calculate scores
                    eye_score = np.mean(data['eye_visibility']) * 100 if data['eye_visibility'] else 0
                    
                    if len(data['movement']) > 5:
                        avg_movement = np.mean(list(data['movement'])[-10:])
                        movement_score = max(0, 100 - avg_movement * 2)
                    else:
                        movement_score = 50
                    
                    engagement = eye_score * 0.7 + movement_score * 0.3
                    
                    if len(data['positions']) >= 10:
                        recent = list(data['positions'])[-10:]
                        x_var = np.var([p[0] for p in recent])
                        y_var = np.var([p[1] for p in recent])
                        attention = max(0, 100 - (x_var + y_var) / 10)
                    else:
                        attention = 50
                    
                    data['engagement_score'].append(engagement)
                    data['attention_score'].append(attention)
                    
                    # Draw
                    color = (0, 255, 0) if engagement > 60 else (0, 165, 255) if engagement > 40 else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, student_id.replace('Student_', 'S'), (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    status = "Engaged" if engagement > 60 else "Moderate" if engagement > 40 else "Distracted"
                    cv2.putText(frame, status, (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                    
                    if hand_raised:
                        cv2.putText(frame, "HAND UP!", (x, y+h+30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 2)
            
            # Draw stats
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            cv2.putText(frame, f"Students: {len(self.students)}", (20, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            avg_eng = np.mean([np.mean(d['engagement_score']) for d in self.students.values() if d['engagement_score']])
            avg_att = np.mean([np.mean(d['attention_score']) for d in self.students.values() if d['attention_score']])
            total_hands = sum(d['hand_raises'] for d in self.students.values())
            
            cv2.putText(frame, f"Avg Engagement: {avg_eng:.1f}%", (20, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Avg Attention: {avg_att:.1f}%", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(frame, f"Hand Raises: {total_hands}", (20, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            
            out.write(frame)
            
            if self.frame_count % 30 == 0:
                print(f"Progress: {(self.frame_count/total_frames)*100:.1f}%", end='\r')
        
        cap.release()
        out.release()
        
        print(f"\n✅ Complete! Output: {output_path}")
        return self.generate_report(fps, total_frames)
    
    def generate_report(self, fps, total_frames):
        duration = total_frames / fps if fps > 0 else 0
        
        student_reports = []
        for sid, data in sorted(self.students.items()):
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
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Duration (seconds)', report['duration']])
            writer.writerow(['Total Students', report['total_students']])
            writer.writerow(['Frames Processed', report['frames']])
            writer.writerow([])
            
            avg_eng = np.mean([s['engagement_score'] for s in report['students']])
            avg_att = np.mean([s['attention_score'] for s in report['students']])
            total_hands = sum(s['hand_raises'] for s in report['students'])
            
            writer.writerow(['SUMMARY', ''])
            writer.writerow(['Average Engagement', f"{avg_eng:.2f}%"])
            writer.writerow(['Average Attention', f"{avg_att:.2f}%"])
            writer.writerow(['Total Hand Raises', total_hands])
            writer.writerow([])
            
            writer.writerow(['Student ID', 'Engagement Score', 'Attention Score', 'Hand Raises'])
            for s in report['students']:
                writer.writerow([s['student_id'], f"{s['engagement_score']}%", f"{s['attention_score']}%", s['hand_raises']])
        
        print(f"📄 Report saved: {path}")
    
    def display_video(self, video_path):
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
    print("🎓 Fixed Student Analyzer (6 Students)")
    print("=" * 60)
    
    analyzer = FixedStudentAnalyzer()
    report = analyzer.process_video("assets/215475_small.mp4", "output_fixed.mp4")
    
    if report:
        analyzer.save_report(report, "student_scores.csv")
        
        print("\n" + "=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(f"Students: {report['total_students']}")
        for s in report['students']:
            print(f"{s['student_id']}: Engagement={s['engagement_score']}%, Attention={s['attention_score']}%, Hands={s['hand_raises']}")
        print("=" * 60)
        
        input("\nPress ENTER to play video...")
        analyzer.display_video("output_fixed.mp4")
