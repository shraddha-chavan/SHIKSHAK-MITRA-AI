# 🚀 Quick Start Guide - Shikshak Mitra AI RAG System

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "d:\shikshak mitrs ai\RAG_System"
pip install -r requirements.txt
```

### Step 2: Run Demo
```bash
python demo.py
```

This will show you:
- ✅ Semantic search in action
- ✅ Similar scenario matching
- ✅ Intervention predictions
- ✅ Smart recommendations
- ✅ Excellent teacher analysis

### Step 3: Test RAG Engine
```bash
python advanced_rag_engine.py
```

### Step 4: Full Integration Test
```bash
python rag_integration.py
```

## 📝 Basic Usage Examples

### Example 1: Analyze Teacher Performance

```python
from advanced_rag_engine import AdvancedRAGEngine

# Initialize
rag = AdvancedRAGEngine()

# Your teacher's metrics
metrics = {
    'avg_engagement': 45,
    'avg_attention': 40,
    'retention_score': 48,
    'curiosity_index': 35,
    'words_per_minute': 195,
    'questions_detected': 8,
    'interaction_rate': 25
}

# Get smart recommendations
recommendations = rag.generate_smart_recommendations(metrics, subject="mathematics")

# Print immediate actions
for action in recommendations['immediate_actions']:
    print(f"Action: {action['action']}")
    print(f"Success Rate: {action['success_prediction']['success_probability']*100}%")
```

### Example 2: Search Knowledge Base

```python
from advanced_rag_engine import AdvancedRAGEngine

rag = AdvancedRAGEngine()

# Search for strategies
results = rag.semantic_search("improve student engagement", top_k=5)

for result in results:
    print(f"Strategy: {result['data']['title']}")
    print(f"Description: {result['data']['description']}")
```

### Example 3: Find Similar Teachers

```python
from advanced_rag_engine import AdvancedRAGEngine

rag = AdvancedRAGEngine()

metrics = {
    'avg_engagement': 45,
    'avg_attention': 40,
    'retention_score': 48
}

# Find similar cases
similar = rag.find_similar_scenarios(metrics, top_k=3)

for scenario in similar:
    print(f"Outcome: {scenario['outcome']}")
    print(f"What worked: {scenario['recommendations']}")
```

### Example 4: Predict Intervention Success

```python
from advanced_rag_engine import AdvancedRAGEngine

rag = AdvancedRAGEngine()

metrics = {
    'avg_engagement': 48,
    'avg_attention': 45,
    'retention_score': 50
}

# Predict success
prediction = rag.predict_intervention_success(
    metrics, 
    "slow_pace_increase_questions"
)

print(f"Success Probability: {prediction['success_probability']*100}%")
print(f"Expected Improvement: {prediction['expected_improvement']}")
print(f"Recommendation: {prediction['recommendation']}")
```

### Example 5: Full Integration with Your System

```python
from rag_integration import RAGIntegration

# Initialize
integration = RAGIntegration()

# Run complete analysis (uses your existing data)
result = integration.analyze_with_rag(subject="science")

# Get report
print(result['report'])

# Get metrics
print(result['metrics'])

# Get recommendations
print(result['recommendations'])
```

## 🎯 Common Use Cases

### Use Case 1: Daily Teacher Evaluation
```python
from rag_integration import RAGIntegration

integration = RAGIntegration()

# After each class
result = integration.analyze_with_rag(subject="mathematics")

# Results automatically saved to outputs/ folder
# - JSON file with all data
# - Text report for teacher
# - CSV history for tracking
```

### Use Case 2: Query Best Practices
```python
from rag_integration import RAGIntegration

integration = RAGIntegration()

# Ask questions
integration.query_knowledge_base("how to handle low attention students")
integration.query_knowledge_base("best questioning strategies")
integration.query_knowledge_base("improve retention in science class")
```

### Use Case 3: Compare Teachers
```python
from advanced_rag_engine import AdvancedRAGEngine

rag = AdvancedRAGEngine()

teacher1_metrics = {'avg_engagement': 45, 'avg_attention': 40, ...}
teacher2_metrics = {'avg_engagement': 85, 'avg_attention': 82, ...}

# Find what excellent teachers do
similar_excellent = rag.find_similar_scenarios(teacher2_metrics, top_k=3)

# Get recommendations for struggling teacher
recommendations = rag.generate_smart_recommendations(teacher1_metrics)
```

## 📊 Understanding the Output

### Metrics Explained
- **Engagement Score (0-100)**: Student participation and involvement
- **Attention Score (0-100)**: Student focus and concentration
- **Retention Score (0-100)**: How well students remember content
- **Curiosity Index (0-100)**: Student interest and question-asking
- **Teacher Impact Score (0-100)**: Overall teaching effectiveness
- **Words Per Minute**: Teaching pace (optimal: 130-160)
- **Questions Detected**: Number of questions asked (optimal: 15-20)
- **Interaction Rate (0-100)**: Percentage of students participating

### Severity Levels
- **CRITICAL**: Immediate intervention required (<50% engagement/attention)
- **HIGH**: Needs attention soon (<60 curiosity, <30% interaction)
- **MEDIUM**: Room for improvement (pacing, questions)

### Success Predictions
- **High Confidence**: Based on 5+ similar cases
- **Medium Confidence**: Based on 3-4 similar cases
- **Low Confidence**: Based on 1-2 similar cases

## 🔧 Troubleshooting

### Issue: "Module not found"
```bash
# Make sure you're in the right directory
cd "d:\shikshak mitrs ai\RAG_System"

# Install dependencies
pip install -r requirements.txt
```

### Issue: "File not found" errors
```bash
# Check knowledge base files exist
dir knowledge_base

# Should see:
# - teaching_best_practices.json
# - educational_research.json
# - intervention_strategies.json
# - subject_specific_strategies.json
# - training_data_scenarios.csv
# - teacher_feedback_corpus.csv
# - successful_interventions.csv
```

### Issue: Slow performance
```bash
# Delete cache to rebuild
rmdir /s cache
mkdir cache

# Run again - will rebuild optimized cache
python demo.py
```

### Issue: Integration errors
```python
# Check data_loader paths
# Edit rag_integration.py if needed
# Make sure paths point to your CSV files
```

## 📈 Next Steps

1. **Run the demo** to see capabilities
2. **Test with your data** using rag_integration.py
3. **Customize knowledge base** by editing JSON files
4. **Add your training data** to CSV files
5. **Integrate with your app** using the API

## 🎓 Learn More

- Read `README.md` for complete documentation
- Check `knowledge_base/` files to see training data
- Explore `advanced_rag_engine.py` for API details
- Review `rag_integration.py` for integration examples

## 💡 Tips

1. **Start with demo.py** - It shows all features
2. **Use semantic search** - Natural language queries work best
3. **Check similar scenarios** - Learn from similar teachers
4. **Trust the predictions** - Based on 40 real interventions
5. **Review outputs/** - All results saved automatically

## 🚀 Ready to Go!

```bash
# Quick test
python demo.py

# Full analysis
python rag_integration.py

# Custom query
python -c "from rag_integration import RAGIntegration; RAGIntegration().query_knowledge_base('your question here')"
```

---

**Need Help?** Check README.md or review the demo.py code for examples.

**Want to Customize?** Edit JSON files in knowledge_base/ folder.

**Ready for Production?** Use rag_integration.py in your main application.
