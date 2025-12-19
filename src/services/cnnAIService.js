class CNNAIService {
  constructor() {
    this.knowledgeBase = new Map();
    this.loadKnowledgeBase();
  }

  async loadKnowledgeBase() {
    const subjects = [
      'software_testing',
      'programming_fundamentals', 
      'system_programming',
      'database_management'
    ];

    for (const subject of subjects) {
      try {
        const response = await fetch(`/Subject_Knowledge_Base/${subject}.json`);
        const data = await response.json();
        this.knowledgeBase.set(subject, data);
      } catch (error) {
        console.error(`Failed to load ${subject}:`, error);
      }
    }
  }

  // CNN-inspired text processing
  extractFeatures(question) {
    const keywords = question.toLowerCase().split(/\s+/);
    const features = {
      subject: this.detectSubject(keywords),
      topic: this.detectTopic(keywords),
      questionType: this.detectQuestionType(keywords),
      keywords: keywords.filter(word => word.length > 3)
    };
    return features;
  }

  detectSubject(keywords) {
    const subjectKeywords = {
      software_testing: ['test', 'testing', 'bug', 'defect', 'quality', 'verification'],
      programming_fundamentals: ['program', 'code', 'variable', 'function', 'loop', 'algorithm'],
      system_programming: ['process', 'thread', 'memory', 'kernel', 'operating', 'system'],
      database_management: ['database', 'sql', 'table', 'query', 'data', 'dbms']
    };

    let maxScore = 0;
    let detectedSubject = 'programming_fundamentals';

    for (const [subject, subjectWords] of Object.entries(subjectKeywords)) {
      const score = keywords.filter(word => subjectWords.includes(word)).length;
      if (score > maxScore) {
        maxScore = score;
        detectedSubject = subject;
      }
    }

    return detectedSubject;
  }

  detectTopic(keywords) {
    const topicKeywords = {
      fundamentals: ['basic', 'fundamental', 'introduction', 'concept'],
      advanced: ['advanced', 'complex', 'optimization', 'performance'],
      practical: ['example', 'implement', 'code', 'practice']
    };

    for (const [topic, words] of Object.entries(topicKeywords)) {
      if (keywords.some(word => words.includes(word))) {
        return topic;
      }
    }
    return 'fundamentals';
  }

  detectQuestionType(keywords) {
    if (keywords.some(word => ['what', 'define', 'explain'].includes(word))) {
      return 'definition';
    }
    if (keywords.some(word => ['how', 'implement', 'create'].includes(word))) {
      return 'implementation';
    }
    if (keywords.some(word => ['why', 'advantage', 'benefit'].includes(word))) {
      return 'explanation';
    }
    return 'general';
  }

  // Generate response using CNN-like pattern matching
  generateResponse(question) {
    const features = this.extractFeatures(question);
    const subjectData = this.knowledgeBase.get(features.subject);
    
    if (!subjectData) {
      return this.getDefaultResponse();
    }

    // Find best matching concepts
    const relevantConcepts = this.findRelevantConcepts(
      subjectData, 
      features.keywords
    );

    // Generate 7-8 line response
    return this.formatResponse(relevantConcepts, features.questionType);
  }

  findRelevantConcepts(subjectData, keywords) {
    const concepts = [];
    
    for (const [topicName, topicData] of Object.entries(subjectData.topics)) {
      for (const concept of topicData.concepts) {
        const relevanceScore = this.calculateRelevance(concept, keywords);
        if (relevanceScore > 0) {
          concepts.push({ concept, score: relevanceScore, topic: topicName });
        }
      }
    }

    return concepts.sort((a, b) => b.score - a.score).slice(0, 4);
  }

  calculateRelevance(concept, keywords) {
    const conceptWords = concept.toLowerCase().split(/\s+/);
    return keywords.filter(keyword => 
      conceptWords.some(word => word.includes(keyword) || keyword.includes(word))
    ).length;
  }

  formatResponse(concepts, questionType, keywords) {
    if (concepts.length === 0) {
      return this.getDefaultResponse();
    }

    const responseVariations = {
      definition: [
        "**Key Definition:**",
        "**Core Concept:**", 
        "**Essential Understanding:**",
        "**Fundamental Meaning:**"
      ],
      implementation: [
        "**Implementation Steps:**",
        "**How to Approach:**",
        "**Practical Method:**",
        "**Step-by-Step Guide:**"
      ],
      explanation: [
        "**Why This Matters:**",
        "**Key Benefits:**",
        "**Important Reasons:**",
        "**Core Advantages:**"
      ]
    };

    const examples = this.generateExamples(concepts[0]?.topic, keywords);
    const randomVariation = responseVariations[questionType] || responseVariations.definition;
    const header = randomVariation[Math.floor(Math.random() * randomVariation.length)];

    const bulletPoints = [];
    bulletPoints.push(header);
    
    // Add concepts as bullet points
    concepts.slice(0, 3).forEach(item => {
      bulletPoints.push(`• **${this.simplifyLanguage(item.concept)}**`);
    });

    // Add examples
    if (examples.length > 0) {
      bulletPoints.push(`\n**Examples:**`);
      examples.forEach(example => {
        bulletPoints.push(`• ${example}`);
      });
    }

    // Add practical tip
    const tips = this.generateTips(concepts[0]?.topic);
    if (tips.length > 0) {
      bulletPoints.push(`\n**💡 Pro Tip:** ${tips[Math.floor(Math.random() * tips.length)]}`);
    }

    return bulletPoints.join('\n');
  }

  generateExamples(topic, keywords) {
    const exampleBank = {
      testing_fundamentals: [
        "Login page validation testing",
        "Calculator app functionality testing", 
        "E-commerce checkout process testing",
        "Mobile app crash testing"
      ],
      programming_fundamentals: [
        "int age = 25; (integer variable)",
        "for(i=0; i<10; i++) (loop example)",
        "if(score > 90) print('A grade')",
        "function calculateArea(length, width)"
      ],
      os_fundamentals: [
        "Chrome browser as a process",
        "RAM allocation for running programs",
        "File explorer managing directories",
        "Task manager showing CPU usage"
      ],
      database_fundamentals: [
        "Student table with ID, Name, Grade",
        "SELECT * FROM students WHERE grade='A'",
        "Primary key: StudentID (unique)",
        "Foreign key: CourseID linking tables"
      ]
    };

    const examples = exampleBank[topic] || [];
    return examples.slice(0, 2); // Return 2 random examples
  }

  generateTips(topic) {
    const tipBank = {
      testing_fundamentals: [
        "Always test edge cases and boundary values",
        "Write test cases before coding (TDD approach)",
        "Test both positive and negative scenarios"
      ],
      programming_fundamentals: [
        "Use meaningful variable names for better code readability",
        "Practice coding daily to build muscle memory",
        "Debug step-by-step using print statements"
      ],
      os_fundamentals: [
        "Use Task Manager to understand process behavior",
        "Practice command line for better OS understanding",
        "Monitor system resources while running programs"
      ],
      database_fundamentals: [
        "Always backup your database before major changes",
        "Use indexes on frequently queried columns",
        "Normalize tables to reduce data redundancy"
      ]
    };

    return tipBank[topic] || ["Practice regularly to master the concepts"];
  }

  simplifyLanguage(concept) {
    return concept
      .replace(/process of evaluating and verifying/g, "checking if software works correctly")
      .replace(/organized collection of structured information/g, "organized way to store data")
      .replace(/step-by-step procedures for solving computational problems/g, "step-by-step instructions to solve problems")
      .replace(/manages computer hardware and provides services/g, "controls computer and helps programs run")
      .replace(/contiguous memory/g, "connected memory spaces")
      .replace(/hierarchical organization/g, "tree-like structure");
  }

  getDefaultResponse() {
    const responses = [
      "**I'm here to help!**\n• Ask me about specific programming concepts\n• Try questions like 'What is a loop?' or 'Explain databases'\n• I can provide examples and simple explanations\n\n**💡 Pro Tip:** Be specific in your questions for better answers!",
      "**Let's learn together!**\n• I specialize in 4 subjects: Programming, Testing, OS, and Databases\n• Ask for definitions, examples, or explanations\n• I'll provide bullet points and practical examples\n\n**💡 Pro Tip:** Try asking 'Give me an example of...' for practical insights!"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  }

  // Learning function to improve responses
  learnFromFeedback(question, response, feedback) {
    // Store feedback for future improvements
    const learningData = {
      question,
      response,
      feedback,
      timestamp: new Date().toISOString()
    };
    
    // In a real implementation, this would update the model
    console.log('Learning from feedback:', learningData);
  }
}

export const cnnAIService = new CNNAIService();