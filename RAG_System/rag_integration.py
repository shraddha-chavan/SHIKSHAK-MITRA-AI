import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "AI for Decision making" / "decision_ai"))

from advanced_rag_engine import AdvancedRAGEngine
from data_loader import DataLoader
import json
import csv
from datetime import datetime

class RAGIntegration:
    """
    Integration layer connecting RAG system with existing Shikshak Mitra AI components
    """
    
    def __init__(self):
        self.rag_engine = AdvancedRAGEngine()
        self.data_loader = DataLoader()
        self.output_path = Path(__file__).parent / "outputs"
        self.output_path.mkdir(exist_ok=True)
    
    def analyze_with_rag(self, subject: str = "general") -> Dict:
        """Complete analysis using RAG enhancement"""
        
        # Load data from existing system
        video_data = self.data_loader.load_video_data()
        voice_data = self.data_loader.load_voice_data()
        feedback_data = self.data_loader.load_feedback_data()
        
        # Combine metrics
        metrics = self._combine_metrics(video_data, voice_data, feedback_data)
        
        # Generate RAG-enhanced recommendations
        rag_recommendations = self.rag_engine.generate_smart_recommendations(metrics, subject)
        
        # Generate detailed report
        report = self._generate_comprehensive_report(metrics, rag_recommendations, subject)
        
        # Save results
        self._save_results(metrics, rag_recommendations, report)
        
        return {
            'metrics': metrics,
            'recommendations': rag_recommendations,
            'report': report
        }
    
    def _combine_metrics(self, video_data, voice_data, feedback_data) -> Dict:
        """Combine metrics from all sources"""
        
        # Video metrics
        avg_engagement = video_data['avg_engagement'] if len(video_data) > 0 else 0
        avg_attention = video_data['avg_attention'] if len(video_data) > 0 else 0
        hand_raises = video_data['total_hand_raises'] if len(video_data) > 0 else 0
        
        # Voice metrics
        wpm = voice_data.get('words_per_minute', 150)
        questions = voice_data.get('questions_detected', 0)
        sentiment = voice_data.get('sentiment', 'neutral')
        
        # Calculate derived metrics
        retention_score = self._calculate_retention_score(avg_attention, questions, feedback_data)
        curiosity_index = self._calculate_curiosity_index(hand_raises, questions, avg_engagement)
        teacher_impact_score = self._calculate_teacher_impact(avg_engagement, avg_attention, retention_score)
        interaction_rate = self._calculate_interaction_rate(hand_raises, questions, video_data)
        
        return {
            'avg_engagement': avg_engagement,
            'avg_attention': avg_attention,
            'retention_score': retention_score,
            'curiosity_index': curiosity_index,
            'teacher_impact_score': teacher_impact_score,
            'words_per_minute': wpm,
            'questions_detected': questions,
            'interaction_rate': interaction_rate,
            'sentiment': sentiment,
            'hand_raises': hand_raises
        }
    
    def _calculate_retention_score(self, attention, questions, feedback) -> float:
        """Calculate retention score"""
        base_score = attention * 0.6
        question_boost = min(questions * 2, 20)
        feedback_boost = len([f for f in feedback if f.get('understanding', 'medium') == 'high']) * 2
        return min(base_score + question_boost + feedback_boost, 100)
    
    def _calculate_curiosity_index(self, hand_raises, questions, engagement) -> float:
        """Calculate curiosity index"""
        hand_raise_score = min(hand_raises * 2, 40)
        question_score = min(questions * 2, 30)
        engagement_factor = engagement * 0.3
        return min(hand_raise_score + question_score + engagement_factor, 100)
    
    def _calculate_teacher_impact(self, engagement, attention, retention) -> float:
        """Calculate teacher impact score"""
        return (engagement * 0.35 + attention * 0.35 + retention * 0.3)
    
    def _calculate_interaction_rate(self, hand_raises, questions, video_data) -> float:
        """Calculate interaction rate"""
        total_students = video_data.get('total_students', 30)
        students_participated = video_data.get('students_raised_hands', 0)
        return (students_participated / total_students * 100) if total_students > 0 else 0
    
    def _generate_comprehensive_report(self, metrics, recommendations, subject) -> str:
        """Generate comprehensive text report"""
        
        report = []
        report.append("=" * 90)
        report.append("SHIKSHAK MITRA AI - RAG-ENHANCED COMPREHENSIVE ANALYSIS")
        report.append("=" * 90)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Subject: {subject.title()}")
        report.append("")
        
        # Metrics Summary
        report.append("=" * 90)
        report.append("PERFORMANCE METRICS")
        report.append("=" * 90)
        report.append(f"Engagement Score:        {metrics['avg_engagement']:.1f}%")
        report.append(f"Attention Score:         {metrics['avg_attention']:.1f}%")
        report.append(f"Retention Score:         {metrics['retention_score']:.1f}")
        report.append(f"Curiosity Index:         {metrics['curiosity_index']:.1f}")
        report.append(f"Teacher Impact Score:    {metrics['teacher_impact_score']:.1f}")
        report.append(f"Words Per Minute:        {metrics['words_per_minute']:.0f}")
        report.append(f"Questions Detected:      {metrics['questions_detected']}")
        report.append(f"Interaction Rate:        {metrics['interaction_rate']:.1f}%")
        report.append(f"Sentiment:               {metrics['sentiment']}")
        
        # Similar Cases
        report.append("\n" + "=" * 90)
        report.append("SIMILAR TEACHING SCENARIOS (From Training Data)")
        report.append("=" * 90)
        for i, scenario in enumerate(recommendations['similar_cases'][:3], 1):
            report.append(f"\n{i}. Scenario {scenario['scenario_id']} (Similarity: {scenario['similarity']:.2f})")
            report.append(f"   Outcome: {scenario['outcome']}")
            report.append(f"   What worked: {scenario['recommendations']}")
        
        # Immediate Actions
        report.append("\n" + "=" * 90)
        report.append("IMMEDIATE ACTIONS (Next 5-10 minutes)")
        report.append("=" * 90)
        for i, action in enumerate(recommendations['immediate_actions'][:5], 1):
            report.append(f"\n{i}. {action['action']}")
            report.append(f"   Target: {action['for_issue'].title()} | Severity: {action['severity'].upper()}")
            pred = action.get('success_prediction', {})
            if pred:
                report.append(f"   Success Probability: {pred.get('success_probability', 0)*100:.0f}% ({pred.get('confidence', 'unknown')} confidence)")
                report.append(f"   Expected Improvement: {pred.get('expected_improvement', 'N/A')}")
        
        # Short-term Strategies
        report.append("\n" + "=" * 90)
        report.append("SHORT-TERM STRATEGIES (Next 1-3 Classes)")
        report.append("=" * 90)
        for i, strategy in enumerate(recommendations['short_term_strategies'][:6], 1):
            report.append(f"{i}. {strategy['strategy']}")
            report.append(f"   For: {strategy['for_issue'].title()}")
        
        # Personalized Insights
        report.append("\n" + "=" * 90)
        report.append("PERSONALIZED INSIGHTS (Research-Backed)")
        report.append("=" * 90)
        for i, insight in enumerate(recommendations['personalized_insights'][:5], 1):
            report.append(f"\n{i}. {insight['insight']}")
            if 'action' in insight:
                report.append(f"   Action: {insight['action']}")
            if 'relevance' in insight:
                report.append(f"   Relevance: {insight['relevance']:.2f}")
        
        # Intervention Predictions
        if recommendations.get('intervention_predictions'):
            report.append("\n" + "=" * 90)
            report.append("INTERVENTION SUCCESS PREDICTIONS")
            report.append("=" * 90)
            for pred in recommendations['intervention_predictions'][:5]:
                report.append(f"\n• {pred['intervention']}")
                report.append(f"  Success Rate: {pred['success_probability']*100:.0f}%")
                report.append(f"  Expected Improvement: {pred['expected_improvement']}")
                report.append(f"  Recommendation: {pred['recommendation'].replace('_', ' ').title()}")
        
        report.append("\n" + "=" * 90)
        report.append("Powered by Shikshak Mitra AI RAG System")
        report.append("Using ML-based pattern matching and educational research database")
        report.append("=" * 90)
        
        return "\n".join(report)
    
    def _save_results(self, metrics, recommendations, report):
        """Save results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = self.output_path / f"rag_analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metrics': metrics,
                'recommendations': {
                    'immediate_actions': recommendations['immediate_actions'],
                    'short_term_strategies': recommendations['short_term_strategies'],
                    'personalized_insights': recommendations['personalized_insights'],
                    'similar_cases': recommendations['similar_cases']
                }
            }, f, indent=2)
        
        # Save text report
        report_file = self.output_path / f"rag_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save CSV for history
        csv_file = self.output_path / "rag_analysis_history.csv"
        file_exists = csv_file.exists()
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'engagement', 'attention', 'retention', 'curiosity', 
                               'teacher_impact', 'wpm', 'questions', 'interaction_rate', 
                               'immediate_actions_count', 'strategies_count'])
            
            writer.writerow([
                timestamp,
                metrics['avg_engagement'],
                metrics['avg_attention'],
                metrics['retention_score'],
                metrics['curiosity_index'],
                metrics['teacher_impact_score'],
                metrics['words_per_minute'],
                metrics['questions_detected'],
                metrics['interaction_rate'],
                len(recommendations['immediate_actions']),
                len(recommendations['short_term_strategies'])
            ])
        
        print(f"\n✓ Results saved:")
        print(f"  - JSON: {json_file}")
        print(f"  - Report: {report_file}")
        print(f"  - History: {csv_file}")
    
    def query_knowledge_base(self, query: str, top_k: int = 5):
        """Query the RAG knowledge base"""
        results = self.rag_engine.semantic_search(query, top_k=top_k)
        
        print(f"\nSearch Results for: '{query}'")
        print("=" * 80)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. [{result['category'].upper()}] Similarity: {result['similarity']:.3f}")
            data = result['data']
            if 'title' in data:
                print(f"   Title: {data['title']}")
            if 'description' in data:
                print(f"   Description: {data['description']}")
            if 'finding' in data:
                print(f"   Finding: {data['finding']}")
            if 'recommendation' in data:
                print(f"   Recommendation: {data['recommendation']}")
        
        return results


def main():
    """Main execution function"""
    print("=" * 90)
    print("SHIKSHAK MITRA AI - RAG SYSTEM")
    print("=" * 90)
    print("\nInitializing RAG Integration...")
    
    integration = RAGIntegration()
    
    print("\n1. Running Complete RAG-Enhanced Analysis...")
    result = integration.analyze_with_rag(subject="mathematics")
    
    print("\n" + result['report'])
    
    print("\n\n2. Testing Knowledge Base Query...")
    integration.query_knowledge_base("how to improve student engagement in mathematics", top_k=3)
    
    print("\n\n3. Testing Another Query...")
    integration.query_knowledge_base("strategies for low attention students", top_k=3)
    
    print("\n" + "=" * 90)
    print("RAG System Test Complete!")
    print("=" * 90)


if __name__ == "__main__":
    main()
