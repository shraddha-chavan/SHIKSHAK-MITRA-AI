import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, Download, Calendar, TrendingUp, Users, Award } from 'lucide-react';
import { toast } from 'sonner';

const reportTypes = [
  {
    icon: TrendingUp,
    title: 'Teacher Performance Report',
    description: 'Comprehensive analysis of teacher impact scores, retention, and engagement metrics',
    formats: ['PDF', 'CSV']
  },
  {
    icon: Users,
    title: 'Student Analytics Report',
    description: 'Detailed student cohort analysis, retention curves, and confusion heatmaps',
    formats: ['PDF', 'Excel']
  },
  {
    icon: Award,
    title: 'Institution Health Report',
    description: 'Overall institutional metrics, department performance, and growth trends',
    formats: ['PDF', 'PPT']
  },
  {
    icon: Calendar,
    title: 'Monthly Summary Report',
    description: 'Month-over-month comparison of key metrics and actionable insights',
    formats: ['PDF', 'Email']
  },
];

const Reports = () => {
  const handleExport = (reportTitle: string, format: string) => {
    toast.success(`Generating ${reportTitle} in ${format} format...`, {
      description: 'This is a mock action. In production, the report would be generated.'
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Smart Reports for Smart Decisions
          </h1>
          <p className="text-muted-foreground">
            Export comprehensive reports in multiple formats for data-driven decision making
          </p>
        </div>

        {/* Report Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {reportTypes.map((report, idx) => (
            <Card key={idx} className="p-6 hover:shadow-lg transition-smooth">
              <div className="flex items-start gap-4 mb-4">
                <div className="rounded-full p-3 bg-primary/10">
                  <report.icon className="h-6 w-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-heading font-semibold text-lg mb-1">{report.title}</h3>
                  <p className="text-sm text-muted-foreground">{report.description}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2 pt-3 border-t">
                {report.formats.map((format) => (
                  <Button
                    key={format}
                    variant="outline"
                    size="sm"
                    onClick={() => handleExport(report.title, format)}
                    className="gap-2"
                  >
                    <Download className="h-4 w-4" />
                    Export as {format}
                  </Button>
                ))}
              </div>
            </Card>
          ))}
        </div>

        {/* Custom Report Generator */}
        <Card className="p-6 gradient-primary text-primary-foreground">
          <div className="flex items-start gap-4">
            <FileText className="h-8 w-8 mt-1" />
            <div className="flex-1">
              <h2 className="text-2xl font-heading font-bold mb-2">Custom Report Generator</h2>
              <p className="mb-4 opacity-90">
                Create custom reports with specific metrics, date ranges, and filters tailored to your needs
              </p>
              <Button
                variant="secondary"
                size="lg"
                onClick={() => toast.info('Custom report builder coming soon!')}
              >
                <FileText className="h-5 w-5 mr-2" />
                Build Custom Report
              </Button>
            </div>
          </div>
        </Card>

        {/* Quick Export Section */}
        <Card className="p-6 mt-6">
          <h3 className="font-heading font-semibold text-lg mb-4">Quick Export Options</h3>
          <div className="grid md:grid-cols-3 gap-3">
            <Button
              variant="outline"
              onClick={() => toast.success('Exporting today\'s data...')}
              className="justify-start"
            >
              <Download className="h-4 w-4 mr-2" />
              Today's Data
            </Button>
            <Button
              variant="outline"
              onClick={() => toast.success('Exporting this week\'s data...')}
              className="justify-start"
            >
              <Download className="h-4 w-4 mr-2" />
              This Week
            </Button>
            <Button
              variant="outline"
              onClick={() => toast.success('Exporting this month\'s data...')}
              className="justify-start"
            >
              <Download className="h-4 w-4 mr-2" />
              This Month
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Reports;
