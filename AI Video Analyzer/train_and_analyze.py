"""
Complete workflow: Train AI on hand raise videos, then analyze classroom
"""

import os
from hand_raise_trainer import HandRaiseTrainer
from accurate_analyzer import AccurateStudentAnalyzer

def main():
    print("=" * 70)
    print("🎓 STUDENT ENGAGEMENT ANALYSIS - COMPLETE WORKFLOW")
    print("=" * 70)
    
    # Step 1: Train AI
    print("\n📚 STEP 1: Training AI on Hand Raise Videos")
    print("-" * 70)
    
    trainer = HandRaiseTrainer()
    
    hand_raise_videos = [
        "assets/handraise tranning/handraise tranning.mp4",
        "assets/handraise tranning/handraise .mp4"
    ]
    
    normal_videos = ["assets/215475_small.mp4"]
    
    print(f"✓ Hand raise videos: {len(hand_raise_videos)}")
    print(f"✓ Normal videos: {len(normal_videos)}\n")
    
    success = trainer.train_model(hand_raise_videos, normal_videos)
    
    if not success:
        print("❌ Training failed!")
        return
    
    # Step 2: Analyze classroom video
    print("\n" + "=" * 70)
    print("📊 STEP 2: Analyzing Classroom Video")
    print("-" * 70)
    
    analyzer = AccurateStudentAnalyzer()
    
    video_path = "assets/215475_small.mp4"
    output_path = "output_accurate.mp4"
    
    report = analyzer.process_video(video_path, output_path)
    
    if not report:
        print("❌ Analysis failed!")
        return
    
    # Step 3: Save report
    analyzer.save_report(report, "accurate_report.csv")
    
    # Step 4: Display results
    print("\n" + "=" * 70)
    print("📊 ANALYSIS RESULTS")
    print("=" * 70)
    print(f"Duration: {report['duration']}s")
    print(f"Students Detected: {report['total_students']}")
    print("\nPer Student:")
    print("-" * 70)
    
    for student in report['students']:
        print(f"{student['student_id']:12} | "
              f"Engagement: {student['engagement_score']:5.1f}% | "
              f"Attention: {student['attention_score']:5.1f}% | "
              f"Hand Raises: {student['hand_raises']}")
    
    print("=" * 70)
    
    # Step 5: Auto-play video
    print("\n🎬 Press ENTER to play analyzed video...")
    input()
    analyzer.display_video(output_path)

if __name__ == "__main__":
    main()
