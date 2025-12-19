import pandas as pd
from data_loader import DataLoader

class InteractionAnalyzer:
    def __init__(self):
        self.loader = DataLoader()
        
    def analyze(self):
        video_df = self.loader.load_video_data()
        voice_df = self.loader.load_voice_data()
        feedback_df = self.loader.load_feedback_data()
        
        # Hand raises
        total_hand_raises = video_df['Hand Raises'].sum()
        students_raised_hands = len(video_df[video_df['Hand Raises'] > 0])
        
        # Questions from voice
        questions = voice_df['questions'].iloc[0]
        curiosity_index = voice_df['curiosity_index'].iloc[0]
        
        # Doubts from feedback
        doubts_yes = (feedback_df['doubts'] == 'yes').sum()
        doubts_no = (feedback_df['doubts'] == 'no').sum()
        
        return {
            'total_hand_raises': total_hand_raises,
            'students_raised_hands': students_raised_hands,
            'questions_detected': questions,
            'curiosity_index': curiosity_index,
            'doubts_reported': doubts_yes,
            'no_doubts_reported': doubts_no,
            'interaction_rate': students_raised_hands / len(video_df) * 100
        }

if __name__ == "__main__":
    analyzer = InteractionAnalyzer()
    results = analyzer.analyze()
    print("Interaction Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
