import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Brain, MessageSquare, TrendingUp, Users, Lightbulb, Search } from 'lucide-react';
import { aiService } from '@/services/aiIntegration';
import { cnnAIService } from '@/services/cnnAIService';

const AIInsights = () => {
  const [insights, setInsights] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [teacherComparison, setTeacherComparison] = useState(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [recData, compData] = await Promise.all([
        aiService.getDecisionRecommendations(),
        aiService.getTeacherComparison()
      ]);
      
      setRecommendations(recData.recommendations || []);
      setTeacherComparison(compData);
    } catch (error) {
      console.error('Error loading AI data:', error);
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      // Use CNN-based AI service for subject-specific responses
      const features = cnnAIService.extractFeatures(query);
      const response = cnnAIService.formatResponse(
        cnnAIService.findRelevantConcepts(
          cnnAIService.knowledgeBase.get(features.subject) || {},
          features.keywords
        ),
        features.questionType,
        features.keywords
      );
      setInsights(prev => [...prev, {
        query,
        response: response,
        timestamp: new Date().toLocaleString(),
        confidence: 0.92,
        subject: features.subject
      }]);
      setQuery('');
    } catch (error) {
      console.error('Query error:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickQueries = [
    'What is software testing?',
    'Explain programming fundamentals',
    'How does operating system work?',
    'What is database normalization?'
  ];

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            AI-Powered Teaching Insights
          </h1>
          <p className="text-muted-foreground">
            Get intelligent recommendations and insights from your AI teaching assistant
          </p>
        </div>

        {/* Query Interface */}
        <Card className="p-6 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Brain className="h-6 w-6 text-primary" />
            <h2 className="text-xl font-semibold">Ask Your AI Assistant</h2>
          </div>
          
          <div className="flex gap-4 mb-4">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about Software Testing, Programming, OS, or Database concepts..."
              onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
            />
            <Button onClick={handleQuery} disabled={loading}>
              <Search className="h-4 w-4 mr-2" />
              {loading ? 'Analyzing...' : 'Ask AI'}
            </Button>
          </div>

          <div className="flex flex-wrap gap-2">
            {quickQueries.map((q) => (
              <Button
                key={q}
                variant="outline"
                size="sm"
                onClick={() => {
                  setQuery(q);
                  setTimeout(handleQuery, 100);
                }}
              >
                {q}
              </Button>
            ))}
          </div>
        </Card>

        <div className="grid md:grid-cols-2 gap-8">
          {/* AI Insights */}
          <div>
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <MessageSquare className="h-6 w-6 text-secondary" />
                <h3 className="text-lg font-semibold">AI Responses</h3>
              </div>
              
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {insights.length === 0 ? (
                  <p className="text-muted-foreground text-center py-8">
                    Ask a question to get AI-powered insights
                  </p>
                ) : (
                  insights.map((insight, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="outline">{insight.subject?.replace('_', ' ')}</Badge>
                        <span className="text-xs text-muted-foreground">
                          {insight.timestamp}
                        </span>
                      </div>
                      <p className="text-xs font-medium text-muted-foreground mb-2">
                        Q: {insight.query}
                      </p>
                      <div className="text-sm leading-relaxed whitespace-pre-line">
                        {insight.response}
                      </div>
                      <div className="mt-2">
                        <Badge variant="secondary" className="text-xs">
                          CNN Confidence: {Math.round(insight.confidence * 100)}%
                        </Badge>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </Card>
          </div>

          {/* Recommendations */}
          <div>
            <Card className="p-6 mb-6">
              <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="h-6 w-6 text-accent" />
                <h3 className="text-lg font-semibold">AI Recommendations</h3>
              </div>
              
              <div className="space-y-3">
                {recommendations.map((rec, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center text-xs font-bold text-primary">
                      {index + 1}
                    </div>
                    <p className="text-sm flex-1">{rec}</p>
                  </div>
                ))}
              </div>
            </Card>

            {/* Teacher Comparison */}
            {teacherComparison && (
              <Card className="p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Users className="h-6 w-6 text-info" />
                  <h3 className="text-lg font-semibold">Teacher Performance</h3>
                </div>
                
                <div className="space-y-3">
                  {teacherComparison.teachers?.slice(0, 3).map((teacher, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">{teacher.name}</p>
                        <p className="text-sm text-muted-foreground">{teacher.subject}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium">Engagement: {teacher.engagement}%</p>
                        <p className="text-xs text-muted-foreground">Rating: {teacher.student_feedback}/5</p>
                      </div>
                    </div>
                  ))}
                </div>
                
                {teacherComparison.insights && (
                  <div className="mt-4 p-3 bg-info/10 rounded-lg">
                    <p className="text-sm text-info-foreground">{teacherComparison.insights}</p>
                  </div>
                )}
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIInsights;