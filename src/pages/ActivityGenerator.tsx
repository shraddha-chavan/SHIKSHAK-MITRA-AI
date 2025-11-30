import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ciActivities, practicalTasks } from '@/data/mockData';
import { Sparkles, Clock, Award, Code } from 'lucide-react';

const ActivityGenerator = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Smart Activities for Smarter Learning
          </h1>
          <p className="text-muted-foreground">
            AI-generated projects and assignments aligned with industry standards
          </p>
        </div>

        {/* CI Activities (20 Marks) */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Award className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-heading font-bold">CI Activities (20 Marks)</h2>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ciActivities.map((activity) => (
              <Card key={activity.id} className="p-6 hover:shadow-lg transition-smooth">
                <div className="flex items-start justify-between mb-3">
                  <Badge className="gradient-primary text-primary-foreground">
                    {activity.marks} Marks
                  </Badge>
                  <Badge variant="outline">{activity.duration}</Badge>
                </div>
                <h3 className="font-heading font-semibold text-lg mb-3">{activity.title}</h3>
                <p className="text-sm text-muted-foreground mb-4">{activity.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {activity.skills.map((skill, idx) => (
                    <Badge key={idx} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
                <Button className="w-full gradient-primary text-primary-foreground" size="sm">
                  <Sparkles className="h-4 w-4 mr-2" />
                  Generate Similar
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* 15-Minute Practical Tasks */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Clock className="h-6 w-6 text-accent" />
            <h2 className="text-2xl font-heading font-bold">15-Minute Practical Tasks</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            {practicalTasks.map((task) => (
              <Card key={task.id} className="p-6 hover:shadow-lg transition-smooth">
                <div className="flex items-center gap-3 mb-3">
                  <div className="rounded-full p-2 bg-accent/10">
                    <Code className="h-5 w-5 text-accent" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-heading font-semibold">{task.title}</h3>
                    <p className="text-sm text-muted-foreground">{task.duration}</p>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-4">{task.description}</p>
                <Button variant="outline" className="w-full" size="sm">
                  Generate Task
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* Non-Copyable Assignments */}
        <Card className="p-6 gradient-secondary text-secondary-foreground">
          <h2 className="text-2xl font-heading font-bold mb-3">Non-Copyable Assignments</h2>
          <p className="mb-4 opacity-90">
            Generate unique assignments for each student that prevent plagiarism and encourage original thinking
          </p>
          <Button variant="secondary" size="lg">
            <Sparkles className="h-5 w-5 mr-2" />
            Generate Assignment Set
          </Button>
        </Card>
      </div>
    </div>
  );
};

export default ActivityGenerator;
