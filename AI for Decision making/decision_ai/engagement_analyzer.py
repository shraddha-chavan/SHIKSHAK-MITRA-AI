import pandas as pd
from data_loader import DataLoader

class EngagementAnalyzer:
    def __init__(self):
        self.loader = DataLoader()
        
    def analyze(self):
        video_df = self.loader.load_video_data()
        voice_df = self.loader.load_voice_data()
        feedback_df = self.loader.load_feedback_data()
        
        # Video engagement analysis
        avg_engagement = video_df['Engagement Score'].mean()
        low_engagement = video_df[video_df['Engagement Score'] < 30]
        high_engagement = video_df[video_df['Engagement Score'] > 80]
        
        # Voice analysis
        wpm = voice_df['words_per_minute'].iloc[0]
        sentiment = voice_df['sentiment'].iloc[0]
        questions = voice_df['questions'].iloc[0]
        
        # Feedback analysis
        engaged_count = (feedback_df['engaged'] == 'Yes').sum()
        total_feedback = len(feedback_df)
        
        return {
            'avg_engagement': avg_engagement,
            'low_engagement_count': len(low_engagement),
            'high_engagement_count': len(high_engagement),
            'words_per_minute': wpm,
            'sentiment': sentiment,
            'questions_asked': questions,
            'feedback_engaged_ratio': engaged_count / total_feedback if total_feedback > 0 else 0
        }

if __name__ == "__main__":
    analyzer = EngagementAnalyzer()
    results = analyzer.analyze()
    print("Engagement Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
