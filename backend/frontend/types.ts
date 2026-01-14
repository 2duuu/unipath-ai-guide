// TypeScript type definitions for UniHub API

export interface Question {
  id: string;
  question: string;
  type: 'choice' | 'multiple_choice' | 'text' | 'number' | 'range';
  field: string;
  options?: string[];
  descriptions?: Record<string, string>;
  min?: number;
  max?: number;
  step?: number;
}

export interface Answer {
  question_id: string;
  answer: string | number | string[] | boolean;
}

export interface UniversityMatch {
  university_name: string;
  location: string;
  match_score: number;
  match_type: 'safety' | 'target' | 'reach';
  reasoning: string;
  tuition_annual: number;
  acceptance_rate: number;
  strong_programs: string[];
  size: string;
  description: string;
}

export interface ProgramMatch {
  program_id: number;
  program_name: string;
  university_name: string;
  university_location: string;
  degree_level: string;
  duration_years: number;
  language: string;
  tuition_annual: number;
  match_score: number;
  match_type: 'safety' | 'target' | 'reach';
  reasoning: string;
  strength_rating: number | null;
  field: string;
}

export type Match = UniversityMatch | ProgramMatch;

export interface QuestionResponse {
  questions: Question[];
}

export interface MatchResponse {
  profile_id: number;
  match_type: 'university' | 'program';
  matches: Match[];
}

export interface FeedbackRequest {
  profile_id: number;
  rating: number;
  helpful: boolean;
  comments?: string;
}

export interface FeedbackResponse {
  status: 'success' | 'error';
  message: string;
}

export interface StatsResponse {
  total_profiles: number;
  total_feedback: number;
}

// API Client class
export class UniHubAPI {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async getInitialQuestions(): Promise<QuestionResponse> {
    const response = await fetch(`${this.baseUrl}/api/questions/initial`);
    if (!response.ok) throw new Error('Failed to fetch questions');
    return response.json();
  }

  async submitInitialQuiz(answers: Answer[]): Promise<MatchResponse> {
    const response = await fetch(`${this.baseUrl}/api/submit/initial`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    });
    if (!response.ok) throw new Error('Failed to submit quiz');
    return response.json();
  }

  async getExtendedQuestions(profileId: number): Promise<QuestionResponse> {
    const response = await fetch(`${this.baseUrl}/api/questions/extended?profile_id=${profileId}`);
    if (!response.ok) throw new Error('Failed to fetch extended questions');
    return response.json();
  }

  async submitExtendedQuiz(profileId: number, answers: Answer[]): Promise<MatchResponse> {
    const response = await fetch(`${this.baseUrl}/api/submit/extended`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile_id: profileId, answers })
    });
    if (!response.ok) throw new Error('Failed to submit extended quiz');
    return response.json();
  }

  async submitFeedback(feedback: FeedbackRequest): Promise<FeedbackResponse> {
    const response = await fetch(`${this.baseUrl}/api/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedback)
    });
    if (!response.ok) throw new Error('Failed to submit feedback');
    return response.json();
  }

  async getStats(): Promise<StatsResponse> {
    const response = await fetch(`${this.baseUrl}/api/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
}

// Helper function to check if match is a program match
export function isProgramMatch(match: Match): match is ProgramMatch {
  return 'program_name' in match;
}

// Helper function to check if match is a university match
export function isUniversityMatch(match: Match): match is UniversityMatch {
  return 'university_name' in match && !('program_name' in match);
}
