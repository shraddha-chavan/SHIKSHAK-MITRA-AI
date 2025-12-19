import pandas as pd
from data_loader import DataLoader

class AttentionAnalyzer:
    def __init__(self):
        self.loader = DataLoader()
        
    def analyze(self):
        video_df = self.loader.load_video_data()
        voice_df = self.loader.load_voice_data()
        
        # Attention metrics
        avg_attention = video_df['Attention Score'].mean()
        low_attention = video_df[video_df['Attention Score'] < 60]
        high_attention = video_df[video_df['Attention Score'] > 90]
        
        # Voice-based focus
        student_focus = voice_df['student_focus'].iloc[0]
        retention_score = voice_df['retention_score'].iloc[0]
        
        return {
            'avg_attention': avg_attention,
            'low_attention_count': len(low_attention),
            'high_attention_count': len(high_attention),
            'student_focus': student_focus,
            'retention_score': retention_score,
            'attention_distribution': {
                'low': len(low_attention),
                'medium': len(video_df[(video_df['Attention Score'] >= 60) & (video_df['Attention Score'] <= 90)]),
                'high': len(high_attention)
            }
        }

if __name__ == "__main__":
    analyzer = AttentionAnalyzer()
    results = analyzer.analyze()
    print("Attention Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
