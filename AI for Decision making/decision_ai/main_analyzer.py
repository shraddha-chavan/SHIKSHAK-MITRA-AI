from engagement_analyzer import EngagementAnalyzer
from attention_analyzer import AttentionAnalyzer
from interaction_analyzer import InteractionAnalyzer
from teaching_quality_analyzer import TeachingQualityAnalyzer
from personalized_tips_generator import PersonalizedTipsGenerator
from decision_maker import DecisionMaker
import json

def main():
    print("=" * 70)
    print("AI DECISION MAKING SYSTEM - COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    
    # Run all analyses
    print("\n📊 Running Engagement Analysis...")
    engagement = EngagementAnalyzer().analyze()
    
    print("👀 Running Attention Analysis...")
    attention = AttentionAnalyzer().analyze()
    
    print("🙋 Running Interaction Analysis...")
    interaction = InteractionAnalyzer().analyze()
    
    print("📚 Running Teaching Quality Analysis...")
    teaching = TeachingQualityAnalyzer().analyze()
    
    # Display results
    print("\n" + "=" * 70)
    print("ENGAGEMENT METRICS")
    print("=" * 70)
    print(f"Average Engagement: {engagement['avg_engagement']:.2f}%")
    print(f"Low Engagement Students: {engagement['low_engagement_count']}")
    print(f"High Engagement Students: {engagement['high_engagement_count']}")
    print(f"Words Per Minute: {engagement['words_per_minute']}")
    print(f"Sentiment: {engagement['sentiment']}")
    
    print("\n" + "=" * 70)
    print("ATTENTION METRICS")
    print("=" * 70)
    print(f"Average Attention: {attention['avg_attention']:.2f}%")
    print(f"Low Attention Students: {attention['low_attention_count']}")
    print(f"High Attention Students: {attention['high_attention_count']}")
    print(f"Student Focus Score: {attention['student_focus']}")
    print(f"Retention Score: {attention['retention_score']}")
    
    print("\n" + "=" * 70)
    print("INTERACTION METRICS")
    print("=" * 70)
    print(f"Total Hand Raises: {interaction['total_hand_raises']}")
    print(f"Students Who Raised Hands: {interaction['students_raised_hands']}")
    print(f"Questions Detected: {interaction['questions_detected']}")
    print(f"Curiosity Index: {interaction['curiosity_index']}")
    print(f"Interaction Rate: {interaction['interaction_rate']:.2f}%")
    
    print("\n" + "=" * 70)
    print("TEACHING QUALITY METRICS")
    print("=" * 70)
    print(f"Teacher Impact Score: {teaching['teacher_impact_score']}")
    print(f"Lesson Clarity Rate: {teaching['lesson_clarity_rate']:.2f}%")
    print(f"Respectful Environment: {teaching['respectful_rate']:.2f}%")
    print(f"Overall Quality Score: {teaching['overall_quality_score']:.2f}")
    print(f"Pace Assessment: {teaching['pace_assessment']}")
    
    # Generate decisions
    print("\n" + "=" * 70)
    print("DECISION RECOMMENDATIONS")
    print("=" * 70)
    decisions = DecisionMaker().make_decisions()
    print(json.dumps(decisions, indent=2))
    
    # Generate personalized tips
    print("\n" + "=" * 70)
    print("PERSONALIZED TIPS")
    print("=" * 70)
    generator = PersonalizedTipsGenerator()
    tips = generator.generate_tips()
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")
    
    print("\n" + "=" * 70)
    print("STUDENT-SPECIFIC RECOMMENDATIONS")
    print("=" * 70)
    student_tips = generator.generate_student_specific_tips()
    for student, tips in student_tips.items():
        print(f"\n{student}:")
        for tip in tips:
            print(f"  • {tip}")
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
