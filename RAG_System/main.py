"""
Shikshak Mitra AI - RAG System Main Entry Point
Complete teacher evaluation with RAG-enhanced recommendations
"""

import sys
from pathlib import Path
from advanced_rag_engine import AdvancedRAGEngine
from rag_engine import RAGEngine
import json

def print_header():
    print("\n" + "=" * 90)
    print("  SHIKSHAK MITRA AI - RAG-ENHANCED TEACHER EVALUATION SYSTEM")
    print("=" * 90)
    print("  Combining AI Analysis with Educational Research Knowledge Base")
    print("  100+ Research-Backed Strategies | 130+ Training Samples | ML Predictions")
    print("=" * 90 + "\n")

def print_menu():
    print("\n📋 MENU:")
    print("  1. Run Complete Analysis (with your data)")
    print("  2. Demo with Sample Data")
    print("  3. Query Knowledge Base")
    print("  4. Find Similar Scenarios")
    print("  5. Predict Intervention Success")
    print("  6. Generate Report for Custom Metrics")
    print("  7. Exit")
    print()

def run_complete_analysis():
    """Run analysis with actual data from your system"""
    print("\n🔄 Running Complete Analysis...")
    print("   Loading data from AI Video Analyzer...")
    print("   Loading data from AI Voice Analysis...")
    print("   Loading feedback data...")
    
    try:
        from rag_integration import RAGIntegration
        integration = RAGIntegration()
        
        subject = input("\n📚 Enter subject (mathematics/science/language_arts/social_studies/general): ").strip()
        if not subject:
            subject = "general"
        
        result = integration.analyze_with_rag(subject=subject)
        
        print("\n" + result['report'])
        
        print("\n✅ Analysis complete! Results saved to outputs/ folder")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure your data files are in the correct location")
        print("   Or try option 2 for demo with sample data")

def run_demo():
    """Run demo with sample data"""
    print("\n🎬 Running Demo...")
    
    rag = AdvancedRAGEngine()
    
    # Sample metrics - struggling teacher
    metrics = {
        'avg_engagement': 42,
        'avg_attention': 38,
        'retention_score': 45,
        'curiosity_index': 32,
        'words_per_minute': 200,
        'questions_detected': 6,
        'interaction_rate': 22
    }
    
    print("\n📊 Sample Teacher Metrics (Struggling):")
    print(f"   Engagement: {metrics['avg_engagement']}% (Critical)")
    print(f"   Attention: {metrics['avg_attention']}% (Critical)")
    print(f"   Retention: {metrics['retention_score']} (Critical)")
    print(f"   Curiosity: {metrics['curiosity_index']} (Low)")
    print(f"   WPM: {metrics['words_per_minute']} (Too Fast)")
    print(f"   Questions: {metrics['questions_detected']} (Too Few)")
    
    print("\n🤖 Generating RAG-Enhanced Recommendations...")
    recommendations = rag.generate_smart_recommendations(metrics, subject="mathematics")
    
    print("\n" + "=" * 90)
    print("IMMEDIATE ACTIONS (Next 5-10 minutes)")
    print("=" * 90)
    for i, action in enumerate(recommendations['immediate_actions'][:5], 1):
        print(f"\n{i}. {action['action']}")
        print(f"   Target: {action['for_issue'].title()} | Severity: {action['severity'].upper()}")
        pred = action.get('success_prediction', {})
        if pred:
            print(f"   ✓ Success Probability: {pred.get('success_probability', 0)*100:.0f}%")
            print(f"   ✓ Expected Improvement: {pred.get('expected_improvement', 'N/A')}")
    
    print("\n" + "=" * 90)
    print("SIMILAR SUCCESSFUL CASES")
    print("=" * 90)
    for i, case in enumerate(recommendations['similar_cases'][:3], 1):
        print(f"\n{i}. Scenario {case['scenario_id']} (Similarity: {case['similarity']:.2f})")
        print(f"   Outcome: {case['outcome']}")
        print(f"   What worked: {case['recommendations']}")
    
    print("\n" + "=" * 90)
    print("PERSONALIZED INSIGHTS")
    print("=" * 90)
    for i, insight in enumerate(recommendations['personalized_insights'][:3], 1):
        print(f"\n{i}. {insight['insight']}")
        if 'action' in insight:
            print(f"   → {insight['action']}")

def query_knowledge_base():
    """Interactive knowledge base query"""
    print("\n🔍 Knowledge Base Query")
    
    rag = AdvancedRAGEngine()
    
    query = input("\n💬 Enter your question: ").strip()
    if not query:
        print("   No query entered")
        return
    
    print(f"\n🔎 Searching for: '{query}'")
    results = rag.semantic_search(query, top_k=5)
    
    print("\n" + "=" * 90)
    print("SEARCH RESULTS")
    print("=" * 90)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [{result['category'].upper()}] Similarity: {result['similarity']:.3f}")
        data = result['data']
        
        if 'title' in data:
            print(f"   📌 {data['title']}")
        if 'description' in data:
            print(f"   💡 {data['description']}")
        if 'implementation' in data:
            print(f"   🔧 {data['implementation']}")
        if 'finding' in data:
            print(f"   📊 {data['finding']}")
        if 'recommendation' in data:
            print(f"   ✅ {data['recommendation']}")

