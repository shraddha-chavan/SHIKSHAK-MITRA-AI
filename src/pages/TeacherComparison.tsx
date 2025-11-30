import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { teacherComparison } from '@/data/mockData';
import { Users, Award, Target } from 'lucide-react';

const TeacherComparison = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Find the Right Teacher for the Right Subject
          </h1>
          <p className="text-muted-foreground">
            Compare teachers side-by-side with AI-powered subject fit analysis
          </p>
        </div>

        {/* Teacher Comparison Table */}
        <Card className="p-6 mb-8 overflow-x-auto">
          <div className="flex items-center gap-2 mb-4">
            <Users className="h-5 w-5 text-primary" />
            <h3 className="text-xl font-heading font-semibold">Teacher Comparison</h3>
          </div>
          <div className="min-w-[800px]">
            <div className="grid grid-cols-7 gap-4 mb-4 pb-3 border-b font-semibold">
              <div>Teacher</div>
              <div>Subject</div>
              <div>Impact Score</div>
              <div>Retention</div>
              <div>Engagement</div>
              <div>Subject Fit</div>
              <div>Experience</div>
            </div>
            {teacherComparison.map((teacher, idx) => (
              <div key={idx} className="grid grid-cols-7 gap-4 py-3 border-b last:border-0 hover:bg-muted/30 transition-smooth">
                <div className="font-medium">{teacher.name}</div>
                <div className="text-sm text-muted-foreground">{teacher.subject}</div>
                <div>
                  <Badge className="gradient-primary text-primary-foreground">
                    {teacher.impactScore}
                  </Badge>
                </div>
                <div className="text-secondary font-semibold">{teacher.retention}%</div>
                <div className="text-accent font-semibold">{teacher.engagement}%</div>
                <div>
                  <Badge variant={teacher.subjectFit >= 95 ? 'default' : 'secondary'}>
                    {teacher.subjectFit}%
                  </Badge>
                </div>
                <div className="text-sm text-muted-foreground">{teacher.experience}</div>
              </div>
            ))}
          </div>
        </Card>

        {/* AI Subject Fit Recommendations */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Target className="h-6 w-6 text-accent" />
            <h2 className="text-2xl font-heading font-bold">AI Recommendations</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="flex items-start gap-3">
                <Award className="h-6 w-6 text-primary mt-1" />
                <div>
                  <h4 className="font-semibold mb-2">Best Fit for New AI/ML Course</h4>
                  <p className="text-sm text-muted-foreground mb-3">
                    Based on technical background, teaching style, and student feedback analysis
                  </p>
                  <div className="flex items-center gap-2">
                    <Badge className="gradient-primary text-primary-foreground">
                      Dr. Priya Sharma
                    </Badge>
                    <span className="text-xs text-muted-foreground">98% Subject Fit Score</span>
                  </div>
                </div>
              </div>
            </Card>

            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="flex items-start gap-3">
                <Award className="h-6 w-6 text-secondary mt-1" />
                <div>
                  <h4 className="font-semibold mb-2">Best Fit for Advanced Mathematics</h4>
                  <p className="text-sm text-muted-foreground mb-3">
                    Strong analytical approach and proven track record with complex topics
                  </p>
                  <div className="flex items-center gap-2">
                    <Badge className="gradient-secondary text-secondary-foreground">
                      Prof. Rajesh Kumar
                    </Badge>
                    <span className="text-xs text-muted-foreground">96% Subject Fit Score</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherComparison;
