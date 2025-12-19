from flask import Flask, render_template, Response, jsonify
import cv2
import os
from pathlib import Path
from video_metrics_extractor import extractor

app = Flask(__name__)

# Path to video file
VIDEO_PATH = Path(__file__).parent.parent / "AI Video Analyzer" / "assets" / "IMG_6783.MOV"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Global variable to store current metrics
current_metrics = {'students': 0, 'engagement': 0, 'attention': 0, 'hand_raises': 0}

def generate_frames():
    global current_metrics
    
    if not VIDEO_PATH.exists():
        blank = cv2.zeros((480, 640, 3), dtype='uint8')
        cv2.putText(blank, 'Video Not Found', (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        blank_bytes = cv2.imencode('.jpg', blank)[1].tobytes()
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + blank_bytes + b'\r\n')
    
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            continue
        
        # Extract real-time metrics from frame
        current_metrics = extractor.analyze_frame(frame)
        
        # Send metrics to AI backend for website sync
        try:
            import requests
            requests.post('http://localhost:8000/update-video-metrics', json=current_metrics, timeout=0.1)
        except:
            pass
        
        # Add face detection and annotations
        annotated_frame = extractor.draw_annotations(frame, current_metrics)
        
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_info')
def video_info():
    if not VIDEO_PATH.exists():
        return jsonify({'status': 'not_found', 'message': 'Video file not found'})
    
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    return jsonify({
        'status': 'ok',
        'fps': fps,
        'duration': f"{int(duration // 60)}:{int(duration % 60):02d}",
        'resolution': f"{width}x{height}",
        'frames': frame_count
    })

@app.route('/live_metrics')
def live_metrics():
    """Return real-time metrics extracted from video"""
    global current_metrics
    
    return jsonify({
        'engagement': current_metrics['engagement'],
        'attention': current_metrics['attention'], 
        'hand_raises': current_metrics['hand_raises'],
        'students': current_metrics['students']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
