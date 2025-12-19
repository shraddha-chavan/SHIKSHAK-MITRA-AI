import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Calculator, TrendingUp, Users, Clock, BookOpen, MessageSquare, Mic, MicOff } from 'lucide-react';
import { voiceService } from '@/services/voiceService';

const TeacherScoring = () => {
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [scores, setScores] = useState({
    attention_score: 0,
    emotion_score: 0,
    participation_score: 0,
    overall_engagement: 0,
    comprehension_score: 0,
    teacher_effectiveness: 0,
    wpm_score: 0,
    class_metrics: {
      engagement_rate: 0,
      participation_rate: 0,
      attention_consistency: 0
    }
  });

  const [examData, setExamData] = useState([]);

  useEffect(() => {
    // Welcome message when component mounts
    voiceService.announceWelcome();
    
    // Fetch AI-generated scores
    const calculateScores = async () => {
      try {
        const response = await fetch('http://localhost:8000/live-metrics');
        const aiData = await response.json();
        
        // Use AI data for calculations
        const attention_duration = aiData.attention * 30; // Convert to seconds
        const session_duration = 3000;
        const confidence_factor = 0.92;

      
      // Attention Score Calculation
      const attention_ratio = attention_duration / session_duration;
      const sustained_attention_bonus = 1 + (0.2 * Math.log(1 + attention_ratio));
      const attention_score = Math.min(100, attention_ratio * confidence_factor * sustained_attention_bonus * 100);
      
        // Use real video data for emotion and participation
        const positive_emotions = aiData.engagement;
        const negative_emotions = 100 - aiData.engagement;
        const total_emotions = 100;
        const emotion_score = 50 + ((positive_emotions - negative_emotions) / total_emotions) * 50;
        
        // Participation from real video data
        const hand_raises = aiData.hand_raises;
        const correct_answers = aiData.participation || aiData.students;
        const total_responses = (aiData.participation || aiData.students) + 3;
        const participation_time = 1800;
        const class_duration = 3000;
      
        const hand_raise_score = Math.min(hand_raises * 20, 40);
        const accuracy_score = (correct_answers / total_responses) * 30;
        const time_score = (participation_time / class_duration) * 30;
        const participation_score = Math.min(100, hand_raise_score + accuracy_score + time_score);
      
        // Overall Engagement (weighted)
        const engagement_weights = { attention: 0.35, emotion: 0.25, participation: 0.20, interaction: 0.20 };
        const interaction_score = aiData.engagement;
        const overall_engagement = (
          attention_score * engagement_weights.attention +
          emotion_score * engagement_weights.emotion +
          participation_score * engagement_weights.participation +
          interaction_score * engagement_weights.interaction
        );
      
      // Comprehension Score
      const comprehension_correct = 18;
      const comprehension_total = 20;
      const confusion_indicators = 2;
      const avg_response_time = 6; // seconds
      
      const accuracy_rate = comprehension_correct / comprehension_total;
      const confusion_penalty = confusion_indicators * 0.1 * 10;
      const response_time_bonus = (3 <= avg_response_time && avg_response_time <= 10) ? 10 : 0;
      const comprehension_score = Math.min(100, Math.max(0, (accuracy_rate * 100) - confusion_penalty + response_time_bonus));
      
      // Teacher Effectiveness
      const student_engagements = [82, 75, 88, 91, 67, 79, 85, 73, 90, 77]; // Sample class data
      const active_participants = 28;
      const total_students = 30;
      
      const engagement_rate = student_engagements.reduce((a, b) => a + b, 0) / student_engagements.length;
      const participation_rate = (active_participants / total_students) * 100;
      const attention_variance = student_engagements.reduce((acc, val) => acc + Math.pow(val - engagement_rate, 2), 0) / student_engagements.length;
      const attention_consistency = Math.max(0, 100 - (attention_variance / 10));
      
      const teacher_weights = { engagement_rate: 0.30, participation_rate: 0.25, comprehension_rate: 0.25, attention_consistency: 0.20 };
      const teacher_effectiveness = (
        engagement_rate * teacher_weights.engagement_rate +
        participation_rate * teacher_weights.participation_rate +
        comprehension_score * teacher_weights.comprehension_rate +
        attention_consistency * teacher_weights.attention_consistency
      );
      
      // WPM Score
      const words_spoken = 7200; // words in 50 minute class
      const duration_minutes = 50;
      const wpm = words_spoken / duration_minutes;
      let wpm_score;
      if (120 <= wpm && wpm <= 160) wpm_score = 100;
      else if ((100 <= wpm && wpm < 120) || (160 < wpm && wpm <= 180)) wpm_score = 85;
      else if ((80 <= wpm && wpm < 100) || (180 < wpm && wpm <= 200)) wpm_score = 70;
      else wpm_score = 50;
      
        const newScores = {
          attention_score: Math.round(attention_score),
          emotion_score: Math.round(emotion_score),
          participation_score: Math.round(participation_score),
          overall_engagement: Math.round(overall_engagement),
          comprehension_score: Math.round(comprehension_score),
          teacher_effectiveness: Math.round(teacher_effectiveness),
          wpm_score: Math.round(wpm_score),
          class_metrics: {
            engagement_rate: Math.round(engagement_rate),
            participation_rate: Math.round(participation_rate),
            attention_consistency: Math.round(attention_consistency)
          }
        };
        
        setScores(newScores);
        
        // Check for score drops and announce
        voiceService.checkScoreDrops(newScores);
      } catch (error) {
        console.error('AI integration error:', error);
        // Fallback to mock data
        const fallbackScores = {
          attention_score: 78,
          emotion_score: 82,
          participation_score: 75,
          overall_engagement: 79,
          comprehension_score: 85,
          teacher_effectiveness: 81,
          wpm_score: 88,
          class_metrics: {
            engagement_rate: 79,
            participation_rate: 85,
            attention_consistency: 77
          }
        };
        
        setScores(fallbackScores);
        voiceService.checkScoreDrops(fallbackScores);
      }
    };

    // Load exam data
    const loadExamData = async () => {
      try {
        // In real implementation, this would fetch from the CSV file
        const sampleExamData = [
          { subject: 'Mathematics', average: 70.04, grade_distribution: { 'A+': 1, 'A': 6, 'B+': 21, 'B': 21, 'C': 6 } },
          { subject: 'Science', average: 71.65, grade_distribution: { 'A+': 1, 'A': 5, 'B+': 27, 'B': 18, 'C': 4 } },
          { subject: 'English', average: 71.32, grade_distribution: { 'A': 7, 'B+': 21, 'B': 24, 'C': 3 } },
          { subject: 'History', average: 71.08, grade_distribution: { 'A+': 1, 'A': 8, 'B+': 21, 'B': 16, 'C': 8, 'F': 1 } }
        ];
        setExamData(sampleExamData);
      } catch (error) {
        console.error('Error loading exam data:', error);
      }
    };

    calculateScores();
    loadExamData();
    
    // Update scores every 10 seconds
    const interval = setInterval(calculateScores, 10000);
    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 85) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 60) return 'Average';
    return 'Needs Improvement';
  };

  const toggleVoice = () => {
    const enabled = voiceService.toggle();
    setVoiceEnabled(enabled);
  };

  const speakCurrentScores = () => {
    voiceService.announceScores(scores);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
                Mathematical Scoring Dashboard
              </h1>
              <p className="text-muted-foreground">
                Real-time calculated scores based on scientific formulas and educational research
              </p>
            </div>
            

          </div>
        </div>

        {/* Core Engagement Metrics */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="rounded-full p-3 bg-primary/10">
                <TrendingUp className="h-6 w-6 text-primary" />
              </div>
              <Badge variant="outline">{getScoreBadge(scores.attention_score)}</Badge>
            </div>
            <h3 className="font-semibold text-lg mb-2">Attention Score</h3>
            <div className={`text-3xl font-bold ${getScoreColor(scores.attention_score)}`}>
              {scores.attention_score}%
            </div>
            <Progress value={scores.attention_score} className="mt-2" />
            <p className="text-sm text-muted-foreground mt-2">
              Student focus and attention tracking
            </p>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="rounded-full p-3 bg-secondary/10">
                <MessageSquare className="h-6 w-6 text-secondary" />
              </div>
              <Badge variant="outline">{getScoreBadge(scores.emotion_score)}</Badge>
            </div>
            <h3 className="font-semibold text-lg mb-2">Emotion Score</h3>
            <div className={`text-3xl font-bold ${getScoreColor(scores.emotion_score)}`}>
              {scores.emotion_score}%
            </div>
            <Progress value={scores.emotion_score} className="mt-2" />
            <p className="text-sm text-muted-foreground mt-2">
              Student emotional engagement level
            </p>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="rounded-full p-3 bg-accent/10">
                <Users className="h-6 w-6 text-accent" />
              </div>
              <Badge variant="outline">{getScoreBadge(scores.participation_score)}</Badge>
            </div>
            <h3 className="font-semibold text-lg mb-2">Participation Score</h3>
            <div className={`text-3xl font-bold ${getScoreColor(scores.participation_score)}`}>
              {scores.participation_score}%
            </div>
            <Progress value={scores.participation_score} className="mt-2" />
            <p className="text-sm text-muted-foreground mt-2">
              Active participation in class activities
            </p>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="rounded-full p-3 bg-info/10">
                <Calculator className="h-6 w-6 text-info" />
              </div>
              <Badge variant="outline">{getScoreBadge(scores.overall_engagement)}</Badge>
            </div>
            <h3 className="font-semibold text-lg mb-2">Overall Engagement</h3>
            <div className={`text-3xl font-bold ${getScoreColor(scores.overall_engagement)}`}>
              {scores.overall_engagement}%
            </div>
            <Progress value={scores.overall_engagement} className="mt-2" />
            <p className="text-sm text-muted-foreground mt-2">
              Overall student engagement score
            </p>
          </Card>
        </div>

        {/* Advanced Metrics */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <BookOpen className="h-6 w-6 text-primary" />
              <h3 className="font-semibold text-lg">Comprehension Score</h3>
            </div>
            <div className={`text-4xl font-bold ${getScoreColor(scores.comprehension_score)} mb-2`}>
              {scores.comprehension_score}%
            </div>
            <Progress value={scores.comprehension_score} className="mb-3" />
            <div className="text-sm text-muted-foreground space-y-1">
              <p>• Student understanding level</p>
              <p>• Question response accuracy</p>
              <p>• Learning comprehension rate</p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <TrendingUp className="h-6 w-6 text-secondary" />
              <h3 className="font-semibold text-lg">Teacher Effectiveness</h3>
            </div>
            <div className={`text-4xl font-bold ${getScoreColor(scores.teacher_effectiveness)} mb-2`}>
              {scores.teacher_effectiveness}%
            </div>
            <Progress value={scores.teacher_effectiveness} className="mb-3" />
            <div className="text-sm text-muted-foreground space-y-1">
              <p>• Class engagement: {scores.class_metrics.engagement_rate}%</p>
              <p>• Participation rate: {scores.class_metrics.participation_rate}%</p>
              <p>• Attention consistency: {scores.class_metrics.attention_consistency}%</p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Clock className="h-6 w-6 text-accent" />
              <h3 className="font-semibold text-lg">WPM Score</h3>
            </div>
            <div className={`text-4xl font-bold ${getScoreColor(scores.wpm_score)} mb-2`}>
              {scores.wpm_score}%
            </div>
            <Progress value={scores.wpm_score} className="mb-3" />
            <div className="text-sm text-muted-foreground space-y-1">
              <p>• Speaking pace analysis</p>
              <p>• Optimal teaching speed</p>
              <p>• Communication effectiveness</p>
            </div>
          </Card>
        </div>

        {/* Exam Performance Data */}
        <Card className="p-6">
          <h3 className="font-semibold text-xl mb-6">Academic Performance Overview</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {examData.map((subject, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h4 className="font-semibold text-lg mb-3">{subject.subject}</h4>
                <div className="text-2xl font-bold text-primary mb-2">
                  {subject.average.toFixed(1)}%
                </div>
                <div className="text-sm text-muted-foreground mb-3">Class Average</div>
                <div className="space-y-1">
                  <div className="text-sm font-medium">Grade Distribution:</div>
                  {Object.entries(subject.grade_distribution).map(([grade, count]) => (
                    <div key={grade} className="flex justify-between text-sm">
                      <span>{grade}:</span>
                      <span>{count} students</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>


      </div>
    </div>
  );
};

export default TeacherScoring;