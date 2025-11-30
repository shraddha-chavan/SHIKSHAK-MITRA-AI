// Mock data for Shikshak Mitra AI

export const teacherMetrics = {
  impactScore: 87,
  retention: 92,
  engagement: 85,
  curiosityIndex: 78,
  trend: '+12%',
  alerts: [
    { id: 1, type: 'warning', message: 'Class 10B engagement dropped by 8%', time: '2h ago' },
    { id: 2, type: 'success', message: 'Class 12A retention improved by 15%', time: '5h ago' },
  ]
};

export const analyticsData = {
  retentionCurve: [
    { week: 'Week 1', retention: 95 },
    { week: 'Week 2', retention: 92 },
    { week: 'Week 3', retention: 90 },
    { week: 'Week 4', retention: 88 },
    { week: 'Week 5', retention: 89 },
    { week: 'Week 6', retention: 91 },
  ],
  confusionHeatmap: [
    { topic: 'Variables', confusion: 15 },
    { topic: 'Functions', confusion: 35 },
    { topic: 'Loops', confusion: 28 },
    { topic: 'Objects', confusion: 42 },
    { topic: 'Arrays', confusion: 22 },
  ],
  cohorts: [
    { name: 'High Performers', count: 12, avg: 92 },
    { name: 'Medium Performers', count: 18, avg: 76 },
    { name: 'Needs Support', count: 8, avg: 58 },
  ],
};

export const aiCoachSuggestions = [
  {
    id: 1,
    title: 'Improve Engagement in Class 10B',
    suggestion: 'Consider incorporating more interactive activities. Students respond well to group discussions.',
    before: 75,
    after: 85,
    impact: 'High'
  },
  {
    id: 2,
    title: 'Reduce Confusion on Objects Topic',
    suggestion: 'Use real-world analogies and practical examples when teaching object-oriented concepts.',
    before: 42,
    after: 28,
    impact: 'Medium'
  },
];

export const ciActivities = [
  {
    id: 1,
    title: 'Design a Smart Home System',
    marks: 20,
    duration: '2 weeks',
    description: 'Create a prototype for an IoT-based smart home system with sensors and automation.',
    skills: ['IoT', 'Programming', 'Design Thinking']
  },
  {
    id: 2,
    title: 'Build a Task Management App',
    marks: 20,
    duration: '10 days',
    description: 'Develop a web application for task management with user authentication and CRUD operations.',
    skills: ['Web Development', 'Database', 'UI/UX']
  },
  {
    id: 3,
    title: 'Create a Chatbot for Student Queries',
    marks: 20,
    duration: '15 days',
    description: 'Build an AI-powered chatbot to answer common student queries about the curriculum.',
    skills: ['AI/ML', 'NLP', 'Python']
  },
];

export const practicalTasks = [
  {
    id: 1,
    title: 'Debug the Login System',
    duration: '15 minutes',
    description: 'Fix authentication bugs in the provided codebase.',
  },
  {
    id: 2,
    title: 'Optimize Database Query',
    duration: '15 minutes',
    description: 'Improve the performance of a slow SQL query.',
  },
];

export const managementMetrics = {
  healthScore: 84,
  totalTeachers: 45,
  avgRetention: 88,
  avgEngagement: 82,
  topTeachers: [
    { name: 'Dr. Priya Sharma', subject: 'Computer Science', score: 94 },
    { name: 'Prof. Rajesh Kumar', subject: 'Mathematics', score: 92 },
    { name: 'Ms. Anita Desai', subject: 'Physics', score: 90 },
  ],
  bottomTeachers: [
    { name: 'Mr. Amit Verma', subject: 'Chemistry', score: 65 },
    { name: 'Ms. Neha Singh', subject: 'Biology', score: 68 },
  ],
  alerts: [
    { id: 1, type: 'critical', message: 'Chemistry department retention dropped 15%', time: '1h ago' },
    { id: 2, type: 'warning', message: 'Need 2 more teachers for new batch', time: '3h ago' },
  ]
};

export const teacherComparison = [
  {
    name: 'Dr. Priya Sharma',
    subject: 'Computer Science',
    impactScore: 94,
    retention: 95,
    engagement: 92,
    subjectFit: 98,
    experience: '12 years'
  },
  {
    name: 'Prof. Rajesh Kumar',
    subject: 'Mathematics',
    impactScore: 92,
    retention: 93,
    engagement: 90,
    subjectFit: 96,
    experience: '15 years'
  },
  {
    name: 'Ms. Anita Desai',
    subject: 'Physics',
    impactScore: 90,
    retention: 91,
    engagement: 88,
    subjectFit: 94,
    experience: '8 years'
  },
];

export const industryAlignment = [
  {
    id: 1,
    subject: 'Data Science & AI',
    demand: 'Very High',
    readyTeachers: 3,
    trainingNeeded: 5,
    priority: 'Critical'
  },
  {
    id: 2,
    subject: 'Cloud Computing',
    demand: 'High',
    readyTeachers: 2,
    trainingNeeded: 4,
    priority: 'High'
  },
  {
    id: 3,
    subject: 'Cybersecurity',
    demand: 'High',
    readyTeachers: 1,
    trainingNeeded: 6,
    priority: 'High'
  },
];

export const liveClasses = [
  {
    id: 1,
    teacher: 'Dr. Priya Sharma',
    subject: 'Computer Science',
    class: '12A',
    topic: 'Object Oriented Programming',
    startTime: '10:00 AM',
    engagement: 88,
    confusion: 22,
    pace: 'Optimal',
    tisPulse: 'green',
    studentCount: 35
  },
  {
    id: 2,
    teacher: 'Prof. Rajesh Kumar',
    subject: 'Mathematics',
    class: '11B',
    topic: 'Calculus - Derivatives',
    startTime: '11:00 AM',
    engagement: 75,
    confusion: 35,
    pace: 'Too Fast',
    tisPulse: 'yellow',
    studentCount: 32
  },
  {
    id: 3,
    teacher: 'Ms. Anita Desai',
    subject: 'Physics',
    class: '12C',
    topic: 'Quantum Mechanics',
    startTime: '12:00 PM',
    engagement: 65,
    confusion: 48,
    pace: 'Too Slow',
    tisPulse: 'red',
    studentCount: 28
  },
];
