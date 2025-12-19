import os
import glob
from main_analyzer import MainAnalyzer

def process_all_videos():
    """Process all videos in assets folder"""
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join('assets', ext)))
    
    if not video_files:
        print("❌ No videos found in assets folder")
        return
    
    print(f"📹 Found {len(video_files)} video(s)\n")
    
    for idx, video_path in enumerate(video_files, 1):
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = f"output_{video_name}.mp4"
        report_path = f"report_{video_name}.csv"
        
        print(f"\n{'='*60}")
        print(f"Processing {idx}/{len(video_files)}: {video_name}")
        print(f"{'='*60}")
        
        analyzer = MainAnalyzer()
        report = analyzer.process_video(video_path, output_path)
        
        if report:
            analyzer.save_report(report, report_path)
            print(f"✅ Completed: {video_name}")
    
    print(f"\n{'='*60}")
    print("🎉 All videos processed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_all_videos()
