from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

@app.route('/video-analysis', methods=['GET', 'POST'])
def video_analysis():
    return jsonify({
        'engagement_score': 78,
        'attention_score': 82,
        'participation_count': 12,
        'student_count': 30,
        'hand_raises': 5,
        'status': 'success'
    })

@app.route('/rag-query', methods=['POST'])
def rag_query():
    data = request.get_json()
    query = data.get('query', '')
    
    responses = {
        'teaching_strategies': 'Implement interactive questioning techniques and use visual aids to enhance student engagement.',
        'student_performance': 'Current analysis shows 78% average engagement with strong participation in STEM subjects.',
        'improvement_suggestions': 'Consider shorter lesson segments, incorporate hands-on activities, and implement frequent comprehension checks.',
        'classroom_management': 'Use positive reinforcement, establish clear expectations, and create an inclusive learning environment.'
    }
    
    return jsonify({
        'response': responses.get(query, 'Focus on student-centered learning approaches with regular feedback loops.'),
        'confidence': 0.85,
        'status': 'success'
    })

@app.route('/teacher-comparison', methods=['GET', 'POST'])
def teacher_comparison():
    return jsonify({
        'teachers': [
            {'name': 'Dr. Smith', 'subject': 'Mathematics', 'engagement': 85, 'effectiveness': 88, 'student_feedback': 4.2},
            {'name': 'Prof. Johnson', 'subject': 'Science', 'engagement': 79, 'effectiveness': 82, 'student_feedback': 4.0},
            {'name': 'Ms. Davis', 'subject': 'English', 'engagement': 91, 'effectiveness': 94, 'student_feedback': 4.6},
            {'name': 'Mr. Wilson', 'subject': 'History', 'engagement': 73, 'effectiveness': 76, 'student_feedback': 3.8}
        ],
        'insights': 'Teachers with higher engagement scores show better student outcomes and feedback ratings.',
        'status': 'success'
    })

@app.route('/decision-ai', methods=['GET', 'POST'])
def decision_ai():
    return jsonify({
        'recommendations': [
            'Implement more interactive elements in lessons to boost engagement',
            'Use peer learning activities to encourage collaboration',
            'Incorporate visual aids and multimedia for complex concepts',
            'Schedule regular comprehension checks every 10-15 minutes',
            'Provide immediate feedback on student responses',
            'Create opportunities for student-led discussions'
        ],
        'priority': 'high',
        'expected_improvement': '15-20% engagement increase',
        'status': 'success'
    })

# Store video metrics
video_metrics = {
    'engagement': 75,
    'attention': 80,
    'participation': 10,
    'students': 30,
    'hand_raises': 3
}

@app.route('/update-video-metrics', methods=['POST'])
def update_video_metrics():
    global video_metrics
    data = request.get_json()
    if data:
        video_metrics.update({
            'engagement': data.get('engagement', 75),
            'attention': data.get('attention', 80),
            'participation': data.get('participation', 10),
            'students': data.get('students', 30),
            'hand_raises': data.get('hand_raises', 3)
        })
    return jsonify({'status': 'updated'})

@app.route('/live-metrics', methods=['GET'])
def live_metrics():
    return jsonify(video_metrics)

if __name__ == '__main__':
    print("AI Backend Server Starting...")
    print("Server running on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)