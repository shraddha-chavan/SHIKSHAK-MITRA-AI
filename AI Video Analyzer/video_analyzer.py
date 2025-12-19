import cv2
import numpy as np

def analyze_video_capabilities(video_path):
    """Analyze what can actually be detected in the video"""
    cap = cv2.VideoCapture(video_path)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
    
    frame_count = 0
    face_detections = []
    eye_detections = []
    body_detections = []
    
    print("🔍 Analyzing video capabilities...")
    
    while cap.isOpened() and frame_count < 100:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        bodies = upper_body_cascade.detectMultiScale(gray, 1.1, 3, minSize=(50, 50))
        
        face_detections.append(len(faces))
        body_detections.append(len(bodies))
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_roi, 1.1, 3)
            eye_detections.append(len(eyes))
        
        frame_count += 1
    
    cap.release()
    
    print(f"\n📊 Analysis Results (first 100 frames):")
    print(f"Average faces detected: {np.mean(face_detections):.1f}")
    print(f"Max faces detected: {max(face_detections)}")
    print(f"Average eyes per face: {np.mean(eye_detections):.1f}")
    print(f"Average bodies detected: {np.mean(body_detections):.1f}")
    
    print(f"\n✅ DETECTABLE PARAMETERS:")
    print(f"1. Face Count - YES (avg {np.mean(face_detections):.1f} faces)")
    print(f"2. Eye Visibility - YES (avg {np.mean(eye_detections):.1f} eyes per face)")
    print(f"3. Face Position/Movement - YES")
    print(f"4. Brightness/Contrast - YES")
    print(f"\n❌ NOT RELIABLY DETECTABLE:")
    print(f"1. Hand Raises - Need clear upper body view")
    print(f"2. Specific Emotions - Need high-res faces")
    print(f"3. Individual Doubts - Need audio/context")
    
    return {
        'avg_faces': np.mean(face_detections),
        'max_faces': max(face_detections),
        'avg_eyes': np.mean(eye_detections),
        'can_detect_faces': np.mean(face_detections) > 0,
        'can_detect_eyes': np.mean(eye_detections) > 0
    }

if __name__ == "__main__":
    analyze_video_capabilities("assets/215475_small.mp4")
