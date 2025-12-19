import pandas as pd
from data_loader import DataLoader

class TeachingQualityAnalyzer:
    def __init__(self):
        self.loader = DataLoader()
        
    def analyze(self):
        voice_df = self.loader.load_voice_data()
        feedback_df = self.loader.load_feedback_data()
        
        # Voice metrics
        wpm = voice_df['words_per_minute'].iloc[0]
        sentiment = voice_df['sentiment'].iloc[0]
        teacher_impact = voice_df['teacher_impact_score'].iloc[0]
        active_events = voice_df['active_events'].iloc[0]
        
        # Feedback metrics
        lesson_clear = (feedback_df['lesson_clear'] == 'Yes').sum()
        respectful = (feedback_df['respectful'] == 'Yes').sum()
        total = len(feedback_df)
        
        # Teaching quality assessment
        quality_score = (teacher_impact + (lesson_clear/total*100 if total > 0 else 0)) / 2
        
        return {
            'words_per_minute': wpm,
            'sentiment': sentiment,
            'teacher_impact_score': teacher_impact,
            'active_events': active_events,
            'lesson_clarity_rate': lesson_clear / total * 100 if total > 0 else 0,
            'respectful_rate': respectful / total * 100 if total > 0 else 0,
            'overall_quality_score': quality_score,
            'pace_assessment': 'Optimal' if 80 <= wpm <= 120 else 'Too Fast' if wpm > 120 else 'Too Slow'
        }

if __name__ == "__main__":
    analyzer = TeachingQualityAnalyzer()
    results = analyzer.analyze()
    print("Teaching Quality Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
