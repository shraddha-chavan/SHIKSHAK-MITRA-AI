import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { analyticsData, aiCoachSuggestions } from '@/data/mockData';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, Lightbulb, Target } from 'lucide-react';

const TeacherAnalytics = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Understand, Improve, Excel
          </h1>
          <p className="text-muted-foreground">
            Deep dive into your class analytics and get AI-powered coaching
          </p>
        </div>

        {/* Retention Curve */}
        <Card className="p-6 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-5 w-5 text-primary" />
            <h3 className="text-xl font-heading font-semibold">Retention Curve</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analyticsData.retentionCurve}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="week" stroke="hsl(var(--muted-foreground))" />
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
                dataKey="retention"
                stroke="hsl(var(--secondary))"
                strokeWidth={3}
                dot={{ fill: 'hsl(var(--secondary))', r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Confusion Heatmap */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Confusion Heatmap</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analyticsData.confusionHeatmap}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="topic" stroke="hsl(var(--muted-foreground))" />
              <YAxis stroke="hsl(var(--muted-foreground))" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="confusion" fill="hsl(var(--accent))" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Cohort Segmentation */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Student Cohorts</h3>
          <div className="grid md:grid-cols-3 gap-4">
            {analyticsData.cohorts.map((cohort, idx) => (
              <div key={idx} className="p-4 border rounded-lg hover:shadow-md transition-smooth">
                <h4 className="font-semibold mb-2">{cohort.name}</h4>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-primary">{cohort.count}</span>
                  <Badge variant="secondary">Avg: {cohort.avg}%</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* AI Coaching Section */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="h-6 w-6 text-accent" />
            <h2 className="text-2xl font-heading font-bold">AI Coaching Suggestions</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            {aiCoachSuggestions.map((suggestion) => (
              <Card key={suggestion.id} className="p-6 hover:shadow-lg transition-smooth">
                <div className="flex items-start gap-3 mb-3">
                  <Target className="h-5 w-5 text-primary mt-1" />
                  <div className="flex-1">
                    <h4 className="font-semibold mb-2">{suggestion.title}</h4>
                    <p className="text-sm text-muted-foreground mb-4">{suggestion.suggestion}</p>
                  </div>
                </div>
                <div className="flex items-center justify-between pt-3 border-t">
                  <div className="flex gap-4">
                    <div>
                      <p className="text-xs text-muted-foreground">Before</p>
                      <p className="text-lg font-bold text-destructive">{suggestion.before}%</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">After</p>
                      <p className="text-lg font-bold text-success">{suggestion.after}%</p>
                    </div>
                  </div>
                  <Badge variant={suggestion.impact === 'High' ? 'default' : 'secondary'}>
                    {suggestion.impact} Impact
                  </Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherAnalytics;
