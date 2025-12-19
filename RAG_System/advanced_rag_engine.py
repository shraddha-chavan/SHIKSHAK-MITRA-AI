import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

class AdvancedRAGEngine:
    """
    Advanced RAG Engine with ML-based similarity and pattern matching
    """
    
    def __init__(self, knowledge_base_path: str = None):
        if knowledge_base_path is None:
            knowledge_base_path = Path(__file__).parent / "knowledge_base"
        
        self.kb_path = Path(knowledge_base_path)
        self.cache_path = Path(__file__).parent / "cache"
        self.cache_path.mkdir(exist_ok=True)
        
        # Load knowledge bases
        self.teaching_practices = self._load_json("teaching_best_practices.json")
        self.research = self._load_json("educational_research.json")
        self.interventions = self._load_json("intervention_strategies.json")
        self.subject_strategies = self._load_json("subject_specific_strategies.json")
        
        # Load training data
        self.training_scenarios = pd.read_csv(self.kb_path / "training_data_scenarios.csv")
        self.feedback_corpus = pd.read_csv(self.kb_path / "teacher_feedback_corpus.csv")
        self.successful_interventions = pd.read_csv(self.kb_path / "successful_interventions.csv")
        
        # Build vector database
        self.vector_db = self._build_vector_database()
        
        # Train pattern matcher
        self.pattern_matcher = self._train_pattern_matcher()
    
    def _load_json(self, filename: str) -> Dict:
        with open(self.kb_path / filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_embedding(self, text: str, dim: int = 256) -> np.ndarray:
        """Enhanced embedding with better text representation"""
        words = text.lower().split()
        
        # Create multi-dimensional embedding
        embedding = np.zeros(dim)
        
        # Word frequency features
        for word in words:
            hash_val = hash(word) % dim
            embedding[hash_val] += 1
        
        # Bigram features
        for i in range(len(words) - 1):
            bigram = f"{words[i]}_{words[i+1]}"
            hash_val = hash(bigram) % dim
            embedding[hash_val] += 0.5
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _build_vector_database(self) -> Dict:
        """Build comprehensive vector database from all knowledge sources"""
        cache_file = self.cache_path / "vector_db.pkl"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        vector_db = {
            'practices': [],
            'research': [],
            'interventions': [],
            'scenarios': [],
            'feedback': []
        }
        
        # Embed teaching practices
        for category in ['engagement_strategies', 'attention_strategies', 
                        'interaction_strategies', 'sentiment_strategies', 'retention_strategies']:
            for item in self.teaching_practices.get(category, []):
                text = f"{item['title']} {item['description']} {item.get('implementation', '')}"
                vector_db['practices'].append({
                    'id': item['id'],
                    'embedding': self._create_embedding(text),
                    'data': item,
                    'category': category
                })
        
        # Embed research
        for item in self.research.get('research_findings', []):
            text = f"{item['topic']} {item['finding']} {item['recommendation']}"
            vector_db['research'].append({
                'id': item['id'],
                'embedding': self._create_embedding(text),
                'data': item
            })
        
        # Embed interventions
        for item in self.interventions.get('interventions', []):
            text = f"{item['problem']} {' '.join(item['immediate_actions'][:2])}"
            vector_db['interventions'].append({
                'id': item['id'],
                'embedding': self._create_embedding(text),
                'data': item
            })
        
        # Embed training scenarios
        for _, row in self.training_scenarios.iterrows():
            text = f"engagement {row['avg_engagement']} attention {row['avg_attention']} {row['outcome']} {row['recommendations']}"
            vector_db['scenarios'].append({
                'id': row['scenario_id'],
                'embedding': self._create_embedding(text),
                'data': row.to_dict()
            })
        
        # Embed feedback patterns
        feedback_groups = self.feedback_corpus.groupby(['engagement_level', 'attention_level', 'overall_rating'])
        for (eng, att, rating), group in feedback_groups:
            text = ' '.join(group['student_feedback'].tolist())
            vector_db['feedback'].append({
                'id': f"feedback_{eng}_{att}_{rating}",
                'embedding': self._create_embedding(text),
                'data': {
                    'engagement': eng,
                    'attention': att,
                    'rating': rating,
                    'sample_feedback': group['student_feedback'].tolist()[:3]
                }
            })
        
        # Cache
        with open(cache_file, 'wb') as f:
            pickle.dump(vector_db, f)
        
        return vector_db
    
    def _train_pattern_matcher(self) -> Dict:
        """Train pattern matcher on successful interventions"""
        cache_file = self.cache_path / "pattern_matcher.pkl"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        # Extract patterns from successful interventions
        patterns = {}
        
        for _, row in self.successful_interventions.iterrows():
            intervention = row['intervention_applied']
            improvement = row['improvement_percentage']
            success = row['success_level']
            
            if intervention not in patterns:
                patterns[intervention] = {
                    'count': 0,
                    'avg_improvement': 0,
                    'success_rates': {'low': 0, 'medium': 0, 'high': 0, 'very_high': 0},
                    'initial_ranges': {
                        'engagement': [],
                        'attention': [],
                        'retention': []
                    }
                }
            
            patterns[intervention]['count'] += 1
            patterns[intervention]['avg_improvement'] += improvement
            patterns[intervention]['success_rates'][success] += 1
            patterns[intervention]['initial_ranges']['engagement'].append(row['initial_engagement'])
            patterns[intervention]['initial_ranges']['attention'].append(row['initial_attention'])
            patterns[intervention]['initial_ranges']['retention'].append(row['initial_retention'])
        
        # Calculate averages
        for intervention in patterns:
            patterns[intervention]['avg_improvement'] /= patterns[intervention]['count']
            
            # Calculate optimal ranges
            for metric in ['engagement', 'attention', 'retention']:
                values = patterns[intervention]['initial_ranges'][metric]
                patterns[intervention]['initial_ranges'][metric] = {
                    'min': min(values),
                    'max': max(values),
                    'mean': np.mean(values)
                }
        
        # Cache
        with open(cache_file, 'wb') as f:
            pickle.dump(patterns, f)
        
        return patterns
    
    def semantic_search(self, query: str, top_k: int = 5, category: str = None) -> List[Dict]:
        """Perform semantic search across vector database"""
        query_embedding = self._create_embedding(query)
        
        results = []
        
        # Search in specified category or all
        categories = [category] if category else ['practices', 'research', 'interventions', 'scenarios']
        
        for cat in categories:
            if cat not in self.vector_db:
                continue
                
            for item in self.vector_db[cat]:
                similarity = cosine_similarity(
                    query_embedding.reshape(1, -1),
                    item['embedding'].reshape(1, -1)
                )[0][0]
                
                results.append({
                    'category': cat,
                    'similarity': float(similarity),
                    'data': item['data'],
                    'id': item['id']
                })
        
        # Sort and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def find_similar_scenarios(self, metrics: Dict[str, float], top_k: int = 3) -> List[Dict]:
        """Find similar teaching scenarios from training data"""
        # Create metric vector
        metric_vector = np.array([
            metrics.get('avg_engagement', 0),
            metrics.get('avg_attention', 0),
            metrics.get('retention_score', 0),
            metrics.get('curiosity_index', 0),
            metrics.get('words_per_minute', 150) / 200,  # Normalize
            metrics.get('questions_detected', 0),
            metrics.get('interaction_rate', 0)
        ]).reshape(1, -1)
        
        similarities = []
        
        for _, row in self.training_scenarios.iterrows():
            scenario_vector = np.array([
                row['avg_engagement'],
                row['avg_attention'],
                row['retention_score'],
                row['curiosity_index'],
                row['words_per_minute'] / 200,
                row['questions_detected'],
                row['interaction_rate']
            ]).reshape(1, -1)
            
            similarity = cosine_similarity(metric_vector, scenario_vector)[0][0]
            
            similarities.append({
                'scenario_id': row['scenario_id'],
                'similarity': float(similarity),
                'outcome': row['outcome'],
                'recommendations': row['recommendations'],
                'metrics': {
                    'engagement': row['avg_engagement'],
                    'attention': row['avg_attention'],
                    'retention': row['retention_score']
                }
            })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def predict_intervention_success(self, metrics: Dict[str, float], intervention: str) -> Dict:
        """Predict success probability of an intervention"""
        if intervention not in self.pattern_matcher:
            return {'success_probability': 0.5, 'confidence': 'low', 'expected_improvement': 'unknown'}
        
        pattern = self.pattern_matcher[intervention]
        
        # Check if metrics fall within successful range
        in_range_count = 0
        total_checks = 0
        
        for metric in ['engagement', 'attention', 'retention']:
            if metric in metrics:
                metric_key = f'avg_{metric}' if metric != 'retention' else 'retention_score'
                value = metrics.get(metric_key, 0)
                
                range_data = pattern['initial_ranges'][metric]
                if range_data['min'] <= value <= range_data['max']:
                    in_range_count += 1
                total_checks += 1
        
        # Calculate success probability
        range_match = in_range_count / total_checks if total_checks > 0 else 0.5
        
        # Weight by historical success
        total_attempts = pattern['count']
        high_success = pattern['success_rates'].get('high', 0) + pattern['success_rates'].get('very_high', 0)
        success_rate = high_success / total_attempts if total_attempts > 0 else 0.5
        
        # Combined probability
        success_prob = (range_match * 0.6 + success_rate * 0.4)
        
        confidence = 'high' if total_attempts >= 5 else 'medium' if total_attempts >= 3 else 'low'
        
        return {
            'success_probability': round(success_prob, 2),
            'confidence': confidence,
            'expected_improvement': f"{pattern['avg_improvement']:.1f}%",
            'historical_attempts': total_attempts,
            'recommendation': 'highly_recommended' if success_prob > 0.7 else 'recommended' if success_prob > 0.5 else 'consider_alternatives'
        }
    
    def generate_smart_recommendations(self, metrics: Dict[str, Any], subject: str = "general") -> Dict:
        """Generate intelligent recommendations using RAG + ML"""
        
        # Find similar scenarios
        similar_scenarios = self.find_similar_scenarios(metrics, top_k=3)
        
        # Identify issues
        issues = self._identify_issues(metrics)
        
        # Generate recommendations for each issue
        recommendations = {
            'immediate_actions': [],
            'short_term_strategies': [],
            'long_term_strategies': [],
            'similar_cases': similar_scenarios,
            'intervention_predictions': [],
            'personalized_insights': []
        }
        
        for issue in issues:
            # Semantic search for solutions
            query = f"improve {issue['metric']} increase {issue['metric']} low {issue['metric']}"
            solutions = self.semantic_search(query, top_k=3)
            
            # Get intervention
            intervention_key = self._get_intervention_key(issue)
            intervention_data = self._find_intervention(intervention_key)
            
            if intervention_data:
                # Predict success
                for action in intervention_data['immediate_actions'][:2]:
                    intervention_name = action.lower().replace(' ', '_')[:30]
                    prediction = self.predict_intervention_success(metrics, intervention_name)
                    
                    recommendations['immediate_actions'].append({
                        'action': action,
                        'for_issue': issue['metric'],
                        'severity': issue['severity'],
                        'success_prediction': prediction
                    })
                
                for strategy in intervention_data['short_term_strategies'][:2]:
                    recommendations['short_term_strategies'].append({
                        'strategy': strategy,
                        'for_issue': issue['metric']
                    })
            
            # Add research-backed solutions
            for solution in solutions:
                if solution['category'] == 'research':
                    recommendations['personalized_insights'].append({
                        'insight': solution['data']['finding'],
                        'action': solution['data']['recommendation'],
                        'relevance': solution['similarity']
                    })
        
        # Add insights from similar scenarios
        for scenario in similar_scenarios[:2]:
            recommendations['personalized_insights'].append({
                'insight': f"Teachers with similar metrics ({scenario['outcome']}) found success with: {scenario['recommendations']}",
                'similarity': scenario['similarity']
            })
        
        return recommendations
    
    def _identify_issues(self, metrics: Dict) -> List[Dict]:
        """Identify issues from metrics"""
        issues = []
        
        if metrics.get('avg_engagement', 100) < 50:
            issues.append({'metric': 'engagement', 'severity': 'critical', 'value': metrics.get('avg_engagement', 0)})
        elif metrics.get('avg_engagement', 100) < 70:
            issues.append({'metric': 'engagement', 'severity': 'medium', 'value': metrics.get('avg_engagement', 0)})
        
        if metrics.get('avg_attention', 100) < 45:
            issues.append({'metric': 'attention', 'severity': 'critical', 'value': metrics.get('avg_attention', 0)})
        elif metrics.get('avg_attention', 100) < 65:
            issues.append({'metric': 'attention', 'severity': 'medium', 'value': metrics.get('avg_attention', 0)})
        
        if metrics.get('retention_score', 100) < 50:
            issues.append({'metric': 'retention', 'severity': 'critical', 'value': metrics.get('retention_score', 0)})
        
        if metrics.get('curiosity_index', 100) < 40:
            issues.append({'metric': 'curiosity', 'severity': 'high', 'value': metrics.get('curiosity_index', 0)})
        
        wpm = metrics.get('words_per_minute', 150)
        if wpm > 180:
            issues.append({'metric': 'pacing', 'severity': 'medium', 'value': wpm, 'issue': 'too_fast'})
        elif wpm < 120:
            issues.append({'metric': 'pacing', 'severity': 'medium', 'value': wpm, 'issue': 'too_slow'})
        
        if metrics.get('interaction_rate', 100) < 30:
            issues.append({'metric': 'interaction', 'severity': 'high', 'value': metrics.get('interaction_rate', 0)})
        
        return issues
    
    def _get_intervention_key(self, issue: Dict) -> str:
        """Get intervention key from issue"""
        metric = issue['metric']
        if metric == 'pacing':
            return f"int_pacing_{issue.get('issue', 'too_fast')}"
        return f"int_low_{metric}"
    
    def _find_intervention(self, key: str) -> Dict:
        """Find intervention by key"""
        for item in self.interventions['interventions']:
            if item['id'] == key:
                return item
        return None


if __name__ == "__main__":
    # Test the advanced RAG engine
    rag = AdvancedRAGEngine()
    
    sample_metrics = {
        'avg_engagement': 45,
        'avg_attention': 40,
        'retention_score': 48,
        'curiosity_index': 35,
        'words_per_minute': 195,
        'questions_detected': 8,
        'interaction_rate': 25
    }
    
    print("=" * 80)
    print("ADVANCED RAG ENGINE TEST")
    print("=" * 80)
    
    # Test semantic search
    print("\n1. Semantic Search for 'improve engagement':")
    results = rag.semantic_search("improve engagement increase student participation", top_k=3)
    for i, r in enumerate(results, 1):
        print(f"   {i}. [{r['category']}] Similarity: {r['similarity']:.3f}")
    
    # Test similar scenarios
    print("\n2. Similar Teaching Scenarios:")
    scenarios = rag.find_similar_scenarios(sample_metrics, top_k=3)
    for i, s in enumerate(scenarios, 1):
        print(f"   {i}. {s['scenario_id']} - Outcome: {s['outcome']} (Similarity: {s['similarity']:.3f})")
    
    # Test smart recommendations
    print("\n3. Smart Recommendations:")
    recs = rag.generate_smart_recommendations(sample_metrics)
    print(f"   Immediate Actions: {len(recs['immediate_actions'])}")
    print(f"   Personalized Insights: {len(recs['personalized_insights'])}")
    
    print("\n" + "=" * 80)
