"""
OpenAI API Integration for Enhanced RAG System
Provides intelligent content generation and analysis using GPT models
"""

import openai
import os
from typing import List, Dict, Optional
import json
import asyncio
from datetime import datetime

class OpenAIEnhancedRAG:
    """Enhanced RAG system with OpenAI GPT integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client"""
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
        )
        self.model = "gpt-3.5-turbo"
    
    async def generate_teaching_insights(self, student_data: Dict) -> Dict:
        """Generate personalized teaching insights using GPT"""
        prompt = f"""
        Analyze this student engagement data and provide actionable teaching insights:
        
        Student Metrics:
        - Engagement Level: {student_data.get('engagement', 0)}%
        - Attention Score: {student_data.get('attention', 0)}%
        - Participation: {student_data.get('participation', 0)}%
        - Subject: {student_data.get('subject', 'General')}
        
        Provide:
        1. Key observations
        2. Specific teaching strategies
        3. Intervention recommendations
        4. Expected outcomes
        
        Format as JSON with clear sections.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational AI assistant specializing in teaching analytics and student engagement."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return {
                "insights": response.choices[0].message.content,
                "generated_at": datetime.now().isoformat(),
                "model_used": self.model,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "generated_at": datetime.now().isoformat()
            }
    
    def generate_lesson_recommendations(self, performance_data: List[Dict]) -> Dict:
        """Generate lesson plan recommendations based on class performance"""
        avg_engagement = sum(d.get('engagement', 0) for d in performance_data) / len(performance_data)
        
        prompt = f"""
        Based on class performance data (Average Engagement: {avg_engagement:.1f}%), 
        generate specific lesson plan recommendations:
        
        1. Interactive activities to boost engagement
        2. Assessment strategies
        3. Technology integration suggestions
        4. Differentiation techniques
        
        Focus on practical, implementable strategies.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a curriculum design expert with deep knowledge of pedagogical strategies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )
            
            return {
                "recommendations": response.choices[0].message.content,
                "class_engagement": avg_engagement,
                "generated_at": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def analyze_teaching_effectiveness(self, metrics: Dict) -> Dict:
        """Analyze overall teaching effectiveness using AI"""
        prompt = f"""
        Evaluate teaching effectiveness based on these metrics:
        
        Performance Indicators:
        - Student Engagement: {metrics.get('engagement', 0)}%
        - Learning Retention: {metrics.get('retention', 0)}%
        - Class Participation: {metrics.get('participation', 0)}%
        - Attention Levels: {metrics.get('attention', 0)}%
        
        Provide:
        1. Overall effectiveness score (1-10)
        2. Strengths identified
        3. Areas for improvement
        4. Specific action items
        
        Be constructive and specific.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational assessment expert providing constructive feedback to teachers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=700
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "metrics_analyzed": metrics,
                "generated_at": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e), "status": "failed"}

# Demo usage
if __name__ == "__main__":
    # Initialize OpenAI RAG
    rag = OpenAIEnhancedRAG()
    
    # Sample student data
    sample_data = {
        "engagement": 75,
        "attention": 82,
        "participation": 68,
        "subject": "Mathematics"
    }
    
    # Generate insights
    insights = asyncio.run(rag.generate_teaching_insights(sample_data))
    print("🤖 AI-Generated Teaching Insights:")
    print(json.dumps(insights, indent=2))