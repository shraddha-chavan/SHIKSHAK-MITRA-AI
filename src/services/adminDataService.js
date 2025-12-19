class AdminDataService {
  constructor() {
    this.baseUrl = 'http://localhost:3001';
  }

  async getTeacherPerformance() {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/teachers`);
      return await response.json();
    } catch (error) {
      return this.getMockTeacherData();
    }
  }

  async getLiveMonitoring() {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/live-classes`);
      return await response.json();
    } catch (error) {
      return this.getMockLiveData();
    }
  }

  async getTeacherComparison() {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/comparison`);
      return await response.json();
    } catch (error) {
      return this.getMockComparisonData();
    }
  }

  async getIndustryAlignment() {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/industry`);
      return await response.json();
    } catch (error) {
      return this.getMockIndustryData();
    }
  }

  async getDashboardSummary() {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/summary`);
      return await response.json();
    } catch (error) {
      return this.getMockSummaryData();
    }
  }

  getMockTeacherData() {
    return [
      { teacher_id: "T001", teacher_name: "Dr. Sarah Smith", subject: "Mathematics", overall_engagement: 87, teacher_effectiveness: 89, student_feedback_rating: 4.3 },
      { teacher_id: "T002", teacher_name: "Prof. John Wilson", subject: "Science", overall_engagement: 82, teacher_effectiveness: 85, student_feedback_rating: 4.1 },
      { teacher_id: "T003", teacher_name: "Ms. Emily Davis", subject: "English", overall_engagement: 91, teacher_effectiveness: 92, student_feedback_rating: 4.6 },
      { teacher_id: "T004", teacher_name: "Mr. Michael Brown", subject: "History", overall_engagement: 78, teacher_effectiveness: 81, student_feedback_rating: 3.9 },
      { teacher_id: "T005", teacher_name: "Dr. Lisa Johnson", subject: "Physics", overall_engagement: 85, teacher_effectiveness: 88, student_feedback_rating: 4.2 }
    ];
  }

  getMockLiveData() {
    return [
      { class_id: "CLS_001", teacher_name: "Dr. Sarah Smith", subject: "Mathematics", current_engagement: 85, student_count: 30, status: "Live" },
      { class_id: "CLS_002", teacher_name: "Prof. John Wilson", subject: "Science", current_engagement: 78, student_count: 28, status: "Live" },
      { class_id: "CLS_003", teacher_name: "Ms. Emily Davis", subject: "English", current_engagement: 92, student_count: 32, status: "Live" }
    ];
  }

  getMockComparisonData() {
    return [
      { teacher_name: "Dr. Sarah Smith", engagement_avg: 87, effectiveness_score: 89, benchmark_rank: 2 },
      { teacher_name: "Ms. Emily Davis", engagement_avg: 91, effectiveness_score: 92, benchmark_rank: 1 },
      { teacher_name: "Prof. John Wilson", engagement_avg: 82, effectiveness_score: 85, benchmark_rank: 3 }
    ];
  }

  getMockIndustryData() {
    return [
      { teacher_name: "Dr. Sarah Smith", subject: "Mathematics", alignment_score: 88, primary_industry: "Data Science" },
      { teacher_name: "Prof. John Wilson", subject: "Science", alignment_score: 85, primary_industry: "Healthcare" },
      { teacher_name: "Ms. Emily Davis", subject: "English", alignment_score: 90, primary_industry: "Media" }
    ];
  }

  getMockSummaryData() {
    return {
      total_teachers: 8,
      active_classes: 5,
      avg_engagement: 84.2,
      avg_effectiveness: 86.1,
      top_performer: "Ms. Emily Davis",
      total_students: 2340
    };
  }
}

export const adminDataService = new AdminDataService();