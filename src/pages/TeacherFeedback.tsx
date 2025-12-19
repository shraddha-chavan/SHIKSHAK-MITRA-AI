import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { MessageSquare, Send } from 'lucide-react';

const TeacherFeedback = () => {
  const { toast } = useToast();
  const [feedback, setFeedback] = useState({
    student_name: '',
    student_id: '',
    teacher_name: '',
    subject: '',
    class_section: '',
    rating: '',
    feedback_type: '',
    message: '',
    suggestions: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!feedback.subject || !feedback.rating || !feedback.feedback_type) {
      toast({
        title: "Missing Fields",
        description: "Please fill in all required fields.",
        variant: "destructive",
      });
      return;
    }
    
    try {
      const response = await fetch('http://localhost:3001/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...feedback,
          timestamp: new Date().toISOString(),
          date: new Date().toLocaleDateString()
        }),
      });

      if (response.ok) {
        toast({
          title: "Feedback Submitted",
          description: "Thank you for your feedback!",
        });
        
        setFeedback({
          student_name: '',
          student_id: '',
          teacher_name: '',
          subject: '',
          class_section: '',
          rating: '',
          feedback_type: '',
          message: '',
          suggestions: ''
        });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to submit feedback');
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit feedback. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFeedback(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold font-heading mb-2">
            Student Feedback System
          </h1>
          <p className="text-muted-foreground">
            Share your learning experience and help improve teaching quality
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-6">
              <MessageSquare className="h-6 w-6 text-primary" />
              <h2 className="text-xl font-semibold">Rate Your Teacher</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="student_name">Your Name</Label>
                  <Input
                    id="student_name"
                    value={feedback.student_name}
                    onChange={(e) => handleInputChange('student_name', e.target.value)}
                    placeholder="Enter your name"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="student_id">Student ID</Label>
                  <Input
                    id="student_id"
                    value={feedback.student_id}
                    onChange={(e) => handleInputChange('student_id', e.target.value)}
                    placeholder="Enter your student ID"
                    required
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="teacher_name">Teacher Name</Label>
                  <Input
                    id="teacher_name"
                    value={feedback.teacher_name}
                    onChange={(e) => handleInputChange('teacher_name', e.target.value)}
                    placeholder="Enter teacher's name"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="subject">Subject *</Label>
                  <Select value={feedback.subject} onValueChange={(value) => handleInputChange('subject', value)} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Select subject" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="mathematics">Mathematics</SelectItem>
                      <SelectItem value="science">Science</SelectItem>
                      <SelectItem value="english">English</SelectItem>
                      <SelectItem value="history">History</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="class_section">Class/Section</Label>
                  <Input
                    id="class_section"
                    value={feedback.class_section}
                    onChange={(e) => handleInputChange('class_section', e.target.value)}
                    placeholder="e.g., 10-A, 12-B"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="rating">Rate Your Teacher *</Label>
                  <Select value={feedback.rating} onValueChange={(value) => handleInputChange('rating', value)} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Rate your teacher" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="5">⭐⭐⭐⭐⭐ Excellent</SelectItem>
                      <SelectItem value="4">⭐⭐⭐⭐ Good</SelectItem>
                      <SelectItem value="3">⭐⭐⭐ Average</SelectItem>
                      <SelectItem value="2">⭐⭐ Poor</SelectItem>
                      <SelectItem value="1">⭐ Very Poor</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="feedback_type">Feedback Category *</Label>
                <Select value={feedback.feedback_type} onValueChange={(value) => handleInputChange('feedback_type', value)} required>
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="teaching_method">Teaching Method</SelectItem>
                    <SelectItem value="explanation_clarity">Explanation Clarity</SelectItem>
                    <SelectItem value="interaction">Teacher Interaction</SelectItem>
                    <SelectItem value="pace">Teaching Pace</SelectItem>
                    <SelectItem value="engagement">Class Engagement</SelectItem>
                    <SelectItem value="general">General Feedback</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="message">Your Feedback</Label>
                <Textarea
                  id="message"
                  value={feedback.message}
                  onChange={(e) => handleInputChange('message', e.target.value)}
                  placeholder="Share your experience about the teacher and class..."
                  rows={4}
                  required
                />
              </div>

              <div>
                <Label htmlFor="suggestions">Suggestions for Teacher</Label>
                <Textarea
                  id="suggestions"
                  value={feedback.suggestions}
                  onChange={(e) => handleInputChange('suggestions', e.target.value)}
                  placeholder="Any suggestions to help your teacher improve?"
                  rows={3}
                />
              </div>

              <Button type="submit" className="w-full" size="lg">
                <Send className="h-4 w-4 mr-2" />
                Submit Feedback
              </Button>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default TeacherFeedback;