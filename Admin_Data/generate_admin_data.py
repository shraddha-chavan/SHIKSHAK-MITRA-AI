import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Generate teacher performance data
teachers = [
    {"id": "T001", "name": "Dr. Sarah Smith", "subject": "Mathematics", "experience": 8},
    {"id": "T002", "name": "Prof. John Wilson", "subject": "Science", "experience": 12},
    {"id": "T003", "name": "Ms. Emily Davis", "subject": "English", "experience": 6},
    {"id": "T004", "name": "Mr. Michael Brown", "subject": "History", "experience": 10},
    {"id": "T005", "name": "Dr. Lisa Johnson", "subject": "Physics", "experience": 15},
    {"id": "T006", "name": "Ms. Anna Garcia", "subject": "Chemistry", "experience": 7},
    {"id": "T007", "name": "Mr. David Lee", "subject": "Biology", "experience": 9},
    {"id": "T008", "name": "Prof. Maria Rodriguez", "subject": "Literature", "experience": 11}
]

# Generate teacher performance metrics
teacher_performance = []
for teacher in teachers:
    base_score = 70 + teacher["experience"] * 1.5 + random.randint(-10, 15)
    
    performance = {
        "teacher_id": teacher["id"],
        "teacher_name": teacher["name"],
        "subject": teacher["subject"],
        "experience_years": teacher["experience"],
        "overall_engagement": min(95, max(60, base_score + random.randint(-5, 10))),
        "attention_score": min(95, max(55, base_score + random.randint(-8, 8))),
        "participation_score": min(95, max(50, base_score + random.randint(-10, 12))),
        "comprehension_score": min(95, max(65, base_score + random.randint(-7, 7))),
        "teacher_effectiveness": min(95, max(60, base_score + random.randint(-6, 9))),
        "student_feedback_rating": round(3.0 + (base_score - 70) * 0.02 + random.uniform(-0.3, 0.5), 1),
        "classes_taught": random.randint(15, 35),
        "total_students": random.randint(180, 420),
        "improvement_trend": random.choice(["Improving", "Stable", "Declining"]),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    teacher_performance.append(performance)

# Save teacher performance
df_teachers = pd.DataFrame(teacher_performance)
df_teachers.to_csv("Admin_Data/Teachers/teacher_performance.csv", index=False)

# Generate live monitoring data
live_classes = []
for i, teacher in enumerate(teachers[:5]):  # 5 active classes
    live_class = {
        "class_id": f"CLS_{i+1:03d}",
        "teacher_id": teacher["id"],
        "teacher_name": teacher["name"],
        "subject": teacher["subject"],
        "class_section": f"{random.randint(9, 12)}-{random.choice(['A', 'B', 'C'])}",
        "current_engagement": random.randint(65, 92),
        "current_attention": random.randint(70, 88),
        "student_count": random.randint(25, 35),
        "hand_raises": random.randint(2, 12),
        "confusion_level": random.randint(5, 25),
        "class_duration": random.randint(35, 50),
        "status": "Live",
        "start_time": (datetime.now() - timedelta(minutes=random.randint(10, 45))).strftime("%H:%M"),
        "tis_pulse": random.choice(["green", "yellow", "red"])
    }
    live_classes.append(live_class)

df_live = pd.DataFrame(live_classes)
df_live.to_csv("Admin_Data/live_monitoring.csv", index=False)

# Generate comparison reports
comparison_data = []
for teacher in teachers:
    comparison = {
        "teacher_id": teacher["id"],
        "teacher_name": teacher["name"],
        "subject": teacher["subject"],
        "engagement_avg": random.randint(70, 92),
        "attention_avg": random.randint(68, 89),
        "participation_avg": random.randint(65, 88),
        "effectiveness_score": random.randint(72, 94),
        "student_satisfaction": round(random.uniform(3.5, 4.8), 1),
        "improvement_rate": round(random.uniform(-2.5, 8.3), 1),
        "benchmark_rank": random.randint(1, len(teachers)),
        "strengths": random.choice([
            "Interactive teaching methods",
            "Clear explanations",
            "Student engagement",
            "Technology integration",
            "Assessment techniques"
        ]),
        "improvement_areas": random.choice([
            "Pace management",
            "Student participation",
            "Technology usage",
            "Assessment frequency",
            "Individual attention"
        ])
    }
    comparison_data.append(comparison)

df_comparison = pd.DataFrame(comparison_data)
df_comparison.to_csv("Admin_Data/Reports/teacher_comparison.csv", index=False)

# Generate industry alignment data
industry_alignment = []
industry_alignment_data = {
    "Mathematics": ["Data Science", "Engineering", "Finance", "Research"],
    "Science": ["Healthcare", "Research", "Technology", "Environment"],
    "English": ["Media", "Publishing", "Education", "Communications"],
    "History": ["Government", "Education", "Research", "Museums"],
    "Physics": ["Engineering", "Research", "Technology", "Energy"],
    "Chemistry": ["Pharmaceuticals", "Research", "Manufacturing", "Environment"],
    "Biology": ["Healthcare", "Research", "Biotechnology", "Environment"],
    "Literature": ["Publishing", "Media", "Education", "Arts"]
}

for teacher in teachers:
    industries = industry_alignment_data.get(teacher["subject"], ["General"])
    alignment = {
        "teacher_id": teacher["id"],
        "teacher_name": teacher["name"],
        "subject": teacher["subject"],
        "primary_industry": industries[0],
        "alignment_score": random.randint(75, 95),
        "skill_relevance": random.randint(70, 90),
        "curriculum_match": random.randint(80, 95),
        "industry_feedback": round(random.uniform(4.0, 4.9), 1),
        "certification_level": random.choice(["Basic", "Intermediate", "Advanced", "Expert"]),
        "last_industry_update": (datetime.now() - timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d")
    }
    industry_alignment.append(alignment)

df_industry = pd.DataFrame(industry_alignment)
df_industry.to_csv("Admin_Data/Reports/industry_alignment.csv", index=False)

# Generate management dashboard summary
dashboard_summary = {
    "total_teachers": len(teachers),
    "active_classes": len(live_classes),
    "avg_engagement": round(df_teachers["overall_engagement"].mean(), 1),
    "avg_effectiveness": round(df_teachers["teacher_effectiveness"].mean(), 1),
    "top_performer": df_teachers.loc[df_teachers["teacher_effectiveness"].idxmax(), "teacher_name"],
    "improvement_needed": len(df_teachers[df_teachers["improvement_trend"] == "Declining"]),
    "total_students": df_teachers["total_students"].sum(),
    "avg_student_rating": round(df_teachers["student_feedback_rating"].mean(), 1),
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

df_summary = pd.DataFrame([dashboard_summary])
df_summary.to_csv("Admin_Data/Reports/dashboard_summary.csv", index=False)

print("Admin data generated successfully!")
print(f"Teachers: {len(teachers)}")
print(f"Live Classes: {len(live_classes)}")
print(f"Reports: 4 files created")
print(f"Location: Admin_Data/")