class ComprehensiveScoring {
  constructor() {
    this.examWeight = 0.4;
    this.videoWeight = 0.35;
    this.audioWeight = 0.25;
  }

  async calculateComprehensiveScores() {
    try {
      const [examData, videoData, audioData] = await Promise.all([
        this.getExamScores(),
        this.getVideoMetrics(),
        this.getAudioMetrics()
      ]);

      return {
        attention_score: this.calculateAttentionScore(examData, videoData, audioData),
        emotion_score: this.calculateEmotionScore(examData, videoData, audioData),
        participation_score: this.calculateParticipationScore(examData, videoData, audioData),
        overall_engagement: this.calculateOverallEngagement(examData, videoData, audioData),
        comprehension_score: this.calculateComprehensionScore(examData, videoData, audioData),
        teacher_effectiveness: this.calculateTeacherEffectiveness(examData, videoData, audioData)
      };
    } catch (error) {
      console.error('Error calculating comprehensive scores:', error);
      return this.getFallbackScores();
    }
  }

  async getExamScores() {
    // Load exam data from CSV
    const response = await fetch('/Scoring_System/Sample_Data/Exam_Scores/exam_scores.csv');
    const csvText = await response.text();
    const lines = csvText.split('\n');
    const headers = lines[0].split(',');
    
    const examScores = lines.slice(1).map(line => {
      const values = line.split(',');
      return {
        student_id: values[0],
        subject: values[1],
        percentage: parseFloat(values[6]) || 0
      };
    });

    const avgPercentage = examScores.reduce((sum, s) => sum + s.percentage, 0) / examScores.length;
    return {
      average_performance: avgPercentage,
      pass_rate: examScores.filter(s => s.percentage >= 60).length / examScores.length * 100,
      excellence_rate: examScores.filter(s => s.percentage >= 90).length / examScores.length * 100
    };
  }

  async getVideoMetrics() {
    const response = await fetch('http://localhost:8000/live-metrics');
    return await response.json();
  }

  async getAudioMetrics() {
    // Simulate audio analysis metrics
    return {
      speech_clarity: Math.random() * 30 + 70, // 70-100%
      pace_score: Math.random() * 25 + 75, // 75-100%
      volume_consistency: Math.random() * 20 + 80, // 80-100%
      question_frequency: Math.random() * 10 + 5 // 5-15 questions per hour
    };
  }

  calculateAttentionScore(exam, video, audio) {
    const examComponent = exam.average_performance * 0.8; // Exam performance indicates attention
    const videoComponent = video.attention || 75;
    const audioComponent = audio.speech_clarity;

    return Math.round(
      examComponent * this.examWeight +
      videoComponent * this.videoWeight +
      audioComponent * this.audioWeight
    );
  }

  calculateEmotionScore(exam, video, audio) {
    const examComponent = exam.pass_rate; // Pass rate indicates positive emotions
    const videoComponent = video.engagement || 75;
    const audioComponent = audio.volume_consistency;

    return Math.round(
      examComponent * this.examWeight +
      videoComponent * this.videoWeight +
      audioComponent * this.audioWeight
    );
  }

  calculateParticipationScore(exam, video, audio) {
    const examComponent = exam.excellence_rate * 2; // Excellence indicates participation
    const videoComponent = (video.hand_raises || 3) * 10; // Hand raises
    const audioComponent = audio.question_frequency * 5;

    return Math.min(100, Math.round(
      examComponent * this.examWeight +
      videoComponent * this.videoWeight +
      audioComponent * this.audioWeight
    ));
  }

  calculateOverallEngagement(exam, video, audio) {
    const attention = this.calculateAttentionScore(exam, video, audio);
    const emotion = this.calculateEmotionScore(exam, video, audio);
    const participation = this.calculateParticipationScore(exam, video, audio);

    return Math.round((attention * 0.4 + emotion * 0.35 + participation * 0.25));
  }

  calculateComprehensionScore(exam, video, audio) {
    const examComponent = exam.average_performance;
    const videoComponent = video.attention || 75;
    const audioComponent = audio.pace_score;

    return Math.round(
      examComponent * 0.6 + // Exam scores heavily weight comprehension
      videoComponent * 0.25 +
      audioComponent * 0.15
    );
  }

  calculateTeacherEffectiveness(exam, video, audio) {
    const examComponent = (exam.pass_rate + exam.excellence_rate) / 2;
    const videoComponent = video.engagement || 75;
    const audioComponent = (audio.speech_clarity + audio.pace_score) / 2;

    return Math.round(
      examComponent * this.examWeight +
      videoComponent * this.videoWeight +
      audioComponent * this.audioWeight
    );
  }

  getFallbackScores() {
    return {
      attention_score: 78,
      emotion_score: 82,
      participation_score: 75,
      overall_engagement: 79,
      comprehension_score: 85,
      teacher_effectiveness: 81
    };
  }
}

export const comprehensiveScoring = new ComprehensiveScoring();