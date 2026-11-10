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

/** A quiz answer: one option ID, several option IDs, a number, or free text. */
export type AnswerValue = string | number | string[];

export interface Answer {
  question_id: string;
  answer: AnswerValue;
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

/** Shapes returned by the account endpoints in backend/app/api/routes/quiz.py. */
export interface QuizResultRecord {
  id: number;
  quiz_type: string;
  main_match_field: string;
  compatibility_score: number;
  description: string;
  matched_universities: string[];
  matched_programs: string[] | null;
  created_at: string;
}

export interface QuizResultsResponse {
  quiz_results: QuizResultRecord[];
}

export interface QuizAttemptRecord {
  id: number;
  quiz_label: string;
  quiz_type: string;
  num_questions: number;
  main_match: string;
  score_percentage: number;
  matched_universities: string[];
  created_at: string;
}

export interface QuizAttemptsResponse {
  quiz_attempts: QuizAttemptRecord[];
}

/** Body of POST /api/quiz/save-attempt (SaveQuizAttemptRequest in the backend). */
export interface SaveQuizAttemptRequest {
  user_id: number;
  quiz_type: 'initial' | 'extended';
  num_questions: number;
  main_match: string;
  score_percentage: number;
  matched_universities: string[];
  quiz_answers: Record<string, AnswerValue>;
}

export interface SaveQuizAttemptResponse {
  success: boolean;
  message: string;
  attempt_id: number;
}
