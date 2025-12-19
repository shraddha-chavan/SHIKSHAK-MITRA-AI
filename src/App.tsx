import { useState, useEffect } from 'react';
import { Toaster } from '@/components/ui/toaster';
import { Toaster as Sonner } from '@/components/ui/sonner';
import { TooltipProvider } from '@/components/ui/tooltip';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from '@/components/Navbar';
import VoiceAssistant from '@/components/VoiceAssistant';
import Index from './pages/Index';
import TeacherDashboard from './pages/TeacherDashboard';
import TeacherAnalytics from './pages/TeacherAnalytics';
import TeacherScoring from './pages/TeacherScoring';
import AIInsights from './pages/AIInsights';
import TeacherFeedback from './pages/TeacherFeedback';
import ManagementDashboard from './pages/ManagementDashboard';
import TeacherComparison from './pages/TeacherComparison';
import IndustryAlignment from './pages/IndustryAlignment';
import LiveMonitoring from './pages/LiveMonitoring';
import Reports from './pages/Reports';
import NotFound from './pages/NotFound';

const queryClient = new QueryClient();

const App = () => {
  const [role, setRole] = useState<'teacher' | 'admin'>('teacher');

  useEffect(() => {
    // Auto-enable voice when in teacher mode
    if (role === 'teacher') {
      import('./services/voiceService').then(({ voiceService }) => {
        setTimeout(() => voiceService.enable(), 1000);
      });
    }
  }, [role]);

  const toggleRole = () => {
    setRole(prev => prev === 'teacher' ? 'admin' : 'teacher');
  };

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <div className="min-h-screen flex flex-col">
            <Navbar role={role} onRoleToggle={toggleRole} />
            <main className="flex-1">
              <Routes>
                <Route path="/" element={<Index />} />
                <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
                <Route path="/teacher-analytics" element={<TeacherAnalytics />} />
                <Route path="/teacher-scoring" element={<TeacherScoring />} />
                <Route path="/ai-insights" element={<AIInsights />} />
                <Route path="/teacher-feedback" element={<TeacherFeedback />} />
                <Route path="/management-dashboard" element={<ManagementDashboard />} />
                <Route path="/teacher-comparison" element={<TeacherComparison />} />
                <Route path="/industry-alignment" element={<IndustryAlignment />} />
                <Route path="/live-monitoring" element={<LiveMonitoring />} />
                <Route path="/reports" element={<Reports />} />
                {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </main>
            
            {/* Voice Assistant - only show in teacher mode */}
            {role === 'teacher' && <VoiceAssistant />}
          </div>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
