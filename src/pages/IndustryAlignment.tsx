import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { industryAlignment } from '@/data/mockData';
import { TrendingUp, Users, AlertCircle } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

const IndustryAlignment = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Stay Ahead With Industry-Ready Courses
          </h1>
          <p className="text-muted-foreground">
            Identify emerging subjects and assess teacher readiness for industry alignment
          </p>
        </div>

        {/* Industry Demand Overview */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {industryAlignment.map((subject) => (
            <Card key={subject.id} className="p-6 hover:shadow-lg transition-smooth">
              <div className="flex items-start justify-between mb-3">
                <Badge
                  variant={subject.priority === 'Critical' ? 'destructive' : 'default'}
                  className={subject.priority === 'High' ? 'gradient-accent text-accent-foreground' : ''}
                >
                  {subject.priority}
                </Badge>
                <TrendingUp className="h-5 w-5 text-success" />
              </div>
              <h3 className="font-heading font-semibold text-lg mb-2">{subject.subject}</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Industry Demand: <span className="font-semibold text-foreground">{subject.demand}</span>
              </p>
              
              <div className="space-y-3 mb-4">
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm flex items-center gap-1">
                      <Users className="h-4 w-4 text-success" />
                      Ready Teachers
                    </span>
                    <span className="text-sm font-semibold">{subject.readyTeachers}</span>
                  </div>
                  <Progress value={subject.readyTeachers * 10} className="h-2" />
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm flex items-center gap-1">
                      <AlertCircle className="h-4 w-4 text-warning" />
                      Training Needed
                    </span>
                    <span className="text-sm font-semibold">{subject.trainingNeeded}</span>
                  </div>
                  <Progress value={subject.trainingNeeded * 10} className="h-2" />
                </div>
              </div>

              <div className="pt-3 border-t">
                <p className="text-xs text-muted-foreground">
                  Total Gap: {subject.trainingNeeded} teachers need upskilling
                </p>
              </div>
            </Card>
          ))}
        </div>

        {/* Recommendations */}
        <Card className="p-6 gradient-hero text-primary-foreground">
          <h2 className="text-2xl font-heading font-bold mb-4">Action Items</h2>
          <ul className="space-y-2 opacity-90">
            <li className="flex items-start gap-2">
              <span className="text-xl">•</span>
              <span>Prioritize training for Data Science & AI - 5 teachers require immediate upskilling</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-xl">•</span>
              <span>Cloud Computing certification program recommended for 4 teachers</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-xl">•</span>
              <span>Consider hiring specialist for Cybersecurity to meet industry demand</span>
            </li>
          </ul>
        </Card>
      </div>
    </div>
  );
};

export default IndustryAlignment;
