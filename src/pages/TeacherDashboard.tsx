import { useState, useEffect } from 'react';
import { MetricCard } from '@/components/MetricCard';
import { AlertItem } from '@/components/AlertItem';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TrendingUp, Users, Heart, Sparkles, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { teacherMetrics } from '@/data/mockData';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

const TeacherDashboard = () => {
  const [scores, setScores] = useState({
    attention_score: 78,
    emotion_score: 82,
    participation_score: 75,
    overall_engagement: 79,
    comprehension_score: 85,
    teacher_effectiveness: 81
  });
  const [trendData, setTrendData] = useState([
    { time: '10:00', score: 75 },
    { time: '10:10', score: 78 },
    { time: '10:20', score: 82 },
    { time: '10:30', score: 85 },
    { time: '10:40', score: 87 },
  ]);

  useEffect(() => {
    const fetchScores = async () => {
      try {
        const response = await fetch('http://localhost:8000/live-metrics');
        const aiData = await response.json();
        
        const newScores = {
          attention_score: aiData.attention || 78,
          emotion_score: aiData.engagement || 82,
          participation_score: aiData.participation || 75,
          overall_engagement: aiData.engagement || 79,
          comprehension_score: 85,
          teacher_effectiveness: 81
        };
        
        setScores(newScores);
        
        const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        setTrendData(prev => [...prev.slice(-4), { time, score: newScores.overall_engagement }]);
      } catch (error) {
        console.error('Error fetching scores:', error);
      }
    };

    fetchScores();
    const interval = setInterval(fetchScores, 10000);
    return () => clearInterval(interval);
  }, []);

  const pieData = [
    { name: 'Attention', value: scores.attention_score, color: '#8884d8' },
    { name: 'Emotion', value: scores.emotion_score, color: '#82ca9d' },
    { name: 'Participation', value: scores.participation_score, color: '#ffc658' },
    { name: 'Comprehension', value: scores.comprehension_score, color: '#ff7300' }
  ];

  const barData = [
    { name: 'Attention', score: scores.attention_score },
    { name: 'Emotion', score: scores.emotion_score },
    { name: 'Participation', score: scores.participation_score },
    { name: 'Engagement', score: scores.overall_engagement }
  ];
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Your Teaching Impact at a Glance
          </h1>
          <p className="text-muted-foreground">
            Track your performance and discover opportunities for growth
          </p>
        </div>

        {/* Main Metrics */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Overall Engagement"
            value={`${scores.overall_engagement}%`}
            icon={TrendingUp}
            trend="+5%"
            trendUp={true}
            valueClassName="text-primary"
          />
          <MetricCard
            title="Attention Score"
            value={`${scores.attention_score}%`}
            icon={Users}
            trend="+2%"
            trendUp={true}
            valueClassName="text-secondary"
          />
          <MetricCard
            title="Participation"
            value={`${scores.participation_score}%`}
            icon={Heart}
            trend="-3%"
            trendUp={false}
            valueClassName="text-accent"
          />
          <MetricCard
            title="Teacher Effectiveness"
            value={`${scores.teacher_effectiveness}%`}
            icon={Sparkles}
            trend="+1%"
            trendUp={true}
            valueClassName="text-info"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Real-time Trend */}
          <Card className="p-6">
            <h3 className="text-xl font-heading font-semibold mb-4">Live Engagement Trend</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="time" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#8884d8"
                  strokeWidth={3}
                  dot={{ fill: '#8884d8', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Score Distribution */}
          <Card className="p-6">
            <h3 className="text-xl font-heading font-semibold mb-4">Score Distribution</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Bar Chart */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Current Performance Metrics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip />
              <Bar dataKey="score" fill="#82ca9d" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Alerts */}
        <div className="mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Recent Alerts</h3>
          <div className="space-y-3">
            {teacherMetrics.alerts.map((alert) => (
              <AlertItem
                key={alert.id}
                type={alert.type as 'success' | 'warning' | 'critical'}
                message={alert.message}
                time={alert.time}
              />
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <Card className="p-6">
          <h3 className="text-xl font-heading font-semibold mb-4">Quick Actions</h3>
          <div className="grid md:grid-cols-3 gap-4">
            <Button variant="outline" className="justify-between h-auto py-4" asChild>
              <Link to="/teacher-analytics">
                <span>View Detailed Analytics</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" className="justify-between h-auto py-4" asChild>
              <Link to="/activity-generator">
                <span>Generate Activities</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" className="justify-between h-auto py-4" asChild>
              <Link to="/teacher-analytics">
                <span>Get AI Coaching</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default TeacherDashboard;
