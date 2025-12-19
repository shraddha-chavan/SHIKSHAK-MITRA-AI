import cv2
import numpy as np
from collections import defaultdict, deque
import mediapipe as mp
from deepface import DeepFace
import json
from datetime import datetime

class StudentEngagementAnalyzer:
    def __init__(self, output_video=False):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=30,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Tracking data
        self.student_data = defaultdict(lambda: {
            'focus_timeline': [],
            'emotions': [],
            'hand_raises': 0,
            'distraction_count': 0,
            'gaze_history': deque(maxlen=30),
            'head_pose_history': deque(maxlen=30),
            'current_emotion': 'neutral',
            'current_focus': True
        })
        
        self.frame_count = 0
        self.total_students = 0
        self.output_video = output_video
        self.video_writer = None
        
    def calculate_eye_aspect_ratio(self, landmarks, eye_indices):
        """Calculate EAR for eye openness detection"""
        points = np.array([[landmarks[i].x, landmarks[i].y] for i in eye_indices])
        vertical_1 = np.linalg.norm(points[1] - points[5])
        vertical_2 = np.linalg.norm(points[2] - points[4])
        horizontal = np.linalg.norm(points[0] - points[3])
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear
    
    def calculate_head_pose(self, landmarks, img_w, img_h):
        """Calculate head orientation (yaw, pitch, roll)"""
        face_2d = []
        face_3d = []
        
        key_points = [1, 33, 263, 61, 291, 199]
        
        for idx in key_points:
            lm = landmarks[idx]
            x, y = int(lm.x * img_w), int(lm.y * img_h)
            face_2d.append([x, y])
            face_3d.append([x, y, lm.z])
        
        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)
        
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                               [0, focal_length, img_w / 2],
                               [0, 0, 1]])
        dist_matrix = np.zeros((4, 1), dtype=np.float64)
        
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        
        yaw = angles[1] * 360
        pitch = angles[0] * 360
        
        return yaw, pitch
    
    def is_looking_forward(self, yaw, pitch):
        """Determine if student is looking at board/teacher"""
        return abs(yaw) < 25 and abs(pitch) < 20
    
    def detect_hand_raise(self, pose_landmarks, img_h):
        """Detect if hand is raised above shoulder level"""
        if not pose_landmarks:
            return False
        
        try:
            left_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            left_raised = left_wrist.y < left_shoulder.y - 0.1
            right_raised = right_wrist.y < right_shoulder.y - 0.1
            
            return left_raised or right_raised
        except:
            return False
    
    def analyze_emotion(self, frame, face_box):
        """Analyze facial emotion using DeepFace"""
        try:
            x, y, w, h = face_box
            face_roi = frame[y:y+h, x:x+w]
            
            if face_roi.size == 0:
                return 'neutral', 0.5
            
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, silent=True)
            
            if isinstance(result, list):
                result = result[0]
            
            emotion = result['dominant_emotion']
            confidence = result['emotion'][emotion] / 100.0
            
            return emotion, confidence
        except:
            return 'neutral', 0.5
    
    def calculate_focus_score(self, student_id):
        """Calculate individual student focus score"""
        data = self.student_data[student_id]
        
        if len(data['focus_timeline']) == 0:
            return 0.0
        
        focused_frames = sum(data['focus_timeline'])
        total_frames = len(data['focus_timeline'])
        
        focus_ratio = focused_frames / total_frames
        distraction_penalty = min(data['distraction_count'] * 0.05, 0.3)
        
        focus_score = max(0, (focus_ratio - distraction_penalty) * 100)
        
        return round(focus_score, 2)
    
    def calculate_sentiment_score(self, student_id):
        """Calculate sentiment score from emotions"""
        data = self.student_data[student_id]
        
        if len(data['emotions']) == 0:
            return 50.0
        
        emotion_weights = {
            'happy': 1.0,
            'neutral': 0.5,
            'surprise': 0.6,
            'sad': -0.5,
            'angry': -1.0,
            'fear': -0.7,
            'disgust': -0.8
        }
        
        total_score = 0
        for emotion, confidence in data['emotions']:
            weight = emotion_weights.get(emotion, 0)
            total_score += weight * confidence
        
        sentiment = ((total_score / len(data['emotions'])) + 1) * 50
        
        return round(max(0, min(100, sentiment)), 2)
    
    def process_frame(self, frame):
        """Process single video frame"""
        self.frame_count += 1
        img_h, img_w = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output_frame = frame.copy() if self.output_video else None
        
        # Face detection and analysis
        face_results = self.face_mesh.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        current_students = 0
        hand_raised = False
        
        if pose_results.pose_landmarks:
            hand_raised = self.detect_hand_raise(pose_results.pose_landmarks, img_h)
        
        if face_results.multi_face_landmarks:
            current_students = len(face_results.multi_face_landmarks)
            self.total_students = max(self.total_students, current_students)
            
            for idx, face_landmarks in enumerate(face_results.multi_face_landmarks):
                student_id = f"student_{idx}"
                
                # Calculate head pose
                yaw, pitch = self.calculate_head_pose(face_landmarks.landmark, img_w, img_h)
                
                # Check if looking forward (focused)
                is_focused = self.is_looking_forward(yaw, pitch)
                self.student_data[student_id]['focus_timeline'].append(1 if is_focused else 0)
                self.student_data[student_id]['gaze_history'].append(is_focused)
                self.student_data[student_id]['current_focus'] = is_focused
                
                if not is_focused:
                    self.student_data[student_id]['distraction_count'] += 1
                
                # Get face bounding box for emotion analysis
                x_coords = [lm.x * img_w for lm in face_landmarks.landmark]
                y_coords = [lm.y * img_h for lm in face_landmarks.landmark]
                x, y = int(min(x_coords)), int(min(y_coords))
                w, h = int(max(x_coords) - x), int(max(y_coords) - y)
                
                # Analyze emotion every 10 frames
                if self.frame_count % 10 == 0:
                    emotion, confidence = self.analyze_emotion(frame, (x, y, w, h))
                    self.student_data[student_id]['emotions'].append((emotion, confidence))
                    self.student_data[student_id]['current_emotion'] = emotion
                
                # Draw on output frame
                if self.output_video:
                    color = (0, 255, 0) if is_focused else (0, 0, 255)
                    cv2.rectangle(output_frame, (x, y), (x+w, y+h), color, 2)
                    
                    emotion = self.student_data[student_id]['current_emotion']
                    focus_text = "Focused" if is_focused else "Distracted"
                    
                    cv2.putText(output_frame, f"S{idx+1}: {focus_text}", (x, y-25), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(output_frame, f"{emotion}", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        # Hand raise detection
        if hand_raised and self.frame_count % 15 == 0:
            for student_id in list(self.student_data.keys())[:current_students]:
                self.student_data[student_id]['hand_raises'] += 1
        
        # Draw overall stats
        if self.output_video:
            cv2.putText(output_frame, f"Students: {current_students}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            if hand_raised:
                cv2.putText(output_frame, "HAND RAISED!", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return current_students, output_frame
    
    def process_video(self, video_path, progress_callback=None, output_path=None):
        """Process entire video and return analytics"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer if output requested
        if self.output_video and output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 2nd frame for speed
            if frame_idx % 2 == 0:
                _, output_frame = self.process_frame(frame)
                if self.video_writer and output_frame is not None:
                    self.video_writer.write(output_frame)
            
            frame_idx += 1
            
            if progress_callback and frame_idx % 30 == 0:
                progress = (frame_idx / total_frames) * 100
                progress_callback(progress)
        
        cap.release()
        if self.video_writer:
            self.video_writer.release()
        
        return self.generate_report(fps, total_frames)
    
    def generate_report(self, fps, total_frames):
        """Generate final analytics report"""
        duration_seconds = total_frames / fps if fps > 0 else 0
        
        # Calculate aggregate metrics
        total_focus_score = 0
        total_sentiment = 0
        total_interactions = 0
        total_questions = 0
        total_doubts = 0
        
        student_reports = []
        
        for student_id, data in self.student_data.items():
            focus = self.calculate_focus_score(student_id)
            sentiment = self.calculate_sentiment_score(student_id)
            hand_raises = data['hand_raises']
            
            # Estimate questions (hand raises with high confidence)
            questions = int(hand_raises * 0.6)
            
            # Estimate doubts (confused emotions + some hand raises)
            confused_count = sum(1 for e, c in data['emotions'] if e in ['sad', 'fear'] and c > 0.5)
            doubts = int(confused_count * 0.3 + hand_raises * 0.4)
            
            total_focus_score += focus
            total_sentiment += sentiment
            total_interactions += hand_raises
            total_questions += questions
            total_doubts += doubts
            
            student_reports.append({
                'student_id': student_id,
                'focus_score': focus,
                'sentiment': sentiment,
                'hand_raises': hand_raises,
                'questions_estimated': questions,
                'doubts_estimated': doubts
            })
        
        num_students = len(self.student_data) if self.student_data else 1
        
        report = {
            'video_duration_seconds': round(duration_seconds, 2),
            'total_students_detected': self.total_students,
            'frames_processed': self.frame_count,
            'aggregate_metrics': {
                'average_focus_score': round(total_focus_score / num_students, 2),
                'average_sentiment': round(total_sentiment / num_students, 2),
                'total_interactions': total_interactions,
                'estimated_questions': total_questions,
                'estimated_doubts': total_doubts
            },
            'student_details': student_reports,
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def save_report(self, report, output_path):
        """Save report to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    analyzer = StudentEngagementAnalyzer(output_video=True)
    
    video_path = "assets/215475_small.mp4"
    output_video_path = "output_analyzed_video.mp4"
    
    print("🎓 Starting Student Engagement Analysis...")
    print("=" * 60)
    
    def progress_update(progress):
        print(f"Progress: {progress:.1f}%", end='\r')
    
    report = analyzer.process_video(video_path, progress_callback=progress_update, output_path=output_video_path)
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\n🎥 Video Duration: {report['video_duration_seconds']}s")
    print(f"👥 Students Detected: {report['total_students_detected']}")
    print(f"\n📈 AGGREGATE METRICS:")
    print(f"   Focus Score: {report['aggregate_metrics']['average_focus_score']}/100")
    print(f"   Sentiment: {report['aggregate_metrics']['average_sentiment']}/100")
    print(f"   Interactions: {report['aggregate_metrics']['total_interactions']}")
    print(f"   Questions (Est.): {report['aggregate_metrics']['estimated_questions']}")
    print(f"   Doubts (Est.): {report['aggregate_metrics']['estimated_doubts']}")
    
    analyzer.save_report(report, "engagement_report.json")
    print(f"\n🎬 Analyzed video saved: {output_video_path}")
