import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { liveClasses } from '@/data/mockData';
import { Video, Users, Activity, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

const LiveMonitoring = () => {
  const [selectedClass, setSelectedClass] = useState<typeof liveClasses[0] | null>(null);

  const getPulseColor = (pulse: string) => {
    switch (pulse) {
      case 'green': return 'bg-success';
      case 'yellow': return 'bg-warning';
      case 'red': return 'bg-destructive';
      default: return 'bg-muted';
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Real-Time Classroom Intelligence
          </h1>
          <p className="text-muted-foreground">
            Monitor ongoing classes and get instant insights on engagement and understanding
          </p>
        </div>

        {/* Live Classes Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {liveClasses.map((classItem) => (
            <Card key={classItem.id} className="p-6 hover:shadow-lg transition-smooth">
              {/* Header with Live Indicator */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className={cn("w-3 h-3 rounded-full animate-pulse", getPulseColor(classItem.tisPulse))} />
                  <Badge variant="outline" className="gap-1">
                    <Video className="h-3 w-3" />
                    LIVE
                  </Badge>
                </div>
                <Badge variant="secondary">{classItem.class}</Badge>
              </div>

              {/* Class Info */}
              <h3 className="font-heading font-semibold text-lg mb-1">{classItem.subject}</h3>
              <p className="text-sm text-muted-foreground mb-1">{classItem.teacher}</p>
              <p className="text-sm text-muted-foreground mb-4">{classItem.topic}</p>

              {/* Metrics */}
              <div className="space-y-3 mb-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm flex items-center gap-2">
                    <Activity className="h-4 w-4 text-primary" />
                    Engagement
                  </span>
                  <span className="font-semibold text-primary">{classItem.engagement}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm flex items-center gap-2">
                    <Users className="h-4 w-4 text-secondary" />
                    Confusion Index
                  </span>
                  <span className="font-semibold text-secondary">{classItem.confusion}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm flex items-center gap-2">
                    <Clock className="h-4 w-4 text-accent" />
                    Pace
                  </span>
                  <Badge
                    variant={classItem.pace === 'Optimal' ? 'default' : 'outline'}
                    className={classItem.pace !== 'Optimal' ? 'border-warning text-warning' : ''}
                  >
                    {classItem.pace}
                  </Badge>
                </div>
              </div>

              {/* TIS Pulse Status */}
              <div className="pt-3 border-t mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">TIS Pulse:</span>
                  <Badge className={cn(
                    classItem.tisPulse === 'green' && 'bg-success',
                    classItem.tisPulse === 'yellow' && 'bg-warning',
                    classItem.tisPulse === 'red' && 'bg-destructive'
                  )}>
                    {classItem.tisPulse.toUpperCase()}
                  </Badge>
                </div>
              </div>

              {/* Action Button */}
              <Button
                variant="outline"
                className="w-full"
                onClick={() => setSelectedClass(classItem)}
              >
                View Detailed Metrics
              </Button>
            </Card>
          ))}
        </div>

        {/* Detailed Metrics Modal */}
        <Dialog open={!!selectedClass} onOpenChange={() => setSelectedClass(null)}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle className="font-heading text-2xl">
                {selectedClass?.subject} - Class {selectedClass?.class}
              </DialogTitle>
              <DialogDescription>
                {selectedClass?.teacher} • {selectedClass?.topic}
              </DialogDescription>
            </DialogHeader>
            {selectedClass && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <Card className="p-4">
                    <p className="text-sm text-muted-foreground mb-1">Engagement Score</p>
                    <p className="text-3xl font-bold text-primary">{selectedClass.engagement}%</p>
                  </Card>
                  <Card className="p-4">
                    <p className="text-sm text-muted-foreground mb-1">Confusion Index</p>
                    <p className="text-3xl font-bold text-secondary">{selectedClass.confusion}%</p>
                  </Card>
                  <Card className="p-4">
                    <p className="text-sm text-muted-foreground mb-1">Student Count</p>
                    <p className="text-3xl font-bold text-accent">{selectedClass.studentCount}</p>
                  </Card>
                  <Card className="p-4">
                    <p className="text-sm text-muted-foreground mb-1">Pace Status</p>
                    <p className="text-xl font-bold text-info">{selectedClass.pace}</p>
                  </Card>
                </div>
                <Card className="p-4">
                  <p className="text-sm font-medium mb-2">AI Recommendations:</p>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Consider slowing down if confusion rises above 40%</li>
                    <li>• Engagement is {selectedClass.engagement > 80 ? 'excellent' : 'moderate'} - keep current approach</li>
                    <li>• {selectedClass.pace !== 'Optimal' && 'Adjust teaching pace based on student feedback'}</li>
                  </ul>
                </Card>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default LiveMonitoring;
