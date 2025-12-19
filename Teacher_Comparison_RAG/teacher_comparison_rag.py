import pandas as pd
import numpy as np
from pathlib import Path

class TeacherComparisonRAG:
    """RAG system for teacher comparison and subject fit analysis"""
    
    def __init__(self):
        self.teachers = pd.read_csv('teachers_profile.csv')
        self.feedback = pd.read_csv('student_feedback.csv')
        self.subjects = pd.read_csv('subject_requirements.csv')
        
    def calculate_subject_fit(self, teacher_row, subject_req):
        """Calculate how well a teacher fits a subject requirement"""
        score = 0
        
        # Subject match (40%)
        if subject_req['subject'].lower() in teacher_row['specialization'].lower():
            score += 40
        elif subject_req['subject'].split()[0].lower() in teacher_row['subject'].lower():
            score += 30
        
        # Teaching style match (30%)
        req_styles = subject_req['preferred_teaching_style'].lower().split(', ')
        teacher_styles = teacher_row['teaching_style'].lower().split(', ')
        style_match = len(set(req_styles) & set(teacher_styles)) / len(req_styles)
        score += style_match * 30
        
        # Experience (15%)
        exp_score = min(teacher_row['experience_years'] / 15 * 15, 15)
        score += exp_score
        
        # Performance metrics (15%)
        avg_performance = (teacher_row['impact_score'] + teacher_row['retention'] + teacher_row['engagement']) / 3
        score += (avg_performance / 100) * 15
        
        return min(score, 100)
    
    def get_teacher_feedback_summary(self, teacher_id):
        """Get aggregated feedback for a teacher"""
        teacher_feedback = self.feedback[self.feedback['teacher_id'] == teacher_id]
        
        if len(teacher_feedback) == 0:
            return None
        
        return {
            'avg_rating': teacher_feedback['rating'].mean(),
            'avg_clarity': teacher_feedback['clarity'].mean(),
            'avg_engagement': teacher_feedback['engagement'].mean(),
            'avg_helpfulness': teacher_feedback['helpfulness'].mean(),
            'total_reviews': len(teacher_feedback),
            'top_feedback': teacher_feedback.nlargest(2, 'rating')['feedback_text'].tolist()
        }
    
    def compare_teachers(self, subject_name, top_n=3):
        """Compare teachers for a specific subject"""
        
        # Find subject requirements
        subject_req = self.subjects[self.subjects['subject'].str.contains(subject_name, case=False, na=False)]
        
        if len(subject_req) == 0:
            print(f"❌ Subject '{subject_name}' not found in requirements")
            return None
        
        subject_req = subject_req.iloc[0]
        
        # Calculate fit scores for all teachers
        results = []
        for _, teacher in self.teachers.iterrows():
            fit_score = self.calculate_subject_fit(teacher, subject_req)
            feedback_summary = self.get_teacher_feedback_summary(teacher['teacher_id'])
            
            results.append({
                'teacher_id': teacher['teacher_id'],
                'name': teacher['name'],
                'subject': teacher['subject'],
                'impact_score': teacher['impact_score'],
                'retention': teacher['retention'],
                'engagement': teacher['engagement'],
                'subject_fit': round(fit_score, 1),
                'experience': f"{teacher['experience_years']} years",
                'teaching_style': teacher['teaching_style'],
                'specialization': teacher['specialization'],
                'feedback_summary': feedback_summary
            })
        
        # Sort by subject fit
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('subject_fit', ascending=False)
        
        return results_df.head(top_n), subject_req
    
    def display_comparison(self, subject_name):
        """Display teacher comparison in terminal"""
        
        print("\n" + "="*100)
        print(f"  🎓 TEACHER COMPARISON - {subject_name.upper()}")
        print("="*100)
        
        top_teachers, subject_req = self.compare_teachers(subject_name, top_n=3)
        
        if top_teachers is None:
            return
        
        # Display subject requirements
        print(f"\n📋 Subject Requirements:")
        print(f"   Difficulty: {subject_req['difficulty_level']}")
        print(f"   Student Level: {subject_req['student_level']}")
        print(f"   Required Skills: {subject_req['required_skills']}")
        print(f"   Preferred Style: {subject_req['preferred_teaching_style']}")
        print(f"   Key Topics: {subject_req['key_topics']}")
        
        # Display comparison table
        print("\n" + "="*100)
        print("📊 TEACHER COMPARISON TABLE")
        print("="*100)
        print(f"{'Teacher':<25} {'Subject':<20} {'Impact':<8} {'Retention':<10} {'Engagement':<12} {'Subject Fit':<12} {'Experience':<12}")
        print("-"*100)
        
        for _, teacher in top_teachers.iterrows():
            print(f"{teacher['name']:<25} {teacher['subject']:<20} {teacher['impact_score']:<8} "
                  f"{teacher['retention']}%{'':<7} {teacher['engagement']}%{'':<9} "
                  f"{teacher['subject_fit']}%{'':<8} {teacher['experience']:<12}")
        
        # Display AI Recommendations
        print("\n" + "="*100)
        print("🤖 AI RECOMMENDATIONS")
        print("="*100)
        
        best_teacher = top_teachers.iloc[0]
        second_teacher = top_teachers.iloc[1] if len(top_teachers) > 1 else None
        
        print(f"\n✨ Best Fit for {subject_name}")
        print(f"   Based on technical background, teaching style, and student feedback analysis")
        print(f"\n   🏆 {best_teacher['name']}")
        print(f"   {'─'*50}")
        print(f"   Subject Fit Score: {best_teacher['subject_fit']}%")
        print(f"   Impact Score: {best_teacher['impact_score']}")
        print(f"   Retention: {best_teacher['retention']}%")
        print(f"   Engagement: {best_teacher['engagement']}%")
        print(f"   Experience: {best_teacher['experience']}")
        print(f"   Teaching Style: {best_teacher['teaching_style']}")
        print(f"   Specialization: {best_teacher['specialization']}")
        
        # Display feedback
        if best_teacher['feedback_summary']:
            feedback = best_teacher['feedback_summary']
            print(f"\n   📝 Student Feedback (Avg Rating: {feedback['avg_rating']:.1f}/5)")
            for i, comment in enumerate(feedback['top_feedback'][:2], 1):
                print(f"      {i}. \"{comment}\"")
        
        if second_teacher is not None:
            print(f"\n   🥈 Alternative Recommendation")
            print(f"   {'─'*50}")
            print(f"   {second_teacher['name']}")
            print(f"   Subject Fit Score: {second_teacher['subject_fit']}%")
            print(f"   {second_teacher['teaching_style']} approach with {second_teacher['experience']}")
        
        print("\n" + "="*100)
    
    def compare_multiple_subjects(self, subjects_list):
        """Compare teachers across multiple subjects"""
        
        print("\n" + "="*100)
        print("  🎓 MULTI-SUBJECT TEACHER COMPARISON")
        print("="*100)
        
        all_recommendations = {}
        
        for subject in subjects_list:
            top_teachers, subject_req = self.compare_teachers(subject, top_n=1)
            if top_teachers is not None:
                best = top_teachers.iloc[0]
                all_recommendations[subject] = {
                    'teacher': best['name'],
                    'fit_score': best['subject_fit'],
                    'impact': best['impact_score']
                }
        
        print("\n📊 Best Teacher for Each Subject:")
        print("-"*100)
        print(f"{'Subject':<30} {'Recommended Teacher':<30} {'Fit Score':<15} {'Impact Score':<15}")
        print("-"*100)
        
        for subject, rec in all_recommendations.items():
            print(f"{subject:<30} {rec['teacher']:<30} {rec['fit_score']}%{'':<10} {rec['impact']:<15}")
        
        print("\n" + "="*100)
    
    def find_best_teacher_overall(self):
        """Find the best overall teacher"""
        
        print("\n" + "="*100)
        print("  🏆 TOP PERFORMING TEACHERS")
        print("="*100)
        
        # Calculate overall score
        self.teachers['overall_score'] = (
            self.teachers['impact_score'] * 0.4 +
            self.teachers['retention'] * 0.3 +
            self.teachers['engagement'] * 0.3
        )
        
        top_5 = self.teachers.nlargest(5, 'overall_score')
        
        print(f"\n{'Rank':<6} {'Teacher':<25} {'Subject':<20} {'Overall Score':<15} {'Experience':<12}")
        print("-"*100)
        
        for i, (_, teacher) in enumerate(top_5.iterrows(), 1):
            print(f"{i:<6} {teacher['name']:<25} {teacher['subject']:<20} "
                  f"{teacher['overall_score']:.1f}{'':<10} {teacher['experience_years']} years")
        
        print("\n" + "="*100)


def main():
    """Main execution"""
    
    print("\n" + "╔" + "="*98 + "╗")
    print("║" + " "*30 + "TEACHER COMPARISON RAG SYSTEM" + " "*39 + "║")
    print("╚" + "="*98 + "╝")
    
    rag = TeacherComparisonRAG()
    
    # Example 1: Compare for AI/ML Course
    rag.display_comparison("AI/ML Course")
    
    # Example 2: Compare for Advanced Mathematics
    rag.display_comparison("Advanced Mathematics")
    
    # Example 3: Multi-subject comparison
    rag.compare_multiple_subjects([
        "AI/ML Course",
        "Advanced Mathematics",
        "Data Science",
        "Web Development"
    ])
    
    # Example 4: Top performers
    rag.find_best_teacher_overall()
    
    print("\n✅ Analysis Complete!")
    print("="*100 + "\n")


if __name__ == "__main__":
    main()
