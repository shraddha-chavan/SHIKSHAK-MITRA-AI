import pandas as pd
from data_loader import DataLoader
from engagement_analyzer import EngagementAnalyzer
from attention_analyzer import AttentionAnalyzer
from interaction_analyzer import InteractionAnalyzer
from teaching_quality_analyzer import TeachingQualityAnalyzer

class DecisionMaker:
    def __init__(self):
        self.loader = DataLoader()
        
    def make_decisions(self):
        engagement = EngagementAnalyzer().analyze()
        attention = AttentionAnalyzer().analyze()
        interaction = InteractionAnalyzer().analyze()
        teaching = TeachingQualityAnalyzer().analyze()
        
        decisions = {
            'class_intervention_needed': False,
            'teaching_method_change': False,
            'individual_attention_required': False,
            'pace_adjustment': None,
            'engagement_strategy': None,
            'priority_students': []
        }
        
        # Decision: Class intervention
        if engagement['avg_engagement'] < 50 or attention['avg_attention'] < 60:
            decisions['class_intervention_needed'] = True
            decisions['intervention_type'] = 'URGENT'
        elif engagement['avg_engagement'] < 70 or attention['avg_attention'] < 75:
            decisions['class_intervention_needed'] = True
            decisions['intervention_type'] = 'MODERATE'
        
        # Decision: Teaching method
        if teaching['teacher_impact_score'] < 60 or teaching['lesson_clarity_rate'] < 70:
            decisions['teaching_method_change'] = True
        
        # Decision: Individual attention
        if engagement['low_engagement_count'] > 5 or attention['low_attention_count'] > 5:
            decisions['individual_attention_required'] = True
            video_df = self.loader.load_video_data()
            priority = video_df[
                (video_df['Engagement Score'] < 30) | (video_df['Attention Score'] < 60)
            ]['Student ID'].tolist()
            decisions['priority_students'] = priority
        
        # Decision: Pace adjustment
        decisions['pace_adjustment'] = teaching['pace_assessment']
        
        # Decision: Engagement strategy
        if interaction['interaction_rate'] < 20:
            decisions['engagement_strategy'] = 'INCREASE_INTERACTION'
        elif engagement['feedback_engaged_ratio'] < 0.5:
            decisions['engagement_strategy'] = 'IMPROVE_CONTENT_DELIVERY'
        else:
            decisions['engagement_strategy'] = 'MAINTAIN_CURRENT'
        
        return decisions

if __name__ == "__main__":
    maker = DecisionMaker()
    decisions = maker.make_decisions()
    
    print("=" * 60)
    print("DECISION ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\n🚨 Class Intervention Needed: {decisions['class_intervention_needed']}")
    if decisions['class_intervention_needed']:
        print(f"   Level: {decisions.get('intervention_type', 'N/A')}")
    
    print(f"\n📚 Teaching Method Change Required: {decisions['teaching_method_change']}")
    print(f"\n👤 Individual Attention Required: {decisions['individual_attention_required']}")
    
    if decisions['priority_students']:
        print(f"\n⚠️ Priority Students ({len(decisions['priority_students'])}):")
        for student in decisions['priority_students']:
            print(f"   • {student}")
    
    print(f"\n⏱️ Pace Adjustment: {decisions['pace_adjustment']}")
    print(f"\n🎯 Engagement Strategy: {decisions['engagement_strategy']}")
