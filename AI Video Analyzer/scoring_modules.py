"""
Mathematical Modules for Score Calculation - Shikshak Mitra AI
Comprehensive scoring algorithms for student engagement and teacher effectiveness
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math

class ScoreType(Enum):
    ENGAGEMENT = "engagement"
    ATTENTION = "attention"
    PARTICIPATION = "participation"
    COMPREHENSION = "comprehension"
    TEACHER_EFFECTIVENESS = "teacher_effectiveness"
    OVERALL_PERFORMANCE = "overall_performance"

@dataclass
class StudentMetrics:
    """Individual student metrics for scoring"""
    face_detection_confidence: float
    emotion_scores: Dict[str, float]  # happy, sad, confused, focused, etc.
    attention_duration: float  # seconds focused
    hand_raise_count: int
    question_responses: int
    correct_answers: int
    participation_time: float
    confusion_indicators: int

@dataclass
class ClassMetrics:
    """Class-level metrics for teacher effectiveness"""
    total_students: int
    active_participants: int
    average_attention_span: float
    question_frequency: float
    response_rate: float
    comprehension_rate: float
    engagement_variance: float

class EngagementScoreCalculator:
    """Calculate student engagement scores using multiple factors"""
    
    def __init__(self):
        # Weights for different engagement factors
        self.weights = {
            'attention': 0.35,      # Eye gaze and focus duration
            'emotion': 0.25,        # Positive emotions vs negative
            'participation': 0.20,  # Hand raises, responses
            'interaction': 0.20     # Questions asked, discussions
        }
    
    def calculate_attention_score(self, metrics: StudentMetrics, session_duration: float) -> float:
        """
        Calculate attention score based on focus duration and quality
        Formula: (attention_duration / session_duration) * confidence_factor
        """
        if session_duration <= 0:
            return 0.0
        
        # Base attention ratio
        attention_ratio = min(metrics.attention_duration / session_duration, 1.0)
        
        # Confidence factor from face detection
        confidence_factor = min(metrics.face_detection_confidence, 1.0)
        
        # Apply exponential smoothing for sustained attention
        sustained_attention_bonus = 1 + (0.2 * math.log(1 + attention_ratio))
        
        score = attention_ratio * confidence_factor * sustained_attention_bonus * 100
        return min(score, 100.0)
    
    def calculate_emotion_score(self, metrics: StudentMetrics) -> float:
        """
        Calculate emotional engagement score
        Formula: Weighted sum of positive emotions - negative emotions
        """
        positive_emotions = ['happy', 'focused', 'interested', 'engaged']
        negative_emotions = ['sad', 'confused', 'bored', 'frustrated']
        
        positive_sum = sum(metrics.emotion_scores.get(emotion, 0) for emotion in positive_emotions)
        negative_sum = sum(metrics.emotion_scores.get(emotion, 0) for emotion in negative_emotions)
        
        # Normalize to 0-100 scale
        total_emotions = positive_sum + negative_sum
        if total_emotions == 0:
            return 50.0  # Neutral score
        
        emotion_balance = (positive_sum - negative_sum) / total_emotions
        score = 50 + (emotion_balance * 50)  # Scale to 0-100
        
        return max(0.0, min(score, 100.0))
    
    def calculate_participation_score(self, metrics: StudentMetrics, class_duration: float) -> float:
        """
        Calculate participation score based on active involvement
        Formula: Weighted combination of hand raises, responses, and participation time
        """
        # Hand raise frequency (per hour)
        hand_raise_frequency = (metrics.hand_raise_count / (class_duration / 3600)) if class_duration > 0 else 0
        
        # Response accuracy rate
        response_accuracy = (metrics.correct_answers / metrics.question_responses) if metrics.question_responses > 0 else 0
        
        # Participation time ratio
        participation_ratio = min(metrics.participation_time / class_duration, 1.0) if class_duration > 0 else 0
        
        # Weighted score calculation
        hand_raise_score = min(hand_raise_frequency * 20, 40)  # Max 40 points for hand raises
        accuracy_score = response_accuracy * 30  # Max 30 points for accuracy
        time_score = participation_ratio * 30  # Max 30 points for participation time
        
        total_score = hand_raise_score + accuracy_score + time_score
        return min(total_score, 100.0)
    
    def calculate_overall_engagement(self, metrics: StudentMetrics, session_duration: float) -> Dict[str, float]:
        """
        Calculate overall engagement score combining all factors
        """
        attention_score = self.calculate_attention_score(metrics, session_duration)
        emotion_score = self.calculate_emotion_score(metrics)
        participation_score = self.calculate_participation_score(metrics, session_duration)
        
        # Interaction score (simplified)
        interaction_score = min((metrics.question_responses + metrics.hand_raise_count) * 10, 100)
        
        # Weighted overall score
        overall_score = (
            attention_score * self.weights['attention'] +
            emotion_score * self.weights['emotion'] +
            participation_score * self.weights['participation'] +
            interaction_score * self.weights['interaction']
        )
        
        return {
            'attention_score': round(attention_score, 2),
            'emotion_score': round(emotion_score, 2),
            'participation_score': round(participation_score, 2),
            'interaction_score': round(interaction_score, 2),
            'overall_engagement': round(overall_score, 2)
        }

class ComprehensionScoreCalculator:
    """Calculate student comprehension and learning effectiveness"""
    
    def __init__(self):
        self.confusion_penalty_factor = 0.1
        self.response_time_factor = 0.15
    
    def calculate_comprehension_score(self, metrics: StudentMetrics, 
                                   response_times: List[float] = None) -> float:
        """
        Calculate comprehension score based on accuracy, confusion, and response patterns
        """
        if metrics.question_responses == 0:
            return 50.0  # Neutral score for no responses
        
        # Base accuracy score
        accuracy_rate = metrics.correct_answers / metrics.question_responses
        base_score = accuracy_rate * 100
        
        # Confusion penalty
        confusion_penalty = metrics.confusion_indicators * self.confusion_penalty_factor * 10
        
        # Response time analysis (if available)
        response_time_bonus = 0
        if response_times:
            avg_response_time = np.mean(response_times)
            # Optimal response time is between 3-10 seconds
            if 3 <= avg_response_time <= 10:
                response_time_bonus = 10
            elif avg_response_time < 3:
                response_time_bonus = 5  # Too fast might indicate guessing
        
        final_score = base_score - confusion_penalty + response_time_bonus
        return max(0.0, min(final_score, 100.0))

class TeacherEffectivenessCalculator:
    """Calculate teacher effectiveness based on class-wide metrics"""
    
    def __init__(self):
        self.effectiveness_weights = {
            'engagement_rate': 0.30,
            'participation_rate': 0.25,
            'comprehension_rate': 0.25,
            'attention_consistency': 0.20
        }
    
    def calculate_class_engagement_rate(self, student_scores: List[float]) -> float:
        """Calculate average engagement rate for the class"""
        if not student_scores:
            return 0.0
        return np.mean(student_scores)
    
    def calculate_participation_rate(self, class_metrics: ClassMetrics) -> float:
        """Calculate percentage of students actively participating"""
        if class_metrics.total_students == 0:
            return 0.0
        return (class_metrics.active_participants / class_metrics.total_students) * 100
    
    def calculate_attention_consistency(self, attention_scores: List[float]) -> float:
        """
        Calculate consistency of attention across students
        Lower variance indicates better teaching effectiveness
        """
        if len(attention_scores) < 2:
            return 50.0
        
        variance = np.var(attention_scores)
        # Convert variance to consistency score (lower variance = higher consistency)
        consistency_score = max(0, 100 - (variance / 10))
        return min(consistency_score, 100.0)
    
    def calculate_teacher_effectiveness(self, class_metrics: ClassMetrics, 
                                     student_engagement_scores: List[float],
                                     student_comprehension_scores: List[float]) -> Dict[str, float]:
        """
        Calculate overall teacher effectiveness score
        """
        # Individual component scores
        engagement_rate = self.calculate_class_engagement_rate(student_engagement_scores)
        participation_rate = self.calculate_participation_rate(class_metrics)
        comprehension_rate = np.mean(student_comprehension_scores) if student_comprehension_scores else 0
        attention_consistency = self.calculate_attention_consistency(student_engagement_scores)
        
        # Weighted overall effectiveness
        overall_effectiveness = (
            engagement_rate * self.effectiveness_weights['engagement_rate'] +
            participation_rate * self.effectiveness_weights['participation_rate'] +
            comprehension_rate * self.effectiveness_weights['comprehension_rate'] +
            attention_consistency * self.effectiveness_weights['attention_consistency']
        )
        
        return {
            'engagement_rate': round(engagement_rate, 2),
            'participation_rate': round(participation_rate, 2),
            'comprehension_rate': round(comprehension_rate, 2),
            'attention_consistency': round(attention_consistency, 2),
            'overall_effectiveness': round(overall_effectiveness, 2)
        }

class RealTimeScoreProcessor:
    """Process and update scores in real-time during class sessions"""
    
    def __init__(self):
        self.engagement_calculator = EngagementScoreCalculator()
        self.comprehension_calculator = ComprehensionScoreCalculator()
        self.teacher_calculator = TeacherEffectivenessCalculator()
        
        # Moving average parameters
        self.window_size = 30  # 30-second windows
        self.score_history = {}
    
    def update_student_score(self, student_id: str, metrics: StudentMetrics, 
                           session_duration: float) -> Dict[str, float]:
        """Update individual student scores in real-time"""
        
        # Calculate current scores
        engagement_scores = self.engagement_calculator.calculate_overall_engagement(
            metrics, session_duration
        )
        comprehension_score = self.comprehension_calculator.calculate_comprehension_score(metrics)
        
        # Add comprehension to the scores
        engagement_scores['comprehension_score'] = comprehension_score
        
        # Update score history for moving averages
        if student_id not in self.score_history:
            self.score_history[student_id] = []
        
        self.score_history[student_id].append(engagement_scores)
        
        # Keep only recent history
        if len(self.score_history[student_id]) > self.window_size:
            self.score_history[student_id] = self.score_history[student_id][-self.window_size:]
        
        # Calculate moving averages
        moving_averages = self._calculate_moving_averages(student_id)
        
        return {**engagement_scores, **moving_averages}
    
    def _calculate_moving_averages(self, student_id: str) -> Dict[str, float]:
        """Calculate moving averages for smoother score updates"""
        if student_id not in self.score_history or not self.score_history[student_id]:
            return {}
        
        history = self.score_history[student_id]
        
        # Calculate averages for each metric
        metrics = ['overall_engagement', 'attention_score', 'emotion_score', 
                  'participation_score', 'comprehension_score']
        
        moving_averages = {}
        for metric in metrics:
            values = [score.get(metric, 0) for score in history if metric in score]
            if values:
                moving_averages[f'{metric}_ma'] = round(np.mean(values), 2)
        
        return moving_averages

class ScoreNormalizer:
    """Normalize and standardize scores across different contexts"""
    
    @staticmethod
    def normalize_to_grade_level(score: float, grade_level: int) -> float:
        """Adjust scores based on grade level expectations"""
        # Grade level adjustment factors
        grade_factors = {
            1: 0.7, 2: 0.75, 3: 0.8, 4: 0.85, 5: 0.9,
            6: 0.95, 7: 1.0, 8: 1.0, 9: 1.05, 10: 1.1,
            11: 1.15, 12: 1.2
        }
        
        factor = grade_factors.get(grade_level, 1.0)
        normalized_score = score * factor
        return min(normalized_score, 100.0)
    
    @staticmethod
    def normalize_to_subject(score: float, subject: str) -> float:
        """Adjust scores based on subject difficulty"""
        subject_factors = {
            'mathematics': 1.1,
            'science': 1.05,
            'english': 1.0,
            'history': 0.95,
            'art': 0.9,
            'physical_education': 0.85
        }
        
        factor = subject_factors.get(subject.lower(), 1.0)
        normalized_score = score * factor
        return min(normalized_score, 100.0)

# Example usage and testing
if __name__ == "__main__":
    # Sample student metrics
    sample_metrics = StudentMetrics(
        face_detection_confidence=0.95,
        emotion_scores={
            'happy': 0.3, 'focused': 0.4, 'confused': 0.1, 
            'bored': 0.05, 'interested': 0.15
        },
        attention_duration=1800,  # 30 minutes
        hand_raise_count=3,
        question_responses=5,
        correct_answers=4,
        participation_time=600,  # 10 minutes
        confusion_indicators=2
    )
    
    # Calculate scores
    processor = RealTimeScoreProcessor()
    scores = processor.update_student_score("student_001", sample_metrics, 2400)  # 40-minute session
    
    print("Student Engagement Scores:")
    for metric, score in scores.items():
        print(f"{metric}: {score}")
    
    # Sample class metrics for teacher effectiveness
    class_metrics = ClassMetrics(
        total_students=25,
        active_participants=20,
        average_attention_span=1500,
        question_frequency=0.5,
        response_rate=0.8,
        comprehension_rate=0.75,
        engagement_variance=15.2
    )
    
    # Calculate teacher effectiveness
    teacher_calc = TeacherEffectivenessCalculator()
    engagement_scores = [75, 82, 68, 90, 77, 85, 72, 88, 79, 83]
    comprehension_scores = [80, 75, 70, 85, 78, 82, 74, 87, 76, 81]
    
    teacher_scores = teacher_calc.calculate_teacher_effectiveness(
        class_metrics, engagement_scores, comprehension_scores
    )
    
    print("\nTeacher Effectiveness Scores:")
    for metric, score in teacher_scores.items():
        print(f"{metric}: {score}")