import numpy as np
import pandas as pd
from pathlib import Path
import json

class MathematicalScoreCalculator:
    def __init__(self):
        self.engagement_weights = {
            'attention': 0.35,
            'emotion': 0.25,
            'participation': 0.20,
            'interaction': 0.20
        }
        
        self.teacher_weights = {
            'engagement_rate': 0.30,
            'participation_rate': 0.25,
            'comprehension_rate': 0.25,
            'attention_consistency': 0.20
        }
    
    def calculate_attention_score(self, attention_duration, session_duration, confidence_factor=0.9):
        """Calculate attention score based on mathematical formula"""
        if session_duration == 0:
            return 0
        
        attention_ratio = attention_duration / session_duration
        sustained_attention_bonus = 1 + (0.2 * np.log(1 + attention_ratio))
        
        attention_score = attention_ratio * confidence_factor * sustained_attention_bonus * 100
        return min(100, max(0, attention_score))
    
    def calculate_emotion_score(self, positive_emotions, negative_emotions, total_emotions):
        """Calculate emotion score"""
        if total_emotions == 0:
            return 50
        
        emotion_score = 50 + ((positive_emotions - negative_emotions) / total_emotions) * 50
        return min(100, max(0, emotion_score))
    
    def calculate_participation_score(self, hand_raises, correct_answers, total_responses, participation_time, class_duration):
        """Calculate participation score"""
        hand_raise_score = min(hand_raises * 20, 40)
        accuracy_score = (correct_answers / max(1, total_responses)) * 30
        time_score = (participation_time / max(1, class_duration)) * 30
        
        return min(100, hand_raise_score + accuracy_score + time_score)
    
    def calculate_overall_engagement(self, attention_score, emotion_score, participation_score, interaction_score):
        """Calculate overall engagement using weighted formula"""
        return (
            attention_score * self.engagement_weights['attention'] +
            emotion_score * self.engagement_weights['emotion'] +
            participation_score * self.engagement_weights['participation'] +
            interaction_score * self.engagement_weights['interaction']
        )
    
    def calculate_comprehension_score(self, correct_answers, total_questions, confusion_indicators, avg_response_time):
        """Calculate comprehension score"""
        if total_questions == 0:
            return 0
        
        accuracy_rate = correct_answers / total_questions
        confusion_penalty = confusion_indicators * 0.1 * 10
        
        # Response time bonus
        response_time_bonus = 10 if 3 <= avg_response_time <= 10 else 0
        
        comprehension_score = (accuracy_rate * 100) - confusion_penalty + response_time_bonus
        return min(100, max(0, comprehension_score))
    
    def calculate_teacher_effectiveness(self, student_engagements, active_participants, total_students, comprehension_scores):
        """Calculate teacher effectiveness score"""
        # Class engagement rate
        engagement_rate = np.mean(student_engagements) if student_engagements else 0
        
        # Participation rate
        participation_rate = (active_participants / max(1, total_students)) * 100
        
        # Comprehension rate
        comprehension_rate = np.mean(comprehension_scores) if comprehension_scores else 0
        
        # Attention consistency
        attention_variance = np.var(student_engagements) if len(student_engagements) > 1 else 0
        attention_consistency = max(0, 100 - (attention_variance / 10))
        
        # Overall effectiveness
        effectiveness = (
            engagement_rate * self.teacher_weights['engagement_rate'] +
            participation_rate * self.teacher_weights['participation_rate'] +
            comprehension_rate * self.teacher_weights['comprehension_rate'] +
            attention_consistency * self.teacher_weights['attention_consistency']
        )
        
        return {
            'overall_effectiveness': effectiveness,
            'engagement_rate': engagement_rate,
            'participation_rate': participation_rate,
            'comprehension_rate': comprehension_rate,
            'attention_consistency': attention_consistency
        }
    
    def calculate_wpm_score(self, words_spoken, duration_minutes):
        """Calculate Words Per Minute score"""
        if duration_minutes == 0:
            return 0
        
        wpm = words_spoken / duration_minutes
        
        # Optimal WPM ranges for teaching
        if 120 <= wpm <= 160:
            return 100
        elif 100 <= wpm < 120 or 160 < wpm <= 180:
            return 85
        elif 80 <= wpm < 100 or 180 < wpm <= 200:
            return 70
        else:
            return 50
    
    def normalize_by_grade_level(self, score, grade_level):
        """Normalize score by grade level"""
        grade_factors = {
            'elementary': 0.8,
            'middle': 0.95,
            'high': 1.1
        }
        
        factor = grade_factors.get(grade_level, 1.0)
        return score * factor
    
    def normalize_by_subject(self, score, subject):
        """Normalize score by subject difficulty"""
        subject_factors = {
            'mathematics': 1.1,
            'science': 1.05,
            'english': 1.0,
            'history': 0.95,
            'arts': 0.9,
            'physical_education': 0.85
        }
        
        factor = subject_factors.get(subject.lower(), 1.0)
        return score * factor

calculator = MathematicalScoreCalculator()