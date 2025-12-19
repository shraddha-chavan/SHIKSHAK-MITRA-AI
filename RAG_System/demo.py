"""
Quick Demo of Shikshak Mitra AI RAG System
Run this to see the RAG system in action
"""

from advanced_rag_engine import AdvancedRAGEngine
import json

def print_section(title):
    print("\n" + "=" * 90)
    print(f"  {title}")
    print("=" * 90)

def demo_semantic_search(rag):
    print_section("1. SEMANTIC SEARCH DEMO")
    
    queries = [
        "how to improve student engagement",
        "strategies for low attention",
        "increase curiosity in classroom"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        results = rag.semantic_search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n   Result {i} [{result['category']}] - Similarity: {result['similarity']:.3f}")
            data = result['data']
            if 'title' in data:
                print(f"   📌 {data['title']}")
            if 'description' in data:
                print(f"   💡 {data['description'][:100]}...")

def demo_similar_scenarios(rag):
    print_section("2. SIMILAR SCENARIO MATCHING DEMO")
    
    # Example: Struggling teacher
    metrics = {
        'avg_engagement': 42,
        'avg_attention': 38,
        'retention_score': 45,
        'curiosity_index': 32,
        'words_per_minute': 200,
        'questions_detected': 6,
        'interaction_rate': 22
    }
    
    print("\n📊 Teacher Metrics:")
    print(f"   Engagement: {metrics['avg_engagement']}%")
    print(f"   Attention: {metrics['avg_attention']}%")
    print(f"   Retention: {metrics['retention_score']}")
    print(f"   Curiosity: {metrics['curiosity_index']}")
    
    print("\n🔎 Finding similar cases from training data...")
    similar = rag.find_similar_scenarios(metrics, top_k=3)
    
    for i, scenario in enumerate(similar, 1):
        print(f"\n   Similar Case {i} - Similarity: {scenario['similarity']:.3f}")
        print(f"   📈 Outcome: {scenario['outcome']}")
        print(f"   ✅ What worked: {scenario['recommendations'][:80]}...")

def demo_intervention_prediction(rag):
    print_section("3. INTERVENTION SUCCESS PREDICTION DEMO")
    
    metrics = {
        'avg_engagement': 48,
        'avg_attention': 45,
        'retention_score': 50
    }
    
    interventions = [
        "slow_pace_increase_questions",
        "active_learning_activities",
        "wait_time_training"
    ]
    
    print("\n📊 Current Metrics:")
    print(f"   Engagement: {metrics['avg_engagement']}%")
    print(f"   Attention: {metrics['avg_attention']}%")
    print(f"   Retention: {metrics['retention_score']}")
    
    print("\n🎯 Predicting intervention success...")
    
    for intervention in interventions:
        prediction = rag.predict_intervention_success(metrics, intervention)
        
        print(f"\n   Intervention: {intervention.replace('_', ' ').title()}")
        print(f"   ✓ Success Probability: {prediction['success_probability']*100:.0f}%")
        print(f"   ✓ Expected Improvement: {prediction['expected_improvement']}")
        print(f"   ✓ Confidence: {prediction['confidence'].upper()}")
        print(f"   ✓ Recommendation: {prediction['recommendation'].replace('_', ' ').title()}")

def demo_smart_recommendations(rag):
    print_section("4. SMART RECOMMENDATIONS DEMO")
    
    # Critical case
    metrics = {
        'avg_engagement': 35,
        'avg_attention': 32,
        'retention_score': 40,
        'curiosity_index': 28,
        'words_per_minute': 210,
        'questions_detected': 5,
        'interaction_rate': 18
    }
    
    print("\n🚨 CRITICAL CASE - Low Performance Across All Metrics")
    print(f"   Engagement: {metrics['avg_engagement']}% (Critical)")
    print(f"   Attention: {metrics['avg_attention']}% (Critical)")
    print(f"   WPM: {metrics['words_per_minute']} (Too Fast)")
    
    print("\n🤖 Generating AI-powered recommendations...")
    recommendations = rag.generate_smart_recommendations(metrics, subject="mathematics")
    
    print("\n⚡ IMMEDIATE ACTIONS:")
    for i, action in enumerate(recommendations['immediate_actions'][:3], 1):
        print(f"\n   {i}. {action['action']}")
        print(f"      Target: {action['for_issue'].title()}")
        pred = action.get('success_prediction', {})
        if pred:
            print(f"      Success Rate: {pred.get('success_probability', 0)*100:.0f}%")
    
    print("\n📚 PERSONALIZED INSIGHTS:")
    for i, insight in enumerate(recommendations['personalized_insights'][:2], 1):
        print(f"\n   {i}. {insight['insight'][:100]}...")

def demo_excellent_teacher(rag):
    print_section("5. EXCELLENT TEACHER ANALYSIS")
    
    # Excellent teacher
    metrics = {
        'avg_engagement': 88,
        'avg_attention': 85,
        'retention_score': 82,
        'curiosity_index': 78,
        'words_per_minute': 148,
        'questions_detected': 22,
        'interaction_rate': 75
    }
    
    print("\n⭐ EXCELLENT PERFORMANCE")
    print(f"   Engagement: {metrics['avg_engagement']}%")
    print(f"   Attention: {metrics['avg_attention']}%")
    print(f"   Retention: {metrics['retention_score']}")
    print(f"   Curiosity: {metrics['curiosity_index']}")
    
    print("\n🔎 Finding similar excellent teachers...")
    similar = rag.find_similar_scenarios(metrics, top_k=2)
    
    for i, scenario in enumerate(similar, 1):
        print(f"\n   Case {i} - Similarity: {scenario['similarity']:.3f}")
        print(f"   Outcome: {scenario['outcome']}")
        print(f"   Best Practices: {scenario['recommendations'][:80]}...")

def main():
    print("\n")
    print("╔" + "=" * 88 + "╗")
    print("║" + " " * 20 + "SHIKSHAK MITRA AI - RAG SYSTEM DEMO" + " " * 33 + "║")
    print("╚" + "=" * 88 + "╝")
    
    print("\n🚀 Initializing RAG Engine...")
    print("   Loading knowledge bases...")
    print("   Loading training data (40 scenarios, 50 feedback samples, 40 interventions)...")
    print("   Building vector database...")
    print("   Training pattern matcher...")
    
    rag = AdvancedRAGEngine()
    
    print("\n✅ RAG Engine Ready!")
    
    # Run demos
    demo_semantic_search(rag)
    demo_similar_scenarios(rag)
    demo_intervention_prediction(rag)
    demo_smart_recommendations(rag)
    demo_excellent_teacher(rag)
    
    print("\n")
    print("╔" + "=" * 88 + "╗")
    print("║" + " " * 35 + "DEMO COMPLETE!" + " " * 38 + "║")
    print("║" + " " * 88 + "║")
    print("║  The RAG system successfully demonstrated:" + " " * 41 + "║")
    print("║  ✓ Semantic search across 100+ knowledge items" + " " * 35 + "║")
    print("║  ✓ Similar scenario matching from training data" + " " * 34 + "║")
    print("║  ✓ ML-based intervention success prediction" + " " * 38 + "║")
    print("║  ✓ Smart, personalized recommendations" + " " * 43 + "║")
    print("║  ✓ Research-backed insights" + " " * 55 + "║")
    print("║" + " " * 88 + "║")
    print("║  Ready to enhance your teaching evaluation system!" + " " * 32 + "║")
    print("╚" + "=" * 88 + "╝")
    print("\n")

if __name__ == "__main__":
    main()
