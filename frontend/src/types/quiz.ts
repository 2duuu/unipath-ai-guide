/**
 * TypeScript types for UniHub Quiz and API integration
 */

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
  answer: any;
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
  strength_rating: number;
  field: string;
}

export type Match = UniversityMatch | ProgramMatch;

export interface InitialQuizResponse {
  questions: Question[];
}

export interface InitialSubmitRequest {
  answers: Answer[];
}

export interface InitialSubmitResponse {
  profile_id: number;
  match_type: 'university';
  matches: UniversityMatch[];
}

export interface ExtendedQuizResponse {
  questions: Question[];
}

export interface ExtendedSubmitRequest {
  profile_id: number;
  answers: Answer[];
}

export interface ExtendedSubmitResponse {
  profile_id: number;
  match_type: 'program';
  matches: ProgramMatch[];
}

export interface FeedbackRequest {
  profile_id: number;
  rating: number;
  helpful: boolean;
  comments?: string;
}

export interface FeedbackResponse {
  status: string;
  message: string;
}

export interface StatsResponse {
  total_profiles: number;
  total_feedback: number;
}
