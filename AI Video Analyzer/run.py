"""
Simple runner script for Student Engagement Analyzer
Automatically processes video and displays results
"""

from main_analyzer import MainAnalyzer
import sys

def main():
    video_path = sys.argv[1] if len(sys.argv) > 1 else "assets/215475_small.mp4"
    
    analyzer = MainAnalyzer()
    
    print("🎓 Student Engagement Analyzer")
    print("=" * 60)
    print(f"📹 Input: {video_path}")
    print("=" * 60 + "\n")
    
    # Process
    output_path = "output_analyzed.mp4"
    report = analyzer.process_video(video_path, output_path)
    
    if report:
        # Save report
        analyzer.save_report(report, "engagement_report.csv")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        metrics = report['aggregate_metrics']
        print(f"👥 Students: {report['total_students']}")
        print(f"🎯 Focus: {metrics['average_focus_score']:.1f}/100")
        print(f"😊 Sentiment: {metrics['average_sentiment']:.1f}/100")
        print(f"🤚 Interactions: {metrics['total_interactions']}")
        print(f"❓ Doubts: {metrics['total_doubts']}")
        print("=" * 60)
        
        # Auto-play
        input("\nPress ENTER to play analyzed video...")
        analyzer.display_video(output_path)

if __name__ == "__main__":
    main()
