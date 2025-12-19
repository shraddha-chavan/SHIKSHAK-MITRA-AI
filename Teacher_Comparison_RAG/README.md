# 🎓 Teacher Comparison RAG System

## Overview

AI-powered system to **compare teachers** and find the **best fit for specific subjects** using RAG (Retrieval-Augmented Generation).

## 🎯 Features

- **Subject Fit Analysis** - Calculate how well teachers match subject requirements
- **Side-by-Side Comparison** - Compare multiple teachers for a subject
- **AI Recommendations** - Get best teacher suggestions based on data
- **Student Feedback Integration** - Real feedback analysis
- **Multi-Subject Analysis** - Compare across multiple subjects
- **Top Performers Ranking** - Find overall best teachers

## 📊 Data Files (3 CSV Files)

1. **teachers_profile.csv** - 15 teachers with profiles
   - Name, subject, scores, experience, teaching style, specialization

2. **student_feedback.csv** - 33 feedback entries
   - Ratings, clarity, engagement, helpfulness, comments

3. **subject_requirements.csv** - 12 subjects
   - Required skills, teaching style, difficulty, topics

## 🚀 Quick Start

```bash
cd Teacher_Comparison_RAG
pip install -r requirements.txt
python teacher_comparison_rag.py
```

## 📈 Output Examples

### Teacher Comparison Table
```
Teacher                   Subject              Impact   Retention  Engagement   Subject Fit  Experience
Dr. Priya Sharma         Computer Science     94       95%        92%          98%          12 years
Prof. Neha Kapoor        Computer Science     92       93%        90%          96%          8 years
Ms. Kavita Joshi         Computer Science     93       94%        91%          94%          6 years
```

### AI Recommendations
```
✨ Best Fit for AI/ML Course

   🏆 Dr. Priya Sharma
   ──────────────────────────────────────────────────
   Subject Fit Score: 98%
   Impact Score: 94
   Retention: 95%
   Engagement: 92%
   Experience: 12 years
   Teaching Style: Interactive, Project-based
   Specialization: AI, Machine Learning, Data Science
   
   📝 Student Feedback (Avg Rating: 4.7/5)
      1. "Excellent teacher! Makes complex AI concepts easy to understand"
      2. "Great at explaining machine learning algorithms"
```

## 🧠 How It Works

### Subject Fit Calculation (100%)
- **Subject Match (40%)** - Specialization alignment
- **Teaching Style (30%)** - Style compatibility
- **Experience (15%)** - Years of teaching
- **Performance (15%)** - Impact, retention, engagement scores

### RAG Components
1. **Retrieval** - Fetch teacher profiles and feedback
2. **Augmentation** - Calculate fit scores and aggregate data
3. **Generation** - Create recommendations and comparisons

## 💻 Usage

### Compare for Specific Subject
```python
from teacher_comparison_rag import TeacherComparisonRAG

rag = TeacherComparisonRAG()
rag.display_comparison("AI/ML Course")
```

### Multi-Subject Comparison
```python
rag.compare_multiple_subjects([
    "AI/ML Course",
    "Advanced Mathematics",
    "Data Science"
])
```

### Find Top Performers
```python
rag.find_best_teacher_overall()
```

## 📊 Analysis Features

### 1. Subject Fit Analysis
- Matches teacher expertise with subject requirements
- Considers teaching style compatibility
- Factors in experience and performance

### 2. Student Feedback Integration
- Aggregates ratings across multiple dimensions
- Extracts top positive feedback
- Calculates average scores

### 3. Comparative Analysis
- Side-by-side comparison table
- Ranking by subject fit
- Multiple recommendation tiers

### 4. Multi-Subject Overview
- Best teacher for each subject
- Cross-subject performance
- Overall rankings

## 🎯 Use Cases

1. **Course Assignment** - Assign teachers to new courses
2. **Hiring Decisions** - Evaluate candidates for positions
3. **Performance Review** - Compare teacher effectiveness
4. **Subject Planning** - Plan course offerings based on teacher strengths
5. **Professional Development** - Identify training needs

## 📈 Metrics Explained

- **Impact Score** - Overall teaching effectiveness (0-100)
- **Retention** - Student retention rate (%)
- **Engagement** - Student engagement level (%)
- **Subject Fit** - How well teacher matches subject (%)
- **Experience** - Years of teaching experience

