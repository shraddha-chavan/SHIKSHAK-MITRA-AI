import { MetricCard } from '@/components/MetricCard';
import { AlertItem } from '@/components/AlertItem';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Building2, Users, TrendingUp, TrendingDown } from 'lucide-react';
import { managementMetrics } from '@/data/mockData';

const ManagementDashboard = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Institution Insights, Simplified
          </h1>
          <p className="text-muted-foreground">
            Comprehensive overview of your institution's teaching performance
          </p>
        </div>

        {/* Main Metrics */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Institution Health Score"
            value={managementMetrics.healthScore}
            icon={Building2}
            trend="+8%"
            trendUp={true}
            valueClassName="text-primary"
          />
          <MetricCard
            title="Total Teachers"
            value={managementMetrics.totalTeachers}
            icon={Users}
            valueClassName="text-secondary"
          />
          <MetricCard
            title="Avg Retention"
            value={`${managementMetrics.avgRetention}%`}
            icon={TrendingUp}
            trend="+6%"
            trendUp={true}
            valueClassName="text-success"
          />
          <MetricCard
            title="Avg Engagement"
            value={`${managementMetrics.avgEngagement}%`}
            icon={TrendingUp}
            trend="+4%"
            trendUp={true}
            valueClassName="text-info"
          />
        </div>

        {/* Top & Bottom Teachers */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Top Performers */}
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-success" />
              <h3 className="text-xl font-heading font-semibold">Top Performers</h3>
            </div>
            <div className="space-y-3">
              {managementMetrics.topTeachers.map((teacher, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-lg border hover:shadow-md transition-smooth">
                  <div className="flex-1">
                    <p className="font-semibold">{teacher.name}</p>
                    <p className="text-sm text-muted-foreground">{teacher.subject}</p>
                  </div>
                  <Badge className="gradient-secondary text-secondary-foreground">
                    {teacher.score}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>

          {/* Needs Attention */}
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingDown className="h-5 w-5 text-warning" />
              <h3 className="text-xl font-heading font-semibold">Needs Attention</h3>
            </div>
            <div className="space-y-3">
              {managementMetrics.bottomTeachers.map((teacher, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-lg border hover:shadow-md transition-smooth">
                  <div className="flex-1">
                    <p className="font-semibold">{teacher.name}</p>
                    <p className="text-sm text-muted-foreground">{teacher.subject}</p>
                  </div>
                  <Badge variant="outline" className="border-warning text-warning">
                    {teacher.score}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Alerts */}
        <div className="mb-8">
          <h3 className="text-xl font-heading font-semibold mb-4">Critical Alerts</h3>
          <div className="space-y-3">
            {managementMetrics.alerts.map((alert) => (
              <AlertItem
                key={alert.id}
                type={alert.type as 'success' | 'warning' | 'critical'}
                message={alert.message}
                time={alert.time}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManagementDashboard;
