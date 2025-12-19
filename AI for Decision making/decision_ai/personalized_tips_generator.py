import pandas as pd
from data_loader import DataLoader
from engagement_analyzer import EngagementAnalyzer
from attention_analyzer import AttentionAnalyzer
from interaction_analyzer import InteractionAnalyzer
from teaching_quality_analyzer import TeachingQualityAnalyzer

class PersonalizedTipsGenerator:
    def __init__(self):
        self.loader = DataLoader()
        
    def generate_tips(self):
        engagement = EngagementAnalyzer().analyze()
        attention = AttentionAnalyzer().analyze()
        interaction = InteractionAnalyzer().analyze()
        teaching = TeachingQualityAnalyzer().analyze()
        
        tips = []
        
        # Engagement tips
        if engagement['avg_engagement'] < 50:
            tips.append("⚠️ CRITICAL: Average engagement is very low. Use interactive activities, games, or group work.")
        elif engagement['avg_engagement'] < 70:
            tips.append("📊 Engagement needs improvement. Try incorporating multimedia content and real-world examples.")
        
        if engagement['low_engagement_count'] > 10:
            tips.append(f"👥 {engagement['low_engagement_count']} students show low engagement. Consider one-on-one check-ins.")
        
        # Attention tips
        if attention['avg_attention'] < 70:
            tips.append("👀 Attention levels are concerning. Break lessons into shorter segments with varied activities.")
        
        if attention['low_attention_count'] > 5:
            tips.append(f"⚡ {attention['low_attention_count']} students have low attention. Use movement breaks or energizers.")
        
        # Interaction tips
        if interaction['interaction_rate'] < 20:
            tips.append("🙋 Very low interaction rate. Encourage questions by creating a safe, non-judgmental environment.")
        
        if interaction['questions_detected'] < 5:
            tips.append("❓ Few questions detected. Use think-pair-share or question prompts to stimulate curiosity.")
        
        # Teaching quality tips
        if teaching['pace_assessment'] == 'Too Fast':
            tips.append("⏱️ Speaking pace is too fast. Slow down and add pauses for comprehension.")
        elif teaching['pace_assessment'] == 'Too Slow':
            tips.append("⏱️ Speaking pace is slow. Increase energy and vary your tone to maintain interest.")
        
        if teaching['teacher_impact_score'] < 60:
            tips.append("📚 Teacher impact score is low. Focus on clarity, enthusiasm, and student connection.")
        
        if teaching['lesson_clarity_rate'] < 80:
            tips.append("💡 Lesson clarity needs improvement. Use visual aids, examples, and check for understanding.")
        
        # Positive reinforcement
        if engagement['high_engagement_count'] > 5:
            tips.append(f"✅ Great! {engagement['high_engagement_count']} students are highly engaged. Keep using current strategies.")
        
        if attention['high_attention_count'] > 10:
            tips.append(f"✅ Excellent! {attention['high_attention_count']} students maintain high attention.")
        
        if teaching['sentiment'] == 'POSITIVE':
            tips.append("😊 Positive classroom sentiment detected. Maintain this encouraging atmosphere.")
        
        return tips
    
    def generate_student_specific_tips(self):
        video_df = self.loader.load_video_data()
        student_tips = {}
        
        for _, row in video_df.iterrows():
            student_id = row['Student ID']
            tips = []
            
            if row['Engagement Score'] < 30:
                tips.append("Needs immediate attention - very low engagement")
            if row['Attention Score'] < 60:
                tips.append("Struggling to maintain attention - seat closer to front")
            if row['Hand Raises'] > 0:
                tips.append("Active participant - encourage continued participation")
            if row['Engagement Score'] > 90 and row['Attention Score'] > 90:
                tips.append("Excellent performance - consider peer mentoring role")
            
            if tips:
                student_tips[student_id] = tips
        
        return student_tips

if __name__ == "__main__":
    generator = PersonalizedTipsGenerator()
    
    print("=" * 60)
    print("PERSONALIZED TEACHING TIPS")
    print("=" * 60)
    
    tips = generator.generate_tips()
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    
    print("\n" + "=" * 60)
    print("STUDENT-SPECIFIC RECOMMENDATIONS")
    print("=" * 60)
    
    student_tips = generator.generate_student_specific_tips()
    for student, tips in student_tips.items():
        print(f"\n{student}:")
        for tip in tips:
            print(f"  • {tip}")
