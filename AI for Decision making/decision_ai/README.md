# AI Decision Making System

This system analyzes student engagement, attention, interaction, and teaching quality to provide personalized tips and actionable decisions.

## Files Overview

1. **data_loader.py** - Loads data from CSV files (video analyzer, voice analysis, feedback)
2. **engagement_analyzer.py** - Analyzes student engagement metrics
3. **attention_analyzer.py** - Analyzes student attention patterns
4. **interaction_analyzer.py** - Analyzes student-teacher interactions
5. **teaching_quality_analyzer.py** - Evaluates teaching effectiveness
6. **decision_maker.py** - Makes actionable decisions based on analyses
7. **personalized_tips_generator.py** - Generates personalized tips for teachers
8. **main_analyzer.py** - Runs all analyses and displays comprehensive results

## Data Sources

- **AI Video Analyzer**: `accurate_report.csv` - Student engagement, attention, hand raises
- **AI Voice Analysis**: `analysis_results.csv` - Speech analysis, sentiment, questions
- **Feedback Form**: `feedback.csv` - Student feedback on lessons

## Usage

### Run Individual Analyzers
```bash
python engagement_analyzer.py
python attention_analyzer.py
python interaction_analyzer.py
python teaching_quality_analyzer.py
```

### Run Decision Maker
```bash
python decision_maker.py
```

### Generate Personalized Tips
```bash
python personalized_tips_generator.py
```

### Run Complete Analysis
```bash
python main_analyzer.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Key Metrics

- **Engagement Score**: Student participation and involvement
- **Attention Score**: Student focus and concentration
- **Hand Raises**: Active participation indicators
- **Words Per Minute**: Teaching pace
- **Sentiment**: Classroom atmosphere
- **Teacher Impact Score**: Teaching effectiveness
- **Curiosity Index**: Student interest level
