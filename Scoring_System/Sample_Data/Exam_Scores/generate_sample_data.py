import pandas as pd
import numpy as np
import random

# Generate sample data for 55 students, 4 subjects
np.random.seed(42)

students = [f"Student_{i:03d}" for i in range(1, 56)]
subjects = ["Mathematics", "Science", "English", "History"]

# Generate exam scores
data = []

for student in students:
    for subject in subjects:
        # CIA 1 (out of 50)
        cia1 = np.random.normal(35, 8)
        cia1 = max(10, min(50, cia1))
        
        # CIA 2 (out of 50) 
        cia2 = np.random.normal(37, 7)
        cia2 = max(12, min(50, cia2))
        
        # End Sem (out of 100)
        end_sem = np.random.normal(70, 15)
        end_sem = max(25, min(100, end_sem))
        
        # Calculate total (CIA1 + CIA2 + EndSem = 200 max)
        total = cia1 + cia2 + end_sem
        percentage = (total / 200) * 100
        
        # Assign grade
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B+"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "F"
        
        data.append({
            'student_id': student,
            'subject': subject,
            'cia1_marks': round(cia1, 1),
            'cia2_marks': round(cia2, 1),
            'end_sem_marks': round(end_sem, 1),
            'total_marks': round(total, 1),
            'percentage': round(percentage, 2),
            'grade': grade
        })

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv('exam_scores.csv', index=False)

print(f"Generated exam scores for {len(students)} students across {len(subjects)} subjects")
print(f"Total records: {len(data)}")
print("\nSample data:")
print(df.head(10))

# Generate summary statistics
print("\n=== SUMMARY STATISTICS ===")
for subject in subjects:
    subject_data = df[df['subject'] == subject]
    print(f"\n{subject}:")
    print(f"  Average: {subject_data['percentage'].mean():.2f}%")
    print(f"  Std Dev: {subject_data['percentage'].std():.2f}")
    print(f"  Grade Distribution:")
    print(subject_data['grade'].value_counts().to_string())