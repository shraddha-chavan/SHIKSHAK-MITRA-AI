import { MetricCard } from '@/components/MetricCard';
import { AlertItem } from '@/components/AlertItem';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TrendingUp, Users, Heart, Sparkles, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { teacherMetrics } from '@/data/mockData';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const trendData = [
  { month: 'Jan', score: 75 },
  { month: 'Feb', score: 78 },
  { month: 'Mar', score: 82 },
  { month: 'Apr', score: 85 },
  { month: 'May', score: 87 },
];

const TeacherDashboard = () => {
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
            title="Teacher Impact Score"
            value={teacherMetrics.impactScore}
            icon={TrendingUp}
            trend={teacherMetrics.trend}
            trendUp={true}
            valueClassName="text-primary"
          />
          <MetricCard
            title="Retention Rate"
            value={`${teacherMetrics.retention}%`}
            icon={Users}
            trend="+5%"
            trendUp={true}
            valueClassName="text-secondary"
          />
          <MetricCard
            title="Engagement Score"
            value={`${teacherMetrics.engagement}%`}
            icon={Heart}
            trend="+3%"
            trendUp={true}
            valueClassName="text-accent"
          />
          <MetricCard
            title="Curiosity Index"
            value={teacherMetrics.curiosityIndex}
            icon={Sparkles}
            trend="-2%"
            trendUp={false}
            valueClassName="text-info"
          />
        </div>

        {/* Trend Chart */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Impact Score Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                }}
              />
              <Line
                type="monotone"
                dataKey="score"
                stroke="hsl(var(--primary))"
                strokeWidth={3}
                dot={{ fill: 'hsl(var(--primary))', r: 6 }}
              />
            </LineChart>
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
