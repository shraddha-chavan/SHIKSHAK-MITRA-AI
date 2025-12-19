import cv2
import numpy as np
import csv
from datetime import datetime
from face_detector import FaceDetector
from focus_analyzer import FocusAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from interaction_detector import InteractionDetector
from doubt_estimator import DoubtEstimator

class MainAnalyzer:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.focus_analyzer = FocusAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.interaction_detector = InteractionDetector()
        self.doubt_estimator = DoubtEstimator()
        
        self.student_tracker = {}
        self.next_student_id = 1
        self.frame_count = 0
    
    def track_student(self, face_center):
        """Track students across frames"""
        # Simple tracking based on proximity
        min_distance = 100
        matched_id = None
        
        for student_id, last_pos in self.student_tracker.items():
            distance = np.sqrt((face_center[0] - last_pos[0])**2 + 
                             (face_center[1] - last_pos[1])**2)
            if distance < min_distance:
                min_distance = distance
                matched_id = student_id
        
        if matched_id is None:
            matched_id = f"S{self.next_student_id}"
            self.next_student_id += 1
        
        self.student_tracker[matched_id] = face_center
        return matched_id
    
    def process_video(self, video_path, output_path):
        """Process video and generate annotated output"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return None
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_center = (width // 2, height // 2)
        
        print(f"🎬 Processing video: {video_path}")
        print(f"📊 Total frames: {total_frames}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            
            # Detect faces
            faces = self.face_detector.detect_faces(frame)
            
            # Process each student
            for face_data in faces:
                student_id = self.track_student(face_data['center'])
                
                # Analyze focus
                focus_score = self.focus_analyzer.analyze_focus(student_id, face_data, frame_center)
                
                # Analyze sentiment
                sentiment_score, emotion = self.sentiment_analyzer.analyze_sentiment(student_id, face_data['face_roi'])
                
                # Detect interactions
                hand_raised, total_interactions = self.interaction_detector.analyze_interaction(student_id, frame, face_data)
                
                # Estimate doubts
                total_doubts, has_doubt = self.doubt_estimator.estimate_doubts(student_id, emotion, focus_score, hand_raised)
                
                # Draw annotations
                x, y, w, h = face_data['bbox']
                
                # Box color based on focus
                color = (0, 255, 0) if focus_score > 60 else (0, 165, 255) if focus_score > 40 else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Student ID
                cv2.putText(frame, student_id, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Emotion
                cv2.putText(frame, emotion, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                
                # Hand raise indicator
                if hand_raised:
                    cv2.putText(frame, "HAND UP!", (x, y+h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                
                # Doubt indicator
                if has_doubt:
                    cv2.circle(frame, (x+w-10, y+10), 8, (0, 0, 255), -1)
                    cv2.putText(frame, "?", (x+w-15, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Draw overall stats
            self.draw_stats(frame, faces)
            
            out.write(frame)
            
            if self.frame_count % 30 == 0:
                progress = (self.frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}%", end='\r')
        
        cap.release()
        out.release()
        
        print(f"\n✅ Video processing complete!")
        print(f"📹 Output saved: {output_path}")
        
        return self.generate_report(fps, total_frames)
    
    def draw_stats(self, frame, faces):
        """Draw statistics overlay"""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 180), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Stats
        cv2.putText(frame, f"Students Detected: {len(faces)}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Calculate aggregate metrics
        total_focus = sum(self.focus_analyzer.get_average_focus(sid) for sid in self.student_tracker.keys())
        avg_focus = total_focus / len(self.student_tracker) if self.student_tracker else 0
        
        total_sentiment = sum(self.sentiment_analyzer.get_average_sentiment(sid) for sid in self.student_tracker.keys())
        avg_sentiment = total_sentiment / len(self.student_tracker) if self.student_tracker else 0
        
        total_interactions = sum(self.interaction_detector.get_total_interactions(sid) for sid in self.student_tracker.keys())
        total_doubts = sum(self.doubt_estimator.get_total_doubts(sid) for sid in self.student_tracker.keys())
        
        cv2.putText(frame, f"Avg Focus Score: {avg_focus:.1f}/100", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Avg Sentiment: {avg_sentiment:.1f}/100", (20, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"Total Interactions: {total_interactions}", (20, 125), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Estimated Doubts: {total_doubts}", (20, 155), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
    
    def generate_report(self, fps, total_frames):
        """Generate final report"""
        duration = total_frames / fps if fps > 0 else 0
        
        student_reports = []
        for student_id in self.student_tracker.keys():
            focus = self.focus_analyzer.get_average_focus(student_id)
            sentiment = self.sentiment_analyzer.get_average_sentiment(student_id)
            interactions = self.interaction_detector.get_total_interactions(student_id)
            doubts = self.doubt_estimator.get_total_doubts(student_id)
            emotions = self.sentiment_analyzer.get_emotion_distribution(student_id)
            
            student_reports.append({
                'student_id': student_id,
                'focus_score': round(focus, 2),
                'sentiment_score': round(sentiment, 2),
                'interactions': interactions,
                'doubts': doubts,
                'emotion_distribution': emotions
            })
        
        num_students = len(student_reports)
        
        report = {
            'video_duration_seconds': round(duration, 2),
            'total_students': num_students,
            'frames_processed': self.frame_count,
            'aggregate_metrics': {
                'average_focus_score': round(sum(s['focus_score'] for s in student_reports) / num_students, 2) if num_students else 0,
                'average_sentiment': round(sum(s['sentiment_score'] for s in student_reports) / num_students, 2) if num_students else 0,
                'total_interactions': sum(s['interactions'] for s in student_reports),
                'total_doubts': sum(s['doubts'] for s in student_reports)
            },
            'student_details': student_reports,
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def save_report(self, report, output_path):
        """Save report to CSV"""
        csv_path = output_path.replace('.json', '.csv')
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Video Duration (seconds)', report['video_duration_seconds']])
            writer.writerow(['Total Students', report['total_students']])
            writer.writerow(['Frames Processed', report['frames_processed']])
            writer.writerow([])
            
            # Aggregate metrics
            writer.writerow(['AGGREGATE METRICS', ''])
            writer.writerow(['Average Focus Score', report['aggregate_metrics']['average_focus_score']])
            writer.writerow(['Average Sentiment', report['aggregate_metrics']['average_sentiment']])
            writer.writerow(['Total Interactions', report['aggregate_metrics']['total_interactions']])
            writer.writerow(['Total Doubts', report['aggregate_metrics']['total_doubts']])
            writer.writerow([])
            
            # Student details
            writer.writerow(['STUDENT DETAILS', ''])
            writer.writerow(['Student ID', 'Focus Score', 'Sentiment Score', 'Interactions', 'Doubts', 'Emotions'])
            
            for student in report['student_details']:
                emotions_str = ', '.join([f"{k}:{v}" for k, v in student['emotion_distribution'].items()])
                writer.writerow([
                    student['student_id'],
                    student['focus_score'],
                    student['sentiment_score'],
                    student['interactions'],
                    student['doubts'],
                    emotions_str
                ])
        
        print(f"📄 Report saved: {csv_path}")
    
    def display_video(self, video_path):
        """Display the analyzed video"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return
        
        print(f"\n🎬 Playing analyzed video...")
        print("Controls: SPACE=Pause | Q=Quit | R=Restart")
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        delay = int(1000 / fps) if fps > 0 else 30
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Student Engagement Analysis', frame)
            
            key = cv2.waitKey(delay if not paused else 1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord(' '):
                paused = not paused
            elif key == ord('r'):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    analyzer = MainAnalyzer()
    
    video_path = "assets/215475_small.mp4"
    output_path = "output_analyzed.mp4"
    report_path = "engagement_report.csv"
    
    print("🎓 Student Engagement Analyzer")
    print("=" * 60)
    
    # Process video
    report = analyzer.process_video(video_path, output_path)
    
    if report:
        # Save report
        analyzer.save_report(report, report_path)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Duration: {report['video_duration_seconds']}s")
        print(f"Students: {report['total_students']}")
        print(f"\n📈 Metrics:")
        print(f"  Focus Score: {report['aggregate_metrics']['average_focus_score']}/100")
        print(f"  Sentiment: {report['aggregate_metrics']['average_sentiment']}/100")
        print(f"  Interactions: {report['aggregate_metrics']['total_interactions']}")
        print(f"  Doubts: {report['aggregate_metrics']['total_doubts']}")
        
        # Auto-play video
        print("\n" + "=" * 60)
        analyzer.display_video(output_path)
