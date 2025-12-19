import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import pickle
import os

class RAGEngine:
    """
    Retrieval-Augmented Generation Engine for Shikshak Mitra AI
    Combines teacher analytics with educational research knowledge base
    """
    
    def __init__(self, knowledge_base_path: str = None):
        if knowledge_base_path is None:
            knowledge_base_path = Path(__file__).parent / "knowledge_base"
        
        self.kb_path = Path(knowledge_base_path)
        self.cache_path = Path(__file__).parent / "cache"
        self.cache_path.mkdir(exist_ok=True)
        
        # Load all knowledge bases
        self.teaching_practices = self._load_json("teaching_best_practices.json")
        self.research = self._load_json("educational_research.json")
        self.interventions = self._load_json("intervention_strategies.json")
        self.subject_strategies = self._load_json("subject_specific_strategies.json")
        
        # Create embeddings cache
        self.embeddings_cache = self._load_or_create_embeddings()
    
    def _load_json(self, filename: str) -> Dict:
        """Load JSON knowledge base file"""
        with open(self.kb_path / filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """Create simple word-based embedding (can be replaced with sentence-transformers)"""
        # Simple bag-of-words style embedding
        words = text.lower().split()
        # Create a simple hash-based embedding
        embedding = np.zeros(128)
        for word in words:
            hash_val = hash(word) % 128
            embedding[hash_val] += 1
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding
    
    def _load_or_create_embeddings(self) -> Dict:
        """Load cached embeddings or create new ones"""
        cache_file = self.cache_path / "embeddings_cache.pkl"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        # Create embeddings for all knowledge base items
        embeddings = {}
        
        # Embed teaching practices
        for category in ['engagement_strategies', 'attention_strategies', 
                        'interaction_strategies', 'sentiment_strategies', 'retention_strategies']:
            for item in self.teaching_practices.get(category, []):
                key = item['id']
                text = f"{item['title']} {item['description']} {item.get('best_for', '')}"
                embeddings[key] = {
                    'embedding': self._simple_embedding(text),
                    'data': item,
                    'type': 'practice'
                }
        
        # Embed research findings
        for item in self.research.get('research_findings', []):
            key = item['id']
            text = f"{item['topic']} {item['finding']} {item['recommendation']}"
            embeddings[key] = {
                'embedding': self._simple_embedding(text),
                'data': item,
                'type': 'research'
            }
        
        # Embed interventions
        for item in self.interventions.get('interventions', []):
            key = item['id']
            text = f"{item['problem']} {' '.join(item['immediate_actions'])}"
            embeddings[key] = {
                'embedding': self._simple_embedding(text),
                'data': item,
                'type': 'intervention'
            }
        
        # Cache embeddings
        with open(cache_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)
    
    def retrieve_relevant_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve most relevant knowledge base items for a query"""
        query_embedding = self._simple_embedding(query)
        
        # Calculate similarities
        similarities = []
        for key, item in self.embeddings_cache.items():
            similarity = self._cosine_similarity(query_embedding, item['embedding'])
            similarities.append({
                'key': key,
                'similarity': similarity,
                'data': item['data'],
                'type': item['type']
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def analyze_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze teacher metrics and identify issues"""
        issues = []
        benchmarks = self.research['benchmarks']
        
        # Check engagement
        engagement = metrics.get('avg_engagement', 0)
        if engagement < 50:
            issues.append({
                'metric': 'engagement',
                'severity': 'critical',
                'value': engagement,
                'benchmark': benchmarks['engagement_score']
            })
        elif engagement < 70:
            issues.append({
                'metric': 'engagement',
                'severity': 'medium',
                'value': engagement,
                'benchmark': benchmarks['engagement_score']
            })
        
        # Check attention
        attention = metrics.get('avg_attention', 0)
        if attention < 45:
            issues.append({
                'metric': 'attention',
                'severity': 'critical',
                'value': attention,
                'benchmark': benchmarks['attention_score']
            })
        elif attention < 65:
            issues.append({
                'metric': 'attention',
                'severity': 'medium',
                'value': attention,
                'benchmark': benchmarks['attention_score']
            })
        
        # Check retention
        retention = metrics.get('retention_score', 0)
        if retention < 50:
            issues.append({
                'metric': 'retention',
                'severity': 'critical',
                'value': retention,
                'benchmark': benchmarks['retention_score']
            })
        elif retention < 65:
            issues.append({
                'metric': 'retention',
                'severity': 'medium',
                'value': retention,
                'benchmark': benchmarks['retention_score']
            })
        
        # Check curiosity
        curiosity = metrics.get('curiosity_index', 0)
        if curiosity < 40:
            issues.append({
                'metric': 'curiosity',
                'severity': 'high',
                'value': curiosity,
                'benchmark': benchmarks['curiosity_index']
            })
        elif curiosity < 60:
            issues.append({
                'metric': 'curiosity',
                'severity': 'medium',
                'value': curiosity,
                'benchmark': benchmarks['curiosity_index']
            })
        
        # Check pacing
        wpm = metrics.get('words_per_minute', 150)
        if wpm < 120:
            issues.append({
                'metric': 'pacing',
                'severity': 'medium',
                'value': wpm,
                'issue': 'too_slow',
                'benchmark': benchmarks['words_per_minute']
            })
        elif wpm > 180:
            issues.append({
                'metric': 'pacing',
                'severity': 'medium',
                'value': wpm,
                'issue': 'too_fast',
                'benchmark': benchmarks['words_per_minute']
            })
        
        # Check questions
        questions = metrics.get('questions_detected', 0)
        if questions < 10:
            issues.append({
                'metric': 'questions',
                'severity': 'medium',
                'value': questions,
                'benchmark': benchmarks['questions_per_class']
            })
        
        # Check interaction rate
        interaction = metrics.get('interaction_rate', 0)
        if interaction < 30:
            issues.append({
                'metric': 'interaction',
                'severity': 'high',
                'value': interaction,
                'benchmark': benchmarks['interaction_rate']
            })
        elif interaction < 50:
            issues.append({
                'metric': 'interaction',
                'severity': 'medium',
                'value': interaction,
                'benchmark': benchmarks['interaction_rate']
            })
        
        return {
            'issues': issues,
            'total_issues': len(issues),
            'critical_count': len([i for i in issues if i['severity'] == 'critical']),
            'high_count': len([i for i in issues if i['severity'] == 'high']),
            'medium_count': len([i for i in issues if i['severity'] == 'medium'])
        }
    
    def generate_recommendations(self, metrics: Dict[str, Any], subject: str = "general") -> Dict[str, Any]:
        """Generate AI-powered recommendations using RAG"""
        
        # Analyze metrics to identify issues
        analysis = self.analyze_metrics(metrics)
        
        recommendations = {
            'immediate_actions': [],
            'short_term_strategies': [],
            'long_term_strategies': [],
            'research_backed': [],
            'subject_specific': [],
            'expected_outcomes': []
        }
        
        # For each issue, retrieve relevant knowledge
        for issue in analysis['issues']:
            metric = issue['metric']
            severity = issue['severity']
            
            # Build query for retrieval
            query = f"improve {metric} low {metric} increase {metric}"
            relevant_knowledge = self.retrieve_relevant_knowledge(query, top_k=3)
            
            # Find matching intervention
            intervention_key = f"int_low_{metric}"
            if metric == 'pacing':
                if issue.get('issue') == 'too_fast':
                    intervention_key = "int_pacing_too_fast"
                else:
                    intervention_key = "int_pacing_too_slow"
            elif metric == 'questions':
                intervention_key = "int_few_questions"
            
            # Get intervention if exists
            intervention = None
            for item in self.interventions['interventions']:
                if item['id'] == intervention_key:
                    intervention = item
                    break
            
            if intervention:
                # Add immediate actions
                for action in intervention['immediate_actions'][:2]:
                    recommendations['immediate_actions'].append({
                        'action': action,
                        'for_issue': metric,
                        'severity': severity
                    })
                
                # Add short-term strategies
                for strategy in intervention['short_term_strategies'][:2]:
                    recommendations['short_term_strategies'].append({
                        'strategy': strategy,
                        'for_issue': metric,
                        'timeframe': '1-3 classes'
                    })
                
                # Add long-term strategies
                for strategy in intervention['long_term_strategies'][:1]:
                    recommendations['long_term_strategies'].append({
                        'strategy': strategy,
                        'for_issue': metric,
                        'timeframe': '3-8 weeks'
                    })
                
                # Add expected improvement
                recommendations['expected_outcomes'].append({
                    'metric': metric,
                    'expected_improvement': intervention['expected_improvement']
                })
            
            # Add research-backed recommendations
            for knowledge in relevant_knowledge:
                if knowledge['type'] == 'research':
                    recommendations['research_backed'].append({
                        'finding': knowledge['data']['finding'],
                        'recommendation': knowledge['data']['recommendation'],
                        'source': knowledge['data']['source'],
                        'for_issue': metric
                    })
                elif knowledge['type'] == 'practice':
                    recommendations['short_term_strategies'].append({
                        'strategy': knowledge['data']['title'] + ": " + knowledge['data']['implementation'],
                        'for_issue': metric,
                        'expected_boost': knowledge['data'].get(f"{metric}_boost", "N/A")
                    })
        
        # Add subject-specific strategies
        if subject in self.subject_strategies:
            subject_data = self.subject_strategies[subject]
            recommendations['subject_specific'] = {
                'engagement_strategies': subject_data.get('engagement_strategies', [])[:3],
                'optimal_wpm': subject_data.get('optimal_wpm', '130-150'),
                'question_types': subject_data.get('question_types', [])[:3],
                'retention_boosters': subject_data.get('retention_boosters', [])[:3]
            }
        
        # Remove duplicates
        recommendations['immediate_actions'] = self._remove_duplicates(recommendations['immediate_actions'])
        recommendations['short_term_strategies'] = self._remove_duplicates(recommendations['short_term_strategies'])
        recommendations['research_backed'] = self._remove_duplicates(recommendations['research_backed'])
        
        return {
            'analysis': analysis,
            'recommendations': recommendations,
            'priority_order': self._prioritize_recommendations(analysis, recommendations)
        }
    
    def _remove_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Remove duplicate recommendations"""
        seen = set()
        unique = []
        for item in items:
            # Create a simple key from the item
            key = str(item.get('action', item.get('strategy', item.get('finding', ''))))[:50]
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique
    
    def _prioritize_recommendations(self, analysis: Dict, recommendations: Dict) -> List[Dict]:
        """Prioritize recommendations based on severity and impact"""
        priority = []
        
        # Critical issues first
        for issue in analysis['issues']:
            if issue['severity'] == 'critical':
                priority.append({
                    'priority': 1,
                    'metric': issue['metric'],
                    'message': f"CRITICAL: {issue['metric'].title()} is at {issue['value']}. Immediate intervention required.",
                    'actions': [a for a in recommendations['recommendations']['immediate_actions'] 
                               if a.get('for_issue') == issue['metric']][:2]
                })
        
        # High severity issues
        for issue in analysis['issues']:
            if issue['severity'] == 'high':
                priority.append({
                    'priority': 2,
                    'metric': issue['metric'],
                    'message': f"HIGH: {issue['metric'].title()} needs attention at {issue['value']}.",
                    'actions': [a for a in recommendations['recommendations']['immediate_actions'] 
                               if a.get('for_issue') == issue['metric']][:2]
                })
        
        # Medium severity issues
        for issue in analysis['issues']:
            if issue['severity'] == 'medium':
                priority.append({
                    'priority': 3,
                    'metric': issue['metric'],
                    'message': f"MEDIUM: {issue['metric'].title()} can be improved from {issue['value']}.",
                    'actions': [s for s in recommendations['recommendations']['short_term_strategies'] 
                               if s.get('for_issue') == issue['metric']][:2]
                })
        
        return priority
    
    def generate_detailed_report(self, metrics: Dict[str, Any], subject: str = "general") -> str:
        """Generate a detailed text report with recommendations"""
        result = self.generate_recommendations(metrics, subject)
        
        report = []
        report.append("=" * 80)
        report.append("SHIKSHAK MITRA AI - RAG-ENHANCED ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        analysis = result['analysis']
        report.append(f"Total Issues Identified: {analysis['total_issues']}")
        report.append(f"  - Critical: {analysis['critical_count']}")
        report.append(f"  - High: {analysis['high_count']}")
        report.append(f"  - Medium: {analysis['medium_count']}")
        report.append("")
        
        # Priority recommendations
        report.append("=" * 80)
        report.append("PRIORITY RECOMMENDATIONS")
        report.append("=" * 80)
        for item in result['priority_order']:
            report.append(f"\n[Priority {item['priority']}] {item['message']}")
            for action in item['actions']:
                report.append(f"  → {action.get('action', action.get('strategy', ''))}")
        
        # Immediate actions
        report.append("\n" + "=" * 80)
        report.append("IMMEDIATE ACTIONS (Next 5 minutes)")
        report.append("=" * 80)
        for i, action in enumerate(result['recommendations']['recommendations']['immediate_actions'][:5], 1):
            report.append(f"{i}. {action['action']}")
            report.append(f"   For: {action['for_issue'].title()} | Severity: {action['severity']}")
        
        # Short-term strategies
        report.append("\n" + "=" * 80)
        report.append("SHORT-TERM STRATEGIES (Next 1-3 classes)")
        report.append("=" * 80)
        for i, strategy in enumerate(result['recommendations']['recommendations']['short_term_strategies'][:5], 1):
            report.append(f"{i}. {strategy['strategy']}")
            if 'expected_boost' in strategy and strategy['expected_boost'] != "N/A":
                report.append(f"   Expected boost: {strategy['expected_boost']}%")
        
        # Research-backed recommendations
        if result['recommendations']['recommendations']['research_backed']:
            report.append("\n" + "=" * 80)
            report.append("RESEARCH-BACKED INSIGHTS")
            report.append("=" * 80)
            for i, research in enumerate(result['recommendations']['recommendations']['research_backed'][:3], 1):
                report.append(f"\n{i}. {research['finding']}")
                report.append(f"   Recommendation: {research['recommendation']}")
                report.append(f"   Source: {research['source']}")
        
        # Subject-specific
        if result['recommendations']['recommendations']['subject_specific']:
            report.append("\n" + "=" * 80)
            report.append(f"SUBJECT-SPECIFIC STRATEGIES ({subject.upper()})")
            report.append("=" * 80)
            subj = result['recommendations']['recommendations']['subject_specific']
            if 'engagement_strategies' in subj:
                report.append("\nEngagement Strategies:")
                for strategy in subj['engagement_strategies']:
                    report.append(f"  • {strategy}")
            if 'question_types' in subj:
                report.append("\nEffective Question Types:")
                for q in subj['question_types']:
                    report.append(f"  • {q}")
        
        # Expected outcomes
        report.append("\n" + "=" * 80)
        report.append("EXPECTED OUTCOMES")
        report.append("=" * 80)
        for outcome in result['recommendations']['recommendations']['expected_outcomes']:
            report.append(f"• {outcome['metric'].title()}: {outcome['expected_improvement']}")
        
        report.append("\n" + "=" * 80)
        report.append("Report generated by Shikshak Mitra AI RAG System")
        report.append("=" * 80)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Example usage
    rag = RAGEngine()
    
    # Sample metrics
    sample_metrics = {
        'avg_engagement': 45,
        'avg_attention': 40,
        'retention_score': 48,
        'curiosity_index': 35,
        'words_per_minute': 195,
        'questions_detected': 8,
        'interaction_rate': 25
    }
    
    # Generate report
    report = rag.generate_detailed_report(sample_metrics, subject="mathematics")
    print(report)