## 🔧 Customization

### Add New Teachers
Edit `teachers_profile.csv`:
```csv
T016,New Teacher,Subject,90,91,89,10,"Qualifications","Style","Specialization"
```

### Add Feedback
Edit `student_feedback.csv`:
```csv
T016,S034,Subject,5,5,5,5,5,5,"Great teacher!"
```

### Add Subjects
Edit `subject_requirements.csv`:
```csv
New Subject,"Skills","Style",Level,Student Level,"Topics"
```

## 📊 Sample Subjects Included

1. AI/ML Course
2. Advanced Mathematics
3. Quantum Physics
4. Data Science
5. Web Development
6. Organic Chemistry
7. Genetics
8. Microeconomics
9. Ancient History
10. Creative Writing
11. Cloud Computing
12. Biotechnology

## 🎓 Sample Teachers Included

- Dr. Priya Sharma (Computer Science - AI/ML)
- Prof. Rajesh Kumar (Mathematics)
- Ms. Anita Desai (Physics)
- Dr. Amit Patel (Chemistry)
- Prof. Sunita Reddy (Biology)
- And 10 more...

## 🚀 Integration

### With RAG System
```python
# Get teacher recommendations
from Teacher_Comparison_RAG.teacher_comparison_rag import TeacherComparisonRAG

rag = TeacherComparisonRAG()
recommendations = rag.compare_teachers("AI/ML Course", top_n=3)
```

### With Existing System
```python
# Use in your application
rag = TeacherComparisonRAG()
best_teacher = rag.compare_teachers(subject_name, top_n=1)
```

## 📈 Output Format

All results displayed in terminal with:
- ✅ Formatted tables
- 🎯 Clear recommendations
- 📊 Comparative metrics
- 💬 Student feedback quotes
- 🏆 Rankings and scores

## 🎉 What You Get

✅ **3 CSV databases** with real data
✅ **RAG-based analysis** engine
✅ **Subject fit calculation** algorithm
✅ **Student feedback** integration
✅ **Multi-dimensional** comparison
✅ **AI recommendations** with reasoning
✅ **Beautiful terminal** output
✅ **Easy to extend** and customize

## 🔍 Example Output

```
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                              TEACHER COMPARISON RAG SYSTEM                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

====================================================================================================
  🎓 TEACHER COMPARISON - AI/ML COURSE
====================================================================================================

📋 Subject Requirements:
   Difficulty: Advanced
   Student Level: Graduate
   Required Skills: Python, Machine Learning, Deep Learning, Statistics
   Preferred Style: Interactive, Project-based, Hands-on
   Key Topics: Neural Networks, NLP, Computer Vision, Model Training

====================================================================================================
📊 TEACHER COMPARISON TABLE
====================================================================================================
Teacher                   Subject              Impact   Retention  Engagement   Subject Fit  Experience
----------------------------------------------------------------------------------------------------
Dr. Priya Sharma         Computer Science     94       95%        92%          98%          12 years
Prof. Neha Kapoor        Computer Science     92       93%        90%          96%          8 years
Ms. Kavita Joshi         Computer Science     93       94%        91%          94%          6 years

====================================================================================================
🤖 AI RECOMMENDATIONS
====================================================================================================

✨ Best Fit for AI/ML Course
   Based on technical background, teaching style, and student feedback analysis

   🏆 Dr. Priya Sharma
   ──────────────────────────────────────────────────
   Subject Fit Score: 98%
   Impact Score: 94
   Retention: 95%
   Engagement: 92%
   Experience: 12 years
   Teaching Style: Interactive, Project-based
   Specialization: AI, Machine Learning, Data Science

   📝 Student Feedback (Avg Rating: 4.7/5)
      1. "Excellent teacher! Makes complex AI concepts easy to understand"
      2. "Great at explaining machine learning algorithms"

   🥈 Alternative Recommendation
   ──────────────────────────────────────────────────
   Prof. Neha Kapoor
   Subject Fit Score: 96%
   Theory + Practice, Innovative approach with 8 years

====================================================================================================
```

---

**Find the Right Teacher for the Right Subject!** 🎓✨
