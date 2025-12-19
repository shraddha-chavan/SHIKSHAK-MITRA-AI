import os
import glob
from student_engagement_analyzer import StudentEngagementAnalyzer
import json

class BatchVideoProcessor:
    def __init__(self, assets_folder="assets"):
        self.assets_folder = assets_folder
        self.results = []
    
    def process_all_videos(self):
        """Process all videos in assets folder"""
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(self.assets_folder, ext)))
        
        if not video_files:
            print(f"❌ No videos found in {self.assets_folder}")
            return
        
        print(f"📹 Found {len(video_files)} video(s) to process\n")
        
        for idx, video_path in enumerate(video_files, 1):
            print(f"\n{'='*60}")
            print(f"Processing Video {idx}/{len(video_files)}: {os.path.basename(video_path)}")
            print(f"{'='*60}")
            
            analyzer = StudentEngagementAnalyzer(output_video=True)
            
            try:
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                output_video_path = f"output_{video_name}.mp4"
                
                report = analyzer.process_video(
                    video_path,
                    progress_callback=lambda p: print(f"Progress: {p:.1f}%", end='\r'),
                    output_path=output_video_path
                )
                
                # Save individual report
                report_path = f"report_{video_name}.json"
                analyzer.save_report(report, report_path)
                
                print(f"\n🎬 Output video: {output_video_path}")
                
                self.results.append({
                    'video': video_name,
                    'report': report
                })
                
                print(f"\n✅ Completed: {video_name}")
                self.print_summary(report)
                
            except Exception as e:
                print(f"\n❌ Error processing {video_path}: {str(e)}")
        
        self.generate_combined_report()
    
    def print_summary(self, report):
        """Print quick summary of results"""
        metrics = report['aggregate_metrics']
        print(f"   👥 Students: {report['total_students_detected']}")
        print(f"   🎯 Focus: {metrics['average_focus_score']}/100")
        print(f"   😊 Sentiment: {metrics['average_sentiment']}/100")
        print(f"   🤚 Interactions: {metrics['total_interactions']}")
        print(f"   ❓ Questions: {metrics['estimated_questions']}")
        print(f"   🤔 Doubts: {metrics['estimated_doubts']}")
    
    def generate_combined_report(self):
        """Generate combined report for all videos"""
        if not self.results:
            return
        
        combined = {
            'total_videos_processed': len(self.results),
            'videos': self.results,
            'overall_statistics': self.calculate_overall_stats()
        }
        
        with open('combined_engagement_report.json', 'w') as f:
            json.dump(combined, f, indent=2)
        
        print(f"\n{'='*60}")
        print("📊 COMBINED REPORT GENERATED")
        print(f"{'='*60}")
        print(f"Total Videos: {len(self.results)}")
        print(f"Report saved: combined_engagement_report.json")
    
    def calculate_overall_stats(self):
        """Calculate statistics across all videos"""
        if not self.results:
            return {}
        
        total_students = sum(r['report']['total_students_detected'] for r in self.results)
        avg_focus = sum(r['report']['aggregate_metrics']['average_focus_score'] for r in self.results) / len(self.results)
        avg_sentiment = sum(r['report']['aggregate_metrics']['average_sentiment'] for r in self.results) / len(self.results)
        total_interactions = sum(r['report']['aggregate_metrics']['total_interactions'] for r in self.results)
        total_questions = sum(r['report']['aggregate_metrics']['estimated_questions'] for r in self.results)
        total_doubts = sum(r['report']['aggregate_metrics']['estimated_doubts'] for r in self.results)
        
        return {
            'total_students_across_videos': total_students,
            'average_focus_score': round(avg_focus, 2),
            'average_sentiment': round(avg_sentiment, 2),
            'total_interactions': total_interactions,
            'total_questions': total_questions,
            'total_doubts': total_doubts
        }


if __name__ == "__main__":
    processor = BatchVideoProcessor()
    processor.process_all_videos()
