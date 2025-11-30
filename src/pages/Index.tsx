import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { GraduationCap, TrendingUp, Users, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import heroImage from '@/assets/hero-education.jpg';

const Index = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/5 via-background to-secondary/5">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="inline-block px-4 py-2 bg-primary/10 rounded-full text-primary font-medium text-sm">
                AI-Powered Teaching Excellence
              </div>
              <h1 className="text-4xl md:text-6xl font-bold font-heading leading-tight">
                Welcome to{' '}
                <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  Shikshak Mitra AI
                </span>
              </h1>
              <p className="text-xl text-muted-foreground">
                Empowering Smarter Teaching Through Data-Driven Insights & AI Coaching
              </p>
              <div className="flex flex-wrap gap-4">
                <Button size="lg" className="gradient-primary shadow-primary" asChild>
                  <Link to="/teacher-dashboard">Get Started</Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link to="/management-dashboard">View Demo</Link>
                </Button>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 to-secondary/20 blur-3xl" />
              <img
                src={heroImage}
                alt="Educational Technology"
                className="relative rounded-2xl shadow-2xl w-full"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 md:py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold font-heading mb-4">
              Why Choose Shikshak Mitra AI?
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Transform your teaching with real-time analytics, AI-powered coaching, and data-driven insights
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="rounded-full p-3 bg-primary/10 w-fit mb-4">
                <TrendingUp className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-heading font-semibold text-xl mb-2">
                Teacher Impact Score
              </h3>
              <p className="text-muted-foreground">
                Track your teaching effectiveness with comprehensive metrics and trends
              </p>
            </Card>

            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="rounded-full p-3 bg-secondary/10 w-fit mb-4">
                <Zap className="h-6 w-6 text-secondary" />
              </div>
              <h3 className="font-heading font-semibold text-xl mb-2">
                AI Coaching
              </h3>
              <p className="text-muted-foreground">
                Get personalized suggestions to improve engagement and retention
              </p>
            </Card>

            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="rounded-full p-3 bg-accent/10 w-fit mb-4">
                <Users className="h-6 w-6 text-accent" />
              </div>
              <h3 className="font-heading font-semibold text-xl mb-2">
                Student Analytics
              </h3>
              <p className="text-muted-foreground">
                Understand student behavior, confusion points, and learning patterns
              </p>
            </Card>

            <Card className="p-6 hover:shadow-lg transition-smooth">
              <div className="rounded-full p-3 bg-info/10 w-fit mb-4">
                <GraduationCap className="h-6 w-6 text-info" />
              </div>
              <h3 className="font-heading font-semibold text-xl mb-2">
                Smart Activities
              </h3>
              <p className="text-muted-foreground">
                Generate industry-aligned projects and assignments instantly
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4">
          <Card className="p-8 md:p-12 gradient-hero text-primary-foreground text-center">
            <h2 className="text-3xl md:text-4xl font-bold font-heading mb-4">
              Ready to Transform Your Teaching?
            </h2>
            <p className="text-lg mb-8 opacity-90 max-w-2xl mx-auto">
              Join thousands of educators using AI to create better learning experiences
            </p>
            <Button size="lg" variant="secondary" className="shadow-lg" asChild>
              <Link to="/teacher-dashboard">Start Your Journey</Link>
            </Button>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;
