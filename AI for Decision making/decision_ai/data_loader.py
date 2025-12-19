import pandas as pd
import os

class DataLoader:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        

    def load_video_data(self):
        path = os.path.join(self.base_path, "AI Video Analyzer", "accurate_report.csv")
        df = pd.read_csv(path, skiprows=4)
        return df
    
    def load_voice_data(self):
        path = os.path.join(self.base_path, "AI Voice Analysis", "analysis_results.csv")
        return pd.read_csv(path)
    
    def load_feedback_data(self):
        path = os.path.join(self.base_path, "server", "data", "feedback.csv")
        return pd.read_csv(path)