def find_similar_scenarios():
    """Find similar teaching scenarios"""
    print("\n🔎 Find Similar Scenarios")
    
    rag = AdvancedRAGEngine()
    
    print("\n📊 Enter teacher metrics:")
    try:
        engagement = float(input("   Engagement (0-100): "))
        attention = float(input("   Attention (0-100): "))
        retention = float(input("   Retention (0-100): "))
        
        metrics = {
            'avg_engagement': engagement,
            'avg_attention': attention,
            'retention_score': retention,
            'curiosity_index': 50,
            'words_per_minute': 150,
            'questions_detected': 12,
            'interaction_rate': 50
        }
        
        print("\n🔍 Finding similar cases...")
        similar = rag.find_similar_scenarios(metrics, top_k=5)
        
        print("\n" + "=" * 90)
        print("SIMILAR TEACHING SCENARIOS")
        print("=" * 90)
        
        for i, scenario in enumerate(similar, 1):
            print(f"\n{i}. Scenario {scenario['scenario_id']} - Similarity: {scenario['similarity']:.3f}")
            print(f"   Metrics: Eng={scenario['metrics']['engagement']}%, "
                  f"Att={scenario['metrics']['attention']}%, "
                  f"Ret={scenario['metrics']['retention']}")
            print(f"   Outcome: {scenario['outcome']}")
            print(f"   Recommendations: {scenario['recommendations']}")
        
    except ValueError:
        print("   Invalid input. Please enter numbers.")

def predict_intervention():
    """Predict intervention success"""
    print("\n🎯 Predict Intervention Success")
    
    rag = AdvancedRAGEngine()
    
    print("\n📊 Enter current metrics:")
    try:
        engagement = float(input("   Engagement (0-100): "))
        attention = float(input("   Attention (0-100): "))
        retention = float(input("   Retention (0-100): "))
        
        metrics = {
            'avg_engagement': engagement,
            'avg_attention': attention,
            'retention_score': retention
        }
        
        print("\n🔧 Available Interventions:")
        interventions = [
            "slow_pace_increase_questions",
            "active_learning_activities",
            "wait_time_training",
            "positive_reinforcement_socratic",
            "multimodal_teaching"
        ]
        
        for i, intervention in enumerate(interventions, 1):
            print(f"   {i}. {intervention.replace('_', ' ').title()}")
        
        choice = int(input("\n   Select intervention (1-5): "))
        if 1 <= choice <= 5:
            intervention = interventions[choice - 1]
            
            print(f"\n🔮 Predicting success for: {intervention.replace('_', ' ').title()}")
            prediction = rag.predict_intervention_success(metrics, intervention)
            
            print("\n" + "=" * 90)
            print("PREDICTION RESULTS")
            print("=" * 90)
            print(f"\n✓ Success Probability: {prediction['success_probability']*100:.0f}%")
            print(f"✓ Expected Improvement: {prediction['expected_improvement']}")
            print(f"✓ Confidence Level: {prediction['confidence'].upper()}")
            print(f"✓ Based on: {prediction['historical_attempts']} historical cases")
            print(f"✓ Recommendation: {prediction['recommendation'].replace('_', ' ').title()}")
        else:
            print("   Invalid choice")
            
    except ValueError:
        print("   Invalid input")

def generate_custom_report():
    """Generate report for custom metrics"""
    print("\n📝 Generate Custom Report")
    
    rag = RAGEngine()
    
    print("\n📊 Enter all metrics:")
    try:
        metrics = {
            'avg_engagement': float(input("   Engagement (0-100): ")),
            'avg_attention': float(input("   Attention (0-100): ")),
            'retention_score': float(input("   Retention (0-100): ")),
            'curiosity_index': float(input("   Curiosity (0-100): ")),
            'words_per_minute': float(input("   Words Per Minute: ")),
            'questions_detected': int(input("   Questions Detected: ")),
            'interaction_rate': float(input("   Interaction Rate (0-100): "))
        }
        
        subject = input("\n📚 Subject (or press Enter for general): ").strip()
        if not subject:
            subject = "general"
        
        print("\n📄 Generating detailed report...")
        report = rag.generate_detailed_report(metrics, subject)
        
        print("\n" + report)
        
        # Save option
        save = input("\n💾 Save report to file? (y/n): ").strip().lower()
        if save == 'y':
            from datetime import datetime
            filename = f"custom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            output_path = Path(__file__).parent / "outputs"
            output_path.mkdir(exist_ok=True)
            
            with open(output_path / filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"   ✅ Saved to: outputs/{filename}")
        
    except ValueError:
        print("   Invalid input")

def main():
    """Main application loop"""
    print_header()
    
    print("🚀 Initializing RAG System...")
    print("   Loading knowledge bases...")
    print("   Loading training data...")
    print("   Building vector database...")
    print("   ✅ Ready!\n")
    
    while True:
        print_menu()
        
        try:
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                run_complete_analysis()
            elif choice == '2':
                run_demo()
            elif choice == '3':
                query_knowledge_base()
            elif choice == '4':
                find_similar_scenarios()
            elif choice == '5':
                predict_intervention()
            elif choice == '6':
                generate_custom_report()
            elif choice == '7':
                print("\n👋 Thank you for using Shikshak Mitra AI!")
                print("   Making teaching evaluation fair, unbiased, and actionable.\n")
                break
            else:
                print("\n❌ Invalid option. Please select 1-7.")
            
            input("\n⏸️  Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()
