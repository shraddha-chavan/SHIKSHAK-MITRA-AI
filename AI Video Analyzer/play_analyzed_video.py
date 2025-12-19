import cv2
import sys

def play_video(video_path):
    """Play analyzed video with controls"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps) if fps > 0 else 30
    
    print(f"🎬 Playing: {video_path}")
    print("Controls: SPACE=Pause/Resume | Q=Quit | R=Restart")
    
    paused = False
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("\n✅ Video finished")
                break
            
            cv2.imshow('Student Engagement Analysis', frame)
        
        key = cv2.waitKey(delay if not paused else 1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
            print("⏸️  Paused" if paused else "▶️  Playing")
        elif key == ord('r'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            print("🔄 Restarted")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_file = sys.argv[1] if len(sys.argv) > 1 else "output_analyzed_video.mp4"
    play_video(video_file)
